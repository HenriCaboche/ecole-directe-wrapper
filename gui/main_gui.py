import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton

script_dir = os.path.dirname(os.path.abspath(__file__))
stylesheet_path = os.path.join(script_dir, "stylesheet.css")

window = None

with open(stylesheet_path, 'r') as f:
    stylesheet = f.read()

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
    login_button = QPushButton("Log in")

    main_layout.addWidget(email_textbox)
    main_layout.addWidget(password_textbox)
    main_layout.addWidget(login_button)

    main_widget.setLayout(main_layout)

    window.setStyleSheet(stylesheet)
    window.show()


def main():
    app = QApplication(sys.argv)

    handle_login()

    sys.exit(app.exec())  

main()