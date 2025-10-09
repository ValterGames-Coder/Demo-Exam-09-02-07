import os
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageOps

import config
import database
from ui.product_editor_window import ProductEditorWindow
from ui.order_editor_window import OrderEditorWindow


class MainAppWindow(tk.Tk):
    """Класс главного окна приложения."""

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.current_view = 'products'
        self.image_references = []
        self.logged_out = False
        self.title(config.MAIN_WINDOW_TITLE_FORMAT.format(
            app_name=config.APP_NAME,
            role_name=user_data['role_name']
        ))
        
        if os.path.exists(config.ICON_PATH):
            try:
                self.iconbitmap(config.ICON_PATH)
            except tk.TclError:
                print(f"Не удалось загрузить иконку: {config.ICON_PATH}")

        self.geometry("1024x768")
        self.resizable(False, False)
        self.configure(bg=config.COLOR_MAIN_BG)

        self._setup_styles()
        self._create_layout()
        self.load_view()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.configure("TLabel", font=config.FONT_PRIMARY, background=config.COLOR_MAIN_BG)
        style.configure("TButton", font=config.FONT_PRIMARY)
        style.configure("TFrame", background=config.COLOR_MAIN_BG)
        style.configure("Card.TFrame", background=config.COLOR_MAIN_BG, borderwidth=1, relief="solid")
        style.configure("Discount.Card.TFrame", background=config.COLOR_DISCOUNT_BG)
        style.configure("OutOfStock.Card.TFrame", background="lightblue")
        style.configure("Accent.TButton", background=config.COLOR_ACCENT, foreground="black")
        style.configure("Discount.TLabel", background=config.COLOR_DISCOUNT_BG, foreground="white", font=config.FONT_CARD_BODY)
        style.configure("Discount.Title.TLabel", background=config.COLOR_DISCOUNT_BG, foreground="white", font=config.FONT_CARD_TITLE)
        style.configure("Discount.Accent.TLabel", background=config.COLOR_DISCOUNT_BG, foreground="white", font=config.FONT_CARD_ACCENT)
        style.configure("Discount.TFrame", background=config.COLOR_DISCOUNT_BG)
        style.configure("OutOfStock.TLabel", background="lightblue", font=config.FONT_CARD_BODY)
        style.configure("OutOfStock.Title.TLabel", background="lightblue", font=config.FONT_CARD_TITLE)
        style.configure("OutOfStock.Accent.TLabel", background="lightblue", font=config.FONT_CARD_ACCENT)
        style.configure("OutOfStock.TFrame", background="lightblue")

    def _create_layout(self):
        # --- Верхняя панель (лого, имя) ---
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill='x', side='top', pady=(0, 5))
        
        if os.path.exists(config.LOGO_PATH):
            try:
                with Image.open(config.LOGO_PATH) as img:
                    img.thumbnail((32, 32), Image.Resampling.LANCZOS)
                    logo_img = ImageTk.PhotoImage(img)
                    self.image_references.append(logo_img)
                    logo_label = ttk.Label(top_frame, image=logo_img)
                    logo_label.image = logo_img  # Дополнительно, на всякий случай
                    logo_label.pack(side='left', padx=(0, 10))
                    
            except Exception as e:
                print(f"Не удалось загрузить логотип: {e}")

        ttk.Label(top_frame, text=config.APP_NAME, font=config.FONT_TITLE).pack(side='left')
        
        ttk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=10)
        ttk.Label(top_frame, text=f"Пользователь: {self.user_data['full_name']}").pack(side='right', padx=10)

        # --- Панель управления (кнопки, поиск) ---
        self.controls_frame = ttk.Frame(self, padding=(10, 0))
        self.controls_frame.pack(fill='x')

        # --- Прокручиваемая область ---
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(container, bg=config.COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window_id, width=e.width))
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def logout(self):
        self.logged_out = True
        self.destroy()

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta') and event.delta:
            delta = -1 * (event.delta // 120)
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            return
        self.canvas.yview_scroll(delta, "units")

    def switch_view(self, view_name):
        if self.current_view == view_name: return
        self.current_view = view_name
        self.load_view()

    def load_view(self):
        self._populate_controls()
        self.populate_content()
        self.update_idletasks()
        self.canvas.yview_moveto(0)

    def _populate_controls(self):
        for widget in self.controls_frame.winfo_children(): widget.destroy()
        parent = self.controls_frame
        is_privileged = self.user_data['role_name'] in ['Менеджер', 'Администратор']
        is_admin = self.user_data['role_name'] == 'Администратор'
        
        left_frame = ttk.Frame(parent); left_frame.pack(side='left', padx=5)
        right_frame = ttk.Frame(parent); right_frame.pack(side='right', padx=5)

        ttk.Button(left_frame, text="Товары", command=lambda: self.switch_view('products')).pack(side='left', padx=2)
        if is_privileged:
            ttk.Button(left_frame, text="Заказы", command=lambda: self.switch_view('orders')).pack(side='left', padx=2)
        
        if self.current_view == 'products':
            if is_privileged:
                ttk.Label(left_frame, text="Поиск:").pack(side='left', padx=(15, 2))
                self.search_var = tk.StringVar()
                self.search_var.trace_add("write", self.populate_content)
                ttk.Entry(left_frame, textvariable=self.search_var, width=20).pack(side='left', padx=2)
                
                ttk.Label(left_frame, text="Поставщик:").pack(side='left', padx=(10, 2))
                suppliers = ["Все поставщики"] + [s['supplier_name'] for s in database.get_suppliers()]
                self.supplier_var = tk.StringVar(value=suppliers[0])
                supplier_combo = ttk.Combobox(left_frame, textvariable=self.supplier_var, values=suppliers, state="readonly", width=15)
                supplier_combo.pack(side='left', padx=2)
                supplier_combo.bind("<<ComboboxSelected>>", self.populate_content)

                ttk.Label(left_frame, text="Сорт-ка (кол-во):").pack(side='left', padx=(10, 2))
                self.sort_order = tk.StringVar(value="asc")
                sort_frame_inner = ttk.Frame(left_frame); sort_frame_inner.pack(side='left')
                asc = ttk.Radiobutton(sort_frame_inner, text="↑", variable=self.sort_order, value="asc", command=self.populate_content)
                desc = ttk.Radiobutton(sort_frame_inner, text="↓", variable=self.sort_order, value="desc", command=self.populate_content)
                asc.pack(side='left'); desc.pack(side='left')
            if is_admin:
                ttk.Button(right_frame, text="Добавить товар", command=self.open_product_editor, style="Accent.TButton").pack()
        elif self.current_view == 'orders' and is_admin:
            ttk.Button(right_frame, text="Добавить заказ", command=self.open_order_editor, style="Accent.TButton").pack()

    def populate_content(self, *args):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.image_references.clear()

        if self.current_view == 'products':
            filters = {}
            if hasattr(self, 'search_var'): filters['search_query'] = self.search_var.get()
            if hasattr(self, 'supplier_var'): filters['supplier'] = self.supplier_var.get()
            if hasattr(self, 'sort_order'):
                filters['sort_by'] = 'stock_quantity'
                filters['sort_order'] = self.sort_order.get()
            for product in database.get_products(filters): self._create_product_card(self.scrollable_frame, product)
        elif self.current_view == 'orders':
            for order in database.get_orders(): self._create_order_card(self.scrollable_frame, order)

    def open_product_editor(self, product_data=None):
        if self.user_data['role_name'] != 'Администратор': return
        ProductEditorWindow(self, self.load_view, product_data)

    def open_order_editor(self, order_data=None):
        if self.user_data['role_name'] != 'Администратор': return
        OrderEditorWindow(self, self.load_view, order_data)

    def _resize_image(self, path, size):
        if not os.path.exists(path):
            return None
        try:
            with Image.open(path) as img:
                img = img.convert("RGBA")
                img = ImageOps.contain(img, size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Ошибка при обработке изображения {path}: {e}")
            return None

    def _bind_recursive(self, widget, command):
        widget.bind("<Button-1>", command)
        for child in widget.winfo_children():
            self._bind_recursive(child, command)

    def _create_product_card(self, parent, product):
        is_admin = self.user_data['role_name'] == 'Администратор'
        has_discount = product.get('current_discount', 0) > 0
        is_out_of_stock = product.get('stock_quantity', 0) == 0
        
        card_style = "Card.TFrame"
        if is_out_of_stock: card_style = "OutOfStock.Card.TFrame"
        elif has_discount and product.get('current_discount') > 15: card_style = "Discount.Card.TFrame"
        child_style_prefix = ""
        if is_out_of_stock: child_style_prefix = "OutOfStock."
        elif has_discount and product.get('current_discount') > 15: child_style_prefix = "Discount."
        command = (lambda e, p=product: self.open_product_editor(p)) if is_admin else None

        card = ttk.Frame(parent, style=card_style); card.pack(pady=5, fill='x', expand=True)

        img_container = tk.Frame(
            card,
            width=300,
            height=200,
            bg=config.COLOR_MAIN_BG,
            highlightbackground="black",
            highlightthickness=1
        )
        img_container.pack_propagate(False)
        img_container.pack(side='left', padx=10, pady=10)

        img_label = tk.Label(img_container, bg=config.COLOR_MAIN_BG)
        img_label.pack(expand=True)

        img = self._resize_image(product.get('image_path') or config.PLACEHOLDER_IMAGE_PATH, (300, 200))
        if img:
            img_label.configure(image=img)
            self.image_references.append(img)

        center = ttk.Frame(card, style=f"{child_style_prefix}TFrame"); center.pack(side='left', expand=True, fill='both', pady=10)
        title = f"{product.get('category_name', 'N/A')} | {product.get('product_name', 'N/A')}"
        ttk.Label(center, text=title, font=config.FONT_CARD_TITLE, style=f"{child_style_prefix}Title.TLabel", wraplength=500).pack(anchor='w', pady=(0, 5))
        
        price_frame = ttk.Frame(center, style=f"{child_style_prefix}TFrame"); price_frame.pack(anchor='w')
        price_val = float(product.get('price', 0)); discount_val = product.get('current_discount', 0)
        if has_discount:
            overstrike_font = font.Font(family="Times New Roman", size=11, overstrike=True)
            ttk.Label(price_frame, text=f"{price_val:.2f} руб.", font=overstrike_font, foreground="red", style=f"{child_style_prefix}TLabel").pack(side='left')
            new_price = price_val * (1 - discount_val / 100)
            ttk.Label(price_frame, text=f" {new_price:.2f} руб.", font=config.FONT_CARD_BODY, style=f"{child_style_prefix}TLabel").pack(side='left')
        else:
            ttk.Label(price_frame, text=f"Цена: {price_val:.2f} руб.", font=config.FONT_CARD_BODY, style=f"{child_style_prefix}TLabel").pack(side='left')

        details = (
            f"Описание: {product.get('description', '-') or '-'}\n"
            f"Производитель: {product.get('manufacturer_name', '-')}\n"
            f"Поставщик: {product.get('supplier_name', '-')}\n"
            f"Кол-во: {product.get('stock_quantity', 0)} {product.get('unit', 'шт.')}"
        )
        ttk.Label(center, text=details, font=config.FONT_CARD_BODY, justify='left', style=f"{child_style_prefix}TLabel").pack(anchor='w', pady=(5,0))
        
        right = ttk.Frame(card, width=130, style=f"{child_style_prefix}TFrame"); right.pack(side='right', fill='y', padx=10, pady=10)
        right.pack_propagate(False)
        ttk.Label(right, text="Действующая\nскидка", justify='center', font=config.FONT_CARD_BODY, style=f"{child_style_prefix}TLabel", anchor="center").pack(expand=True)
        ttk.Label(right, text=f"{discount_val}%", font=config.FONT_CARD_ACCENT, style=f"{child_style_prefix}Accent.TLabel", anchor="center").pack(expand=True)
        
        if command: self._bind_recursive(card, command)

    def _create_order_card(self, parent, order):
        is_admin = self.user_data['role_name'] == 'Администратор'
        command = (lambda e, o=order: self.open_order_editor(o)) if is_admin else None
        
        card = ttk.Frame(parent, style="Card.TFrame"); card.pack(pady=5, fill='x', expand=True)
        left = ttk.Frame(card); left.pack(side='left', expand=True, fill='both', padx=10, pady=10)
        details = (
            f"Артикул заказа: {order.get('order_id', 'N/A')}",
            f"Статус: {order.get('status', 'N/A')}",
            f"Пункт выдачи: {order.get('pickup_point_address', 'N/A')}",
            f"Дата заказа: {order.get('order_date', 'N/A')}"
        )
        for detail in details:
            ttk.Label(left, text=detail, font=config.FONT_CARD_BODY).pack(anchor='w')
        right = ttk.Frame(card, width=150); right.pack(side='right', fill='y', padx=10, pady=10)
        right.pack_propagate(False)
        ttk.Label(right, text="Дата доставки", font=config.FONT_CARD_BODY, anchor="center", justify='center').pack(expand=True)
        ttk.Label(right, text=str(order.get('delivery_date', 'N/A')), font=config.FONT_CARD_ACCENT, anchor="center").pack(expand=True)
        if command: self._bind_recursive(card, command)