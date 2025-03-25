from utils import read_puzzle_file
from utils import save_puzzle_file
from utils import find_empty

from pathlib import Path

if __name__ == '__main__':
    try:
        current_dir = Path(__file__).parent
        input_file = current_dir / "input" / "3x3_easy.txt"

        state, width, height = read_puzzle_file(str(input_file))
        print(f"Wczytano układankę o wymiarach {height}x{width}:")
        for row in state:
            print(row)

        empty_y, empty_x = find_empty(state)
        print(f"Położenie pustego pola: ({empty_y}, {empty_x})")

        test_solution = ['L', 'R', 'U', 'D']
        output_file = "test.txt"
        save_puzzle_file(test_solution, output_file)
    except Exception as e:
        print(e)

