import sqlite3


conn = sqlite3.connect('enterprise.db')
curs = conn.cursor()
curs.execute('''
 
    CREATE TABLE game (
        id integer,
        highscore integer,
        monety integer,
        cars integer,
        selected_car integer)
        
''')

int ='insert into game (id,highscore,monety,cars,selected_car) values (? ,?, ?, ?, ?)'
curs.execute(int,(1,0,0,0,0))

conn.commit()
conn.close()

class Sql():
    pass