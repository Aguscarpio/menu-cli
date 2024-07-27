from .core import *
main = Menu("Categorías", [
    #  Action("TF", lambda: tomate("TF")),
    Action("Lectura", lambda: tomate("Lectura")),
    Action("META", lambda: tomate("META")),
    Menu("Estudio", [
        Action("Doctorado", lambda: tomate("Doctorado")),
        Action("General", lambda: tomate("General"))]
        ),
    Menu("Skills", [
        Action("Programación", lambda: tomate("Programación")),
        Action("Inglés", lambda: tomate("Inglés")),
        Action("Piano", lambda: tomate("Piano"))])])

main.navigate()
