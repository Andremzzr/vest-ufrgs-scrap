from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()


class DatabaseService: 

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.connection.cursor()
        self.start()

    def close_connection(self):
        self.cursor.close()

    def start(self): 
        query = """ 
            CREATE TABLE IF NOT EXISTS public.candidates (
            id bigserial NOT NULL,
            course_name varchar(255) NULL,
            exam_type varchar(4) NOT NULL,
            "year" int4 NULL,
            classification int4 NULL,
            score numeric(6, 2) NULL,
            concurrence_type varchar(50) NULL,
            "period" varchar(10) NULL,
            enter_type varchar(50) NULL,
            status varchar(50) NULL,
            "date" date NULL,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
            updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
            CONSTRAINT candidates_pkey PRIMARY KEY (id),
            CONSTRAINT candidate_course_year UNIQUE (classification, year, course_name)
        );
        """
        try: 
            self.cursor.execute(query)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"An error occurred while creating table: {e}")
            self.connection.rollback()
            

    def insert_batch(self, candidates_batch):
        query = """
            INSERT INTO candidates
            (course_name, year, classification, score, concurrence_type, period, enter_type, status, date, exam_type)
            VALUES (%(course_name)s, %(year)s, %(classification)s, %(score)s, 
                    %(concurrence_type)s, %(period)s, %(enter_type)s, %(status)s, %(date)s, %(exam_type)s)
        """
        try:
            self.cursor.executemany(query, candidates_batch)
            self.connection.commit()
            print(f"{len(candidates_batch)} candidates inserted successfully.")
        except psycopg2.Error as e:
            print(f"An error occurred during batch insert: {e}")
            self.connection.rollback()



            

