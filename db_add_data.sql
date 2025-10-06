-- Очистка таблиц
DELETE FROM "order_items";
DELETE FROM "orders";
DELETE FROM "products";
DELETE FROM "users";
DELETE FROM "pickup_points";

-- Сброс автоинкрементных счетчиков 
ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
ALTER SEQUENCE pickup_points_point_id_seq RESTART WITH 1;
ALTER SEQUENCE orders_order_id_seq RESTART WITH 1;
ALTER SEQUENCE order_items_order_item_id_seq RESTART WITH 1;

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

-- Продукты
INSERT INTO "products" (
    "product_sku", "product_name", "unit", "price", "supplier_name", "manufacturer_name", "category_name",
    "current_discount", "stock_quantity", "description", "image_path"
) VALUES
('A112T4', 'Ботинки', 'шт.', 4990, 'Kari', 'Kari', 'Женская обувь', 3, 6, 'Женские ботинки демисезонные kari', 'resources/product_images/1.jpg'),
('F635R4', 'Ботинки', 'шт.', 3244, 'Обувь для вас', 'Marco Tozzi', 'Женская обувь', 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', 'resources/product_images/2.jpg'),
('H782T5', 'Туфли', 'шт.', 4499, 'Kari', 'Kari', 'Мужская обувь', 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', 'resources/product_images/3.jpg'),
('G783F5', 'Ботинки', 'шт.', 5900, 'Kari', 'Poc', 'Мужская обувь', 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', 'resources/product_images/4.jpg'),
('J384T6', 'Ботинки', 'шт.', 3800, 'Обувь для вас', 'Rieker', 'Мужская обувь', 2, 16, 'B3430/14 Полуботинки мужские Rieker', 'resources/product_images/5.jpg'),
('D572U8', 'Кроссовки', 'шт.', 4100, 'Обувь для вас', 'Poc', 'Мужская обувь', 3, 6, '129615-4 Кроссовки мужские', 'resources/product_images/6.jpg'),
('F572H7', 'Туфли', 'шт.', 2700, 'Kari', 'Marco Tozzi', 'Женская обувь', 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', 'resources/product_images/7.jpg'),
('D329H3', 'Полуботинки', 'шт.', 1890, 'Обувь для вас', 'Alessio Nesca', 'Женская обувь', 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', 'resources/product_images/8.jpg'),
('B320R5', 'Туфли', 'шт.', 4300, 'Kari', 'Rieker', 'Женская обувь', 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', 'resources/product_images/9.jpg'),
('G432E4', 'Туфли', 'шт.', 2800, 'Kari', 'Kari', 'Женская обувь', 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', 'resources/product_images/10.jpg'),
('S213E3', 'Полуботинки', 'шт.', 2156, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL),
('E482R4', 'Полуботинки', 'шт.', 1800, 'Kari', 'Kari', 'Женская обувь', 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL),
('S634B5', 'Кеды', 'шт.', 5500, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL),
('K345R4', 'Полуботинки', 'шт.', 2100, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL),
('0754F4', 'Туфли', 'шт.', 5400, 'Обувь для вас', 'Rieker', 'Женская обувь', 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL),
('G531F4', 'Ботинки', 'шт.', 6600, 'Kari', 'Kari', 'Женская обувь', 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL),
('J542F5', 'Тапочки', 'шт.', 500, 'Kari', 'Kari', 'Мужская обувь', 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL),
('B431R5', 'Ботинки', 'шт.', 2700, 'Обувь для вас', 'Rieker', 'Мужская обувь', 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL),
('P764G4', 'Туфли', 'шт.', 6800, 'Kari', 'CROSBY', 'Женская обувь', 15, 15, 'Туфли женские, ARGO, размер 38', NULL),
('C436G5', 'Ботинки', 'шт.', 10200, 'Kari', 'Alessio Nesca', 'Женская обувь', 15, 9, 'Ботинки женские, ARGO, размер 40', NULL),
('F427R5', 'Ботинки', 'шт.', 11800, 'Обувь для вас', 'Rieker', 'Женская обувь', 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL),
('N457T5', 'Полуботинки', 'шт.', 4600, 'Kari', 'CROSBY', 'Женская обувь', 3, 13, 'Полуботинки женские черные зимние, мех', NULL),
('D364R4', 'Туфли', 'шт.', 12400, 'Kari', 'Kari', 'Женская обувь', 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL),
('S326R5', 'Тапочки', 'шт.', 9900, 'Обувь для вас', 'CROSBY', 'Мужская обувь', 17, 15, 'Мужские кожаные тапочки "Профиль С.Дали"', NULL),
('L754R4', 'Полуботинки', 'шт.', 1700, 'Kari', 'Kari', 'Женская обувь', 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL),
('M542T5', 'Кроссовки', 'шт.', 2800, 'Обувь для вас', 'Rieker', 'Мужская обувь', 18, 3, 'Кроссовки мужские TOFA', NULL),
('D268G5', 'Туфли', 'шт.', 4399, 'Обувь для вас', 'Rieker', 'Женская обувь', 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL),
('T324F5', 'Сапоги', 'шт.', 4699, 'Kari', 'CROSBY', 'Женская обувь', 2, 5, 'Сапоги замша Цвет: синий', NULL),
('K358H6', 'Тапочки', 'шт.', 599, 'Kari', 'Rieker', 'Мужская обувь', 20, 2, 'Тапочки мужские син р.41', NULL),
('H535R5', 'Ботинки', 'шт.', 2300, 'Обувь для вас', 'Rieker', 'Женская обувь', 2, 7, 'Женские ботинки демисезонные', NULL);


-- Пункты выдачи
INSERT INTO "pickup_points" ("address") VALUES
('420151, г. Лесной, ул. Вишневая, 32'),
('125061, г. Лесной, ул. Подгорная, 8'),
('630370, г. Лесной, ул. Шоссейная, 24'),
('400562, г. Лесной, ул. Зеленая, 32'),
('614510, г. Лесной, ул. Маяковского, 47'),
('410542, г. Лесной, ул. Светлая, 46'),
('620839, г. Лесной, ул. Цветочная, 8'),
('443890, г. Лесной, ул. Коммунистическая, 1'),
('603379, г. Лесной, ул. Спортивная, 46'),
('603721, г. Лесной, ул. Гоголя, 41'),
('410172, г. Лесной, ул. Северная, 13'),
('614611, г. Лесной, ул. Молодежная, 50'),
('454311, г. Лесной, ул. Новая, 19'),
('660007, г. Лесной, ул. Октябрьская, 19'),
('603036, г. Лесной, ул. Садовая, 4'),
('394060, г. Лесной, ул. Фрунзе, 43'),
('410661, г. Лесной, ул. Школьная, 50'),
('625590, г. Лесной, ул. Коммунистическая, 20'),
('625683, г. Лесной, ул. 8 Марта, 26'),
('450983, г. Лесной, ул. Комсомольская, 26'),
('394782, г. Лесной, ул. Чехова, 3'),
('603002, г. Лесной, ул. Дзержинского, 28'),
('450558, г. Лесной, ул. Набережная, 30'),
('344288, г. Лесной, ул. Чехова, 1'),
('614164, г. Лесной, ул. Степная, 30'),
('394242, г. Лесной, ул. Коммунистическая, 43'),
('660540, г. Лесной, ул. Солнечная, 25'),
('125837, г. Лесной, ул. Шоссейная, 40'),
('125703, г. Лесной, ул. Партизанская, 49'),
('625283, г. Лесной, ул. Победы, 46'),
('614753, г. Лесной, ул. Полевая, 35'),
('426030, г. Лесной, ул. Маяковского, 44'),
('450375, г. Лесной, ул. Клубная, 44'),
('625560, г. Лесной, ул. Некрасова, 12'),
('630201, г. Лесной, ул. Комсомольская, 17'),
('190949, г. Лесной, ул. Мичурина, 26');

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