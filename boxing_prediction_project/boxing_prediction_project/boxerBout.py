class BoxerBout:
    def __init__(self):
        self.name = None
        self.age = None
        self.stance = None
        self.height = None
        self.reach = None
        self.recordWon = None
        self.recordLost = None
        self.recordDraw = None
        self.__boutNumber = None
        self.recordKOs = None
    
    def refreshBoutNumber(self):
        self.__boutNumber = self.recordWon + self.recordLost + self.recordDraw