import json
import os
from GenerateRandom import GenerateRandom
from utili import capture
import easyocr


class DetectTarget:
    def __init__(self, target):
        with open("./config/HealthBar.json", "r", encoding='utf-8') as f:
            HealthBar = json.load(f)
            self.one = HealthBar["1"]
            self.two = HealthBar["2"]
            self.three = HealthBar["3"]
            self.five = HealthBar["5"]
            self.target = target

        poke_recode = f"data/{self.target}.json"
        if not os.path.exists(poke_recode):
            # 然后再打开文件进行读取
            with open(poke_recode, 'w', encoding='utf-8') as f:
                json.dump({'poke_num': 0,
                           'target_num': 0}, f)
        with open(poke_recode, 'r', encoding='utf-8') as data:
            poke_recode = json.load(data)
            self.poke_num = poke_recode["poke_num"]
            self.target_num = poke_recode["target_num"]
        self.reader = easyocr.Reader(['ch_sim', 'en'])

    def one_detect(self):
        self.is_target = False
        img = capture(self.one)
        results = self.reader.readtext(img)

        text_list = [item[1] for item in results if item[1]]
        poke_info = ' '.join(text_list)
        if self.target in poke_info or "闪光" in poke_info:
            self.is_target = True
            self.target_num +=1
        self.poke_num+=1
        print(f"{self.poke_num} \t {self.target_num} \t {poke_info}")
        return self.is_target



    def two_detect(self):
        pass

    def three_detect(self):
        pass

    def five_detect(self):
        pass


# fd = DetectTarget("土")
# print(fd.one_detect())
