from socket import *
from game import boardPos, printBoard, validInput, checkVictory, checkMovement, doMovement, atualizaBoard

serverPort = 12500
serverIp = '192.168.0.111'     

serverSocket = socket(AF_INET,SOCK_STREAM)	# TCP
serverSocket.bind((serverIp, serverPort))
serverSocket.listen(1)
print ("..... Aguardando Jogador......")

while 1:
    connectionSocket, clientAddress = serverSocket.accept()		# conectado com o cliente
    #print("Jogador 1: 192.168.0.111 e Jogador 2: ", clientAddress[0])

    message = connectionSocket.recv(1500)	# message recebida em bytes
    while(message.decode() != 'start'):	# só começa o jogo quando receber o start
        message = connectionSocket.recv(1500)		   

    pos = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    token = ['X', 'O']
    boardPosic = boardPos()
    player = 1
    
    print("Jogador X: ", clientAddress[0], "  vs  Jogador O: ", serverIp, "\n\n")
    connectionSocket.send(bytes(clientAddress[0], "ascii")) # envia o endereco ip do outro jogador 
    print("---------- Jogo da Velha -----------")
    gameBoard = "123456789"
    connectionSocket.send(bytes(gameBoard, "ascii"))	# Começa enviando o tabuleiro inicial (vazio)


    # ----- loop de um game -------
    while(True):
        board = connectionSocket.recv(1500)         # Recebe o tabuleiro
        board = board.decode()
        sair = False

        # ---- verifica se o outro jogador venceu ou se deu empate -----
        if((board == "win")or(board == "emp")):     # jogador 0 ganhou
            board2 = connectionSocket.recv(1500) # Recebe o tabuleiro final
            board2 = board2.decode()
            boardGame = atualizaBoard(list(board2))			
            if(board == "win"): # jogador 0 venceu
                winner = 0
                print("------- Você perdeu :(  --------\n")
            else:   # empatou
                winner = 3
                print("-------- Deu Velha -------")
            printBoard(boardGame)
            sair = True
        else:
            boardGame = atualizaBoard(list(board)) # converte a string do tabuleiro recebida em um vetor e transforma no tabuleiro atualizado

            # ---------- Minha vez ---------	
            jogada = False
            while(jogada != True):  # enquanto a jogada nao for valida
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
                if(jogada):	# jogada valida
                    doMovement(boardGame, i, j, player)	# faz uma jogada
                    printBoard(boardGame)   # printa tabuleiro
                    aux = (list(board))
                    aux[n] = token[player]
                    board = (aux[0]+aux[1]+aux[2]+aux[3]+aux[4]+aux[5]+aux[6]+aux[7]+aux[8])
                    winner = checkVictory(boardGame)
                    if(winner == token[player]):    # verifica se ganhou
                        connectionSocket.send((bytes("win", "ascii"))) 	# avisa que ganhou
                        print("------ Parabens você venceu! :D ----- \n")
                        winner = 1
                        connectionSocket.send((bytes(board, "ascii"))) # tabuleiro final enviado
                        sair = True
                    if(winner == "Empate"):
                        clientSocket.send((bytes("emp", "ascii"))) 	# avisa que empatou
                        print("------- Empatou -------")
                        winner = 3
                        clientSocket.send((bytes(board, "ascii"))) # tabuleiro final enviado 
                        sair = True                        
                    if(sair == False):  # o jogo continua
                        print("-> Vez do jogador: X...")
                        connectionSocket.send((bytes(board, "ascii"))) # tabuleiro enviado em bytes
                else: # jogada invalida
                    print("Posição Ocupada")
                if(sair):
                    break
        if(sair):
            break

    if(winner == 3):
        print("-------- Ninguém venceu! Deu Velha! ---------")
    else:
        print("\n----------  VENCEDOR: ", token[winner], "  ------------")
        if(winner == 0):
            winner = clientAddress[0]
        else:
            winner = serverIp
        print(" #  O vencedor foi o jogador =>  ", winner)
        connectionSocket.close()
