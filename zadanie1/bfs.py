from collections import deque
import time
from puzzle import PuzzleState
from utils import get_possible_moves, apply_move


def bfs(initial_state, order='LRUD'):
    start_time = time.time()

    initial = PuzzleState(initial_state)
    if initial.is_goal():
        end_time = time.time()
        stats = {
            'length': 0,
            'visited': 1,
            'processed': 0,
            'max_depth': 0,
            'time': (end_time - start_time) * 1000  # czas w ms
        }
        return [], stats

    queue = deque([initial])  # kolejka FIFO
    visited = {str(initial.state)}  # odwiedzone stany
    visited_count = 1
    processed_count = 0
    max_depth = 0

    while queue:
        current = queue.popleft()
        processed_count += 1

        max_depth = max(max_depth, current.depth)

        # Generowanie i sortowanie możliwych ruchów według zadanego porządku
        possible_moves = get_possible_moves(current.state)
        sorted_moves = sorted(possible_moves, key=lambda x: order.index(x) if x in order else len(order))

        for move in sorted_moves:
            new_state = apply_move(current.state, move)
            state_str = str(new_state)

            if state_str not in visited:
                child = PuzzleState(new_state, current, move, current.depth + 1)

                if child.is_goal():
                    # Znaleziono rozwiązanie
                    solution = child.get_solution_path()
                    end_time = time.time()
                    stats = {
                        'length': len(solution),
                        'visited': visited_count,
                        'processed': processed_count,
                        'max_depth': max_depth,
                        'time': (end_time - start_time) * 1000
                    }
                    return solution, stats

                visited.add(state_str)
                visited_count += 1
                queue.append(child)

    # Brak rozwiązania
    end_time = time.time()
    stats = {
        'length': -1,
        'visited': visited_count,
        'processed': processed_count,
        'max_depth': max_depth,
        'time': (end_time - start_time) * 1000
    }
    return None, stats