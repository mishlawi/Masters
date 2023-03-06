import textwrap
from prettytable import PrettyTable
from getpass import getpass

from LN.RASBet import RASBet

class RASBetUI:

    def __init__(self) -> None:
        self.rb = RASBet()
        self.rb.get_bets_all()
        self.rb.get_exchange_rate()

    def menu(self):
        return input(textwrap.dedent('''
                Welcome to RASBet!
                1 - List bets
                2 - Exchange rates
                3 - Register
                4 - Login
                0 - Leave
                '''))

    def run(self):
        op = int(self.menu())
        while op != 0:
            if op == 1:
                for bet in self.rb.get_bets():
                    print(str(object=bet))
            elif op == 2:
                exchanges = self.rb.get_exchanges()
                print("Exchange rates:")
                for item in exchanges:
                    print(item,' to')
                    for i in exchanges[item]:
                        print(f'    {i}: {exchanges[item][i]}')
            elif op == 3:
                mail = input("Enter your email: ")
                if self.rb.contains_user(mail):
                    print("Email já registado!")
                else:
                    name = input("Enter your name: ")
                    pw = getpass("Enter a password: ")
                    pw2 = getpass("Confirm your password: ")
                    if pw == pw2:
                        credit = float(input("Enter an amount to deposit: "))
                        moeda = self.selectCode()
                        self.rb.adiciona_registo(mail,name,pw,moeda,credit)
                        print("You are now registered!")
                    else:
                        print("The passwords do not match!")
            elif op == 4:
                count = 0
                mail = input("Enter your email: ")
                if self.rb.contains_user(mail):
                    pw = getpass("Enter your password: ")  
                    valido = self.rb.verifica_credenciais(mail,pw)
                    while not valido and count<2:
                        print("Wrong password, please try again")
                        count+=1
                        pw = getpass("Enter your password: ")  
                        valido = self.rb.verifica_credenciais(mail,pw)
                    if count==2:
                        print("You exceeded the number of tries!")
                    else:
                        self.rb.set_autenticado(mail)
                        self.runUser(self.rb.get_name(mail))
                else:
                    print("User does not exist")
            op = int(self.menu())

    def menuUser(self,name):
        return input(textwrap.dedent(f'''
                Welcome, {name}!
                1 - Make bet
                2 - Add credits         
                3 - Draw credits
                4 - List your bets
                5 - Exchange credits   
                0 - Logout
                '''))

    def selectCode(self):
        moeda = ''
        while not (moeda == 'EUR' or moeda == 'USD' or moeda == 'GBP' or moeda== 'ADA'):
            print("---------- COINS -----------")
            print("EUR - Euro (€)")
            print("USD - United States Dollar ($)")
            print("GBP - Pound Sterling (£)")
            print("ADA - Cardano ")
            moeda = input("Enter the code of the desired currency: \n")
        return moeda
   
    def selectDriver(self,dic):
        driver = ''
        while not (driver in dic.keys()):
            my_table = PrettyTable()
            my_table.field_names = ["DRIVER", "ODDS"]
            for (elem, odd) in dic.items():
                my_table.add_row([elem, str(odd)])
            print(my_table)
            driver = input("Please select the name of the driver to bet on: \n")
        return driver

    def get_id_aposta(self,dic):
        identification = 0
        ids =  [aposta.id for aposta in dic]
        while not (int(identification) in ids):
            print("+++++++++++++++++++++ BETs ++++++++++++++++++++++")
            my_table = PrettyTable()
            my_table.field_names = ["Bet id", "SPORT", "DETAILS"]
            for obj in dic:
                if obj.sport=='soccer' or obj.sport=='football':
                   my_table.add_row([str(obj.id), obj.sport, obj.home_team+'-'+obj.away_team])
                elif obj.sport=='f1':
                    drivers = obj.driver_odds.get_all(obj.id)
                    answ=''
                    for elem in drivers:
                        answ += elem + ' - '
                    my_table.add_row([str(obj.id), obj.sport, answ])
            print(my_table)
            identification = input("Please select the id of the bet of your interest: \n")
        return identification

    def runUser(self,name):
        op = int(self.menuUser(name))
        while op != 0:
            if op == 1:
                id_aposta = self.get_id_aposta(self.rb.get_bets())
                bet = self.rb.get_bet(id_aposta)
                if bet.sport == 'soccer' or bet.sport == 'football':
                    my_table = PrettyTable()
                    my_table.field_names = ["1", "X", "2"]
                    my_table.add_row([bet.odd_home, bet.odd_tie, bet.odd_away])
                    tipo=''
                    while not (tipo =='1' or tipo=='X' or tipo=='2'):
                        tipo = str(input("What's your bet ->  1 X 2 ?"))
                        if tipo =='1':
                            percentagem = bet.odd_home
                        elif tipo=='X':
                            percentagem = bet.odd_tie
                        elif tipo=='2':
                            percentagem = bet.odd_away
                elif bet.sport == 'f1':
                    tipo = self.selectDriver(bet.get_driver_odds())
                    percentagem = bet.get_driver_odds()[tipo]
                print("Your wallets - Which one do you choose to start betting?")
                dic = self.rb.get_wallets()
                for (key,value) in dic.items(): 
                    print(key, value)
                wallet = self.selectCode()
                credit = float(input("How much credits do you wish to spend?\n"))
                if self.rb.get_credits_user(wallet) is None:
                    print("You don't have this wallet")
                elif credit>self.rb.get_credits_user(wallet)[0] or credit<=0:
                    print("You don't have enough credits to do this action.")
                else:
                    if bet.sport=='soccer' or bet.sport=='football':
                        answer = input(f"Click 'y' to confirm your bet {bet.home_team}-{bet.away_team} with result {tipo}[y/n]")
                        if answer=='y':        
                            self.rb.subtrai_credits_user(credit,wallet)
                            self.rb.add_bet_user(tipo,credit,id_aposta)
                            print("Bet successfully registered!")
                    elif bet.sport=='f1':
                        answer = input(f"Click 'y' to confirm your bet on driver {tipo}[y/n]\n")
                        if answer=='y':        
                            self.rb.subtrai_credits_user(credit,wallet)
                            self.rb.add_bet_user(tipo,credit,id_aposta)
                            print("Bet successful registered!")
            elif op == 2:
                print('\033c')
                creditos = float(input("Enter the number of credits: "))
                if(creditos>=5):    
                    moeda = self.selectCode()
                    if self.rb.user_contains_code(moeda):
                        self.rb.update_credits(creditos,moeda)
                    else:
                        self.rb.add_credits(creditos,moeda)
                else:
                    print("The minimum number of credits to add is 5!")
            elif op == 3:
                print('\033c')
                valido = False
                iban = input("Enter your IBAN: ")
                n = float(input("Enter the number of credits: "))
                if(n>=5):
                    moeda = self.selectCode()
                    valido = self.rb.levantar_creditos(n, iban, moeda)
                    if not valido:
                        print("You don't enough credits in the chosen wallet")
                else:
                    print("The minimum number of credits to draw is 5!")
            elif op == 4:
                print('\033c')
                for bet in self.rb.get_bets_user():
                    print(str(object=bet))
            elif op == 5:
                print("Choose the currency from wich you want to exchange")
                moeda_from = self.selectCode()
                print("Choose the currency to wich you want to exchange")
                moeda_to = self.selectCode()
                credit = float(input("Enter the amount of credits to exchange: "))
                print(f"New amount of {moeda_to} credits: {self.rb.exchange_credits(moeda_from,moeda_to,credit)}")
            else:
                print("Choose an option from the available ones.")
            op = int(self.menuUser(name))
        if op == 0:
            self.rb.set_autenticado('') # terminar sessão
