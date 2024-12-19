from main import planner
import numpy as np
import random


def generate_test_map(size=(242, 242), wall_density=0.2):
    map = np.zeros(size)

    # Randomly place walls based on density
    for i in range(size[0]):
        for j in range(size[1]):
            if random.random() < wall_density:
                map[i, j] = 1

    # Keep borders clear
    map[0, :] = 0
    map[-1, :] = 0
    map[:, 0] = 0
    map[:, -1] = 0

    # Find a valid start position (empty cell)
    valid_starts = []
    for i in range(size[0]):
        for j in range(size[1]):
            if map[i, j] == 0:
                # Check if there's some empty space around this position
                empty_neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if (0 <= i + di < size[0] and
                                0 <= j + dj < size[1] and
                                map[i + di, j + dj] == 0):
                            empty_neighbors += 1
                if empty_neighbors >= 5:  # Require at least 5 empty neighbors
                    valid_starts.append((i, j))

    if not valid_starts:
        # If no valid start found, clear some space
        center_i, center_j = size[0] // 2, size[1] // 2
        map[center_i - 1:center_i + 2, center_j - 1:center_j + 2] = 0
        valid_starts = [(center_i, center_j)]

    # Choose random start position
    start_row, start_col = random.choice(valid_starts)

    # Place goal in a valid position far from start
    valid_goals = []
    min_distance = max(size[0], size[1]) // 3  # Minimum distance between start and goal

    for i in range(size[0]):
        for j in range(size[1]):
            if map[i, j] == 0:
                distance = ((i - start_row) ** 2 + (j - start_col) ** 2) ** 0.5
                if distance >= min_distance:
                    valid_goals.append((i, j))

    if valid_goals:
        goal_row, goal_col = random.choice(valid_goals)
        map[goal_row, goal_col] = 2
    else:
        # If no valid goal position found, place it in the furthest corner
        corners = [(0, 0), (0, size[1] - 1), (size[0] - 1, 0), (size[0] - 1, size[1] - 1)]
        goal_row, goal_col = max(corners, key=lambda pos:
        ((pos[0] - start_row) ** 2 + (pos[1] - start_col) ** 2) ** 0.5)
        map[goal_row, goal_col] = 2

    return map, start_row + 1, start_col + 1


# Test the maze generator with different densities
def test_maze_generator(num_tests=5):
    densities = [0.1, 0.2, 0.3, 0.4, 0.5]
    for density in densities:
        print(f"\nTesting with wall density: {density}")
        for test in range(num_tests):
            print(f"Test {test + 1}:")
            map, start_row, start_col = generate_test_map(wall_density=density)
            value_map, path = planner(map, start_row, start_col)
            if path is None:
                print("No path found")
            else:
                print(f"Path found with length: {len(path)}")


# Example usage:
if __name__ == "__main__":
    # Run multiple tests with different densities
    test_maze_generator()
