import sys
import os
from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QLabel, QTextEdit, QHBoxLayout, QGridLayout, QScrollArea
from PySide6.QtCore import Qt
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import main


debug_show_password = True

id_textbox: Optional[QLineEdit] = None
password_textbox: Optional[QLineEdit] = None
responses = None

script_dir = os.path.dirname(os.path.abspath(__file__))
stylesheet_path = os.path.join(script_dir, "stylesheet.css")

window = None
question_window = None
wrong_awnser_label = None
main_window = None

user_id_global = None
token_global = None

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
    
    id_textbox = QLineEdit()
    id_textbox.setPlaceholderText("ID")
    password_textbox = QLineEdit()
    password_textbox.setPlaceholderText("Password")
    login_button = QPushButton("Log in")
    login_button.clicked.connect(handle_login_clicked)
    if not debug_show_password:
        password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
    
    main_layout.addWidget(id_textbox)
    main_layout.addWidget(password_textbox)
    main_layout.addWidget(login_button)

    
    main_widget.setLayout(main_layout)

    window.setStyleSheet(stylesheet)
    window.show()

def handle_login_clicked():
    global id_textbox, password_textbox, window, question_window, responses, wrong_awnser_label
    user_id = id_textbox.text()                     #type:ignore
    password = password_textbox.text()              #type:ignore
    questions = main.second_auth(user_id, password) #type:ignore
    if questions == False or not questions:
        print("Unable to connect, Maybe wrong password ?")
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
    
    wrong_awnser_label = QLabel("Wrong awnser, try again.")
    wrong_awnser_label.hide()
    wrong_awnser_label.setObjectName("Error")
    
    main_layout.addWidget(question_label)
    main_layout.addWidget(responses)
    main_layout.addWidget(continue_button)
    main_layout.addWidget(wrong_awnser_label)
    
    
    question_window.setStyleSheet(stylesheet)
    question_window.setCentralWidget(main_widget)
    question_window.show()

def handle_question_awnser():
    global responses, id_textbox, password_textbox, question_window, user_id_global, token_global
    response = responses.currentText() #type:ignore
    user_id = id_textbox.text() #type:ignore
    password = password_textbox.text() #type:ignore
    is_correct = main.final_login(response, user_id, password) #type:ignore
    if is_correct[0]:
        user_id_global = is_correct[1]
        token_global = is_correct[2]
        question_window.close()
        handle_main_app()
    else:
        print("Wrong awnser")
        wrong_awnser_label.show()

def handle_main_app():
    global main_window
    main_window = QMainWindow()
    main_window.setWindowTitle("WrapperDirecte")
    main_window.setGeometry(100, 100, 1000, 700)
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    
    # Navigation buttons
    nav_layout = QHBoxLayout()
    
    timetable_btn = QPushButton("Timetable")
    timetable_btn.clicked.connect(show_timetable)
    
    homework_btn = QPushButton("Homework")
    homework_btn.clicked.connect(show_homework)
    
    notes_btn = QPushButton("Notes")
    notes_btn.clicked.connect(show_notes)
    
    moyennes_btn = QPushButton("Moyennes")
    moyennes_btn.clicked.connect(show_moyennes)
    
    nav_layout.addWidget(timetable_btn)
    nav_layout.addWidget(homework_btn)
    nav_layout.addWidget(notes_btn)
    nav_layout.addWidget(moyennes_btn)
    
    main_layout.addLayout(nav_layout)
    
    # Content area - will be replaced with grid for timetable
    content_widget = QWidget()
    content_widget.setObjectName("contentWidget")
    main_layout.addWidget(content_widget)
    
    main_widget.setLayout(main_layout)
    main_window.setCentralWidget(main_widget)
    main_window.setStyleSheet(stylesheet)
    main_window.show()
    
    # Show timetable by default
    show_timetable()

def show_timetable():
    global user_id_global, token_global, main_window
    
    # Get or create content widget
    content_widget = main_window.findChild(QWidget, "contentWidget")
    
    # Clear existing layout
    if content_widget.layout():
        QWidget().setLayout(content_widget.layout())
    
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_widget = QWidget()
    grid = QGridLayout()
    
    try:
        import datetime
        timetable_data = main.timetable(user_id_global, token_global)
        
        # Parse timetable data
        events = []
        i = 0
        while i < len(timetable_data):
            if '--' in timetable_data[i+1]:
                subject = timetable_data[i]
                time_range = timetable_data[i+1]
                events.append({'subject': subject, 'time': time_range})
                i += 2
            else:
                i += 1
        
        # Color palette for subjects
        colors = [
            '#D8B4E2', '#B4D8E8', '#FFD6A5', '#FFB3BA', '#FFDFBA',
            '#FFFFBA', '#BAFFC9', '#BAE1FF', '#C9C9FF', '#FFB3E6'
        ]
        
        # Group by day and time slot
        schedule = {}
        for event in events:
            time = event['time']
            if time not in schedule:
                schedule[time] = []
            schedule[time].append(event['subject'])
        
        # Create grid
        time_slots = sorted(schedule.keys())
        row = 0
        
        for time_slot in time_slots:
            # Time label
            time_label = QLabel(time_slot)
            time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            time_label.setStyleSheet("font-weight: bold; padding: 10px;")
            grid.addWidget(time_label, row, 0)
            
            # Subjects
            col = 1
            for subject in schedule[time_slot]:
                subject_label = QLabel(subject)
                subject_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                subject_label.setWordWrap(True)
                subject_label.setMinimumSize(150, 80)
                subject_label.setStyleSheet(f"""
                    background-color: {colors[col % len(colors)]};
                    border: 2px solid #4C566A;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 12px;
                    color: #2E3440;
                """)
                grid.addWidget(subject_label, row, col)
                col += 1
            
            row += 1
        
        scroll_widget.setLayout(grid)
        scroll.setWidget(scroll_widget)
        
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        content_widget.setLayout(layout)
        
    except Exception as e:
        error_label = QLabel(f"Error loading timetable: {e}")
        layout = QVBoxLayout()
        layout.addWidget(error_label)
        content_widget.setLayout(layout)
        import traceback
        print(traceback.format_exc())

def show_homework():
    global user_id_global, token_global, main_window
    content_widget = main_window.findChild(QWidget, "contentWidget")
    
    # Clear existing layout
    if content_widget.layout():
        QWidget().setLayout(content_widget.layout())
    
    content_area = QTextEdit()
    content_area.setReadOnly(True)
    content_area.append("Loading homework...\n")
    
    try:
        homework_data = main.homework(user_id_global, token_global)
        content_area.clear()
        content_area.append("=== HOMEWORK ===\n\n")
        for item in homework_data:
            content_area.append(item)
    except Exception as e:
        content_area.clear()
        content_area.append(f"Error loading homework: {e}")
    
    layout = QVBoxLayout()
    layout.addWidget(content_area)
    content_widget.setLayout(layout)

def show_notes():
    global user_id_global, token_global, main_window
    content_widget = main_window.findChild(QWidget, "contentWidget")
    
    # Clear existing layout
    if content_widget.layout():
        QWidget().setLayout(content_widget.layout())
    
    content_area = QTextEdit()
    content_area.setReadOnly(True)
    content_area.append("Loading notes...\n")
    
    try:
        notes_data = main.notes(user_id_global, token_global)
        content_area.clear()
        content_area.append("=== NOTES ===\n\n")
        content_area.append(str(notes_data))
    except Exception as e:
        content_area.clear()
        content_area.append(f"Error loading notes: {e}")
    
    layout = QVBoxLayout()
    layout.addWidget(content_area)
    content_widget.setLayout(layout)

def show_moyennes():
    global user_id_global, token_global, main_window
    content_widget = main_window.findChild(QWidget, "contentWidget")
    
    # Clear existing layout
    if content_widget.layout():
        QWidget().setLayout(content_widget.layout())
    
    content_area = QTextEdit()
    content_area.setReadOnly(True)
    content_area.append("Loading moyennes...\n")
    
    try:
        moyennes_data = main.moyennes(user_id_global, token_global)
        content_area.clear()
        content_area.append("=== MOYENNES ===\n\n")
        for course in moyennes_data:
            if 'effectif' in course and course['effectif']:
                content_area.append(f"{course['name']}: {course['rang']}/{course['effectif']} ({course['moyenne']}-{course['moyenneClasse']})\n")
            else:
                content_area.append(f"{course['name']}: ({course['moyenne']}-{course['moyenneClasse']})\n")
    except Exception as e:
        content_area.clear()
        content_area.append(f"Error loading moyennes: {e}")
    
    layout = QVBoxLayout()
    layout.addWidget(content_area)
    content_widget.setLayout(layout)

def main_loop():
    app = QApplication(sys.argv)

    handle_login()

    sys.exit(app.exec())  

main_loop()