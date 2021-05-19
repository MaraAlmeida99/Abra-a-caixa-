# Abra a Caixa

<p align="center">
 <a href="#objetivo">Descrição do Projeto</a> •
 <a href="#Componentes">Interligação dos Componentes</a> •
 <a href="#ReqF">Requisitos Funcionais</a> •
 <a href="#Setup">Setup</a> • 
 <a href="#Inst">Instalação</a> • 
 <a href="#Configurações Iniciais">Configurações Iniciais</a> • 
 <a href="#Execução">Passos de Execução</a> • 
 <a href="#autor">Autores</a>
</p>


## Descrição do Projeto 
O tema escolhido para o projeto da UC Sistemas Embutidos foi “Abra a Caixa”. O objetivo deste projeto, é a construção de um caixa, com um sistema de fecho, que apenas abre após a introdução correta de um certo código, composto por uma combinação de um código numérico com uma sequência de batidas e de rotações, pela ordem de execução definida.  Outro método de abertura de caixa será a partir de uma aplicação para smartphone.
A caixa irá possuir também um mecanismo luminoso para indicar se a caixa se encontra aberta ou fechada e um mecanismo de som, que será emitido durante a abertura da caixa ou como alarme quando o código é inserido incorretamente vezes consecutivas.
A aplicação de smartphone, para além de permitir a abertura da caixa, terá também incorporada uma característica que indica o estado da caixa, isto é, se a caixa se encontra aberta ou fechada, tal como o estado do progresso da introdução dos códigos e em caso da introdução incorreta do código, será emitida uma notificação. 
Para desativar o alarme, o utilizador terá que ter acesso ao smartphone ou introduzir o código correto. Após demasiadas tentativas incorretas, só será possível abrir a caixa a partir do smartphone.

### Interligação dos Componentes

No projeto temos três elementos principais de hardware, o Android, Raspberry Pi e Arduino, sendo que todos se encontram ligados à base de dados, sendo o firebase que serve de ponto intermédio entre os três elementos, conseguindo atualizar e consultar a mesma.

1. Android 

No que diz respeito ao android, serve de ponto de ligação entre a caixa e o utilizador. É no android que é possivel tanto fechar, abrir e desbloquear a caixa, como alterar o código caso seja inserido um código errado mais de 3 vezes, e receber notificações sobre os vários estados da caixa.

2. Raspberry Pi 

O elemento de hardware Raspberry Pi, será responsável pelo mecanismo de abertura da caixa, através de um pequeno motor rotativo. Neste será também possível verificar o estado da caixa através de dois sensores, um luminoso e uns speakers. Neste elemento de hardware vai ser possível abrir e fechar a caixa, assim como alterar a cor do sensor luminoso consoante o estado da caixa, por fim, vai ser possível emitir um som dependendo da ação que foi realizada.

3. Arduino 

O Arduino, segundo ponto de interação entre o utilizador e a caixa. Através dos seus três sensores, é possível introduzir o código que permite que a caixa se abra.


### Requisitos Funcionais 

RF001 - Aplicação móvel: Para que seja possível configurar e visualizar o estado da caixa, é apresentada um aplicação móvel.

RF001.1 - Definir código: A definição do código que permite a abertura da caixa é configurado na aplicação móvel. Este código tem de ser constituído obrigatoriamente por uma combinação de batidas, rotações e um código numérico de 4 dígitos.
Caso estas condições não verifiquem, será apresentada um mensagem de erro. Também na aplicação é possível visualizar que partes do código já foram introduzidas corretamente.

RF001.2 - Estado caixa: Através da aplicação é possível verificar o estado da caixa, que pode variar entre aberta ou fechada. Aqui é também possível alterar o estado da caixa sem que seja necessária a introdução do código.

RF002 - Código de abertura: É apresentado ao utilizador três formas de input do código que permite a abertura da caixa, um teclado numérico, um touch e um joycestick. Caso o código inserido não esteja correto, a caixa permanece fechada sendo disparada um notificação para o smartphone. Caso o utilizador insira três vezes consecutivas o código errado em menos de 5 minutos, será ativado um alarme sonoro, assim como disparada uma notificação no smartphone. Este sinal sonoro indica que a caixa se encontra bloqueada, só sendo possível desbloqueá-la através do smartphone através da  desativação do alarme e definindo um novo código para a caixa.

RF003 - Funções da caixa: A caixa contém um mecanismo luminoso que indica se a mesma se encontra aberta, (sinal luminoso verde), ou fechada (sinal luminoso vermelho). Contém também, um sinal sonoro, que pode ser ativado de duas formas, a primeira é através da abertura da caixa, através do código ou do smartphone, em que é emitido um sinal sonoro de curta duração. A segunda forma acontece quando é introduzido o código incorreto mais de três vezes seguidas, no espaço de 5 minutos, onde será emitido um sinal sonoro de longa duração, que só poderá ser desativado através do smartphone.
É ainda disponibilizado ao utilizador um botão que irá permitir que o mesmo possa fechar a caixa quando esta se encontrar aberta.

## Setup 
Nesta secção são descritos os passos necessários para uma prévia instalação e configurações necessárias para ser possível executar o projeto com sucesso. 

### Instalação
-Descarregar o projeto 

-instalaço de bibliotecas 

### Configurações Iniciais 
-compilação()


## Passos de Execução


## Autores


