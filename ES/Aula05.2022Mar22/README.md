# P.VII.1.1

Sendo o grupo 8, usamos curvas elíticas para gerar o par de chaves no programa. Para a cifragem da chave de sessão foi usada a troca de chaves de curvas elítivcas Diffie-Helman. Para isso usamos a classe _ec_ e _ECDH_ do _packege_ **cryptography** do _python_ que permite a geração de uma chave partilhada pela troca de chave privada <-> chave pública. Para poder efetuar esta troca, é necessário inserir na função de cifra, para além da chave pública do destinatário, também a chave privada do remetente e a sua password. Assim como, na função de decifra, é necessário inserir a chave pública do remetente da mensagem, para além da chave privada de quem está a decifrar (o destinatário da mensagem). <br>
Para o resto das operações foi usado o _package_ **Crypto**, de acordo com aquilo que tinha sido implementado no trabalho anterior. <br>
Foi criada uma função de derivação de chave **pkfile_pw(password)** para dar entropia à password usada para guardar o ficheiro da chave privada. <br>
Há a opção de invocar a função de cifra com ou sem os dados para guardar as chaves geradas. No caso de não serem inseridos, as chaves são geradas e usadas, mas não guardadas.

Uso do programa na linha de comando, substituindo os campos entre <> pelos seus valores:
- Para cifrar:
   + Caso não queira guardar as chaves em ficheiros:
      > digital_envelope.py encrypt <public_key_file> <input.txt> <output.txt>
   + Caso pretenda guardar as chaves em ficheiros:
      > digital_envelope.py encrypt <public_key_file> <input.txt> <output.txt> <public_key_file> <private_key_file> <password_to_private_file> 
- Para decifrar:
   > digital_envelope.py decrypt <private_key_file> <password_to_private_file> <public_key_file> session_key.txt <input.txt> <output.txt>

Comandos linha de exemplo utilizando o programa desenvolvido e o ficheiro de teste 'exemplo.txt:

```python3 digital_envelope.py generate_keys bob_public bob_private 1234567```

```python3 digital_envelope.py encrypt bob_public.pem exemplo1.txt exemplo1encrypt.txt alice_public alice_private aliceisawesome```

```python3 digital_envelope.py decrypt bob_private.pem 1234567 alice_public.pem session_key.txt exemplo1encrypt.txt exemplo1decrypt.txt```


# P.VII.1.2

O processo de assinatura e verificação da mesma pode ser feito diversas vezes, com diferentes ficheiros, numa mesma execução do programa. Tal não se verifica se se interromper a execução do mesmo visto que o conjunto de chaves não será o mesmo. <br>
Há a capacitância de gerar assinaturas de vários ficheiros de forma sequencial, sendo que os dados relativos a assinaturas e respetivos ficheiros são guardados no ficheiro `signature.txt`. É, portanto, especialmente necessário que se eliminem estes dados sempre que a aplicação é fechada, devido à sua pouca utilidade após a execução do programa.

Comandos linha de exemplo utilizando o programa desenvolvido:

- Para usar este programa é necessário inserir um número relativo à operação a efetuar (assinatura (1) ou verificação (2)). De seguida, é necessário introduzir o nome do ficheiro sobre o qual se pretende efetuar a operação escolhida.

Exemplo:

```
Choose one operation
1 - Sign a file
2 - Verify a file signature
0 - Leave
1
File name: 
Tutorial__Docker.pdf
File signed successfully!


Choose one operation
1 - Sign a file
2 - Verify a file signature
0 - Leave
2
File name: 
Tutorial__Docker.pdf
The signature is valid!


Choose one operation
1 - Sign a file
2 - Verify a file signature
0 - Leave
0
```