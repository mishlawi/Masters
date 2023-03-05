# Pergunta P1.1

### 1

O RPGD deve ser levado em conta na função de negócio de **construção**, na prática de segurança de **requisitos de segurança**, nas atividades:
+ A. Incorporar requisitos de segurança nos acordos com fornecedores
+ B. Expandir o programa de auditoria aos requisitos de segurança


### 2

A empresa deve estar no **nível de maturidade 3** da prática de segurança referida para levar em conta o RGPD, pois é nesse nível em que se tem em conta um processo de requisitos de segurança obrigatório a todos os projetos de software e dependências de terceiros.


# Pergunta P1.2

### 1

As bibliotecas usadas no nosso projeto de desenvolvimento 1 foram as seguintes:
+ *crypto* - com a versão "^1.0.1" <br>
  Licenciamento: ISC License
  (*Deprecated package*)

+ *crypto-js* - com a versão "^4.1.1" <br>
  Licenciamento: The MIT License (MIT)

+ *fs* - com a versão "^0.0.1-security" <br>
  Licenciamento: ISC License
  (*Security holding package*)

+ *path* - com a versão "^0.12.7" <br>
  Licenciamento: MIT License

+ *prompt-sync* - com a versão "^4.2.0" <br>
  Licenciamento: MIT License

+ *shamirs-secret-sharing* - com a versão "^1.0.1" <br>
  Licenciamento: MIT License

Usamos ainda o JavaScript runtime *Node.js*, com a versão "v17.8.0", que está sob licenciamento do MIT.


### 2

Os pacotes sob [licenciamento do MIT](http://opensource.org/licenses/MIT) tem as seguintes permissões e restrições:

+ Permissões:
  +  Uso comercial
  +  Modificação
  +  Distribuição
  +  Uso privado

+ Limitações:
  + Responsabilidade
  + Garantia

Tâm ainda a condição de aviso de licença e direitos de autor aquando do seu uso.

Já os pacotes sob [licenciamento ISC](https://opensource.org/licenses/ISC), tem as seguintes permissões e limitações:

+ Permissões:
  + Uso para qualquer propósito
  + Cópia
  + Modificação
  + Distribuição

+ Limitações:
  + Responsabilidade
  + Garantia

Tal como no licenciamento MIT, têm a condição de que um aviso de licença e de direitos de autor deve aparecer em todas as cópias.

### 3

Consideramos importante anotar os direitos de autor do código *open source* usado, assim como dar a conhecer o seu licenciamento. Para além disto, a documentação do uso desse código, instalação das respetivas dependências e até vulnerabilidades são tópicos de interesse que devem, tanto quanto o possível, ser referidos.


# Pergunta P2.1
As práticas de segurança escolhidas foram o *Threat Assessment* e os *Security Requirements* da área *Construction*, e o *Security Testing* da área *Verification*. As áreas escolhidas são as mais adequadas e as mais exequíveis ao nosso projeto, dada a dimensão do mesmo e dos recursos humanos e técnicos da equipa de desenvolvimento.

# Pergunta P2.2
O *score* obtido pelo preenchimento do documento *SAMM_grupo8.xlsx* relativamente às práticas de *Threat Assessment* e *Security Testing*, revela o objetivo de alcançar o nível 1 de maturidade. Em relação à prática de *Security Requirements*, uma vez já atingido o nível 1, o objetivo é avançar para o nível 2.

# Pergunta P2.3
***Threat Assessment***: documentar os piores casos de ataque ao software, bem como os tipos de agentes invasores e atacantes e as suas potenciais motivações para abusar do nosso software.

***Security Testing***: documentar os casos de teste que são desejáveis executar e
informar devidamente os *stakeholders* dos resultados destas operações e das questões de segurança relacionadas com a criação do projeto.

***Security Requirements***: definir uma equipa para rever, periodicamente, a maioria dos controlos de acesso ao projeto, e fazer *benchmarking* de diferentes atividades de segurança, implementando as que forem consideradas importantes.