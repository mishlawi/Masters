
Trabalho Prático 1


1. Use o “package” Cryptography para
    1. Implementar uma AEAD com “Tweakable Block Ciphers” conforme está descrito na última secção do texto +Capítulo 1: Primitivas Criptográficas Básicas.  A cifra por blocos primitiva, usada para gerar a “tweakable block cipher”, é o AES-256 ou o ChaCha20.
    2. Use esta construção para construir um canal privado de informação assíncrona com acordo de chaves feito com “X448 key exchange” e “Ed448 Signing&Verification” para autenticação  dos agentes. Deve incluir uma fase de confirmação da chave acordada.


2. Use o SageMath para, 
    1. Construir uma classe Python que implemente um KEM- RSA. A classe deve
        1. Inicializar cada instância recebendo  o parâmetro de segurança (tamanho em bits do módulo RSA) e gere as chaves pública e privada.
        2. Conter funções para encapsulamento e revelação da chave gerada.
    2. Construir,  a partir deste KEM e usando a transformação de Fujisaki-Okamoto, um PKE que seja IND-CCA seguro.
    
3. Use o Sagemath para
    1. Construir uma classe Python que implemente o  EdCDSA a partir do “standard” FIPS186-5
        1. A implementação deve conter funções para assinar digitalmente e verificar a assinatura.
        2. A implementação da classe deve usar  uma das “Twisted Edwards Curves” definidas no standard e escolhida  na iniciação da classe: a curva  “edwards25519” ou “edwards448”.
