#Лагранжев подход
#Создадим обьект материальная точка
class MaterialPoint():
    def __init__(self, X1, X2, x1, x2,v1,v2,T1,T2):
        self.X1 = X1
        self.X2 = X2
        self.x1 = x1
        self.x2 = x2
        self.v1 = v1
        self.v2 = v2
        #Траектории
        self.T1 = T1
        self.T2 = T2


#оздадим обьект Материальное тело, который потом будет содержать в себе материальные точки
class MaterialBody():
    def __init__(self, X1, X2, points,Points):
        #Координаты центра тела
        self.X1 = X1
        self.X2 = X2
        #Количество точек в теле
        self.points = points
        #Массив с материальными точками
        self.Points = Points

#Эйлеров подход
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