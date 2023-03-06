

## To have in mind:

#### **Aplicação mID (portador)**

+ na **primeira** utilização:
  + conecta-se com a infra-estrutura de uma entidade emissora de documentos (usando comunicação TCP/IP) para o download de todos os dados associados a este documento
  + o cidadão autentica-se ao serviço para iniciar a transferência
+ o download dos dados **repete-se** periodicamente para atualizações
+ nas **repetições** não há necessidade de autenticação explícita
+ em **ambas** as situações:
  + garantir confidencialidade e integridade dos dados transferidos **para** o dispositivo
  + garantir mecanismos robustos de autenticação
+ dados transferidos em formato JSON (por TCP/IP)
+ garantir a autenticidade e integridade dos dados armazenados no dispositivo

+ operações de prova de identidade (entre portador e leitor) podem acontecer de dois modos:
  + offline - portador transfere os atributos de identificação para o leitor e os dados necessários à sua verificação
  + online - leitor transfere um token de autorização para o verificador consultar a entidade emissora diretamente (garante dados mais recentes sobre o cidadão)
+ em **ambos** os modos:
  + comunicação estabelecida sempre primeiro pelo portador através de um qrcode que contém toda a informação para que o leitor o encontra e inicia a conexão
  + a conexão pode usar uma das seguintes tecnologias
    + BLE - Bluetooth Low Energy
    + NFC - Near Field Communication
    + WiFi-Aware

+ depois de estabelecido um canal entre os dispositivos:
  + verificador envia pedido que contem identificadores dos atributos desejados
  + portador tem duas opções:
    + aceitar a transferência na totalidade
    + aceitar apenas a transferência de um subconjunto dos atributos
  + comunicação é suportada por mensagens codificadas no formato CBOR (Concise Binary Object Representation)
  
+ garantir ocnfidencialidade e integridade dos dados transmitidos entre portador e leitor
+ permitir auditar (analisar e validar atividade, informação ou processos) as interações ocorridas com leitores - por exemplo, indicando os dados transmitidos para um leitor em particular e quando ocorreu



#### **Aplicação leitora (verificador)**

+ o verificador estabelece comunicação com o portador e solicita atributos suficientes para o identificar
+ suporta todos os protocolos indicados para a aplicação mID
+ decide se a operação é feita em modo offline ou online
+ fornece os dados necessários para permitir a auditoria das operações pelo portador
+ a aplicação ou o utilizador devem ser autenticados
+ no **modo online**, garantir que a aplicação leitora não é capaz de alterar a lista de atributos pelo portador antes da consulta à entidade emissora
  


#### **Entidade emissora (backend do sistema)**


+ entidade com poder de emitir e conferir autenticidade a um documento de identificação pessoal
+ responsável por prover os mecanismos que garantem a autenticidade e integridade dos documentos digitais transmitidos (tanto no modo online, quanto no modo offline)
+ +comunica-se com a aplicação mID por TCP/IP (rede pública)
