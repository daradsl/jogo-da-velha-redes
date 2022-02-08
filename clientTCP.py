from socket import *
from game import boardPos, printBoard, validInput, checkVictory, checkMovement, doMovement, atualizaBoard

serverIp='192.168.0.111'  
serverPort= 12500

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIp,serverPort))

message = ' '
while(message != 'start'):     # se nao for start envia de novo outra msg
    message = input("Digite start para começar: ")
    clientSocket.send((bytes(message, "ascii"))) # message é enviada p servidor em bytes

player = 0
token = ['X', 'O']
pos = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
boardPosic = boardPos()


myIp = clientSocket.recv(1500)  # servidor retorna meu ip
print("Jogador X: ", myIp.decode(),  "  vs  Jogador O: ", serverIp, "\n\n")
print("---------- Jogo da Velha -----------")

# ------- loop de um game ---------
while(True):
    sair = False
    board = clientSocket.recv(1500)         # Recebe o tabuleiro
    board = board.decode()

    # ---- verifica se o outro jogador venceu ou se deu empate -----
    if((board == "win")or(board == "emp")):             
        board2 = clientSocket.recv(1500)     # recebe o tabuleiro final
        board2 = board2.decode()
        boardGame = atualizaBoard(list(board2)) # converte a string do tabuleiro recebida em um vetor e transforma no tabuleiro atualizado
        if(board == "win"):
            winner = 1      # jogador 1 venceu
            print("-------- Você perdeu :(  -------\n")
        else:
            winner = 3    # empatou
            print("-------- Deu Velha -------")
        printBoard(boardGame)
        sair = True
    else:
        boardGame = atualizaBoard(list(board)) # converte a string do tabuleiro recebida em um vetor e transforma no tabuleiro atualizado

        jogada = False
        # ---------- Minha vez -----------
        while(jogada != True):	# enquanto for posicao invalida
            print("Posições: ")
            printBoard(boardPosic)
            print("\nTabuleiro: ")
            printBoard(boardGame)
            n = validInput("\n-> Sua Vez!\nEscolha a posição: ")
            n = n-1
            a = pos[n]
            i = a[0]
            j = a[1]
            jogada = (checkMovement(boardGame, i, j))

            if(jogada): # jogada valida
                doMovement(boardGame, i, j, player) # faz uma jogada
                printBoard(boardGame)   # printa tabuleiro
                aux = (list(board))
                aux[n] = token[player]
                board = (aux[0]+aux[1]+aux[2]+aux[3]+aux[4]+aux[5]+aux[6]+aux[7]+aux[8])
                winner = checkVictory(boardGame)    # checa se venceu
                if(winner == token[player]):    # verifica se ganhou
                    clientSocket.send((bytes("win", "ascii"))) 	# avisa que ganhou
                    print("----- Parabens você venceu! :D ------\n")
                    winner = 0
                    clientSocket.send((bytes(board, "ascii"))) # tabuleiro final enviado 
                    sair = True
                if(winner == "Empate"):
                    clientSocket.send((bytes("emp", "ascii"))) 	# avisa que empatou
                    print("------- Empatou -------")
                    winner = 3
                    clientSocket.send((bytes(board, "ascii"))) # tabuleiro final enviado 
                    sair = True
                # o jogo continua 
                if(sair == False):
                    print("-> Vez do jogador: O...")
                    clientSocket.send((bytes(board, "ascii"))) # envia o tabuleiro para continuar
            else:
                print("Posição Ocupada")
            if(sair):
                break
    if(sair):
        break


if(winner == 3):
    print("------- Ninguém venceu! Deu Velha! ---------")
else:
    print("\n----------  VENCEDOR: ", token[winner], "  ------------")
    if(winner == 1):
        winner = serverIp
    else:
        winner = myIp.decode()
    print(" #  O vencedor foi o jogador =>  ", winner)
    clientSocket.close()