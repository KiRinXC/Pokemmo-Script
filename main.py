import time
from BattleProcess import BattleProcess
from utili import FindWindow
from CharacterMove import CharacterMove

if __name__ == '__main__':
    battle = BattleProcess()
    character = CharacterMove()
    window = FindWindow()
    while window:
        window.activate()
        character.RandomMove()
        flag=battle.battleDetect(window)
        if flag:
            print("进入对战")
            time.sleep(1000)
    else:
        print("找不到窗口")