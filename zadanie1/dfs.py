import time
from pathlib import Path
from input.puzzle import PuzzleState  # Upewnij się, że plik puzzle.py zawiera wymagany kod


def apply_move(state, move):
    """
    Wykonuje ruch w układance i zwraca nowy stan (planszę).
    """
    width = len(state[0])
    height = len(state)

    zero_x, zero_y = next(
        (i, j)
        for i, row in enumerate(state)
        for j, val in enumerate(row)
        if val == 0
    )

    moves = {
        "up": (zero_x - 1, zero_y),
        "down": (zero_x + 1, zero_y),
        "left": (zero_x, zero_y - 1),
        "right": (zero_x, zero_y + 1),
    }

    if move not in moves:
        return None

    new_x, new_y = moves[move]

    if 0 <= new_x < height and 0 <= new_y < width:
        new_state = [row[:] for row in state]
        new_state[zero_x][zero_y], new_state[new_x][new_y] = (
            new_state[new_x][new_y],
            new_state[zero_x][zero_y],
        )
        return new_state

    return None


def save_solution_file(file_path, solution):
    """
    Zapisuje plik z rozwiązaniem układanki.
    :param file_path: Ścieżka do pliku z rozwiązaniem
    :param solution: Lista ruchów rozwiązania lub None, jeśli brak rozwiązania
    """
    with open(file_path, "w") as file:
        if solution is None:
            file.write("-1\n")
        else:
            file.write(f"{len(solution)}\n")
            file.write(" ".join(solution) + "\n")


def save_stats_file(file_path, stats, solution_length, elapsed_time):
    """
    Zapisuje plik z dodatkowymi informacjami o działaniu algorytmu.
    :param file_path: Ścieżka do pliku z dodatkowymi informacjami
    :param stats: Słownik ze statystykami odwiedzin, przetwarzania itp.
    :param solution_length: Długość rozwiązania (liczba ruchów) lub -1, jeśli brak rozwiązania
    :param elapsed_time: Czas działania w milisekundach
    """
    with open(file_path, "w") as file:
        file.write(f"{solution_length}\n")
        file.write(f"{stats['visited']}\n")
        file.write(f"{stats['processed']}\n")
        file.write(f"{stats['max_depth']}\n")
        file.write(f"{elapsed_time:.3f}\n")


def dfs_solver(initial_state, limit=20, solution_file="solution.txt", stats_file="stats.txt"):
    """
    Rozwiązanie układanki przy użyciu DFS z ograniczeniem głębokości, zapisującej wyniki do plików.
    :param initial_state: Obiekt PuzzleState – układ początkowy
    :param limit: Ograniczenie głębokości DFS
    :param solution_file: Ścieżka do pliku z rozwiązaniem
    :param stats_file: Ścieżka do pliku z dodatkowymi informacjami
    """
    # Uruchomienie mierzenia czasu
    start_time = time.time()

    stack = [initial_state]
    visited = set()
    stats = {"visited": 0, "processed": 0, "max_depth": 0}

    while stack:
        current = stack.pop()
        stats["processed"] += 1

        if current.is_goal():
            elapsed_time = (time.time() - start_time) * 1000  # Czas działania w ms
            solution = current.get_solution_path()
            save_solution_file(solution_file, solution)
            save_stats_file(stats_file, stats, len(solution), elapsed_time)
            return solution, stats

        if current.depth > limit:
            continue

        state_str = str(current.state)

        if state_str not in visited:
            visited.add(state_str)
            stats["visited"] += 1
            stats["max_depth"] = max(stats["max_depth"], current.depth)

            for move in ["up", "down", "left", "right"]:
                new_state = apply_move(current.state, move)
                if new_state is not None and str(new_state) not in visited:
                    stack.append(PuzzleState(new_state, parent=current, action=move, depth=current.depth + 1))

    # Jeśli nie znaleziono rozwiązania
    elapsed_time = (time.time() - start_time) * 1000  # Czas działania w ms
    save_solution_file(solution_file, None)
    save_stats_file(stats_file, stats, -1, elapsed_time)
    return None, stats
