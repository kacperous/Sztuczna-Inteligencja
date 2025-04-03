from pathlib import Path
from io import StringIO

def read_puzzle(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            puzzle_size = lines[0].strip().split()
            if len(puzzle_size) != 2:
                raise ValueError('Wrong format of puzzle file')

            height, width = map(int, puzzle_size)

            #Wczytywanie
            state = []
            for i in range(1, height + 1):
                if i >= len(lines):
                    raise ValueError('Wrong format of puzzle file i >= len(lines)')
                row_values = lines[i].strip().split()
                if len(row_values) != width:
                    raise ValueError('Wrong format of puzzle file len(row_values) != width')
                row = list(map(int, row_values))
                state.append(row)

            #Sprawdzanie czy kazde pole ma inna wartość
            flat_state = [num for row in state for num in row]
            expected_numbers = set(range(height * width))
            actual_numbers = set(flat_state)

            if len(flat_state) != height * width:
                raise ValueError(
                    f"Wrong file format: elements: ({len(flat_state)}) is not equal size of puzzle ({height * width}).")

            if expected_numbers != actual_numbers:
                missing = expected_numbers - actual_numbers
                duplicated = [num for num in flat_state if flat_state.count(num) > 1]

                error_msg = "Wrong file format: "
                if missing:
                    error_msg += f"missing: {missing}, "
                if duplicated:
                    error_msg += f"duplicated: {set(duplicated)}, "

                raise ValueError(error_msg[:-2] + ".")

            return state, width, height

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except ValueError as e:
        raise ValueError(f"Error while reading file: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def save_solution(solution, filename):
    try:
        solutions_dir = Path(__file__).parent / "solutions"
        solutions_dir.mkdir(exist_ok=True)

        output_filename = Path(filename).name
        output_path = solutions_dir / output_filename

        with open(output_path, 'w') as file:
            if solution is None:
                file.write('-1\n')
            else:
                file.write(f"{len(solution)}\n")
                if solution:
                    file.write(''.join(solution) + '\n')
    except Exception as e:
        raise Exception(f"Error while saving file: {str(e)}")

def save_stats(file_path, path, visited, processed, max_depth, elapsed):
    output = StringIO()
    output.write(f"{len(path) if path != '-1' else -1}\n")
    output.write(f"{visited}\n")
    output.write(f"{processed}\n")
    output.write(f"{max_depth}\n")
    output.write(f"{elapsed:.3f}\n")
    with open(file_path, "w") as f:
        f.write(output.getvalue())
    output.close()

def find_empty(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j
    return None

def get_possible_moves(state):
    # Zwraca możliwe ruchy dla danego stanu
    empty_y, empty_x = find_empty(state)
    height = len(state)
    width = len(state[0])
    moves = []

    if empty_x > 0:
        moves.append('L')
    if empty_x < width -1:
        moves.append('R')
    if empty_y > 0:
        moves.append('U')
    if empty_y < height - 1:
        moves.append('D')

    return moves


def apply_move(state, move):
    # Wykonuje ruch i zwraca nowy stan
    new_state = [row[:] for row in state]
    empty_y, empty_x = find_empty(new_state)

    if move == 'L':
        new_state[empty_y][empty_x], new_state[empty_y][empty_x - 1] = new_state[empty_y][empty_x - 1], \
        new_state[empty_y][empty_x]
    elif move == 'R':
        new_state[empty_y][empty_x], new_state[empty_y][empty_x + 1] = new_state[empty_y][empty_x + 1], \
        new_state[empty_y][empty_x]
    elif move == 'U':
        new_state[empty_y][empty_x], new_state[empty_y - 1][empty_x] = new_state[empty_y - 1][empty_x], \
        new_state[empty_y][empty_x]
    elif move == 'D':
        new_state[empty_y][empty_x], new_state[empty_y + 1][empty_x] = new_state[empty_y + 1][empty_x], \
        new_state[empty_y][empty_x]

    return new_state