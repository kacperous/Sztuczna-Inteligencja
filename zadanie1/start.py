import os
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from utils import read_puzzle, save_solution, save_stats
from bfs import bfs
from dfs import dfs
from astar import astar

#wykorzystujemy wiedze z sysopów ze procesy mogą byc przetwarzane równolegle (współbiegłość) ESSA
def wykonaj_zadanie(args):
    plik, algo, param = args
    try:
        state, _, _ = read_puzzle(plik)
        file_name = plik.stem
        solution_file = Path('solutions') / f"{file_name}_{algo}_{param.lower()}_sol.txt"
        stats_file = Path('stats') / f"{file_name}_{algo}_{param.lower()}_stats.txt"

        if algo == 'bfs':
            solution, stats = bfs(state, param)
        elif algo == 'dfs':
            solution, stats = dfs(state, param)
        else:
            solution, stats = astar(state, param)

        save_solution(solution, solution_file)
        save_stats(stats_file, solution, stats['visited'], stats['processed'],
                  stats['max_depth'], stats['time'])
        return True
    except Exception as e:
        print(f"BŁĄD: {algo} {param} dla {plik.name}: {str(e)}")
        return False

def main():
    Path('solutions').mkdir(exist_ok=True)
    Path('stats').mkdir(exist_ok=True)

    strategie = {
        'bfs': ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD'],
        'dfs': ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD'],
        'astar': ['manh', 'hamm']
    }

    pliki = list(Path('input').glob('*.txt'))
    print(f"Znaleziono {len(pliki)} plików wejściowych")

    zadania = [(plik, algo, param)
              for plik in pliki
              for algo, params in strategie.items()
              for param in params]

    print(f"Rozpoczynam przetwarzanie {len(zadania)} zadań")
    start = time.time()

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(wykonaj_zadanie, zadania)

    print(f"Zakończono w {time.time() - start:.2f} sekund")

if __name__ == "__main__":
    main()