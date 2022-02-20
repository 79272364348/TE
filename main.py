#импорт модулей
import matplotlib.pyplot as plt# для отрисовки графиков
import managersLagr as ML#вызовем написанные модули
import managersEul as ME#
#Создадим материальное тело
a = ML.create_body()
#двигаем материальное тело
b = ML.move_material_body(a)
#Движение в пространстве
d = ME.Move_through_space()


