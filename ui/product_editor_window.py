import os
import shutil
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import config
import database


def generate_sku():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class ProductEditorWindow(tk.Toplevel):
    def __init__(self, parent, callback, product_data=None):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.product_data = dict(product_data) if product_data else None
        self.is_edit_mode = self.product_data is not None
        self.selected_image_path = (self.product_data.get("image_path") if self.is_edit_mode else None)

        self.title("Редактирование товара" if self.is_edit_mode else "Добавление товара")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(bg=config.COLOR_MAIN_BG)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._setup_styles()
        self._create_widgets()

        if self.is_edit_mode:
            self._populate_data()
        else:
            self.entries["product_sku"].insert(0, generate_sku())
            self.entries["product_sku"].config(state="readonly")

        self.after(10, self._make_modal)

    def _make_modal(self):
        self.grab_set()
        self.transient(self.parent)
        self.wait_window(self)

    def _setup_styles(self):
        style = ttk.Style(self)
        style.configure("TLabel", font=config.FONT_PRIMARY, background=config.COLOR_MAIN_BG)
        style.configure("TButton", font=config.FONT_PRIMARY, padding=5)
        style.configure("TEntry", font=config.FONT_PRIMARY)
        style.configure("TFrame", background=config.COLOR_MAIN_BG)
        style.configure("Accent.TButton", background=config.COLOR_ACCENT)

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        fields = {
            "Артикул": "product_sku", "Наименование": "product_name",
            "Цена": "price", "Скидка (%)": "current_discount",
            "Кол-во на складе": "stock_quantity", "Категория": "category_name",
            "Производитель": "manufacturer_name", "Поставщик": "supplier_name"
        }
        self.entries = {}
        for label_text, key in fields.items():
            row_frame = ttk.Frame(main_frame)
            row_frame.pack(fill='x', pady=2)
            ttk.Label(row_frame, text=label_text, width=20).pack(side='left')
            entry = ttk.Entry(row_frame)
            entry.pack(side='left', expand=True, fill='x')
            self.entries[key] = entry

        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill='both', pady=(10, 2), expand=True)
        ttk.Label(desc_frame, text="Описание", width=20).pack(side='left', anchor='n', pady=3)
        self.desc_text = tk.Text(desc_frame, height=4, font=config.FONT_PRIMARY,
                                 borderwidth=1, relief="solid")
        self.desc_text.pack(side='left', expand=True, fill='both')

        img_frame = ttk.Frame(main_frame)
        img_frame.pack(fill='x', pady=(10, 2))
        ttk.Button(img_frame, text="Выбрать изображение...", command=self._choose_image).pack(side='left')
        self.image_label = ttk.Label(img_frame, text="Файл не выбран", anchor="w")
        self.image_label.pack(side='left', expand=True, fill='x', padx=10)

        self._create_buttons(main_frame)

    def _create_buttons(self, parent):
        button_frame = ttk.Frame(parent, padding=(0, 20, 0, 0))
        button_frame.pack(fill='x', side='bottom')
        ttk.Button(button_frame, text="Сохранить", command=self.save, style="Accent.TButton").pack(side='left', expand=True, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.on_close).pack(side='left', expand=True, padx=5)
        if self.is_edit_mode:
            ttk.Button(button_frame, text="Удалить", command=self.delete).pack(side='right', expand=True, padx=5)

    def _populate_data(self):
        for key, entry in self.entries.items():
            value = self.product_data.get(key)
            entry.insert(0, str(value) if value is not None else "")
        self.entries["product_sku"].config(state="readonly")
        description = self.product_data.get("description")
        if description:
            self.desc_text.insert("1.0", description)
        if self.selected_image_path:
            self.image_label.config(text=os.path.basename(self.selected_image_path))

    def _choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path: return
        os.makedirs(config.PRODUCT_IMAGES_DIR, exist_ok=True)
        filename = os.path.basename(file_path)
        dest_path = os.path.join(config.PRODUCT_IMAGES_DIR, filename)
        try:
            shutil.copy(file_path, dest_path)
            self.selected_image_path = dest_path
            self.image_label.config(text=filename)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать файл: {e}")

    def save(self):
        new_data = {key: entry.get() for key, entry in self.entries.items()}
        new_data["description"] = self.desc_text.get("1.0", tk.END).strip()
        new_data["image_path"] = self.selected_image_path
        if not new_data.get("product_sku") or not new_data.get("product_name"):
            messagebox.showerror("Ошибка", "Артикул и наименование обязательны.")
            return
        try:
            if self.is_edit_mode:
                database.update_product(new_data)
            else:
                database.add_product(new_data)
            self.on_close()
        except Exception as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить данные:\n{e}")

    def delete(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены?"):
            try:
                database.delete_product(self.product_data["product_sku"])
                self.on_close()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить товар:\n{e}")

    def on_close(self):
        self.callback()
        self.destroy()