import sqlite3
from sqlite3 import Error

# ponizsze funckje odpalone tylko raz - zeby utworzyc db
"""
def create_gamedata(conn, game_data):
    sql = ''' INSERT INTO GAME_DATA(high_score, coins, car0_unlocked, car1_unlocked, car2_unlocked, games_played, total_time_ig)
            VALUES(?,?,?, ?,?,?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, game_data)
    conn.commit()
    return cur.lastrowid

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def run_once():
    db = 'baza2.db'
    sql_create_gamedata_table = ''' CREATE TABLE IF NOT EXISTS GAME_DATA (
                                        high_score integer,
                                        coins integer,
                                        car0_unlocked integer,
                                        car1_unlocked integer,
                                        car2_unlocked integer,
                                        games_played integer,
                                        total_time_ig integer
                                    ); '''

    
    conn = create_connection(db)

    with conn:
        create_table(conn, sql_create_gamedata_table)
        
        game_data = (0, 0, 1, 0, 0, 0, 0)
        gamedata_id = create_gamedata(conn, game_data)


"""

class DatabaseFunctionalities():
    db_file = 'baza2.db'

    def create_connection(db_file):
        '''create a database connection to a SQLite database'''
        # obiekt połączenia - póki co None
        conn = None
        try:
            # fcja connect zwraca obiekt Connection
            # na którym można wykonać operacje
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        
        return conn


    def get_coins(cur):
        return cur.execute("SELECT coins FROM game_data").fetchone()[0]

    def update_coins(conn, coins):
        cur = conn.cursor()
        current_coins = get_coins(cur)

        sql = ''' UPDATE GAME_DATA
                SET coins = ?'''
        
        cur.execute(sql, (current_coins + coins, ))
        conn.commit()


    def get_highscore(cur):
        # dostaje kursor i zwraca high score
        return cur.execute("SELECT high_score FROM game_data").fetchone()[0]

    def update_highscore(conn, score):
        
        cur = conn.cursor()
        current_hs = DatabaseFunctionalities.get_highscore(cur)
        print(current_hs)
        if score > current_hs:
            sql = ''' UPDATE GAME_DATA
                    SET high_score = ?'''
            cur.execute(sql, (score, ))
            conn.commit()

    def update_games_played(conn):
        cur = conn.cursor()
        games_played = cur.execute("SELECT games_played FROM game_data").fetchone()[0]
        sql = ''' UPDATE GAME_DATA
                SET games_played = ?'''
        cur.execute(sql, (games_played + 1, ))
        conn.commit()

    def update_total_time_ig(conn, time):
        '''dostaje czas w ms, przelicza na sekundy i dodaje do calkowitego
        no i wpisuje to do bazy'''
        cur = conn.cursor()
        ttig = cur.execute("SELECT total_time_ig FROM game_data").fetchone()[0]
        time_updated = ttig + round(time, -3)/1000
        sql = ''' UPDATE GAME_DATA
                SET total_time_ig = ?'''
        cur.execute(sql, (time_updated, ))
        conn.commit()

    def unlock_car(conn, car_id):
        '''dostaje id auta do odblokowania 1 lub 2
        sprawdza czy auto nie jest juz odblokowane
        no i wpisuje to do bazy. odblokowane auto oznaczone jest jako 1'''
        cur = conn.cursor()
        is_unlocked = cur.execute(f"SELECT car{car_id}_unlocked FROM game_data").fetchone()[0]
        if not is_unlocked:
            sql = f''' UPDATE GAME_DATA
                    SET car{car_id}_unlocked = ?'''
            cur.execute(sql, (1, ))
            conn.commit()

    def main():
        database = 'baza2.db'


        # create a database connection
        conn = test2.create_connection(database)
        with conn:
            update_coins(conn, 5)
            update_highscore(conn, 2000)
            update_games_played(conn)
            update_total_time_ig(conn, 4769)
            unlock_car(conn, 1)


if __name__ == '__main__':
    DatabaseFunctionalities.update_highscore(DatabaseFunctionalities.create_connection(DatabaseFunctionalities.db_file), 200)

