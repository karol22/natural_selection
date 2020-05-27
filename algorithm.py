import numpy as np
import random
import matplotlib.pyplot as plt
from svgpath2mpl import parse_path


GAME_X = 50
GAME_Y = 50
SENSE = 20
INITIAL_ENERGY = 4
INITIAL_POPULATION = 10
FOOD_PER_STEP = 50
NUM_ITERATIONS = 200

MEAN = 0
SD_SIZE = 0.5
SD_SPEED = 0.5

class Rabbit:
    def __init__(self, speed, size, energy = INITIAL_ENERGY):
        self.speed = speed
        self.size = size
        self.posx = GAME_X * np.random.rand()
        self.posy = GAME_Y * np.random.rand()
        self.energy_consumption = 0.5 * size**3 * speed**2 
        self.energy_level = energy
        self.vision = SENSE
        if(self.energy_consumption > self.energy_level):
            self.energy_level = 0
        if(self.size < 0.1):
            self.energy_level = 0
        if(self.speed**2 > 2500):
            self.energy_level = 0
    
    def mutate(self, energy = INITIAL_ENERGY):
        new_speed = self.speed * 2 ** np.random.normal(MEAN, SD_SPEED, 1)[0]
        new_size  = self.size * 2 ** np.random.normal(MEAN, SD_SIZE, 1)[0]
        if new_speed > np.sqrt(2500) or new_size<0.1:
            energy = 0
        return Rabbit(new_speed, new_size, energy)


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
        self.rabbits = list(filter(lambda x : x.speed < np.sqrt(2500), self.rabbits))
        self.rabbits = list(filter(lambda x : x.size < np.sqrt(25), self.rabbits))
        self.rabbits = list(filter(lambda x : x.size > 0.1, self.rabbits))
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
            r.energy_level = r.energy_level - r.energy_consumption
            moved = False
            closex = 1000
            closey = 1000
            closef = Food()
            for f in self.foods:
                if (r.posx - f.posx)**2 + (r.posy - f.posy)**2 < (r.posx - closex)**2 + (r.posy - closey)**2 and f.available:
                    closex = f.posx
                    closey = f.posy
                    closef = f

            for f in self.foods:
                if moved:
                    break
                if  closef.available:
                    ddx = closef.posx - r.posx
                    ddy = closef.posy - r.posy
                    dist = np.sqrt(ddx**2 + ddy**2)
                    prop = 1 if r.speed >= dist else r.speed/dist
                    r.posx, r.posy = r.posx + prop * ddx, r.posy + prop * ddy
                    if(prop == 1):
                        r.energy_level = r.energy_level + 1
                        closef.available = False
                    r = r.mutate(energy = r.energy_level)
                    moved = True
                    break
            if moved:
                continue
            for presa in self.rabbits:
                if isclose(r.vision, r.posx, r.posy, presa.posx, presa.posy):
                    if(r.size**3 >= 2 * presa.size):
                        ddx = presa.posx - presa.posx
                        ddy = presa.posy - presa.posy
                        dist = np.sqrt(ddx**2 + ddy**2)
                        prop = 1 if r.speed >= dist else r.speed/dist
                        r.posx, r.posy = r.posx + prop * ddx, r.posy + prop * ddy
                        if(prop == 1):
                            r.energy_level = r.energy_level + presa.energy_level
                            presa.energy_level = 0
                        r = r.mutate(energy = r.energy_level)
                        moved = True
                        break
            if not moved:        
                r.posx, r.posy = new_point(r.posx, r.posy, r.vision)
                moved = True
                r = r.mutate(energy = r.energy_level)
    


def main():
    popu = input("Enter a number for the initial population: ")
    if popu != '':
        INITIAL_POPULATION = int(popu)
    food = input("Enter a number for the food amount: ")
    if food != '':
        FOOD_PER_STEP = int(food)

    smiley = parse_path("""m393.56 121.87c6.883 57.336 2.6723 121.13 35.926 170.34 17.542 13.456 62.225 56.831 57.208 52.071-18.748-44.024-77.104-55.949-75.103-110.81-8.1597-36.772-13.133-74.222-18.031-111.6zm258.19 346.34c-25.172 3.8064-43.674 44.382-41.886 55.706 7.3239-23.655 23.896-40.531 41.886-55.706zm-628.48 236.06c1.779 20.66 55.921 56.37 25.998 18.91-10.007-4.34-20.943-7.66-25.998-18.91zm45.023-12.577c2.8411-44.7-70.653-30.773-46.861 9.6744-3.9793-28.688 30.631-43.155 39.51-12.577l7.3507 2.9023zm-2.7565 119.96c2.3865 41.699-53.947 63.222-33.186 105.86 30.943 17.882 76.078 10.378 107.03-7.3432 8.2848-15.315-34.813-45.901-17.566-7.9225-13.758 23.693-80.078 38.098-87.155-2.7965 4.2562-31.694 41.913-53.324 30.874-87.795zm66.156 29.023c-10.25 14.102-19.063 25.796-7.1236 2.7267 2.8604-5.3701 2.6104-10.988 7.1236-2.7267zm207.66 3.8698c0.10805 20.197 48.73 38.927 5.714 23.46-10.022-3.2245-8.1687-66.87-5.714-23.46zm-79.224 1.8175c17.476 47.579 73.365 51.482 114.64 45.424 21.664 0.32891 33.078-2.7175 5.9334-9.5109-35.39-9.8535-77.152 21.652-104.05-19.24-5.7071-5.3332-11.227-10.89-16.525-16.673zm-105.46-21.166c52.091 14.482 108.47 26.319 160.45 4.6811 18.44-8.6743 86.769 6.6037 35.108-6.6811-39.866-10.145-76.69 23.706-117.45 13.609-23.992-15.492-51.022-13.599-78.101-11.609zm-85.462-23.21c16.225 37.805 66.334 46.794 89.592 10.471 28.99-35.062 25.359-85.807 25.263-129.47-5.7022 48.939-3.6284 108.83-47.171 140.06-20.745 21.153-53.474-3.4394-67.684-21.061zm358.35-316.36c-26.633 38.951-76.761 14.479-114.86 20.082-53.729-0.18419-114.27 4.9813-156.34 44.029-38.69 41.413-79.154 88.349-83.171 149.35-2.4552 26.699-23.629 74.632-5.0694 86.287-3.5256-63.348 14.314-130.19 60.674-173.36 22.343-26.773 29.813-68.139 68.135-77.049 45.879-26.301 100.76-25.525 149.82-10.855 27.955-4.0489 68.894-6.3497 80.81-38.485zm-33.078 185.75c-3.8182 37.825-45.265 65.234-30.347 105.17 13.655 50.865 50.914 91.342 58.831 144.43-0.4057 45.737 66.402 36.231 77.402 40.446-21.81-1.95-44.821 0.094-65.905-4.2674-32.855-24.739-15.67-76.715-47.536-106.21-6.9482-40.395-59.634-73.978-32.308-116.53 15.362-19.857 32.587-37.348 39.862-63.036zm121.29 118.03c-0.70143 42.665-0.30714 84.337 29.941 115.4 26.344 31.299-46.398 25.741-23.943 17.394 48.709 3.6859-1.676-49.392-16.105-65.076-4.2605-22.855 3.6789-46.167 10.107-67.721zm117.61-203.16c-9.4695 36.014-34.54 65.621-37.672 103.52-11.797 42.405-43.455 77.827-81.651 94.839-25.707 24.103-50.175 65.14-30.448 101.55 12.467 18.843 52.034 58.287 24.809 75.46 14.667-34.528-32.45-67.328-36.754-103.52-1.2462-33.461 19.368-75.797 52.418-83.633 29.313-24.19 55.311-58.737 69.692-95.178 8.1985-32.848 22.838-64.132 39.605-93.04zm-178.81-54.45c44.497 4.2194 60.999 58.973 106.78 57.263 17.486 8.0092 65.897-5.9 68.718-11.967-36.328 12.991-79.046 17.746-110.81-10.008-16.987-20.464-39.093-32.335-64.69-35.288zm1.2994-120.4c-12.148 34.838-35.277 72.496-16.243 110.14-13.036-40.451 14.143-71.135 16.243-110.14zm265.08 68.408c11.202 35.178-3.7535 93.91-47.429 86.879 38.743-1.4054 54.588-46.163 47.429-86.879zm-24.689 45.15c-2.4701 42.009-73.335 69.767-89.021 26.3-3.7224-18.608-2.3143-34.275 3.258-6.4616 9.4696 43.394 72.236 23.093 81.566-11.65l2.2264-4.2318 1.9702-3.9568zm-12.99-36.26c4.2188 15.197 16.913 44.427 22.74 15.734 13.973-21.717-2.3182-28.987-2.8756-0.60572-7.4118 0.36253-6.6809-24.037-19.865-15.128zm-134.49-69.78c24.268-21.52 48.605 1.794 46.555 29.035-0.30079 9.3188-56.727 7.4693-46.223-25.884l-0.24174-2.2906-0.0908-0.86038zm70.819-80.722c43.202 14.292 84.891 48.194 81.63 100.75 3.7943 15.514 31.308 51.742 5.5141 19.827-15.121-36.903-19.906-86.563-60.515-106.37-8.6542-5.1775-17.565-9.8761-26.63-14.203zm-242.99-227.8c-25.415 56.737-7.7583 123.68 15.628 177.76 12.96 33.069 45.755 50.476 59.74 82.187-13.773 19.31 18.29 44.873 11.362 15.432-8.7537-22.412-25.288-48.91-46.241-68.101-46.6-55.559-57.402-136.92-40.488-207.28zm263.14 24.627c-27.434 53.628-37.779 115.57-40.977 175.79-3.1467 19.457 27.096 34.082-1.2549 15.75-8.13-32.197 2.1381-66.874 7.1827-99.22 7.4559-32.445 11.338-67.597 35.049-92.324zm-105.26 119.71c3.7907-43.752 26.968-81.963 60.729-107.08 17.945-11.8 54.56-68.89 67.676-39.261 3.1839 24.473-33.915 31.388-10.99 6.3001 22.531-34.387-30.465 7.4727-34.901 21.012-31.459 22.909-58.392 52.983-71.372 91.55-3.8901 9.0796-7.6122 18.24-11.142 27.481zm16.243 76.617c-17.213-31.902-15.864-73.212-23.155-109.5-0.60121-13.697-24.361-54.359-8.9119-18.997 13.304 41.835 10.159 90.586 27.519 129.18 0.18011 0.70874 14.292 3.2205 4.548-0.68408zm-51.328 56.779c16.724-32.457 34.867-66.99 26.448-105.7-5.778-42.764-10.198-87.027-25.896-127.19-19.922-33.893-46.755-82.137-91.503-72.54-18.288 2.7402-42.119 40.692-10.404 16.755 37.144-21.138 76.296 15.696 92.26 49.254 29.14 51.916 22.904 113.74 18.192 171.02 1.8509 26.26-51.728 78.11-16.058 87.737 7.952-4.0068 8.6249-11.244 6.9624-19.329z""")

    smiley.vertices -= smiley.vertices.mean(axis=0)
    
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
    axs[0][0].set_xticklabels([])
    axs[0][0].set_yticklabels([])

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

    while True > 0:
        if len(game.rabbits) == 0:
            plt.pause(0.1)
            continue
        plt.pause(0.5)
        game.movement()
        game.clean()
        game.reproduce()
        game.clean()
        print("Iteration #", i)
        sum_speed = 0
        sum_size = 0
        sum_energy = 0
        for r in game.rabbits:
            sum_speed += r.speed
            sum_size += r.size
            sum_energy += r.energy_level
        print("    Population: {}  Avg. speed: {:.4f}   Avg. size: {:.4f}  Avg. energy: {:.4f}".format(pop, sum_speed/pop, sum_size/pop, sum_energy/pop))
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
        axs[0][0].scatter(xc, yc, s=ss*100, color='r', marker=smiley)
        axs[0][0].scatter(xp, yp, s=100.0, marker=r'$\clubsuit$', color = 'g', alpha = 0.5)
        axs[0][0].set_xticklabels([])
        axs[0][0].set_yticklabels([])       

        axs[0][1].plot(its, speeds, 'b')
        axs[0][1].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[0][1].set_ylim([0, max(3, max(speeds) + 1)])

        axs[1][0].plot(its, sizes, 'g')
        axs[1][0].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[1][0].set_ylim([0, max(3, max(sizes) + 1)])

        axs[1][1].plot(its, pops, 'r')
        axs[1][1].set_xlim([0, max(NUM_ITERATIONS, i+10)])
        axs[1][1].set_ylim([0, max(10, max(pops) + 100)])
        plt.draw()
        i +=1
        pop = len(game.rabbits)
    


        
if __name__ == "__main__":
    main()