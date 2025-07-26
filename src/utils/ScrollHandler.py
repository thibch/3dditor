from direct.showbase import DirectObject


class ScrollHandler(DirectObject.DirectObject):
    cube = None
    def __init__(self):
        super().__init__()

        self.accept('wheel_up', self.wheel_up)
        self.accept('wheel_down', self.wheel_down)


    def cube_to_call(self, cube):
        self.cube = cube

    def wheel_up(self):
        if self.cube:
            self.cube.scroll('up')

    def wheel_down(self):
        if self.cube:
            self.cube.scroll('down')