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

all_games = []
active_game: gm.Game = None #type: ignore

def set_active_game(game: gm.Game):
    global active_game
    if game not in all_games:
        print("game is not registered!")
        return
    active_game = game

def add_game(game: gm.Game):
    if game in all_games:
        #* Not sure if this is accurate
        print("game is already there!")
        return
    all_games.append(game)

def delete_game(game: gm.Game):
    if game not in all_games:
        print("game is not registered")
        return
    all_games.remove(game)
    
def get_active_game():
    if active_game == None:
        print("No active game!")
        return
    return active_game


def hirearchy_panel_scr_func(obj):
    obj.update_rect()
    obj.draw()

if __name__ == "__main__":
    pyg.init()
    
    WIDTH, HEIGHT = 1800, 1000
    
    deusludi = ll.load_game("./thagames/mygame.ludi.json")
    # editor = go.Scene()
    # deusludi.add_scene(editor)
    # deusludi.set_active_scene(editor)

    # hirearchy_panel = go.RectangleGameObject(go.Transform(100, HEIGHT/2, 0, 0, 200, HEIGHT), color='grey')
    # editor.add_gameobject(hirearchy_panel)
    
    # hirearchy_panel_script = go.Script(hirearchy_panel)
    
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
    
