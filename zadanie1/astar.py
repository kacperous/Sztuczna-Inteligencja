from utils import get_goal_position, get_possible_moves, apply_move
from puzzle import PuzzleState
import time
import heapq

# PROSTE OBJAŚNIENIA JAK DLA STUDENTA DEBILA

def hamming(state, goal_state):
    distance = 0
    for i in range(len(state)):  # Dla każdej wiersza w stanie
        for j in range(len(state[0])):  # Dla każdej kolumny w stanie
            value = state[i][j]  # Pobierz wartość w polu [i][j]
            if value != 0 and goal_state[value] != (i, j):  # Jeśli to nie puste (0) i nie jest na właściwej pozycji
                distance += 1  # Dodaj 1 do liczby błędów
    return distance  # Zwracamy ile jest błędów (elementów na złym miejscu)

def manhattan(state, goal_state):
    distance = 0
    for i in range(len(state)):  # Iteruje po wierszach
        for j in range(len(state[0])):  # Iteruje po kolumnach
            value = state[i][j]  # Pobiera wartość w polu
            if value != 0:  # Pusty klocek (0) ignorujemy
                goal_x, goal_y = goal_state[value]  # Pobieramy właściwą pozycję tego klocka
                distance += abs(i - goal_x) + abs(j - goal_y)  # Dodajemy odległość (suma różnic wierszy i kolumn)
    return distance

def astar(init_state, heuristic):
    start_time = time.time()
    width = len(init_state[0])  # Szerokość planszy
    height = len(init_state)  # Wysokość planszy
    goal_position = get_goal_position(width, height)  # Pobieramy układ docelowy klocków/ tam gdzie ich miejsce

    heuristic_func = manhattan if heuristic.lower() == 'manh' else hamming

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

    # f_score = g_score (głębokość) + h_score (heurystyka)
    f_score = heuristic_func(initial.state, goal_position) # Liczymy f(n) = h(start)
    heapq.heappush(open_set, (f_score, counter, initial)) # Dodaj stan początkowy do kolejki
    counter += 1

    visited = {str(initial)}  # Zbiór odwiedzonych stanów
    visited_count = 1  # Ile odwiedzono?
    processed_count = 0  # Ile przetworzono?
    max_depth = 0  # Maksymalna głębokość w drzewie

    while open_set:
        _,_, current = heapq.heappop(open_set) # Pobieramy stan o najniższym f(n)
        processed_count += 1
        max_depth = max(max_depth, current.depth)

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

        for move in get_possible_moves(current.state): # Sprawdzamy gdzie się możemy ruszyć
            new_state = apply_move(current.state, move) # Tworzymy nowy stan z ruchem
            state_str = str(new_state) # Żeby łatwiej porównywać to zmieniamy na stringa

            if state_str not in visited: # Czy ten stan już był odwiedzony?
                child = PuzzleState(new_state, current, move, current.depth + 1) # Tworzymy nowego "dzieciaka"
                h_score = heuristic_func(new_state, goal_position) # Obliczamy heurystyke czy jak to tam sie pisze
                f_score = child.depth + h_score  # g_score + h_score, czyli łączny koszt f(n)

                heapq.heappush(open_set, (f_score, counter, child)) #Kolejkujemy (dodajemy do kolejki)
                counter += 1
                visited.add(state_str) # Te to w miare jasne chyba
                visited_count += 1

    end_time = time.time()
    stats = {
        'visited': visited_count,
        'processed': processed_count,
        'max_depth': max_depth,
        'time': (end_time - start_time) * 1000
    }
    return None, stats