import sqlite3


class Save:

    data = 0

    def savescore(self, score):
        self.score = score
        self.db = sqlite3.connect("enterprise.db")
        self.cursor = self.db.cursor()

        self.int ='insert into game (highscore) values (?)'
        self.cursor.execute(self.int,(self.score,))

        self.db.commit()
        self.db.close()

    def savecoins(self, coins):
        self.coins = coins

        self.db = sqlite3.connect("enterprise.db")
        self.cursor = self.db.cursor()

        self.int = 'insert into game (monety) values (?)'
        self.cursor.execute(self.int, (self.coins,))

        self.db.commit()
        self.db.close()

    def readdata(self):
        self.db = sqlite3.connect("enterprise.db")
        self.cursor = self.db.cursor()
        self.res = self.cursor.execute("SELECT * FROM game")
        data = self.res.fetchone()
        self.db.commit()
        self.db.close()

        return data

    def deleterow(self):
        self.db = sqlite3.connect("enterprise.db")
        self.cursor = self.db.cursor()
        self.res = self.cursor.execute("DELETE FROM game WHERE id=1")
        self.db.commit()
        self.db.close()


    def newtable(self):
        self.conn = sqlite3.connect('enterprise.db')
        self.curs = self.conn.cursor()
        self.curs.execute('''

            CREATE TABLE game (
                highscore integer,
                monety integer,
                cars integer,
                selected_car integer)

        ''')

        self.conn.commit()
        self.conn.close()





