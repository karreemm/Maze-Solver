from ourQueue import OurQueue

from scipy.io import loadmat
import matplotlib.pyplot as plt

mat_data = loadmat('maze.mat')
map = mat_data['map'].astype(float)

start_row = 45
start_column = 4

# map = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 0, 0, 2],
# ]

# start_row = 1
# start_column = 1


def planner(map, start_row, start_column):
    # inside map 2d array, 1 => obstacle, 0 => free space, 2 => goal.
    goal_column, goal_row = get_goal(map)
    value_map = get_value_map(map, goal_row, goal_column)
    path = get_path(value_map, start_row - 1, start_column - 1)
    if path is None:
        print("No path available")
        return value_map, None
    plot_trajectory(map, goal_row, goal_column, start_row, start_column, path)
    return value_map, path


def get_goal(map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 2:
                return col, row
    return None


def get_value_map(map, goal_row, goal_column):
    visited = {}
    queue = OurQueue()
    queue.add((goal_row, goal_column))
    visited[(goal_row, goal_column)] = 0
    value_map = map.copy()
    while not queue.is_empty():
        row, column = queue.pop()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                next_row = row + i
                next_column = column + j
                if next_row < 0 or next_row >= len(map) or next_column < 0 or next_column >= len(map[0]):
                    continue
                if value_map[next_row][next_column] == 1:
                    continue
                if (next_row, next_column) in visited:
                    continue
                value_map[next_row][next_column] = value_map[row][column] + 1
                queue.add((next_row, next_column))
                visited[(next_row, next_column)] = 0
    return value_map


def get_path(value_map, start_row, start_column):
    path = [(start_row, start_column)]
    current_row, current_column = start_row, start_column
    while value_map[current_row][current_column] != 2:
        # check orthogonal directions

        # up
        if current_row - 1 >= 0:  # up
            if value_map[current_row - 1][current_column] < value_map[current_row][current_column]:
                if value_map[current_row - 1][current_column] != 1:
                    current_row -= 1
                    path.append((current_row, current_column))
                    continue

        # right
        if current_column + 1 < len(value_map[current_row]):
            if value_map[current_row][current_column + 1] < value_map[current_row][current_column]:
                if value_map[current_row][current_column + 1] != 1:
                    current_column += 1
                    path.append((current_row, current_column))
                    continue

        # down
        if current_row + 1 < len(value_map):
            if value_map[current_row + 1][current_column] < value_map[current_row][current_column]:
                if value_map[current_row + 1][current_column] != 1:
                    current_row += 1
                    path.append((current_row, current_column))
                    continue

        # left
        if current_column - 1 >= 0:
            if value_map[current_row][current_column - 1] < value_map[current_row][current_column]:
                if value_map[current_row][current_column - 1] != 1:
                    current_column -= 1
                    path.append((current_row, current_column))
                    continue

        # check diagonal directions

        # up-right
        if current_row - 1 >= 0 and current_column + 1 < len(value_map[current_row]):
            if value_map[current_row - 1][current_column + 1] < value_map[current_row][current_column]:
                if value_map[current_row - 1][current_column + 1] != 1:
                    current_row -= 1
                    current_column += 1
                    path.append((current_row, current_column))
                    continue

        # down-right
        if current_row + 1 < len(value_map) and current_column + 1 < len(value_map[current_row]):
            if value_map[current_row + 1][current_column + 1] < value_map[current_row][current_column]:
                if value_map[current_row + 1][current_column + 1] != 1:
                    current_row += 1
                    current_column += 1
                    path.append((current_row, current_column))
                    continue

        # down-left
        if current_row + 1 < len(value_map) and current_column - 1 >= 0:
            if value_map[current_row + 1][current_column - 1] < value_map[current_row][current_column]:
                if value_map[current_row + 1][current_column - 1] != 1:
                    current_row += 1
                    current_column -= 1
                    path.append((current_row, current_column))
                    continue

        # up-left
        if current_row - 1 >= 0 and current_column - 1 >= 0:
            if value_map[current_row - 1][current_column - 1] < value_map[current_row][current_column]:
                if value_map[current_row - 1][current_column - 1] != 1:
                    current_row -= 1
                    current_column -= 1
                    path.append((current_row, current_column))
                    continue

        return None  # no path available

    return [(x + 1, y + 1) for x, y in path]


def plot_trajectory(map, goal_row, goal_column, start_row, start_col, path):
    fig, ax = plt.subplots()
    ax.imshow(map, cmap='Greys', origin='upper')
    # Adjust start and goal coordinates to match path coordinates
    ax.plot(start_col - 1, start_row - 1, 'bo')  # Start point (blue)
    ax.plot(goal_column, goal_row, 'ro')  # Goal point (red)

    # Plot the path
    for i in range(len(path) - 1):
        ax.plot([path[i][1] - 1, path[i + 1][1] - 1],
                [path[i][0] - 1, path[i + 1][0] - 1], 'r-')
    plt.show()


value_map, path = planner(map, start_row, start_column)
