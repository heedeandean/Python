class MYSU:
    def __init__(self, Su):
        self.Su=Su
    def __lt__(self, Su):
        print("self .Su < other.Su")
    def __gt__(self, Su):
        print("self .Su > other.Su")
    