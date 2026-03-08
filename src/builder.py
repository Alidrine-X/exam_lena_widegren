"""
builder.py

Skapar och placerar ut väggar, föremål, spelare och exit i spelets rutnät.
Innehåller metoder som körs vid spelets start för att bygga upp banan.
"""

#==============================================================================

from src.objects import Edible, Exit, Chest, Key, Trap, Wall, edible_templates, traps, tools, bombs


def make_outer_walls(grid):
    """Skapar oförstörbara ytterväggar runt hela spelvärlden"""
    # Vertikala väggar (vänster och höger sida)
    for i in range(grid.height):
        grid.set(0, i, Wall("Outer Wall", "█", destructible=False, wall_id=None))
        grid.set(grid.width - 1, i, Wall("Outer Wall", "█", destructible=False, wall_id=None))

    # Horisontella väggar (topp och botten)
    for j in range(1, grid.width - 1):
        grid.set(j, 0, Wall("Outer Wall", "█", destructible=False, wall_id=None))
        grid.set(j, grid.height - 1, Wall("Outer Wall", "█", destructible=False, wall_id=None))


def add_l_walls(grid):
    """Placerar ut 2 stycken L-formade innerväggar på fasta platser. Väggarna kan rivas med verktyg"""

    # Wall 1, rita ut höjd nedåt och längd vänster
    start_wall_1_x = 9
    start_wall_1_y = 3

    new_wall_id_11 = ("W1", "S1")
    for k in range(3):
        grid.set(start_wall_1_x, start_wall_1_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_11))
        start_wall_1_y += 1

    new_wall_id_12 = ("W1", "S2")
    for l in range(5):
        grid.set(start_wall_1_x, start_wall_1_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_12))
        start_wall_1_x -= 1

    # Wall 2, rita ut höjd nedåt och längd höger
    start_wall_2_x = 23
    start_wall_2_y = 5

    new_wall_id_21 = ("W2", "S1")
    for k in range(3):
        grid.set(start_wall_2_x, start_wall_2_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_21))
        start_wall_2_y += 1

    new_wall_id_22 = ("W2", "S2")
    for l in range(5):
        grid.set(start_wall_2_x, start_wall_2_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_22))
        start_wall_2_x += 1


def set_player(grid, player):
    """Placerar spelaren på mitten av spelvärlden"""
    grid.player = player
    player.pos_x = grid.width // 2
    player.pos_y = grid.height // 2


def place_items_from_list(grid, item_list, is_new=False):
    """Skapar instanser av objekt från mallar och placerar dem slumpmässigt i spelvärlden."""
    for template in item_list:
        if isinstance(template, Edible):
            spawned_item = Edible(name=template.name, symbol=template.symbol, points=template.points, is_new=is_new)

            # Original-ätbara saker räknas för att sedan veta när alla är upplockade
            if not spawned_item.is_new:
                grid.edibles_left += 1

        elif isinstance(template, (Trap, Chest)):
            spawned_item = type(template)(name=template.name, symbol=template.symbol, points=template.points)

        else:
            # Skapa nya objekt för övrigt som läggs ut på spelplanen
            spawned_item = type(template)(name=template.name, symbol=template.symbol)


        while True:
            # Slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, spawned_item)
                break


def randomize_items(grid, is_new):
    """Huvudfunktion som slumpmässigt placerar ut alla objekt i spelets värld, inklusive kistor och nycklar."""
    place_items_from_list(grid, edible_templates, is_new)
    place_items_from_list(grid,traps)
    place_items_from_list(grid,tools)
    place_items_from_list(grid,bombs)

    # Skapa 3 kistor och 3 matchande nycklar
    for i in range(3):
        key = Key(f"Key {i + 1}", "k")
        chest = Chest(f"Chest {i + 1}", "C", 100)  # Varje kista ger 100 poäng

        place_items_from_list(grid,[key])
        place_items_from_list(grid,[chest])


def set_exit(grid, player):
    """Placerar ut spelets utgång (E) på en ledig position."""
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y) and (x != player.pos_x or y != player.pos_y):
            new_exit = Exit()
            grid.set(x, y, new_exit)
            break
