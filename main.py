from ui.login_window import LoginWindow
from ui.main_app_window import MainAppWindow

if __name__ == "__main__":
    while True:
        user_info = None
        
        login_app = LoginWindow()
        login_app.mainloop()
        
        if hasattr(login_app, 'user_data') and login_app.user_data:
            user_info = login_app.user_data
        else:
            break

        if user_info:
            main_app = MainAppWindow(user_info)
            main_app.mainloop()

            if not hasattr(main_app, 'logged_out') or not main_app.logged_out:
                break
        else:
            break