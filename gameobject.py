import pygame as pyg
import math


class Transform:
    def __init__(self, posx, posy, rot_x, rot_y, scal_x, scal_y):
        self.x = posx
        self.y = posy
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.scal_x = scal_x
        self.scal_y = scal_y

class Vector:
    def __init__(self, ihatl, jhatl):
        self.x = ihatl
        self.y = jhatl
        self.magnitude = math.sqrt(self.x**2 + self.y**2)
        self.direction = math.atan(self.y/self.x)
        
        if self.magnitude != 1:
            self.normalized = Vector(self.x/self.magnitude, self.y/self.magnitude)
    
    def get_normalized(self):
        self.magnitude = math.sqrt(self.x**2 + self.y**2)
        self.direction = math.atan(self.y/self.x)
        if self.magnitude != 1:
            self.normalized = Vector(self.x/self.magnitude, self.y/self.magnitude)
        return self.normalized

    def get_magnitude(self): 
        self.magnitude = math.sqrt(self.x**2 + self.y**2)
        self.direction = math.atan(self.y/self.x)
        return self.magnitude

    def get_direction(self):
        self.magnitude = math.sqrt(self.x**2 + self.y**2)
        self.direction = math.atan(self.y/self.x)
        return self.direction
    

class GameObject:
    # TODO: Add rotational functionality
    def __init__(self, transform: Transform):
        self.transform = transform
        self.script: Script = None
    
    def run_script(self):
        self.script.script_function(self)

class RectangleGameObject(GameObject):
    def __init__(self, transform: Transform, color=None):
        super().__init__(transform)
        self.color = color
        self.rect = pyg.FRect((self.transform.x, self.transform.y), (self.transform.scal_x, self.transform.scal_y))
        self.rect.center = (self.transform.x, self.transform.y)
    
    def draw(self):
        pyg.draw.rect(pyg.display.get_surface(), self.color, self.rect)
    
    def update_rect(self):
        #TODO: Rotational functionalityi
        self.rect.center = (self.transform.x, self.transform.y)
        self.rect.width = self.transform.scal_x
        self.rect.height = self.transform.scal_y
        

class Script:
    def __init__(self, gameobject):
        self.gameobject = gameobject
        self.script_function = None

class Scene:
    def __init__(self):
        self.gameobjects = []
    
    # TODO: Add a way to differentiate every gameobject
    def add_gameobject(self, gameobject: GameObject):
        self.gameobjects.append(gameobject)
    
    def remove_gameobject(self, gameobject:GameObject):
        if gameobject in self.gameobjects:
            self.gameobjects.remove(gameobject)
            return
        print("GameObject belongs to a different Scene!")
        return
    
    
    def play(self):
        for gameobj in self.gameobjects:
            if gameobj.script == None:
                continue
            gameobj.run_script()
        
    
    def link_script_and_object(self, object: GameObject, script_class: Script, script_function):
        if object not in self.gameobjects:
            print("Gameobject belongs to different scene!")
            return
        script_class.gameobject = object
        script_class.script_function = script_function
        
        object.script = script_class



        


