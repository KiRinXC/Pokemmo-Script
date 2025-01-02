import threading
import time
import pyautogui
from BattleDetect import BattleDetect
from MouseMove import MouseMove
from utili import adjust_window
from CharacterMove import CharacterMove


# mouse_position()
if __name__ == '__main__':
    # 共享的标志变量，用于控制线程是否应该继续运行
    should_continue = True
    window = adjust_window()
    battle = BattleDetect()
    character = CharacterMove()
    mouse = MouseMove()
    pyautogui.moveTo(mouse.win_p[0]+5, mouse.win_p[1]+5)
    def quit_loop():
        global should_continue
        while should_continue:
            time.sleep(1)
            x, y = pyautogui.position()
            if x < mouse.win_reg[0] or y > mouse.win_reg[3]:
                print("程序终止")
                should_continue = False

    def battle_loop():
        global should_continue
        while should_continue:
            battle.is_battle()

    def character_loop():
        global should_continue
        while should_continue:
            character.RandomMove([3,5])

    # 创建线程
    thread1 = threading.Thread(target=quit_loop)  # 注意这里不需要括号
    thread2 = threading.Thread(target=battle_loop)  # 传递参数需要使用args
    thread3 = threading.Thread(target=character_loop)
    # 启动线程
    thread1.start()
    thread2.start()
    thread3.start()

    # 等待线程完成
    thread1.join()
    thread2.join()
    thread3.join()





