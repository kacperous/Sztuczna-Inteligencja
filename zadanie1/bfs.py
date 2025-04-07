from collections import deque
import time
from puzzle import PuzzleState
from utils import get_possible_moves, apply_move


def bfs(initial_state, order='LRUD'):
    start_time = time.time() # Mierzymy, kiedy zaczęto algorytm.

    initial = PuzzleState(initial_state) # Tworzymy "stan gry" na podstawie układanki początkowej.
    if initial.is_goal():  # Czy od razu jest gotowe? Sprawdzamy metodą is_goal().
        end_time = time.time()
        stats = {  # Zbieramy statystyki.
            'length': 0,  # Długość rozwiązania (liczba kroków), tu wynosi 0.
            'visited': 1,  # Liczba odwiedzonych stanów (tu: początkowy).
            'processed': 0,  # Nic nie przetwarzaliśmy, bo to gotowe.
            'max_depth': 0,  # Maksymalna głębokość przeszukiwania to 0.
            'time': (end_time - start_time) * 1000  # Mierzony czas w milisekundach.
        }
        return [], stats  # Zwracamy pustą ścieżkę (bo układanka gotowa) i statystyki

    queue = deque([initial])  # Tworzymy kolejkę (FIFO) z początkowego stanu.
    visited = {str(initial.state)}  # Zapisujemy odwiedzony stan (na razie: tylko początek).

    visited_count = 1  # Dzięki zmiennej "visited_count" liczymy odwiedzone stany.
    processed_count = 0  # Procesujemy na razie 0.
    max_depth = 0  # Głębokość drzewa (zaczyna się od 0).

    while queue:  # Dopóki mamy coś w kolejce, pracujemy.
        current = queue.popleft()  # Pobieramy pierwszy element (stan gry).
        processed_count += 1  # Zwiększamy licznik przetworzonych stanów.

        max_depth = max(max_depth, current.depth)  # Aktualizujemy maksymalną głębokość.

        # Generujemy możliwe ruchy i sortujemy wg kolejności (np. 'LRUD').
        possible_moves = get_possible_moves(current.state)
        sorted_moves = sorted(possible_moves, key=lambda x: order.index(x))

        for move in sorted_moves:  # Dla każdego ruchu:
            new_state = apply_move(current.state, move)  # Tworzymy nowy stan po wykonaniu ruchu.
            state_str = str(new_state)  # Zamieniamy na string dla łatwego porównania.

            if state_str not in visited:  # Jeżeli tego stanu wcześniej nie widzieliśmy:
                child = PuzzleState(new_state, current, move, current.depth + 1)  # Nowy stan „dziecko”.
                max_depth = max(max_depth, child.depth)

                if child.is_goal(): # Jeśli układanka gotowa:
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

                visited.add(state_str) # Zapisujemy ten stan jako odwiedzony.
                visited_count += 1 # Liczymy odwiedzenia.
                queue.append(child) # Dodajemy ten stan jako element do przetworzenia (kolejka).

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