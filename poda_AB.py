import matplotlib.pyplot as plt
import networkx as nx
import random
from copy import deepcopy

class TresEnRaya:
    def __init__(self):
        self.tablero = [" " for _ in range(9)]
        self.jugador_humano = "O"
        self.jugador_ia = "X"
        self.historial_jugadas = []  # [(jugador, pos, f(v), alternativas)]
        self.podados_en_turno = []

    def imprimir_tablero(self):
        for i in range(0, 9, 3):
            print(f"{self.tablero[i]} | {self.tablero[i+1]} | {self.tablero[i+2]}")
            if i < 6:
                print("---------")

    def movimientos_disponibles(self):
        return [i for i, casilla in enumerate(self.tablero) if casilla == " "]

    def realizar_movimiento(self, posicion, jugador):
        if self.tablero[posicion] == " ":
            self.tablero[posicion] = jugador
            print(f"\n{jugador} juega en la posición {posicion}")
            self.imprimir_tablero()
            f_valor, lineas_ia, lineas_humano = self.evaluar_heuristica()
            print(f"Heurística actual: f(v) = {lineas_ia} - {lineas_humano} = {f_valor}")
            return True
        return False

    def verificar_ganador(self):
        for i in range(0, 9, 3):
            if self.tablero[i] == self.tablero[i + 1] == self.tablero[i + 2] != " ":
                return self.tablero[i]
        for i in range(3):
            if self.tablero[i] == self.tablero[i + 3] == self.tablero[i + 6] != " ":
                return self.tablero[i]
        if self.tablero[0] == self.tablero[4] == self.tablero[8] != " ":
            return self.tablero[0]
        if self.tablero[2] == self.tablero[4] == self.tablero[6] != " ":
            return self.tablero[2]
        return None

    def tablero_lleno(self):
        return " " not in self.tablero

    def juego_terminado(self):
        return self.verificar_ganador() is not None or self.tablero_lleno()

    def evaluar_heuristica(self):
        def contar_lineas_ganadoras(jugador):
            lineas_ganadoras = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]
            ]
            conteo = 0
            oponente = self.jugador_humano if jugador == self.jugador_ia else self.jugador_ia
            for linea in lineas_ganadoras:
                valores = [self.tablero[pos] for pos in linea]
                if oponente not in valores:
                    conteo += 1
            return conteo

        lineas_ia = contar_lineas_ganadoras(self.jugador_ia)
        lineas_humano = contar_lineas_ganadoras(self.jugador_humano)
        return lineas_ia - lineas_humano, lineas_ia, lineas_humano

    def minimax_ab(self, profundidad, es_maximizando, alpha, beta, contador):
        if self.verificar_ganador() == self.jugador_ia:
            return 10 - profundidad
        if self.verificar_ganador() == self.jugador_humano:
            return profundidad - 10
        if self.tablero_lleno():
            return 0

        if es_maximizando:
            max_eval = float("-inf")
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento] = self.jugador_ia
                contador["evaluados"] += 1
                evaluacion = self.minimax_ab(profundidad + 1, False, alpha, beta, contador)
                self.tablero[movimiento] = " "
                max_eval = max(max_eval, evaluacion)
                alpha = max(alpha, evaluacion)
                if beta <= alpha:
                    contador["podados"] += 1
                    self.podados_en_turno.append(movimiento)
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento] = self.jugador_humano
                contador["evaluados"] += 1
                evaluacion = self.minimax_ab(profundidad + 1, True, alpha, beta, contador)
                self.tablero[movimiento] = " "
                min_eval = min(min_eval, evaluacion)
                beta = min(beta, evaluacion)
                if beta <= alpha:
                    contador["podados"] += 1
                    self.podados_en_turno.append(movimiento)
                    break
            return min_eval

    def obtener_mejor_movimiento(self):
        mejor_puntaje = float("-inf")
        mejor_movimiento = None
        mejor_f_valor = None
        mejor_lineas_ia = None
        mejor_lineas_humano = None
        alternativas = []

        contador = {"evaluados": 0, "podados": 0}
        self.podados_en_turno = []

        for movimiento in self.movimientos_disponibles():
            self.tablero[movimiento] = self.jugador_ia
            f_valor, lineas_ia, lineas_humano = self.evaluar_heuristica()
            puntaje = self.minimax_ab(0, False, float("-inf"), float("inf"), contador)
            self.tablero[movimiento] = " "
            if puntaje > mejor_puntaje:
                if mejor_movimiento is not None:
                    alternativas.append((mejor_movimiento, mejor_f_valor))
                mejor_puntaje = puntaje
                mejor_movimiento = movimiento
                mejor_f_valor = f_valor
                mejor_lineas_ia = lineas_ia
                mejor_lineas_humano = lineas_humano
            else:
                alternativas.append((movimiento, f_valor))

        alt_textos = [f"Pos {mov}: f(v)={v}" for mov, v in alternativas]
        podados_textos = [f"Pos {mov}: PODADO" for mov in self.podados_en_turno]
        self.historial_jugadas.append(("IA", mejor_movimiento, f"f(v)={mejor_f_valor}", alt_textos + podados_textos))

        print(f"\n[Resumen poda alfa-beta]")
        print(f"Nodos evaluados: {contador['evaluados']}")
        print(f"Ramas podadas: {contador['podados']}")
        print(f"IA elige la posición {mejor_movimiento} con heurística: f(v) = {mejor_lineas_ia} - {mejor_lineas_humano} = {mejor_f_valor}")
        return mejor_movimiento

    def jugar(self):
        print("¡Bienvenido al Tres en Raya!")
        print("Eres 'O' y el agente es 'X'")
        print("Tablero por posiciones:")
        print("0 | 1 | 2")
        print("---------")
        print("3 | 4 | 5")
        print("---------")
        print("6 | 7 | 8\n")

        turno_ia = random.choice([True, False])

        while not self.juego_terminado():
            if turno_ia:
                print("\nTurno de la IA...")
                if self.tablero == [" " for _ in range(9)]:
                    movimiento = 4
                    print("[IA juega su apertura en el centro (posición 4)]")
                    self.historial_jugadas.append(("IA", 4, "f(v)=N/A", []))
                else:
                    movimiento = self.obtener_mejor_movimiento()
                self.realizar_movimiento(movimiento, self.jugador_ia)
            else:
                while True:
                    try:
                        movimiento = int(input("\nTu turno (0-8): "))
                        if 0 <= movimiento <= 8 and self.realizar_movimiento(movimiento, self.jugador_humano):
                            f_valor, _, _ = self.evaluar_heuristica()
                            self.historial_jugadas.append(("Humano", movimiento, f"f(v)={f_valor}", []))
                            break
                        else:
                            print("¡Movimiento inválido! Intenta de nuevo.")
                    except ValueError:
                        print("Por favor, ingresa un número entre 0 y 8.")
            turno_ia = not turno_ia

        self.imprimir_tablero()
        ganador = self.verificar_ganador()
        if ganador == self.jugador_ia:
            print("\nLa IA gana!")
        elif ganador == self.jugador_humano:
            print("\nFelicidades, ganaste!!!")
        else:
            print("\nEs un empate!")
            
if __name__ == "__main__":
    juego = TresEnRaya()
    juego.jugar()
