from record_data import record
import StartAttackReturn
import pygetwindow as gw
from time import sleep
from wall_upgrade import WallUpgrade
from datetime import datetime

def CheckCocActive():
    window = gw.getActiveWindow()
    while True:
        if "Clash of Clans" in window.title:
            return True
        
def suru():
    sleep(1)
    # while CheckCocActive():
    for i in range(20):
        coc = StartAttackReturn.COC()
        data = coc.coc()
        data.update({
            "Attack Number" : i
        })
        record(data)
            # if i > 14:
            #     sleep(10)
            #     wu = WallUpgrade()
            #     wu.wall()
            #     break
            
    # sleep(10)
    # wu = WallUpgrade()
    # wu.wall()
        

a = StartAttackReturn.Attack()
def at():
    a.attack()
        
suru()
# at()