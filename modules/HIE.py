import os
os.sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
import cv2
import json
import collections
from tool_pool import geological_knwoledge_type
from utils import api, prompt, vision, common
from agents import geologist_agent

class hierarchical_information_extraction:
    def __init__(self):
        self.geologist = geologist_agent()

    def digitalize(self, image_path, progress_callback=None):
        if progress_callback:
            progress_callback("📊 [HIE] 正在加载图像文件...")
        
        image = cv2.imread(image_path)
        name = common.path2name(image_path)
        meta_path = os.path.join(common.cache_path(), "meta", name + ".json")
        
        if progress_callback:
            progress_callback("📊 [HIE] 检查缓存文件...")
            
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.loads(f.read())
            if progress_callback:
                progress_callback("✅ [HIE] 从缓存加载完成")
            return meta

        if progress_callback:
            progress_callback("📊 [HIE] 初始化元数据结构...")
            
        # get headers of geologic map.
        meta = dict()
        meta["date"] = common.today_date()
        meta["name"] = name
        meta["version"] = "v1.0"
        meta["source"] = common.dataset_source
        meta["size"] = {"width": image.shape[1], "height": image.shape[0]}
        meta["regions"] = dict()
        meta["legend"] = dict()
        meta["information"] = dict()
        meta["faults"] = None

        if progress_callback:
            progress_callback("📊 [HIE] 正在分析地图布局结构...")
            
        # get layout of geologic map.
        map_layout = self.geologist.get_map_layout(image_path)
        regions = map_layout["regions"]
        meta["regions"] = regions

        if progress_callback:
            progress_callback("📊 [HIE] 正在裁剪和保存地图组件...")
            
        # crop each component in geologic map.
        region_path_and_bbox = collections.defaultdict(list)
        for region_name, region_bndboxes in regions.items():
            if progress_callback:
                progress_callback(f"📊 [HIE] 处理组件: {region_name}")
                
            for i, region_bndbox in enumerate(region_bndboxes):
                region_path = os.path.join(common.cache_path(), "det", name, f"{region_name}_{i}.png")
                common.create_folder_by_file_path(region_path)
                vision.crop_and_save_image(image, region_bndbox, region_path)
                region_path_and_bbox[region_name].append((region_path, region_bndbox))

                if "main_map" == region_name:
                    # crop latitude and longitude region of geologic map.
                    lonlat_name = "lonlat"
                    lonlat_region_path = os.path.join(common.cache_path(), "det", name, f"{lonlat_name}_{i}.png")
                    common.create_folder_by_file_path(lonlat_region_path)
                    vision.crop_corners_and_save_image(region_path, lonlat_region_path)
                    region_path_and_bbox[lonlat_name].append((lonlat_region_path, None))
                elif "index_map" == region_name:
                    # extend index map and add vision prompt.
                    vision.annotate_image_with_directions(region_path, region_path)

        if len(region_path_and_bbox["legend"]) > 0:
            if progress_callback:
                progress_callback("📊 [HIE] 正在提取图例信息...")
                
            legend_path, legend_bndbox = region_path_and_bbox["legend"][0]
            legend_metadata = self.geologist.get_legend_metadata(legend_path, legend_bndbox)
            legends = legend_metadata["legend"]
            
            if progress_callback:
                progress_callback("📊 [HIE] 正在匹配岩石类型和地层年代...")
                
            for legend in legends.values():
                legend["lithology"] = self.geologist.get_knowledge(geological_knwoledge_type.Rock_Type, legend["text"])["rock_type"]
                legend["stratigraphic_age"] = self.geologist.get_knowledge(geological_knwoledge_type.Rock_Age, legend["text"])["rock_age"]
            meta["legend"] = legends

        if progress_callback:
            progress_callback("📊 [HIE] 正在提取基本信息（标题、比例尺等）...")
            
        # get basic information of geologic map.
        region_names = ["title", "scale", "lonlat", "index_map"]
        for region_name in region_names:
            if region_name not in region_path_and_bbox:
                continue
            if progress_callback:
                progress_callback(f"📊 [HIE] 分析{region_name}信息...")
                
            region_path, region_bndbox = region_path_and_bbox[region_name][0]
            keys, instruction = prompt.get_component_instruction(region_name)
            prompt_content = [
                {"type": "image_url", "image_url": {"url": api.local_image_to_data_url(region_path)}},
                {"type": "text", "text": instruction},
            ]
            messages = [
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt_content},
            ]

            answer = api.answer_wrapper(messages, structured=True)
            infos = eval(answer)
            key_value_pairs = prompt.get_basic_information(region_name, infos)
            for key, value in key_value_pairs:
                meta["information"][key] = value

        if len(region_path_and_bbox["main_map"]) > 0:
            if progress_callback:
                progress_callback("📊 [HIE] 正在进行岩石区域分割...")
                
            main_map_path, main_map_bndbox = region_path_and_bbox["main_map"][0]
            vision.rock_region_seg(main_map_path, list(meta["legend"].values()))

        if progress_callback:
            progress_callback("📊 [HIE] 正在保存数字化结果...")
            
        # output digitalization result of geologic map.
        common.create_folder_by_file_path(meta_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(meta, indent=4, ensure_ascii=False))
            
        if progress_callback:
            progress_callback("✅ [HIE] 分层信息提取完成")
            
        return meta


if __name__ == "__main__":
    image_path = "sample.jpg"
    hie = hierarchical_information_extraction()
    meta = hie.digitalize(image_path)
    print(meta)
