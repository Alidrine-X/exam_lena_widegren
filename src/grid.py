"""
Grid.py

Startpunkt för spelets rutnät och objekts-hantering, inklusive spelarposition
och föremål.

Initierar och lagrar spelets rutnät med tomma rutor (= en punkt "."), väggar
och objekt. Håller reda på spelarens position, placerade föremål och antalet
ursprungliga ätbara saker. Innehåller metoder för att läsa och skriva till
rutor, kontrollera lediga rutor samt visa spelets status.
"""

#==============================================================================

import random
from src.objects import Wall

class Grid:
    """Representerar spelvärlden med rutnät, väggar, objekt och spelarposition
    samt metoder för interaktion med rutorna."""
    width = 36
    height = 12
    empty = "."
    wall = "■"
    blast = "X"


    def __init__(self):
        """Initierar spelvärlden, lagrar tomma rutor och förbereder spelaren och poängräkning."""
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]
        self.player = None
        self.edibles_left = 0


    def __str__(self):
        """Returnerar en sträng som visar hela spelvärlden med objekt och spelaren."""
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


    def get(self, x, y):
        """Returnerar objektet på en given position, eller en vägg om positionen är utanför spelvärlden."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]

        return Wall("Outer Wall", "█", destructible=False)


    def set(self, x, y, value):
        """Sätter ett objekt på angiven position i spelvärlden."""
        self.data[y][x] = value


    def clear(self, x, y):
        """Tar bort objekt från positionen och markerar rutan som tom."""
        self.set(x, y, self.empty)


    def print_status(self, score):
        """Skriver ut hela spelvärlden och spelarens aktuella poäng."""
        print("--------------------------------------")
        print(f"You have {score} points.")
        print(self)


    def get_random_x(self):
        """Returnerar en slumpad x-position i spelvärlden."""
        return random.randint(0, self.width-1)


    def get_random_y(self):
        """Returnerar en slumpad y-position i spelvärlden."""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Returnerar True om rutan är tom, inom spelvärldens gränser, och spelaren inte står där."""

        # Kolla yttre gränser av grid
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Kolla om väggar/items
        if self.data[y][x] != self.empty:
            return False

        # Kolla om spelaren står här, alltså inte "empty"
        if self.player is not None and x == self.player.pos_x and y == self.player.pos_y:
                return False

        return True  # Hittade inget hinder
