# Práctica 1 – Hilos RicardoSiles

**Materia:** Sistemas Operativos – Ingeniería de Sistemas
**Estudiante:** Siles Rivero Ricardo Alexander
**Escenario:** Sistema de procesamiento de pedidos (24 documentos, 4 trabajadores concurrentes)

## Contenido del repositorio

| Archivo | Descripción |
| --- | --- |
| `hilos.py` | Programa con 4 hilos, cola compartida `queue.Queue` y `Lock` |
| `README.md` | Interpretación de cada trabajador y respuestas a las preguntas |

Ejecución: `python hilos.py` (Python 3, sin bibliotecas externas).

## Cómo funciona el programa

1. Se cargan en una `queue.Queue` 24 documentos, cada uno como tupla `(id, tamaño)` con tamaño aleatorio de 1 a 5.
2. Se crean 4 hilos (`Siles`, `Candia`, `Figueredo` y `Poma`) y se inician con `start()`.
3. Cada trabajador ejecuta un ciclo: intenta `get_nowait()`; si la cola está vacía se captura `queue.Empty` y el hilo termina de forma controlada.
4. El procesamiento se simula con `time.sleep(tamaño × 0.1)`.
5. El contador del trabajador y el registro detallado se actualizan dentro de `with lock:`.
6. El hilo principal espera a los cuatro con `join()` y muestra el total, el resumen por trabajador y las tres verificaciones.

## Asignación de los 24 documentos (ejemplo de una ejecución)

| Trabajador | Documentos procesados | Cantidad |
| --- | --- | --- |
| Siles | 1, 9, 13, 17, 20, 23 | 6 |
| Candia | 2, 6, 10, 14, 15, 18, 21, 24 | 8 |
| Figueredo | 3, 7, 11, 16, 22 | 5 |
| Poma | 4, 5, 8, 12, 19 | 5 |
| **Total** | | **24** |

## Interpretación de cada trabajador

- **Siles:** procesó 6 documentos (1, 9, 13, 17, 20 y 23) primero empezó con el documento 1 que era de tamaño 5 y después siguió agarrando documentos de la cola hasta que ya no quedaron.
- **Candia:** procesó 8 documentos (2, 6, 10, 14, 15, 18, 21 y 24) el que más hizo porque le tocaron varios documentos de tamaño 1 (el 6, 14, 15 y 21), que se procesan rápido entonces volvía a la cola más veces que los demás.
- **Figueredo:** procesó 5 documentos (3, 7, 11, 16 y 22) el tuvo documentos de tamaño 3 y 5 por eso fue un poco más lento que el de Candia.
- **Poma:** procesó 5 documentos (4, 5, 8, 12 y 19). Le tocaron dos documentos de tamaño 5 (el 12 y el 19) que son los más pesados y por eso hizo menos.

El reparto no fue parejo (8, 6, 5 y 5) pero está bien porque ningún trabajador tenía documentos asignados desde antes. Cada uno agarraba el siguiente apenas se desocupaba entonces el que terminaba más rápido hacía más. La suma da 24, ningún documento se repitio y ninguno se perdio.

## Verificaciones

1. La suma de documentos por trabajador es 24.
2. Cada ID aparece una sola vez en el registro detallado.
3. Los cuatro hilos finalizan sin quedarse bloqueados (`is_alive()` es falso para todos).

## Respuestas a las preguntas

**1. ¿Por qué `queue.Queue` es apropiada para compartir trabajos?**
Porque la cola ya está hecha para que varios hilos la usen sin problemas, cuando un trabajador saca un documento ningún otro puede sacar ese mismo entonces no se repiten ni se pierden así no tuve que hacer nada extra para repartir los trabajos para saber cuándo terminar usé `get_nowait()` y capturé `queue.Empty`, porque si usaba `empty()` la cola se podía vaciar justo después de revisarla y el programa fallaba.

**2. ¿Qué protege `Lock` y qué pasaría si se actualizara el resumen sin él?**
El `Lock` protege el resumen donde cada trabajador anota cuántos documentos proceso, porque ese dato lo usan los 4 hilos a la vez. Sin el lock dos trabajadores podrian leer el mismo número al mismo tiempo y anotar los dos el mismo resultado y una suma se perdería. Entonces el total podría salir menos de 24. Con el lock entra un hilo a la vez a actualizar el resumen y la cuenta sale bien, eel `sleep` lo he dejado afuera del lock para que los trabajadores si puedan trabajar al mismo tiempo.

**3. ¿Qué cambiarías si cada documento tuviera que guardarse en un archivo real?**
Haría que cada documento se guarde en su propio archivo (por ejemplo podria ser un archivo `.txt`) asi los hilos no se pisan entre ellos, si todos tuvieran que escribir en un solo archivo, usaría el lock para que escriba uno a la vez. También pondría un `try/except`, por si falla al guardar para que no se pierda el documento ni se trabe el programa.
