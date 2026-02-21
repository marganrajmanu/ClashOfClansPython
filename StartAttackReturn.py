from OCR import ocr
from TrOCR import money
from time import sleep
from ahk import AHK
from pydirectinput import click
from record_data import record
from datetime import datetime

ahk = AHK(version='v2')
ahk.run_script("CoordMode 'Mouse', 'Screen'")

class StartAttackReturn:
    ATTACK_ONE =          [200,  1400, 400,  1480]
    FIND_A_MATCH =        [517,  1018, 681,  1075]
    ATTACK_TWO =          [2040, 1220, 2330, 1290]
    ADD_REINFORCEMENT =   [1955, 1111, 2135, 1187]
    ADD_REINFORCEMENT_ADD=[1505, 949,  1787, 1042]
    NEXT =                [2271, 1193, 2458, 1262]
    RETURN_HOME =         [1158, 1271, 1504, 1349]
    OKAY =                [1460,  915, 1570, 1000]
    TRY_RELOAD =          [787,  641,  1866, 933 ]
    END_BATTLE =          [190, 1277,  420,  1330]
    
    MIN_LOOT = 460000

    def tryReoladWindow(self):
        foundT, xT, yT = ocr("try", StartAttackReturn.TRY_RELOAD)
        foundR, xR, yR = ocr("reload", StartAttackReturn.TRY_RELOAD)
        if foundT:
            click(888, 888)
            sleep(5)
        elif foundR:
            click(xR, yR)
            sleep(5)

    def pressOkay(self):
        for i in range(10):
            sleep(0.5)
            found, x, y = ocr("okay", xy=StartAttackReturn.OKAY)
            if found:
                click(x, y)
                return

    def addReinforcement(self):
        reinforcement_added = False
        sleep(0.5)
        found, x, y = ocr("free", StartAttackReturn.ADD_REINFORCEMENT)
        if found:
            click(2028, 1148)
            for i in range(5):
                sleep(1)
                found, x, y = ocr("convfirm", StartAttackReturn.ADD_REINFORCEMENT_ADD, confidence=0.3)
                if found:
                    click(x, y)
                    reinforcement_added = True
                    break
        click(2100, 1000)
        sleep(0.2)
        return reinforcement_added

    def attackOne(self):
        count = 0
        while True:
            sleep(0.5)
            found, x, y = ocr("attackl", xy=StartAttackReturn.ATTACK_ONE)
            if found:
                click(x, y)
                break
            if count == 20:
                self.pressOkay()
                self.tryReoladWindow()
                self.start()
                return
            count += 1
    
    def findMatch(self):
        count = 0
        while True:
            sleep(0.5)
            found, x, y = ocr("match", xy=StartAttackReturn.FIND_A_MATCH)
            if found:
                click(x, y)
                break
            if count == 20:
                self.pressOkay()
                self.tryReoladWindow()
                self.start()
                return
            count += 1
    
    def attackTwo(self):
        count = 0
        while True:
            sleep(0.5)
            found, x, y = ocr("attackl", xy=StartAttackReturn.ATTACK_TWO, confidence=0.4)
            if found:
                click(x, y)
                break
            if count == 20:
                self.tryReoladWindow()
                self.start()
                return
            count += 1
            sleep(0.5)
    
    def start(self):
        self.attackOne()
        self.findMatch()
        reinforcement_added = self.addReinforcement()
        self.attackTwo()
        return reinforcement_added

    def returnHomeCheck(self):
        sleep(0.5)
        found, x, y = ocr("RetuRn Home", xy=StartAttackReturn.RETURN_HOME, confidence=0.1)
        if found:
            return [found, x, y]
        else:
            return [found, x, y]
    def returnHome(self):
        for i in range(420):
            found, x, y = self.returnHomeCheck()
            if found:
                click(x, y)
                sleep(0.5)
                return datetime.now()
        self.tryReoladWindow()
        return datetime.now()
        
    def checkLoot(self, amount=False):
        m = money()
        moneyG = m.gold(villageGold=False)
        moneyX = m.elixier(villageElixier=False)
        if moneyG > StartAttackReturn.MIN_LOOT or moneyX > StartAttackReturn.MIN_LOOT:
            return [moneyG, moneyX] if amount else True
        else:
            return False 

    def endWaitCheck(self):
        count = 0
        while True:
            found, x, y = ocr("next", xy=StartAttackReturn.NEXT)
            if found:
                if self.checkLoot():
                    return True
                else:
                    click(x, y)
                    sleep(1)
                    return False
            if count == 150:
                self.tryReoladWindow()
                self.start()
                self.endWaitCheck()
                return False
            count += 1
            sleep(0.5)

    def endBattle(self):
        sleep(0.5)
        found, x, y = ocr("end battle", xy=StartAttackReturn.END_BATTLE, confidence=0.1)
        if found:
            click(300, 1300)
        sleep(1)
        found, x, y = ocr("okay", xy=StartAttackReturn.OKAY, confidence=0.1)
        if found:
            click(1500, 950)
        return       

class Attack:
    @staticmethod
    def troopDeploy():
        for i in range(10):
            if i % 3 == 1:
                click(1720, 320)
            elif i % 3 == 2:
                click(1750, 347)
            else:
                click(1780, 380)
            sleep(0.05)

    @staticmethod
    def attack(reinforcement_added):
        start = datetime.now()
        sleep(0.5)
        ahk.key_press('2')
        sleep(0.1)
        click(1330, 69)
        sleep(0.1)
        ahk.key_press('1')
        sleep(0.1)
        click(1330, 69)
        sleep(0.1)

        ahk.key_press('2')
        sleep(0.1)
        click(2270, 775)
        sleep(0.1)
        ahk.key_press('1')
        sleep(0.1)
        click(2270, 775)
        sleep(0.1)

        sleep(10)
        ahk.key_press('2')
        sleep(0.1)
        click(1750, 347)
        sleep(0.05)
        click(1750, 347)
        sleep(0.1)
        ahk.key_press('1')
        sleep(0.1)
        Attack.troopDeploy()
        sleep(0.1)

        ahk.key_press('z')
        sleep(0.1)
        click(1750, 347)
        sleep(0.1)

        ahk.key_press('r')
        sleep(0.1)
        click(1750, 347)
        sleep(0.1)
        ahk.key_press('e')
        sleep(0.1)
        click(1750, 347)
        sleep(0.1)
        ahk.key_press('w')
        sleep(0.1)
        click(1750, 347)
        sleep(0.1)
        ahk.key_press('q')
        sleep(0.1)
        click(1750, 347)
        sleep(0.1)

        sleep(1)
        ahk.key_press('a')
        sleep(10)
        click(1610, 673)
        sleep(0.1)
        click(1286, 493)
        sleep(4.25)

        if reinforcement_added:
            ahk.key_press('d')
            click(1567, 723)
            sleep(0.1)
            click(1244, 556)
            sleep(1)

        ahk.key_press('e')
        sleep(0.1)

        ahk.key_press('a')
        sleep(5.25)

        click(1308, 689)

        sleep(5)
        ahk.key_press('r')
        sleep(5.5)
        ahk.key_press('a')
        sleep(0.1)
        click(1352, 925)
        sleep(0.1)
        click(1092, 703)
        sleep(0.1)

        ahk.key_press('e')
        sleep(0.1)
        ahk.key_press('w')
        sleep(0.1)
        ahk.key_press('q')
        sleep(6)

        ahk.key_press('s')
        sleep(0.1)
        click(1143, 895)
        sleep(0.1)
        ahk.key_press('d')
        sleep(2)
        click(1143, 895)
        sleep(2.5)
        return start

class COC:
    @staticmethod
    def coc():
        sar = StartAttackReturn()  # create instance
        reinforcement_added = sar.start()
        while not sar.endWaitCheck():
            pass
        [moneyG, moneyX] = sar.checkLoot(amount=True)
        sleep(0.5)
        att = Attack()
        start_time = att.attack(reinforcement_added)
        end = False
        while not end:
            m = money()
            gold_loot_left = m.gold(villageGold=False)
            elixier_loot_left = m.elixier(villageElixier=False)
            if gold_loot_left <= 30000 and elixier_loot_left <= 30000:
                sar.endBattle()
                end = True
                break
            sleep(3)
        end_time = sar.returnHome()
        return {
            "Total Loot Gold": moneyG,
            "Total Loot Elixier": moneyX,
            "Attack start time": start_time,
            "Attack end time": end_time,
            "Total attack duration" : end_time - start_time,
            "Battle ended" : end
        }