Inicialmente o servidor deve ser iniciado (serverTCP.py), o qual irá esperar a conexão de um cliente que será o outro jogador (clientTCP.py).
Depois do cliente se conectar ao servidor é necessário que o cliente entre com a palavra "start", que será enviada ao servidor para que seja dado inicio a partida.
A partir deste momento a partida é iniciada. Será alternado entre cliente e servidor o turno de cada jogada, informando a vez de cada um jogar.
Para efetuar uma jogada basta entrar com o número correspondente a cada posição do tabuleiro que é printado na tela.
Exemplo de tabuleiro:
1 | 2 | 3
_________
4 | 5 | 6
_________
7 | 8 | 9
Para efetuar uma jogada basta escolher por uma posição de acordo com o exemplo acima, que ainda esteja livre (em branco).
O jogo acaba quando algum jogador vencer ou quando a partida empatar.