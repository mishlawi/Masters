# Notas

## Etapa 1: Estratégia 1

ver código

---

## Etapa 2: Estratégia 1

Fluxo:
- Nodo anterior: `InetAddress`
- Métrica: `int`
- Nodos seguintes: `Set<Pair<InetAddress, Estado>>`

Estado:
- Ativo
- Inativo

Lista de fluxos em cada nodo

Mensagens:
- fluxo info
- streaming data
- ack negativo

---

## Etapa 3

...

---

## Etapa 4: Estratégia 1

...

--- 

## coisas a implementar/corrigir

- Sofia: Envio do ANNOUNCEMENT mesmo quando a informação não é melhor (para reconstruir rotas perdidas)
  - Tirar flood das condições, mandar sempre
- Sofia: Fazer RT_ACTIVATE, RT_DEACTIVATE e RT_LOST
- Duarte: Fazer cliente com "GUI"
- ???: Fazer componente streamer do servidor

## pseudo-código para RT_LOST: situação em que existem rotas geradas entre pai e filho

filho deixa de receber heartbeats do pai ou recebe RT_LOST
- manda RT_LOST para os filhos
- apaga tabela de rotas

pai deixa de receber heartbeats do filho
- apaga rota

## opcional

- Mensagem de log (etapa 3)
- Overlay não dependente do underlay (vários IPs para o mesmo host + hosts não diretamente conectados entre si)
  