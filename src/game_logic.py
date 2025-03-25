# src/game_logic.py

import chess

def encode_moves(board: chess.Board) -> bytes:
    """Converteix les jugades d'un tauler en un format binari."""
    moves = []
    for move in board.move_stack:
        # Codifica cada moviment com un enter de 4 bytes
        move_int = (move.from_square << 6) | move.to_square
        if move.promotion:  # Afegir informació de promoció si és necessari
            move_int |= move.promotion
        moves.append(move_int.to_bytes(4, byteorder='big'))
    return b''.join(moves)


def decode_moves(encoded_moves: bytes) -> list:
    """Decodifica un format binari en una llista de jugades."""
    if not encoded_moves:  # Comprova si és None o buit
        return []

    moves = []
    for i in range(0, len(encoded_moves), 4):
        move_int = int.from_bytes(encoded_moves[i:i+4], byteorder='big')
        from_square = (move_int >> 6) & 0x3F
        to_square = move_int & 0x3F
        promotion = chess.PieceType((move_int >> 12) & 0x7) if move_int >> 12 else None
        moves.append(chess.Move(from_square, to_square, promotion=promotion))
    return moves


def translate_pgn(move_san: str) -> str:
    """
    Tradueix una jugada en notació SAN del anglès al català.
    KQRBN → RDTAC
    """
    translation_map = {
        "K": "R",  # Rei
        "Q": "D",  # Dama
        "R": "T",  # Torre
        "B": "A",  # Alfil
        "N": "C"   # Cavall
    }

    # Substitueix cada lletra segons el mapa de traducció
    for english, catalan in translation_map.items():
        move_san = move_san.replace(english, catalan)

    return move_san  







