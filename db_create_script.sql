-- Удаление таблиц в обратном порядке для чистого пересоздания
DROP TABLE IF EXISTS "order_items";
DROP TABLE IF EXISTS "orders";
DROP TABLE IF EXISTS "products";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "pickup_points";
DROP TABLE IF EXISTS "categories";
DROP TABLE IF EXISTS "manufacturers";
DROP TABLE IF EXISTS "suppliers";

-- Таблицы-справочники
CREATE TABLE "categories" (
    "category_id" SERIAL PRIMARY KEY,
    "category_name" VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE "manufacturers" (
    "manufacturer_id" SERIAL PRIMARY KEY,
    "manufacturer_name" VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE "suppliers" (
    "supplier_id" SERIAL PRIMARY KEY,
    "supplier_name" VARCHAR(100) UNIQUE NOT NULL
);

-- Основные таблицы
CREATE TABLE "users" (
    "user_id" SERIAL PRIMARY KEY,
    "full_name" VARCHAR(255) NOT NULL,
    "login" VARCHAR(100) UNIQUE NOT NULL,
    "password" VARCHAR(100) NOT NULL,
    "role_name" VARCHAR(50) NOT NULL
);

CREATE TABLE "pickup_points" (
    "point_id" SERIAL PRIMARY KEY,
    "address" TEXT NOT NULL
);

CREATE TABLE "products" (
    "product_sku" VARCHAR(20) PRIMARY KEY,
    "product_name" VARCHAR(255) NOT NULL,
    "unit" VARCHAR(20) NOT NULL DEFAULT 'шт.',
    "price" DECIMAL(10, 2) NOT NULL CHECK ("price" >= 0),
    "current_discount" INT NOT NULL DEFAULT 0,
    "stock_quantity" INT NOT NULL DEFAULT 0,
    "description" TEXT,
    "image_path" VARCHAR(255),
    "category_id" INT,
    "manufacturer_id" INT,
    "supplier_id" INT,
    FOREIGN KEY ("category_id") REFERENCES "categories"("category_id"),
    FOREIGN KEY ("manufacturer_id") REFERENCES "manufacturers"("manufacturer_id"),
    FOREIGN KEY ("supplier_id") REFERENCES "suppliers"("supplier_id")
);

CREATE TABLE "orders" (
    "order_id" SERIAL PRIMARY KEY,
    "status" VARCHAR(50) NOT NULL,
    "order_date" DATE NOT NULL,
    "delivery_date" DATE NOT NULL,
    "pickup_point_id" INT NOT NULL,
    "client_user_id" INT,
    "order_code" INT NOT NULL,
    FOREIGN KEY ("pickup_point_id") REFERENCES "pickup_points"("point_id"),
    FOREIGN KEY ("client_user_id") REFERENCES "users"("user_id")
);

CREATE TABLE "order_items" (
    "order_item_id" SERIAL PRIMARY KEY,
    "order_id" INT NOT NULL,
    "product_sku" VARCHAR(20) NOT NULL,
    "quantity" INT NOT NULL,
    FOREIGN KEY ("order_id") REFERENCES "orders"("order_id") ON DELETE CASCADE,
    FOREIGN KEY ("product_sku") REFERENCES "products"("product_sku")
);