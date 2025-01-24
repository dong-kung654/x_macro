import sys
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSlider

key_to_press = KeyCode.from_char('x')  
controller = Controller()

x_key_pressed = False

status_text = "정지"
delay = 0.05  

def press_key():
    global status_text, delay
    while True:
        if x_key_pressed:
            
            controller.press(key_to_press)
            controller.release(key_to_press)
            status_text = "작동"
        else:
            status_text = "정지"
        time.sleep(delay) 


def on_press(key):
    global x_key_pressed
    try:
        if key == keyboard.Key.esc:
            
            return False
        if key == keyboard.KeyCode.from_char('x'):
            x_key_pressed = True  
            status_text = "작동"
    except AttributeError:
        pass

def on_release(key):
    global x_key_pressed
    if key == keyboard.KeyCode.from_char('x'):
        x_key_pressed = False  


class KeyPressApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("키 연타 프로그램")
        self.setGeometry(100, 100, 300, 200)
        
        self.status_label = QLabel("정지", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(1, 100) 
        self.slider.setValue(50)  
        self.slider.valueChanged.connect(self.update_delay)
        
        
        self.slider_label = QLabel("연타 속도: 50ms", self)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.slider_label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)
        
       
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

        
        self.thread = threading.Thread(target=press_key)
        self.thread.daemon = True
        self.thread.start()

      
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)  

    def update_delay(self):
        
        global delay
        delay = self.slider.value() / 1000.0  
        self.slider_label.setText(f"연타 속도: {self.slider.value()}ms")

    def update_status(self):
        self.status_label.setText(status_text)
        self.status_label.repaint()


def main():
    app = QApplication(sys.argv)
    window = KeyPressApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
