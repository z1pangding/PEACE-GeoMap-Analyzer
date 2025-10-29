import os
os.sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
from utils import common
import random

class landcover_type_api:
    def __init__(self):
        # define the landcover type (mock data)
        self.landcover_class_names = {
            10: "Trees",
            20: "Shrubland",
            30: "Grassland",
            40: "Cropland",
            50: "Built-up",
            60: "Bare / Sparse Vegetation",
            70: "Snow and Ice",
            80: "Permanent Water Bodies",
            90: "Herbaceous Wetland",
            95: "Mangroves",
            100: "Moss and Lichen"
        }

    def get_landcover_distribution(self, min_lon, min_lat, max_lon, max_lat, scale=100):
        """
        模拟获取土地覆盖分布数据
        基于给定的地理区域返回模拟的土地覆盖类型分布
        """
        # 模拟基于地理位置的土地覆盖分布
        # 这里使用随机生成的数据作为示例，实际应用中可以有更复杂的逻辑
        mock_data = {
            "Trees": round(random.uniform(10, 40), 3),
            "Grassland": round(random.uniform(5, 25), 3),
            "Cropland": round(random.uniform(15, 35), 3),
            "Built-up": round(random.uniform(5, 15), 3),
            "Permanent Water Bodies": round(random.uniform(2, 10), 3),
            "Bare / Sparse Vegetation": round(random.uniform(5, 20), 3)
        }
        
        # 确保总和接近100%
        total = sum(mock_data.values())
        if total > 0:
            # 调整最后一项以确保总和为100%
            keys = list(mock_data.keys())
            last_key = keys[-1]
            adjustment = 100.0 - sum(mock_data.values())
            mock_data[last_key] = round(mock_data[last_key] + adjustment, 3)
        
        landcover_distribution = mock_data
        return landcover_distribution

if __name__ == "__main__":
    min_lon = 108.00#E
    max_lon = 109.00#E
    min_lat = 19.33#N
    max_lat = 20.00#N
    landcover_type_api = landcover_type_api()
    print(landcover_type_api.get_landcover_distribution(min_lon, min_lat, max_lon, max_lat))
