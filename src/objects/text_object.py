from panda3d.core import Point3, NodePath, TextNode


class TextObject():
    def __init__(self, text_3d: TextNode, text_node_path: NodePath, default_pos: Point3):
        self.text_3d = text_3d
        self.text_node_path = text_node_path
        self.default_pos = default_pos
    
    def get_text_node_path(self) -> NodePath:
        return self.text_node_path

    def get_text_3d(self) -> TextNode:
        return self.text_3d

    def get_default_pos(self) -> Point3:
        return self.default_pos
