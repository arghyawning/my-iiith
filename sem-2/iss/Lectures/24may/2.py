import sqlite3

#creates file-based database
stack_connection = sqlite3.connect("record.db")

stack_cursor=stack_connection.cursor()
stack_cursor.execute("CREATE TABLE DEMO")