from record_data import record
import StartAttackReturn
import pygetwindow as gw
from time import sleep
from wall_upgrade import WallUpgrade as wu
from datetime import datetime

coc = StartAttackReturn.COC

def CheckCocActive():
    window = gw.getActiveWindow()
    while True:
        if "Clash of Clans" in window.title:
            return True
        
def suru():
    sleep(1)
    while CheckCocActive():
        for i in range(20):
            record({
                "date" : datetime.now(),
                "Attack Number" : i
            })
            coc.coc()
            
        wu.wallUpgrade()

        

a = StartAttackReturn.Attack
def at():
    a.attack()
        
suru()
# at()