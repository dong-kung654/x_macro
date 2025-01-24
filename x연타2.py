import sys
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode
import tkinter as tk


key_to_press = KeyCode.from_char('x')  


controller = Controller()

x_key_pressed = False


status_text = "정지"
delay = 0.02  


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
            update_status_text("작동")
    except AttributeError:
        pass

def on_release(key):
    global x_key_pressed
    if key == keyboard.KeyCode.from_char('x'):
        x_key_pressed = False  
        update_status_text("정지")


def update_status_text(text):
    status_label.config(text=text)

def update_delay(val):
    global delay
    delay = int(val) / 1000.0  
    slider_label.config(text=f"연타 속도: {val}ms")


class KeyPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("키 연타 프로그램")
        
        global status_label
        status_label = tk.Label(root, text="정지", font=("Arial", 16))
        status_label.pack(pady=20)
        
        global slider_label
        slider_label = tk.Label(root, text="연타 속도: 50ms", font=("Arial", 12))
        slider_label.pack()

        self.slider = tk.Scale(root, from_=1, to=100, orient="horizontal", command=self.update_delay)
        self.slider.set(50)  
        self.slider.pack(pady=10)

        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()


        self.thread = threading.Thread(target=press_key)
        self.thread.daemon = True
        self.thread.start()

    def update_delay(self, val):
        global delay
        delay = int(val) / 1000.0  
        slider_label.config(text=f"연타 속도: {val}ms")
    

    def update_gui(self):
        self.root.after(100, self.update_gui)  
        update_status_text(status_text)

def main():
    root = tk.Tk()
    app = KeyPressApp(root)
    root.geometry("300x250")
    app.update_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
