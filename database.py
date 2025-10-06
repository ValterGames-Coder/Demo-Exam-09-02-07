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
    if not conn:
        raise ConnectionError("Не удалось подключиться к базе данных.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    finally:
        if conn:
            conn.close()


def fetch_all(query, params=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        if conn:
            conn.close()


def check_user(login, password):
    query = "SELECT * FROM users WHERE login = %s AND password = %s"
    results = fetch_all(query, (login, password))
    return results[0] if results else None


def get_products(filters=None):
    base_query = """
        SELECT
            product_sku, product_name, price, current_discount,
            stock_quantity, image_path, category_name,
            manufacturer_name, supplier_name, description, unit
        FROM products
    """
    where_clauses = []
    params = []

    if filters:
        search_query = filters.get("search_query")
        if search_query:
            search_term = f"%{search_query}%"
            where_clauses.append(
                "(product_name ILIKE %s OR product_sku ILIKE %s OR description ILIKE %s)"
            )
            params.extend([search_term, search_term, search_term])
        
        supplier = filters.get("supplier")
        if supplier and supplier != "Все поставщики":
            where_clauses.append("supplier_name = %s")
            params.append(supplier)

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    sort_by_stock = filters.get("sort_by") if filters else None
    if sort_by_stock == "stock_quantity":
        order = "ASC" if filters.get("sort_order") == "asc" else "DESC"
        base_query += f" ORDER BY stock_quantity {order}"
    else:
        base_query += " ORDER BY CASE WHEN current_discount > 0 THEN 0 ELSE 1 END, product_name"

    return fetch_all(base_query, tuple(params))


def get_orders():
    query = """
        SELECT o.*, pp.address AS pickup_point_address, u.full_name AS client_name
        FROM orders o
        LEFT JOIN pickup_points pp ON o.pickup_point_id = pp.point_id
        LEFT JOIN users u ON o.client_user_id = u.user_id
        ORDER BY o.order_date DESC;
    """
    return fetch_all(query)


def get_suppliers():
    return fetch_all("SELECT DISTINCT supplier_name FROM products WHERE supplier_name IS NOT NULL ORDER BY supplier_name")


def add_product(data):
    query = """
        INSERT INTO products (product_sku, product_name, price, current_discount, stock_quantity,
        category_name, manufacturer_name, supplier_name, description, image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data['product_sku'], data['product_name'], float(data.get('price', 0)),
        int(data.get('current_discount', 0)), int(data.get('stock_quantity', 0)),
        data.get('category_name'), data.get('manufacturer_name'), data.get('supplier_name'),
        data.get('description'), data.get('image_path')
    )
    _execute_modification(query, params)


def update_product(data):
    query = """
        UPDATE products SET product_name = %s, price = %s, current_discount = %s,
        stock_quantity = %s, category_name = %s, manufacturer_name = %s,
        supplier_name = %s, description = %s, image_path = %s
        WHERE product_sku = %s
    """
    params = (
        data['product_name'], float(data.get('price', 0)), int(data.get('current_discount', 0)),
        int(data.get('stock_quantity', 0)), data.get('category_name'),
        data.get('manufacturer_name'), data.get('supplier_name'),
        data.get('description'), data.get('image_path'), data['product_sku']
    )
    _execute_modification(query, params)


def delete_product(sku):
    _execute_modification("DELETE FROM products WHERE product_sku = %s", (sku,))


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