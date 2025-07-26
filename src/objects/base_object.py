from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3, CollisionNode, CollisionRay, BitMask32

class BaseObject(DirectObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.render = game.render
        self.loader = game.loader

        # Propriétés de base
        self.model = None
        self.position = Point3(0, 0, 0)
        self.scale = Point3(1, 1, 1)
        self.rotation = Point3(0, 0, 0)
        
        # État de l'objet
        self.is_visible = True
        self.is_mouse_over = False
        self.is_clickable = False
        self.is_draggable = False
        
        # Propriétés personnalisées
        self.properties = {}

    def setup_collision(self):
        """Configure la détection de collision pour l'objet"""
        if self.model:
            self.collider = self.model.attachNewNode(CollisionNode(f'{id(self)}_collider'))
            self.collider.node().addSolid(self.model.node().getGeom(0))
            
    def setup_mouse_detection(self):
        """Active la détection de la souris sur l'objet"""
        self.is_clickable = True
        self.setup_collision()
        self.accept('mouse1', self.on_click)

    def set_position(self, x, y, z):
        """Définit la position de l'objet"""
        self.position = Point3(x, y, z)
        if self.model:
            self.model.setPos(self.position)
            
    def set_scale(self, x, y, z):
        """Définit l'échelle de l'objet"""
        self.scale = Point3(x, y, z)
        if self.model:
            self.model.setScale(self.scale)
            
    def set_rotation(self, h, p, r):
        """Définit la rotation de l'objet (heading, pitch, roll)"""
        self.rotation = Point3(h, p, r)
        if self.model:
            self.model.setHpr(self.rotation)
            
    def show(self):
        """Rend l'objet visible"""
        if self.model:
            self.model.show()
        self.is_visible = True
        
    def hide(self):
        """Cache l'objet"""
        if self.model:
            self.model.hide()
        self.is_visible = False
        
    def set_property(self, key, value):
        """Définit une propriété personnalisée"""
        self.properties[key] = value
        
    def get_property(self, key, default=None):
        """Récupère une propriété personnalisée"""
        return self.properties.get(key, default)
        
    def on_mouse_over(self):
        """Appelé quand la souris survole l'objet"""
        self.is_mouse_over = True
        if self.model:
            self.model.setColor(1, 0, 0, 1)  # Rouge en survol
            
    def on_mouse_out(self):
        """Appelé quand la souris ne survole plus l'objet"""
        self.is_mouse_over = False
        if self.model:
            self.model.setColor(1, 1, 1, 1)  # Blanc par défaut
            
    def on_click(self):
        """Appelé quand l'objet est cliqué"""
        if self.is_clickable and self.is_mouse_over:
            print(f"Objet {id(self)} cliqué!")
            
    def update(self, dt):
        """Mise à jour par frame (à surcharger dans les classes enfants)"""
        pass
        
    def cleanup(self):
        """Nettoie l'objet avant sa suppression"""
        if self.model:
            self.model.removeNode()
        self.ignoreAll()  # Supprime tous les événements