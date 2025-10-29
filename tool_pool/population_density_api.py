import os
os.sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/..")
from utils import common
import random

class population_density_api:
    def __init__(self):
        pass

    def get_population_density(self, min_lon, min_lat, max_lon, max_lat, scale=100):
        """
        模拟获取人口密度数据
        基于给定的地理区域返回模拟的人口密度
        """
        # 计算区域面积 (平方千米)
        area_km2 = abs(max_lon - min_lon) * abs(max_lat - min_lat) * 111 * 111  # 粗略计算
        
        # 模拟人口密度计算，基于地理位置的一些假设
        # 例如，靠近赤道或城市地区人口密度可能更高
        base_density = random.uniform(50, 200)  # 基础人口密度
        
        # 根据纬度调整人口密度（通常低纬度地区人口更密集）
        lat_factor = 1.0 + (90 - abs((min_lat + max_lat) / 2)) / 90 * 0.5
        density = base_density * lat_factor
        
        # 根据区域面积进行调整
        population_density = round(density, 2)
        population_density_str = f"{population_density} people/km^2"
        
        return population_density_str

if __name__ == "__main__":
    min_lon = 108.00#E
    max_lon = 109.00#E
    min_lat = 19.33#N
    max_lat = 20.00#N
    population_density_api = population_density_api()
    print(population_density_api.get_population_density(min_lon, min_lat, max_lon, max_lat))
