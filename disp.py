
import sqlite3 as sq

con = sq.connect("fruits.db")
print("Fruit Databases Opened")

print(con.execute("select * from fruit"))

print("Fruit Table Created")
con.close()