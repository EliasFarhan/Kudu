#kudu start program
import sys
import os
sys.path.append(os.path.abspath("../script"))
import engine.loop as game



if __name__ == "__main__":
	game.start()