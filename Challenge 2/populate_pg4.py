from sqlalchemy import create_engine, text
from faker import Faker
import time

import dotenv
import os

env = dotenv.load_dotenv()

engine = create_engine(f'postgresql+psycopg2://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@{os.getenv("PG_ADDRESS")}/{os.getenv("PG_DB")}').connect()

fake = Faker()

try:
    engine.execute(text(
        """
            CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            address VARCHAR(200),
            phone_number VARCHAR(50)
        );
        """
    ))
    engine.commit()
except Exception as e:
    print("Exception: ", e)
    engine.rollback()

for i in range(10000): # generate 100 customers
    try:
        name = fake.name()
        email = fake.email()
        address = fake.address()
        phone_number = fake.phone_number()
        result = engine.execute(text(f"INSERT INTO customers (name, email, address, phone_number) VALUES ('{name}', '{email}', '{address}', '{phone_number}')"))
        print("Result: ", result)
        print("{"f"""
            'name' : '{name}',
            'email' : '{email}',
            'address' : '{address}',
            'phone_number' : '{phone_number}'
        """"}")
        engine.commit()
    except:
        print("Exception: ", e)
        engine.rollback()
    time.sleep(0.2)
    
