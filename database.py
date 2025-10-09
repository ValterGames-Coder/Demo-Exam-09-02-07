import psycopg2
from psycopg2.extras import DictCursor
import config


def get_connection():
    try:
        return psycopg2.connect(**config.DB_SETTINGS)
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


def _execute_modification(query, params=None):
    conn = get_connection()
    if not conn: raise ConnectionError("Не удалось подключиться к базе данных.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    finally:
        if conn: conn.close()


def fetch_all(query, params=None):
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        if conn: conn.close()


def check_user(login, password):
    query = "SELECT * FROM users WHERE login = %s AND password = %s"
    results = fetch_all(query, (login, password))
    return results[0] if results else None


def get_products(filters=None):
    # ИСПРАВЛЕНО: Запрос переписан с использованием JOIN
    base_query = """
        SELECT
            p.product_sku, p.product_name, p.price, p.current_discount,
            p.stock_quantity, p.image_path, p.description, p.unit,
            c.category_name, m.manufacturer_name, s.supplier_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
    """
    where_clauses, params = [], []
    order_clause = "ORDER BY CASE WHEN p.current_discount > 0 THEN 0 ELSE 1 END, p.product_name"
    if filters:
        search_query = filters.get("search_query")
        if search_query:
            where_clauses.append("(p.product_name ILIKE %s OR p.product_sku ILIKE %s OR p.description ILIKE %s)")
            params.extend([f"%{search_query}%"] * 3)
        if filters.get("sort_by") == "stock_quantity":
            order = "ASC" if filters.get("sort_order") == "asc" else "DESC"
            order_clause = f"ORDER BY p.stock_quantity {order}, p.product_name"
    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)
    base_query += f" {order_clause}"
    return fetch_all(base_query, tuple(params))


def get_full_product_info(sku):
    query = """
        SELECT p.*, c.category_name, m.manufacturer_name, s.supplier_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.product_sku = %s
    """
    results = fetch_all(query, (sku,))
    return results[0] if results else None


def get_suppliers(): return fetch_all("SELECT * FROM suppliers ORDER BY supplier_name")
def get_categories(): return fetch_all("SELECT * FROM categories ORDER BY category_name")
def get_manufacturers(): return fetch_all("SELECT * FROM manufacturers ORDER BY manufacturer_name")


def add_product(data):
    query = """
        INSERT INTO products (product_sku, product_name, price, current_discount, stock_quantity,
        description, image_path, category_id, manufacturer_id, supplier_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data['product_sku'], data['product_name'], float(data.get('price', 0)),
        int(data.get('current_discount', 0)), int(data.get('stock_quantity', 0)),
        data.get('description'), data.get('image_path'),
        data.get('category_id'), data.get('manufacturer_id'), data.get('supplier_id')
    )
    _execute_modification(query, params)


def update_product(data):
    query = """
        UPDATE products SET product_name = %s, price = %s, current_discount = %s,
        stock_quantity = %s, description = %s, image_path = %s,
        category_id = %s, manufacturer_id = %s, supplier_id = %s
        WHERE product_sku = %s
    """
    params = (
        data['product_name'], float(data.get('price', 0)), int(data.get('current_discount', 0)),
        int(data.get('stock_quantity', 0)), data.get('description'), data.get('image_path'),
        data.get('category_id'), data.get('manufacturer_id'), data.get('supplier_id'),
        data['product_sku']
    )
    _execute_modification(query, params)


def delete_product(sku):
    _execute_modification("DELETE FROM products WHERE product_sku = %s", (sku,))

def get_orders():
    query = """
        SELECT o.*, pp.address AS pickup_point_address, u.full_name AS client_name
        FROM orders o
        LEFT JOIN pickup_points pp ON o.pickup_point_id = pp.point_id
        LEFT JOIN users u ON o.client_user_id = u.user_id
        ORDER BY o.order_date DESC;
    """
    return fetch_all(query)


def add_order(details, items):
    conn = get_connection()
    if not conn: raise ConnectionError("Нет подключения к БД.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO orders (status, order_date, delivery_date, client_user_id, pickup_point_id, order_code) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING order_id",
                (details['status'], details['order_date'], details['delivery_date'],
                 details['client_user_id'], details['pickup_point_id'], 1234)
            )
            order_id = cursor.fetchone()[0]
            for item in items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_sku, quantity) VALUES (%s, %s, %s)",
                    (order_id, item['sku'], item['qty'])
                )
            conn.commit()
    finally:
        if conn: conn.close()


def update_order(details, items):
    conn = get_connection()
    if not conn: raise ConnectionError("Нет подключения к БД.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE orders SET status = %s, order_date = %s, delivery_date = %s, "
                "client_user_id = %s, pickup_point_id = %s WHERE order_id = %s",
                (details['status'], details['order_date'], details['delivery_date'],
                 details['client_user_id'], details['pickup_point_id'], details['order_id'])
            )
            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (details['order_id'],))
            for item in items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_sku, quantity) VALUES (%s, %s, %s)",
                    (details['order_id'], item['sku'], item['qty'])
                )
            conn.commit()
    finally:
        if conn: conn.close()


def delete_order(order_id):
    _execute_modification("DELETE FROM orders WHERE order_id = %s", (order_id,))