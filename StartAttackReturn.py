from EasyOCR import ocr
from TrOCR import LootMoney
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
        found_try_again, xT, yT = ocr("try", StartAttackReturn.TRY_RELOAD)
        found_reload, xR, yR = ocr("reload", StartAttackReturn.TRY_RELOAD)
        if found_try_again:
            click(888, 888)
            sleep(5)
        elif found_reload:
            click(xR, yR)
            sleep(5)

    def pressOkay(self):
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
        found, x, y = ocr("attackl", xy=StartAttackReturn.ATTACK_ONE)
        if found:
            click(x, y)
        return found
    
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
        while not self.attackOne():
            sleep(0.5)
            self.tryReoladWindow()
            self.pressOkay()
        self.findMatch()
        reinforcement_added = self.addReinforcement()
        self.attackTwo()
        return reinforcement_added

    def returnHomeCheck(self):
        sleep(0.5)
        found, x, y = ocr("RetuRn Home", xy=StartAttackReturn.RETURN_HOME, confidence=0.1)
        if found:
            return [found, x, y]
        found, x, y = ocr("RetuRn Hore", xy=StartAttackReturn.RETURN_HOME, confidence=0.1)
        if found:
            return [found, x, y]
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
        
    def checkLoot(self):
        loot_money = LootMoney()
        total_gold_loot = loot_money.lootGold()
        total_elixier_loot = loot_money.lootElixier()
        if total_gold_loot > StartAttackReturn.MIN_LOOT or total_elixier_loot > StartAttackReturn.MIN_LOOT:
            return [True, total_gold_loot, total_elixier_loot]
        else:
            return [False, None, None] 

    def endWaitCheck(self):
        count = 0
        while True:
            found, x, y = ocr("next", xy=StartAttackReturn.NEXT)
            if found:
                approved, total_gold_loot, total_elixier_loot = self.checkLoot()
                if approved:
                    return [True, total_gold_loot, total_elixier_loot]
                else:
                    click(x, y)
                    sleep(1)
                    return [False, None, None] 
            if count == 150:
                self.tryReoladWindow()
                self.start()
                self.endWaitCheck()
                return [False, None, None] 
            count += 1
            sleep(0.5)

    def endBattle(self):
        sleep(0.2)
        found, x, y = ocr("end battle", xy=StartAttackReturn.END_BATTLE, confidence=0.1)
        if found:
            click(300, 1300)
        sleep(0.7)
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
        while not sar.endWaitCheck()[0]:
            pass
        [_, loot_gold, loot_elixier] = sar.checkLoot()
        sleep(0.5)
        att = Attack()
        attack_start_time = att.attack(reinforcement_added)
        end = False
        while True:
            m = LootMoney()
            gold_loot_left = m.lootGold()
            elixier_loot_left = m.lootElixier()
            if gold_loot_left <= 30000 and elixier_loot_left <= 30000:
                sar.endBattle()
                end = True
                break
            x = StartAttackReturn()
            if x.returnHomeCheck()[0]:
                break
            sleep(3)
        loot_money = LootMoney()
        loot_dark_elixier = loot_money.lootGold()
        looted_gold = loot_money.lootedGold()
        looted_elixier = loot_money.lootedElixier()
        looted_dark_elixier = loot_money.lootedDarkElixier()
        # bonus_gold = loot_money.bonusGold()
        # bonus_elixier = loot_money.bonusElixier()
        # bonus_dark_elixier = loot_money.bonusElixier()
        attack_end_time = sar.returnHome()
        return {
            "Total Loot Gold": loot_gold,
            "Total Loot Elixier": loot_elixier,
            "Total Loot Dark Elixier" : loot_dark_elixier,
            "Looted Gold" : looted_gold,
            "Looted Elixier" : looted_elixier,
            "Looted Dark Elixier" : looted_dark_elixier,
            # "Bonus Gold" : bonus_gold,
            # "Bonus Elixier" : bonus_elixier,
            # "Bonus Dark Elixier" : bonus_dark_elixier,
            "Attack start time": attack_start_time,
            "Attack end time": attack_end_time,
            "Total attack duration" : attack_end_time - attack_start_time,
            "Battle ended" : end
        }