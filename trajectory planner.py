def planner(map, start_row, start_column):
    # inside map 2d array, 1 => obstacle, 0 => free space, 2 => goal.
    goal_row, goal_column = find_goal(map)
    value_map = get_value_map(map, goal_row, goal_column)
    path = get_path(value_map, start_row - 1, start_column - 1)
    return value_map, path


def find_goal(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 2:
                return (i, j)


def get_value_map(map, goal_row, goal_column):
    visited = {}
    queue = [(goal_row, goal_column)]
    visited[(goal_row, goal_column)] = 0
    value_map = map.copy()
    while len(queue) > 0:
        row, column = queue.pop(0)
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
                queue.append((next_row, next_column))
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
                current_row -= 1
                path.append((current_row, current_column))
                continue

        # right
        if current_column + 1 < len(value_map[current_row]):
            if value_map[current_row][current_column + 1] < value_map[current_row][current_column]:
                current_column += 1
                path.append((current_row, current_column))
                continue

        # down
        if current_row + 1 < len(value_map):
            if value_map[current_row + 1][current_column] < value_map[current_row][current_column]:
                current_row += 1
                path.append((current_row, current_column))
                continue

        # left
        if current_column - 1 >= 0:
            if value_map[current_row][current_column - 1] < value_map[current_row][current_column]:
                current_column -= 1
                path.append((current_row, current_column))
                continue

        # check diagonal directions

        # upper-right
        if current_row - 1 >= 0 and current_column + 1 < len(value_map[current_row]):
            if value_map[current_row - 1][current_column + 1] < value_map[current_row][current_column]:
                current_row -= 1
                current_column += 1
                path.append((current_row, current_column))
                continue

        # lower-right
        if current_row + 1 < len(value_map) and current_column + 1 < len(value_map[current_row]):
            if value_map[current_row + 1][current_column + 1] < value_map[current_row][current_column]:
                current_row += 1
                current_column += 1
                path.append((current_row, current_column))
                continue

        # lower-left
        if current_row + 1 < len(value_map) and current_column - 1 >= 0:
            if value_map[current_row + 1][current_column - 1] < value_map[current_row][current_column]:
                current_row += 1
                current_column -= 1
                path.append((current_row, current_column))
                continue

        # upper-left
        if current_row - 1 >= 0 and current_column - 1 >= 0:
            if value_map[current_row - 1][current_column - 1] < value_map[current_row][current_column]:
                current_row -= 1
                current_column -= 1
                path.append((current_row, current_column))
                continue

    path = [(row + 1, column + 1) for row, column in path]
    return path
