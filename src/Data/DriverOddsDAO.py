import mysql.connector

class DriverOddsDAO:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="root", 
            database="rasdb")
        self.mycursor = self.mydb.cursor()

    def get_all(self,id_aposta):
        driver_odds = {}
        self.mycursor.execute(f"SELECT * FROM DriverOdds WHERE Aposta_id = {id_aposta}")
        for (driver,odd,_) in self.mycursor.fetchall():
            driver_odds.update({driver:odd})
        return driver_odds