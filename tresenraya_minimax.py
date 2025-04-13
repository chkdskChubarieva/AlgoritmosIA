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

    def minimax(self, profundidad, es_maximizando):
        if self.verificar_ganador() == self.jugador_ia:
            return 10 - profundidad
        if self.verificar_ganador() == self.jugador_humano:
            return profundidad - 10
        if self.tablero_lleno():
            return 0

        if es_maximizando:
            mejor_puntaje = float("-inf")
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento] = self.jugador_ia
                puntaje = self.minimax(profundidad + 1, False)
                self.tablero[movimiento] = " "
                mejor_puntaje = max(mejor_puntaje, puntaje)
            return mejor_puntaje
        else:
            mejor_puntaje = float("inf")
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento] = self.jugador_humano
                puntaje = self.minimax(profundidad + 1, True)
                self.tablero[movimiento] = " "
                mejor_puntaje = min(mejor_puntaje, puntaje)
            return mejor_puntaje

    def obtener_mejor_movimiento(self):
        mejor_puntaje = float("-inf")
        mejor_movimiento = None
        mejor_f_valor = None
        mejor_lineas_ia = None
        mejor_lineas_humano = None
        alternativas = []

        for movimiento in self.movimientos_disponibles():
            self.tablero[movimiento] = self.jugador_ia
            f_valor, lineas_ia, lineas_humano = self.evaluar_heuristica()
            print(f"Evaluando jugada IA en posición {movimiento}: f(v) = {lineas_ia} - {lineas_humano} = {f_valor}")
            puntaje = self.minimax(0, False)
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
        self.historial_jugadas.append(("IA", mejor_movimiento, f"f(v)={mejor_f_valor}", alt_textos))

        print(f"IA elige la posición {mejor_movimiento} con score heurístico: f(v) = {mejor_lineas_ia} - {mejor_lineas_humano} = {mejor_f_valor}")
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
                            f_valor, lineas_ia, lineas_humano = self.evaluar_heuristica()
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

        self.graficar_arbol()

    def graficar_arbol(self):
        G = nx.DiGraph()
        pos = {}
        labels = {}
        nivel_y = 0
        nodo_id = 0
        rama_anterior = None

        spacing_x = 10  # Más espacio horizontal
        spacing_y = 4   # Más espacio vertical

        for idx, (jugador, jugada, heuristica, alternativas) in enumerate(self.historial_jugadas):
            nodo_label = f"{jugador} jugó {jugada}\n{heuristica}"
            G.add_node(nodo_id)
            pos[nodo_id] = (idx * spacing_x, -nivel_y * spacing_y)
            labels[nodo_id] = nodo_label

            if rama_anterior is not None:
                G.add_edge(rama_anterior, nodo_id)

            padre_actual = nodo_id
            nodo_id += 1

            for i, alt in enumerate(alternativas):
                alt_label = f"{alt}"  # Sin la palabra "Alternativa"
                G.add_node(nodo_id)
                x_offset = (i - len(alternativas) / 2) * (spacing_x * 0.6)
                pos[nodo_id] = (idx * spacing_x + x_offset, -nivel_y * spacing_y - spacing_y * 1.5)
                labels[nodo_id] = alt_label
                G.add_edge(padre_actual, nodo_id)
                nodo_id += 1

            rama_anterior = padre_actual
            nivel_y += 1

        plt.figure(figsize=(24, 14))  # Aumentamos tamaño total del gráfico
        nx.draw(G, pos=pos, labels=labels, with_labels=False, node_color="lightblue", node_size=3200,
                edge_color="gray", font_size=10, font_weight="bold")
        nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight="bold")
        plt.title("Árbol de jugadas con evaluación heurística", fontsize=16)
        plt.axis("off")
        plt.tight_layout()
        plt.show()



# Iniciar el juego
if __name__ == "__main__":
    juego = TresEnRaya()
    juego.jugar()
