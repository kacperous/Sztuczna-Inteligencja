<<<<<<< HEAD
from utils import read_puzzle_file
from utils import save_puzzle_file

from input.puzzle import PuzzleState
from dfs import dfs_solver

=======
import sys
import argparse
>>>>>>> fa091ec531d5714de5731fd911ba01040ff18184
from pathlib import Path
from utils import read_puzzle, save_solution, save_stats, find_empty
from bfs import bfs

def main():
    parser = argparse.ArgumentParser(description='Program do rozwiązywania układanek przesuwnych.')
    parser.add_argument('strategy', help='Strategia rozwiązywania: bfs, dfs, astr')
    parser.add_argument('param', help='Parametr dla strategii (dla bfs/dfs: kolejność ruchu [LRUD], dla astr: heurystyka [hamm/manh])')
    parser.add_argument('input_file', help='Ścieżka do pliku wejściowego z układanką')
    parser.add_argument('solution_file', help='Ścieżka do pliku, w którym zapisane zostanie rozwiązanie')
    parser.add_argument('stats_file', help='Ścieżka do pliku, w którym zapisane zostaną statystyki')

    args = parser.parse_args()

    try:
        # Wczytanie układanki z pliku
        state, width, height = read_puzzle(args.input_file)

        solution = None
        stats = None

        if args.strategy.lower() == 'bfs':
            print(f"Uruchamianie algorytmu BFS z kolejnością ruchów: {args.param}...")
            solution, stats = bfs(state, args.param)
        else:
            # Obsługa pozostałych strategii zostanie dodana w przyszłości
            print(f"Strategia {args.strategy} nie jest jeszcze zaimplementowana.")
            return

        # Zapisanie rozwiązania i statystyk
        save_solution(solution, args.solution_file)
        save_stats(args.stats_file, solution, stats['visited'], stats['processed'],
                  stats['max_depth'], stats['time'])

        print(f"Zapisano rozwiązanie do pliku {args.solution_file}")
        print(f"Zapisano statystyki do pliku {args.stats_file}")

    except Exception as e:
        print(f"Błąd: {e}")
        sys.exit(1)

<<<<<<< HEAD
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
=======
if __name__ == '__main__':
    main()
>>>>>>> fa091ec531d5714de5731fd911ba01040ff18184
