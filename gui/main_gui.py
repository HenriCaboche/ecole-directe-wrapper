import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QLineEdit

window = None

def handle_login():
    global window
    window = QMainWindow()
    window.setWindowTitle("Login in WrapperDirecte")
    window.setGeometry(100, 100, 800, 600)
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    
    window.setCentralWidget(main_widget)
    
    email_textbox = QLineEdit(placeholderText="Email")
    password_textbox = QLineEdit(placeholderText= "Password")
    
    main_layout.addWidget(email_textbox)
    main_layout.addWidget(password_textbox)
    main_widget.setLayout(main_layout)

    window.show()


def main():
    app = QApplication(sys.argv)

    handle_login()

    sys.exit(app.exec())  

main()