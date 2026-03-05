class Entity:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def interact(self, player, grid, target_x, target_y):
        """Standardinteraktion: gör ingenting"""
        pass

    def __str__(self):
        return self.symbol

# Ätbart som plockas upp och läggs i inventory och ger spelare gratis steg
class Edible(Entity):
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
        print(f"You found a {self.name} and got {self.points} points!")


# Verktyg som plockas upp läggs i inventory och kan användas till att ta bort innervägg
# Den tas bort när den använts
class Tool(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points
        self.can_dig = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)  # Tas bort från grid
        print(f"You found a {self.name} but got no extra points")


# Fälla som ger minuspoäng varje gång spelaren går på rutan
class Trap(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        player.score -= self.points
        print(f"Oh no, you accidentally fell into a {self.name} and got -{self.points} points.")

    def disarm(self, grid, x, y):
        grid.clear(x, y)  # Tas bort från grid
        print(f"You successfully disarmed the {self.name}")

# Skattkista som ger poäng om spelare öppnar den med en nyckel
# Den tas bort när den öppnas
class Chest(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points

    def interact(self, player, grid, target_x, target_y):
        # Leta efter första saken som kan låsa upp kistan (oberoende av namn!)
        key = next((i for i in player.inventory if getattr(i, 'can_unlock', False)), None)

        if key:
            print("You unlocked the chest!")
            player.score += self.points
            player.inventory.remove(key) # Nyckeln försvinner efter användning
            grid.clear(target_x, target_y)
        else:
            print("The chest is locked. You need a key!")


# Nyckel som plockas upp och läggs i inventory och kan låsa upp en kista
# Den tas bort när den använts
class Key(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points
        self.can_unlock = True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        player.grace_period = 5
        grid.clear(target_x, target_y)
        print("You found a key!")


# Två typer av väggar, yttervägg som inte kan krossas och innervägg som
# kan tas bort med en spade
class Wall(Entity):
    def __init__(self, name="Wall", symbol="■", destructible=False, wall_id=None):
        super().__init__(name, symbol)
        self.destructible = destructible
        self.wall_id = wall_id

    def interact(self, player, grid, target_x, target_y):
        pass

    def try_to_demolish(self, player, grid):
        # Om väggen inte kan förstöras (yttervägg)
        if not self.destructible:
            print("This wall is too massive to move.")
            return False  # Hindra flytt

        # Om det är en innervägg, leta efter spade (Tool)
        shovel = next((i for i in player.inventory if getattr(i, 'can_dig', False)), None)

        if shovel:
            print(f"You used your {shovel.name} and tore down the entire wall!")

            # Spara väggens ID före rivning av vägg
            target_id = self.wall_id

            # Loopa igenom hela grid:en och ta bort alla väggbitar med samma ID
            for y in range(grid.height):
                for x in range(grid.width):
                    target_item = grid.get(x, y)

                    # Kolla om objektet är en vägg och har rätt ID
                    if isinstance(target_item, Wall) and target_item.wall_id == target_id:
                        grid.clear(x, y)

            player.inventory.remove(shovel)
            return True
        else:
            print("You need a shovel to get through the wall.")
            return False

# Bomb som plockas upp och läggs i inventory och spränger 3 x 3 rutor
# Den tas bort när den placerats ut
class Bomb(Entity):
    def __init__(self, name, symbol, points):
        super().__init__(name, symbol)
        self.points = points
        self.can_explode= True

    def interact(self, player, grid, target_x, target_y):
        player.inventory.append(self)
        grid.clear(target_x, target_y)
        print(f"You found a {self.name}! Press B to use it")

class Exit(Entity):
    def __init__(self, name= "Portal", symbol= "E"):
        super().__init__(name, symbol)

    def interact(self, player, grid, target_x, target_y):
        if grid.edibles_left > 0:
            print(f" You can't exit when there are {grid.edibles_left} original edibles left.")
            return False
        else:
            print("Congratulations! You found the exit and won the game!")
            return True


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
    Tool("shovel", "!", 0),
    Tool("spade", "!", 0)
]

bombs = [
    Bomb("bomb", "B", 0)
]
