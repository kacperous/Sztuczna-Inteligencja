class PuzzleState:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.width = len(state[0]) if state else 0
        self.height = len(state)

    def is_goal(self):
        # Sprawdza czy układanka jest w stanie docelowym
        flat = []
        for row in self.state:
            flat.extend(row)

        goal = list(range(1, self.width * self.height)) + [0]
        return flat == goal

    def get_solution_path(self):
        # Odtwarza ścieżkę rozwiązania od końca do początku
        path = []
        current = self
        while current.parent:
            path.append(current.action)
            current = current.parent
        return path[::-1]