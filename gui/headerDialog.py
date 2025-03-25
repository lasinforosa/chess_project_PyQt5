from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class HeaderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dades de la Partida")
        self.setFixedSize(400, 600)

        # Crear el formulari
        layout = QFormLayout()

        # Camps del formulari
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
        self.extra = QLineEdit("")  # Text extra

        # Afegir els camps al formulari
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
        layout.addRow("Extra:", self.extra)

        # Botó d'acceptació
        ok_button = QPushButton("Acceptar")
        ok_button.clicked.connect(self.accept)
        layout.addRow(ok_button)

        self.setLayout(layout)

    def get_headers(self):
        """Retorna les dades introduïdes per l'usuari."""
        return {
            "white": self.white_player.text(),
            "black": self.black_player.text(),
            "tournament": self.tournament.text(),
            "location": self.location.text(),
            "result": self.result.text(),
            "eco": self.eco.text(),
            "round_num": self.round_num.text(),
            "elo_white": self.elo_white.text(),
            "elo_black": self.elo_black.text(),
            "team_white": self.team_white.text(),
            "team_black": self.team_black.text(),
            "date": self.date.text(),
            "extra": self.extra.text()
        }



       
