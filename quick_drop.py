import sys
import os
from pynput import keyboard
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QGraphicsDropShadowEffect

class HotkeySignaler(QObject):
    toggle_signal = pyqtSignal()

class QuickDropNotepad(QWidget):
    def __init__(self):
        super().__init__()
        
        # Transparent background, no border, stays on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Get screen width and define window size
        screen = QApplication.primaryScreen().geometry()
        self.W = int(screen.width() * 0.4)  # 40% of screen width
        self.H = int(screen.height() * 0.5) # 50% of screen height
        
        # Start hidden off-screen (above the top edge)
        self.hidden_y = -self.H - 50
        self.visible_y = 0
        self.x_pos = int((screen.width() - self.W) / 2)
        
        self.setGeometry(self.x_pos, self.hidden_y, self.W, self.H)
        
        self.is_visible = False
        self.setup_ui()
        
        # Setup Animation
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutExpo)
        
        # Setup Global Hotkey via Signaler
        self.signaler = HotkeySignaler()
        self.signaler.toggle_signal.connect(self.toggle)
        
        def on_activate():
            self.signaler.toggle_signal.emit()

        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+<space>': on_activate
        })
        self.hotkey_listener.start()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        
        # Main text area
        self.text_area = QTextEdit()
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 2px solid #444;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                border-top: none;
                padding: 15px;
            }
        """)
        font = QFont("Segoe UI", 12)
        self.text_area.setFont(font)
        self.text_area.setPlaceholderText("Type your quick notes here... (Press Esc to hide, Ctrl+Shift+Space to toggle)")
        
        # Add a subtle drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.text_area.setGraphicsEffect(shadow)
        
        layout.addWidget(self.text_area)
        
        # Load saved notes if any
        self.save_file = os.path.join(os.path.dirname(__file__), "notes.txt")
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as f:
                self.text_area.setPlainText(f.read())
                
        # Save automatically when typing
        self.text_area.textChanged.connect(self.save_notes)

    def save_notes(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            f.write(self.text_area.toPlainText())

    def toggle(self):
        if self.is_visible:
            self.anim.setStartValue(QRect(self.x_pos, self.visible_y, self.W, self.H))
            self.anim.setEndValue(QRect(self.x_pos, self.hidden_y, self.W, self.H))
            self.is_visible = False
            self.anim.start()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
            self.text_area.setFocus()
            self.anim.setStartValue(QRect(self.x_pos, self.hidden_y, self.W, self.H))
            self.anim.setEndValue(QRect(self.x_pos, self.visible_y, self.W, self.H))
            self.is_visible = True
            self.anim.start()

    def keyPressEvent(self, event):
        # Allow Esc to hide the window
        if event.key() == Qt.Key_Escape and self.is_visible:
            self.toggle()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Needs to stay open in background
    app.setQuitOnLastWindowClosed(False)
    
    notepad = QuickDropNotepad()
    # Ensure it's active in the system
    print("Quick-Drop Notepad is running. Press Ctrl+Shift+Space to toggle.")
    sys.exit(app.exec_())
