
import numpy as np
import random
import string


def crea_tablero(lado=10):
    tablero = np.full((lado, lado), " ", dtype="<U1")
    return tablero


def coloca_barco_plus(tablero, barco):
    tablero_temp = tablero.copy()
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]

    for pieza in barco:
        fila = pieza[0]
        columna = pieza[1]

        if fila < 0 or fila >= num_max_filas:
            return False

        if columna < 0 or columna >= num_max_columnas:
            return False

        if tablero_temp[pieza] in ("O", "X"):
            return False

        tablero_temp[pieza] = "O"

    return tablero_temp


def crea_barco_aleatorio(tablero, eslora=4, num_intentos=100):
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]

    for intento in range(num_intentos):
        barco = []

        pieza_original = (
            random.randint(0, num_max_filas - 1),
            random.randint(0, num_max_columnas - 1)
        )

        barco.append(pieza_original)
        orientacion = random.choice(["N", "S", "O", "E"])

        fila = pieza_original[0]
        columna = pieza_original[1]

        for i in range(eslora - 1):
            if orientacion == "N":
                fila -= 1
            elif orientacion == "S":
                fila += 1
            elif orientacion == "E":
                columna += 1
            else:
                columna -= 1

            pieza = (fila, columna)
            barco.append(pieza)

        tablero_temp = coloca_barco_plus(tablero, barco)

        if isinstance(tablero_temp, np.ndarray):
            return tablero_temp

    return False


def coloca_flota(lado=10):
    esloras = [4, 3, 3, 2, 2]

    for intento in range(100):
        tablero = crea_tablero(lado)
        colocacion_correcta = True

        for eslora in esloras:
            tablero_temp = crea_barco_aleatorio(
                tablero, eslora, num_intentos=100
            )

            if not isinstance(tablero_temp, np.ndarray):
                colocacion_correcta = False
                break

            tablero = tablero_temp

        if colocacion_correcta:
            return tablero

    raise RuntimeError("No se ha podido colocar la flota")

def alea():
    l=['A','B','C','D','E','F','G','H','I','J']
    p2=random.randint(1,10)
    p0=random.randint(0,len(l)-1)
    p1=l[p0]
    p3=f"{p1}{p2}"
    return p3
'''
def alea():
    l = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    p0 = random.randint(0, len(l) - 1)
    p1 = l[p0]
    p2 = random.randint(1, 10)
    p3 = f"{p1}{p2}"
    return p3'''
def recibir_disparo(tablero, coordenada):
    if tablero[coordenada] == "O":
        tablero[coordenada] = "X"
        print("¡Tocado!")
        return "tocado"

    elif tablero[coordenada] == "X":
        print("Esa posición ya tenía un impacto")
        return "repetido"

    elif tablero[coordenada] == "-":
        print("Ya habías disparado ahí")
        return "repetido"

    else:
        tablero[coordenada] = "-"
        print("Agua")
        return "agua"


def conversion_coordenadas(entrada, lado=10):
    entrada = entrada.strip().upper()

    if len(entrada) < 2:
        return None

    letra = entrada[0]
    numero = entrada[1:]

    if letra not in string.ascii_uppercase[:lado]:
        return None

    if not numero.isdigit():
        return None

    fila = int(numero) - 1
    columna = string.ascii_uppercase.index(letra)

    if fila < 0 or fila >= lado:
        return None

    return (fila, columna)


def formato_tablero(tablero, ocultar_barcos=False):
    tablero_formateado = tablero.copy()

    if ocultar_barcos:
        tablero_formateado[tablero_formateado == "O"] = " "

    num_filas = tablero_formateado.shape[0]
    num_columnas = tablero_formateado.shape[1]
    letras = string.ascii_uppercase[:num_columnas]

    print("   " + " ".join(letras))

    for fila in range(num_filas):
        numero = str(fila + 1).rjust(2)
        contenido = " ".join(tablero_formateado[fila])
        print(f"{numero} {contenido}")


def mostrar_tableros(tablero_jugador, tablero_disparos):
    print("\n" + "=" * 35)
    print("TU FLOTA")
    print("=============================")
    formato_tablero(tablero_jugador)

    print("\n" + "=============================")
    print("TUS DISPAROS AL ENEMIGO")
    print("=============================")
    formato_tablero(tablero_disparos)


def turno_jugador(tablero_maquina, tablero_disparos):
    while True:
        print("\nIntroduce una coordenada (ej. C4):")
        
        a=alea()               #comentar esta liena 
        print(f"{a}")          #comentar esta linea
        #entrada=input() #<-- si quieres turnos manuales
        
        coordenada = conversion_coordenadas(a)#comentar esta linea
        #coordenada = conversion_coordenadas(entrada) #<-- si quieres turnos manuales
        

        if coordenada is None:
            print("Coordenada inválida. Usa letras A-J y filas 1-10")
            continue

        if tablero_disparos[coordenada] != " ":
            print("Ya has disparado a esa posición")
            continue

        resultado = recibir_disparo(tablero_maquina, coordenada)

        if resultado == "tocado":
            tablero_disparos[coordenada] = "X"
        else:
            tablero_disparos[coordenada] = "-"

        return


def turno_maquina(tablero_jugador, disparos_maquina):
    posiciones_disponibles = []

    num_filas = disparos_maquina.shape[0]
    num_columnas = disparos_maquina.shape[1]

    for fila in range(num_filas):
        for columna in range(num_columnas):
            if disparos_maquina[fila, columna] == " ":
                posiciones_disponibles.append((fila, columna))

    if len(posiciones_disponibles) == 0:
        return

    coordenada = random.choice(posiciones_disponibles)
    letra = string.ascii_uppercase[coordenada[1]]
    numero = coordenada[0] + 1

    print(f"\nLa máquina dispara a {letra}{numero}")

    resultado = recibir_disparo(tablero_jugador, coordenada)

    if resultado == "tocado":
        disparos_maquina[coordenada] = "X"
    else:
        disparos_maquina[coordenada] = "-"


def quedan_barcos(tablero):
    return np.any(tablero == "O")


def jugar():
    print("=============================")
    print("HUNDIR LA FLOTA")
    print("=============================")
    tablero_jugador = coloca_flota()
    tablero_maquina = coloca_flota()
    disparos_jugador = crea_tablero()
    disparos_maquina = crea_tablero()

    while True:
        mostrar_tableros(tablero_jugador, disparos_jugador)
        turno_jugador(tablero_maquina, disparos_jugador)

        if not quedan_barcos(tablero_maquina):
            mostrar_tableros(tablero_jugador, disparos_jugador)
            print("\n¡HAS GANADO! Has hundido toda la flota enemiga")
            break
        turno_maquina(tablero_jugador, disparos_maquina)

        if not quedan_barcos(tablero_jugador):
            mostrar_tableros(tablero_jugador, disparos_jugador)
            print("\nHAS PERDIDO. La máquina ha hundido tu flota")
            break

    print("\nFin de la partida")