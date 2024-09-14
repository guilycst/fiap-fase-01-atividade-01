import sqlite3
from dataclasses import dataclass
from typing import Generator

@dataclass
class Model:
    id: int | None
    crop: str
    shape: str
    total_area: float
    management_area: float
    usable_area: float
    input : float
    input_amount: float
    
class Field:
    def __init__(self, name):
        self.name = name
        
    def update_field(self, id, value):
        _update_field(id, self.name, value)
        
DB_NAME = "fiap-agro.db"

CROP = Field("crop")
SHAPE = Field("shape")
TOTAL_AREA = Field("total_area")
MANAGEMENT_AREA = Field("management_area")
USABLE_AREA = Field("usable_area")
INPUT = Field("input")
INPUT_AMOUNT = Field("input_amount")

# Função para salvar os dados no banco de dados
def save_data(model: Model):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planting_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT,
            shape TEXT,
            total_area REAL,
            management_area REAL,
            usable_area REAL,
            input TEXT,
            input_amount REAL
        )
    """)
    if model.id:
        cursor.execute("""
            UPDATE planting_data
            SET crop = ?, shape = ?, total_area = ?, management_area = ?, usable_area = ?, input = ?, input_amount = ?
            WHERE id = ?
        """, (model.crop, model.shape, model.total_area, model.management_area, model.usable_area, model.input, model.input_amount, model.id))
    else:
        cursor.execute("""
            INSERT INTO planting_data (crop, shape, total_area, management_area, usable_area, input, input_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (model.crop, model.shape, model.total_area, model.management_area, model.usable_area, model.input, model.input_amount))
    conn.commit()
    conn.close()
    
def delete_data(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM planting_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def _update_field(id, field, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE planting_data SET {field} = ? WHERE id = ?", (value, id))
    conn.commit()
    conn.close()

# Função para carregar dados paginados
def load_data(page_size=10) -> Generator[Model, None, None]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    offset = 0
    cursor.execute("SELECT * FROM planting_data LIMIT ? OFFSET ?", (page_size, offset))
    records = cursor.fetchall()
    
    while len(records) > 0:
        for record in records:
            yield Model(*record)
        offset += page_size
        cursor.execute("SELECT * FROM planting_data LIMIT ? OFFSET ?", (page_size, offset))
        records = cursor.fetchall()
    conn.close()
