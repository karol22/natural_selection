import numpy as np
import random
GAME_X = 100
GAME_Y = 100
SENSE = 5

class Rabbit:
    def __init__(self, speed, size):
        self.speed = speed
        self.size = size
        self.posx = GAME_X * np.random.rand()
        self.posy = GAME_Y * np.random.rand()
        self.energy_consumption = size**3 * speed**2
        self.energy_level = 10
        self.vision = 5
    
    def mutate(self):
        new_speed = self.speed * 1.3 ** (2 * np.random.rand() - 1)
        new_size  = self.size * 1.3 ** (2 * np.random.rand() - 1)
        return Rabbit(new_speed, new_size)


class Food:
    def __init__(self, amount):
        self.posx = GAME_X * np.random.rand()
        self.posy = GAME_Y * np.random.rand()

def isclose(r, x, y, x_target, y_target):
    return r*r >= (x_target - x)**2 + (y_target - y)**2

def new_point(x, y, r):
    angle = np.random.rand() * 2 * np.pi
    dx = np.cos(angle)
    dy = np.sin(angle)
    newx = max(0, dx)
    newx = min(newx, GAME_X)
    newy = max(0, dy)
    newy = min(newy, GAME_Y)
    return newx, newy


class Game:
    def __init__(self, food_level, num_rabbits):
        self.rabbits = [Rabbit(i, i) for i in range(num_rabbits)]
        self.foods = [Food(food_level) for i in range(food_level)]

    def clean(self):
        self.rabbits = list(filter(lambda x : x.speed != 0, self.rabbits))

    def sort(self):
        self.rabbits.sort(key=lambda x: x.posx, reverse=True)

    def reproduce(self):
        new_rabbits = []
        for rabbit in rabbits:
            if rabbit.energy_level >= 2 * rabbit.energy_consumption:
                new_rabbit = Rabbit(rabbit.speed, rabbit.size)
                new_rabbits.append(new_rabbit)
        self.rabbits.append(new_rabbits)
    
    def movement(self):
        for r in self.rabbits:
            if r.energy_level == 0:
                continue
            moved = False
            for f in self.foods:
                if moved:
                    break
                if isclose(r.vision, r.posx, r.posy, f.posx, f.posx):
                    r.posx, r.posy = f.posx, f.posy
                    r.energy_level = r.energy_level + 1
                    break
                else:
                    for presa in self.rabbits:
                        if isclose(r.vision, r.posx, r.posy, presa.posx, presa.posy):
                            if(r.size >= 1.3 * presa.size):
                                r.energy_level = r.energy_level + presa.energy_level
                                presa.energy_level = 0
                                r.posx, r.posy = presa.posx, presa.posy
                                moved = True
                                break
                    r.posx, r.posy = new_point(r.posx, r.posy, r.vision)
                    moved = True
    


def main():
    game = Game(10, 10)
    game.movement()
    print(game.rabbits)
    """
    for r in game.rabbits:
        print(r.speed, r.size, r.posx, r.posy)
    print("update")
    game.update()
    for r in game.rabbits:
        print(r.speed, r.size, r.posx, r.posy)

    print("sort by posx")
    game.sort()
    for r in game.rabbits:
        print(r.speed, r.size, r.posx, r.posy)
    
    print("shuffle")
    random.shuffle(game.rabbits)
    for r in game.rabbits:
        print(r.speed, r.size, r.posx, r.posy)
    """
        
if __name__ == "__main__":
    main()