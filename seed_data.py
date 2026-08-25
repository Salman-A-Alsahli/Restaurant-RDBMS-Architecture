import random
from datetime import datetime

import psycopg2
from faker import Faker

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "restaurant_db",
    "user": "postgres",
    "password": "postgres",
}

faker = Faker()


def truncate_text(value, length):
    if value is None:
        return None
    return str(value)[:length]


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def clear_data(cur):
    print("Clearing existing seed data...")
    cur.execute(
        """
        TRUNCATE TABLE hasordercook, cooking, provide, person_order, customer, employee, chef, dish, restaurant_branch, person
        RESTART IDENTITY CASCADE;
        """
    )


def seed_branches(cur):
    branches = [
        ("Chicago", "100 W Randolph St", "60601", "chicago@northstargrill.com", "+1-312-555-0101"),
        ("New York", "25 Broadway Ave", "10004", "newyork@northstargrill.com", "+1-212-555-0102"),
        ("Los Angeles", "890 Sunset Blvd", "90028", "la@northstargrill.com", "+1-323-555-0103"),
    ]

    branch_rows = []
    for city, street, zip_code, email, phone in branches:
        branch_rows.append((city, street, zip_code, email, phone))

    cur.executemany(
        """
        INSERT INTO restaurant_branch (city, street, zip_code, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        branch_rows,
    )
    print(f"Inserted {len(branch_rows)} branches.")


def seed_dishes(cur):
    dishes = [
        ("Margherita Pizza", 14.25, "Tomato basil sauce, mozzarella", "Gluten", "15 min"),
        ("BBQ Chicken Burger", 16.50, "Grilled chicken, bbq sauce", "None", "12 min"),
        ("Truffle Pasta", 18.00, "Cream sauce, mushrooms", "Dairy", "18 min"),
        ("Caesar Salad", 11.75, "Lettuce, parmesan", "Egg", "8 min"),
        ("Salmon Bowl", 19.50, "Salmon, rice, greens", "Fish", "15 min"),
        ("Beef Tacos", 15.95, "Seasoned beef, tortillas", "None", "10 min"),
        ("Veggie Risotto", 17.25, "Arborio rice, vegetables", "Dairy", "20 min"),
        ("Lemon Herb Chicken", 18.75, "Roasted chicken, herbs", "None", "18 min"),
        ("Shrimp Alfredo", 20.00, "Shrimp, creamy pasta", "Shellfish", "16 min"),
        ("Spicy Ramen", 17.50, "Noodles, broth, chili", "Soy", "14 min"),
        ("Crispy Calamari", 13.25, "Fried squid rings", "Shellfish", "9 min"),
        ("Steak Frites", 23.00, "Prime steak, fries", "None", "22 min"),
        ("Avocado Toast", 10.50, "Sourdough, avocado", "None", "7 min"),
        ("Greek Wrap", 12.90, "Chicken, feta, lettuce", "Dairy", "9 min"),
        ("Mango Salsa Tacos", 13.75, "Mango, black beans", "None", "10 min"),
        ("Pesto Gnocchi", 16.75, "Potato gnocchi, pesto", "Nuts", "15 min"),
        ("Miso Glazed Tofu", 15.00, "Tofu, rice, vegetables", "Soy", "13 min"),
        ("Buffalo Wings", 14.95, "Chicken wings, buffalo sauce", "None", "11 min"),
        ("Chocolate Lava Cake", 9.50, "Dark chocolate cake", "Dairy", "6 min"),
        ("Fruit Parfait", 8.75, "Yogurt, berries", "Dairy", "5 min"),
    ]

    cur.executemany(
        """
        INSERT INTO dish (name, price, recipe, food_allergy, serving_time)
        VALUES (%s, %s, %s, %s, %s)
        """,
        dishes,
    )
    print(f"Inserted {len(dishes)} dishes.")


def seed_people(cur):
    people = []
    customer_count = 700
    employee_count = 250
    chef_count = 50

    for _ in range(1000):
        first_name = truncate_text(faker.first_name(), 15)
        middle_name = truncate_text(faker.first_name(), 15) if random.choice([True, False]) else None
        last_name = truncate_text(faker.last_name(), 15)
        phone = truncate_text(faker.phone_number(), 20)
        email = truncate_text(faker.unique.email(), 100)
        address = truncate_text(f"{faker.street_name()} {faker.building_number()}", 30)
        people.append((first_name, middle_name, last_name, phone, email, address))

    new_person_ids = []
    for person in people:
        cur.execute(
            """
            INSERT INTO person (first_name, middle_name, last_name, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            person,
        )
        new_person_ids.append(cur.fetchone()[0])

    print(f"Inserted {len(new_person_ids)} persons.")
    return new_person_ids


def seed_roles(cur, person_ids):
    customer_ids = person_ids[:700]
    employee_ids = person_ids[700:950]
    chef_ids = person_ids[950:]

    for person_id in customer_ids:
        cur.execute(
            "INSERT INTO customer (personid, password) VALUES (%s, %s)",
            (person_id, faker.password(length=12)),
        )

    for person_id in employee_ids:
        cur.execute(
            "INSERT INTO employee (personid, position, salary) VALUES (%s, %s, %s)",
            (person_id, random.choice(["Manager", "Cashier", "Waiter", "Host", "Supervisor", "Cleaner"]), round(random.uniform(30000, 85000), 2)),
        )

    chef_rows = []
    previous_chef_ids = []
    for idx, person_id in enumerate(chef_ids):
        mentor_id = previous_chef_ids[random.randrange(len(previous_chef_ids))] if previous_chef_ids else None
        chef_rows.append((
            person_id,
            round(random.uniform(55000, 140000), 2),
            random.choice(["Italian", "Japanese", "Mexican", "French", "Seafood", "Pastry", "Grill", "Vegetarian"]),
            random.randint(1, 3),
            mentor_id,
        ))
        previous_chef_ids.append(person_id)

    cur.executemany(
        """
        INSERT INTO chef (personid, salary, speciality, branchnumber, chef_tutorid)
        VALUES (%s, %s, %s, %s, %s)
        """,
        chef_rows,
    )

    print(f"Inserted {len(customer_ids)} customers, {len(employee_ids)} employees, and {len(chef_rows)} chefs.")
    return customer_ids, employee_ids, chef_ids


def seed_branch_dishes(cur):
    dish_names = [
        "Margherita Pizza", "BBQ Chicken Burger", "Truffle Pasta", "Caesar Salad", "Salmon Bowl",
        "Beef Tacos", "Veggie Risotto", "Lemon Herb Chicken", "Shrimp Alfredo", "Spicy Ramen",
        "Crispy Calamari", "Steak Frites", "Avocado Toast", "Greek Wrap", "Mango Salsa Tacos",
        "Pesto Gnocchi", "Miso Glazed Tofu", "Buffalo Wings", "Chocolate Lava Cake", "Fruit Parfait",
    ]

    provide_rows = []
    for branch_id in range(1, 4):
        for dish_name in dish_names:
            provide_rows.append((branch_id, dish_name))

    cur.executemany(
        "INSERT INTO provide (branchnum, dishname) VALUES (%s, %s)",
        provide_rows,
    )
    print(f"Inserted {len(provide_rows)} branch-dish mappings.")


def seed_chef_dishes(cur, chef_ids):
    dish_names = [
        "Margherita Pizza", "BBQ Chicken Burger", "Truffle Pasta", "Caesar Salad", "Salmon Bowl",
        "Beef Tacos", "Veggie Risotto", "Lemon Herb Chicken", "Shrimp Alfredo", "Spicy Ramen",
        "Crispy Calamari", "Steak Frites", "Avocado Toast", "Greek Wrap", "Mango Salsa Tacos",
        "Pesto Gnocchi", "Miso Glazed Tofu", "Buffalo Wings", "Chocolate Lava Cake", "Fruit Parfait",
    ]

    cooking_rows = []
    for chef_id in chef_ids:
        selected_dishes = random.sample(dish_names, random.randint(3, 5))
        for dish_name in selected_dishes:
            cooking_rows.append((chef_id, dish_name))

    cur.executemany(
        "INSERT INTO cooking (chefid, dishname) VALUES (%s, %s)",
        cooking_rows,
    )
    print(f"Inserted {len(cooking_rows)} chef-dish mappings.")


def seed_orders(cur, customer_ids):
    dish_names = [
        "Margherita Pizza", "BBQ Chicken Burger", "Truffle Pasta", "Caesar Salad", "Salmon Bowl",
        "Beef Tacos", "Veggie Risotto", "Lemon Herb Chicken", "Shrimp Alfredo", "Spicy Ramen",
        "Crispy Calamari", "Steak Frites", "Avocado Toast", "Greek Wrap", "Mango Salsa Tacos",
        "Pesto Gnocchi", "Miso Glazed Tofu", "Buffalo Wings", "Chocolate Lava Cake", "Fruit Parfait",
    ]

    order_count = 5000
    order_dish_rows = []

    for order_index in range(1, order_count + 1):
        customer_id = random.choice(customer_ids)
        order_time = faker.time()
        order_date = faker.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        comments = truncate_text(faker.sentence(nb_words=6), 50) if random.choice([True, False]) else None

        cur.execute(
            """
            INSERT INTO person_order (o_time, o_date, comments, person_id)
            VALUES (%s, %s, %s, %s)
            RETURNING num
            """,
            (order_time, order_date, comments, customer_id),
        )
        order_num = cur.fetchone()[0]

        selected_dishes = random.sample(dish_names, random.randint(1, 4))
        for dish_name in selected_dishes:
            order_dish_rows.append((order_num, dish_name))

        if order_index % 500 == 0:
            print(f"Inserted {order_index} orders so far...")

    cur.executemany(
        "INSERT INTO hasordercook (ordernum, dishname) VALUES (%s, %s)",
        order_dish_rows,
    )

    print(f"Inserted {order_count} orders and {len(order_dish_rows)} order-dish mappings.")


def main():
    print("Starting restaurant database seed generation...")
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            clear_data(cur)
            seed_branches(cur)
            seed_dishes(cur)
            person_ids = seed_people(cur)
            customer_ids, employee_ids, chef_ids = seed_roles(cur, person_ids)
            seed_branch_dishes(cur)
            seed_chef_dishes(cur, chef_ids)
            seed_orders(cur, customer_ids)
        conn.commit()
        print("Database seeding completed successfully.")
    except Exception as exc:
        conn.rollback()
        print(f"Seeding failed: {exc}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
