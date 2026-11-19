import os
import json
import csv
import sqlite3
import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml

DB_PATH = 'DB.db'
OUT_DIR = 'out'

# Главная таблица и её поля
MAIN_TABLE = 'Session'
MAIN_FIELDS = ['session_id', 'film_id', 'hall_id', 'start_time', 'price']

# Связанные таблицы
RELATIONS = [
    {
        'fk_field': 'film_id',
        'table': 'Film',
        'fields': ['film_id', 'title', 'duration'],
        'alias': 'film'
    },
    {
        'fk_field': 'hall_id',
        'table': 'Hall',
        'fields': ['hall_id', 'name', 'rows_count', 'seats_per_row'],
        'alias': 'hall'
    }
]

def get_connection():
    conn = sqlite3.connect("DB.db")
    conn.row_factory = sqlite3.Row
    return conn


def fetch_rows(table, fields):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT {', '.join(fields)} FROM {table}")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def fetch_related(related_table, fk_field, fk_value, fields):
    """Извлекает связанную запись по внешнему ключу."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT {', '.join(fields)} FROM {related_table} WHERE {fk_field} = ?",
        (fk_value,)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def build_data(main_table,main_fields, relations):
    """Собирает данные с вложенными связями."""
    rows = fetch_rows(main_table, main_fields)

    data = []
    for row in rows:
        record = dict(row)
        for rel in relations:
            related = fetch_related(
                rel['table'],
                rel['fk_field'],
                row[rel['fk_field']],
                rel['fields']
            )
            record[rel['alias']] = related
        data.append(record)

    return data


# ============================================================
# Экспорт в JSON
# ============================================================

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# Экспорт в CSV
# ============================================================

def flatten_record(record, relations_aliases):
    """Превращает вложенный словарь в плоский для CSV."""
    flat = {}
    for key, value in record.items():
        if key in relations_aliases and isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flat[f"{key}_{sub_key}"] = sub_value
        else:
            flat[key] = value
    return flat


def save_csv(data, path, relations_aliases):
    flat_rows = [flatten_record(r, relations_aliases) for r in data]
    fieldnames = list(flat_rows[0].keys())

    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_rows)


# ============================================================
# Экспорт в XML
# ============================================================

def dict_to_xml(tag, d):
    """Рекурсивно превращает словарь в XML-элемент."""
    elem = ET.Element(tag)
    for key, val in d.items():
        if isinstance(val, dict):
            child = dict_to_xml(key, val)
            elem.append(child)
        else:
            child = ET.Element(key)
            child.text = str(val) if val is not None else ''
            elem.append(child)
    return elem


def save_xml(data, path, root_tag='sessions', item_tag='session'):
    root = ET.Element(root_tag)
    for record in data:
        root.append(dict_to_xml(item_tag, record))

    rough_string = ET.tostring(root, encoding='unicode')
    parsed = minidom.parseString(rough_string)
    pretty = parsed.toprettyxml(indent='  ', encoding='utf-8')

    with open(path, 'wb') as f:
        f.write(pretty)


# ============================================================
# Экспорт в YAML
# ============================================================

def save_yaml(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return True


# ============================================================
# Главная функция
# ============================================================

def export_all(main_table, main_fields, relations):
    """Собирает данные и сохраняет во все 4 формата."""

    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_data(main_table,main_fields, relations)

    json_path = os.path.join(OUT_DIR, 'data.json')
    csv_path = os.path.join(OUT_DIR, 'data.csv')
    xml_path = os.path.join(OUT_DIR, 'data.xml')
    yaml_path = os.path.join(OUT_DIR, 'data.yaml')

    save_json(data, json_path)
    print(f"✓ JSON:  {len(data)} записей -> {json_path}")

    relations_aliases = [rel['alias'] for rel in relations]
    save_csv(data, csv_path, relations_aliases)
    print(f"✓ CSV:   {len(data)} записей -> {csv_path}")

    save_xml(data, xml_path)
    print(f"✓ XML:   {len(data)} записей -> {xml_path}")

    ok = save_yaml(data, yaml_path)
    if ok:
        print(f"✓ YAML:  {len(data)} записей -> {yaml_path}")

    print(f"\nФайлы сохранены в папке: {os.path.abspath(OUT_DIR)}")


print(f"Экспорт таблицы '{MAIN_TABLE}' со связями...")
export_all(MAIN_TABLE, MAIN_FIELDS, RELATIONS)