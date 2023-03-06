
from Data.ApostaUserDAO import ApostaUserDAO
from Data.CreditosUserDAO import CreditosUserDAO

class User:
    def __init__(self,mail,name,pw):
        self.mail = mail
        self.name = name
        self.pw = pw
        self.credit = CreditosUserDAO()
        self.bets = ApostaUserDAO()
    
    def get_all(self):
        return self.credit.get_all(self.mail)

    def get_all_bets(self):
        return self.bets.get_all(self.mail)

    def update_creditos(self,credit,moeda):
        self.credit.update_creditos(self.mail,credit,moeda)

    def add_creditos(self,moeda,credit):
        self.credit.add_creditos(self.mail,credit,moeda)

    def get_creditos(self, moeda):
        return self.credit.get_creditos(self.mail, moeda)

    def subtrai_creditos(self, credit, moeda):
        self.credit.subtrai_creditos(self.mail, credit, moeda)

    def add_bet(self,result,amount,aposta_id):
        self.bets.add(result,amount,aposta_id,self.mail)

    def exchange_credits(self,credit_new,moeda_new,credit_old,moeda_old):
        if self.credit.contains(moeda_new):
            self.credit.update_creditos(self.mail,credit_new,moeda_new)
        else:
            self.credit.add_creditos(self.mail,credit_new,moeda_new)
        self.credit.subtrai_creditos(self.mail,credit_old,moeda_old)
        
    def contains_code(self,moeda):
        return self.credit.contains(moeda)
        

    