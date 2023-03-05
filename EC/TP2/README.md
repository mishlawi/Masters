# Trabalho Prático 2

Este trabalho é dedicado às candidaturas finalistas ao concurso NIST Post-Quantum Cryptography na categoria de criptosistemas PKE-KEM. 

De momento estão selecionadas 4 candidaturas finalistas (Classical McEliece, NTRU, KYBER e SABER) mas também estão selecionadas 5 outras candidaturas com oportunidade de virem a ser selecionadas. Deste último grupo destacamos BIKE por ser um criptosistemas que, tal como o Classical McEliece, é baseado em problemas de códigos mas é muito mais simples de implementar.


    - O objetivo deste trabalho é a criação de 3 protótipos em Sagemath de três  técnicas representativas cada uma delas das principais famílias de criptosistemas pós-quânticos: BIKE (“code based”), NTRU (“lattice based”) e KYBER (“LWE based”). 
    - Para cada uma destas técnicas pretende-se implementar um KEM, que seja IND-CPA seguro, e um PKE que seja IND-CCA seguro.
    - A descrição, outra documentação e implementações em C/C++ das candidaturas aqui referidas pode ser obtida na página do concurso NIST  ou na diretoria Dropbox da disciplina: Docs/NIST-PQC-ROUND3-PKE 
