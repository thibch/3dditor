from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionHandlerQueue, CollisionRay, CollisionTraverser, CollisionNode, TextNode
from src.scene.basic_scene import BasicScene
from direct.showbase import DirectObject


class Game(ShowBase):
    def __init__(self):
        # Initialise la fenêtre de base
        ShowBase.__init__(self)

        # Définit la couleur de fond (noir)
        self.pickerNP = None
        self.pickerNode = None
        self.pickerRay = None
        self.queue = None
        self.scenes = []
        self.setBackgroundColor(0, 0, 0)
        self.list_of_cubes = {}

        # camera
        self.camera.setPos(0, -20, 0)
        self.disableMouse()
        
        self.accept("escape", self.userExit)

        self.init_first_window()
        self.add_collision_mouse()
        
        # Ajouter la tâche de détection
        self.taskMgr.add(self.mouseOverTask, "MouseOverTask")


    def init_first_window(self):
        basic_scene = BasicScene(self)
        self.scenes.append(basic_scene)
        basic_scene.define_tasks(self.taskMgr)

    def add_collision_mouse(self):
        
        # Configurer le système de collision
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        # self.cTrav.showCollisions(self.render)

        # Créer un rayon de collision pour la souris
        self.pickerRay = CollisionRay()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.cTrav.addCollider(self.pickerNP, self.queue)

    def mouseOverTask(self, task):
        if self.mouseWatcherNode.hasMouse():
            # Obtenir la position de la souris
            mpos = self.mouseWatcherNode.getMouse()

            # Mettre à jour le rayon
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            
            # Vérifier les collisions
            self.cTrav.traverse(self.render)

            cube_found = None
            x_normalized = 0
            z_normalized = 0

            # Traiter les résultats
            if self.queue.getNumEntries() > 0:
                self.queue.sortEntries()
                entry = self.queue.getEntry(0)
                hit_pos_local = entry.getSurfacePoint(entry.getIntoNodePath())
                x_normalized = hit_pos_local.x
                z_normalized = hit_pos_local.z
                
                cube_found = entry.getIntoNode().getName()

            self.scenes[0].mouse_on_something(cube_found, x_normalized, z_normalized)
            #else self.queue.getNumEntries() == 0:
            #    self.scenes[0].empty_mouse()
            #    print("Souris hors du cube!")

        return task.cont