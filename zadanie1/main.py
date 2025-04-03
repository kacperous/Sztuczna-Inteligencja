import sys
import argparse
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

if __name__ == '__main__':
    main()