
def create_product_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INT PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            total INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)

def insert_product(conn, id: int, name: str, total: int):
    with conn.cursor() as cursor:
        cursor.execute("""INSERT IGNORE INTO product (id, name, total) VALUES (%s, %s, %s)""", (id, name, total))
        conn.commit()

def select_product_by_id(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM product WHERE id = %s""", (id,))
        return cursor.fetchone()

def select_product_for_update_by_id(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM product WHERE id = %s FOR UPDATE""", (id,))
        return cursor.fetchone()

def select_product_for_share_by_id(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM product WHERE id = %s FOR SHARE""", (id,))
        return cursor.fetchone()

def increment_product(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("""UPDATE product SET total = total + 1 WHERE id = %s""", (id,))

def update_product_total(conn, id: int, total: int):
    with conn.cursor() as cursor:
        cursor.execute("""UPDATE product SET total = %s WHERE id = %s""", (total, id))

def delete_product(conn, id: int):
    with conn.cursor() as cursor:
        cursor.execute("""DELETE FROM product WHERE id = %s""", (id,))
    