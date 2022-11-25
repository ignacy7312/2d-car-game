import sqlite3


conn = sqlite3.connect('enterprise.db')
curs = conn.cursor()
curs.execute('''

    CREATE TABLE game (
        highscore integer,
        monety integer,
        cars integer,
        selected_car integer)
        
''')

conn.commit()
conn.close()

class Sql():
    pass