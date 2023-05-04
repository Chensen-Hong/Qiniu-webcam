import tkinter as tk
from tkinter import ttk
import threading
from pprint import pprint
from PIL import Image, ImageTk
from qiniu_api import *


class CameraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Camera App')
        self.geometry('400x400')
        self.resizable(False, False)

        # Create buttons
        self.start_device_button = ttk.Button(self, text='Start Device', command=self.start_device)
        self.stop_device_button = ttk.Button(self, text='Stop Device', command=self.stop_device)
        self.start_streams_button = ttk.Button(self, text='Start Streams', command=self.start_streams)
        self.stop_streams_button = ttk.Button(self, text='Stop Streams', command=self.stop_streams)

        # Pack buttons
        self.start_device_button.pack(side='top', pady=10)
        self.stop_device_button.pack(side='top', pady=10)
        self.start_streams_button.pack(side='top', pady=10)
        self.stop_streams_button.pack(side='top', pady=10)

        # Create text widget
        self.result_text = tk.Text(self, height=10, width=40)
        self.result_text.pack(side='top', pady=10)

    def start_device(self):
        headers, result = startDevice(app_key, app_sec, ns_id, stm_id)
        self.update_result(headers, result)

    def stop_device(self):
        headers, result = stopDevice(app_key, app_sec, ns_id, stm_id)
        self.update_result(headers, result)

    def start_streams(self):
        headers, result = enableStreams(app_key, app_sec, ns_id, stm_id)
        self.update_result(headers, result)

    def stop_streams(self):
        headers, result = stopStreams(app_key, app_sec, ns_id, stm_id)
        self.update_result(headers, result)

    def update_result(self, headers, result):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, 'Headers:\n')
        self.result_text.insert(tk.END, pprint(headers, indent=4))
        self.result_text.insert(tk.END, '\n\nResult:\n')
        self.result_text.insert(tk.END, pprint(result, indent=4))

    def show_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 300))
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(self, image=photo)
        label.image = photo
        label.pack(side='top', pady=10)


if __name__ == '__main__':
    app_key = 'RofRgvw0K2egvDxKz7n75RJCH_R49e-hQLk_z1kk'
    app_sec = 'dMj5nG4ybGwzynCeoqopytKmsN2QDzg1QVnUF277'
    stm_id = '31011500991320020843'
    ns_id = 'qvs'

    app = CameraApp()
    app.mainloop()
