import mysql.connector

from LN.Bet import FootballBet, F1Bet

class ApostaDAO:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="root", 
            database="rasdb")
        self.mycursor = self.mydb.cursor()

    ## -- add apostas de diferentes tipos -- ##
    def addFootball(self,id_aposta,sport,home_team,away_team,odd_home,odd_tie,odd_away):
        val = (id_aposta,sport,home_team,away_team,odd_home,odd_tie,odd_away)
        self.mycursor.execute(f"INSERT INTO Aposta (id,sport,home_team,away_team,odd_home,odd_tie,odd_away) VALUES {val} \
                                ON DUPLICATE KEY UPDATE home_team='{home_team}', away_team='{away_team}', odd_home={odd_home}, odd_tie={odd_tie}, odd_away={odd_away}")
        self.mydb.commit()

    def addF1(self,id_aposta,drivers,odds):
        self.mycursor.execute(f"INSERT INTO Aposta (id,sport) VALUES {(id_aposta,'f1')} \
                                ON DUPLICATE KEY UPDATE id={id_aposta}")
        for driver, odd in zip(drivers,odds):
            self.mycursor.execute(f"INSERT INTO DriverOdds (driver, odd, Aposta_id) VALUES {(driver,odd,id_aposta)} \
                                    ON DUPLICATE KEY UPDATE driver='{driver}', odd={odd}, Aposta_id={id_aposta}")
            self.mydb.commit()

     ## -- delete todas as apostas na bd (feito sempre que há acesso à API para update) -- ##
    def delete_all(self):
        self.mycursor.execute("SET SQL_SAFE_UPDATES = 0")
        self.mycursor.execute("DELETE FROM DriverOdds")
        self.mycursor.execute("DELETE FROM Aposta")
        self.mycursor.execute("SET SQL_SAFE_UPDATES = 1")

     ## -- get de todas as apostas disponíveis na bd -- ##
    def get_all(self):
        bets = []
        self.mycursor.execute("SELECT * FROM Aposta")
        for (id_aposta,sport,home_team,away_team,home_odd,tie_odd,away_odd) in self.mycursor.fetchall():
            if sport == 'soccer' or sport == 'football':
                bet = FootballBet(id_aposta,sport,home_team,away_team,home_odd,tie_odd,away_odd)
                bets.append(bet)
            elif sport == 'f1':
                bet = F1Bet(id_aposta,sport)
                bets.append(bet)
        return bets

    def get_bet(self, id):
        self.mycursor.execute(f'SELECT * FROM Aposta where id={id}')
        (id_aposta, sport, home_team, away_team, home_odd,
         tie_odd, away_odd) = self.mycursor.fetchone()
        if sport == 'soccer' or sport == 'football':
            bet = FootballBet(id_aposta, sport, home_team,
                              away_team, home_odd, tie_odd, away_odd)
        elif sport == 'f1':
            bet = F1Bet(id_aposta, sport) 
        return bet
        