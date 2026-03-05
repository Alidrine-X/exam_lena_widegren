import random
import time
from src.entity import Entity, Wall, Key, Chest, Bomb, Edible, edible_templates, traps, tools, bombs, Exit

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg
    blast = "X"

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att
        # sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]
        self.edibles_left = 0

    def get(self, x, y):
        """Hämta det som finns på en viss position. Returnera vägg om det är utanför spelplanen"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]

        return Wall("Outer Wall", "█", destructible=False)

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    # Placera spelaren på mitten av spelplanen
    def set_player(self, player):
        self.player = player  # <--- LÄGG TILL DENNA RAD
        player.pos_x = self.width // 2
        player.pos_y = self.height // 2

    # Rensa på spelplanen från något som plockats upp och sätt empty
    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs

    def make_outer_walls(self):
        """Skapar oförstörbara ytterväggar runt hela spelplanen"""
        # Vertikala väggar (vänster och höger sida)
        for i in range(self.height):
            self.set(0, i, Wall("Outer Wall", "█", destructible=False, wall_id=None))
            self.set(self.width - 1, i, Wall("Outer Wall", "█", destructible=False, wall_id=None))

        # Horisontella väggar (topp och botten)
        for j in range(1, self.width - 1):
            self.set(j, 0, Wall("Outer Wall", "█", destructible=False, wall_id=None))
            self.set(j, self.height - 1, Wall("Outer Wall", "█", destructible=False, wall_id=None))

    def add_random_l_walls(self, count=2):
        """Placerar ut 2 stycken L-formade väggar på fasta platser."""

        # Wall 1, rita ut höjd nedåt och längd vänster
        start_wall_1_x = 9
        start_wall_1_y = 3

        new_wall_id_11 = ("W1", "S1")
        for k in range(3):
            self.set(start_wall_1_x, start_wall_1_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_11))
            start_wall_1_y += 1

        new_wall_id_12 = ("W1", "S2")
        for l in range(5):
            self.set(start_wall_1_x, start_wall_1_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_12))
            start_wall_1_x -= 1

        # Wall 2, rita ut höjd nedåt och längd höger
        start_wall_2_x = 23
        start_wall_2_y = 5

        new_wall_id_21 = ("W2", "S1")
        for k in range(3):
            self.set(start_wall_2_x, start_wall_2_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_21))
            start_wall_2_y += 1

        new_wall_id_22 = ("W2", "S2")
        for l in range(5):
            self.set(start_wall_2_x, start_wall_2_y, Wall("Inner Wall", "■", True, wall_id=new_wall_id_22))
            start_wall_2_x += 1

    # Används i filen entity.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)

    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""

        # Kolla yttre gränser (förhindra krasch)
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Kolla om väggar/items
        if self.data[y][x] != self.empty:
            return False

        # Kolla spelaren (om spelaren har skapats än)
        if hasattr(self, 'player') and self.player is not None:
            if x == self.player.pos_x and y == self.player.pos_y:
                return False  # Spelaren står här, alltså inte "empty"

        return True  # Hittade inget hinder!

    def print_status(self, score):
        """Visa spelvärlden och antal poäng."""
        print("--------------------------------------")
        print(f"You have {score} points.")
        print(self)

    def try_move_player(self, player, dx, dy, move_count):
        """
        Försöker flytta spelaren move_count steg i riktningen dx, dy.
        Returnerar True om flytten (och eventuella rivningar) genomfördes.
        """
        # Scanna vägen för hinder (1 eller 2 steg framåt)
        for i in range(1, move_count + 1):
            check_x = player.pos_x + (dx * i)
            check_y = player.pos_y + (dy * i)
            item = self.get(check_x, check_y)

            if isinstance(item, Wall):
                # Försök riva väggen. Om det misslyckas stannar vi helt.
                if not item.try_to_demolish(player, self):
                    return False

        # Om vi kom hit är vägen fri (eller röjd). Genomför flytten.
        player.pos_x += (dx * move_count)
        player.pos_y += (dy * move_count)

        # Uppdatera poäng och bördig jord för varje steg som tagits
        for _ in range(move_count):
            player.move_points()

        # Interagera med det som finns på slutdestinationen
        final_item = self.get(player.pos_x, player.pos_y)
        if isinstance(final_item, Entity):
            final_item.interact(player, self, player.pos_x, player.pos_y)

        # Uppdatera världen med nytt ätbart tack vare bördig jord
        self.update_world(player)

        return True


    def place_items_from_list(self, item_list, is_new=False):
        for template in item_list:
            if isinstance(template, Edible):
                # Skapa nya objekt för Edibles som läggs ut på spelplanen
                spawned_item = type(template)(name=template.name, symbol=template.symbol, points=template.points, is_new=is_new)

                # Original-ätbara saker räknas för att sedan veta när alla är upplockade
                if not spawned_item.is_new:
                    self.edibles_left += 1

            else:
                # Skapa nya objekt för övrigt som läggs ut på spelplanen
                spawned_item = type(template)(name=template.name, symbol=template.symbol, points=template.points)


            while True:
                # Slumpa en position tills vi hittar en som är ledig
                x = self.get_random_x()
                y = self.get_random_y()
                if self.is_empty(x, y):
                    self.set(x, y, spawned_item)
                    break

    def randomize_items(self, is_new):
        """Huvudfunktion som placerar ut allt i spelet."""
        self.place_items_from_list(edible_templates, is_new)
        self.place_items_from_list(traps)
        self.place_items_from_list(tools)
        self.place_items_from_list(bombs)

        # Skapa 3 kistor och 3 matchande nycklar
        for i in range(3):
            key = Key(f"Key {i + 1}", "k", 0)
            chest = Chest(f"Chest {i + 1}", "C", 100)  # Varje kista ger 100 poäng

            self.place_items_from_list([key])
            self.place_items_from_list([chest])

    def spawn_random_edible(self, is_new):
        """Väljer ut EN slumpmässig grönsak från listan och placerar på griden."""
        # Välj ett objekt-template från den importerade listan 'edible_templates'
        new_edible = random.choice(edible_templates)

        # Skicka föremålet i en lista för utplacering i grid
        self.place_items_from_list([new_edible], is_new)

        # Returnera namnet så att game_new.py kan skriva ut det
        return new_edible.name

    # När spelaren tagit 25 steg läggs något nytt ätbart till
    # Det markeras att det är nytt med is_new
    def update_world(self, player):
        if player.fertile_soil >= 25:
            is_new = True
            name = self.spawn_random_edible(is_new)
            print(f"🌱 A new {name} grew from the fertile soil!")
            player.fertile_soil -= 25

    def detonate_bomb(self, player):
        for y in range(self.height):
            for x in range(self.width):

                # Bomben har hittats, rensa 3 x 3 rutor
                if isinstance(self.get(x, y), Bomb):
                    print("\n💥 TICK... TICK... BOOM!")

                    # Rita ut explosionen först i 3x3
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            self.set(x + dx, y + dy, self.blast)

                    print(self)  # Skriv ut grid så spelaren ser explosionen
                    time.sleep(0.5)  # Pausa i en halv sekund så man hinner se!

                    # Faktisk rensning i 3x3
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            self.clear(x + dx, y + dy)

                    # Spelaren stod i vägen
                    if abs(player.pos_x - x) <= 1 and abs(player.pos_y - y) <= 1:
                        print("Aargh! You got caught in the blast wave!")
                        player.score -= 20  # Eller dör spelaren direkt?

                    return  # Vi hittade och sprängde bomben, vi kan sluta leta

    def set_exit(self, player):
        while True:
            # Slumpa en position tills vi hittar en som är ledig
            x = self.get_random_x()
            y = self.get_random_y()
            if self.is_empty(x, y) and (x != player.pos_x or y != player.pos_y):
                new_exit = Exit()
                self.set(x, y, new_exit)
                break
