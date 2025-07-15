import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import main

email_textbox = None
password_textbox = None

script_dir = os.path.dirname(os.path.abspath(__file__))
stylesheet_path = os.path.join(script_dir, "stylesheet.css")

window = None

with open(stylesheet_path, 'r') as f:
    stylesheet = f.read()

def handle_login():
    global window, email_textbox, password_textbox
    window = QMainWindow()
    window.setWindowTitle("Login in WrapperDirecte")
    window.setGeometry(100, 100, 400, 200)
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    
    window.setCentralWidget(main_widget)
    
    email_textbox = QLineEdit(placeholderText="Email")
    password_textbox = QLineEdit(placeholderText= "Password")
    login_button = QPushButton("Log in")
    login_button.clicked.connect(handle_login_clicked)
    
    main_layout.addWidget(email_textbox)
    main_layout.addWidget(password_textbox)
    main_layout.addWidget(login_button)

    main_widget.setLayout(main_layout)

    window.setStyleSheet(stylesheet)
    window.show()

def handle_login_clicked():
    global email_textbox, password_textbox
    email = email_textbox.text()
    password = password_textbox.text()
    main.login(email, password)
    

def main_loop():
    app = QApplication(sys.argv)

    handle_login()

    sys.exit(app.exec())  

main_loop()