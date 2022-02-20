from models import MaterialBody
from models import MaterialPoint
from models import Space_mesh
from models import Space_point
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
#Эйлеров подход
# Получим поле скоростей
def get_velfield (x11,x12,x21,x22,meshpoints,t):
    Mesh = Space_mesh(x11,x12,x21,x22,meshpoints)
    Points_space = []
    X1 = []
    X2 = []
    x1 = x11
    x2 = x21
    for i in range (0,meshpoints):
        X1.append(x1)
        x1 = x1 + abs((x11 - x12)/meshpoints)
        X2.append(x2)
        x2 = x2 + abs((x21 - x22) / meshpoints)
    print (X1,X2)


    def f1(x,t):
        f = -x * t**2
        return f

    def f2(x,t):
        f = -x**3*t
        return f
    for i in range (0,len(X1)):
        for j in range (0,len(X1)):
            P = Space_point(X1[i],X2[j],f1(X1[i],t),f2(X2[j],t))
            Points_space.append(P)
    return Points_space, Mesh

# Движение сковозь пространство
def Move_through_space():
    # функции для скорости
    def f1(x,t):
        f = -x * t**2
        return f

    def f2(x,t):
        try:
            f = -x**3*t
        except Exception:
            f = 0*x*t
        return f

    # параметры сетки
    x11 = -10
    x12 = 0
    x21 = 0
    x22 = 10
    meshpoints = 10
    steps = 100
    lines = 10
    tfl = 1.5
# количество временных точе
    ntp = 3
    plt.figure()
    # постороим линии тока
    for h in range (1,2*ntp + 1,2):
        t =  (tfl)/ntp*h
        SP, Mesh = get_velfield(x11, x12, x21, x22,meshpoints, t)
        L1 = {}
        L2 = {}

        for j in range(0, lines):
            X1l = []
            X2l = []
            x1 = x11
            x2 = x21 + abs(x22 - x21) / lines * j
            for i in range(0, steps):
                X1l.append(x1)
                X2l.append(x2)

                x2 += f2(x2, t) / f1(x1, t)*abs(x12 - x11) / steps
                x1 += abs(x12 - x11) / steps
                # print (x2)
            L1.update({'L1+' + str(j): X1l})
            L2.update({'L1+' + str(j): X2l})
        n1 = []
        n2 = []
        x1 = x11
        x2 = x21
        for i in range(0, meshpoints):
            n1.append(x1)
            x1 = x1 + abs((x11 - x12) / meshpoints)
            n2.append(x2)
            x2 = x2 + abs((x21 - x21) / meshpoints)


        plt.subplot(2, ntp, h,aspect = 'equal')
        plt.title('t = ' + str(t))
        plt.ylim(ymin=0, ymax=10, auto=False)
        plt.xlim(xmin=-10, xmax=0, auto=False)
        # посторим поле скоростей
        for i in SP:
            print (i.x2)
            plt.quiver(i.x1, i.x2,i.v1,i.v2, color='black')

            x, y = np.meshgrid(n1, n2)

        plt.plot(x, y)

        segs1 = np.stack((x, y), axis=2)
        segs2 = segs1.transpose(1, 0, 2)
        plt.gca().add_collection(LineCollection(segs1))
        plt.gca().add_collection(LineCollection(segs2))

        plt.subplot(2, ntp, h + 1,aspect = 'equal')
        plt.title('t = ' + str(t))
        for n in L1.keys():
            plt.ylim(ymin=0, ymax=10, auto=False)
            plt.xlim(xmin=-10, xmax=0, auto=False)
            plt.plot(L1[n], L2[n])

#Лагранжев подход
# Функция для интегратора


def integrator (steps,y0,x0,xf,f):
    step = (xf - x0)/steps
    Yd = {'y 0': y0}
    x = x0
    X = [x]
    for i in range (1,steps):
        x = x + step
        X.append(x)
        yn = Yd['y ' + str(i - 1)]
        y = yn + step*1/6*f(x)*yn
        y = y + step*4/6*f(x + 1/2*step)*(yn + 1/2*step*f(x)*f(x)*yn)
        y = y + step * 1 / 6 * f(x + step)*(yn -1*step*f(x)*(f(x + 1/2*step)*(yn + 1/2*step*f(x)*f(x)*yn)) + 2*step*f(x)*(f(x + 1/2*step)*(yn + 1/2*step*f(x)*f(x)*yn)))

        Yd.update({'y ' + str(i):y})
    Y = []
    for i in Yd.keys():
        Y.append(Yd[i])
    return Y,X
# Функция для получения траектории
def get_trajectory(steps,t0,tf,X1,X2):
    def f1(x):
        f =  -(x**2)
        return f
    def f2(x):
        f = -x**3
        return f

    x1,T = integrator(steps,X1,t0,tf,f1)
    x2,T = integrator(steps,X2,t0,tf,f2)
    x1f = x1[len(x1)-1]
    x2f = x1[len(x2)-1]
    v1 = f1(x1f)
    v2 = f2(x2f)
    return  x1,x2,v1,v2,x1f,x2f
# функция для создания тела
def create_body():
    def get_Materialpoints(points,C1,C2):
        def f1(x):
            f = -1.0* x**2
            return f
        def f2(x):
            f = x
            return f
        Points = []
        for prt in range(1, 3):
            for prt2 in range(1, 3):
                for i in range(0, points):
                    for j in range(0, points):
                        A1 = C1 + (-1)**prt * 2 / points * i
                        A2 = C2 + (-1)**(prt2) * 2 / points * j
                        if (A1 - C1) ** 2 + (A2 - C2) ** 2 <= 4 and (A1 - C1) ** 2 + (A2 - C2) ** 2 >= 3:
                            v2 = f2(A2)
                            v1 = f1(A2)
                            M = MaterialPoint(A1, A2, A1, A2,v1,v2,[],[])
                            Points.append(M)
            for prt in range(0, 2):
                for prt2 in range(0, 2):
                    for i in range(0, points):
                        for j in range(0, points):
                            A1 = C1 + (-1) ** prt * 2 / points * i
                            A2 = C2 + (-1) ** (prt2) * 2 / points * j
                            if (A1 - C1) ** 2 + (A2 - C2) ** 2 <= 4 and (A1 - C1) ** 2 + (A2 - C2) ** 2 >= 3:
                                v2 = f2(A2)
                                v1 = f1(A2)
                                M = MaterialPoint(A1, A2, A1, A2, v1, v2, [], [])
                                Points.append(M)

            return Points
    Body = MaterialBody( -2,2,10,get_Materialpoints(10,-2,2))

    return Body

# движение материального тела

def move_material_body (Body):
    def f1(x):
        f =  -1.0 * (x**2)
        return f
    def f2(x):
        f = x
        return f
    for i in Body.Points:
        T1, T2, x1, x2, v1, v2 = get_trajectory(100,0,2,i.X1,i.X2)
        i.x1 = x1
        i.x2 = x2
        i.v1 = v1
        i.v2 = v2
        i.T1 = T1
        i.T2 = T2

        OX1 = np.zeros(1000)
        OY1 = np.linspace(-10, 10, 1000)
        OY2 = np.zeros(1000)
        OX2 = np.linspace(-10, 10, 1000)
        plt.Figure(figsize=(2, 2))
        plt.ylim(ymin=-10, ymax=10, auto=False)
        plt.xlim(xmin=-10, xmax=10, auto=False)


        for i in Body.Points:

            plt.scatter(i.X1, i.X2)

            plt.plot(i.T1, i.T2)

        plt.plot(OX1, OY1, c='y')
        plt.plot(OX2, OY2, c='y')


    return Body