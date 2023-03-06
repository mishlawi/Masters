# Relatório
# Trabalho Prático de SPLN
## Multi-word term processor
### by: Angélica Cunha `PG47024`, Duarte Vilar`PG47157`, Tiago Barata `PG47695`

---

Este relatório pretende esclarecer o funcionamento deste programa, funcionando como um filtro unix. A informação aqui apresentada está mais compacta executando o comando `./rr --help`

### Resumo:
Este filtro pretende ser uma facilidade/utilidade no pré-processamento de linguagem natural, com algumas funcionalidades com o objetivo de poupar tempo e trabalho ao utilizador.

O programa é executado através da linha de comandos, com várias flags que podem ser usadas em simultâneo.

### Flags
* `-g <file-name>` &rarr; permite a geração de código python. É util na medida em que se o utilizador quiser fazer recorrentemente as mesmas tarefas, cria um filtro que automatiza esse processo.
* `-r <rules-file>` &rarr; permite passar um ficheiro de regras tipo NL-flex de modo a fazer alterações a um ficheiro original. As regras são executadas por ordem, sem nunca haver sobreposição das regras posteriores às anteriores.
    O formato do ficheiro é: 
    * `padrão -> subs` onde `padrão` é uma expresão regex a ser substituída por `subs` que pode ser uma expressão ou um grupo de captura do regex
    * `func()` chamando uma função a aplicar a todo(s) o(s) ficheiro(s). As funções estão na pasta `./functions`. O utilizador, com conhecimentos na área, pode adicionar funções na pasta. Cada função num ficheiro isolado, em que o nome do ficheiro é o nome da função. A partir daí pode usá-la no ficheiro de regras.
    As funções pré-definidas disponíveis são:
        * `acentos()`  &rarr; função que retira os acentos a todas as palavras
        * `converter2digit()` &rarr; função que transforma os números por extenso em dígitos
        * `converter2word()` &rarr; função que transforma os dígitos em números por extenso
        * `emoji2text()` &rarr; função que transforma emojis em texto, ficando `:significado:`
        * `lower()` &rarr; função que coloca todo o texto em minúsculas
        * `spacy_func()` &rarr; função que transforma um texto dividido por frases, onde cada frase é dividida por uma linha com #ocorrência, palavra, lemma e tipo. Entidades multi-palavra são unidas.
        * `text2emoji()` &rarr; função que transforma texto `:significado:` em emojis
        * `upper()` &rarr; função que coloca todo o texto em maiúsculas
        * `w2v()`  &rarr; cria uma lista, em que cada sublista tem a frase separada por palavras, sem as stopwords
* `-t <lang>` &rarr; executa a tradução de todo o documento numa das linguagens disponíveis:
    * ES - Espanhol
    * EN - Inglês
    * FR - Francês
    * IT - Italiano
* `--dir <caminho-pasta>` &rarr; permite a execução do programa para vários ficheiros dentro de uma única pasta
* `--print`  &rarr; permite o utilizador, em vez de gerar um novo ficheiro, escrever as alterações no ecrã
* `--spacy`  &rarr; permite o utilizador gerar um ficheiro dividido por frases, onde cada frase é dividida por uma linha com #ocorrência, palavra, lemma e tipo. Entidades multi-palavra são unidas.
* `-w2v` &rarr; permite o utilizador criar uma lista, em que cada sublista tem a frase separada por palavras, sem as stopwords. Pretende ser uma ferramente de pré-processamento para word embendings.


### Todas estas funcionalidades podem ser aplicadas
* `Documentos em específico`
* `Conjuntos de documentos`
* `Diretorias`