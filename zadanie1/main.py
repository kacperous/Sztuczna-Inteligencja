from utils import read_puzzle_file
from utils import save_puzzle_file

from input.puzzle import PuzzleState
from dfs import dfs_solver

from pathlib import Path

if __name__ == "__main__":

    # Wczytaj układ z pliku tekstowego
    current_dir = Path(__file__).parent
    input_file = current_dir / "input" / "4x4_medium.txt"
    state, width, height = read_puzzle_file(str(input_file))

    # Tworzenie obiektu PuzzleState
    initial_state = PuzzleState(state)

    # Wywołanie dfs_solver z limitem głębokości 20
    solution, stats = dfs_solver(initial_state, limit=20)

    if solution:
        print("Znaleziono rozwiązanie!")
        print("Ścieżka ruchów:", solution)
    else:
        print("Nie znaleziono rozwiązania w ograniczeniu głębokości.")

    print("Statystyki przeszukiwania:")
    print(stats)
