import sys
import os
from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QLabel
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import main

id_textbox: Optional[QLineEdit] = None
password_textbox: Optional[QLineEdit] = None
responses = None

script_dir = os.path.dirname(os.path.abspath(__file__))
stylesheet_path = os.path.join(script_dir, "stylesheet.css")

window = None
question_window = None

with open(stylesheet_path, 'r') as f:
    stylesheet = f.read()

def handle_login():
    global window, id_textbox, password_textbox
    window = QMainWindow()
    window.setWindowTitle("Login in WrapperDirecte")
    window.setGeometry(100, 100, 400, 200)
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    
    window.setCentralWidget(main_widget)
    
    id_textbox = QLineEdit(placeholderText="ID")
    password_textbox = QLineEdit(placeholderText= "Password")
    login_button = QPushButton("Log in")
    login_button.clicked.connect(handle_login_clicked)
    
    main_layout.addWidget(id_textbox)
    main_layout.addWidget(password_textbox)
    main_layout.addWidget(login_button)

    main_widget.setLayout(main_layout)

    window.setStyleSheet(stylesheet)
    window.show()

def handle_login_clicked():
    global id_textbox, password_textbox, window, question_window, responses
    user_id = id_textbox.text()                  #type:ignore
    password = password_textbox.text()            #type:ignore
    questions = main.second_auth(user_id, password) #type:ignore
    window.close() #type:ignore
    question_window = QMainWindow()
    question_window.setWindowTitle("Login to WrapperDirecte")
    question_window.setGeometry(100,100,500,100)

    main_widget = QWidget()
    main_layout = QVBoxLayout()

    main_widget.setLayout(main_layout)
    question = questions[0]
    question_label = QLabel(question)
    
    responses = QComboBox()
    responses.addItems(questions[1])
    
    continue_button = QPushButton('Continue')
    continue_button.clicked.connect(handle_question_awnser)
    
    main_layout.addWidget(question_label)
    main_layout.addWidget(responses)
    main_layout.addWidget(continue_button)
    
    question_window.setStyleSheet(stylesheet)
    question_window.setCentralWidget(main_widget)
    question_window.show()

def handle_question_awnser():
    global responses, id_textbox, password_textbox
    response = responses.currentText() #type:ignore
    user_id = id_textbox.text() #type:ignore
    password = password_textbox.text() #type:ignore
    is_correct = main.final_login(response, user_id, password) #type:ignore
    if is_correct:
        print("Should call 'handle_continue_to_app'")
    else:
        print('Should quit the app')
def main_loop():
    app = QApplication(sys.argv)

    handle_login()

    sys.exit(app.exec())  

main_loop()