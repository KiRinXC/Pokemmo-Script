import pyautogui
from MouseMove import MouseMove
from utili import adjust_window

from PokeOS import CatchFlash

if __name__ == '__main__':
    window = adjust_window()
    mouse = MouseMove()
    pyautogui.moveTo(mouse.win_p[0]+5, mouse.win_p[1]+5)
    pyautogui.click()
    CF = CatchFlash("闪光")
    CF.run()




