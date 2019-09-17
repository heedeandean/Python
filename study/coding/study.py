class Doit:
    def __init__(self, temp = 0):
        self._temp = temp
    
    def to_value(self):
        return (self.temp * 1.8) + 32

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        self._temp = value

v = Doit()

for i in range(10, 15):
    v.temp = i
    print(str(v.to_value()))