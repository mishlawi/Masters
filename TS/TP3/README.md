# Pré requisitos

+ python3
+ mongodb (e ter o serviço do mongo ativo)
+ no caso do macOS, [macFUSE](https://osxfuse.github.io) instalado e devidas permissões dadas
+ o utilizador ter uma conta no serviço Gmail

# Instalação de dependências

Correr o script `install.sh` através do comando 
```
bash install.sh
```

# Configuração da base de dados

1. abrir uma shell do mongo, escrevendo `mongo` num terminal
2. alterar para a base de dados 'fs':
  ``` 
  use fs
  ```
2. criar um novo utilizador (aqui damos o exemplo de um username 'root' e password 'root' que são os default no ficheiro de configuração):
  ```
  db.createUser({
    user:"root",
    pwd:"root",
    roles:[
      {role:"readWrite",db:"fs"}
    ]
  })
  ```

Ainda, é necessário preencher/alterar o ficheiro [config.ini](config.ini) com os dados necessários:
  + credenciais do utilizador criado na configuração da base de dados
  + credenciais do utilizador Gmail do qual os emails serão enviados (para a autenticação ser bem sucedida, é necessário ter uma palavra-passe de aplicações, que pode ser obtida [aqui](https://myaccount.google.com/apppasswords?rapt=AEjHL4OkuDw_loyhKgzSEbWstzE0dw3VRZBhr-1Ka5VdL6YQ4TT-5gXfUuhszPHXY53Y89nFNCozdqxJkiUHIVWpa4LxmVJlhA))


# Utilização

Num terminal, ir para a diretoria dist, criada na instalação, com `cd dist` (se já na diretoria do script de instalação) ou `cd <caminho absoluto para dist>`. Nessa diretoria:

+ adicionar permissões
  ```
  ./access_control <caminho do ficheiro> <nome do utilizador> <email>
  ```
+ iniciar o sistema de ficheiros virtual
  ```
  ./passthroughfs <caminho da diretoria a copiar> <caminho da diretoria para onde copiar>
  ```
  para abrir um ficheiro, se tiver acesso ao mesmo, será pedida a introdução de um código, previamente enviado para o email indicado aquando da adição de permissões