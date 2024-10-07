import sys
import Constants
from openai import OpenAI
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel, 
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit
)

client =  OpenAI(api_key = Constants.API_KEY)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
    # Logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('chatbot.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)

        # Input Label and Field (Styled as a modern chat input box)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a question...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;  /* Light grey background */
                border: 1px solid #D3D3D3;  /* Soft grey border */
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 16px;
                color: #333;  /* Darker grey text */
            }
        """)

        # Answer Label and Field (Styled as a chat response box)
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.answer_field.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
                padding: 10px;
                font-size: 15px;
                color: #333;
            }
        """)

        # Submit Button (Styled as a modern chat send button)
        self.submit_button = QPushButton("Send")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF; /* Dodger Blue */
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 20px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #1C86EE; /* Slightly darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #104E8B; /* Even darker blue when pressed */
            }
        """)

        # Popular Questions Group (Styled like quick-access buttons for chat)
        self.popular_questions_group = QGroupBox("Popular Questions")
        self.popular_questions_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px; /* Increase the font size */
                font-weight: bold; /* Make the font bold */
                margin-bottom: 10px; /* Add some space below the group box */
            }
        """)
        # Popular Questions Group (Styled like quick-access buttons for chat)
        self.popular_questions_group = QGroupBox("Popular Questions")
        self.popular_questions_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px; /* Increase the font size */
                font-weight: bold; /* Make the font bold */
                margin-bottom: 10px; /* Add some space below the group box */
            }
        """)
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions_layout.setContentsMargins(10, 30, 10, 10)  # Adjust top margins for the layout
        self.popular_questions = ["Why is a skincare routine important?", "When can I use retinol?", "How do I make my own routine?"]
        self.question_buttons = []

        for q in self.popular_questions:
            button = QPushButton(q)
            button.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB; /* Sky Blue */
                border: 1px solid #4682B4; /* Steel Blue Border */
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 20px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #00BFFF; /* Deep Sky Blue on hover */
            }
            QPushButton:pressed {
                background-color: #1E90FF; /* Dodger Blue when pressed */
                border: 1px solid #104E8B; /* Darker blue border on press */
            }
            """)
            button.clicked.connect(lambda _, q=q: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)

        self.popular_questions_group.setLayout(self.popular_questions_layout)


        # Layout Setup
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        layout.addWidget(self.answer_field)
        layout.addWidget(self.popular_questions_group)

        self.setLayout(layout)
        self.setWindowTitle("Skincare Advisor Bot")
        self.setGeometry(300, 300, 500, 600)

        # Connect Submit Button
        self.submit_button.clicked.connect(self.get_answer)


    def get_answer(self):
        question = self.input_field.text()
        c = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "You are a skincare expert. Answer the question in a concise manner. If the question is irrelevant to skincare, say that it is outside your scope"},
                {"role": "user", "content": f'{question}'}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = c.choices[0].message.content.strip()
        self.answer_field.setText(answer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
