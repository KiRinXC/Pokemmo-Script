import time
import pyautogui
import pygetwindow
import json
with open('config.json', 'r') as file:
    config = json.load(file)
    # 电脑屏幕大小
    scr_h, scr_w = config["screen_size"][0], config["screen_size"][1]
    # 窗口坐标原点
    win_p_x,win_p_y=config["window_position"][0], config["window_position"][1]
    # 缩放后的窗口大小
    win_h, win_w = config["window_size"][0], config["window_size"][1]


def FindWindow():
    windows = pygetwindow.getAllWindows()
    trans_table = str.maketrans({
            'Р': 'P',
            'М': 'M',
            'е': 'e',
            'о': 'o'
    })
    for window in windows:
        title_trans = window.title.translate(trans_table)
        if title_trans == config['title']:
            # 调整窗口
            window.activate()
            window.resizeTo(win_h, win_w)
            window.moveTo(win_p_x, win_p_y)
            return window
    return False



# def img_match(screenshot,template):
#     # 读取模板图片的信息
#     height, width, channel = template.shape
#     # 进行模板匹配
#     result = cv2.matchTemplate(screenshot,template,cv2.TM_SQDIFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     if min_val < 0.2:
#         print("匹配位置:", min_loc)
#
#         # 获取模板的宽高
#         top_left = min_loc
#         bottom_right = (top_left[0] + width, top_left[1] + height)
#
#         # 在截图上绘制一个矩形框，表示最匹配的位置
#         cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)  # 绿色矩形框，线宽为2
#
#         # 保存结果图像
#         cv2.imwrite("./template/tag.png", screenshot)
#         return True
#     else:
#         return False

def mouse_position():
    time.sleep(3)
    x, y = pyautogui.position()
    print(f"当前鼠标位置：({x}, {y})")


