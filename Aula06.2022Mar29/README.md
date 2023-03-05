# Pergunta P.VIII.1.1

#### 1.

Primeiro, foi necessário obter o URL do serviço OCSP indicado no certificado, através do seguinte comando:

```
openssl x509 -noout -ocsp_uri -in CertExchangeMelâniaPereira.cer 
```
Cuja resposta foi: 
```
http://ocsp.cmd.cartaodecidadao.pt/publico/ocsp
```

Depois de saber o URL do serviço OCSP, o comando usado para ver o conteúdo do certificado foi o seguinte:

```
openssl ocsp -issuer CertExchangeAssinante.cer -cert CertExchangeMelâniaPereira.cer -url http://ocsp.cmd.cartaodecidadao.pt/publico/ocsp -text -noverify
```

Algumas das componentes do certificado que se puderam ver na resposta obtida do servidor OCSP foram:

- o ID do certificado, que inclui:
   - a identificação do algoritmo de hash usado;
   - a hash do nome do emissor;
   - a hash da chave do emissor;
   - o seu número de série.
- o estado do certificado, onde é possível ver se o certificado se encontra revogado, ou não, no nosso caso, o valor deste campo é "good";
- o algoritmo de assinatura do certificado;
- dados sobre o emissor do certificado, que permitem a validação do certificado;
- a validade do certificado;
- informações sobre a chave pública associada ao certificado;
- informações sobre a CRL, incluindo o URL da mesma.

---

Para a resolução das próximas duas perguntas, foi usada a biblioteca `cryptography` do _pyhton_ por ser uma biblioteca muito ampla que oferece muitas funcionalidades, nomeadamente relacionadas com o x509, disponibilizando bastantes funções para carregamento de certificados, exploração de listas de revogação e ainda para comunicação com o servidor OCSP.

#### 2.

Para utilizar o o programa desenvolvido para esta pergunta, é necessário passar como argumento o nome do ficheiro do certificado. <br>

Exemplo de utilização:
```
P.VIII.1.1.2.py <certificado.cer>
```

#### 3.

Para utilizar o o programa desenvolvido para esta pergunta, é necessário passar como argumento o nome do ficheiro do certificado a analisar e de seguida o nome do ficheiro do certificado da entidade emissora. <br>
Exemplo de utilização:
```
P.VIII.1.1.3.py <certificado.cer> <certificado_emissora.cer>
```