import json

from utili import whiter
from GenerateRandom import GenerateRandom


class DetectBattle:
    def __init__(self):
        with open("config/RegWhite.json", "r", encoding='utf-8') as f:
            RegWhite = json.load(f)
            self.nick_name = RegWhite['nick_name']

    def is_battle(self):
        return not whiter(self.nick_name, is_save=False)

#
# bd = DetectBattle()
# # s =time.time()
# # print(bd.is_battle())a
# # e= time.time()
# # print(e-s)
# while True:
#     print(bd.is_battle())