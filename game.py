import pygame as pyg
from gameobject import *

class Game:
    #TODO: add lots more functionality like delta time, scene manager, tiler etcccc
    def __init__(self):
        self.scenes = []
        self.active_scene: Scene = None
        
    
    def set_active_scene(self, scene: Scene):
        if scene not in self.scenes:
            print("The scene is not linked to this game!")
            return
        self.active_scene = scene
    
    #TODO: add way to differentiate every scene as unique
    def add_scene(self, scene: Scene):
        self.scenes.append(scene)
    
    def remove_scene(self, scene: Scene):
        if scene not in self.scenes:
            print("The scene is already not in this game!")
            return
        self.scenes.remove(scene)
    
    def run(self):
        self.active_scene.play()
         
