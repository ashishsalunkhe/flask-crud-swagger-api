import sqlite3 as sq

con = sq.connect("fruits.db")
print("Fruit Databases Opened")

con.execute("create table fruit (id INTEGER PRIMARY KEY AUTOINCREMENT, fruit_name TEXT NOT NULL, quantity INTEGER, price INTEGER NOT NULL)")
print(con.execute("select * from fruit"))
print("Fruit Table Created")
con.close()