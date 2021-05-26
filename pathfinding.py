from display import Window, Point


class PathFinding:
    class Path:
        def __init__(self, estado, g, h, parent):
            self.estado = estado
            self.g_cost = g
            self.h_cost = h
            self.parent = parent
        
        def f_cost(self):
            return self.g + self.h

        def __eq__(self, othr):
            return (isinstance(othr, type(self))
                    and self.estado == othr.estado)

        def __hash__(self):
            return hash(self.estado)

    def __init__(self):
        self.open = []
        self.close = set()
        self.paths = {}

    def get_conexao_path(self, estado):
        for conexao in estado.conexao:
            yield self.paths.setdefault(conexao, self.Path(conexao.espaco, conexao.custo, 0, None))

    def repro_path(self, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = current.parent
        return reversed(path)
    
    def find_path(self, start, end):
        start = self.Path(start, 0, start.point.distance_to(end.point), None)
        end = self.Path(end, 0, 0, None)

        self.open.append(start)
        while self.open:
            current = self.open.pop(0)
            self.close.add(current)

            if current == end:
                return self.repro_path(start, current)

            for next_path in self.get_conexao_path(current.estado):
                if next_path in self.close:
                    continue

                new_g_cost = current.g_cost + current.estado.point.distance_to(next_path.estado.point)
                if new_g_cost < next_path.g_cost or next_path not in self.open:
                    next_path.g_cost = new_g_cost
                    next_path.h_cost = next_path.estado.point.distance_to(end.estado.point)
                    next_path.parent = current

                    if next_path not in self.open:
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

espacos["F"].conecta_espaco(15, espacos["B"])
espacos["B"].conecta_espaco(15, espacos["F"])

espacos["C"].conecta_espaco(5, espacos["F"])
espacos["F"].conecta_espaco(5, espacos["C"])

espacos["F"].conecta_espaco(7.5, espacos["D"])
espacos["D"].conecta_espaco(7.5, espacos["F"])

espacos["F"].conecta_espaco(12.5, espacos["E"])
espacos["E"].conecta_espaco(12.5, espacos["F"])

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

print(start.label, '->')
for p in path:
    print(p.estado.label, '->')
window.run(call_on_update)