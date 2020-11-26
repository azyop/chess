from interface import *
from connexion import connection, reconnect
from stockfish import Stockfish


sf = Stockfish(r"C:\Users\dyildiz\Downloads\stockfish_12_win_x64_avx2\stockfish_20090216_x64_avx2.exe",
                      parameters={
                        "Threads": 3,
                        "Hash": 2048,
                        "Skill Level": 20,
                        "Minimum Thinking Time": 1,
                        "Slow Mover": 200
                    })
sf.set_depth(17)

chromedriver = "path/to/chromedriver"
driver = initialise(chromedriver)
driver = reconnect(driver)
# driver = connection(driver)
driver.get("https://www.chess.com/play/online")
sleep(10)


while(True):
    print("Search for a new Game")
    home = time.time()
    ng = False
    while(not ng):
        sleep(1)
        ng = nouveau_jeu(driver)
        if (time.time() - home) > 30:
            print("Cannot play a new game")
            exit()
    start = time.time()
    cnt = 0
    while(not in_game(driver)):
        sleep(1)
        cnt += 1
        if cnt%10 == 0:
            print("Wait the starting of game",str(round(time.time() - start))+" sec")
        if (time.time() - start) > 1800:
            print("Game not starting")
            exit()
    print("Game beginning")
    play(driver,sf)
    sleep(2)


