import sqlite3

# Função para salvar os dados no banco de dados
def save_data(crop, shape, total_area, usable_area, product, input_needed):
    conn = sqlite3.connect("agriculture.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planting_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT,
            shape TEXT,
            total_area REAL,
            usable_area REAL,
            product TEXT,
            input_needed REAL
        )
    """)
    cursor.execute("""
        INSERT INTO planting_data (crop, shape, total_area, usable_area, product, input_needed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (crop, shape, total_area, usable_area, product, input_needed))
    conn.commit()
    conn.close()

# Função para carregar dados paginados
def load_paginated_data(page_size=10, page=1):
    conn = sqlite3.connect("agriculture.db")
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM planting_data LIMIT ? OFFSET ?", (page_size, offset))
    records = cursor.fetchall()
    conn.close()
    return records
