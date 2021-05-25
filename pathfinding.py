from display import Window, Point


class PathFinding:
    class Path:
        def __init__(self, estado, g, h, p_estado):
            self.estado = estado
            self.g = g
            self.h = h
            self.p_estado = p_estado
            
    def __init__(self):
        self.open = []
        self.close = set()
        self.paths = set()

    def add_open(self, path):
        self.opend.append(path)

    def find_path(self, start, end):
        self.add_open(self.Path(start, 0, start.point.distance_to(end.point), None))
        while open:
            
        


for k in path.keys():
    g, espaco = path[k]
    print(k.label, g, espaco.label)
    
# router = [end]
# t = end
# while True:
#     g, c = path[t]
#     router.append(c)
#     if c == start:
#         break
#     t = c

# for r in reversed(router):
#     print(r.label, '>')

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

espacos["F"].conecta_espaco(1, espacos["B"])
espacos["B"].conecta_espaco(1, espacos["F"])

espacos["C"].conecta_espaco(15, espacos["F"])
espacos["F"].conecta_espaco(15, espacos["C"])

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

window.run(call_on_update)