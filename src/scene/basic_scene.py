from src.objects.my_cube import Cube
from src.utils.ScrollHandler import ScrollHandler


class BasicScene():
    list_of_cubes = {}
    x = 0

    def __init__(self, game):
        print("i")
        cube = Cube(game)
        self.list_of_cubes[f"{id(cube)}_collider"] = cube

        self.scrollHandler = ScrollHandler()

    def printWheelUp(self):
        print("printWheelUp")

    def printWheelDown(self):
        print("printWheelDown")

    def found_something(self, name: str, x_normalized, z_normalized):
        self.scrollHandler.cube_to_call(self.list_of_cubes[name])
        self.list_of_cubes[name].mouseOnMe(x_normalized, z_normalized)

    def define_tasks(self, taskMgr):
        taskMgr.add(self.run_here, "moveCube")

    def run_here(self, task):
        # self.x = self.x + 0.05

        # for i in self.list_of_cubes.values():
        #    i.mouseOnMe(self.x, 0)

        return task.cont

    def empty_mouse(self):
        for key, value in self.list_of_cubes.items():
            value.no_mouse_on_me()
