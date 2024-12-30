from sys import flags

import cv2
import pyautogui

from PIL import Image
import pytesseract

from utili import img_match


class FlashDetect():
    def __init__(self):
        self.screen="./template/FlashDetect.png"
        self.template="./template/FlashDetect_template.png"

    def flashDetect(self,window):
        left, top, width, height = window.left, window.top, window.width, window.height
        # 截取当前窗口区域的截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 保存截图
        screenshot.save(self.screen)
        screenshot = cv2.imread(self.screen)
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(Image.open(self.screen))
        if '闪光' in text:
            print("检测到'闪光'字样")
        return 0

if __name__ == '__main__':
    img1= cv2.imread("./template/img.png")
    img2 = cv2.imread("./template/img_1.png")
    flag = img_match(img1, img2)
    print(flag)
