"""
objects.py

Definierar alla spelobjekt i Fruit Loop; ätbart, verktyg, fällor, nycklar,
kistor, väggar och utgång. Varje klass hanterar sin egen interaktion
med spelaren och spelvärlden.
"""

#==============================================================================

class Entity:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def interact(self, player, grid, target_x, target_y):
        """Standardinteraktion: gör ingenting"""
        pass

    def __str__(self):
        return self.symbol


class Edible(Entity):
    """Ätbart plockas upp, läggs i inventory och ger spelare gratis steg (grace_period)."""
    def __init__(self, name, symbol, points, is_new=True):
        super().__init__(name, symbol)
        self.points = points
        self.is_new = is_new

    def interact(self, player, grid, target_x, target_y):
        player.score += self.points
        player.inventory.append(self)

        if not self.is_new:
            grid.edibles_left -= 1

        player.grace_period = 5
        grid.clear(target_x, target_y)  # Tas bort från grid
        print(f"\nYou found a {self.name} and got {self.points} points!")


class Tool(Entity):
    """Verktyg plockas upp, läggs i inventory och kan användas till att ta
    bort innervägg. Verktyget tas bort när det använts"""
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.can_dig = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)  # Tas bort från grid
        print(f"\nYou found a {self.name} but got no extra points")


class Bomb(Entity):
    """Bomb plockas upp, läggs i inventory och kan spränga 3 x 3 rutor. Bomben
    tas bort från inventory när den placerats ut och sätts till placed
    för att inte kunna plockas upp igen"""
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.can_explode= True
        self.placed = False

    def interact(self, player, grid, target_x, target_y):
        if not self.placed:
            player.inventory.append(self)
            grid.clear(target_x, target_y)
            print(f"\nYou found a {self.name}! Press B to use it")
        else:
            # Bomben är redan placerad, spelaren kan inte plocka upp den
            print(f"\nThe bomb is already placed! You can't pick it up.")


class Key(Entity):
    """Nyckel plockas upp, läggs i inventory och kan låsa upp en kista.
    Nyckeln tas bort från inventory när den använts"""
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.can_unlock = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)
        print("\nYou found a key!")


class Chest(Entity):
    """Skattkista ger poäng när spelare öppnar den med en nyckel. Kistan
    tas bort när den öppnats"""
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        # Leta efter första saken som kan låsa upp kistan (oberoende av namn!)
        key = next((i for i in player.inventory if getattr(i, 'can_unlock', False)), None)

        if key:
            print("\nYou unlocked the chest!")
            player.score += self.points
            player.inventory.remove(key) # Nyckeln försvinner efter användning
            grid.clear(target_x, target_y)
        else:
            print("\nThe chest is locked. You need a key!")


class Trap(Entity):
    """Fälla ger minuspoäng varje gång spelaren går på rutan. Fälla kan tas
    bort med kommando T"""
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        player.score -= self.points
        print(f"\nOh no, you accidentally fell into a {self.name} and got -{self.points} points.")

    def disarm(self, grid, x, y):
        grid.clear(x, y)  # Tas bort från grid
        print(f"\nYou successfully disarmed the {self.name}")


class Wall(Entity):
    """Två typer av vägg skapas, yttervägg som inte kan krossas och innervägg som
    kan tas bort med hjälp av en spade"""
    def __init__(self, name="Wall", symbol="■", destructible=False, wall_id=None):
        super().__init__(name, symbol)
        self.destructible = destructible
        self.wall_id = wall_id

    def interact(self, player, grid, target_x, target_y):
        pass

    # Försöker gå in eller hoppa över en vägg.
    def try_to_demolish(self, player, grid):
        # Om väggen inte kan förstöras (yttervägg)
        if not self.destructible:
            print("\nThis wall is too massive to move.")
            return False  # Hindra flytt

        # Om det är en innervägg, leta efter spade (Tool)
        shovel = next((i for i in player.inventory if getattr(i, 'can_dig', False)), None)

        if shovel:
            print(f"\nYou used your {shovel.name} and tore down the entire wall!")

            # Spara väggens ID före rivning av vägg
            target_id = self.wall_id

            # Loopa igenom hela spelvärlden och ta bort alla väggbitar med samma ID
            for y in range(grid.height):
                for x in range(grid.width):
                    target_item = grid.get(x, y)

                    # Kolla om objektet är en vägg och har rätt ID
                    if isinstance(target_item, Wall) and target_item.wall_id == target_id:
                        grid.clear(x, y)

            player.inventory.remove(shovel)
            return True
        else:
            print("\nYou need a shovel to get through the wall.")
            return False


class Exit(Entity):
    """Avslutar spelet med kommando E om alla ursprungliga ätbara saker är upplockade"""
    def __init__(self, name= "Portal", symbol= "E"):
        super().__init__(name, symbol)

    def interact(self, player, grid, target_x, target_y):
        if grid.edibles_left > 0:
            print(f"\nYou can't exit when there are {grid.edibles_left} original edibles left.")
            return False
        else:
            print("\nCongratulations! You found the exit and won the game!")
            return True


# Mallar för slumpmässig placering i spelvärlden, används av builder.py
edible_templates = [
    Edible("carrot", "?", 20, False),
    Edible("apple", "?", 20, False),
    Edible("strawberry", "?", 20, False),
    Edible("cherry", "?", 20, False),
    Edible("watermelon", "?", 20, False),
    Edible("radish", "?", 20, False),
    Edible("cucumber", "?", 20, False),
    Edible("meatball", "?", 20, False)
]

traps = [
    Trap("snare", "¤", 10),
    Trap("maple door", "¤", 10),
    Trap("quicksand", "¤", 10),
    Trap("bear shears", "¤", 10),
    Trap("floor hatch", "¤", 10),
    Trap("fishing net", "¤", 10),
    Trap("fire", "¤", 10)
]

tools = [
    Tool("shovel", "!"),
    Tool("spade", "!")
]

bombs = [
    Bomb("bomb", "B")
]
