import time
from BattleProcess import BattleProcess
from utili import FindWindow
from CharacterMove import CharacterMove

from utili import mouse_position
# mouse_position()
if __name__ == '__main__':
    battle = BattleProcess()
    character = CharacterMove()
    window = FindWindow()
    while window:
        counter =battle.is_battle()
        if not counter:
            character.RandomMove()
        else:
            time.sleep(1.2*counter)
    else:
        print("找不到窗口")
