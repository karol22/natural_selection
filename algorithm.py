import numpy as np
import random
import matplotlib.pyplot as plt


GAME_X = 50
GAME_Y = 50
SENSE = 20
INITIAL_ENERGY = 20
INITIAL_POPULATION = 100
FOOD_PER_STEP = 100
NUM_ITERATIONS = 100

MEAN = 0
SD_SIZE = 0.2
SD_SPEED = 0.2

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
        new_speed = self.speed * 2 ** np.random.normal(MEAN, SD_SPEED, 1)[0]
        new_size  = self.size * 2 ** np.random.normal(MEAN, SD_SIZE, 1)[0]
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
            new_speed = rabbit.speed * 2 ** np.random.normal(MEAN, SD_SPEED, 1)[0]
            new_size  = rabbit.size * 2 ** np.random.normal(MEAN, SD_SIZE, 1)[0]
            rabbit.speed = new_speed
            rabbit.size = new_size
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
            if r.energy_level <= 0:
                continue
            moved = False
            for f in self.foods:
                if moved:
                    break
                if isclose(r.vision, r.posx, r.posy, f.posx, f.posx) and f.available:
                    ddx = f.posx - r.posx
                    ddy = f.posy - r.posy
                    dist = np.sqrt(ddx**2 + ddy**2)
                    prop = 1 if r.speed >= dist else r.speed/dist
                    r.posx, r.posy = r.posx + prop * ddx, r.posy + prop * ddy
                    if(prop == 1):
                        r.energy_level = r.energy_level + 1
                        f.available = False
                        planta = planta + 1
                    moved = True
                    break
            if moved:
                continue
            for presa in self.rabbits:
                if isclose(r.vision, r.posx, r.posy, presa.posx, presa.posy):
                    if(r.size >= 1.3 * presa.size):
                        ddx = presa.posx - presa.posx
                        ddy = presa.posy - presa.posy
                        dist = np.sqrt(ddx**2 + ddy**2)
                        prop = 1 if r.speed >= dist else r.speed/dist
                        r.posx, r.posy = r.posx + prop * ddx, r.posy + prop * ddy
                        if(prop == 1):
                            r.energy_level = r.energy_level + presa.energy_level
                            presa.energy_level = 0
                            f.available = False
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

    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Natural Selection Simulation')
    its = np.array([0])
    speeds = np.array([1.0])
    sizes = np.array([1.0])
    pops = np.array([INITIAL_POPULATION])

    xc = np.array([r.posx for r in game.rabbits])
    yc = np.array([r.posy for r in game.rabbits])
    ss = np.array([r.size for r in game.rabbits])

    xp = np.array([r.posx for r in game.foods])
    yp = np.array([r.posy for r in game.foods])

    axs[0][0].title.set_text("\n\nDistribution")
    axs[0][0].scatter(xc, yc, s=ss, color='r')
    axs[0][0].scatter(xp, yp, marker='^', s=1.0, color = 'g')
    axs[0][0].set_xlim([0, GAME_X])
    axs[0][0].set_ylim([0, GAME_Y])

    axs[0][1].plot(its, speeds, 'b')
    axs[0][1].set_xlim([0, 100])
    axs[0][1].set_xlabel('Iterations')
    axs[0][1].set_ylabel('Avg. speed')
    axs[0][1].set_ylim([0, 3])
    
    axs[1][0].plot(its, sizes, 'g')
    axs[1][0].set_xlim([0, 100])
    axs[1][0].set_ylim([0, 5])
    axs[1][0].set_xlabel('Iterations')
    axs[1][0].set_ylabel('Avg. size')

    axs[1][1].plot(its, pops, 'r')
    axs[1][1].set_xlim([0, 100])
    axs[1][1].set_ylim([0, 500])
    axs[1][1].set_xlabel('Iterations')
    axs[1][1].set_ylabel('Population')
    plt.draw()

    while pop > 0:
        plt.pause(0.5)
        game.movement()
        game.clean()
        game.reproduce()
        print("Iteration #", i)
        sum_speed = 0
        sum_size = 0
        if len(game.rabbits) == 0:
            break
        for r in game.rabbits:
            sum_speed += r.speed
            sum_size += r.size
        print("    Population: ", pop, " Avg. speed: ", sum_speed/pop, " Avg. size: ", sum_size/pop)
        its = np.append(its, i)
        speeds = np.append(speeds,  sum_speed/pop)
        sizes = np.append(sizes,  sum_size/pop)
        pops = np.append(pops, pop)
        xc = np.array([r.posx for r in game.rabbits])
        yc = np.array([r.posy for r in game.rabbits])
        ss = np.array([r.size for r in game.rabbits])
        xp = np.array([r.posx for r in game.foods])
        yp = np.array([r.posy for r in game.foods])
        axs[0][0].clear()
        axs[0][0].scatter(xc, yc, s=ss*5, color='r')
        axs[0][0].scatter(xp, yp, marker='^', s=1.0, color = 'g')

        axs[0][1].plot(its, speeds, 'b')
        axs[0][1].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[0][1].set_ylim([0, max(3, sum_speed/pop + 1)])

        axs[1][0].plot(its, sizes, 'g')
        axs[1][0].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[1][0].set_ylim([0, max(3, sum_size/pop + 1)])

        axs[1][1].plot(its, pops, 'r')
        axs[1][1].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[1][1].set_ylim([0, max(500, pop + 100)])
        plt.draw()
        i +=1
        pop = len(game.rabbits)

        
if __name__ == "__main__":
    main()