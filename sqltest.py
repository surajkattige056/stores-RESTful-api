import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users(id int, username text, password text)"
cursor.execute(create_table)

user = (3, "jose", "asdf")
insert_query = "INSERT INTO users(id, username, password) VALUES (?, ?, ?)"
cursor.execute(insert_query, user)
connection.commit()

users = [
    (2, 'rolf', 'asdf'),
    (1, 'anne', 'xyz')
]

cursor.executemany(insert_query, users)
connection.commit()

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

