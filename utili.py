import pyautogui
import pygetwindow
import json

from PIL import Image, ImageDraw


def adjust_window():
    '''
    调整窗口并激活
    '''
    with open('./Data/config.json', 'r', encoding='utf-8') as data:
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
    with open("./Data/config.json", "w", encoding='utf-8') as data:
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
            window.resizeTo(win_w, win_h)
            window.moveTo(win_p_x, win_p_y)
            return window
    return False


def screenshot(window,path="window_screenshot.png"):
    '''
    游戏窗口屏幕截图
    :param window: 游戏窗口
    :param path: 存放路径
    :return:
    '''
    left, top, width, height = window.left, window.top, window.width, window.height
    # 截图窗口区域
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # 保存截图
    screenshot.save(path)



def window_markup(offset, path="window_screenshot.png"):
    '''
    对图片的元素划定范围
    :param offset: 指定区域
    :param path: 图片存放路径
    '''
    # 打开图像
    image = Image.open(path)
    # 创建一个绘图对象
    draw = ImageDraw.Draw(image)

    # 定义矩形框的左上角和右下角坐标
    left, top, right, bottom = offset[0], offset[1], offset[2], offset[3]  # 这里的坐标需要根据实际屏幕长度宽度调整

    # 在图像上绘制矩形框
    draw.rectangle(((left, top), (right, bottom)), outline="red", width=1)

    # 保存绘制了矩形框的图像
    image.save("window_markup.png")
