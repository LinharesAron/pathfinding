from display import Window, Point


class PathFinding:
    class Path:
        def __init__(self, estado, g, h, parent):
            self.estado = estado
            self.g_cost = g
            self.h_cost = h
            self.parent = parent
        
        @property
        def f_cost(self):
            return self.g_cost + self.h_cost

        def __eq__(self, othr):
            return ((isinstance(othr, type(self))
                    and self.estado == othr.estado) or
                    (isinstance(othr, type(self.estado))
                    and self.estado == othr))

        def __hash__(self):
            return hash(self.estado)

    def __init__(self):
        self.open = []
        self.close = set()

    def get_conexao_path(self, estado, end_point, parent):
        for conexao in estado.conexao:
            if conexao.espaco in self.open:
                yield  True, conexao.custo, [ item for item in self.open if item.estado == conexao.espaco][0]
            else:
                yield False, conexao.custo, self.Path(conexao.espaco, conexao.custo, estado.point.distance_to(end_point), parent)
            

    def repro_path(self, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = current.parent
        return list(reversed(path))
    
    def find_path(self, start, end):
        start = self.Path(start, 0, start.point.distance_to(end.point), None)
        end = self.Path(end, 0, 0, None)

        self.open.append(start)
        while self.open:
            current = self.open[0]
            for b in self.open:
                if b.f_cost < current.f_cost or (b.f_cost == current.f_cost and b.h_cost < current.h_cost):
                    current = b
            
            self.open.remove(current)
            self.close.add(current)

            if current == end:
                return [start] + self.repro_path(start, current)

            for is_in_open, g_cost, next_path in self.get_conexao_path(current.estado, end.estado.point, current):
                if next_path in self.close:
                    continue

                if is_in_open:
                    new_g_cost = current.g_cost + g_cost
                    if new_g_cost < next_path.g_cost:
                        next_path.g_cost = new_g_cost
                        next_path.parent = current
                else:
                    self.open.append(next_path)



class Conexao:
    def __init__(self, custo, espaco):
        self.custo = custo
        self.espaco = espaco

class Espaco:
    def __init__(self, label, point):
        self.label = label
        self.point = point
        self.conexao = []

    def conecta_espaco(self, custo, espaco):
        self.conexao.append(Conexao(custo, espaco))

def call_on_update(event):
    # print(event)
    if window.is_quit(event.type):
        window.stop()

window = Window(1000, 1000, "pathfinding")
window.draw_grid()

espacos = {
    "A": Espaco("A", Point(0, 0)),
    "B": Espaco("B", Point(2, 0)),
    "C": Espaco("C", Point(0, 2)),
    "D": Espaco("D", Point(2, 2)),
    "E": Espaco("E", Point(4, 3)),
    "F": Espaco("F", Point(0, 4)),
}

espacos["A"].conecta_espaco(5, espacos["B"])
espacos["B"].conecta_espaco(5, espacos["A"])

espacos["A"].conecta_espaco(5, espacos["C"])
espacos["C"].conecta_espaco(5, espacos["A"])

espacos["C"].conecta_espaco(7.5, espacos["B"])
espacos["B"].conecta_espaco(7.5, espacos["C"])

espacos["F"].conecta_espaco(45, espacos["B"])
espacos["B"].conecta_espaco(45, espacos["F"])

espacos["C"].conecta_espaco(5, espacos["F"])
espacos["F"].conecta_espaco(5, espacos["C"])

espacos["F"].conecta_espaco(7.5, espacos["D"])
espacos["D"].conecta_espaco(7.5, espacos["F"])

espacos["F"].conecta_espaco(15, espacos["E"])
espacos["E"].conecta_espaco(15, espacos["F"])

espacos["E"].conecta_espaco(5, espacos["D"])
espacos["D"].conecta_espaco(5, espacos["E"])

for espaco in espacos.values():
    window.draw_circle(Point(espaco.point.x, espaco.point.y))
    window.draw_letter(espaco.point, espaco.label)
    for conexao in espaco.conexao:
        window.draw_line(espaco.point, conexao.espaco.point, thickness=5)

start = espacos["A"]
end = espacos["E"]

pathfinding = PathFinding()

path = pathfinding.find_path(start, end)

for i in range(0, len(path) - 1):
    window.draw_line(path[i].estado.point, path[i+1].estado.point, thickness=5, colour=(255,0,0))

window.run(call_on_update)