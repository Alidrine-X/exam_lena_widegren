"""
player.py

Definierar Player-klassen för Fruit Loop.

Håller reda på spelarens position, poäng, inventory, grace-period, bomb-timer
och bördighet. Innehåller metoder för förflyttning, steg-uppdatering,
visning av inventory och kontroll av om spelaren lever.
"""

#==============================================================================

class Player:
    marker = "@"    # Symbol som representerar spelaren i spelvärlden

    def __init__(self, x=None, y=None):
        """Initierar spelarens position, poäng, timers och inventory."""
        self.pos_x = x
        self.pos_y = y
        self.score = 10
        self.grace_period = 0
        self.fertile_soil = 0
        self.bomb_timer = 0
        self.inventory = []


    def move(self, dx, dy):
        """Flyttar spelaren dx steg horisontellt och dy steg vertikalt."""
        self.pos_x += dx
        self.pos_y += dy


    def move_points(self):
        """Uppdaterar poäng, grace-period och bördig jord per utfört steg."""
        if self.grace_period > 0:
            self.grace_period -= 1
        else:
            self.score -= 1

        self.fertile_soil += 1

        if self.bomb_timer > 0:
            self.bomb_timer += 1


    def show_inventory(self):
        """Visar spelarens innehåll i inventory med kommando I"""
        if not self.inventory:
            print(f"\nYour inventory is empty")
            return

        item_names = ', '.join([item.name for item in self.inventory])
        print(f"\nYour inventory: {item_names}")


    def is_alive(self):
        """Returnerar True om spelaren har poäng kvar."""
        return self.score > 0
