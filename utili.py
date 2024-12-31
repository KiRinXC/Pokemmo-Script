import time
from audioop import ratecv

import pyautogui
import pygetwindow
import json

from PIL import Image, ImageDraw


def adjust_window():
    with open('config.json', 'r') as data:
        config = json.load(data)
    # 获取屏幕尺寸并添加至config中
    scr_x,scr_y = pyautogui.size()
    config["scr_size"] = [scr_x, scr_y]

    # 获取设定的缩放游戏窗口大小
    win_w,win_h = config["win_size"][0],config["win_size"][1]

    # 确定游戏界面的左上角起始坐标 并添加至config
    win_p_x,win_p_y = scr_x-win_w,0
    config["win_position"] = [win_p_x,win_p_y]

    # 更新config
    with open("config.json", "w") as data:
        json.dump(config, data)
    # 获取当前所有已开启的窗口
    windows = pygetwindow.getAllWindows()
    # PokeMMO窗口名称使用了部分西里尔字母进行编码，需要转换成拉丁字母
    trans_table = str.maketrans({
            'Р': 'P',
            'М': 'M',
            'е': 'e',
            'о': 'o'
    })
    for window in windows:
        # 将窗口的字符转换后在进行比较
        title_trans = window.title.translate(trans_table)
        if title_trans == config['title']:
            # 激活窗口并调整大小和位置
            window.activate()
            window.resizeTo(win_w,win_h)
            window.moveTo(win_p_x, win_p_y)
            return window
    return False


def mouse_position():
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"当前鼠标位置：({x}, {y})")


def screenshot(window):
    left, top, width, height = window.left, window.top, window.width, window.height
    # 截图窗口区域
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # 保存截图
    screenshot.save('window_screenshot.png')
    return "window_screenshot.png"

def window_markup(path):
    # 打开图像
    image = Image.open(path)
    print(image.size)
    # 创建一个绘图对象
    draw = ImageDraw.Draw(image)
    # 定义矩形框的左上角和右下角坐标
    left, top, right, bottom = 470, 500, 630,610  # 这里的坐标需要根据实际屏幕长度宽度调整

    # 在图像上绘制矩形框
    draw.rectangle(((left, top), (right, bottom)), outline="red", width=1)

    # 保存绘制了矩形框的图像
    image.save("window_markup.png")

# window_markup("window_screenshot.png")
