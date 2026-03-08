"""
game.py

Startpunkt för spelet Fruit Loop

Initierar spelvärlden genom att skapa Grid och Player samt bygga upp
banan via builder-funktioner. Huvudloopen läser spelarens input, tolkar
kommandon och anropar rätt action-funktioner för att utföra spelhandlingar.

"""
#==============================================================================
from src.grid import Grid
from src.player import Player
from src.actions import try_move_player, try_place_bomb, detonate_bomb, try_exit_game, try_disarm_trap, commands
from src.builder import make_outer_walls, add_l_walls, set_player, randomize_items, set_exit

grid = Grid()
player = Player()

make_outer_walls(grid)
add_l_walls(grid)
set_player(grid, player)
randomize_items(grid, is_new=False)
set_exit(grid, player)


# Huvudloopen hanterar spelarens input och utför spelhandlingar
command = ""
while command not in ["q", "x"]:
    grid.print_status(player.score)
    print("Use WASD to move | J+WASD to jump | Q/X to quit")
    print("I = show inventory | T = disarm trap | B = place bomb | E = exit as a winner")

    # Läser spelarens kommando (max 2 tecken och case-insensitive)
    command = input("> ").casefold()[:2]

    # Slår upp kommandot i commands-dictionary och packa upp action, direction och steps
    if command in commands:
        action, direction, steps = commands[command]

        # Hanterar spelarens förflyttning, steg eller hopp
        if action in ["move", "jump"]:
            dx, dy = direction
            if try_move_player(grid, player, dx, dy, steps):

                # Bomben exploderar efter 3 steg (timer startar på 1 vid placering)
                if player.bomb_timer >= 4:
                    detonate_bomb(grid, player)
                    player.bomb_timer = 0

        # Visar spelarens inventory
        elif action == "inventory":
            player.show_inventory()

        # Avslutar spelet via Exit om alla ursprungliga ätbara saker är upplockade
        elif action == "exit":
            if try_exit_game(grid, player):
                command = "q"

        # Desarmerar en fälla
        elif action == "trap":
            try_disarm_trap(grid, player)

        # Placerar ut en bomb
        elif action == "bomb":
            try_place_bomb(grid, player)

        # Avslutar spelet
        elif action == "quit":
            break

    else:
        print(f"\nI don't understand your command: {command}")


    # Avslutar spelet om spelaren inte har några poäng kvar
    if not player.is_alive():
        print("\nYour score is 0 and you lose :(")
        break


# Körs när huvudloopen avslutats
print("\nThank you for playing!")
