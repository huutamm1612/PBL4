import mysql.connector

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "PBL4"
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print("Kết nối cơ sở dữ liệu thành công")
        except mysql.connector.Error as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        return result

    def check_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone() is not None

    def signup(self, username, password):
        if self.check_username(username):
            return False
        else:
            try:
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                self.cursor.execute(query, (username, password))
                self.conn.commit()
                return True
            except mysql.connector.Error as e:
                return False

    def update_password(self, username, password):
        query = "update users set password = %s where username = %s"
        self.cursor.execute(query, (password, username))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("Password updated successfully.")
            return True
        else:
            print("No user found with the provided username.")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")