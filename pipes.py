from collections import deque

def find_connected_sinks(file_path):
    grid = {}
    source = None
    sinks = set()

    def is_connected(cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        dx, dy = abs(x1 - x2), abs(y1 - y2)

        if dx + dy != 1:  # Cells are not adjacent
            return False

        pipe1, pipe2 = grid.get(cell1, ''), grid.get(cell2, '')

        if '*' in (pipe1, pipe2):  # Source/sink connects to everything
            return True

        connections = {
            '═': [(1, 0), (-1, 0)],
            '║': [(0, 1), (0, -1)],
            '╔': [(0, 1), (-1, 0)],
            '╗': [(0, 1), (1, 0)],
            '╚': [(0, -1), (-1, 0)],
            '╝': [(0, -1), (1, 0)],
            '╠': [(1, 0), (-1, 0), (0, 1)],
            '╣': [(1, 0), (-1, 0), (0, -1)],
            '╦': [(1, 0), (-1, 0), (0, -1)],
            '╩': [(1, 0), (-1, 0), (0, 1)],
        }

        return any(
            (x2 - x1, y2 - y1) in connections.get(pipe1, [])
            and (x1 - x2, y1 - y2) in connections.get(pipe2, [])
        )

    def bfs(start):
        visited = set()
        queue = deque([start])
        connected_sinks = set()

        while queue:
            x, y = queue.popleft()
            visited.add((x, y))

            if grid[(x, y)] in sinks:
                connected_sinks.add(grid[(x, y)])

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in grid and (nx, ny) not in visited and is_connected((x, y), (nx, ny)):
                    queue.append((nx, ny))

        return connected_sinks

    # Read the file and populate the grid
    with open(file_path, 'r') as file:
        for line in file:
            obj, x, y = line.strip().split()
            x, y = int(x), int(y)
            grid[(x, y)] = obj
            if obj == '*':
                source = (x, y)
            elif obj.isupper():
                sinks.add(obj)

    # Error handling for missing source
    if source is None:
        raise ValueError("Source ('*') not found in the input file.")

    connected_sinks = bfs(source)
    return ''.join(sorted(connected_sinks)) python pipes.py 
