from os import curdir
from display import Window, Point

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
    "A": Espaco("A", Point(2, 4)),
    "B": Espaco("B", Point(2, 2)),
    "C": Espaco("C", Point(4, 2)),
    "D": Espaco("D", Point(2, 0)),
    "E": Espaco("E", Point(0, 2)),
}

espacos["A"].conecta_espaco(10, espacos["B"])
espacos["B"].conecta_espaco(10, espacos["A"])

espacos["C"].conecta_espaco(10, espacos["B"])
espacos["B"].conecta_espaco(10, espacos["C"])

espacos["D"].conecta_espaco(10, espacos["B"])
espacos["B"].conecta_espaco(10, espacos["D"])

espacos["E"].conecta_espaco(10, espacos["B"])
espacos["B"].conecta_espaco(10, espacos["E"])

for espaco in espacos.values():
    window.draw_circle(Point(espaco.point.x, espaco.point.y))
    for conexao in espaco.conexao:
        window.draw_line(espaco.point, conexao.espaco.point, thickness=5)

start = espacos["A"]
end = espacos["E"]

open = [start]
close = []
path = {}

# while open:
#     current = open.pop()

#     if current.label == end.label:
#         path[current] = current
#     else:
#         for conexao in current.conexao:

window.run(call_on_update)