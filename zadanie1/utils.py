def read_puzzle_file(filename):
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

def find_empty(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j
    return None


