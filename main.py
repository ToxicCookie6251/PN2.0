from game import Game
from menu import Menu

def main():
    menu = Menu()
    game_state = menu.run()  # Call the run method of the Menu class

    if game_state == "playing":
        game = Game()
        game.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)