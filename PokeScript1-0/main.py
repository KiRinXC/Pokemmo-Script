import datetime
import os
import time
import pyautogui

from MouseMove import MouseMove
from utili import adjust_window

from PokeOS import CatchFlash
from Encoder import Encoder
if __name__ == '__main__':
    is_run = 0
    Encoder = Encoder()
    date = str(datetime.date.today())
    print(">>" + str(Encoder.cpu_info) + "<<")
    if not os.path.exists(Encoder.path):
        # 文件不存在 ，则认为是首次运行
        password = Encoder.generate_key(date)
        a = input("请输入产品密钥:")
        if password == a:
            Encoder.store_key(date, password)
            is_run = 1
    else:
        # 文件存在，则直接验证是否相等
        if Encoder.verify_key():
            is_run = 1
    if is_run == 1:
        print("验证成功，正在启动......")
        window = adjust_window()
        mouse = MouseMove()
        pyautogui.moveTo(mouse.win_p[0] + 5, mouse.win_p[1] + 5)
        pyautogui.click()
        CF = CatchFlash("蘑菇")
        CF.run()
    else:
        print("验证失败，请联系【闲鱼】https://m.tb.cn/h.TQrD4j3?tk=l3kmeXpUvUA")
        time.sleep(100)






