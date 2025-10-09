import os
from dotenv import load_dotenv

load_dotenv(".env")

# Настройки для подключения к базе данных
DB_SETTINGS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Названия
APP_NAME = "ООО «Обувь»"
LOGIN_WINDOW_TITLE = "Авторизация - {app_name}"
MAIN_WINDOW_TITLE_FORMAT = "Информационная система - {app_name} ({role_name})"

# Геометрия окон
LOGIN_WINDOW_GEOMETRY = "400x250"
MAIN_WINDOW_GEOMETRY = "1024x768"

# Цвета
COLOR_MAIN_BG = "#FFFFFF"
COLOR_ADDITIONAL_BG = "#7FFF00"
COLOR_ACCENT = "#00FA9A"
COLOR_DISCOUNT_BG = "#2E8B57"

# Шрифты
FONT_PRIMARY = ("Times New Roman", 12)
FONT_PRIMARY_BOLD = ("Times New Roman", 12, "bold")
FONT_TITLE = ("Times New Roman", 16, "bold")
FONT_CARD_TITLE = ("Times New Roman", 14, "bold")
FONT_CARD_BODY = ("Times New Roman", 11)
FONT_CARD_ACCENT = ("Times New Roman", 12, "bold")

# Пути
RESOURCES_DIR = "./resources/"
LOGO_PATH = os.path.join(RESOURCES_DIR, "icon.jpg")
ICON_PATH = os.path.join(RESOURCES_DIR, "icon.ico")
PLACEHOLDER_IMAGE_PATH = os.path.join(RESOURCES_DIR, "picture.png")
PRODUCT_IMAGES_DIR = os.path.join(RESOURCES_DIR, "product_images/")

# Размеры изображений
LOGO_SIZE = (250, 60)
PRODUCT_IMAGE_SIZE = (300, 200)