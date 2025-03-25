import sqlite3
import chess        # Importa el mòdul chess aquí

def create_connection():
    conn = sqlite3.connect('db/chess.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    # Crear taula d'usuaris
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Crear taula de partides
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,           -- ID de l'usuari que ha guardat la partida
            white TEXT NOT NULL,                -- Nom del jugador blanc
            black TEXT NOT NULL,                -- Nom del jugador negre
            elo_white INTEGER DEFAULT 0,        -- ELO del jugador blanc
            elo_black INTEGER DEFAULT 0,        -- ELO del jugador negre
            tournament TEXT DEFAULT '',         -- Nom del torneig
            location TEXT DEFAULT '',           -- Lloc on es va jugar
            round_num TEXT DEFAULT '',          -- Ronda del torneig
            result TEXT DEFAULT '',             -- Resultat de la partida (1-0, 0-1, 1/2-1/2)
            team_white TEXT DEFAULT '',         -- Equip del jugador blanc
            team_black TEXT DEFAULT '',         -- Equip del jugador negre
            eco TEXT DEFAULT '',                -- Codi ECO de l'obertura
            date TEXT DEFAULT CURRENT_TIMESTAMP,-- Data de la partida
            extra TEXT DEFAULT '',
            moves BLOB NOT NULL,                -- Jugades emmagatzemades en format binari
            FOREIGN KEY(user_id) REFERENCES users(id)
        )   	    
    ''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def save_game(user_id, white, black, elo_white, elo_black, tournament, location, round_num, result, team_white, team_black, eco, date, extra, moves: bytes):
    conn = create_connection()
    cursor = conn.cursor()

    # Insereix les dades a la taula
    cursor.execute("""
        INSERT INTO games (
            user_id, white, black, elo_white, elo_black, tournament, location, round_num, result,
            team_white, team_black, eco, date, extra, moves) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, white, black, elo_white, elo_black, tournament, location, round_num, result, team_white, team_black, eco, date, extra, moves))

    conn.commit()
    conn.close()


# src/database.py

def load_game(game_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Carrega les dades de la partida
    cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
    row = cursor.fetchone()

    if row:
        # Comprova si les jugades són None abans de decodificar-les
        moves = decode_moves(row[15]) if row[15] is not None else []

        game_data = {
            "id": row[0],
            "user_id": row[1],
            "white": row[2],
            "black": row[3],
            "elo_white": row[4],
            "elo_black": row[5],
            "tournament": row[6],
            "location": row[7],
            "round_num": row[8],
            "result": row[9],
            "team_white": row[10],
            "team_black": row[11],
            "eco": row[12],
            "date": row[13],
            'extra': row[14],
            "moves": moves  # Jugades decodificades o llista buida
            
        }
        return game_data
    return None

