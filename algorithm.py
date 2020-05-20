import numpy as np
import random
import matplotlib.pyplot as plt


GAME_X = 50
GAME_Y = 50
SENSE = 20
INITIAL_ENERGY = 4
INITIAL_POPULATION = 100
FOOD_PER_STEP = 20

MEAN = 0
SD = 1.0

class Rabbit:
    def __init__(self, speed, size):
        self.speed = speed
        self.size = size
        self.posx = GAME_X * np.random.rand()
        self.posy = GAME_Y * np.random.rand()
        self.energy_consumption = 0.5 * size**3 * speed**2
        self.energy_level = INITIAL_ENERGY
        self.vision = SENSE
    
    def mutate(self):
        new_speed = self.speed * 1.3 ** np.random.normal(MEAN, SD, 1)[0]
        new_size  = self.size * 1.3 ** np.random.normal(MEAN, SD, 1)[0]
        return Rabbit(new_speed, new_size)


class Food:
    def __init__(self):
        self.posx = GAME_X * np.random.rand()
        self.posy = GAME_Y * np.random.rand()
        self.available = True

def isclose(r, x, y, x_target, y_target):
    return r*r >= (x_target - x)**2 + (y_target - y)**2

def new_point(x, y, r):
    angle = np.random.rand() * 2 * np.pi
    dx = r * np.cos(angle)
    dy = r * np.sin(angle)
    newx = max(0, x + dx)
    newx = min(newx, GAME_X)
    newy = max(0, y + dy)
    newy = min(newy, GAME_Y)
    return newx, newy


class Game:
    def __init__(self, food_level, num_rabbits):
        self.rabbits = [Rabbit(1, 1) for i in range(num_rabbits)]
        self.foods = [Food() for i in range(food_level)]

    def clean(self):
        self.rabbits = list(filter(lambda x : x.energy_level > 0, self.rabbits))
        for f in self.foods:
            if (not f.available):
                f.posx = GAME_X * np.random.rand()
                f.posy = GAME_Y * np.random.rand()
                f.available = True

    def sort(self):
        self.rabbits.sort(key=lambda x: x.posx, reverse=True)

    def reproduce(self):
        new_rabbits = []
        for rabbit in self.rabbits:
            if rabbit.energy_level >= 2 * INITIAL_ENERGY:
                new_rabbit = rabbit.mutate()
                new_rabbits.append(new_rabbit)
                rabbit.energy_level = rabbit.energy_level - INITIAL_ENERGY
        self.rabbits = self.rabbits + new_rabbits
    
    def movement(self):
        planta = 0
        comidos = 0
        self.rabbits.sort(key=lambda x: x.size, reverse=True)
        for r in self.rabbits:
            if r.energy_level == 0:
                continue
            moved = False
            for f in self.foods:
                if moved:
                    break
                if isclose(r.vision, r.posx, r.posy, f.posx, f.posx) and f.available:
                    r.posx, r.posy = f.posx, f.posy
                    r.energy_level = r.energy_level + 1
                    f.available = False
                    moved = True
                    planta = planta + 1
                    break
            if moved:
                continue
            for presa in self.rabbits:
                if isclose(r.vision, r.posx, r.posy, presa.posx, presa.posy):
                    if(r.size >= 1.3 * presa.size):
                        r.energy_level = r.energy_level + presa.energy_level
                        presa.energy_level = 0
                        r.posx, r.posy = presa.posx, presa.posy
                        moved = True
                        comidos = comidos + 1
                        break
                    if not moved:        
                        r.posx, r.posy = new_point(r.posx, r.posy, r.vision)
                        moved = True
            r.energy_level = r.energy_level - r.energy_consumption
        # print("Plantas: ", planta, "  Comidos: ", comidos)
    


def main():
    game = Game(FOOD_PER_STEP, INITIAL_POPULATION)
    print("Initial state ")
    print("Population: ", len(game.rabbits))
    i = 1
    pop = len(game.rabbits)

    fig, axs = plt.subplots(3)
    fig.suptitle('Natural Selection Simulation')
    its = np.array([0])
    speeds = np.array([1.0])
    sizes = np.array([1.0])
    pops = np.array([INITIAL_POPULATION])
    axs[0].title.set_text("Average speed")
    axs[0].plot(its, speeds)
    axs[0].set_xlim([0, 100])
    axs[0].set_ylim([0, 5])
    
    axs[1].title.set_text("Average size")
    axs[1].plot(its, sizes)
    axs[1].set_xlim([0, 100])
    axs[1].set_ylim([0, 5])

    axs[2].title.set_text("Population")
    axs[2].plot(its, pops)
    axs[2].set_xlim([0, 100])
    axs[2].set_ylim([0, 1500])
    plt.draw()

    while pop > 0:
        plt.pause(0.5)
        game.movement()
        game.clean()
        game.reproduce()
        print("Iteration #", i)
        sum_speed = 0
        sum_size = 0
        for r in game.rabbits:
            sum_speed += r.speed
            sum_size += r.size
        print("    Population: ", pop, " Avg. speed: ", sum_speed/pop, " Avg. size: ", sum_size/pop)
        its = np.append(its, i)
        speeds = np.append(speeds,  sum_speed/pop)
        sizes = np.append(sizes,  sum_size/pop)
        pops = np.append(pops, pop)
        axs[0].plot(its, speeds)
        axs[1].plot(its, sizes)
        axs[2].plot(its, pops)
        plt.draw()
        i +=1
        pop = len(game.rabbits)

        
if __name__ == "__main__":
    main()