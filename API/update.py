import sqlite3
import time
import csv
import os

os.chdir("/media/sf_knighthorse4/API")

conn = sqlite3.connect("./var/hs.db")
cursor = conn.cursor()

file = open('HS.csv')
csvreader = csv.reader(file)

rows = []
for row in csvreader:
        rows.append(row)
rows

cursor.execute("UPDATE hs SET High_score = ?", rows[1])
conn.commit()
file.close()
conn.close()
