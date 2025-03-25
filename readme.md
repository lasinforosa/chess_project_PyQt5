BBDD SQLITE3

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,           -- ID de l'usuari que ha guardat la partida
    white TEXT NOT NULL,                -- Nom del jugador blanc
    black TEXT NOT NULL,                -- Nom del jugador negre
    elo_white INTEGER DEFAULT 0,        -- ELO del jugador blanc
    elo_black INTEGER DEFAULT 0,        -- ELO del jugador negre
    tournament TEXT DEFAULT '',         -- Nom del torneig
    location TEXT DEFAULT '',           -- Lloc on es va jugar
    round TEXT DEFAULT '',              -- Ronda del torneig
    result TEXT DEFAULT '',             -- Resultat de la partida (1-0, 0-1, 1/2-1/2)
    team_white TEXT DEFAULT '',         -- Equip del jugador blanc
    team_black TEXT DEFAULT '',         -- Equip del jugador negre
    eco TEXT DEFAULT '',                -- Codi ECO de l'obertura
    moves BLOB NOT NULL,                -- Jugades emmagatzemades en format binari
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-----------------------------


