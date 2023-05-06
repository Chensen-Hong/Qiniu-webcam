import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk
from qiniu_api import *


class CameraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Live streaming service')
        self.geometry('500x500')
        self.resizable(False, False)

        # Create text widget
        self.result_text = tk.Text(self, height=23, width=60)
        self.result_text.pack(side='top', pady=10)

        # Create button frames
        button_frame1 = tk.Frame(self)
        button_frame2 = tk.Frame(self)

        # Create buttons
        self.start_device_button = ttk.Button(button_frame1, text='Start Device', command=self.start_device)
        self.stop_device_button = ttk.Button(button_frame1, text='Stop Device', command=self.stop_device)
        self.list_info_button = ttk.Button(button_frame2, text='List info', command=self.list_info)
        self.start_live_button = ttk.Button(button_frame2, text='Start Live', command=self.start_live)

        # Pack buttons
        self.start_device_button.pack(side='left', padx=5, pady=5)
        self.stop_device_button.pack(side='right', padx=5, pady=5)
        self.list_info_button.pack(side='left', padx=5, pady=5)
        self.start_live_button.pack(side='right', padx=5, pady=5)

        # Pack button frames
        button_frame1.pack(side='top', pady=10)
        button_frame2.pack(side='top', pady=10)

        # Pack start button

    def list_info(self):
        headers, result = listNamespacesInfo(app_key, app_sec, ns_id, stm_id)
        formatted_json = json.dumps(result, indent=4)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, formatted_json)

    def start_device(self):
        headers, result = startDevice(app_key, app_sec, ns_id, stm_id)
        if result["code"] == 200:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, 'Successful start!')
        else:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, 'Start Failed!')

    def stop_device(self):
        headers, result = stopDevice(app_key, app_sec, ns_id, stm_id)
        if result["code"] == 200:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, 'Successful stop!')
        else:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, 'Stop Failed!')

    def show_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 300))
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(self, image=photo)
        label.image = photo
        label.pack(side='top', pady=10)

    def start_live(self):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, 'Live screen being acquired!')
        start(app_key, app_sec, ns_id, stm_id)


if __name__ == '__main__':
    app_key = 'RofRgvw0K2egvDxKz7n75RJCH_R49e-hQLk_z1kk'
    app_sec = 'dMj5nG4ybGwzynCeoqopytKmsN2QDzg1QVnUF277'
    stm_id = '31011500991320020843'
    ns_id = 'qvs'

    app = CameraApp()
    app.mainloop()
