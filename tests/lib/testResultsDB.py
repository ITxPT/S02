import os
import mysql.connector
from dotenv import load_dotenv



class TestResultDB:
    conn = None
    
    def createConnection(self):
        load_dotenv()
        DB_HOST = os.getenv("DB_HOST")
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_DATABASE = os.getenv("DB_DATABASE")

        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            ssl_verify_identity=True,
            ssl_ca="/etc/ssl/certs/ca-certificates.crt"
        )
    
    def create_table(self, table_name):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    datetime DATETIME,
                    testname VARCHAR(255),
                    testversion VARCHAR(255),
                    sutname VARCHAR(255),
                    sutversion VARCHAR(255),
                    verdict VARCHAR(255)
                )
            """)
        self.conn.commit()

    def insert_test_result(self, table_name, datetime, testname, testversion, sutname, sutversion, verdict):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {table_name} (datetime, testname, testversion, sutname, sutversion, verdict)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (datetime, testname, testversion, sutname, sutversion, verdict))
        self.conn.commit()
    
    def close(self):
        self.conn.close()