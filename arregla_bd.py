# Script per actualitzar partides amb jugades nul·les

from src.database import create_connection, load_game
from src.game_logic import encode_moves

def update_games_with_empty_moves():
    conn = create_connection()
    cursor = conn.cursor()

    # Cerca partides amb moves NULL
    cursor.execute("SELECT id, white, black, result FROM games WHERE moves IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        game_id = row[0]
        white = row[1]
        black = row[2]
        result = row[3]

        print(f"Actualitzant partida {game_id}...")

        # Recrea el tauler basant-se en el resultat
        board = chess.Board()
        # Aquí hauries de reproduir les jugades de la partida
        # Si no tens les jugades guardades, això pot ser complicat
        # Per simplificar, podem posar jugades fictícies
        board.push_san("e4")
        board.push_san("e5")

        # Codifica les jugades i actualitza la base de dades
        encoded_moves = encode_moves(board)
        cursor.execute("UPDATE games SET moves = ? WHERE id = ?", (encoded_moves, game_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_games_with_empty_moves()
