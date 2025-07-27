from typing import Literal, List

from panda3d.core import Point3, CollisionNode, CollisionBox, TextNode, TextFont, NodePath

from src.backend_editor.text_file import TextFile
from src.objects.text_object import TextObject
from src.utils.id_singleton import IdSingleton


class Cube():

    scale_X = 5
    scale_Y = 0.1
    scale_Z = 5

    is_mouse_on_me = False
    last_mouse_x = 0
    last_mouse_z = 0

    how_much_scrolled = 0

    def __init__(self, game):
        # super().__init__(game)
        self.text_node_paths: List[TextObject] = []
        self.txt_infos = None
        self.game = game
        self.mainObject = game.render.attachNewNode("pivot")
        self.model = game.loader.loadModel("models/box")

        # Créer un nœud intermédiaire pour la collision
        self.collision_root = self.mainObject.attachNewNode("collision_root")
        self.model.reparentTo(self.mainObject)
        self.model.setPos(-0.5, 0, -0.5)
        self.mainObject.setScale(self.scale_X, self.scale_Y, self.scale_Z)
        self.model.setColorScale(1, 0, 0, 0)

        self.setCollision()
        self.set_text(game.loader)

    def set_text(self, loader):

        self.txt_infos = TextFile("assets/test_file.txt")

        text_models = []
        texts_node_path = []

        offset_pos = 0
        for line in self.txt_infos.lines:
            text = TextNode('texte_3d_' + str(IdSingleton().get_next_id()))
            text.setText(line)
            text.setFont(loader.loadFont('assets/fonts/Monaco.ttf', renderMode = TextFont.RMSolid))
            text.setAlign(TextNode.ABoxedLeft)
            # text.setWordwrap(10)
            text.setTextScale(0.7)
            #print(text.get_line_height())
            #print(text.getWordwrap())

            text_node_path: NodePath = self.mainObject.attachNewNode(text)
            text_node_path.setScale(0.1)
            pos = Point3(-0.475, -1.5, 0.4 - offset_pos*0.075)
            text_node_path.setPos(pos)
            offset_pos+=1

            self.text_node_paths.append(TextObject(text, text_node_path, pos))

            print("------------------")


    def setCollision(self):
        collision_node = CollisionNode(f'{id(self)}_collider')

        collision_box = CollisionBox(
            Point3(-0.5, -0.5, -0.5),
            Point3(0.5, 0.5, 0.5)
        )
        collision_node.addSolid(collision_box)

        # Attacher le nœud de collision au modèle
        self.collider = self.collision_root.attachNewNode(collision_node)

        # Pour debug : rendre le collider visible
        self.collider.show()
        self.collider.setColor(1, 0, 0, 0.3)

    def mouse_on_me(self, mouse_normalized_x, mouse_normalized_z):
        # print("mousOnMe")
        self.last_mouse_x = mouse_normalized_x
        self.last_mouse_z = mouse_normalized_z

        self.is_mouse_on_me = True
        mult = 35

        self.mainObject.setHpr(-mouse_normalized_x*mult, mouse_normalized_z*mult, 0)
        #   print(f"Position relative sur le cube: x={mouse_normalized_x:.2f}, y={mouse_normalized_z:.2f}")

    def no_mouse_on_me(self):
        self.is_mouse_on_me = False

    def click(self):
        print('clicked here : ', self.last_mouse_x, ',',self.last_mouse_z)

    def scroll(self, direction : Literal["up","down"] = "up"):

        if self.is_mouse_on_me:
            if direction == "up":
                self.how_much_scrolled += 1
            else:
                self.how_much_scrolled -= 1

            if self.how_much_scrolled < 0:
                self.how_much_scrolled = 0

            len_txt_np = len(self.text_node_paths)-1
            if self.how_much_scrolled > len_txt_np:
                self.how_much_scrolled = len_txt_np

            for text_obj in self.text_node_paths:
                z = text_obj.get_default_pos().z
                text_obj.get_text_node_path().set_z(z + (self.how_much_scrolled * 0.075))
                # print(z + (self.how_much_scrolled * 0.074))
                if text_obj.get_text_node_path().getPos().z > 0.43 or text_obj.get_text_node_path().getPos().z < -0.49:
                    text_obj.get_text_node_path().hide()
                else:
                    text_obj.get_text_node_path().show()