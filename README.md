# P1 (`P1.py`):

**Para hacer esta pregunta, fueron utilizadas las librerías `numpy` y el módulo auxiliar propio `Aux_Func` (que se encarga de cargar, guardar y medir las imágenes).**

Se definieron las siguientes funciones:

1. *padding*: Recibe como argumento el array de la imagen, el modo de padding y el tamaño objetivo `L` (un entero que corresponde al lado deseado de la imagen tras el relleno). Si el modo es `None`, retorna una copia de la imagen sin modificar junto a la tupla `(0, L, L, 0)`. En otro caso, calcula cuántos píxeles faltan en cada eje restando el tamaño de la imagen a `L` (usando `max(0, ...)` para no obtener valores negativos) y los reparte entre ambos lados: la mitad (división entera) arriba y a la izquierda, y el resto abajo y a la derecha. Luego utiliza la función `numpy.pad()` según el modo: `"zero"` rellena con ceros (`mode="constant"`), `"period"` usa `mode="reflect"` y `"edge"` repite el valor del borde. Si el modo no es ninguno de los anteriores, levanta un **ValueError**. Retorna la imagen con padding y la tupla `(arriba, derecha, abajo, izquierda)` con el tamaño de cada borde agregado.
2. *aplicar_fft*: Recibe como argumento el array de la imagen. Para hacerlo, utiliza `numpy.fft.fft2()` para obtener su transformada de Fourier y luego `numpy.fft.fftshift()` para llevar el origen de frecuencias al centro del espectro. Retorna la transformada centrada.
3. *crear_coords*: Recibe como argumento el espectro (la imagen en Fourier). Obtiene sus dimensiones con la función `obtener_tamaño_imagen` de `Aux_Func`, luego crea dos vectores con `numpy.arange()` que van desde `-tamaño // 2` hasta `tamaño // 2` (uno para cada eje) y los combina con `numpy.meshgrid()`. Retorna las matrices de coordenadas `U` (en x) y `V` (en y), con el origen al centro del espectro.
4. *calculo_distancias*: Recibe como argumento un punto `(u_0, v_0)` y las matrices de coordenadas `U` y `V`. Aprovechando la simetría del espectro, calcula dos distancias euclidianas píxel a píxel: una hasta el punto `(u_0, v_0)` y otra hasta su simétrico `(-u_0, -v_0)`. Retorna ambas matrices de distancia.
5. *obtener_H*: Recibe como argumento la lista de puntos a eliminar, las matrices `U` y `V`, el radio de eliminación y el tipo de notch (`1` para corte limpio, `2` para Gaussiano). Si el notch no es 1 ni 2, levanta un **ValueError**. Parte con una matriz `H` de unos del tamaño del espectro y, para cada punto, llama a *calculo_distancias* y multiplica `H` por el filtro correspondiente (para ambas distancias):

   - Notch `1`: se multiplica por la máscara booleana que vale 1 donde la distancia es mayor al radio y 0 en el resto, es decir, se corta un círculo limpio.
   - Notch `2`: se multiplica por 1 menos una exponencial negativa, que depende del cuadrado de la distancia dividido por el doble del cuadrado del radio. De esta forma, el corte baja de manera suave alrededor del punto.

   Retorna la matriz `H`.
6. *aplicar_H*: Recibe como argumento el espectro `F` y la matriz `H`. Retorna el producto punto a punto `G = F * H` (que en el dominio espacial equivale a una convolución).
7. *regresar_a_espacio*: Recibe como argumento la matriz `G`. Aplica `numpy.fft.ifftshift()` para deshacer el centrado, luego `numpy.fft.ifft2()` para volver al dominio espacial y finalmente `numpy.real()` para quedarse solo con la parte real. Retorna la imagen espacial con padding (`g_padded`).
8. *unpadding*: Recibe como argumento la imagen espacial, la tupla de bordes y el modo de padding. Recorta los bordes agregados por *padding* usando slicing simple, luego escala la imagen por 255, la limita entre 0 y 255 con `numpy.clip()` y la convierte a `uint8`. Si el modo es `None`, no recorta y solo hace el escalamiento y la conversión. Retorna la imagen con el tamaño original.
9. *proceso_completo*: Recibe como argumento el radio, el notch, el nombre de la imagen, un booleano `guardar_todo`, el tamaño objetivo del padding, la lista de puntos, el nombre del experimento (por defecto `None`) y el modo de padding (por defecto `"period"`). Encadena todas las funciones anteriores: carga la imagen con `cargar_imagen` de `Aux_Func`, luego aplica *padding*, *aplicar_fft*, *crear_coords*, *obtener_H*, *aplicar_H*, *regresar_a_espacio* y finalmente *unpadding*. Si `guardar_todo` es `True`, guarda con `Aux_Func.guardar` las siguientes imágenes dentro de la carpeta del experimento:

   - `imagen_ruido.jpg`: la imagen original.
   - `trans_pre.jpg`: el espectro antes del filtro.
   - `mascara.jpg`: la máscara `H`.
   - `trans_post.jpg`: el espectro después del filtro.
   - `sin_ruido.jpg`: la imagen final.

   Retorna la imagen final `g`, a la que ya se le quitó el ruido y se le realizó el recorte. Al final de la función se deja comentado un segmento que imprime los valores de `F`, `H` y `G` en una coordenada del espectro (usado para la quinta pregunta).

## Uso de `P1.py`:

Se puede ejecutar el archivo directamente.

Al final del archivo (desde la línea XX) se encuentran los parámetros modificables del archivo, siendo estos `r`, `notch`, `imagen`, `guardar_todo`, `experimento`, `lista_puntos` y `L`.

`r` es el radio de los círculos cortados en *obtener_H*, como entero. Ejemplo: `100`.

`notch` es un entero: `1` para cortes limpios y `2` para notch Gaussiano. Cualquier otro valor (por ejemplo `3`) levantará un error.

`imagen` debe ser un string con el nombre del archivo con su extensión, por ejemplo: `"P1.CR2"`.

`guardar_todo` es un booleano. Si es `True`, se guardan las imágenes intermedias del proceso (ver *proceso_completo*).

`experimento` es un string con el nombre de la carpeta donde se guardarán los resultados. Ejemplo: `"testP1"`.

`lista_puntos` son los puntos del espectro (respecto al centro) donde se ven los picos de ruido. Es **necesario** que sea una lista y que dicha lista contenga tuplas de formato `(u_i, v_i)`. Ejemplo: `[(1400, 0), (1540, 0), (1680, 0)]`. Cada punto elimina también su simétrico.

`L` es el tamaño objetivo del padding, como entero. Ejemplo: `4096`.

# P1_exp (`P1_exp.py`):

**Para hacer esta pregunta, fueron utilizadas las librerías `numpy` y `os`, además del módulo auxiliar `Aux_Func` y la función `proceso_completo` de `P1.py`.**

Este archivo no define el procesamiento en sí, sino los experimentos que se hicieron sobre `P1.py` para elegir los parámetros del filtro. Se definieron las siguientes funciones:

1. *exp1*: No recibe argumentos. Ejecuta *proceso_completo* con `r = 50`, notch Gaussiano (`2`), `L = 4096` y cinco puntos sobre el eje horizontal del espectro, partiendo desde `(1094, 0)` y avanzando de a 260 píxeles. Guarda todas las imágenes intermedias en la carpeta `1/identificar_componentes`. Sirve para identificar visualmente las componentes del ruido.
2. *exp2*: Recibe como argumento una tupla de radios `rs` y una tupla de notchs `notchs`. Para cada notch, y luego para cada radio, ejecuta *proceso_completo* con los mismos cinco puntos de *exp1* y guarda todo en la carpeta `2/notch_<notch>/r_<r>`. Después calcula la diferencia absoluta entre la imagen original (escalada por 255) y la imagen filtrada, y la guarda como `diferencia_notch_<notch>_r_<r>.jpg`. Si algún notch no es 1 ni 2, se interrumpe el recorrido (por eso se puede pasar un `0` al final de la tupla de notchs para evitar repetir el notch). Se utilizó de forma iterativa para buscar el radio óptimo, y los pasos quedaron comentados en el archivo:

   - Para el notch Gaussiano, se probó primero con `(1, 10, 50, 100)`, luego `(20, 30, 40)` y finalmente de 35 a 45. El resultado fue `punto_dulce_2 = 38`.
   - Para el notch limpio, se probó con `(60, 70)` y luego de 45 a 55. El resultado fue `r_dulce_1 = 46`.
3. *comparar_ideales*: No recibe argumentos. Ejecuta *proceso_completo* para el notch limpio con `r = 46` y para el Gaussiano con `r = 38` (sin guardar las intermedias). Luego calcula la diferencia absoluta entre ambas imágenes resultantes y la guarda como `diferencia_ideal_vs_gauss.jpg` en la carpeta `2/comparacion_puntos_dulces`.
4. *exp3*: No recibe argumentos. Estudia el efecto del padding: para cada notch (con su radio óptimo, `46` para el limpio y `38` para el Gaussiano), para cada modo de padding (`None` y `"period"`) y para cada tamaño `L` en `(2256, 4096, 8192)`, ejecuta *proceso_completo* guardando todo en la carpeta `3/notch_<notch>/<modo>/<L>`.
5. *comparar_padding*: No recibe argumentos. Ejecuta *proceso_completo* con notch Gaussiano, `r = 38` y `L = 4096`, usando padding `"zero"` y luego `"period"`. Después calcula la diferencia absoluta entre ambos resultados (convertida a `uint8`) y la guarda como `zero_vs_period.jpg` en la carpeta `3/comparacion_padding`.
6. *exp4*: No recibe argumentos. Ejecuta *proceso_completo* con notch Gaussiano, `r = 38`, `L = 4096` y padding `"period"`. Luego calcula la diferencia absoluta entre la imagen original (escalada por 255) y la final (convertida a `uint8`) y la guarda como `og_vs_final.jpg` en la carpeta `4`. Finalmente, imprime un mensaje de confirmación.

## Uso de `P1_exp.py`:

Para ejecutarlo, `P1.py`, `Aux_Func.py` y la imagen de prueba (`P1.CR2`) **deben** estar en la misma carpeta que `P1_exp.py`.

Al final de cada experimento (y de las búsquedas del radio) se encuentra su llamada, **comentada** con `#`. Para correr un experimento en particular basta con descomentar su llamada. Actualmente, la única llamada activa es `exp4()`, por lo que ejecutar el archivo directamente corre solo ese experimento.

Los parámetros de cada experimento están definidos dentro de su función (`r`, `notch`, `L`, `imagen`, `lista_puntos`), excepto en *exp2*, que recibe `rs` y `notchs` como argumentos. Ejemplo: `exp2((35, 36, 37), (2, 0))` probará los radios 35, 36 y 37 solo para el notch Gaussiano.

`lista_puntos` es la misma en todos los experimentos: `[(1094, 0), (1094 + 260*1, 0), ..., (1094 + 260*4, 0)]`. Si se cambia la imagen de prueba, **debe** modificarse en cada función.

Los resultados se guardan en carpetas con el nombre del experimento (`1`, `2`, `3` y `4`), según lo definido en `Aux_Func.guardar`.
