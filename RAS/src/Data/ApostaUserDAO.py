import mysql.connector

from LN.ApostaUser import ApostaUser

class ApostaUserDAO:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="root", 
            database="rasdb")
        self.mycursor = self.mydb.cursor()

     ## -- add aposta realizada a um user -- ##
    def add(self,result,amount,aposta_id,user_mail):
        val = (result,amount,aposta_id,user_mail)
        self.mycursor.execute(f"INSERT INTO ApostaUser (result,amount,Aposta_id,User_mail) VALUES {val}")
        self.mydb.commit()
    
     ## -- get das apostas realizadas de um user -- ##
    def get_all(self,mail):
        betsUser = []
        self.mycursor.execute(f"SELECT * FROM ApostaUser WHERE User_mail = '{mail}'")
        for (id,result,amount,aposta_id,user_mail) in self.mycursor.fetchall():
            betUser = ApostaUser(id,result,amount,aposta_id,user_mail)
            betsUser.append(betUser)
        return betsUser
