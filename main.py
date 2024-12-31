import time
from BattleProcess import BattleProcess
from utili import adjust_window
from CharacterMove import CharacterMove

from utili import mouse_position

# mouse_position()d
if __name__ == '__main__':
    battle = BattleProcess()
    character = CharacterMove()
    window = adjust_window()
    while window:
        sec = battle.is_battle(window)
        if not sec:
            character.RandomMove(3)
        else:
            time.sleep(sec)
    else:
        print("找不到窗口")




