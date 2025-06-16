import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QTimer
import pyautogui
import time
import threading

class SimultaneousClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simultaneous Clicker")
        self.setFixedSize(400, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Instructions
        instructions = QLabel("Click the button below to trigger simultaneous clicks.\nMake sure your windows are in position first!")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Click button
        self.click_button = QPushButton("Click Both Windows")
        self.click_button.clicked.connect(self.trigger_clicks)
        layout.addWidget(self.click_button)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Countdown label
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.countdown_label)
        
        # Window positions
        self.window1_pos = None
        self.window2_pos = None
        
        # Setup buttons
        self.setup_button1 = QPushButton("Set Window 1 Position")
        self.setup_button1.clicked.connect(self.set_window1_position)
        layout.addWidget(self.setup_button1)
        
        self.setup_button2 = QPushButton("Set Window 2 Position")
        self.setup_button2.clicked.connect(self.set_window2_position)
        layout.addWidget(self.setup_button2)
        
        # Position labels
        self.pos1_label = QLabel("Window 1: Not set")
        self.pos1_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pos1_label)
        
        self.pos2_label = QLabel("Window 2: Not set")
        self.pos2_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pos2_label)
        
        # Add some spacing at the bottom
        layout.addStretch()
        
        # Set up timer for countdown
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_value = 0

    def set_window1_position(self):
        self.status_label.setText("Move mouse to Window 1 position and press Enter...")
        self.setup_button1.setEnabled(False)
        self.setup_button2.setEnabled(False)
        self.click_button.setEnabled(False)
        QApplication.instance().installEventFilter(self)

    def set_window2_position(self):
        self.status_label.setText("Move mouse to Window 2 position and press Enter...")
        self.setup_button1.setEnabled(False)
        self.setup_button2.setEnabled(False)
        self.click_button.setEnabled(False)
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress and event.key() == Qt.Key_Return:
            if self.status_label.text().startswith("Move mouse to Window 1"):
                self.save_window1_position()
            elif self.status_label.text().startswith("Move mouse to Window 2"):
                self.save_window2_position()
            QApplication.instance().removeEventFilter(self)
            self.setup_button1.setEnabled(True)
            self.setup_button2.setEnabled(True)
            self.click_button.setEnabled(True)
            return True
        return super().eventFilter(obj, event)

    def save_window1_position(self):
        self.window1_pos = pyautogui.position()
        self.pos1_label.setText(f"Window 1: {self.window1_pos}")
        self.status_label.setText("Window 1 position saved!")

    def save_window2_position(self):
        self.window2_pos = pyautogui.position()
        self.pos2_label.setText(f"Window 2: {self.window2_pos}")
        self.status_label.setText("Window 2 position saved!")

    def click_window(self, position, window_num):
        if position:
            try:
                pyautogui.doubleClick(position)
                print(f"Successfully clicked window {window_num} at position {position}")
            except Exception as e:
                print(f"Error clicking window {window_num}: {str(e)}")

    def update_countdown(self):
        if self.countdown_value > 0:
            self.countdown_label.setText(str(self.countdown_value))
            self.countdown_value -= 1
        else:
            self.countdown_timer.stop()
            self.countdown_label.setText("")
            self.status_label.setText("Clicking!")
            self.click_window(self.window1_pos, 1)
            self.click_window(self.window2_pos, 2)
            self.status_label.setText("Clicks completed!")
            self.click_button.setEnabled(True)

    def trigger_clicks(self):
        if not self.window1_pos or not self.window2_pos:
            self.status_label.setText("Please set both window positions first!")
            return
            
        self.status_label.setText("Starting in 3 seconds...")
        self.click_button.setEnabled(False)
        self.countdown_value = 3
        self.countdown_timer.start(1000)  # Update every 1000ms (1 second)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set modern style
    app.setStyle("Fusion")
    
    window = SimultaneousClicker()
    window.show()
    sys.exit(app.exec()) 