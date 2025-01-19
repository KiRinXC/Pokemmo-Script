import json

import cv2
import numpy as np
import pyautogui
import pygetwindow


def adjust_window():
    '''
    调整窗口并激活
    '''
    with open('config/RegMouse.json', 'r', encoding='utf-8') as data:
        config = json.load(data)
    # 获取屏幕尺寸并添加至config中
    scr_x, scr_y = pyautogui.size()
    config["scr_size"] = [scr_x, scr_y]

    # 获取设定的缩放游戏窗口大小
    win_w, win_h = config["win_size"][0], config["win_size"][1]

    # 确定游戏界面的左上角起始坐标 并添加至config
    win_p_x, win_p_y = scr_x - win_w, 0
    config["win_reg"]["data"] = [win_p_x, win_p_y, win_p_x + win_w, win_p_y + win_h]

    # 更新config
    with open("config/RegMouse.json", "w", encoding='utf-8') as data:
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
        if title_trans == "PokeMMO":
            # 激活窗口并调整大小和位置
            window.activate()
            window.resizeTo(win_w, win_h)
            window.moveTo(win_p_x, win_p_y)
            return window
    return False


def capture(offset,is_save=False,is_ocr = True):
    with open("config/RegMouse.json", "r", encoding='utf-8') as f:
        Region = json.load(f)
        origin = Region['win_reg']['data']
    left = origin[0] + offset[0]
    top = origin[1] + offset[1]
    width = offset[2]
    height = offset[3]
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # 变成灰度图像
    grayscale_image = screenshot.convert('L')
    if is_ocr: # 如果待识别的对象是白色的，则需要变成二值图像增加识别的精度
        binary_image = grayscale_image.point(lambda x: 0 if x < 245 else 255, '1').convert('RGB')
    else: # 如果待识别图像不是白色，则转换成RGB图像
        binary_image = grayscale_image.convert('RGB')

    # 保存处理后的图片
    if is_save:
        binary_image.save('test.png')
    return np.array(binary_image)


def img_match(template_path, offset,is_save=False,is_ocr = True,confidence = 0.05):
    with open("config/RegMouse.json", "r", encoding='utf-8') as f:
        Region = json.load(f)
        origin = Region['win_reg']['data']
    left = origin[0] + offset[0]
    top = origin[1] + offset[1]
    width = offset[2]
    height = offset[3]
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # 变成灰度图像
    grayscale_image = screenshot.convert('L')
    if is_ocr: # 如果待识别的对象是白色的，则需要变成二值图像增加识别的精度
        binary_image = grayscale_image.point(lambda x: 0 if x < 245 else 255, '1').convert('RGB')
    else: # 如果待识别图像不是白色，则转换成RGB图像
        binary_image = grayscale_image.convert('RGB')

    # 保存处理后的图片
    if is_save:
        binary_image.save('test.png')

    # 截取逃跑框中的信息
    img_1 = np.array(binary_image)
    # 读取模板中的逃跑框
    img_2 = cv2.imread(template_path)
    # print(img_1.shape,img_2.shape)
    # 计算MSE损失
    mse = np.mean((img_1 - img_2) ** 2)
    if is_save:
        print(mse)
    if mse > confidence:
        return False
    else:
        return True


# img_match('template/B_ico.png', [812,656,7,8], True, is_ocr=False)
# img_match('template/escape_txt.png', [574,635,15,17], True, is_ocr=True)