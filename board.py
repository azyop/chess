import re


SizeBoard = 8
initial_coord = [[(0, 0) for x in range(SizeBoard)] for y in range(SizeBoard)]
initial_board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

def calcul_offset(src, dst):
    xoff = dst[0] - src[0]
    yoff = dst[1] - src[1]
    return (int(xoff),int(yoff))

def board_to_fen(board,coups,castle,color):
    fen = ""
    for y in reversed(board):
        line = ""
        for x in y:
            line += x
        cnt = 0
        for i in line:
            if i!= " ":
                if cnt!=0:
                    fen += str(cnt)
                    cnt = 0
                fen += i
            else:
                cnt += 1
        if cnt != 0:
            fen += str(cnt)
        fen += '/'
    fen = fen[:-1] + " " + color[0] + " "+castle+" - 0 "+str(coups)
    return fen



def check_castle_white(board, cw):
    s = ""
    if board[0][4] != "K":
        return s
    if 'K' in cw:
        if board[0][4] == "K" and \
            board[0][7] == "R":
            s += 'K'
    if 'Q' in cw:
        if board[0][4] == "K" and \
            board[0][0] == "R":
            s += 'Q'
    return s


def check_castle_black(board, cb):
    s = ""
    if board[7][4] != "k":
        return s
    if 'k' in cb:
        if board[7][4] == "k" and \
            board[7][7] == "r":
            s += 'k'
    if 'q' in cb:
        if board[7][4] == "k" and \
            board[7][0] == "r":
            s += 'q'
    return s

def board_modif(board,src,dst):
    eat = False
    src = sf_pos_to_board_pos(src)
    dst = sf_pos_to_board_pos(dst)
    if board[dst[1]][dst[0]] != " " and board[dst[1]][dst[0]].lower() != "p":
        eat = True
    board[dst[1]][dst[0]] = board[src[1]][src[0]]
    board[src[1]][src[0]] = " "
    return (board,eat)

def board_state(driver):
    board = [[" " for x in range(SizeBoard)] for y in range(SizeBoard)]
    all_p = driver.find_elements_by_xpath("//div[contains(@class, 'square-') and contains(@class, 'piece')]")
    for p in all_p:
        try:
            v = p.get_attribute("class")
            color = re.search(r"([w|b][a-z])", v)
            pos = re.search(r"square-(\d{2})", v)
            # reg = re.search(r"piece ([a-z]{2}) square-(..)", v)
            if color is not None and pos is not None:
                p = color.group(1)
                c = pos.group(1)
                if p[0] == "w":
                    board[int(c[1])-1][int(c[0])-1] = p[1].upper()
                else:
                    board[int(c[1])-1][int(c[0])-1] = p[1]
        except Exception as e:
            print("ERROR:",e)
    return board

def pos_to_coord(pos,coord,color):
    if color == "white":
        x = ord(pos[0])-ord('a')
        y = int(pos[1])-1
        return coord[x][y]
    else:
        x = 7 - (ord(pos[0])-ord('a'))
        y = 7 - (int(pos[1]) - 1)
        print(x,y)
        return coord[x][y]

def sf_pos_to_board_pos(pos):
    x = ord(pos[0])-ord('a')
    y = int(pos[1])-1
    return (x,y)


def sf_pos_to_chesscom_piece(driver,pos):
    x = ord(pos[0])-ord('a')+1
    y = int(pos[1])
    chesscom_pos = "square-"+str(x)+str(y)
    p = driver.find_element_by_xpath("//div[contains(@class, '"+chesscom_pos+"') and contains(@class, 'piece')]")
    return p
