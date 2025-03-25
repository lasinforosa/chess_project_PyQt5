from stockfish import Stockfish
import subprocess
from src.defs import *




class ChessEngine:
    def __init__(self, path_to_stockfish):
        self.stockfish = Stockfish(path_to_stockfish)

    def make_move(self, fen, depth=10):
        """Calcula el millor moviment per a una posició donada."""
        self.stockfish.set_fen_position(fen)
        return self.stockfish.get_best_move()

    def get_evaluation(self):
            """Obté l'avaluació de la posició actual."""
            info = self.stockfish.get_evaluation()
            return f"{info['value']} ({info['type']})"


class UCIMotor:
    def __init__(self, path_to_engine):
        self.process = subprocess.Popen(path_to_engine, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.send_command("uci")

    def send_command(self, command):
        self.process.stdin.write(f"{command}\n")
        self.process.stdin.flush()

    def get_response(self):
        while True:
            output = self.process.stdout.readline().strip()
            if "bestmove" in output:
                return output.split()[1]

    def set_position(self, fen):
        self.send_command(f"position fen {fen}")

    def find_best_move(self):
        self.send_command("go movetime 1000")  # Busca el millor moviment en 1 segon
        return self.get_response()


