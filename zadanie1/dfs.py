import time
from puzzle import PuzzleState
from utils import get_possible_moves, apply_move

def dfs(initial_state, order='LRUD'):
    start_time = time.time() # Startujemy licznik czasu.

    max_search_depth = 20 # Maksymalna głębokość przeszukiwania (zabezpieczenie)

    initial = PuzzleState(initial_state)  # Tworzymy obiekt stanu gry na podstawie układanki początkowej.
    if initial.is_goal():  # Jeśli od razu mamy ułożoną układankę, kończymy.
        end_time = time.time()  # Zapisujemy czas rozwiązania.
        stats = {
            'visited': 1,  # Odwiedzono tylko 1 stan (początkowy).
            'processed': 0,  # Brak przetworzonych stanów.
            'max_depth': 0,  # Głębokość 0.
            'time': (end_time - start_time) * 1000
        }
        return [], stats  # Zwracamy pustą ścieżkę i statystyki.

    stack = [initial]  # STOS LIFO: będziemy tam wrzucać elementy do przetwarzania.
    visited = {str(initial.state)}  # Odwiedzone stany.
    visited_count = 1  # Licznik odwiedzonych stanów.
    processed_count = 0  # Licznik przetworzonych stanów.
    max_depth = 0  # Śledzimy maksymalną głębokość, na jaką zeszliśmy.

    while stack:  # Dopóki stos nie jest pusty:
        current = stack.pop()  # Zdejmujemy ze stosu *ostatni* dodany element.
        processed_count += 1  # Liczymy przetworzone stany.

        max_depth = max(max_depth, current.depth)  # Aktualizujemy maksymalną głębokość.

        # Sprawdzamy, czy przypadkiem nie osiągnęliśmy maksymalnej głębokości szukania.
        if current.depth >= max_search_depth:
            continue  # Jeżeli tak, pomijamy ten stan (wracamy do pętli).

        # Generujemy możliwe ruchy i ustawiamy ich kolejność zgodnie z 'order'.
        possible_moves = get_possible_moves(current.state) # Pobieramy możliwe ruchy (np. L, R, U, D).
        sorted_moves = sorted(possible_moves, key=lambda x: order.index(x) if x in order else len(order))

        sorted_moves.reverse() # Odwracamy kolejność, bo stos działa jak LIFO (Last In, First Out).

        for move in sorted_moves:  # Iterujemy po możliwych ruchach.
            new_state = apply_move(current.state, move)  # Tworzymy nowy stan po wykonaniu ruchu.
            state_str = str(new_state)  # Zamieniamy stan na string, żeby łatwo porównać.

            if state_str not in visited:  # Jeśli ten stan nie był jeszcze odwiedzony:
                child = PuzzleState(new_state, current, move, current.depth + 1)  # Tworzymy nowy obiekt stanu.
                max_depth = max(max_depth, child.depth)  # Aktualizujemy głębokość.

                if child.is_goal(): # Jeśli układanka została ułożona:
                    solution = child.get_solution_path()
                    end_time = time.time()
                    stats = {
                        'visited': visited_count,
                        'processed': processed_count,
                        'max_depth': max_depth,
                        'time': (end_time - start_time) * 1000
                    }
                    return solution, stats

                visited.add(state_str)  # Dodajemy stan do odwiedzonych.
                visited_count += 1
                stack.append(child)  # Dodajemy dziecko do stosu (LIFO).

    # Jeżeli rozwiązania brak:
    end_time = time.time()
    stats = {
        'visited': visited_count,
        'processed': processed_count,
        'max_depth': max_depth,
        'time': (end_time - start_time) * 1000
    }
    return [], stats  # Zwracamy pustą ścieżkę i statystyki.