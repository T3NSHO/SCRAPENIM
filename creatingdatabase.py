import sqlite3

con = sqlite3.connect("sessions.db")
cur = con.cursor()
res = cur.execute("CREATE TABLE sessions (username TEXT ,cookie TEXT)")
