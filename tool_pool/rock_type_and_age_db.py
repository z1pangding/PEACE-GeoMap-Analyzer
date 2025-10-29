import re
import json

class rock_type_and_age_db:
    def __init__(self, mode):
        self.rock_name2type = dict()
        db_path = f"./dependencies/knowledge/k2_rock_{mode}.json"
        with open(db_path, 'r', encoding='utf-8') as f:
            rock_types = json.loads(f.read())
        for rock_type in rock_types:
            rock_name = rock_type["rock_name"].lower()
            rock_type = rock_type[f"rock_value"].lower()
            self.rock_name2type[rock_name] = rock_type

    def clean_rock_name(self, name):
        black_list1 = ["脉", "?", ")", "member", "."]
        for key in black_list1:
            name = name.replace(key, "").strip()
        black_list2 = ["夹", "（", "。", ":"]
        for key in black_list2:
            if key in name:
                s = name.find(key)
                name = name[:s].strip()
        black_list3 = ["的", "色", "—"]
        for key in black_list3:
            if key in name:
                s = name.find(key)
                name = name[s+1:].strip()
        return name.strip()

    def rock_split(self, rock_name):
        keywords = [",", "、", "-", " and ", "和", "及", "或", "\n", "/", "("]
        pattern = '|'.join(map(re.escape, keywords))
        rock_name = rock_name.lower().strip()
        names = re.split(pattern, rock_name)
        names = list(map(lambda name: self.clean_rock_name(name.strip().strip(")")), names))
        names = list(filter(lambda name: len(name) > 0, names))
        return names

    def get_rock_type_or_age(self, rock_name):
        if rock_name is None:
            return "unknown"
    
        names = self.rock_split(rock_name)

        find_type = None
        for rock_name, rock_type in self.rock_name2type.items():
            for name in names:
                if name in rock_name or rock_name in name:
                    find_type = rock_type

        if find_type is None:
            find_type = "unknown"
        return find_type


if __name__ == "__main__":
    rock_name = "few"
    rock_type_and_age_db = rock_type_and_age_db(mode="type")
    rock_type = rock_type_and_age_db.get_rock_type_or_age(rock_name)
    print(rock_type)
