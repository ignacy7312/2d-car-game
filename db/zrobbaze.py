import sqlite3
from sqlite3 import Error

# ponizsze funckje odpalone tylko raz - zeby utworzyc db


db_file = 'db/baza2.db'

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

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, ud):
    sql = ''' INSERT INTO user(id, name, high_score, coins, games_played, time_spent, car0, car1, car2)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, ud)
    conn.commit()
    return cur.lastrowid

def create_car(conn, cd):
    sql = ''' INSERT INTO cars(id, name, price, path_to_graphics)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, cd)
    conn.commit()
    return cur.lastrowid

def create_mapowania(conn, md):
    sql = ''' INSERT INTO cur_user_car(user_id, car_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, md)
    conn.commit()
    return cur.lastrowid

def create_gamedata(conn, gd):
    sql = ''' INSERT INTO games(user_id, car_id, duration, coins_collected, score)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gd)
    conn.commit()
    return cur.lastrowid

def create_gamesettings(conn, gs):
    sql = ''' INSERT INTO settings(WIDTH, HEIGHT, FPS, sounds)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gs)
    conn.commit()
    return cur.lastrowid

def main(db_file):
    conn = create_connection(db_file)

    # ponizszy kod tworzy trzy tabele w bazie danych 
    # tabela mapowanie odwołuje się do dwóch poprzednich i służy do opierdalania aktualnego użytkownika
    
    sql_create_game_settings_table = """ CREATE TABLE IF NOT EXISTS settings (
                                        WIDTH integer PRIMARY KEY,
                                        HEIGHT integer,
                                        FPS integer,
                                        sounds integer
                                    ); """
    
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        high_score integer,
                                        coins integer CHECK (coins >= 0),
                                        games_played integer,
                                        time_spent integer,
                                        car0 integer CHECK (car0 == 1),
                                        car1 integer,
                                        car2 integer
                                    ); """

    sql_create_cars_table = """ CREATE TABLE IF NOT EXISTS cars (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        price integer,
                                        path_to_graphics text NOT NULL
                                    ); """
    
    sql_create_mapping_table = """CREATE TABLE IF NOT EXISTS cur_user_car (
                                    user_id integer,
                                    car_id integer,
                                    FOREIGN KEY (user_id) REFERENCES user (id),
                                    FOREIGN KEY (car_id) REFERENCES cars (id)
                                );"""

    
    sql_create_games_table = """CREATE TABLE IF NOT EXISTS games (
                                    user_id integer,
                                    car_id integer,
                                    duration integer CHECK (duration >= 0),
                                    coins_collected integer CHECK (coins_collected >= 0),
                                    score integer CHECK (score >= 0)
                                );"""


    sql = ''' INSERT INTO user(id, name, high_score, coins, games_played, time_spent,car0,car1,car2)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    sql2 = ''' INSERT INTO cars(id, name, price, path_to_graphics)
              VALUES(?,?,?,?) '''

    user_data = (0, "ja", 0, 0, 0, 0,1,0,0)
    
    car0_data = (0, "gtr", 0, 'textures/czerwonegora.png')
    car1_data = (1, "lambo", 100,'textures/lambogora.png')
    car2_data = (2, "supra", 500, 'textures/bialegora.png')
    
    gamedata = (0, 0, 10, 5, 2000)
    mapdata = (0, 0)
    
    setdata = (600, 800, 30, 1)

    sql3 = '''SELECT user.name 
            FROM user INNER JOIN cur_user_car ON user.id == cur_user_car.user_id
            '''
    sql4 = '''SELECT cars.name 
            FROM cars INNER JOIN cur_user_car ON cars.id == cur_user_car.car_id
            '''

    #gamedata_id = create_gamedata(conn, game_data)

    with conn:
        # egzekucja poleceń bazodanowych tworzących poszczególne tabele
        # create_table(conn, sql_create_user_table)
        # create_table(conn, sql_create_game_settings_table)
        # create_table(conn, sql_create_cars_table)
        # create_table(conn, sql_create_games_table)
        # create_table(conn, sql_create_mapping_table)
        # a = create_user(conn, user_data)
        # b = create_car(conn, car0_data)
        # c = create_car(conn, car1_data)
        # d = create_car(conn, car2_data)
        # z = create_mapowania(conn, mapdata)
        # e = create_gamedata(conn, gamedata)
        # f = create_gamesettings(conn, setdata)

        # tutaj tylko dla testu / pierwsze stworzenie:
        # e = create_mapowania(conn, mapdata)
        # mapowania powinny się tworzyć przy uruchomieniu programu
        
        # costam z tablicy:
        cur = conn.cursor()
        # cur.execute(sql3)
        # cur.execute(sql4)
        


if __name__ == "__main__":
    main(db_file)