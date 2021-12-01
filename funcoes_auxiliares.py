import pandas as pd

'''
FUNCAO DE LIMPEZA DE VALORES
'''
def limpa_valores(training,test):
    # AVERAGE_CLOUDINESS
    training.loc[training.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'nuvens quebradas'
    training.loc[training.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
    training.loc[training.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'

    test.loc[test.AVERAGE_CLOUDINESS == 'nuvens quebrados', 'AVERAGE_CLOUDINESS'] = 'nuvens quebradas'
    test.loc[test.AVERAGE_CLOUDINESS == 'tempo nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'
    test.loc[test.AVERAGE_CLOUDINESS == 'nublado', 'AVERAGE_CLOUDINESS'] = 'céu nublado'


    
    training.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva de intensidade pesada' 
    
    test.loc[training.AVERAGE_RAIN == 'chuva de intensidade pesado', 'AVERAGE_RAIN'] = 'chuva de intensidade pesada'
    


'''
FUNCOES DE TRANSFORMACAO EM VALORES NUMERICOS
'''
# AVERAGE_SPEED_DIFF

def speedType(vel):
    if( vel == 'None'):
        return 0
    elif( vel == 'Low' ):
        return 1/4
    elif( vel == 'Medium'):
        return 2/4
    elif( vel == 'High' ):
        return 3/4
    elif( vel == 'Very_High'):
        return 4/4

    
# LUMINOSITY
def luminosityType(lux):
    if( lux == 'DARK' ):
        return 0
    elif( lux == 'LOW_LIGHT' ):
        return 1/2
    elif( lux == 'LIGHT' ):
        return 2/2
    
# AVERAGE_CLOUDINESS
def weatherType(tempo):
    if( tempo == 'céu limpo' ):
        return 0
    elif( tempo == 'céu pouco nublado' ):
        return 1/2
    elif( tempo == 'céu nublado' ):
        return 2/2

# AVERAGE_RAIN
def rainType(chuva):
    if( chuva == 'sem chuva'):
        return 0.0
    elif( chuva == 'aguaceiros fracos' ):
        return 1/7
    elif( chuva == 'aguaceiros' ):
        return 2/7
    elif( chuva == 'chuva fraca' ):
        return 3/7
    elif( chuva == 'chuva moderada' ):
        return 4/7
    elif( chuva == 'trovoada com chuva leve' ):
        return 5/7
    elif( chuva == 'chuva forte' ):
        return 6/7
    elif( chuva == 'trovoada com chuva' ):        
        return 7/7


'''
FUNCAO DE TRANSFORM DAS PREDICTIONS PARA CSV
'''
def predictions_to_csv(pred,filename):
    predictions = pd.DataFrame(pred, columns=['Speed_Diff'])
    predictions.index.name='RowId'
    predictions.index += 1 
    predictions.to_csv("./"+filename+".csv")