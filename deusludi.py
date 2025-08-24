import gameobject as go
import sys
import ludilector as ll
import game as gm
# TODO: NO OOP SYSTEM FUNCTIONALITY OF DEUS LUDI
# TODO: STORES GAMES, BUILD OPTIONS, UTILITY FUNCTIONS
# TODO: SEARCH FOR OBJECT IN GAME

# TODO: Make a way to save for game to be a file
# TODO: .ludi and .ludsc extensions for games and scene

import pygame as pyg


def hirearchy_panel_scr_func(obj):
    obj.update_rect()
    obj.draw()

if __name__ == "__main__":
    pyg.init()
    
    WIDTH, HEIGHT = 1800, 1000
    
    deusludi = ll.load_game("./thagames/mygame.ludi.json")
    
    editor = deusludi.active_scene
    editor.link_script_and_object(editor.gameobjects[0], editor.gameobjects[0].script, hirearchy_panel_scr_func)
   
    screen = pyg.display.set_mode((WIDTH, HEIGHT))
    pyg.display.set_caption("Deus Ludi")
    
    running = True
    
    while running:
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                running = False
       
        pyg.display.get_surface().fill('white')  # type: ignore
        deusludi.run()
        pyg.display.update()
    
    pyg.quit()

sys.exit()
    
