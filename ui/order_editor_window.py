import tkinter as tk
from tkinter import ttk, messagebox
import database


class OrderEditorWindow(tk.Toplevel):
    def __init__(self, parent, callback, order_data=None):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.order_data = dict(order_data) if order_data else None
        self.is_edit_mode = self.order_data is not None

        self.title("Редактирование заказа" if self.is_edit_mode else "Добавление заказа")
        self.geometry("700x500")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.clients = database.fetch_all("SELECT user_id, full_name FROM users ORDER BY full_name")
        self.pickup_points = database.fetch_all("SELECT point_id, address FROM pickup_points ORDER BY address")
        self.products = database.fetch_all("SELECT product_sku, product_name FROM products ORDER BY product_name")

        self._create_widgets()
        if self.is_edit_mode:
            self._populate_data()

        self.after(10, self._make_modal)

    def _make_modal(self):
        self.grab_set()
        self.transient(self.parent)
        self.wait_window(self)

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill="both", expand=True)

        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side='left', fill='y', padx=(0, 15))

        ttk.Label(left_panel, text="Статус заказа:").pack(anchor='w')
        self.status_combo = ttk.Combobox(left_panel, values=["В обработке", "В пути", "Готов к выдаче", "Доставлен"], state="readonly")
        self.status_combo.pack(anchor='w', fill='x', pady=(0, 10))

        ttk.Label(left_panel, text="Дата заказа (ГГГГ-ММ-ДД):").pack(anchor='w')
        self.order_date_entry = ttk.Entry(left_panel)
        self.order_date_entry.pack(anchor='w', fill='x', pady=(0, 10))

        ttk.Label(left_panel, text="Дата доставки (ГГГГ-ММ-ДД):").pack(anchor='w')
        self.delivery_date_entry = ttk.Entry(left_panel)
        self.delivery_date_entry.pack(anchor='w', fill='x', pady=(0, 10))

        ttk.Label(left_panel, text="Клиент:").pack(anchor='w')
        self.client_combo = ttk.Combobox(left_panel, values=[c['full_name'] for c in self.clients], state="readonly")
        self.client_combo.pack(anchor='w', fill='x', pady=(0, 10))

        ttk.Label(left_panel, text="Пункт выдачи:").pack(anchor='w')
        self.point_combo = ttk.Combobox(left_panel, values=[p['address'] for p in self.pickup_points], state="readonly")
        self.point_combo.pack(anchor='w', fill='x', pady=(0, 10))

        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='left', expand=True, fill='both')
        ttk.Label(right_panel, text="Состав заказа:").pack(anchor='w')

        self.tree = ttk.Treeview(right_panel, columns=("sku", "name", "qty"), show="headings", height=5)
        self.tree.heading("sku", text="Артикул"); self.tree.heading("name", text="Наименование"); self.tree.heading("qty", text="Кол-во")
        self.tree.column("sku", width=80); self.tree.column("name", width=150); self.tree.column("qty", width=50, anchor='e')
        self.tree.pack(expand=True, fill='both')

        item_controls = ttk.Frame(right_panel)
        item_controls.pack(fill='x', pady=5)
        self.product_combo = ttk.Combobox(item_controls, values=[f"{p['product_sku']} | {p['product_name']}" for p in self.products], state="readonly")
        self.product_combo.pack(side='left', expand=True, fill='x')
        self.qty_spinbox = ttk.Spinbox(item_controls, from_=1, to=100, width=5); self.qty_spinbox.pack(side='left', padx=5)
        ttk.Button(item_controls, text="+", command=self.add_item, width=2).pack(side='left')
        ttk.Button(item_controls, text="-", command=self.remove_item, width=2).pack(side='left', padx=5)

        button_frame = ttk.Frame(self, padding=15)
        button_frame.pack(fill='x', side='bottom')
        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side='left', expand=True, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.on_close).pack(side='left', expand=True, padx=5)
        if self.is_edit_mode:
            ttk.Button(button_frame, text="Удалить", command=self.delete).pack(side='right', expand=True, padx=5)

    def add_item(self):
        selected = self.product_combo.get()
        if not selected: return
        sku, name = selected.split(' | ', 1)
        qty = self.qty_spinbox.get()
        self.tree.insert("", "end", values=(sku, name, qty))

    def remove_item(self):
        if self.tree.selection(): self.tree.delete(self.tree.selection())

    def _populate_data(self):
        self.status_combo.set(self.order_data.get("status", ""))
        self.order_date_entry.insert(0, str(self.order_data.get("order_date", "")))
        self.delivery_date_entry.insert(0, str(self.order_data.get("delivery_date", "")))
        self.point_combo.set(self.order_data.get("pickup_point_address", ""))
        self.client_combo.set(self.order_data.get("client_name", ""))
        items = database.fetch_all(
            "SELECT oi.quantity, p.product_sku, p.product_name FROM order_items oi "
            "JOIN products p ON oi.product_sku = p.product_sku WHERE oi.order_id = %s",
            (self.order_data['order_id'],)
        )
        for item in items:
            self.tree.insert("", "end", values=(item['product_sku'], item['product_name'], item['quantity']))

    def save(self):
        client_id = next((c['user_id'] for c in self.clients if c['full_name'] == self.client_combo.get()), None)
        point_id = next((p['point_id'] for p in self.pickup_points if p['address'] == self.point_combo.get()), None)
        
        if not all([self.status_combo.get(), self.order_date_entry.get(), self.delivery_date_entry.get(), client_id, point_id]):
            messagebox.showerror("Ошибка валидации", "Все поля должны быть заполнены.")
            return

        order_details = {
            "status": self.status_combo.get(), "order_date": self.order_date_entry.get(),
            "delivery_date": self.delivery_date_entry.get(), "client_user_id": client_id, "pickup_point_id": point_id
        }
        items = [{"sku": self.tree.item(r)['values'][0], "qty": int(self.tree.item(r)['values'][2])} for r in self.tree.get_children()]
        
        if not items:
            messagebox.showerror("Ошибка валидации", "В заказе должен быть хотя бы один товар.")
            return

        try:
            if self.is_edit_mode:
                order_details["order_id"] = self.order_data['order_id']
                database.update_order(order_details, items)
            else:
                database.add_order(order_details, items)
            self.on_close()
        except Exception:
            messagebox.showerror("Ошибка сохранения", "Не удалось сохранить заказ. Проверьте, что все поля заполнены корректно и что даты указаны в формате ГГГГ-ММ-ДД.")

    def delete(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот заказ? Отменить это действие будет невозможно."):
            try:
                database.delete_order(self.order_data['order_id'])
                self.on_close()
            except Exception:
                messagebox.showerror("Ошибка удаления", "Не удалось удалить заказ. Пожалуйста, попробуйте еще раз.")

    def on_close(self):
        self.callback()
        self.destroy()