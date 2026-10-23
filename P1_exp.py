from P1 import proceso_completo
import Aux_Func as aux
import numpy as np


def exp1():
    r = 50  # Radio de los círculos cortados en obtener_H
    notch = 2  # 1 para cortes limpios. 2 para notch Gaussiano
    imagen = "P1.CR2"  # imagen de prueba entregada con la tarea
    guardar_todo = True
    experimento = "1_identificar_componentes"

    # Puntos con fallos visibles en el espectro de Fourier
    lista_puntos = [
        (-306, -306), (306, -306), (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]

    L = 4096  # Tamaño objetivo del padding

    g = proceso_completo(r, notch, imagen, guardar_todo,
                         L, lista_puntos, experimento)
    return


# exp1()


def exp2(rs: tuple):
    notches = (1, 2)
    for notch in notches:
        for r in rs:
            print(f"Empezando {str(r)}")
            imagen = "P1.CR2"
            guardar_todo = True
            experimento = f"2_notch_{str(notch)}_comparar_r_{str(r)}_"

            # Puntos con fallos visibles en el espectro de Fourier
            lista_puntos = [
                (-306, -306), (306, -306), (1094, 0), (1094+260*1, 0),
                (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
            ]

            L = 4096  # Tamaño objetivo del padding

            g = proceso_completo(r, notch, imagen, guardar_todo,
                                 L, lista_puntos, experimento)

            array_imagen = aux.cargar_imagen(imagen)
            diferencia = np.abs(
                (array_imagen * 255).astype(float) - g.astype(float))
            aux.guardar(
                diferencia, False, f"diferencia_notch_{str(notch)}_r_{str(r)}.jpg", experimento)
    return


exp2(rs=(1, 10, 50, 100))
