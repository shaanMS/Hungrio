# datafeed.py - CORRECTED VERSION (all NOT NULL fields included)
import psycopg2
from datetime import datetime

DB_CONFIG = {
    'dbname': 'restaurant_database',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

# CATEGORIES: id, name, slug, is_active, dt
CATEGORIES = [
    ("cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "Starters", "starters", True, "2025-12-27 00:38:33.214518"),
    ("41e695cf-fafe-4a0f-9729-bcacc2e7841f", "Breads", "breads", True, "2025-12-27 00:38:33.214518"),
    ("609f622d-72d8-428c-8f54-bfe9b0731f4d", "Biryani", "biryani", True, "2025-12-27 00:38:33.214518"),
    ("630b0281-5c91-42b0-8321-c2f4305d24b2", "Accompaniments", "accompaniments", True, "2025-12-27 00:38:33.214518"),
    ("e7c3965c-29e7-4193-ba58-6a6e42b23b13", "Desserts", "desserts", True, "2025-12-27 00:38:33.214518"),
]

# SUBCATEGORIES: id, category_id, name, slug, is_active, dt
SUBCATEGORIES = [
    ("de2a7d3f-d0bd-450a-9467-c6eb678fd214", "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "Paneer Tikka Variants", "paneer-tikka-variants", True, "2025-12-27 00:38:33.237905"),
    ("846cf48b-d3a7-445e-9131-6370840e04f8", "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "Mushroom Starters", "mushroom-starters", True, "2025-12-27 00:38:33.237905"),
    ("2e4cd871-4341-4789-bafc-466c83746092", "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "Aloo Starters", "aloo-starters", True, "2025-12-27 00:38:33.237905"),
    ("80fe5aec-35c6-43e8-9722-fd003d1f6e41", "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "Veg Platters", "veg-platters", True, "2025-12-27 00:38:33.237905"),
    ("d1ac2337-d9e8-40a5-ba06-226ea79aa030", "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "Roti", "roti", True, "2025-12-27 00:38:33.261331"),
    ("94484e15-0875-4306-b0a7-7fc1d338075a", "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "Paratha", "paratha", True, "2025-12-27 00:38:33.261331"),
    ("25760bb9-b54e-4c31-a2f4-130cec20b472", "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "Kulcha", "kulcha", True, "2025-12-27 00:38:33.261331"),
    ("b64b12b9-4172-454b-8cc2-f351451ffe05", "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "Naan", "naan", True, "2025-12-27 00:38:33.261331"),
    ("8391f6d4-4aca-438a-bed7-5b110f795bc4", "609f622d-72d8-428c-8f54-bfe9b0731f4d", "Veg Dum Biryani", "veg-dum-biryani", True, "2025-12-27 00:38:33.264317"),
    ("d701d5ab-34a2-4edd-9297-dedaaa086ef5", "609f622d-72d8-428c-8f54-bfe9b0731f4d", "Paneer Biryani", "paneer-biryani", True, "2025-12-27 00:38:33.264317"),
    ("5f13c71c-a562-4f2a-8217-d5166ee5880a", "630b0281-5c91-42b0-8321-c2f4305d24b2", "Papad", "papad", True, "2025-12-27 00:38:33.266487"),
    ("3f6640bb-400a-4305-80ab-0d44621b65f7", "630b0281-5c91-42b0-8321-c2f4305d24b2", "Salad", "salad", True, "2025-12-27 00:38:33.266487"),
    ("b3e6a3d0-a8af-451d-86b4-af8d825f476e", "630b0281-5c91-42b0-8321-c2f4305d24b2", "Raita", "raita", True, "2025-12-27 00:38:33.266487"),
    ("f4cd7ce1-b77d-4399-80d7-42f919ba5ca8", "630b0281-5c91-42b0-8321-c2f4305d24b2", "Curd", "curd", True, "2025-12-27 00:38:33.266487"),
    ("e4d85311-aedb-47a2-beff-c60cbda536b6", "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "Kheer / Phirni", "kheer-phirni", True, "2025-12-27 00:38:33.268993"),
    ("309dfe12-f5c2-45b6-bbdf-3f17f93072ad", "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "Indian Sweets", "indian-sweets", True, "2025-12-27 00:38:33.268993"),
]

# PRODUCTS: id, cat_id, sub_id, name, desc, is_veg, price, slug, discount_percentage, final_price, is_active, dt
PRODUCTS = [
    (1, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Tandoori Paneer Tikka", "Fresh cottage cheese marinated in yoghurt, red chilli paste, spices & grilled", True, 320.00, "tandoori-paneer-tikka", 0.00, 320.00, True, "2025-12-27 00:39:03.08645"),
    (2, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Malai Paneer Tikka", "Fresh cottage cheese marinated in creamy cashewnut paste & grilled", True, 340.00, "malai-paneer-tikka", 0.00, 340.00, True, "2025-12-27 00:39:03.08645"),
    (3, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Afghani Paneer Tikka", "Fresh cottage cheese marinated in mildly spiced marination & grilled", True, 330.00, "afghani-paneer-tikka", 0.00, 330.00, True, "2025-12-27 00:39:03.08645"),
    (4, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Zafrani Paneer Tikka", "Fresh cottage cheese marinated in yoghurt, saffron flavours & grilled", True, 360.00, "zafrani-paneer-tikka", 0.00, 360.00, True, "2025-12-27 00:39:03.08645"),
    (5, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Lasooni Paneer Tikka", "Fresh cottage cheese marinated in yoghurt, garlic & spices & grilled", True, 330.00, "lasooni-paneer-tikka", 0.00, 330.00, True, "2025-12-27 00:39:03.08645"),
    (6, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Paneer Harimirchi Tikka", "Fresh cottage cheese marinated in yoghurt, green chilli paste & spices", True, 340.00, "paneer-harimirchi-tikka", 0.00, 340.00, True, "2025-12-27 00:39:03.08645"),
    (7, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "de2a7d3f-d0bd-450a-9467-c6eb678fd214", "Paneer Ajwaini Tikka", "Fresh cottage cheese marinated in yoghurt, spices & carom seeds", True, 330.00, "paneer-ajwaini-tikka", 0.00, 330.00, True, "2025-12-27 00:39:03.08645"),
    (8, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "846cf48b-d3a7-445e-9131-6370840e04f8", "Tandoori Mushroom", "Button mushrooms marinated in spiced yoghurt & grilled", True, 280.00, "tandoori-mushroom", 0.00, 280.00, True, "2025-12-27 00:39:03.08645"),
    (9, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "846cf48b-d3a7-445e-9131-6370840e04f8", "Butter Garlic Mushroom", "Button mushrooms grilled with butter garlic marinade", True, 290.00, "butter-garlic-mushroom", 0.00, 290.00, True, "2025-12-27 00:39:03.08645"),
    (10, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "2e4cd871-4341-4789-bafc-466c83746092", "Atishi Aloo", "Baby potatoes grilled with spicy marinade", True, 260.00, "atishi-aloo", 0.00, 260.00, True, "2025-12-27 00:39:03.08645"),
    (11, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "2e4cd871-4341-4789-bafc-466c83746092", "Tandoori Chatpata Aloo", "Baby potatoes in tangy marinade & grilled", True, 270.00, "tandoori-chatpata-aloo", 0.00, 270.00, True, "2025-12-27 00:39:03.08645"),
    (12, "cd7fb741-a12e-4a50-a0b4-45f41e9db2e7", "80fe5aec-35c6-43e8-9722-fd003d1f6e41", "Vegetarian Platter", "Assortment of paneer, potatoes & mushrooms", True, 480.00, "vegetarian-platter", 0.00, 480.00, True, "2025-12-27 00:39:03.08645"),
    (13, "609f622d-72d8-428c-8f54-bfe9b0731f4d", "8391f6d4-4aca-438a-bed7-5b110f795bc4", "Subz Dum Biryani", "", True, 380.00, "subz-dum-biryani", 0.00, 380.00, True, "2025-12-27 00:39:03.08645"),
    (14, "609f622d-72d8-428c-8f54-bfe9b0731f4d", "d701d5ab-34a2-4edd-9297-dedaaa086ef5", "Paneer Tikka Biryani", "", True, 420.00, "paneer-tikka-biryani", 0.00, 420.00, True, "2025-12-27 00:39:03.08645"),
    (15, "609f622d-72d8-428c-8f54-bfe9b0731f4d", "d701d5ab-34a2-4edd-9297-dedaaa086ef5", "Paneer Makhni Biryani", "", True, 430.00, "paneer-makhni-biryani", 0.00, 430.00, True, "2025-12-27 00:39:03.08645"),
    (16, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "d1ac2337-d9e8-40a5-ba06-226ea79aa030", "Roomali Roti", "", True, 45.00, "roomali-roti", 0.00, 45.00, True, "2025-12-27 00:39:03.08645"),
    (17, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "94484e15-0875-4306-b0a7-7fc1d338075a", "Mughlai Paratha", "", True, 80.00, "mughlai-paratha", 0.00, 80.00, True, "2025-12-27 00:39:03.08645"),
    (18, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "94484e15-0875-4306-b0a7-7fc1d338075a", "Lachha Paratha", "", True, 75.00, "lachha-paratha", 0.00, 75.00, True, "2025-12-27 00:39:03.08645"),
    (19, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "94484e15-0875-4306-b0a7-7fc1d338075a", "Lachha Paratha (Ajwain/Pudina)", "", True, 85.00, "lachha-paratha-ajwain-pudina", 0.00, 85.00, True, "2025-12-27 00:39:03.08645"),
    (20, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "25760bb9-b54e-4c31-a2f4-130cec20b472", "Stuffed Kulcha (Aalo/Onion/Garlic)", "", True, 90.00, "stuffed-kulcha-aalo-onion-garlic", 0.00, 90.00, True, "2025-12-27 00:39:03.08645"),
    (21, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "25760bb9-b54e-4c31-a2f4-130cec20b472", "Stuffed Kulcha (Paneer /Mix)", "", True, 110.00, "stuffed-kulcha-paneer-mix", 0.00, 110.00, True, "2025-12-27 00:39:03.08645"),
    (22, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "b64b12b9-4172-454b-8cc2-f351451ffe05", "Stuffed Naan (Aloo/Onion/Garlic)", "", True, 100.00, "stuffed-naan-aloo-onion-garlic", 0.00, 100.00, True, "2025-12-27 00:39:03.08645"),
    (23, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "b64b12b9-4172-454b-8cc2-f351451ffe05", "Stuffed Naan (Paneer /Mix)", "", True, 120.00, "stuffed-naan-paneer-mix", 0.00, 120.00, True, "2025-12-27 00:39:03.08645"),
    (24, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "d1ac2337-d9e8-40a5-ba06-226ea79aa030", "Onion Missi Roti", "", True, 70.00, "onion-missi-roti", 0.00, 70.00, True, "2025-12-27 00:39:03.08645"),
    (25, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "b64b12b9-4172-454b-8cc2-f351451ffe05", "Naan", "", True, 60.00, "naan", 0.00, 60.00, True, "2025-12-27 00:39:03.08645"),
    (26, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "d1ac2337-d9e8-40a5-ba06-226ea79aa030", "Tandori Roti", "", True, 45.00, "tandori-roti", 0.00, 45.00, True, "2025-12-27 00:39:03.08645"),
    (27, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "d1ac2337-d9e8-40a5-ba06-226ea79aa030", "Tawa Roti", "", True, 40.00, "tawa-roti", 0.00, 40.00, True, "2025-12-27 00:39:03.08645"),
    (28, "41e695cf-fafe-4a0f-9729-bcacc2e7841f", "d1ac2337-d9e8-40a5-ba06-226ea79aa030", "Missi Roti", "", True, 55.00, "missi-roti", 0.00, 55.00, True, "2025-12-27 00:39:03.08645"),
    (29, "630b0281-5c91-42b0-8321-c2f4305d24b2", "5f13c71c-a562-4f2a-8217-d5166ee5880a", "Roasted Papad", "", True, 25.00, "roasted-papad", 0.00, 25.00, True, "2025-12-27 00:39:03.08645"),
    (30, "630b0281-5c91-42b0-8321-c2f4305d24b2", "5f13c71c-a562-4f2a-8217-d5166ee5880a", "Fried Papad", "", True, 30.00, "fried-papad", 0.00, 30.00, True, "2025-12-27 00:39:03.08645"),
    (31, "630b0281-5c91-42b0-8321-c2f4305d24b2", "5f13c71c-a562-4f2a-8217-d5166ee5880a", "Masala Papad", "", True, 40.00, "masala-papad", 0.00, 40.00, True, "2025-12-27 00:39:03.08645"),
    (32, "630b0281-5c91-42b0-8321-c2f4305d24b2", "3f6640bb-400a-4305-80ab-0d44621b65f7", "Onion Salad", "", True, 50.00, "onion-salad", 0.00, 50.00, True, "2025-12-27 00:39:03.08645"),
    (33, "630b0281-5c91-42b0-8321-c2f4305d24b2", "3f6640bb-400a-4305-80ab-0d44621b65f7", "Green Salad", "", True, 60.00, "green-salad", 0.00, 60.00, True, "2025-12-27 00:39:03.08645"),
    (34, "630b0281-5c91-42b0-8321-c2f4305d24b2", "b3e6a3d0-a8af-451d-86b4-af8d825f476e", "Mixed Veg Raita", "", True, 70.00, "mixed-veg-raita", 0.00, 70.00, True, "2025-12-27 00:39:03.08645"),
    (35, "630b0281-5c91-42b0-8321-c2f4305d24b2", "b3e6a3d0-a8af-451d-86b4-af8d825f476e", "Boondi Raita", "", True, 65.00, "boondi-raita", 0.00, 65.00, True, "2025-12-27 00:39:03.08645"),
    (36, "630b0281-5c91-42b0-8321-c2f4305d24b2", "b3e6a3d0-a8af-451d-86b4-af8d825f476e", "Bhurani Raita", "", True, 70.00, "bhurani-raita", 0.00, 70.00, True, "2025-12-27 00:39:03.08645"),
    (37, "630b0281-5c91-42b0-8321-c2f4305d24b2", "f4cd7ce1-b77d-4399-80d7-42f919ba5ca8", "Curd", "", True, 50.00, "curd", 0.00, 50.00, True, "2025-12-27 00:39:03.08645"),
    (38, "630b0281-5c91-42b0-8321-c2f4305d24b2", "3f6640bb-400a-4305-80ab-0d44621b65f7", "Tomato and Onion Kachumber", "", True, 55.00, "tomato-and-onion-kachumber", 0.00, 55.00, True, "2025-12-27 00:39:03.08645"),
    (39, "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "e4d85311-aedb-47a2-beff-c60cbda536b6", "Kulhad Phirni", "", True, 120.00, "kulhad-phirni", 0.00, 120.00, True, "2025-12-27 00:39:03.08645"),
    (40, "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "e4d85311-aedb-47a2-beff-c60cbda536b6", "Zafrani Kheer", "", True, 140.00, "zafrani-kheer", 0.00, 140.00, True, "2025-12-27 00:39:03.08645"),
    (41, "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "309dfe12-f5c2-45b6-bbdf-3f17f93072ad", "Shahi Tukda", "", True, 150.00, "shahi-tukda", 0.00, 150.00, True, "2025-12-27 00:39:03.08645"),
    (42, "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "309dfe12-f5c2-45b6-bbdf-3f17f93072ad", "Seviyan Ka Muzaffar", "", True, 160.00, "seviyan-ka-muzaffar", 0.00, 160.00, True, "2025-12-27 00:39:03.08645"),
    (43, "e7c3965c-29e7-4193-ba58-6a6e42b23b13", "309dfe12-f5c2-45b6-bbdf-3f17f93072ad", "ZamZam Kalakand", "", True, 180.00, "zamzam-kalakand", 0.00, 180.00, True, "2025-12-27 00:39:03.08645"),
]

def insert_data():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("Inserting Categories...")
        cur.executemany(
            "INSERT INTO category_category (id, name, slug, is_active, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
            [(id, name, slug, is_active, dt, dt) for id, name, slug, is_active, dt in CATEGORIES]
        )

        print("Inserting Subcategories...")
        cur.executemany(
            "INSERT INTO category_subcategory (id, category_id, name, slug, is_active, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
            [(id, cat_id, name, slug, is_active, dt, dt) for id, cat_id, name, slug, is_active, dt in SUBCATEGORIES]
        )

        print("Inserting Products...")
        cur.executemany(
            "INSERT INTO product_product (id, category_id, subcategory_id, name, description, is_veg, base_price, slug, discount_percentage, final_price, is_active, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
            [(pid, cat_id, sub_id if sub_id else None, name, desc, is_veg, price, slug, discount, final_price, is_active, dt, dt)
             for pid, cat_id, sub_id, name, desc, is_veg, price, slug, discount, final_price, is_active, dt in PRODUCTS]
        )

        conn.commit()
        print("\n" + "="*70)
        print("             अब सब डेटा डाल दिया गया है! अब खुश? 😎             ")
        print("="*70)

    except Exception as e:
        print("Error:", e)
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    insert_data()








