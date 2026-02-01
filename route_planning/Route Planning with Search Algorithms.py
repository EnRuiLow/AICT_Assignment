import math
from collections import deque
import heapq
import time

stations = {
    # East-West / Downtown Line
    "Changi Airport": (10, 2),
    "Expo": (9, 3),
    "Upper Changi": (8.6, 3.4),
    "Tanah Merah": (8, 4),
    "Simei": (7.6, 4.2),
    "Tampines": (7, 4),
    "Tampines East": (7.4, 3.6),
    "Paya Lebar": (6, 5),
    "Bugis": (4, 5.5),
    "City Hall": (4, 6),
    "Lavender": (3.8, 5.8),
    "Kallang": (3.6, 6),
    "Aljunied": (3.5, 6.2),
    "Eunos": (7, 5),
    "Kembangan": (6.5, 4.5),
    "Bedok": (6, 4),

    # North-South / Circle Line
    "Bishan": (4, 8),

    "Serangoon": (6, 8),
    "Bartley": (7, 8),
    "Tai Seng": (7.5, 7),
    "MacPherson": (8, 6.5),
    "Braddell": (4, 7),
    "Toa Payoh": (4.5, 6.5),
    "Novena": (5, 6),
    "Newton": (5.5, 5.8),
    "Somerset": (5.7, 5.5),
    "Dhoby Ghaut": (5.8, 5.2),
    "Orchard": (3, 7),
    "Raffles Place": (3, 5.5),

    # Circle Line towards Marina Bay
    "Dakota": (5.5, 4.5),
    "Mountbatten": (6, 4.7),
    "Stadium": (6.2, 4.4),
    "Nicoll Highway": (6.5, 4.2),
    "Promenade": (6.8, 4),
    "Bayfront": (6.9, 3.8),

    # Thomson-East Coast Line
    "Marina Bay": (6, 5),
    "Gardens by the Bay": (5, 4)
}



# --------------------------
# 2️⃣ Station lines
# --------------------------
station_line = {
    "Changi Airport": "EWL",
    "Expo": "EWL",
    "Upper Changi": "DTL",
    "Tanah Merah": "EWL",
    "Simei": "EWL",
    "Tampines": "EWL",
    "Tampines East": "DTL",
    "Paya Lebar": "EWL",
    "Bugis": "DTL/EWL",
    "City Hall": "NSL",
    "Orchard": "NSL",
    "Bishan": "NSL/CCL",
    "Lorong Chuan": "CCL",
    "Serangoon": "CCL",
    "Bartley": "CCL",
    "Tai Seng": "CCL",
    "MacPherson": "CCL",
    "Braddell": "NSL",
    "Toa Payoh": "NSL",
    "Novena": "NSL",
    "Newton": "NSL",
    "Somerset": "NSL",
    "Dhoby Ghaut": "NSL/EWL",
    "Lavender": "EWL",
    "Kallang": "EWL",
    "Aljunied": "EWL",
    "Eunos": "EWL",
    "Kembangan": "EWL",
    "Bedok": "EWL",
    "Dakota": "CCL",
    "Mountbatten": "CCL",
    "Stadium": "CCL",
    "Nicoll Highway": "CCL",
    "Promenade": "CCL",
    "Bayfront": "CCL",
    "Raffles Place": "NSL/TECL",
    "Marina Bay": "TECL",
    "Gardens by the Bay": "TECL"
}


# --------------------------
# 3️⃣ Today graph with weights (minutes)
# --------------------------
graph_today = {
    # Downtown / East-West Line from Tampines
    "Tampines": {"Tampines East": 2, "Simei": 2,},
    "Tampines East": {"Upper Changi": 2, "Tampines": 2},
    "Upper Changi": {"Expo": 2, "Tampines East": 2},
    "Simei": {"Tanah Merah": 2, "Tampines": 2},
    "Tanah Merah": {"Expo": 3, "Bedok": 3},
    "Expo": {"Changi Airport": 2, "Tanah Merah": 3},
    "Changi Airport": {"Expo": 2},

    "Paya Lebar": {"MacPherson": 2, "Eunos": 2, "Dakota": 2},
    "Bugis": {"City Hall": 2, "Lavender": 2,"Promenade":2},
    "City Hall": {"Bugis": 2, "Dhoby Ghaut": 2, "Raffles Place": 2},
    "Orchard": {"City Hall": 2, "Somerset": 2, "Newton": 2},
    "Somerset": {"Orchard": 2, "Dhoby Ghaut": 2},
    "Dhoby Ghaut": {"Somerset": 2, "City Hall": 2},
    "Lavender": {"Bugis": 2, "Kallang": 2},
    "Kallang": {"Lavender": 2, "Aljunied": 2},
    "Aljunied": {"Kallang": 2, "Paya Lebar": 2},
    "Eunos": {"Paya Lebar": 2, "Kembangan": 2},
    "Kembangan": {"Eunos": 2, "Bedok": 2},
    "Bedok": {"Kembangan": 2, "Tanah Merah": 3},

    # Circle / NSL routes from Bishan
    "Bishan": {"Lorong Chuan": 3, "Braddell": 3},
    "Lorong Chuan": {"Bishan": 3, "Serangoon": 2},
    "Serangoon": {"Lorong Chuan": 2, "Bartley": 2},
    "Bartley": {"Serangoon": 2, "Tai Seng": 2},
    "Tai Seng": {"Bartley": 2, "MacPherson": 2},
    "MacPherson": {"Tai Seng": 2, "Paya Lebar": 2},

    "Braddell": {"Bishan": 3, "Toa Payoh": 2},
    "Toa Payoh": {"Braddell": 2, "Novena": 2},
    "Novena": {"Toa Payoh": 2, "Newton": 2},
    "Newton": {"Novena": 2, "Orchard": 2},

    # Circle Line from Paya Lebar to Marina Bay
    "Dakota": {"Paya Lebar": 2, "Mountbatten": 2},
    "Mountbatten": {"Dakota": 2, "Stadium": 2},
    "Stadium": {"Mountbatten": 2, "Nicoll Highway": 2},
    "Nicoll Highway": {"Stadium": 2, "Promenade": 2},
    "Promenade": {"Nicoll Highway": 2, "Bayfront": 2},
    "Bayfront": {"Promenade": 2, "Marina Bay": 2},

    # Thomson-East Coast Line
    "Marina Bay": {"Raffles Place": 3, "Gardens by the Bay": 2},
    "Gardens by the Bay": {}
}





import math
from collections import deque
import heapq
import time
# ------------------------------
# Future stations with coordinates
# ------------------------------
future_stations = {
    # East-West / Downtown Line stations
    "Tampines": (7, 4),
    "Tampines East": (7.4, 3.6),
    "Simei": (7.6, 4.2),
    "Tanah Merah": (8, 4),
    "Expo": (9, 3),
    "Upper Changi": (8.6, 3.4),
    "Bedok": (6, 4),
    "Kembangan": (6.5, 4.5),
    "Eunos": (7, 5),
    "Paya Lebar": (6, 5),
    "Aljunied": (3.5, 6.2),
    "Kallang": (3.6, 6),
    "Lavender": (3.8, 5.8),
    "Bugis": (4, 5.5),
    "City Hall": (4, 6),
    "Raffles Place": (3, 6),
    "Marina Bay": (6, 5),

    # Future Cross Island Line (CRL) stations
    "Pasir Ris": (10, 5),
    "Pasir Ris East": (10.2, 4),
    "Loyang": (10.4, 3.8),
    "Aviation Park": (10.6, 3.5),
    "Changi Terminal 5": (10.8, 3.2),
    "Ang Mo Kio": (4, 8.5),
    "Tavistock": (5, 8.8),
    "Serangoon North": (6, 9),
    "Hougang": (7, 9),
    "Defu": (7.5, 8.5),
    "Tampines North": (7, 5),
    "Lorong Chuan": (5, 8),

    # Thomson-East Coast Line (TECL) extension
    "Changi Airport": (10, 2),
    "Sungei Bedok": (10.5, 3),
    "Bedok South": (10, 3.5),
    "Bayshore": (9.5, 4),
    "Siglap": (9, 4.5),
    "Marine Terrace": (8.5, 5),
    "Marine Parade": (8, 5.5),
    "Tanjong Katong": (7.5, 6),
    "Katong Park": (7, 6.5),
    "Tanjong Rhu": (6.5, 7),
    "Gardens by the Bay": (5, 4),

    # Circle Line
    "Dakota": (5.5, 4.5),
    "Mountbatten": (6, 4.7),
    "Stadium": (6.2, 4.4),
    "Nicoll Highway": (6.5, 4.2),
    "Promenade": (6.8, 4),
    "Bayfront": (6.9, 3.8),
    "Bishan": (4, 8),
    "Serangoon": (6, 8),
    "Bartley": (7, 8),
    "Tai Seng": (7.5, 7),
    "MacPherson": (8, 6.5),
    "Braddell": (4, 7),
    "Toa Payoh": (4, 7.5),
    "Novena": (4, 6.5),
    "Newton": (4, 6),
    "Orchard": (4, 5.5),
    "Dhoby Ghaut": (3.5, 5.5),
    "Marina South Pier": (6, 2.5),
    "Somerset": (3.0, 5.5),
}

# ------------------------------
# Future station lines
# ------------------------------
future_station_line = {
    # East-West / Downtown Line
    "Tampines": "EWL",
    "Tampines East": "DTL",
    "Simei": "EWL",
    "Tanah Merah": "EWL/TECL",
    "Expo": "DTL/TECL",
    "Upper Changi": "DTL",
    "Bedok": "EWL",
    "Kembangan": "EWL",
    "Eunos": "EWL",
    "Paya Lebar": "EWL",
    "Aljunied": "EWL",
    "Kallang": "EWL",
    "Lavender": "EWL",
    "Bugis": "EWL/DTL",
    "City Hall": "NSL",
    "Raffles Place": "NSL",
    "Marina Bay": "NSL/TECL/CCL",

    # Cross Island Line (CRL)
    "Pasir Ris": "EWL/CRL",
    "Pasir Ris East": "CRL",
    "Loyang": "CRL",
    "Aviation Park": "CRL",
    "Changi Terminal 5": "CRL/TECL",
    "Ang Mo Kio": "CRL",
    "Tavistock": "CRL",
    "Serangoon North": "CRL",
    "Hougang": "CRL",
    "Defu": "CRL",
    "Tampines North": "CRL",
    "Lorong Chuan": "CCL",

    # Thomson-East Coast Line (TECL)
    "Changi Airport": "TECL",
    "Sungei Bedok": "TECL",
    "Bedok South": "TECL",
    "Bayshore": "TECL",
    "Siglap": "TECL",
    "Marine Terrace": "TECL",
    "Marine Parade": "TECL",
    "Tanjong Katong": "TECL",
    "Katong Park": "TECL",
    "Tanjong Rhu": "TECL",
    "Gardens by the Bay": "TECL",

    # Circle Line
    "Dakota": "CCL",
    "Mountbatten": "CCL",
    "Stadium": "CCL",
    "Nicoll Highway": "CCL",
    "Promenade": "CCL",
    "Bayfront": "CCL",
    "Bishan": "NSL/CRL",
    "Serangoon": "CCL",
    "Bartley": "CCL",
    "Tai Seng": "CCL",
    "MacPherson": "CCL",
    "Braddell": "NSL",
    "Toa Payoh": "NSL",
    "Novena": "NSL",
    "Newton": "NSL",
    "Orchard": "NSL",
    "Dhoby Ghaut": "NSL/CCL/DTL",
    "Marina South Pier": "NSL"
}

# ------------------------------
# Future graph (today / future)
# ------------------------------
future_graph_today = {
    # EWL / DTL
    "Tampines": {"Pasir Ris": 1, "Tampines East": 2, "Simei": 2},
    "Tampines East": {"Tampines": 2, "Upper Changi": 2},
    "Upper Changi": {"Tampines East": 2, "Expo": 2},
    "Simei": {"Tampines": 2, "Tanah Merah": 2},
    "Tanah Merah": {"Simei": 2, "Expo": 3, "Bedok": 2},
    "Expo": {"Upper Changi": 2, "Tanah Merah": 3, "Changi Airport": 2},
    "Changi Airport": {"Expo": 2, "Tanah Merah": 5, "Changi Terminal 5": 2},
    "Bedok": {"Tanah Merah": 2, "Kembangan": 2},
    "Kembangan": {"Bedok": 2, "Eunos": 2},
    "Eunos": {"Kembangan": 2, "Paya Lebar": 2},
    "Paya Lebar": {"Eunos": 2, "Aljunied": 2, "Dakota": 2},
    "Aljunied": {"Paya Lebar": 2, "Kallang": 2},
    "Kallang": {"Aljunied": 2, "Lavender": 2},
    "Lavender": {"Kallang": 2, "Bugis": 2},
    "Bugis": {"Lavender": 2, "City Hall": 2, "Promenade": 2},
    "City Hall": {"Bugis": 2, "Raffles Place": 2},
    "Raffles Place": {"City Hall": 2, "Marina Bay": 3},
    "Marina Bay": {"Raffles Place": 3, "Gardens by the Bay": 2, "Bayfront": 2},
    "Gardens by the Bay": {"Marina Bay": 2, "Tanjong Rhu": 2},

    # TECL extension
    "Sungei Bedok": {"Changi Terminal 5": 2, "Bedok South": 2},
    "Bedok South": {"Sungei Bedok": 2, "Bayshore": 2},
    "Bayshore": {"Bedok South": 2, "Siglap": 2},
    "Siglap": {"Bayshore": 2, "Marine Terrace": 2},
    "Marine Terrace": {"Siglap": 2, "Marine Parade": 2},
    "Marine Parade": {"Marine Terrace": 2, "Tanjong Katong": 2},
    "Tanjong Katong": {"Marine Parade": 2, "Katong Park": 2},
    "Katong Park": {"Tanjong Katong": 2, "Tanjong Rhu": 2},
    "Tanjong Rhu": {"Katong Park": 2, "Gardens by the Bay": 2},
    "Changi Terminal 5": {"Changi Airport": 2, "Aviation Park": 2, "Sungei Bedok": 2},

    # CRL branch
    "Pasir Ris": {"Tampines": 2, "Pasir Ris East": 2},
    "Pasir Ris East": {"Pasir Ris": 2, "Loyang": 2},
    "Loyang": {"Pasir Ris East": 2, "Aviation Park": 2},
    "Aviation Park": {"Loyang": 2, "Changi Terminal 5": 2},
    "Ang Mo Kio": {"Bishan": 2, "Tavistock": 2},
    "Tavistock": {"Ang Mo Kio": 2, "Serangoon North": 2},
    "Serangoon North": {"Tavistock": 2, "Hougang": 3},
    "Hougang": {"Serangoon North": 3, "Defu": 2},
    "Defu": {"Hougang": 2, "Tampines North": 3},
    "Tampines North": {"Defu": 3, "Pasir Ris": 2},
    "Lorong Chuan": {"Bartley": 2, "Serangoon": 2},
    "Bishan": {"Ang Mo Kio": 2, "Serangoon": 3, "Bartley": 3},
    "Serangoon": {"Bishan": 3, "Lorong Chuan": 2},
    "Bartley": {"Bishan": 3, "Lorong Chuan": 2, "Tai Seng": 2},
    "Tai Seng": {"Bartley": 2, "MacPherson": 2},
    "MacPherson": {"Tai Seng": 2},
    
    # Circle Line / other
    "Dakota": {"Paya Lebar": 2, "Mountbatten": 2},
    "Mountbatten": {"Dakota": 2, "Stadium": 2},
    "Stadium": {"Mountbatten": 2, "Nicoll Highway": 2},
    "Nicoll Highway": {"Stadium": 2, "Promenade": 2},
    "Promenade": {"Nicoll Highway": 2, "Bayfront": 2},
    "Bayfront": {"Promenade": 2, "Marina Bay": 2},
    "Braddell": {"Toa Payoh": 2, "Bishan": 2},
    "Toa Payoh": {"Novena": 2, "Braddell": 2},
    "Novena": {"Newton": 2, "Toa Payoh": 2},
    "Newton": {"Orchard": 2, "Novena": 2},
    "Orchard": {"Dhoby Ghaut": 2, "Newton": 2},
    "Dhoby Ghaut": {"Orchard": 2, "City Hall": 2},
    "Marina South Pier": {"Marina Bay": 2},
}



# --------------------------
# 4️⃣ Heuristic function
# --------------------------
def heuristic(a, b):
    x1, y1 = future_stations[a]
    x2, y2 = future_stations[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# --------------------------
# 5️⃣ Path cost with transfer penalty
# --------------------------
def path_cost_with_transfer(path, graph, station_line, transfer_penalty=2):
    cost = 0
    for i in range(len(path)-1):
        cost += graph[path[i]][path[i+1]]
        if station_line.get(path[i]) != station_line.get(path[i+1]):
            cost += transfer_penalty
    return cost


# --------------------------
# 6️⃣ BFS
# --------------------------
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            return path, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, nodes_expanded

# --------------------------
# 7️⃣ DFS
# --------------------------
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()
    nodes_expanded = 0

    while stack:
        path = stack.pop()
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            return path, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)

    return None, nodes_expanded

# --------------------------
# 8️⃣ GBFS
# --------------------------
def greedy_bfs(graph, start, goal):
    pq = []
    heapq.heappush(pq, (heuristic(start, goal), [start]))
    visited = set()
    nodes_expanded = 0

    while pq:
        _, path = heapq.heappop(pq)
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            return path, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(pq, (heuristic(neighbor, goal), new_path))

    return None, nodes_expanded

# --------------------------
# 9️⃣ A* Search
# --------------------------
def astar(graph, start, goal, station_line, transfer_penalty=2):
    pq = []
    heapq.heappush(pq, (0 + heuristic(start, goal), 0, [start]))
    visited = set()
    nodes_expanded = 0

    while pq:
        f, g, path = heapq.heappop(pq)
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            return path, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor, cost in graph.get(node, {}).items():
                extra = transfer_penalty if station_line.get(node) != station_line.get(neighbor) else 0
                new_g = g + cost + extra
                new_f = new_g + heuristic(neighbor, goal)
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(pq, (new_f, new_g, new_path))

    return None, nodes_expanded



import time

import time

import time

def compare_today_future(today_graph, today_line, future_graph, future_line, od_pairs):
    for start, goal in od_pairs:
        print("="*80)
        print(f"Origin: {start} → Destination: {goal}\n")

        # -------- TODAY --------
        print("TODAY:")
        for alg_name, func in [("BFS", bfs), ("DFS", dfs), ("GBFS", greedy_bfs), ("A*", astar)]:
            t_start = time.perf_counter()
            if alg_name == "A*":
                path, nodes = func(today_graph, start, goal, today_line)
            else:
                path, nodes = func(today_graph, start, goal)
            t_time = int((time.perf_counter() - t_start) * 1_000_000)  # microseconds
            cost = path_cost_with_transfer(path, today_graph, today_line)
            print(f"{alg_name:<5} → Path: {path}, Cost: {cost}, Nodes: {nodes}, Time: {t_time} µs")
        
        # -------- FUTURE --------
        print("\nFUTURE:")
        for alg_name, func in [("BFS", bfs), ("DFS", dfs), ("GBFS", greedy_bfs), ("A*", astar)]:
            f_start = time.perf_counter()
            if alg_name == "A*":
                path, nodes = func(future_graph, start, goal, future_line)
            else:
                path, nodes = func(future_graph, start, goal)
            f_time = int((time.perf_counter() - f_start) * 1_000_000)  # microseconds
            cost = path_cost_with_transfer(path, future_graph, future_line)
            print(f"{alg_name:<5} → Path: {path}, Cost: {cost}, Nodes: {nodes}, Time: {f_time} µs")

        print("="*80 + "\n")






# Helper function to time algorithms
def run_algorithm(func, graph, start, goal, line=None):
    t_start = time.time()
    if line:
        path, nodes = func(graph, start, goal, line)
    else:
        path, nodes = func(graph, start, goal)
    t_time = time.time() - t_start
    return path, nodes, t_time




od_pairs = [
     ("Changi Airport", "Marina Bay"),
     ("Changi Airport", "Gardens by the Bay"),
    ("Changi Airport", "Promenade"),
    ("Bishan", "Changi Airport"),
    ("Tampines", "Changi Airport"),
    
]

compare_today_future(graph_today, station_line, future_graph_today, future_station_line, od_pairs)












