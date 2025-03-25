import sys
from gui.main_pqt import Escacs
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
window = Escacs()
window.show()
sys.exit(app.exec())
