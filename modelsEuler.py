#Создадим класс пространственная точка

class Space_point():
    def __init__(self,x1,x2,v1,v2):
        self.x1 = x1
        self.x2 = x2
        self.v1 = v1
        self.v2 = v2
# Создадим класс пространственная сетка
class Space_mesh():
    def __init__(self,x11,x12,x21,x22,meshpoints):
        self.x11 = x11
        self.x12 = x12
        self.x21 = x21
        self.x22 = x22
        self.meshpoints = meshpoints




