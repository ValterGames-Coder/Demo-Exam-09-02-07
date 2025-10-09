DELETE FROM "order_items";
DELETE FROM "orders";
DELETE FROM "products";
DELETE FROM "users";
DELETE FROM "pickup_points";
DELETE FROM "categories";
DELETE FROM "manufacturers";
DELETE FROM "suppliers";

-- 2. Сброс всех счетчиков
ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
ALTER SEQUENCE pickup_points_point_id_seq RESTART WITH 1;
ALTER SEQUENCE orders_order_id_seq RESTART WITH 1;
ALTER SEQUENCE order_items_order_item_id_seq RESTART WITH 1;
ALTER SEQUENCE categories_category_id_seq RESTART WITH 1;
ALTER SEQUENCE manufacturers_manufacturer_id_seq RESTART WITH 1;
ALTER SEQUENCE suppliers_supplier_id_seq RESTART WITH 1;

-- =================================================================
-- 3. ЗАПОЛНЕНИЕ ТАБЛИЦ-СПРАВОЧНИКОВ
-- =================================================================

INSERT INTO "categories" ("category_name") VALUES ('Женская обувь'), ('Мужская обувь');

INSERT INTO "manufacturers" ("manufacturer_name") VALUES
('Kari'), ('Marco Tozzi'), ('Poc'), ('Rieker'), ('Alessio Nesca'),
('CROSBY'), ('Caprice'), ('ROMER'), ('ARGO'), ('FRAU'),
('Luiza Belly'), ('Профиль С.Дали'), ('TOFA');

INSERT INTO "suppliers" ("supplier_name") VALUES ('Kari'), ('Обувь для вас');

-- =================================================================
-- 4. ЗАПОЛНЕНИЕ ОСНОВНЫХ ТАБЛИЦ
-- =================================================================

-- Пользователи
INSERT INTO "users" ("full_name", "login", "password", "role_name") VALUES
('Никифорова Весения Николаевна', '94d5ous@gmail.com', 'uzWC67', 'Администратор'),
('Сазонов Руслан Германович', 'uth4iz@mail.com', '2L6KZG', 'Администратор'),
('Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JIFRCZ', 'Администратор'),
('Степанов Михаил Артёмович', '1diph5e@tutanota.com', '8ntwUp', 'Менеджер'),
('Ворсин Петр Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR', 'Менеджер'),
('Старикова Елена Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv', 'Менеджер'),
('Михайлюк Анна Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9', 'Авторизированный клиент'),
('Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos', 'Авторизированный клиент'),
('Ворсин Петр Евгеньевич', '1qz4kw@mail.com', 'gynQMT', 'Авторизированный клиент'),
('Старикова Елена Павловна', '4np6se@mail.com', 'AtnDjr', 'Авторизированный клиент');

-- Пункты выдачи
INSERT INTO "pickup_points" ("address") VALUES
('420151, г. Лесной, ул. Вишневая, 32'), ('125061, г. Лесной, ул. Подгорная, 8'),
('630370, г. Лесной, ул. Шоссейная, 24'), ('400562, г. Лесной, ул. Зеленая, 32'),
('614510, г. Лесной, ул. Маяковского, 47'), ('410542, г. Лесной, ул. Светлая, 46'),
('620839, г. Лесной, ул. Цветочная, 8'), ('443890, г. Лесной, ул. Коммунистическая, 1'),
('603379, г. Лесной, ул. Спортивная, 46'), ('603721, г. Лесной, ул. Гоголя, 41'),
('410172, г. Лесной, ул. Северная, 13'), ('614611, г. Лесной, ул. Молодежная, 50'),
('454311, г. Лесной, ул. Новая, 19'), ('660007, г. Лесной, ул. Октябрьская, 19'),
('603036, г. Лесной, ул. Садовая, 4'), ('394060, г. Лесной, ул. Фрунзе, 43'),
('410661, г. Лесной, ул. Школьная, 50'), ('625590, г. Лесной, ул. Коммунистическая, 20'),
('625683, г. Лесной, ул. 8 Марта, 26'), ('450983, г. Лесной, ул. Комсомольская, 26'),
('394782, г. Лесной, ул. Чехова, 3'), ('603002, г. Лесной, ул. Дзержинского, 28'),
('450558, г. Лесной, ул. Набережная, 30'), ('344288, г. Лесной, ул. Чехова, 1'),
('614164, г. Лесной, ул. Степная, 30'), ('394242, г. Лесной, ул. Коммунистическая, 43'),
('660540, г. Лесной, ул. Солнечная, 25'), ('125837, г. Лесной, ул. Шоссейная, 40'),
('125703, г. Лесной, ул. Партизанская, 49'), ('625283, г. Лесной, ул. Победы, 46'),
('614753, г. Лесной, ул. Полевая, 35'), ('426030, г. Лесной, ул. Маяковского, 44'),
('450375, г. Лесной, ул. Клубная, 44'), ('625560, г. Лесной, ул. Некрасова, 12'),
('630201, г. Лесной, ул. Комсомольская, 17'), ('190949, г. Лесной, ул. Мичурина, 26');

-- Продукты
INSERT INTO "products" (
    "product_sku", "product_name", "price", "current_discount", "stock_quantity", "description", "image_path",
    "category_id", "manufacturer_id", "supplier_id"
) VALUES
('A112T4', 'Ботинки', 4990, 3, 6, 'Женские ботинки демисезонные kari', 'resources/product_images/1.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('F635R4', 'Ботинки', 3244, 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', 'resources/product_images/2.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Marco Tozzi'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('H782T5', 'Туфли', 4499, 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', 'resources/product_images/3.jpg', (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('G783F5', 'Ботинки', 5900, 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', 'resources/product_images/4.jpg', (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Poc'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('J384T6', 'Ботинки', 3800, 2, 16, 'B3430/14 Полуботинки мужские Rieker', 'resources/product_images/5.jpg', (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('D572U8', 'Кроссовки', 4100, 3, 6, '129615-4 Кроссовки мужские', 'resources/product_images/6.jpg', (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Poc'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('F572H7', 'Туфли', 2700, 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', 'resources/product_images/7.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Marco Tozzi'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('D329H3', 'Полуботинки', 1890, 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', 'resources/product_images/8.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Alessio Nesca'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('B320R5', 'Туфли', 4300, 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', 'resources/product_images/9.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('G432E4', 'Туфли', 2800, 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', 'resources/product_images/10.jpg', (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('S213E3', 'Полуботинки', 2156, 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('E482R4', 'Полуботинки', 1800, 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('S634B5', 'Кеды', 5500, 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('K345R4', 'Полуботинки', 2100, 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('0754F4', 'Туфли', 5400, 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('G531F4', 'Ботинки', 6600, 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('J542F5', 'Тапочки', 500, 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('B431R5', 'Ботинки', 2700, 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('P764G4', 'Туфли', 6800, 15, 15, 'Туфли женские, ARGO, размер 38', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('C436G5', 'Ботинки', 10200, 15, 9, 'Ботинки женские, ARGO, размер 40', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Alessio Nesca'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('F427R5', 'Ботинки', 11800, 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('N457T5', 'Полуботинки', 4600, 3, 13, 'Полуботинки женские черные зимние, мех', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('D364R4', 'Туфли', 12400, 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('S326R5', 'Тапочки', 9900, 17, 15, 'Мужские кожаные тапочки "Профиль С.Дали"', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('L754R4', 'Полуботинки', 1700, 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Kari'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('M542T5', 'Кроссовки', 2800, 18, 3, 'Кроссовки мужские TOFA', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('D268G5', 'Туфли', 4399, 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас')),
('T324F5', 'Сапоги', 4699, 2, 5, 'Сапоги замша Цвет: синий', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'CROSBY'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('K358H6', 'Тапочки', 599, 20, 2, 'Тапочки мужские син р.41', NULL, (SELECT category_id FROM categories WHERE category_name = 'Мужская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Kari')),
('H535R5', 'Ботинки', 2300, 2, 7, 'Женские ботинки демисезонные', NULL, (SELECT category_id FROM categories WHERE category_name = 'Женская обувь'), (SELECT manufacturer_id FROM manufacturers WHERE manufacturer_name = 'Rieker'), (SELECT supplier_id FROM suppliers WHERE supplier_name = 'Обувь для вас'));

-- ЗАКАЗ 1
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Доставлен', '2025-02-27', '2025-04-20', 1,
 (SELECT user_id FROM users WHERE full_name = 'Степанов Михаил Артёмович' AND role_name = 'Менеджер'), 101);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'A112T4', 2),
(CURRVAL('orders_order_id_seq'), 'F635R4', 2);

-- ЗАКАЗ 2
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Доставлен', '2022-09-28', '2025-04-21', 11,
 (SELECT user_id FROM users WHERE full_name = 'Никифорова Весения Николаевна'), 102);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'H782T5', 1),
(CURRVAL('orders_order_id_seq'), 'G783F5', 1);

-- ЗАКАЗ 3
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('В обработке', '2025-03-21', '2025-04-22', 2,
 (SELECT user_id FROM users WHERE full_name = 'Сазонов Руслан Германович'), 103);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'J384T6', 10),
(CURRVAL('orders_order_id_seq'), 'D572U8', 10);

-- ЗАКАЗ 4
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('В пути', '2025-02-20', '2025-04-23', 11,
 (SELECT user_id FROM users WHERE full_name = 'Одинцов Серафим Артёмович'), 104);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'F572H7', 5),
(CURRVAL('orders_order_id_seq'), 'D329H3', 4);

-- ЗАКАЗ 5
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Готов к выдаче', '2025-03-17', '2025-04-24', 2,
 (SELECT user_id FROM users WHERE full_name = 'Степанов Михаил Артёмович' AND role_name = 'Менеджер'), 105);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'A112T4', 2),
(CURRVAL('orders_order_id_seq'), 'F635R4', 2);

-- ЗАКАЗ 6
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Готов к выдаче', '2025-03-01', '2025-04-25', 15,
 (SELECT user_id FROM users WHERE full_name = 'Никифорова Весения Николаевна'), 106);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'H782T5', 1),
(CURRVAL('orders_order_id_seq'), 'G783F5', 1);

-- ЗАКАЗ 7
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('В обработке', '2025-02-28', '2025-04-26', 3,
 (SELECT user_id FROM users WHERE full_name = 'Сазонов Руслан Германович'), 107);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'J384T6', 10),
(CURRVAL('orders_order_id_seq'), 'D572U8', 10);

-- ЗАКАЗ 8
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('В пути', '2025-03-31', '2025-04-27', 19,
 (SELECT user_id FROM users WHERE full_name = 'Одинцов Серафим Артёмович'), 108);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'F572H7', 5),
(CURRVAL('orders_order_id_seq'), 'D329H3', 4);

-- ЗАКАЗ 9
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Доставлен', '2025-04-02', '2025-04-28', 5,
 (SELECT user_id FROM users WHERE full_name = 'Степанов Михаил Артёмович' AND role_name = 'Менеджер'), 109);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'B320R5', 5),
(CURRVAL('orders_order_id_seq'), 'G432E4', 1);

-- ЗАКАЗ 10
INSERT INTO "orders" ("status", "order_date", "delivery_date", "pickup_point_id", "client_user_id", "order_code") VALUES
('Готов к выдаче', '2025-04-03', '2025-04-29', 19,
 (SELECT user_id FROM users WHERE full_name = 'Степанов Михаил Артёмович' AND role_name = 'Менеджер'), 110);

INSERT INTO "order_items" ("order_id", "product_sku", "quantity") VALUES
(CURRVAL('orders_order_id_seq'), 'S213E3', 5),
(CURRVAL('orders_order_id_seq'), 'E482R4', 5);