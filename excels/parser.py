import psycopg2
import pandas as pd
import sys
import os

from config import DB_SETTINGS

def clear_tables(connection):
    cursor = connection.cursor()
    print("Clearing tables...")
    cursor.execute("DELETE FROM order_items;")
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM products;")
    cursor.execute("DELETE FROM pickup_points;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM categories;")
    cursor.execute("DELETE FROM manufacturers;")
    cursor.execute("DELETE FROM suppliers;")
    connection.commit()
    cursor.close()
    print("Tables cleared.")

def get_or_create_id(cursor, table_name, column_name, value, name_column='name'):
    """
    Функция для поиска ID записи в таблице или вставки новой записи и возврата её ID.
    """
    query_check = f"SELECT {column_name} FROM {table_name} WHERE {name_column} = %s"
    cursor.execute(query_check, (value,))
    result = cursor.fetchone()
    if result:
        return result[0] # Возвращаем найденный ID

    query_insert = f"INSERT INTO {table_name} ({name_column}) VALUES (%s) RETURNING {column_name}"
    cursor.execute(query_insert, (value,))
    new_id = cursor.fetchone()[0]
    return new_id

def import_categories(connection):
    query = '''
    INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT (category_name) DO NOTHING
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Tovar.xlsx', engine='openpyxl')
    unique_categories = data_frame['Категория товара'].dropna().unique()

    for category in unique_categories:
        print(f"Processing category: {category}")
        cursor.execute(query, (category,))

    connection.commit()
    cursor.close()

def import_manufacturers(connection):
    query = '''
    INSERT INTO manufacturers (manufacturer_name) VALUES (%s) ON CONFLICT (manufacturer_name) DO NOTHING
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Tovar.xlsx', engine='openpyxl')
    unique_manufacturers = data_frame['Производитель'].dropna().unique()

    for manufacturer in unique_manufacturers:
        print(f"Processing manufacturer: {manufacturer}")
        cursor.execute(query, (manufacturer,))

    connection.commit()
    cursor.close()

def import_suppliers(connection):
    query = '''
    INSERT INTO suppliers (supplier_name) VALUES (%s) ON CONFLICT (supplier_name) DO NOTHING
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Tovar.xlsx', engine='openpyxl')
    unique_suppliers = data_frame['Поставщик'].dropna().unique()

    for supplier in unique_suppliers:
        print(f"Processing supplier: {supplier}")
        cursor.execute(query, (supplier,))

    connection.commit()
    cursor.close()

def import_users(connection):
    query = '''
    INSERT INTO users (role_name, full_name, login, password) VALUES (%s, %s, %s, %s)
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/user_import.xlsx', engine='openpyxl')

    for excel_row in data_frame.itertuples(index=False):
        print(excel_row)
        role = excel_row[0]
        full_name = excel_row[1]
        login = excel_row[2]
        password = excel_row[3]

        values = (role, full_name, login, password)
        cursor.execute(query, values)

    connection.commit()
    cursor.close()

def import_pickup_points(connection):
    query = '''
    INSERT INTO pickup_points (address) VALUES (%s)
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Пункты выдачи_import.xlsx', engine='openpyxl')

    for excel_row in data_frame.itertuples(index=False): # index=False для корректного доступа к данным
        print(excel_row)
        address = str(excel_row[0]).strip()
        values = (address,)
        cursor.execute(query, values)

    connection.commit()
    cursor.close()

def import_products(connection):
    query = '''
    INSERT INTO products (
        product_sku, product_name, unit, price, current_discount, 
        stock_quantity, description, image_path, category_id, 
        manufacturer_id, supplier_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Tovar.xlsx', engine='openpyxl')

    for excel_row in data_frame.itertuples(index=False): 
        sku = excel_row[0]
        name = excel_row[1]
        unit = excel_row[2]
        price = float(excel_row[3]) if pd.notna(excel_row[3]) else 0.0
        supplier_name = excel_row[4]
        manufacturer_name = excel_row[5]
        category_name = excel_row[6]
        discount = int(excel_row[7]) if pd.notna(excel_row[7]) else 0
        stock = int(excel_row[8]) if pd.notna(excel_row[8]) else 0
        description = excel_row[9] if pd.notna(excel_row[9]) else None
        image_path = "./resources/product_images/" + excel_row[10] if pd.notna(excel_row[10]) else None

        # Получаем ID связанных записей
        category_id = get_or_create_id(cursor, "categories", "category_id", category_name, "category_name")
        manufacturer_id = get_or_create_id(cursor, "manufacturers", "manufacturer_id", manufacturer_name, "manufacturer_name")
        supplier_id = get_or_create_id(cursor, "suppliers", "supplier_id", supplier_name, "supplier_name")

        values = (
            sku, name, unit, price, discount, stock, description,
            image_path, category_id, manufacturer_id, supplier_id
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()

def import_orders_and_items(connection):
    query_order = '''
    INSERT INTO orders (order_id, status, order_date, delivery_date, pickup_point_id, client_user_id, order_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    query_item = '''
    INSERT INTO order_items (order_id, product_sku, quantity)
    VALUES (%s, %s, %s)
    '''
    cursor = connection.cursor()
    data_frame = pd.read_excel('./excels/Заказ_import.xlsx', engine='openpyxl')

    for excel_row in data_frame.itertuples(index=False):
        print(excel_row)
        order_id = int(excel_row[0])
        items_str = excel_row[1]
        order_date_str = excel_row[2]
        delivery_date_str = excel_row[3]
        pickup_point_index = int(excel_row[4]) 
        client_full_name = excel_row[5]
        order_code = int(excel_row[6])
        status = excel_row[7]

        # Парсим даты
        # pandas может читать дату как Timestamp, строку или float
        if pd.isna(order_date_str):
             raise ValueError(f"Order date is missing for order {order_id}")
        if isinstance(order_date_str, pd.Timestamp):
            order_date = order_date_str.strftime('%Y-%m-%d')
        else:
            corrected_date_str = str(order_date_str).replace("30.02.2025", "28.02.2025")
            try:
                order_date = pd.Timestamp(corrected_date_str).strftime('%Y-%m-%d')
            except ValueError:
                import datetime
                try:
                    parsed_date = datetime.datetime.strptime(corrected_date_str, '%d.%m.%Y')
                    order_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Cannot parse order date '{corrected_date_str}' for order {order_id}")

        if pd.isna(delivery_date_str):
             raise ValueError(f"Delivery date is missing for order {order_id}")
        if isinstance(delivery_date_str, pd.Timestamp):
            delivery_date = delivery_date_str.strftime('%Y-%m-%d')
        else:
            try:
                delivery_date = pd.Timestamp(str(delivery_date_str)).strftime('%Y-%m-%d')
            except ValueError:
                import datetime
                try:
                    parsed_date = datetime.datetime.strptime(str(delivery_date_str), '%d.%m.%Y')
                    delivery_date = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Cannot parse delivery date '{delivery_date_str}' for order {order_id}")

        cursor.execute("SELECT point_id FROM pickup_points ORDER BY point_id ASC")
        pickup_points_ids = [row[0] for row in cursor.fetchall()]
        if 1 <= pickup_point_index <= len(pickup_points_ids):
            pickup_point_id = pickup_points_ids[pickup_point_index - 1]
        else:
            raise ValueError(f"Pickup point index {pickup_point_index} is out of range (1 to {len(pickup_points_ids)})")

        cursor.execute("SELECT user_id FROM users WHERE full_name = %s", (client_full_name,))
        user_result = cursor.fetchone()
        if user_result:
            client_user_id = user_result[0]
        else:
            raise ValueError(f"Client user '{client_full_name}' not found in users table")

        # Вставляем заказ
        order_values = (order_id, status, order_date, delivery_date, pickup_point_id, client_user_id, order_code)
        cursor.execute(query_order, order_values)

        items_parts = [part.strip() for part in str(items_str).split(',')]
        if len(items_parts) % 2 != 0:
            raise ValueError(f"Items string format is incorrect for order {order_id}: {items_str}")

        for i in range(0, len(items_parts), 2):
            sku = items_parts[i]
            quantity = int(items_parts[i+1])

            cursor.execute("SELECT product_sku FROM products WHERE product_sku = %s", (sku,))
            if not cursor.fetchone():
                 raise ValueError(f"Product SKU '{sku}' from order {order_id} not found in products table")

            item_values = (order_id, sku, quantity)
            cursor.execute(query_item, item_values)

    connection.commit()
    cursor.close()


def start_import():
    connection_uri = psycopg2.connect(**DB_SETTINGS)

    clear_tables(connection_uri)

    import_categories(connection_uri)
    import_manufacturers(connection_uri)
    import_suppliers(connection_uri)
    import_users(connection_uri)
    import_pickup_points(connection_uri) 
    import_products(connection_uri)
    import_orders_and_items(connection_uri)

    connection_uri.close()