### REPOSITORI DE FRAGMENTS DE CODI

def create_controls(self):
        control_widget = QWidget()
        layout = QVBoxLayout()

        self.info_label = QLabel("Info: Juga!")
        layout.addWidget(self.info_label)

        save_button = QPushButton("Guardar Partida")
        save_button.clicked.connect(self.save_current_game)
        layout.addWidget(save_button)

        load_button = QPushButton("Carregar Partida")
        load_button.clicked.connect(self.load_saved_game)
        layout.addWidget(load_button)

        toggle_stockfish_button = QPushButton("Alternar Stockfish")
        toggle_stockfish_button.clicked.connect(self.toggle_stockfish)
        layout.addWidget(toggle_stockfish_button)

        load_button = QPushButton("Reiniciar partida")
        load_button.clicked.connect(self.reset_board)
        layout.addWidget(load_button)

        control_widget.setLayout(layout)
        self.setMenuWidget(control_widget)


 def create_header_inputs(self):
        """Crea un formulari per a les dades de capçalera."""
        self.header_inputs = QWidget()
        layout = QFormLayout()

        # Crear camps editables
        self.white_player = QLineEdit("Pares Vives, Natalia")
        self.elo_white = QLineEdit("2149")
        self.black_player = QLineEdit("Pares Vives, Natalia")
        self.elo_black = QLineEdit("2149")
        self.tournament = QLineEdit("Torneig d'Escacs")
        self.location = QLineEdit("Amposta")
        self.round_num  = QLineEdit("4.4")
        self.team_white = QLineEdit("AMPOSTA A")
        self.team_black = QLineEdit("AMPOSTA A")
        self.result = QLineEdit("*")  # Resultat inicialment desconegut
        self.eco = QLineEdit("")  # Codi ECO
        self.date = QLineEdit("03/02/2025") # Data de la partida


        # Afegir els camps al layout
        layout.addRow("Blanc:", self.white_player)
        layout.addRow("Elo:", self.elo_white)
        layout.addRow("Negre:", self.black_player)
        layout.addRow("Elo:", self.elo_black)
        layout.addRow("Torneig:", self.tournament)
        layout.addRow("Lloc:", self.location)
        layout.addRow("Ronda:", self.round_num)
        layout.addRow("Equip blanc:", self.team_white)
        layout.addRow("Equip_negre:", self.team_black)
        layout.addRow("Resultat:", self.result)
        layout.addRow("ECO:", self.eco)
        layout.addRow("Data:", self.date)

        self.header_inputs.setLayout(layout)

 # Crea un layout per al tauler i els widgets laterals
        # top_layout = QHBoxLayout()  # Layout superior horitzontal

        # Afegir el tauler al layout superior
        # top_layout.addWidget(self.board_widget)  # Tauler

        # Afegir el PGN i l'anàlisi de Stockfish al layout lateral
        # right_column = QVBoxLayout()
        # right_column.addWidget(self.pgn_display)  # Quadre de PGN
        # right_column.addWidget(self.stockfish_analysis_display)  # Quadre d'anàlisi

        # top_layout.addLayout(right_column)  # Afegir el layout lateral al layout superior

        # Afegir el layout superior al layout principal
        # main_layout.addLayout(top_layout)

        # Configurar el widget central amb el layout principal
        # container = QWidget()
        # container.setLayout(main_layout)
        # self.setCentralWidget(container)

        # Afegir el formulari de capçalera
        # main_layout.addLayout(top_layout)
        # main_layout.addWidget(self.header_inputs)  

        # Botons addicionals
        self.create_controls()# Crea un layout per al tauler i els widgets laterals
