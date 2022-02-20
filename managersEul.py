from modelsEuler import Space_mesh
from modelsEuler import Space_point
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

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
        for j in range(0, lines):
            X1l = []
            X2l = []
            x1 = x11 + abs(x12 - x11) / lines * j
            if x21 != 0:
                x2 = x21
            else:
                x2 = x21 + 0.1

            for i in range(0, steps):
                X1l.append(x1)
                X2l.append(x2)
                try:
                    x2 += f2(x2, t) / f1(x1, t)*abs(x12 - x11) / steps
                    x1 += abs(x12 - x11) / steps
                except Exception:
                    pass
            L1.update({'L2+' + str(j): X1l})
            L2.update({'L2+' + str(j): X2l})
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
    plt.show()
