# Pergunta 1.1

### 1.

Para conseguir que o programa imprima ficheiros não terminados em .txt foram exploradas as vulnerabilidades de ***buffer overflow*** e de **validação de *input*** baseado em **metacaracteres**, nomeadamente sobre **delimitadores embebidos**.

Visto que a escrita do argumento passado para o *buffer* é limitada aos 64 caracteres do mesmo, se o argumento passado tiver mais do que essa quantidade de caracteres, o '.txt' que é adicionado à *string* não será copiada. Desta forma, conseguimos excluir a restrição da extensão do ficheiro. Mas isto não é o suficiente, pois precisamos de conseguir que nesses 64 caracteres esteja o nome correto do ficheiro ao qual pretendemos aceder, ou o seu caminho absoluto ou relativo.

Para tal, podemos recorrer aos delimitadores embebidos dos caminhos. No nosso caso, por trabalharmos em sistema UNIX, o delimitador de diretorias é o `/`, no caso de Windows será `\`. Assim, para acedermos a um qualquer ficheiro na mesma diretoria de onde o programa está a ser executado, basta passar como argumento do programa uma *string* que se inicie com um `.` (para indicar a diretoria em que nos encontramos com o `./`) e que se siga do número necessário de `/` para que, em conjunto com o número de caracteres do nome do ficheiro e o `.` no início da string faça os 63 caracteres que junto com o `\0` de término de *string* que é usado no C, fazem os 64 caracteres de tamanho máximo do *buffer*.

No caso de querer aceder a um ficheiro numa diretoria diferente, poderá ser usado `../` para navegar para a diretoria "pai", ou simplesmente usar o caminho absoluto do ficheiro e adicionar o número necessário de `/` para preencher os 63 caracteres, como é feito a seguir para aceder ao ficheiro `/etc/passwd`.

### 2.

```
gcc readfile.c -o readfile
```
```
./readfile `python3 -c 'print("/etc"+"/"*53+"passwd")'`
```



# Pergunta 1.2

Programa no ficheiro [P1.2.py](P1.2.py).

Algumas notas:
+ A validação do intervalo de valores para a validade do cartão de crédito teria de ser repensada para o caso de mudança de século.
+ A validação do CVC poderia ser feita também verificando o valor do CVC para o número de cartão de crédito inserido, no entanto, não conseguimos encontrar o algoritmo de verificação do mesmo.
