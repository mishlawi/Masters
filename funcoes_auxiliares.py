import pandas as pd

'''
FUNCAO DE LIMPEZA DE VALORES
'''
def limpa_valores(training,test):
    # AVERAGE_CLOUDINESS
    training.loc[training.AVERAGE_CLOUDINESS == 'céu claro', 'AVERAGE_CLOUDINESS'] = 'céu limpo'
    training.loc[training.AVERAGE_CLOUDINESS == 'algumas nuvens', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
    training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'nuvens quebradas'
    training.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
    training.loc[training.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

    test.loc[test.AVERAGE_CLOUDINESS == 'céu claro', 'AVERAGE_CLOUDINESS'] = 'céu limpo'
    test.loc[test.AVERAGE_CLOUDINESS == 'algumas nuvens', 'AVERAGE_CLOUDINESS'] = 'céu pouco nublado'
    test.loc[test.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'nuvens quebradas'
    test.loc[test.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
    test.loc[test.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

    # AVERAGE_RAIN
    training.loc[training.AVERAGE_RAIN == 'chuvisco fraco', 'AVERAGE_RAIN'] = 'chuva fraca' 
    training.loc[training.AVERAGE_RAIN == 'chuvisco e chuva fraca', 'AVERAGE_RAIN'] = 'chuva fraca' 
    training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesada', 'AVERAGE_RAIN'] = 'chuva forte' 
    training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva forte' 

    test.loc[test.AVERAGE_RAIN == 'chuvisco fraco', 'AVERAGE_RAIN'] = 'chuva fraca' 
    test.loc[test.AVERAGE_RAIN == 'chuvisco e chuva fraca', 'AVERAGE_RAIN'] = 'chuva fraca' 
    test.loc[test.AVERAGE_RAIN == 'chuva de intensidade pesada', 'AVERAGE_RAIN'] = 'chuva forte' 
    test.loc[test.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva forte' 
    


'''
FUNCOES DE TRANSFORMACAO EM VALORES NUMERICOS
'''
   
    
# AVERAGE_CLOUDINESS
def weatherType(tempo):
    if( tempo == 'céu limpo' ):
        return 0
    elif( tempo == 'céu pouco nublado' ):
        return 1
    elif( tempo == 'céu nublado' ):
        return 2

# AVERAGE_RAIN
def rainType(chuva):
    if( chuva == 'sem chuva'):
        return 0
    elif( chuva == 'aguaceiros fracos' ):
        return 1
    elif( chuva == 'aguaceiros' ):
        return 2
    elif( chuva == 'chuva fraca' ):
        return 3
    elif( chuva == 'chuva moderada' ):
        return 4
    elif( chuva == 'trovoada com chuva leve' ):
        return 5
    elif( chuva == 'chuva forte' ):
        return 6
    elif( chuva == 'trovoada com chuva' ):        
        return 7

def roundInt(num):
    return int(round(num,0))

'''
FUNCAO DE TRANSFORM DAS PREDICTIONS PARA CSV
'''
def predictions_to_csv(pred,filename):
    predictions = pd.DataFrame(pred, columns=['Speed_Diff'])
    predictions.index.name='RowId'
    predictions.index += 1 
    predictions.to_csv("./"+filename+".csv")