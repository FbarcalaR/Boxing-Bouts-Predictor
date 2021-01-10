import boxerBout

class Bout:
    def __init__(self, id):
        self.id = id
        self.country = ""
        self.winner = None # -1 for A, 0 for draw, 1 for B
        self.boxerA = boxerBout.BoxerBout()
        self.boxerB = boxerBout.BoxerBout()

    def toString(self):
        result = self.id + ","
        result += str(self.country) + ","
        result += str(self.winner) + ","

        result += str(self.boxerA.name) + ","
        result += str(self.boxerA.age) + ","
        result += str(self.boxerA.stance) + ","
        result += str(self.boxerA.height) + ","
        result += str(self.boxerA.reach) + ","
        result += str(self.boxerA.recordWon) + ","
        result += str(self.boxerA.recordLost) + ","
        result += str(self.boxerA.recordDraw) + ","
        result += str(self.boxerA._BoxerBout__boutNumber) + ","
        result += str(self.boxerA.recordKOs) + ","

        result += str(self.boxerB.name) + ","
        result += str(self.boxerB.age) + ","
        result += str(self.boxerB.stance) + ","
        result += str(self.boxerB.height) + ","
        result += str(self.boxerB.reach) + ","
        result += str(self.boxerB.recordWon) + ","
        result += str(self.boxerB.recordLost) + ","
        result += str(self.boxerB.recordDraw) + ","
        result += str(self.boxerB._BoxerBout__boutNumber) + ","
        result += str(self.boxerB.recordKOs)

        return result
