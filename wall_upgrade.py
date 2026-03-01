import EasyOCR
from pydirectinput import click, moveTo
from ahk import AHK
from time import sleep
from record_data import record
from TrOCR import money

ahk = AHK(version='v2')

class WallUpgrade:
    BUILDER_COOR = [1080, 222, 1164, 987]
    OKAY = [1388, 900, 1720, 1020]
    MAX_MONEY = 20001500
    WALL_COST = 4000000

    def __init__(self):
        m = money()
        self.gold = m.gold() or 0
        self.elixier = m.elixier() or 0

    def refresh(self):
        m = money()
        self.gold = m.gold() or 0
        self.elixier = m.elixier() or 0

    def checkUpgrade(self):
        return self.gold > 20000000 or self.elixier > 20000000

    def wallSearch(self):
        count = 0
        while True:
            found, x, y = EasyOCR.ocr("wall", WallUpgrade.BUILDER_COOR, relax=False)
            print(f"here {found}")
            if found:
                moveTo(x, y, duration=0.1)
                sleep(1)
                click()
                return True
            
            ahk.run_script(f"""
                Click "WheelDown"
                Sleep 1000
                Click "WheelDown"
                Sleep 1000
                Click "WheelDown"
                Sleep 3000
            """)

            count += 1
            if count == 20:
                return False

    def addWall(self, num):
        moveTo(1258, 1218)
        num -= 1
        sleep(0.2)
        click()
        for i in range(num):
            sleep(0.5)
            click()
        return

    def spendGold(self):
        num = self.gold // WallUpgrade.WALL_COST
        if num != 0:
            found = self.wallSearch()  # check if wall was found
            if not found:
                return
            self.addWall(num=num)
            click(1500, 1200)
            while True:
                found, x, y = EasyOCR.ocr("okay", WallUpgrade.OKAY)
                if found:
                    click(x, y)
                    sleep(0.5)
                    click(2500, 750)
                    return num

    def spendElixier(self):
        num = self.elixier // WallUpgrade.WALL_COST
        if num != 0:
            found = self.wallSearch()  # check if wall was found
            if not found:
                return
            self.addWall(num=num)
            click(1750, 1200)
            while True:
                found, x, y = EasyOCR.ocr("okay", WallUpgrade.OKAY)
                if found:
                    click(x, y)
                    sleep(0.5)
                    click(2500, 750)
                    return num

    def wall(self):
        while self.gold == 0 or self.elixier == 0:
            self.refresh()
        else:
            if self.gold >= self.MAX_MONEY or self.elixier >= self.MAX_MONEY:
                sleep(0.5)
                click(1322, 115)
                sleep(2)
                moveTo(1515, 590)
                sleep(1)
                self.wallSearch()
                sleep(1)
                x = self.spendGold()    # spendGold now calls wallSearch internally

                sleep(0.5)
                click(1322, 115)
                sleep(2)
                moveTo(1515, 590)
                sleep(1)
                self.wallSearch()
                sleep(1)
                x += self.spendElixier() # spendElixier now calls wallSearch internally
                record({
                    "Gold" : self.gold,
                    "Elixier" : self.elixier,
                    "Walls upgraded" : x
                })