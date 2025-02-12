import psycopg2

class DatabaseService: 

    def __init__(self):
        self.connection = psycopg2.connect(database="database", user="user", password="pass", host="localhost", port=5432);
        self.cursor = self.connection.cursor()

    def insert_candidates(self, values):
        query = """
           INSERT INTO candidates
           (classification, score, concurrence_type, period, enter_type, status, date)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Candidates inserted successfully.")
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
        finally:
            self.cursor.close()
            self.connection.close()

