import sys
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSlider

# 연타할 키 (예: 'x' 키를 연타)
key_to_press = KeyCode.from_char('x')  # 'x' 키로 설정

# 키보드 컨트롤러 초기화
controller = Controller()

# X 키가 눌린 상태 추적
x_key_pressed = False

# GUI 업데이트를 위한 변수
status_text = "정지"
delay = 0.05  # 기본 연타 간격 (초)

# 연타 함수
def press_key():
    global status_text, delay
    while True:
        if x_key_pressed:
            # 'x' 키를 눌러줌, 화면에 출력되지 않도록 처리
            controller.press(key_to_press)
            controller.release(key_to_press)
            status_text = "작동"
        else:
            status_text = "정지"
        time.sleep(delay)  # 슬라이더 값에 따라 연타 간격 조정

# 키보드 리스너 정의
def on_press(key):
    global x_key_pressed
    try:
        if key == keyboard.Key.esc:
            # ESC 키를 누르면 프로그램 종료
            return False
        if key == keyboard.KeyCode.from_char('x'):
            x_key_pressed = True  # x 키가 눌렸을 때 연타 시작
            status_text = "작동"
    except AttributeError:
        pass

def on_release(key):
    global x_key_pressed
    if key == keyboard.KeyCode.from_char('x'):
        x_key_pressed = False  # x 키에서 손을 떼면 연타 멈춤

# GUI 클래스 정의
class KeyPressApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("키 연타 프로그램")
        self.setGeometry(100, 100, 300, 200)
        
        self.status_label = QLabel("정지", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 슬라이더 추가 (연타 속도 조절)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(1, 100)  # 1~100 범위 (밀리초 단위로 설정)
        self.slider.setValue(50)  # 기본값 50 (슬라이더 범위의 중간)
        self.slider.valueChanged.connect(self.update_delay)
        
        # 슬라이더의 레이블 추가
        self.slider_label = QLabel("연타 속도: 50ms", self)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.slider_label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)
        
        # 키보드 리스너 시작
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

        # 키 연타 함수 스레드로 실행
        self.thread = threading.Thread(target=press_key)
        self.thread.daemon = True
        self.thread.start()

        # 타이머로 상태 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)  # 100ms마다 상태 업데이트

    def update_delay(self):
        # 슬라이더 값을 연타 간격에 반영 (1-100 -> 0.01s-1.00s)
        global delay
        delay = self.slider.value() / 1000.0  # 슬라이더 값에 맞는 밀리초로 변환
        self.slider_label.setText(f"연타 속도: {self.slider.value()}ms")

    def update_status(self):
        self.status_label.setText(status_text)
        self.status_label.repaint()

# PyQt6 애플리케이션 설정
def main():
    app = QApplication(sys.argv)
    window = KeyPressApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
