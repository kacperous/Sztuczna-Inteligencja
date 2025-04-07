from utils import get_goal_position, get_possible_moves, apply_move
from puzzle import PuzzleState
import time
import heapq

def hamming(state, goal_state):
    distance = 0
    for i in range(len(state)):  # Iterujemy po wierszach stanu.
        for j in range(len(state[0])):  # Iterujemy po kolumnach.
            value = state[i][j]  # Pobieramy wartość w polu [i][j].
            if value != 0 and goal_state[value] != (i, j):  # Jeśli wartość nie jest na właściwym miejscu:
                distance += 1  # Zwiększamy odległość o 1.
    return distance  # Zwracamy liczbę kafelków w złych pozycjach.

def manhattan(state, goal_state):
    distance = 0
    for i in range(len(state)):  # Przechodzimy przez wiersze.
        for j in range(len(state[0])):  # Przechodzimy przez kolumny.
            value = state[i][j]  # Pobieramy wartość w polu.
            if value != 0:  # Ignorujemy kafelek `0`.
                goal_x, goal_y = goal_state[value]  # Znajdujemy docelową pozycję danego kafelka.
                distance += abs(i - goal_x) + abs(j - goal_y)  # Dodajemy odległość w poziomie i pionie.
    return distance

def astar(init_state, heuristic):
    start_time = time.time()  # Uruchamiamy licznik czasu.
    width = len(init_state[0])  # Szerokość planszy.
    height = len(init_state)  # Wysokość planszy.
    goal_position = get_goal_position(width, height)  # Docelowe pozycje puzzli.

    heuristic_func = manhattan if heuristic.lower() == 'manh' else hamming # Wybór heurystyki.

    initial = PuzzleState(init_state) # Ustalamy stan początkowy

    if initial.is_goal(): # Jeśli już na początku jesteśmy w układzie docelowym:
        end_time = time.time()
        stats = { # Tworzymy statystyki
            'visited': 1,
            'processed': 0,
            'max_depth': 0,
            'time': (end_time - start_time) * 1000
        }
        return [], stats # Zwróć pustą listę ruchów + statystyki

    open_set = [] # Kolejka priorytetowa
    counter = 0 # Licznik, by rozróżnić stany z tym samym f_score

    # Dodajemy stan początkowy do kolejki:
    f_score = heuristic_func(initial.state, goal_position) # Koszt f(n) = h(start).
    heapq.heappush(open_set, (f_score, counter, initial)) # Dodajemy stan do kolejki.
    counter += 1

    visited = {str(initial)}  # Zbiór odwiedzonych stanów.
    visited_count = 1  # Ile odwiedzono?
    processed_count = 0  # Ile przetworzono?
    max_depth = 0  # Maksymalna głębokość w drzewie

    while open_set:
        _,_, current = heapq.heappop(open_set) # Pobieramy stan o najniższym `f(n)` z kolejki.
        processed_count += 1
        max_depth = max(max_depth, current.depth) # Aktualizujemy maksymalną głębokość.

        if current.is_goal(): # Jest rowiązanie?
            solution = current.get_solution_path() # Pobierz je i zapisz statystyki
            end_time = time.time()
            stats = {
                'visited': visited_count,
                'processed': processed_count,
                'max_depth': max_depth,
                'time': (end_time - start_time) * 1000
            }
            return solution, stats

        for move in get_possible_moves(current.state): # Sprawdzamy możliwe ruchy.
            new_state = apply_move(current.state, move) # Tworzymy nowy stan z ruchem
            state_str = str(new_state) # Żeby łatwiej porównywać to zmieniamy na stringa

            if state_str not in visited: # Czy ten stan już był odwiedzony?
                child = PuzzleState(new_state, current, move, current.depth + 1) # Tworzymy obiekt "dziecka".
                h_score = heuristic_func(new_state, goal_position) # Liczymy heurystykę h(n).
                f_score = child.depth + h_score  # Całkowity koszt f(n).

                heapq.heappush(open_set, (f_score, counter, child)) # Dodajemy dziecko do kolejki.
                counter += 1
                visited.add(state_str)
                visited_count += 1

    end_time = time.time()
    stats = { # Jeśli nie znaleziono rozwiązani
        'visited': visited_count,
        'processed': processed_count,
        'max_depth': max_depth,
        'time': (end_time - start_time) * 1000
    }
    return None, stats