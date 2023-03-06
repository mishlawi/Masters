class ApostaUser:
    def __init__(self,id,result,amount,aposta_id,user_mail) -> None:
        self.id = id
        self.result = result
        self.amount = amount
        self.aposta_id = aposta_id
        self.user_mail = user_mail
    
    def __str__(self) -> str:
        return "{id: " + str(self.id) + " | result: " + self.result + " | bet: " + str(self.aposta_id) + "]}"