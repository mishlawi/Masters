# Pergunta P1.1

No ranking 8 podemos encontrar a *Weakness* com o ID 22: ***CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')***.

Esta *weakness* é caracterizada pelo facto do *software* utilizar *input* externo para construir um caminho destinado a identificar um ficheiro ou diretoria numa diretoria "pai" restrita. No entanto, esse *software* não neutraliza elementos especiais que podem causar uma resolução do caminho para uma localização fora da diretoria à qual está restrita.

Por exemplo, elementos como ".." e "/" são elementos especiais que podem ser usados para navegar entre diretorias e, especialmente o elemento "../", utilizados para sair dessa diretoria. Isto é conhecido como "*path traversal*" e também cobre o uso de caminhos absolutos como "/usr/local/bin", permitindo o acesso a ficheiros indesejáveis. Em algumas linguagens de programação, a injeção de um *null byte* (0 ou NULL), pode permitir ao atacante truncar um caminho gerado pelo *software*, por exemplo, o *software* pode adicionar a extensão ".txt" a qualquer caminho recebido, restringindo o acesso a ficheiros de texto, no entnato, com a *null injection*, o atacante pode remover essa restrição.

O **modo de introdução** desta falha pode ser na fase de aquitetura e design e também na fase de implementação, tornando esta uma **vulnerabilidade de projeto ou de codificação**.

Esta *weakness* é **independente de linguagens**, não há nenhuma linguagem prevalente determinada.

Listamos agora as suas consequências mais comuns:
| *Scope*                                          | Impacto                                                                                                                                                                                                                                                                                                                                                                                                                        |
| :----------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Integridade, Confidencialidade e Disponibilidade | **Impacto técnico:** Executar cóigo ou comandos não autorizados <br> O atacante pode criar ou reescrever ficheiros usados para executar código, como programas ou librarias                                                                                                                                                                                                                                                    |
| Integridade                                      | **Impacto técnico:** Modificar ficheiros ou diretorias <br> O atacante pode reescrever ou criar ficheiros criticos como programas, librarias ou dados importantes. Se o ficheiro alvo é usado para um mecanismo de segurança, então o atacante pode conseguir ultrapassar esse mecanismo. Por exemplo, adicionar uma conta no final de um ficheiro de *passwords* pode permitir-lhe ultrapassar autenticação.                  |
| Confidencialidade                                | **Impacto técnico:** Ler ficheiros ou diretorias <br> O atacante pode conseguir ler o conteúdo de alguns ficheiros e expor dados sensíveis. Se o ficheiro alvo for usado para um mecanismo de segurança, o atacante pode conseguir ultrapassar esse mecanismo. Por exemplo, ao ler um ficheiro de *passwords*, o atacante pode realizar ataques de *brute force* para adivinhar as *passwords* e entrar numa conta do sistema. |
| Disponibilidade                                  | **Impacto técnico:** *Denial of service* - *Crash*, saída ou reinício <br> O atacante pode reescrever, apagar ou corromper ficheiros críticos como programas, librarias ou dados importante. Isto pode impedir o *software* de funcionar de todo e, no caso de um mecanismo de proteção como autenticação, tem o potencial de bloquear todos os utilizadores do *software*.                                                    |


Podemos ver um exemplo demonstrativo desta *weakness* no código seguinte:
```Java
String path = getInputPath();
if (path.startsWith("/safe_dir/")){
    File f = new File(path);
    f.delete()
}
```
Este excerto de código Java valida um determinado *input path* ao verificar se este começa com "/safe_dir/" e, se for validado, apaga o ficheiro.

No entanto, um atacante pode introduzir o seguinte caminho `/safe_dir/../important.dat`, que é válido, pois começa com "/safe_dir/", mas acede a um ficheiro fora dessa diretoria.

O **CVE-2010-0467** é um exemplo de vulnerabilidade onde esta *weakness* é explorada. Aqui, a componente ccNewsletter 1.0.5 do Joomla! permite que um atacante leia ficheiros arbitrários usando o elemento ".." no parâmetro controlador numa ação ccnewsletter para o index.php.



# Pergunta P1.2

Vulnerabilidades de projeto:

+ utilização de um mecanismo de autenticação fraco
+ não colocar nenhum requisito de um canal TLS entre o cliente e o servidor (pois a comunicação pode ser observada na rede)
  
  A correção destas vulnerabilidades podem ser complicadas na medida em que pode ser necessário um redesenho de todo o projeto, deste vez tendo em conta novos requisitos de segurança.

Vulnerabilidades de codificação:

+ não verificação de limites de escrita num *buffer*, provocando a possibilidade de um ataque de *buffer overflow*
+ não verificação de elementos especiais na introdução de caminhos para ficheiros
  
  Para este tipo de vulnerabilidades, a dificuldade de correção depende bastante da vulnerabilidade em si, pode tornar-se bastante difícil em códigos *legacy* por exemplo, nos quais não é possível efetuar certas alterações. Por exemplo, no caso do primeiro exemplo, o uso de uma linguagem que contenha um sistema de verificação contra *buffer overflow* seria uma opção, no entanto, isto seria também bastante trabalhoso, se se tratar de um *software* com muitas linhas de código.


Vulnerabilidades operacionais:

+ existência de conta sem password numa base de dados
+ configuração por defeito que não é alterada após a instalação do sistema
  
  Este tipo de vulnerabilidades dependem de terceiros e de condições externas e fora do controlo de quem desenvolveu o *software*, podendo tornar a sua correção nais difícil. No entanto, poderá também ser tão simples como guiar um utilizador numa configuração nova do sistema, no caso de uma vulnerabilidade causada pelo descrito no segundo exemplo.



# Pergunta P1.3

Uma vulnerabilidade dia-zero é uma vulnerabilidade que é conhecida apenas num meio muito restrito e que é usada por grupos de piratas informáticos para ataques ou venda, ou pelo meio militar de um país como ciber-arma, já uma vulnerabilidade de operação que não seja dia-zero é uma vulnerabilidade que é conhecida na comunidade de segurança informática e pelo público em geral, visto que, ao ser tornada pública, qualquer pessoa pode tomar conhecimento da existência da mesma.