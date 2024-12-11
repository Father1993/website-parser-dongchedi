import tkinter as tk
from tkinter import ttk, scrolledtext
from parser import CarParser
import json
import os
from threading import Thread
from queue import Queue

class CarParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер автомобилей DongCheDi")
        self.root.geometry("800x600")
        
        self.parser = CarParser()
        self.queue = Queue()
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.url_label = ttk.Label(main_frame, text="Введите ссылку на автомобиль:")
        self.url_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.url_entry = ttk.Entry(main_frame, width=60)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.parse_button = ttk.Button(main_frame, text="Получить данные", command=self.start_parsing)
        self.parse_button.grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.result_text = scrolledtext.ScrolledText(main_frame, height=20, width=70)
        self.result_text.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.root.after(100, self.check_queue)

    def start_parsing(self):
        url = self.url_entry.get()
        if not url:
            self.show_message("Введите URL автомобиля")
            return
            
        self.parse_button.config(state='disabled')
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        self.show_message("Начинаем парсинг...")
        Thread(target=self.parse_car).start()

    def parse_car(self):
        url = self.url_entry.get()
        try:
            car_data = self.parser.parse_car_page(url)
            if car_data:
                self.queue.put(("message", "Данные успешно получены и сохранены!\n\n"))
                self.queue.put(("message", json.dumps(car_data, ensure_ascii=False, indent=2)))
            else:
                self.queue.put(("message", "Ошибка при получении данных"))
        except Exception as e:
            self.queue.put(("message", f"Произошла ошибка: {str(e)}"))
        finally:
            self.queue.put(("finish", None))

    def check_queue(self):
        while not self.queue.empty():
            action, data = self.queue.get()
            if action == "message":
                self.show_message(data)
            elif action == "finish":
                self.finish_parsing()
        self.root.after(100, self.check_queue)

    def finish_parsing(self):
        self.progress.stop()
        self.parse_button.config(state='normal')

    def show_message(self, message):
        self.result_text.insert(tk.END, f"{message}\n")
        self.result_text.see(tk.END)

if __name__ == "__main__":
    if not os.path.exists('cars'):
        os.makedirs('cars')
    
    root = tk.Tk()
    app = CarParserApp(root)
    root.mainloop()