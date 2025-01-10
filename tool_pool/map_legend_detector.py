import os
os.sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
import cv2
from dependencies.ultralytics import YOLOv10

class map_legend_detector:
    def __init__(self, model_path="./dependencies/models/det_legend/weights/best.pt"):
        self.model = YOLOv10(model_path)

    def overlap(self, anchor_col, bndbox):
        x0, y0, x1, y1 = bndbox
        x = (x0 + x1) / 2
        return anchor_col[0] < x < anchor_col[1]

    def bndboxes_tabulation(self, color_bndboxes, width):
        cols = []
        visited = [False] * len(color_bndboxes)
        
        # Group bounding boxes into columns
        while True:
            anchor_col = None
            for i, color_bndbox in enumerate(color_bndboxes):
                if visited[i]:
                    continue
                if anchor_col is None:
                    anchor_col = (color_bndbox[0], color_bndbox[2])
                    visited[i] = True
                elif self.overlap(anchor_col, color_bndbox):
                    visited[i] = True
            if anchor_col is not None:
                cols.append(anchor_col)
            else:
                break
        
        # Sort columns and add the rightmost boundary
        cols = sorted(cols, key=lambda col: col[0])
        cols.append((width, width))
        
        # Assign bounding boxes to text regions
        text_bndboxes = []
        for color_bndbox in color_bndboxes:
            x0, y0, x1, y1 = color_bndbox
            anchor_idx = -1
            for idx, col in enumerate(cols):
                if self.overlap(col, color_bndbox):
                    anchor_idx = idx
                    break
            if anchor_idx == -1:
                continue
            x0, x1 = cols[anchor_idx][1], cols[anchor_idx + 1][0]
            if x0 >= x1:
                continue
            if y0 >= y1:
                continue
            text_bndbox = (x0, y0, x1, y1)
            text_bndboxes.append(text_bndbox)
        
        return text_bndboxes

    def distance(self, color_bndbox, text_bndbox):
        c_x0, c_y0, c_x1, c_y1 = color_bndbox
        t_x0, t_y0, t_x1, t_y1 = text_bndbox
        c_x = c_x1
        c_y = (c_y0 + c_y1) / 2
        t_x = t_x0
        t_y = (t_y0 + t_y1) / 2
        return ((c_x - t_x) ** 2 + (c_y - t_y) ** 2) ** 0.5
    
    def shrink_bndbox(self, image, bndbox):
        x0, y0, x1, y1 = bndbox
        image = image[y0:y1, x0:x1]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        s = gray.min(axis=0)

        thred = 32
        width = s.shape[0]
        dx0 = int(width * 0.01)
        while dx0 < s.shape[0]:
            if s[dx0] < 256 - thred:
                break
            dx0 += 1
        dx1 = int(width * 0.99) - 1
        while dx1 > dx0:
            if s[dx1] < 256 - thred:
                break
            dx1 -= 1
        x1 = x0 + dx1 + 1
        x0 = x0 + dx0 - 1

        bndbox = (x0, y0, x1, y1)
        return bndbox

    def detect(self, image_path):
        objs = self.model.predict(source=image_path)[0]
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        color_bndboxes = objs["color_bndbox"]
        #text_bndboxes = self.bndboxes_tabulation(color_bndboxes, width)# debug
        text_bndboxes = objs["text_bndbox"]

        legends = dict()
        idx = 0
        for color_bndbox in color_bndboxes:
            thred = color_bndbox[3] - color_bndbox[1]
            paired_text_bndbox = None
            min_dist = float("inf")
            for text_bndbox in text_bndboxes:
                dist = self.distance(color_bndbox, text_bndbox)
                if min_dist > dist:
                    min_dist = dist
                    paired_text_bndbox = text_bndbox
            if paired_text_bndbox is None or min_dist > thred:
                continue
            text_bndboxes.remove(paired_text_bndbox)
            paired_text_bndbox = self.shrink_bndbox(image, paired_text_bndbox)
            legends[idx] = {
                "color_bndbox": color_bndbox,
                "text_bndbox": paired_text_bndbox,
                "color": [0, 0, 0],
                "color_name": "",
                "text": "",
                "area": 0,
            }
            idx += 1

        return legends


if __name__ == "__main__":
    map_legend_detector = map_legend_detector()
    print(map_legend_detector.detect("sample.jpg"))
