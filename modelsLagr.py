#Создадим обьект материальная точка
class MaterialPoint():
    def __init__(self, X1, X2, x1, x2,v1,v2,T1,T2):
        self.X1 = X1
        self.X2 = X2
        self.x1 = x1
        self.x2 = x2
        self.v1 = v1
        self.v2 = v2
        self.T1 = T1
        self.T2 = T2


#оздадим обьект Материальное тело, который потом будет содержать в себе материальные точки
class MaterialBody():
    def __init__(self, X1, X2, points,Points):
        self.X1 = X1
        self.X2 = X2
        self.points = points
        self.Points = Points
