import sys
from PySide6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("WrapperDirecte")
window.setGeometry(100, 100, 800, 600)  
window.show()

sys.exit(app.exec_())  
