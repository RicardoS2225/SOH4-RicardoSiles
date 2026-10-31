import threading
import queue
import time
import random
 
NUM_DOCUMENTOS = 24
NOMBRES_TRABAJADORES = ["Siles", "Candia", "Figueredo", "Poma"]
NUM_TRABAJADORES = len(NOMBRES_TRABAJADORES)
 
trabajos = queue.Queue()
resultados = {}
registro = []
lock = threading.Lock()
 
 
for doc_id in range(1, NUM_DOCUMENTOS + 1):
    trabajos.put((doc_id, random.randint(1, 5)))
 
 
def trabajador(nombre):
 
    while True:
        try:
 
            doc_id, tamano = trabajos.get_nowait()
        except queue.Empty:
            break
 
        time.sleep(tamano * 0.1)
 
 
        with lock:
            resultados[nombre] = resultados.get(nombre, 0) + 1
            registro.append((doc_id, tamano, nombre))
            print(f"[{nombre}] procesó documento {doc_id:02d} (tamaño {tamano})")
 
 
def main():
    inicio = time.time()
 
 
    hilos = []
    for nombre in NOMBRES_TRABAJADORES:
        resultados[nombre] = 0
        hilo = threading.Thread(target=trabajador, args=(nombre,), name=nombre)
        hilos.append(hilo)
 
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
 
    duracion = time.time() - inicio
 
 
    total = sum(resultados.values())
    print("\nRESUMEN POR TRABAJADOR")
    for nombre in NOMBRES_TRABAJADORES:
        print(f"{nombre}: {resultados[nombre]} documentos")
    print(f"TOTAL PROCESADO: {total} de {NUM_DOCUMENTOS}")
    print(f"Tiempo total: {duracion:.2f} s")
 
 
    print("\nASIGNACIÓN DE DOCUMENTOS")
    for nombre in NOMBRES_TRABAJADORES:
        docs = sorted(d for d, _, t in registro if t == nombre)
        print(f"{nombre}: {docs}")
 
 
    ids = [d for d, _, _ in registro]
    print("\nVERIFICACIONES")
    print("1) Suma por trabajador == 24:", total == NUM_DOCUMENTOS)
    print("2) Cada ID aparece una sola vez:", len(ids) == len(set(ids)) == NUM_DOCUMENTOS)
    print("3) Los 4 hilos finalizaron:", not any(h.is_alive() for h in hilos))
 
 
if __name__ == "__main__":
    main()  