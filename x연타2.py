import sys
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode
import tkinter as tk

# 연타할 키 (예: 'x' 키를 연타)
key_to_press = KeyCode.from_char('x')  # 'x' 키로 설정

# 키보드 컨트롤러 초기화
controller = Controller()

# X 키가 눌린 상태 추적
x_key_pressed = False

# GUI 업데이트를 위한 변수
status_text = "정지"
delay = 0.02  # 기본 연타 간격 (초)

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
            update_status_text("작동")
    except AttributeError:
        pass

def on_release(key):
    global x_key_pressed
    if key == keyboard.KeyCode.from_char('x'):
        x_key_pressed = False  # x 키에서 손을 떼면 연타 멈춤
        update_status_text("정지")

# GUI 업데이트 함수
def update_status_text(text):
    # Tkinter 메인 루프에서 GUI 업데이트
    status_label.config(text=text)

# 슬라이더 값 업데이트 함수
def update_delay(val):
    global delay
    delay = int(val) / 1000.0  # 슬라이더 값에 맞는 밀리초로 변환
    slider_label.config(text=f"연타 속도: {val}ms")

# Tkinter GUI 클래스
class KeyPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("키 연타 프로그램")
        
        # 상태 레이블
        global status_label
        status_label = tk.Label(root, text="정지", font=("Arial", 16))
        status_label.pack(pady=20)
        
        # 슬라이더 레이블
        global slider_label
        slider_label = tk.Label(root, text="연타 속도: 50ms", font=("Arial", 12))
        slider_label.pack()

        # 슬라이더 추가 (연타 속도 조절)
        self.slider = tk.Scale(root, from_=1, to=100, orient="horizontal", command=self.update_delay)
        self.slider.set(50)  # 기본값 50 (슬라이더 범위의 중간)
        self.slider.pack(pady=10)

        # 키보드 리스너 시작
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

        # 키 연타 함수 스레드로 실행
        self.thread = threading.Thread(target=press_key)
        self.thread.daemon = True
        self.thread.start()

    def update_delay(self, val):
        global delay
        delay = int(val) / 1000.0  # 슬라이더 값에 맞는 밀리초로 변환
        slider_label.config(text=f"연타 속도: {val}ms")
    
    # GUI 업데이트가 안전하게 이루어지도록 Tkinter 메인 루프에 등록
    def update_gui(self):
        self.root.after(100, self.update_gui)  # 100ms마다 호출
        update_status_text(status_text)

# Tkinter 애플리케이션 설정
def main():
    root = tk.Tk()
    app = KeyPressApp(root)
    root.geometry("300x250")

    # Tkinter 메인 루프에서 GUI 업데이트를 위한 메서드 호출
    app.update_gui()

    root.mainloop()

if __name__ == "__main__":
    main()
