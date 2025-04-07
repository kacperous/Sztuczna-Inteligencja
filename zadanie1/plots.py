import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from pathlib import Path

def read_stats_file(file_path):
    """Odczytuje plik statystyk i zwraca dane jako słownik."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) >= 5:
        try:
            return {
                'solution_length': int(lines[0].strip()),
                'visited_states': int(lines[1].strip()),
                'processed_states': int(lines[2].strip()),
                'max_depth': int(lines[3].strip()),
                'time': float(lines[4].strip())
            }
        except ValueError:
            return None
    return None

def extract_info_from_filename(filename):
    """Wyciąga informacje z nazwy pliku statystyk."""
    # Format: SIZE_DEPTH_ID_ALGORITHM_PARAM_stats.txt
    # Np.: 4x4_01_00001_astar_hamm_stats.txt
    pattern = r'(\d+x\d+)_(\d+)_(\d+)_(\w+)_(\w+)_stats\.txt'
    match = re.match(pattern, filename)

    if match:
        size, depth, puzzle_id, algorithm, param = match.groups()
        return {
            'size': size,
            'depth': int(depth),
            'puzzle_id': puzzle_id,
            'algorithm': algorithm.lower(),
            'param': param.lower()
        }
    return None

def collect_stats(stats_dir):
    """Zbiera statystyki ze wszystkich plików."""
    stats_list = []

    for file_name in os.listdir(stats_dir):
        if file_name.endswith('_stats.txt'):
            file_path = os.path.join(stats_dir, file_name)
            stats_data = read_stats_file(file_path)

            if stats_data:
                info = extract_info_from_filename(file_name)
                if info:
                    stats_data.update(info)
                    stats_list.append(stats_data)

    return pd.DataFrame(stats_list)

def create_algorithms_comparison(df, stat_name, stat_label, output_file):
    """Tworzy wykres porównujący wszystkie algorytmy."""
    plt.figure(figsize=(10, 6))

    # Grupowanie po głębokości i algorytmie
    grouped = df.groupby(['depth', 'algorithm'])[stat_name].mean().unstack()

    # Tworzenie wykresu
    grouped.plot(kind='bar', ax=plt.gca())

    # Ustawienie skali logarytmicznej dla osi Y
    if (grouped > 0).all().all():  # Sprawdź czy wszystkie wartości są dodatnie
        plt.yscale('log')
    else:
        # Dla danych zawierających zera użyj skali symlog
        plt.yscale('symlog', linthresh=0.1)

    plt.xlabel('Głębokość układanki')
    plt.ylabel(stat_label)
    plt.title(f'Porównanie algorytmów - {stat_label}')
    plt.legend(title='Algorytm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()


def create_astar_comparison(df, stat_name, stat_label, output_file):
    """Tworzy wykres porównujący heurystyki A*."""
    plt.figure(figsize=(10, 6))

    # Filtrowanie tylko dla A*
    astar_df = df[df['algorithm'] == 'astar']

    # Grupowanie po głębokości i parametrze
    grouped = astar_df.groupby(['depth', 'param'])[stat_name].mean().unstack()

    # Tworzenie wykresu
    grouped.plot(kind='bar', ax=plt.gca())

    # Ustawienie skali logarytmicznej dla osi Y
    if (grouped > 0).all().all():  # Sprawdź czy wszystkie wartości są dodatnie
        plt.yscale('log')
    else:
        # Dla danych zawierających zera użyj skali symlog
        plt.yscale('symlog', linthresh=0.1)

    plt.xlabel('Głębokość układanki')
    plt.ylabel(stat_label)
    plt.title(f'Porównanie heurystyk A* - {stat_label}')
    plt.legend(title='Heurystyka')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()


def create_bfs_comparison(df, stat_name, stat_label, output_file):
    """Tworzy wykres porównujący kolejności ruchu dla BFS."""
    plt.figure(figsize=(12, 6))

    # Filtrowanie tylko dla BFS
    bfs_df = df[df['algorithm'] == 'bfs']

    # Grupowanie po głębokości i parametrze
    grouped = bfs_df.groupby(['depth', 'param'])[stat_name].mean().unstack()

    # Tworzenie wykresu
    grouped.plot(kind='bar', ax=plt.gca())

    # Ustawienie skali logarytmicznej dla osi Y
    if (grouped > 0).all().all():  # Sprawdź czy wszystkie wartości są dodatnie
        plt.yscale('log')
    else:
        # Dla danych zawierających zera użyj skali symlog
        plt.yscale('symlog', linthresh=0.1)

    plt.xlabel('Głębokość układanki')
    plt.ylabel(stat_label)
    plt.title(f'Porównanie kolejności ruchów BFS - {stat_label}')
    plt.legend(title='Kolejność', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()


def create_dfs_comparison(df, stat_name, stat_label, output_file):
    """Tworzy wykres porównujący kolejności ruchu dla DFS."""
    plt.figure(figsize=(12, 6))

    # Filtrowanie tylko dla DFS
    dfs_df = df[df['algorithm'] == 'dfs']

    # Grupowanie po głębokości i parametrze
    grouped = dfs_df.groupby(['depth', 'param'])[stat_name].mean().unstack()

    # Tworzenie wykresu
    grouped.plot(kind='bar', ax=plt.gca())

    # Ustawienie skali logarytmicznej dla osi Y
    if (grouped > 0).all().all():  # Sprawdź czy wszystkie wartości są dodatnie
        plt.yscale('log')
    else:
        # Dla danych zawierających zera użyj skali symlog
        plt.yscale('symlog', linthresh=0.1)

    plt.xlabel('Głębokość układanki')
    plt.ylabel(stat_label)
    plt.title(f'Porównanie kolejności ruchów DFS - {stat_label}')
    plt.legend(title='Kolejność', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()

def main():
    # Ścieżka do katalogu ze statystykami
    stats_dir = Path('stats')

    # Ścieżka do folderu na wykresy
    plots_dir = Path('plots')
    plots_dir.mkdir(exist_ok=True)

    # Zbieranie statystyk
    df = collect_stats(stats_dir)

    if df.empty:
        print("Nie znaleziono danych statystycznych.")
        return

    # Statystyki do porównania
    stats = {
        'solution_length': 'Długość znalezionego rozwiązania',
        'visited_states': 'Liczba odwiedzonych stanów',
        'processed_states': 'Liczba przetworzonych stanów',
        'max_depth': 'Maksymalna osiągnięta głębokość',
        'time': 'Czas wykonania [ms]'
    }

    # Tworzenie wykresów dla każdej statystyki
    for stat_name, stat_label in stats.items():
        # Porównanie algorytmów
        create_algorithms_comparison(
            df, stat_name, stat_label,
            plots_dir / f'algorithms_{stat_name}.png'
        )

        # Porównanie heurystyk A*
        create_astar_comparison(
            df, stat_name, stat_label,
            plots_dir / f'astar_{stat_name}.png'
        )

        # Porównanie BFS
        create_bfs_comparison(
            df, stat_name, stat_label,
            plots_dir / f'bfs_{stat_name}.png'
        )

        # Porównanie DFS
        create_dfs_comparison(
            df, stat_name, stat_label,
            plots_dir / f'dfs_{stat_name}.png'
        )

    print(f"Wykresy zostały zapisane w katalogu {plots_dir}")

if __name__ == "__main__":
    main()