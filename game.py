#-------- Funções -------------

token = ["X", "O"]

def boardPos():
    board = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ]
    return board

# ---- imprime o tabuleiro ----
def printBoard(board):
    for i in range(3):
        print("|".join(board[i]))
        if(i<2):
            print("------")

# ---- verifica se a entrada é um numero válido ----
def validInput(msg):
    try:
        n = int(input(msg))
        if(n >=1 and n <= 9):
            return n
        else:
            print("Numero inválido")
            return validInput(msg)
    except:
        print("Numero inválido")
        return validInput(msg)

#---- Checa se deu vitoria ou empate ----
def checkVictory(board):  
    for i in range(3): # linhas
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != ' '):
            return board[i][0]
    
    for i in range(3):  # colunas
        if(board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != ' '):
            return board[0][i]
  
    if(board[0][0] != ' ' and board[0][0] == board[1][1] and board[1][1]==board[2][2]): # diagonal principal
        return board[0][0]
   
    if(board[0][2] != ' ' and board[0][2] == board[1][1] and board[1][1]==board[2][0]): # diagonal secundaria
        return board[0][2]

    for i in range(3):
        for j in range(3):
            if(board[i][j] == ' '):
                return False
    
    return "Empate"

# ---- Checa se a posicao esta livre -----
def checkMovement(board, i, j):
    if(board[i][j] == ' '):
        return True
    else:
        return False

# ---- Faz a Jogada -------
def doMovement(board, i, j, player):
    board[i][j] = token[player]

# ---- Atualiza o vetor que é passado como mensagem em tabuleiro do jogo ------
def atualizaBoard(gameBoard):
    pos = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    board = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
    for aux in range(9):
        a = pos[aux]
        i = a[0]
        j = a[1]
        if(gameBoard[aux]=='X'):
            board[i][j] = 'X'
        if(gameBoard[aux]=='O'):
            board[i][j] = 'O'

    return board
