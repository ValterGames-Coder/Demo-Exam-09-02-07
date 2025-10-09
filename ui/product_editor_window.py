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
    def __init__(self, parent, callback, product_sku=None):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.product_data = database.get_full_product_info(product_sku) if product_sku else None
        self.is_edit_mode = self.product_data is not None
        self.selected_image_path = self.product_data.get("image_path") if self.is_edit_mode else None
        
        self.title("Редактирование товара" if self.is_edit_mode else "Добавление товара")
        self.geometry("600x600")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.categories = database.get_categories()
        self.manufacturers = database.get_manufacturers()
        self.suppliers = database.get_suppliers()
        
        self.widgets = {}
        self._create_widgets()
        if self.is_edit_mode:
            self._populate_data()
        else:
            self.widgets["product_sku"].insert(0, generate_sku())
            self.widgets["product_sku"].config(state="readonly")
        
  
        self.transient(parent)
        self.after(0, self._make_modal)

    def _make_modal(self):
        try:
            self.wait_visibility()
            self.grab_set()
            self.focus_set()
        except Exception as e:
            print(f"Ошибка modal-граб: {e}")

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        simple_fields = {"Артикул": "product_sku", "Наименование": "product_name", "Цена": "price",
                         "Скидка (%)": "current_discount", "Кол-во на складе": "stock_quantity"}
        for label, key in simple_fields.items():
            self.widgets[key] = self._create_entry_row(main_frame, label)

        self.widgets["category_name"] = self._create_combo_row(main_frame, "Категория", [c['category_name'] for c in self.categories])
        self.widgets["manufacturer_name"] = self._create_combo_row(main_frame, "Производитель", [m['manufacturer_name'] for m in self.manufacturers])
        self.widgets["supplier_name"] = self._create_combo_row(main_frame, "Поставщик", [s['supplier_name'] for s in self.suppliers])

        desc_frame = ttk.Frame(main_frame); desc_frame.pack(fill='both', pady=5, expand=True)
        ttk.Label(desc_frame, text="Описание", width=20).pack(side='left', anchor='n', pady=3)
        self.widgets["description"] = tk.Text(desc_frame, height=4, font=config.FONT_PRIMARY, borderwidth=1, relief="solid")
        self.widgets["description"].pack(side='left', expand=True, fill='both')
        
        img_frame = ttk.Frame(main_frame); img_frame.pack(fill='x', pady=5)
        ttk.Button(img_frame, text="Выбрать изображение...", command=self._choose_image).pack(side='left')
        self.image_label = ttk.Label(img_frame, text="Файл не выбран", anchor="w")
        self.image_label.pack(side='left', expand=True, fill='x', padx=10)

        btn_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0)); btn_frame.pack(fill='x', side='bottom')
        ttk.Button(btn_frame, text="Сохранить", command=self.save, style="Accent.TButton").pack(side='left', expand=True, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.on_close).pack(side='left', expand=True, padx=5)
        if self.is_edit_mode:
            ttk.Button(btn_frame, text="Удалить", command=self.delete).pack(side='right', expand=True, padx=5)

    def _create_entry_row(self, parent, label_text):
        row_frame = ttk.Frame(parent); row_frame.pack(fill='x', pady=2)
        ttk.Label(row_frame, text=label_text, width=20).pack(side='left')
        entry = ttk.Entry(row_frame)
        entry.pack(side='left', expand=True, fill='x')
        return entry

    def _create_combo_row(self, parent, label_text, values):
        row_frame = ttk.Frame(parent); row_frame.pack(fill='x', pady=2)
        ttk.Label(row_frame, text=label_text, width=20).pack(side='left')
        combo = ttk.Combobox(row_frame, values=values, state="readonly")
        combo.pack(side='left', expand=True, fill='x')
        return combo

    def _populate_data(self):
        data = dict(self.product_data)
        for key, widget in self.widgets.items():
            value = data.get(key)
            if value is None: continue
            if isinstance(widget, tk.Text):
                widget.insert("1.0", value)
            elif isinstance(widget, ttk.Combobox):
                widget.set(str(value))
            else:
                widget.insert(0, str(value))
        self.widgets["product_sku"].config(state="readonly")
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
        except Exception:
            messagebox.showerror("Ошибка копирования", "Не удалось скопировать файл изображения. Убедитесь, что файл доступен и не поврежден.")

    def save(self):
        new_data = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, tk.Text):
                new_data[key] = widget.get("1.0", tk.END).strip()
            else:
                new_data[key] = widget.get()

        if not new_data.get("product_sku") or not new_data.get("product_name"):
            messagebox.showerror("Ошибка валидации", "Артикул и наименование являются обязательными для заполнения.")
            return

        # Преобразование имен в ID перед сохранением
        new_data['category_id'] = next((c['category_id'] for c in self.categories if c['category_name'] == new_data['category_name']), None)
        new_data['manufacturer_id'] = next((m['manufacturer_id'] for m in self.manufacturers if m['manufacturer_name'] == new_data['manufacturer_name']), None)
        new_data['supplier_id'] = next((s['supplier_id'] for s in self.suppliers if s['supplier_name'] == new_data['supplier_name']), None)
        new_data['image_path'] = self.selected_image_path

        try:
            if self.is_edit_mode:
                database.update_product(new_data)
            else:
                database.add_product(new_data)
            self.on_close()
        except Exception:
            messagebox.showerror("Ошибка сохранения", "Не удалось сохранить данные. Проверьте, что все поля, особенно числовые (цена, скидка, кол-во), заполнены корректно.")

    def delete(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар? Это действие нельзя будет отменить."):
            try:
                database.delete_product(self.product_data["product_sku"])
                self.on_close()
            except Exception:
                messagebox.showerror("Ошибка удаления", "Не удалось удалить товар. Возможно, он связан с существующими заказами и не может быть удален.")

    def on_close(self):
        self.callback()
        self.destroy()