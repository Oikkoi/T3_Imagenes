from P1 import proceso_completo
import Aux_Func as aux
import numpy as np
import os


def exp1():
    r = 50  # Radio de los círculos cortados en obtener_H
    notch = 2  # 1 para cortes limpios. 2 para notch Gaussiano
    imagen = "P1.CR2"  # imagen de prueba entregada con la tarea
    guardar_todo = True
    experimento = os.path.join("1", "identificar_componentes")

    # Puntos con fallos visibles en el espectro de Fourier
    lista_puntos = [
        (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]

    L = 4096  # Tamaño objetivo del padding

    g = proceso_completo(r, notch, imagen, guardar_todo,
                         L, lista_puntos, experimento)
    return


# exp1()


def exp2(rs: tuple, notchs: tuple):
    for notch in notchs:
        if notch not in (1, 2):
            break
        for r in rs:
            print(f"Empezando {str(r)}")
            imagen = "P1.CR2"
            guardar_todo = True
            experimento = os.path.join(
                "2", f"notch_{str(notch)}",  f"r_{str(r)}")

            # Puntos con fallos visibles en el espectro de Fourier
            lista_puntos = [
                (1094, 0), (1094+260*1, 0),
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


# exp2(rs=(1, 10, 50, 100), notchs=(1, 2))

# En notch 2, 10 quita muy poco y 50 quita demasiado, como se ve en las figuras.
# Con esto, buscamos el 'punto dulce' de r

# exp2((20, 30, 40), notchs=(2, 0))

# Nuevamente, alrededor de 40 es que está en punto dulce.
# exp2((35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45), (2, 0))
punto_dulce_2 = 38

# repetimos para el notch 1
# exp2((60, 70), (1, 0))
# El punto dulce sigue alrededor de 50
# exp2((45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55), (1, 0))
r_dulce_1 = 46


def comparar_ideales():
    imagen = "P1.CR2"
    experimento = os.path.join("2", "comparacion_puntos_dulces")
    L = 4096
    lista_puntos = [
        (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]
    g_ideal = proceso_completo(
        46, 1, imagen, False, L, lista_puntos, experimento)

    g_gauss = proceso_completo(
        38, 2, imagen, False, L, lista_puntos, experimento)
    diferencia = np.abs(g_ideal.astype(float) - g_gauss.astype(float))
    aux.guardar(diferencia, False,
                "diferencia_ideal_vs_gauss.jpg", experimento)

# comparar_ideales()


def exp3():
    Ls = (2256, 4096, 8192)
    modos = (None, "period")
    imagen = "P1.CR2"
    lista_puntos = [
        (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]
    for notch in (1, 2):
        if notch == 1:
            r = 46
        else:
            r = 38
        for modo in modos:
            if modo == None:
                nombre = "None"
            else:
                nombre = modo
            for L in Ls:
                experimento = os.path.join(
                    "3", f"notch_{str(notch)}", nombre, str(L))
                proceso_completo(r, notch, imagen, True, L,
                                 lista_puntos, experimento, modo)


# exp3()


def comparar_padding():
    imagen = "P1.CR2"
    experimento = os.path.join("3", "comparacion_padding")
    L = 4096
    notch = 2
    r = 38

    lista_puntos = [
        (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]
    g_zero = proceso_completo(r, notch, imagen, False,
                              L, lista_puntos, experimento, modo_pad="zero")
    g_period = proceso_completo(
        r, notch, imagen, False, L, lista_puntos, experimento, modo_pad="period")
    diferencia = np.abs(g_zero.astype(float) -
                        g_period.astype(float)).astype(np.uint8)
    aux.guardar(diferencia, False, "zero_vs_period.jpg", experimento)
    return


# comparar_padding()

def exp4():
    imagen = "P1.CR2"
    experimento = "4"
    L = 4096
    notch = 2
    r = 38

    lista_puntos = [
        (1094, 0), (1094+260*1, 0),
        (1094+260*2, 0), (1094+260*3, 0), (1094+260*4, 0)
    ]

    g_ideal = proceso_completo(
        r, notch, imagen, False, L, lista_puntos, experimento, modo_pad="period")
    array_imagen_original = aux.cargar_imagen(imagen)

    diferencia = np.abs((array_imagen_original * 255).astype(float) -
                        g_ideal.astype(float)).astype(np.uint8)

    aux.guardar(diferencia, False, "og_vs_final.jpg", experimento)
    print("Listo. Imagen diferencia del exp4 guardada.")


exp4()
