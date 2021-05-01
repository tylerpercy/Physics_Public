# Tyler Percy
# 4/19/21
# PHY 2200

from vpython import *

'''
CONSTANTS:

    DEBUG_MODE: binary to display debug information

    CONSTANT_HEAT_SOURCE: whether grid[0][0] should stay at max heat or not
    RATE: how fast the vpython animation iterates
    n: number of iterations
    r: rate of heat transfer
    x: number of sections on x-axis
    y: number of sections on y-axis
    z: number of sections on z-axis

'''

DEBUG_MODE = 0

CONSTANT_HEAT_SOURCE = 1 # Keep this as 1 for now
RATE = 50
n = 10000
r = 0.1  
x = 12   
y = 12
z = 12

'''
FUNCTION

    Name:
        print_grid
    
    Description:
        Print the current state of the temperature grid

    Parameters:
        grid: grid to be printed
        x:    constant x-axis size of grid
        y:    constant y-axis size of grid
        z:    constant z-axis size of grid

    Returns:
        N/A
'''

def print_grid(grid, x, y, z):
    for i in range(0, x):
        for j in range(0, y):
            for k in range(0,z):
                print("{:.02f}\t".format(grid[i][j][k]), end = "")
        print()

'''
FUNCTION

    Name: 
        get_new_cell_temp

    Description:
        Calculate the new temperatue of the current cell based on the temperature of
        adjacent cells using the following formula:
        
        site + ∆site = (1-xr) + (from 1 to x)∑neighbor[i], where 0 < r < 1/x
        r = .1
        x = adjacent sides
            - in this implementation x = 4
        i = adjacent side

    Parameters:
        temps: a 2-dimensional list containing the current temperatures
        r:     the constant value r: .1
        i:     the current x position of the cell being updated, ranges from 0 to x-1
        j:     the current y position of the cell being updated, ranges from 0 to y-1
        k:     the current z position of the cell being updated, ranges from 0 to z-1
        x:     constant x-axis size of temps
        y:     constant y-axis size of temps
        z:     constant z-axis size of temps

    Returns:
        delta_ti: the change in temperature of cell[i][j][k] represented as a float

'''

def get_new_cell_temp(temps, r, i, j, k, x, y, z):

    if DEBUG_MODE:
        print(f"x: {i} y: {j} z: {k}")

    # starting coordinate
    if i == j == k == 0:
        delta_ti = (3 * r * (((temps[i+1][j][k] + temps[i][j+1][k] + temps[i][j][k+1]) / 3) - temps[i][j][k]))
    # along 0 < j < y-1
    elif 0 < i < x-1 and j == 0 and k == 0:
        delta_ti = (4 * r * (((temps[i-1][j][k] + temps[i+1][j][k] + temps[i][j+1][k] + temps[i][j][k+1]) / 4) - temps[i][j][k]))
    # along 0 < i < x-1
    elif i == 0 and 0 < j < y-1 and k == 0:
        delta_ti = (4 * r * (((temps[i+1][j][k] + temps[i][j-1][k] + temps[i][j+1][k] + temps[i][j][k+1]) / 4) - temps[i][j][k]))
    # along 0 < k < z-1
    elif i == 0 and j == 0 and 0 < k < z-1:
        delta_ti = (4 * r * (((temps[i+1][j][k] + temps[i][j+1][k] + temps[i][j][k-1] + temps[i][j][k+1]) / 4) - temps[i][j][k]))
    # final coordinate
    elif i == x-1 and j == y-1 and k == z-1:
        delta_ti = (3 * r * (((temps[i-1][j][k] + temps[i][j-1][k] + temps[i][j][k-1]) / 3) - temps[i][j][k]))
    elif i == x-1 and j == y-1:
        delta_ti = (4 * r * (((temps[i-1][j][k] + temps[i][j-1][k] + temps[i][j][k-1] + temps[i][j][k+1]) / 4) - temps[i][j][k]))
    elif i == x-1 and k == z-1:
        delta_ti = (4 * r * (((temps[i-1][j][k] + temps[i][j-1][k] + temps[i][j+1][k] + temps[i][j][k-1]) / 4) - temps[i][j][k]))
    elif j == y-1 and k == z-1:
        delta_ti = (4 * r * (((temps[i-1][j][k] + temps[i+1][j-1][k] + temps[i][j-1][k] + temps[i][j][k-1]) / 4) - temps[i][j][k])) 
    # along k = z-1
    elif k == z-1:
        delta_ti = (5 * r * (((temps[i-1][j][k] + temps[i+1][j][k] + temps[i][j+1][k] + temps[i][j-1][k] + temps[i][j][k-1]) / 5) - temps[i][j][k]))
    # along j = y-1
    elif j == y-1:
        delta_ti = (5 * r * (((temps[i+1][j][k] + temps[i-1][j][k] + temps[i][j-1][k] + temps[i][j][k-1] + temps[i][j][k+1]) / 5) - temps[i][j][k]))
    # along i = x-1
    elif i == x-1:
        delta_ti = (5 * r * (((temps[i-1][j][k] + temps[i][j+1][k] + temps[i][j-1][k] + temps[i][j][k-1] + temps[i][j][k+1]) / 5) - temps[i][j][k]))
    # any coordinate touched by 6 adjacent sections
    else:
        delta_ti = (6 * r * (((temps[i-1][j][k] + temps[i+1][j][k] + temps[i][j-1][k] + \
            temps[i][j+1][k] + temps[i][j][k-1] + temps[i][j][k+1]) / 6) - temps[i][j][k]))

    return delta_ti

def main():
    ''' Initial conditions for the grids '''
    scene = canvas(center= vec(5,-5,0), userzoom= False)
    lbl = label(pos= vec(1,2,0), text= "Processing...")
    lbl_temps = label(pos= vec(8,2,0))
    boxes = [[[box(pos= vec(i, -j, k)) for i in range(x)] for j in range(y)] for k in range(z)]
    grid = [[[0 for _ in range(x)] for _ in range(y)] for _ in range(z)]
    temps = [[[0 for _ in range(x)] for _ in range(y)] for _ in range(z)]
    grid[0][0][0] = 100
    temps[0][0][0] = 100
    boxes[0][0][0].color = vec(50,0,0)

    # default grid
    if DEBUG_MODE:
        print_grid(grid, x, y, z)

    for i in range(n):
        rate(RATE)
        # Print current iteration of main loop
        if DEBUG_MODE:
            print(f"Iteration: {i+1}")

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if CONSTANT_HEAT_SOURCE:
                        grid[0][0][0] = 100
                        temps[0][0][0] = 100
                        boxes[0][0][0].color = vec(50,0,0)
                    delta_ti = get_new_cell_temp(temps, r, i, j, k, x, y, z)

                    # print return value of update_cell_temp
                    if DEBUG_MODE:
                        print(f"delta_ti: {delta_ti}")

                    grid[i][j][k] += delta_ti
                    boxes[i][j][k].color += vec(delta_ti,delta_ti,delta_ti)

        temps = grid

    lbl.text = "Finished."

    if DEBUG_MODE:
        print()
        print_grid(grid, x, y)

    while(True):
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if boxes[i][j][k] == scene.mouse.pick:
                        lbl_temps.text = "{:.02f}% heated".format(temps[i][j][k])


if __name__ == "__main__":
    main()