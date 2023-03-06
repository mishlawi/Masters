import threading
import json
import requests
import pandas as pd

from Data.ApostaDAO import ApostaDAO
from Data.UserDAO import UserDAO


class RASBet:
    URL_bets = 'http://127.0.0.1:5000/info'
    URL_exchange = 'http://127.0.0.1:5000/exchange'

    def __init__(self):
        self.autenticado = ""
        self.exchanges = {}
        self.bets = ApostaDAO() # -- data object access
        self.users = UserDAO()

    ## -- buscar dados à api e guardar na bd -- ##
    def get_bets_all(self):
        # access BettingAPI - RESTApi
        data = json.loads(requests.get(self.URL_bets).text)
        normalized_dict = pd.json_normalize(data, record_path=['listEventsAll'])
        data = pd.DataFrame.from_dict(normalized_dict, orient='columns')
        for index in data.index:
            d = data.iloc[index]
            if d['event.sport'] == 'soccer' or d['event.sport'] == 'football':
                self.bets.addFootball(d['event.id'],d['event.sport'],d['event.team1'],d['event.team2'],d['event.result_odd.home'],d['event.result_odd.tie'],d['event.result_odd.away'])
            elif d['event.sport'] == 'f1':
                self.bets.addF1(d['event.id'],d['event.drivers'],d['event.odds'])
        t = threading.Timer(60,self.get_bets_all)
        t.daemon = True
        t.start()

    def get_exchange_rate(self):
        data = json.loads(requests.get(self.URL_exchange).text)
        for dic in data:
            self.exchanges.update(dic)
        t = threading.Timer(86400,self.get_exchange_rate)
        t.daemon = True
        t.start()

    ## -- mail do user autenticado -- ##
    def set_autenticado(self,mail):
        self.autenticado = mail

    ## -- buscar apostas disponíveis -- ##
    def get_bets(self):
        return self.bets.get_all()

    def get_exchanges(self):
        return self.exchanges

    def get_bet(self,idAposta):
        return self.bets.get_bet(idAposta)
    
    ## -- adicionar novo user -- ##
    def adiciona_registo(self,mail,name,pw,moeda,credit): 
        self.users.add(mail,name,pw)
        user = self.users.get_user(mail)
        user.add_creditos(moeda,credit)
    
    ## -- get do nome de determinado user -- ##
    def verifica_credenciais(self,mail,pw):
        if pw == self.users.get_password(mail=mail)[0]:
            return True
        else:
            return False

    ## -- get do nome de determinado user -- ##
    def get_name(self,mail):
        return self.users.get_name(mail)[0]
    
    ## -- check se já existe um user com determinado mail na bd -- ##
    def contains_user(self,mail):
        return self.users.contains(mail);

    def executa_transferencia(self, n, iban):
        # send the money to the iban account
        print(f"You will get the {n} in your account in 5 week days.")
            
    def levantar_creditos(self, n, iban, moeda):
        user = self.users.get_user(self.autenticado)
        if user.get_creditos(moeda) is None or user.get_creditos(moeda)[0] - n < 0:
            return False
        else:
            user.subtrai_creditos(n, moeda)
            self.executa_transferencia(n, iban)
            return True

    def update_credits(self,creditos,moeda):
        user = self.users.get_user(self.autenticado)
        user.update_creditos(creditos,moeda)

    def get_bets_user(self):
        user = self.users.get_user(self.autenticado)
        return user.get_all_bets()

    def exchange_credits(self,moeda_old,moeda_new,credit_old):
        user = self.users.get_user(self.autenticado)
        credit_new = self.exchanges[moeda_old][moeda_new] * credit_old
        user.exchange_credits(credit_new, moeda_new, credit_old, moeda_old)
        return user.get_creditos(moeda_new)

    def get_wallets(self):
        user = self.users.get_user(self.autenticado)
        return user.get_all()

    def get_credits_user(self,wallet):
        user = self.users.get_user(self.autenticado)
        return user.get_creditos(wallet)

    def subtrai_credits_user(self,credit,moeda):
        user = self.users.get_user(self.autenticado)
        user.subtrai_creditos(credit,moeda)

    def add_bet_user(self,tipo,credit,id_aposta):
        user = self.users.get_user(self.autenticado)
        user.add_bet(tipo,credit,id_aposta)

    def user_contains_code(self,moeda):
        user = self.users.get_user(self.autenticado)
        return user.contains_code(moeda)
    
    def update_credits(self,creditos,moeda):
        user = self.users.get_user(self.autenticado)
        user.update_creditos(creditos,moeda)

    def add_credits(self,creditos,moeda):
        user = self.users.get_user(self.autenticado)
        user.add_creditos(moeda,creditos)
        
