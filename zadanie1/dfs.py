import time
from puzzle import PuzzleState
from utils import get_possible_moves, apply_move

def dfs(initial_state, order='LRUD'):
    start_time = time.time()

    # Maksymalna głębokość przeszukiwania (zabezpieczenie)
    max_search_depth = 20

    initial = PuzzleState(initial_state)
    if initial.is_goal():
        end_time = time.time()
        stats = {
            'visited': 1,
            'processed': 0,
            'max_depth': 0,
            'time': (end_time - start_time) * 1000
        }
        return [], stats

    # Używamy listy jako stosu LIFO
    stack = [initial]
    visited = {str(initial.state)}
    visited_count = 1
    processed_count = 0
    max_depth = 0

    while stack:
        current = stack.pop()  # Zdejmujemy element z końca stosu (LIFO)
        processed_count += 1

        max_depth = max(max_depth, current.depth)

        # Sprawdzamy czy nie osiągnęliśmy maksymalnej głębokości
        if current.depth >= max_search_depth:
            continue

        # Generowanie i sortowanie możliwych ruchów według zadanego porządku
        possible_moves = get_possible_moves(current.state)
        sorted_moves = sorted(possible_moves, key=lambda x: order.index(x) if x in order else len(order))

        # Odwracamy kolejność, by zachować priorytet z parametru order
        # (w stosie ostatnio dodany jest pierwszym przetwarzanym)
        sorted_moves.reverse()

        for move in sorted_moves:
            new_state = apply_move(current.state, move)
            state_str = str(new_state)

            if state_str not in visited:
                child = PuzzleState(new_state, current, move, current.depth + 1)
                max_depth = max(max_depth, child.depth)

                if child.is_goal():
                    # Znaleziono rozwiązanie
                    solution = child.get_solution_path()
                    end_time = time.time()
                    stats = {
                        'visited': visited_count,
                        'processed': processed_count,
                        'max_depth': max_depth,
                        'time': (end_time - start_time) * 1000
                    }
                    return solution, stats

                visited.add(state_str)
                visited_count += 1
                stack.append(child)

    # Brak rozwiązania - zwracamy pustą listę zamiast None
    end_time = time.time()
    stats = {
        'visited': visited_count,
        'processed': processed_count,
        'max_depth': max_depth,
        'time': (end_time - start_time) * 1000
    }
    return [], stats  # Zmieniłem None na pustą listę