class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.human_player = "O"
        self.ai_player = "X"

    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != " ":
                return self.board[i]
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return self.board[i]
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]
        return None

    def is_board_full(self):
        return " " not in self.board

    def game_over(self):
        return self.check_winner() is not None or self.is_board_full()

    def evaluate_heuristic(self):
        def count_winning_lines(player):
            winning_lines = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]
            ]
            count = 0
            for line in winning_lines:
                line_values = [self.board[pos] for pos in line]
                if all(cell == player or cell == " " for cell in line_values):
                    count += 1
            return count

        max_lines = count_winning_lines(self.ai_player)
        min_lines = count_winning_lines(self.human_player)
        return max_lines - min_lines

    def minimax(self, depth, is_maximizing):
        if self.check_winner() == self.ai_player:
            return 10 - depth
        if self.check_winner() == self.human_player:
            return depth - 10
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                self.board[move] = self.ai_player
                score = float("inf")
                for min_move in self.available_moves():
                    self.board[min_move] = self.human_player
                    eval_score = self.evaluate_heuristic()
                    score = min(score, eval_score)
                    self.board[min_move] = " "
                best_score = max(best_score, score)
                self.board[move] = " "
            return best_score
        else:
            best_score = float("inf")
            for move in self.available_moves():
                self.board[move] = self.human_player
                score = float("-inf")
                for max_move in self.available_moves():
                    self.board[max_move] = self.ai_player
                    eval_score = self.evaluate_heuristic()
                    score = max(score, eval_score)
                    self.board[max_move] = " "
                best_score = min(best_score, score)
                self.board[move] = " "
            return best_score

    def get_best_move(self):
        best_score = float("-inf")
        best_move = None

        for move in self.available_moves():
            self.board[move] = self.ai_player
            score = self.minimax(0, False)
            self.board[move] = " "
            print(f"Evaluando jugada IA en posición {move}: score = {score}")
            if score > best_score:
                best_score = score
                best_move = move

        print(f"IA elige la posición {best_move} con score = {best_score}")
        return best_move

    def play_game(self):
        print("Bienvenido al Tres en Línea!")
        print("Tú eres 'O' y la IA es 'X'")
        print("Tablero por posiciones:")
        print("0 | 1 | 2")
        print("---------")
        print("3 | 4 | 5")
        print("---------")
        print("6 | 7 | 8\n")

        import random
        ai_turn = random.choice([True, False])

        while not self.game_over():
            self.print_board()

            if ai_turn:
                print("\nTurno de la IA...")
                if self.board == [" " for _ in range(9)]:
                    move = 4
                    print("[IA juega su apertura en el centro (posición 4)]")
                else:
                    move = self.get_best_move()
                self.make_move(move, self.ai_player)
            else:
                while True:
                    try:
                        move = int(input("\nTu turno (0-8): "))
                        if 0 <= move <= 8 and self.make_move(move, self.human_player):
                            break
                        else:
                            print("¡Movimiento inválido! Intenta de nuevo.")
                    except ValueError:
                        print("Por favor, ingresa un número entre 0 y 8.")

            ai_turn = not ai_turn

        self.print_board()
        winner = self.check_winner()
        if winner == self.ai_player:
            print("\n¡La IA gana!")
        elif winner == self.human_player:
            print("\n¡Felicidades, tú ganas!")
        else:
            print("\n¡Es un empate!")


# Iniciar el juego
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
