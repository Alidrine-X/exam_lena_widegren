"""
actions.py

Hanterar spelarens kommandon och deras effekter i spelvärlden.
Innehåller rörelse, fällor, bombhantering, spawn av nytt ätbart
och spelets avslut via exit.
"""

#==============================================================================

import random
import time
from src.builder import place_items_from_list
from src.objects import Bomb, Entity, Exit, Trap, Wall, edible_templates


# -----------------------------------------------------------------------------
# Funktioner som hanterar spelarens kommandon och rörelser
# -----------------------------------------------------------------------------

# Dictionary med alla giltiga kommandon
commands = {
    "w": ("move", (0, -1), 1),  # Move up
    "a": ("move", (-1, 0), 1),  # Move left
    "s": ("move", (0, 1), 1),  # Move down
    "d": ("move", (1, 0), 1),  # Move right
    "jw": ("jump", (0, -1), 2),  # Jump up
    "ja": ("jump", (-1, 0), 2),  # Jump left
    "js": ("jump", (0, 1), 2),  # Jump down
    "jd": ("jump", (1, 0), 2),  # Jump right
    "i": ("inventory", None, None),  # Show inventory
    "t": ("trap", None, None),  # Disarm trap
    "b": ("bomb", None, None),  # Place bomb
    "e": ("exit", None, None),  # Exit as winner
    "q": ("quit", None, None),  # Quit
    "x": ("quit", None, None)  # Quit
}


def try_move_player(grid, player, dx, dy, move_count):
    """Flyttar spelaren move_count steg och returnerar True om flytten lyckades."""

    # Skannar vägen för hinder (1 eller 2 steg framåt)
    for i in range(1, move_count + 1):
        check_x = player.pos_x + (dx * i)
        check_y = player.pos_y + (dy * i)
        item = grid.get(check_x, check_y)

        if isinstance(item, Wall):

            # Försöker riva väggen. Om det misslyckas stannar vi helt.
            if not item.try_to_demolish(player, grid):
                return False

    # Genomför flytten om vägen hit var fri (eller röjd).
    player.move(dx * move_count, dy * move_count)

    # Uppdaterar poäng och bördig jord för varje steg som tagits
    for _ in range(move_count):
        player.move_points()

    # Interagerar med det som finns på slutdestinationen
    final_item = grid.get(player.pos_x, player.pos_y)
    if isinstance(final_item, Entity):
        final_item.interact(player, grid, player.pos_x, player.pos_y)

    # Uppdaterar världen med nytt ätbart tack vare bördig jord
    update_world(grid, player)

    return True


def try_disarm_trap(grid, player):
    """Med kommando T, tas fälla bort om spelaren står på den"""
    current_item = grid.get(player.pos_x, player.pos_y)

    if isinstance(current_item, Trap):
        current_item.disarm(grid, player.pos_x, player.pos_y)
    else:
        print(f"\nYou need to stand on a trap to remove it.")


def try_place_bomb(grid, player):
    """Med kommando B, placeras bomb ut i spelvärlden där spelaren står"""
    bomb = next((i for i in player.inventory if getattr(i, 'can_explode', False)), None)

    # Tänder bomben, om bomb finns i inventory och spelare är tillräckligt långt från väggen
    if bomb:
        if (1 < player.pos_x < grid.width - 2) and (1 < player.pos_y < grid.height - 2):
            player.bomb_timer = 1   # Start timer (1 = bomb placed, explosion after >=4)
            bomb.symbol = "*"
            bomb.placed = True
            grid.set(player.pos_x, player.pos_y, bomb)
            player.inventory.remove(bomb)
            print(f"\nNow you have placed the bomb and lit the fuse.")
        else:
            print(f"\nYou are to close to the wall, you got to move to place the bomb.")
    else:
        print(f"\nThere is no bomb in your inventory, you have to pick it up first.")


def try_exit_game(grid, player):
    """Med kommando E, avslutas spelet om alla ursprungliga ätbara saker är upplockade."""
    current_item = grid.get(player.pos_x, player.pos_y)

    if isinstance(current_item, Exit):
        if current_item.interact(player, grid, player.pos_x, player.pos_y):
            return True
    else:
        print(f"\nYou need to stand on E to Exit.")

    return False

# -----------------------------------------------------------------------------
# Funktioner som körs automatiskt eller som en konsekvens av en handling
# -----------------------------------------------------------------------------

def spawn_random_edible(grid, is_new):
    """Väljer ut något slumpmässig ätbart från originallistan och placerar i spelvärlden."""
    # Väljer ett objekt-template från den importerade listan 'edible_templates'
    new_edible = random.choice(edible_templates)

    # Skickar föremålet i en lista för utplacering i grid
    place_items_from_list(grid,[new_edible], is_new)

    # Returnerar namnet så att game_new.py kan skriva ut det
    return new_edible.name


def update_world(grid, player):
    """Lägger till nytt ätbart i spelvärlden när spelaren tagit 25 steg (med is_new=True)."""
    if player.fertile_soil >= 25:
        is_new = True
        name = spawn_random_edible(grid, is_new)
        print(f"\n🌱 A new {name} grew from the fertile soil!")
        player.fertile_soil -= 25


def detonate_bomb(grid, player):
    """Detonerar bomben när spelaren plockat upp den, placerat ut den och gått 3 steg"""
    for y in range(grid.height):
        for x in range(grid.width):

            # Bomben har hittats, rensa 3 x 3 rutor
            if isinstance(grid.get(x, y), Bomb):
                print("\n💥 TICK... TICK... BOOM!")

                # Ritar ut explosionen först i 3x3
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        grid.set(x + dx, y + dy, grid.blast)

                # Skriver ut grid och pausar, så spelaren hinner se explosionen
                print(grid)
                time.sleep(0.5)

                # Rensar i 3x3 runt bomben
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        grid.clear(x + dx, y + dy)

                # Kontrollerar om spelaren träffas av explosionen
                if abs(player.pos_x - x) <= 1 and abs(player.pos_y - y) <= 1:
                    print("\nAargh! You got caught in the blast wave!")
                    player.score -= 20

                return  # Vi hittade och sprängde bomben, vi kan sluta leta
