import mysql.connector

class DatabaseController:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create_server_record(self, server_id, name):
        sql = "INSERT INTO servers (server_id, name) VALUES (%s, %s)"
        val = (server_id, name)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("Server record created successfully.")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()