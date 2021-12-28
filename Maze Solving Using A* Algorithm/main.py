from tkinter.constants import S
from pyamaze import maze,agent,textLabel,COLOR
from queue import PriorityQueue

# Heuristic Function which returns the Manhatten Distance between start cell and end cell
def hDist(startCell,endCell):
    x1,y1 = startCell
    x2,y2 = endCell
    return abs(x2-x1) + abs(y2-y1)

# A Star Algorithm 
def aStarAlgorithm(maze: maze):
    # Start Cell is the right bottom cell i.e (n,n) where n is the size of maze
    startCell = (maze.rows,maze.cols) 

    # Creating dictionary of a cell and its distance from the start cell.
    # Initially every cell is at infinity from the start cell
    gDist = {cell:float('inf') for cell in maze.grid}
    gDist[startCell] = 0

    # Creating dictionary to store the the sum of gDist and hDist for each cell
    # Initially every cell has infinity 
    fDist = {cell:float('inf') for cell in maze.grid}
    fDist[startCell] = gDist[startCell] + hDist(startCell,(1,1))

    # Creating a priority queue
    openList = PriorityQueue()
    openList.put((fDist[startCell],hDist(startCell,(1,1)),startCell))

    # It stores the Child Cell and Its Parent Cell
    path1 = {}

    while not openList.empty():
        # Get the cell wit minimum fDist from the Priority Queue
        currentCell = openList.get()[2]

        # Check if the Current Cell is Goal Cell
        if currentCell == (1,1):
            break
        for direction in 'NEWS':
            if maze.maze_map[currentCell][direction]==True:

                # Decrease the Row count if we move up
                if direction == 'N':
                    childCell = (currentCell[0]-1,currentCell[1])
                
                # Increase the Column count if we move right
                if direction == 'E':
                    childCell = (currentCell[0],currentCell[1]+1)

                # Decrease the Column count if we move left
                if direction == 'W':
                    childCell = (currentCell[0],currentCell[1]-1)

                # Increase the Row count if we move down
                if direction == 'S':
                    childCell = (currentCell[0]+1,currentCell[1])
                
                # Calculating the new gDist and fDist for the child cell
                newGDist = gDist[currentCell] + 1
                newFDist = newGDist + hDist(childCell,(1,1))

                # Store the gDist and fDist values if new fDist is less than the old one
                if newFDist < fDist[childCell]:
                    gDist[childCell] = newGDist
                    fDist[childCell] = newFDist

                    # Add the cell to the Open List (Priority Queue)
                    openList.put((fDist[childCell],hDist(childCell,(1,1)),childCell))

                    # Update the parent cell of the child cell
                    path1[childCell] = currentCell
    
    # The Final Path must be from start cell to gaol cell
    finalPath = {}
    cell = (1,1)

    # Reversing the path
    while cell != startCell:
        finalPath[path1[cell]] = cell
        cell = path1[cell]
    return finalPath


if __name__ == "__main__":
    sizeOfMaze = int(input("Enter the size of the Maze: "))
    n = sizeOfMaze

    # Generating Perfect maze of size n X n
    m = maze(n,n)
    m.CreateMaze(theme="light")
    path1 = aStarAlgorithm(m)

    # Creating an agent to travel through the path1 from startcell(n,n) to goalcell(1,1)
    a = agent(m,footprints=True,color=COLOR.red)

    # Animating the path of agent with a delay of 100ms
    m.tracePath({a:path1},delay=100)

    # Displaying the Cost of the path``
    l = textLabel(m,"Cost of Path:",len(path1))
    m.run()