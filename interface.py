from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
from time import sleep
from random import randint, random

from connexion import connection
from board import *




def check_turn(driver,color="white"):
    try:
        number_move = driver.find_elements_by_xpath("//div[@data-ply]")
        number_move = len(list(number_move)) / 2
    except:
        try:
            number_move = driver.find_elements_by_xpath("//div[contains(@class, 'move-text')]")
            number_move = len(list(number_move))

        except:
            print("Check turn ERROR")
            return False
    # print("NB MOVE", number_move)
    # print("NUMB. MOVE", len(list(number_move)))
    if color == "white":
        if number_move%2 == 0:
            return True
        else:
            return False
    else:
        if number_move%2 == 1:
            return True
        else:
            return False

def clock_catch(driver):
    times = []
    clock = driver.find_elements_by_xpath("//div[contains(@class, 'clock-component')]")
    for i in list(clock):
        try:
            time = i.find_element_by_tag_name('span').text
            times.append(time)
        except:
            pass
    t1 = time_to_sec(times[0])
    t2 = time_to_sec(times[1])
    return (t1,t2)


def check_color(driver):
    for i in driver.find_elements_by_tag_name('text'):
        if i.get_attribute("x") == '0.75' and \
            i.get_attribute("y") == '3.5':
            number = int(i.text)
            break
    if number == 8:
        return "white"
    else:
        return "black"


def check_number_of_piece(board,c):
    cnt = 0
    if c=='black':
        for i in board:
            for j in i:
                if j !="k" and j!="p" and i!=" ":
                    cnt += 1
    if c == 'white':
        for i in board:
            for j in i:
                if j != "K" and j != "P" and j!=" ":
                    cnt += 1
    if cnt == 0:
        return (800,1000)
    elif cnt == 1:
        return (1000,1400)
    elif cnt == 2:
        return (1000,1400)
    else:
        return (2700,4000)


def deplace(action, piece, dst):
    xoff, yoff = dst
    action.drag_and_drop_by_offset(piece, xoff, yoff)
    action.perform()


def initialise(chromedriver_path):
    # path_driver = r"C:\Users\dyildiz\Downloads\chromedriver_win32\chromedriver.exe"
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument("user-agent=" + UA)
    driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
    return driver



def in_game(driver):
    try:
        nulle = driver.find_element_by_xpath("//span[@class='draw-button-label']")
        return True
    except:
        return False

def end_game(driver):
    try:
        for i in range(4):
            gameover = driver.find_element_by_xpath("//div[@class='live-game-buttons-game-over']")
            sleep(1)
        return True
    except:
        return False


def nouveau_jeu(driver):
    try:
        all = driver.find_elements_by_xpath("//button[@class='ui_v5-button-component ui_v5-button-basic']")
        for i in all:
            if "nouvelle" in i.text.lower():
                new = i
                break
        new.click()
        return True
    except:
        pass
    try:
        play = driver.find_element_by_xpath(
            "//button[@class='ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full']")
        play.click()
        return True
    except:
        pass
    return False



def time_to_sec(t):
    min = int(t.split(':')[0])
    sec = t.split(':')[1]
    if '.' in sec:
        sec = int(sec.split('.')[0])
    else:
        sec = int(sec)
    return min*60+sec

def move_cnt(driver):
    try:
        number_move = driver.find_elements_by_xpath("//div[contains(@class, 'move-text')]")
        return len(list(number_move))
    except:
        return -1

def time_to_move(times):

    if times[1] <= 60:
        return
    if times[1] <= 90:
        sleep(randint(1,3)+random())
        return

    time = abs(times[0]-times[1])
    if time < 10:
        sleep(randint(0, 6000)/1000)
        return
    if time > 90:
        sleep(randint(0, 1800)/1000)
        return
    if times[1] < times[0]:
        if time > 30:
            t = time * ((random() % 0.1) + 0.05)
        else:
            t = time*((random()%0.2)+0.1)
        sleep(t)
    else:
        t = time * ((random() % 0.4) + 0.1)
        sleep(t)
    return

def play(driver, sf):
    global initial_board
    global initial_coord

    color = check_color(driver)

    board = initial_board
    coord = initial_coord

    if color == "white":
        p = driver.find_element_by_xpath("//div[contains(@class, 'square-11')]")
    else:
        p = driver.find_element_by_xpath("//div[contains(@class, 'square-88')]")
    print(p.location)
    for x in range(SizeBoard):
        for y in range(SizeBoard):
            coord[x][y] = (p.location['x']+p.size['height']*x, p.location['y']-p.size['height']*y)

    castleB = True
    castleW = True
    cw = "KQ"
    cb = "kq"
    castle = cw + cb
    coups = 1
    Game = True

    while(Game):
        action = ActionChains(driver)
        ok = True
        # t1, t2 = clock_catch(driver)
        print("Enter OK loop")
        while (ok):
            if end_game(driver):
                Game = False
                break
            if check_turn(driver, color=color):
                print("Enter Check_Turn loop")
                sleep(0.1)
                new_board = board_state(driver)
                # for i in reversed(new_board):
                #     print(i)
                break
            sleep(0.05)


        if Game:
            board = new_board

            fen = board_to_fen(board, coups, castle,color)# board_to_fen(board,coups,castle,color)
            print("FEN:", fen)
            sf.set_fen_position(fen)
            print("Check BM loop")
            times = clock_catch(driver)
            if times[1] < 60:
                bm = sf.get_best_move_time(300)
            elif times[1] < 90:
                bm = sf.get_best_move_time(500)
            else:
                if random()<0.25: #bad moves
                    bm = sf.get_best_move()
                else:
                    bm = sf.get_best_move_time(1000)
            print("Best Move:", bm)

            src = bm[:2]
            dst = bm[2:]


            board,eat = board_modif(board, src, dst)
            print("Catch positions")
            p = sf_pos_to_chesscom_piece(driver, src)
            src = pos_to_coord(src,coord,color)
            dst = pos_to_coord(dst,coord,color)
            diff = calcul_offset(src, dst)
            # times = clock_catch(driver)
            # print(times)
            print("Pause")
            if not eat and coups > 5:
                time_to_move(times)
            else:
                sleep(randint(300,600)/1000)
            print("Catch mv_cnt")
            mcnt = move_cnt(driver)
            print("Moving the piece")
            deplace_bool = 5
            while(deplace_bool > 0):
                try:
                    deplace(action, p, diff)
                    break
                except:
                    deplace_bool -= 1
                    sleep(0.5)
            start_move = time.time()
            while(mcnt <= move_cnt(driver)):
                if end_game(driver):
                    Game = False
                    break
                sleep(0.05)
                if (time.time()-start_move > 3):
                    print("Move not Done")
                    break
            if Game:
                print("Castling check")
                coups += 1
                if castleW:
                    cw = check_castle_white(board, cw)
                    if cw == "":
                        casleW = False

                if castleB:
                    cb = check_castle_black(board, cb)
                    if cb == "":
                        casleB = False
                castle = cw + cb
                if castle == "":
                    castle = "-"

                for i in reversed(board):
                    print(i)


    print("END GAME")


def play_computer(driver, sf):
    global initial_board
    global initial_coord

    color = check_color(driver)
    print(color)

    board = initial_board
    coord = initial_coord

    if color == "white":
        p = driver.find_element_by_xpath("//div[contains(@class, 'square-11')]")
    else:
        p = driver.find_element_by_xpath("//div[contains(@class, 'square-88')]")
    print(p.location)
    for x in range(SizeBoard):
        for y in range(SizeBoard):
            coord[x][y] = (p.location['x']+p.size['height']*x, p.location['y']-p.size['height']*y)

    castleB = True
    castleW = True
    cw = "KQ"
    cb = "kq"
    castle = cw + cb
    coups = 1
    Game = True

    while(Game):
        action = ActionChains(driver)
        ok = True
        while (ok):
            if end_game(driver):
                Game = False
                break
            if check_turn(driver, color=color):
                sleep(0.1)
                new_board = board_state(driver)
                for i in reversed(new_board):
                    print(i)
                break
            sleep(0.05)


        if Game:
            board = new_board

            fen = board_to_fen(board, coups, castle,color)# board_to_fen(board,coups,castle,color)
            print("FEN:", fen)
            sf.set_fen_position(fen)


            bm = sf.get_best_move()
            print("Best Move:", bm)

            src = bm[:2]
            dst = bm[2:]


            board,eat = board_modif(board, src, dst)

            p = sf_pos_to_chesscom_piece(driver, src)
            src = pos_to_coord(src,coord,color)
            dst = pos_to_coord(dst,coord,color)
            diff = calcul_offset(src, dst)

            sleep(randint(300,600)/1000)
            mcnt = move_cnt(driver)
            # print("Moving from ",bm[:2],bm[2:])
            deplace(action, p, diff)
            # print("Wait moving")
            while(mcnt == move_cnt(driver)):
                if end_game(driver):
                    Game = False
                    break
                sleep(0.05)
            if Game:
                # print("Move done")
                coups += 1
                if castleW:
                    cw = check_castle_white(board, cw)
                    if cw == "":
                        casleW = False

                if castleB:
                    cb = check_castle_black(board, cb)
                    if cb == "":
                        casleB = False
                castle = cw + cb
                if castle == "":
                    castle = "-"

                for i in reversed(board):
                    print(i)


    print("END GAME")