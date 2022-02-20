#импорт модулей
import matplotlib.pyplot as plt# для отрисовки графиков
import managers as MN#вызовем написанные модули
#
#Создадим материальное тело
a = MN.create_body()
#двигаем материальное тело
b = MN.move_material_body(a)
#Движение в пространстве
d = MN.Move_through_space()
plt.show()

