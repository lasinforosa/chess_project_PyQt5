import sys
import chess
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction
from PyQt5.QtGui import QIcon, QPixmap 
from PyQt5.QtCore import Qt
from src.defs import *
from src.game_logic import encode_moves, decode_moves, translate_pgn
from src.database import save_game, load_game
from src.uci import ChessEngine
from gui.headerDialog import HeaderDialog



class Escacs(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Inicialització del tauler i motor
        self.board = chess.Board()
        self.engine = ChessEngine(path_to_stockfish)
        self.stockfish_active = False  # Per defecte, Stockfish està desactivat per jugar
                                       # pero no per analitzar
        self.ply = 0
        

        # Inicialització de les dades de capçalera
        self.tournament = "CAT tch 1Div G1"
        self.location = "Local"
        self.white = "Pares Vives, Natalia"
        self.black = "Pares Vives, Natalia"
        self.elo_white = "2149"
        self.elo_black = "2149"
        self.result = "*"
        self.round_num = "1"
        self.team_white = ""
        self.team_black = ""
        self.date = "03/02/2025"
        self.extra = ""
        self.eco = "?"

        self.initUI()

        
    def initUI(self):
        # Crear el centralWidget (on anirà tot el contingut principal)
        central_widget = QWidget()
        main_layout = QVBoxLayout()  # Layout principal: vertical

        # Part superior: Tauler d'escacs i QTextEdit lateral
        top_layout = QHBoxLayout()

        # Crear el tauler d'escacs
        self.chessboard_widget = QWidget()  # Widget que conte el tauler
        
        # crea el tauler
        self.create_board()
        
        # Posar el tauler d'escacs dins d'un QGroupBox per mantenir-lo contenidor
        chessboard_group = QGroupBox()
        group_layout = QVBoxLayout()  # Layout per al grup
        group_layout.addWidget(self.chessboard_widget, alignment=Qt.AlignTop | Qt.AlignLeft)  # Alinia al costat superior-esquerra
        chessboard_group.setLayout(group_layout)

        # Afegir el tauler al layout superior
        top_layout.addWidget(chessboard_group)

        # Afegir un QTextEdit lateral a la dreta del tauler
        # pgn_display
        self.pgn_display = QTextEdit()
        self.pgn_display.setReadOnly(True)  # Fa que el quadre sigui de només lectura
        self.pgn_display.setMinimumWidth(200)  # Estableix una amplada mínima
        self.pgn_display.setSizePolicy(
            self.pgn_display.sizePolicy().horizontalPolicy(),  # Política horitzontal
            self.pgn_display.sizePolicy().Expanding           # Expandeix horitzontalment
        )
        self.generate_pgn_header()

        # AFEGIR EL QTextEdit AL LAYOUT (FIX!)
        top_layout.addWidget(self.pgn_display)

        # Ajustar els factors de creixement per als elements del layout
        top_layout.setStretch(0, 1)  # El tauler té un factor de creixement fixe
        top_layout.setStretch(1, 2)  # El QTextEdit té un factor de creixement major

        # Afegir el layout superior al layout principal
        main_layout.addLayout(top_layout)

        # Part inferior: Dos QTextEdit per informació addicional
        bottom_layout = QVBoxLayout()

        # Primer QTextEdit (per informació d'anàlisi)
        # stockfish_analysis_display
        self.stockfish_analysis_display = QTextEdit()
        self.stockfish_analysis_display.setReadOnly(True)  # Només lectura
        
        bottom_layout.addWidget(self.stockfish_analysis_display)

        # Segon QTextEdit (per informació diversa)
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        bottom_layout.addWidget(self.info_text)

        # Afegir el layout inferior al layout principal
        main_layout.addLayout(bottom_layout)

        # Configurar el layout principal
        self.setLayout(main_layout)

        # Assignar el layout al centralWidget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)  # Establir el centralWidget
        
        # Crear el menú principal
        self.create_menu()

        self.setWindowTitle(wTitle)
        self.setGeometry(x0, y0, x1, y1)


    def create_board(self):
        chessboard_layout = QGridLayout()

        # Eliminar tots els marges i l'espaiat del layout
        chessboard_layout.setContentsMargins(0, 0, 0, 0)  # Elimina els marges exteriors
        chessboard_layout.setSpacing(0)  # Elimina l'espaiat entre els widgets

        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                button = QPushButton()
                button.setFixedSize(sqSIZE, sqSIZE)  # Tamany fixe per a cada casella
                if (row + col) % 2 == 0:
                    button.setStyleSheet(f"background-color: {sqW_bg}; border: none")
                else:
                    button.setStyleSheet(f"background-color: {sqB_bg}; border: none")
                # estil boto sense marges
                button.setIconSize(button.size())  # Ajusta la mida de la icona
                button.clicked.connect(lambda _, r=row, c=col: self.on_square_click(r, c))

                chessboard_layout.addWidget(button, row, col)

                # Carrega la imatge de la peça si hi ha alguna
                self.update_piece_image(button, square)

        self.chessboard_widget.setLayout(chessboard_layout)

    
    def update_piece_image(self, button, square):
        piece = self.board.piece_at(square)
        if piece:
            color = "w" if piece.color == chess.WHITE else "b"
            piece_type = chess.piece_symbol(piece.piece_type).upper()
            image_path = f"{pathPieces}{color}{piece_type}.png"
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                button.setIcon(QIcon(pixmap))
        else:
            # Si no hi ha cap peça, elimina l'icona
            button.setIcon(QIcon())  # Això neteja l'icona 

    
    def create_menu(self):
        """Crea el menú principal de l'aplicació."""
        menu_bar = self.menuBar()

        # Menú "Joc"
        game_menu = menu_bar.addMenu("Joc")

        # Opció "Nova Partida"
        new_game_action = QAction("Nova Partida", self)
        new_game_action.triggered.connect(self.reset_board)
        game_menu.addAction(new_game_action)

        # Opció "Dades de la Partida"
        header_action = QAction("Dades de la Partida", self)
        header_action.triggered.connect(self.show_header_dialog)
        game_menu.addAction(header_action)

        # Opció "Guardar Partida"
        save_action = QAction("Guardar Partida", self)
        save_action.triggered.connect(self.save_current_game)
        game_menu.addAction(save_action)

        # Opció "Carregar Partida"
        load_action = QAction("Carregar Partida", self)
        load_action.triggered.connect(self.load_saved_game)
        game_menu.addAction(load_action)

        # Menú "Stockfish"
        stockfish_menu = menu_bar.addMenu("Stockfish")

        # Opció "Alternar Stockfish"
        toggle_stockfish_action = QAction("Alternar Stockfish", self)
        toggle_stockfish_action.triggered.connect(self.toggle_stockfish)
        stockfish_menu.addAction(toggle_stockfish_action)    


    def on_square_click(self, row, col):
        square = chess.square(col, 7 - row)

        #### DEBUG INFO ==================
        # print(f"Clic a la casella {chess.SQUARE_NAMES[square]}")
        # print(f"Torn actual: {'Blanc' if self.board.turn else 'Negre'}")
        # print(f"Estat del tauler:\n{self.board}")

        if hasattr(self, "selected_square"):
            if square == self.selected_square:
                # Cancel·la la selecció si cliques dues vegades a la mateixa casella
                del self.selected_square
                self.update_board_display()
                return

        if not hasattr(self, "selected_square"):
            # Selecciona una nova casella
            self.selected_square = square
            self.update_board_display()
        else:
            # Mou la peça
            self.move = chess.Move(self.selected_square, square)
            #### DEBUG INFO ==================
            # self.info_text.append(f"Estat del tauler abans del moviment {self.move.uci()}:\n{self.board}")
            # print(f"Estat del tauler abans del moviment {self.move.uci()}:\n{self.board}")

            if self.move in self.board.legal_moves:
                # Comprova que el moviment és legal per al jugador actual
                if self.board.turn == chess.WHITE and chess.square_file(self.selected_square) >= 0:
                    # Moviment legal per als blancs
                    self.update_pgn_display()
                    self.board.push(self.move)
                    self.ply = self.ply + 1
                elif self.board.turn == chess.BLACK and chess.square_file(self.selected_square) >= 0:
                    # Moviment legal per als negres
                    self.update_pgn_display()
                    self.board.push(self.move)
                    self.ply = self.ply + 1

                del self.selected_square

                #### DEBUG INFO ==================
                # self.info_text.append(f"Estat del tauler abans del moviment {move.uci()}:\n{self.board}")
                # print(f"Estat del tauler després del moviment {move.uci()}:\n{self.board}")

                # Actualitza l'interfície gràfica i el PGN
                self.update_board_display()
                # self.update_pgn_display()

                # Si Stockfish està activat, fa una jogada
                if self.stockfish_active:
                    self.update_pgn_display()
                    best_move = self.engine.make_move(self.board.fen())
                    self.board.push(chess.Move.from_uci(best_move))  # Actualitza l'estat del tauler amb el moviment de Stockfish
                    self.update_board_display()
                    self.ply = self.ply + 1
                    
                    #### DEBUG INFO ==================
                    # print(f"Stockfish ha jugat: {best_move}")
                    # print(f"Estat actual del tauler després de Stockfish:\n{self.board}")

                    # Mostra l'anàlisi de Stockfish
                    # self.update_stockfish_analysis()
                else:
                    # Mostra l'anàlisi de Stockfish (independentment de si està activat)
                    self.update_stockfish_analysis()


            else:
                self.info_text.append(f"El moviment {self.move.uci()} no és legal")
                # print(f"El moviment {self.move.uci()} no és legal.")


    def update_stockfish_analysis(self):
        """Actualitza el quadre d'anàlisi de Stockfish."""
        # if not self.stockfish_active:
        #     self.stockfish_analysis_display.setPlainText("Stockfish està desactivat.")
        #    return

        # Obtenir la posició actual del tauler
        fen = self.board.fen()
        
        # NPV conf per analisi infinit


        # Demanar a Stockfish la millor jugada
        try:
            best_move = self.engine.make_move(fen, depth=10)  # Profunditat personalitzable
            evaluation = self.engine.get_evaluation()  # Obté l'avaluació de la posició
            analysis_text = f"Millor moviment: {best_move}\nAvaluació: {evaluation}"
            self.stockfish_analysis_display.setPlainText(analysis_text)
        except Exception as e:
            self.stockfish_analysis_display.setPlainText(f"Error en l'anàlisi: {str(e)}")


    def toggle_stockfish(self):
        """Alterna l'estat de Stockfish (activat/desactivat)."""
        self.stockfish_active = not self.stockfish_active
        status = "activat" if self.stockfish_active else "desactivat"
        self.info_text.append(f"Stockfish ara està {status}.")

    
    def reset_board(self):
        """Reinicia el tauler a la posició inicial."""
        self.board = chess.Board()  # Restableix el tauler intern
        self.selected_square = None  # Elimina la selecció actual
        self.update_board_display()  # Actualitza l'interfície gràfica
        self.update_pgn_display()    # Netegen el PGN
        self.update_stockfish_analysis()  # Reinicia l'anàlisi

    def update_board_display(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                button = self.chessboard_widget.layout().itemAtPosition(row, col).widget()

                # Estableix el color de fons de la casella
                color = sqW_bg if (row + col) % 2 == 0 else sqB_bg

                # Destaca la casella seleccionada
                if hasattr(self, "selected_square") and square == self.selected_square:
                    color = sq_sel  

                # Destaca els moviments possibles
                if hasattr(self, "selected_square"):
                    # self.info_text.append(f"Sq_Selected: {self.selected_square}")
                    piece = self.board.piece_at(self.selected_square)
                    if piece and chess.Move(self.selected_square, square) in self.board.legal_moves:
                        color = sq_lgl

                button.setStyleSheet(f"background-color: {color}; border: none;")

                # Carrega la imatge de la peça si hi ha alguna
                self.update_piece_image(button, square)


    def update_pgn_display(self):
        """Actualitza el contingut del quadre de PGN amb el PGN complet."""
        self.generate_pgn()


    def generate_pgn_header(self):
        # Obté les dades de capçalera
        # header_data = self.get_headers()
        header_data = [
            f"[Event \"{self.tournament}\"]",
            f"[Site \"{self.location}\"]",
            f"[White \"{self.white}\" - Elo: \"{self.elo_white}\"]",
            f"[Black \"{self.black}\" - Elo: \"{self.elo_black}\"]",
            f"[Result \"{self.result}\"]",
            f"[ECO \"{self.eco}\"]",
            f"[Round \"{self.round_num}\"]",
            f"[Team \"{self.team_white}\"]",
            f"[Team \"{self.team_black}\"]",
            f"[Date \"{self.date}\"]",
            f"[Extra \"{self.extra}\"]"
        ]
        # Construir el PGN amb les dades de capçalera
        pgn = "\n".join(header_data) + "\n\n"
        
        self.pgn_display.setPlainText(pgn)

    
    def generate_full_pgn(self) -> str:
        """
        Genera el PGN complet amb les dades de capçalera i els moviments.
        """
        pass


    def generate_pgn(self):
        """
        Genera la seqüència de jugades en format PGN.
        """
        san_move = self.board.san(self.move)  # Obtenir el moviment en notació SAN
        translated_move = translate_pgn(san_move)  # Traduir les inicials
   
        # Construir la cadena PGN final
        pgn = self.pgn_display.toPlainText()
        # Afegir el número del moviment i la jugada de les blanques
        if (self.ply % 2) == 0:
            move_number = (self.ply//2) +1
            pgn += f"{move_number}.{translated_move} "
        else:
            # Afegir la jugada de les negres si existeix
            pgn += f"{translated_move} "
            
        self.pgn_display.setPlainText(pgn)
        
    
    def update_move_history(self):
        """Actualitza la història de moviments."""
        self.move_history.clear()
        for move in self.board.move_stack:
            self.move_history.addItem(move.uci())

    def save_current_game(self):
        try:
            # Verifica que tots els moviments són legals
            board = self.board.copy()
            for move in self.board.move_stack:
                if move not in board.legal_moves:
                    print(f"Error: El moviment {move.uci()} no és legal.")
                    self.info_text.append("Error: La partida conté moviments no vàlids.")
                    return
                board.push(move)

            # Genera el PGN complet
            pgn = self.generate_full_pgn()

            # Codifica les jugades en format binari
            encoded_moves = encode_moves(self.board)

            # Guarda la partida a la base de dades
            save_game(
                user_id=1,
                white=self.white_player.text(),
                black=self.black_player.text(),
                elo_white=1500,
                elo_black=1400,
                tournament=self.tournament.text(),
                location=self.location.text(),
                round_num="1",
                result=self.result.text(),
                team_white="",  # Pots afegir suport per equips si vols
                team_black="",  # Pots afegir suport per equips si vols
                eco=self.eco.text(),
                moves=encoded_moves
            )

            # Mostra un missatge d'éxit
            self.info_text.append("Partida guardada!")

        except Exception as e:
            # Captura qualsevol error i mostra'un missatge d'error
            print(f"Error al guardar la partida: {e}")
            self.info_text.append("Error: No s'ha pogut guardar la partida.")


    def load_saved_game(self):
        game = load_game(1)
        if game:
            self.nfo_text.append(f"Carregant partida {game['id']}: {game['white']} vs {game['black']}")
            decoded_moves = decode_moves(game["moves"])
            for move in decoded_moves:
                self.board.push(move)
            self.update_board_display()

    def show_header_dialog(self):
        """Mostra una finestra modal per editar les dades de capçalera."""
        dialog = HeaderDialog(self)
        if dialog.exec_() == dialog.Accepted:  # Si l'usuari accepta les dades
            headers = dialog.get_headers()
            print(f"Dades de capçalera actualitzades: {headers}")

            # Actualitza els atributs de l'aplicació
            self.white = headers["white"]
            self.elo_white = headers["elo_white"]
            self.black = headers["black"]
            self.elo_black = headers["elo_black"]
            self.tournament = headers["tournament"]
            self.location = headers["location"]
            self.result = headers["result"]
            self.eco = headers["eco"]
            self.round_num  = headers["round_num"]
            self.team_white = headers["team_white"]
            self.team_black = headers["team_black"]
            self.date = headers["date"]
            self.extra = headers["extra"]

            # Actualitza el PGN
            # self.update_pgn_display()
