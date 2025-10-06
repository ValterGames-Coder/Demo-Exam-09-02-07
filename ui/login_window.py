import os
import tkinter as tk
from tkinter import messagebox, ttk

import config
import database
from ui.main_app_window import MainAppWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(config.LOGIN_WINDOW_TITLE.format(app_name=config.APP_NAME))
        self.geometry(config.LOGIN_WINDOW_GEOMETRY)
        self.resizable(False, False)
        self.configure(bg=config.COLOR_MAIN_BG)

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.configure(
            "TLabel", font=config.FONT_PRIMARY, background=config.COLOR_MAIN_BG
        )
        style.configure("TButton", font=config.FONT_PRIMARY, padding=5)
        style.configure("TEntry", font=config.FONT_PRIMARY)
        style.configure("TFrame", background=config.COLOR_MAIN_BG)
        style.configure(
            "Accent.TButton", background=config.COLOR_ACCENT, foreground="black"
        )

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Логин:").pack(pady=(0, 5))
        self.login_entry = ttk.Entry(main_frame, width=30)
        self.login_entry.pack()

        ttk.Label(main_frame, text="Пароль:").pack(pady=(10, 5))
        self.password_entry = ttk.Entry(main_frame, show="*", width=30)
        self.password_entry.pack()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill='x', side='bottom')

        login_button = ttk.Button(
            button_frame,
            text="Войти",
            command=self.attempt_login,
            style="Accent.TButton"
        )
        login_button.pack(side='left', expand=True, padx=5)

        guest_button = ttk.Button(
            button_frame, text="Войти как гость", command=self.login_as_guest
        )
        guest_button.pack(side='right', expand=True, padx=5)

    def attempt_login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror(
                "Ошибка", "Логин и пароль не могут быть пустыми."
            )
            return

        user_data = database.check_user(login, password)
        if user_data:
            self.open_main_window(user_data)
        else:
            messagebox.showerror("Ошибка входа", "Неверный логин или пароль.")

    def login_as_guest(self):
        guest_data = {"full_name": "Гость", "role_name": "Гость"}
        self.open_main_window(guest_data)

    def open_main_window(self, user_data):
        self.destroy()
        app = MainAppWindow(user_data)

        if os.path.exists(config.ICON_PATH):
            try:
                app.iconbitmap(default=config.ICON_PATH)
            except tk.TclError:
                print("Ошибка установки иконки для главного окна.")
        app.mainloop()