import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_database_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    return connection


if __name__ == "__main__":
    try:
        connection = get_database_connection()

        if connection.is_connected():
            print("Successfully connected to MySQL!")

            cursor = connection.cursor()

            cursor.execute("""
                SELECT plant_id, plant_name, scientific_name
                FROM plants
            """)

            plants = cursor.fetchall()

            print("\nPlants in database:")

            for plant in plants:
                print(
                    plant[0],
                    "-",
                    plant[1],
                    "-",
                    plant[2]
                )

            cursor.close()
            connection.close()

    except mysql.connector.Error as error:
        print("Database connection failed:")
        print(error)