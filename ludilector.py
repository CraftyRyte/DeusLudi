"""
LudiLector - Game File Loader Module

This module is responsible for loading and parsing game files for the DeusLudi game engine.
It reads JSON-based game configuration files and creates runtime game objects from them.

The module supports loading:
- Game definition files (.ludi.json)
- Scene definition files (.ludsc.json) 
- Game object resource files (.ludres.json)

Author: DeusLudi Game Engine
"""

import sys
import os
import pygame as pyg
import gameobject as go
import game as ga
import universal_constants as uc
import json

# Initialize Pygame - required for game engine functionality
pyg.init()

def load_game(game_file_path):
    """
    Load a complete game from a .ludi.json file.
    
    This function parses a game definition file and creates all associated
    scenes and game objects. It validates file paths and extensions before
    attempting to load the game data.
    
    Args:
        game_file_path (str): Path to the .ludi.json game definition file
        
    Returns:
        ga.Game: A fully initialized Game object with all scenes and objects loaded,
                 or None if loading failed
                 
    File Structure Expected:
        .ludi.json: Contains game metadata and references to scene files (Game Files)
        .ludsc.json: Scene files containing gameobject references (Scene files)
        .ludres.json: Individual gameobject resource files (Gameobject files)
    """
    # Validate that the game file exists at the specified path
    if not os.path.exists(game_file_path):
        print(f"Game file not found: {game_file_path}")
        return None

    # Open the game definition file for reading
    game_file = open(game_file_path, 'r')

    # Validate the file extension to ensure it's a proper game definition file
    if not game_file_path.endswith(".ludi.json"):
        print(f"Invalid game file extension: {game_file_path}")
        return None

    # Create a new Game runtime object to hold all game data
    game_runtime_object = ga.Game()
    # List to store all loaded scenes before adding them to the game
    scenes = []

    # Use context manager to ensure proper file handling
    with game_file:
        # Parse the JSON data from the game definition file
        game_data = json.loads(game_file.read())
        
        # Iterate through each scene referenced in the game file
        for scene in game_data["scenes"]["all_scenes"]:
            # Open and parse each scene file (.ludsc.json)
            scene_file = open(scene, 'r')
            scene_data = json.loads(scene_file.read())
            # Create a new Scene runtime object
            scene_runtime_object = go.Scene()

            # Process all gameobjects defined in this scene
            for gameobject in scene_data["gameobjects"]["all_gameobjects"]:
                # Open and parse each gameobject resource file (.ludres.json)
                obj_file = open(gameobject)
                obj_data = json.loads(obj_file.read())

                # Create the appropriate gameobject type based on the type field
                if obj_data["type"] == uc.game_object_types.get("rgo"):
                    # Rectangle Game Object - has visual properties like color
                    gameobject_runtime_object = go.RectangleGameObject(
                        go.Transform(obj_data["properties"]["transform"]), 
                        color=obj_data["properties"]["color"]
                    )
                elif obj_data["type"] == uc.game_object_types.get("go"):
                    # Basic Game Object - only has transform properties
                    gameobject_runtime_object = go.GameObject(
                        go.Transform(obj_data["properties"]["transform"])
                    )
                else:
                    # Unknown gameobject type - skip this object and continue
                    print(f"Invalid gameobject type: {obj_data['type']}")
                    continue

                # MAKING THE BLANK THE SCRIPT
                gameobject_runtime_object.script = go.Script(gameobject_runtime_object)
                # Add the created gameobject to the current scene
                scene_runtime_object.add_gameobject(gameobject_runtime_object)
                # Close the gameobject resource file
                obj_file.close()

            # Add the completed scene to our scenes list
            scenes.append(scene_runtime_object)
            # Close the scene definition file
            scene_file.close()
            
        # Add all loaded scenes to the game runtime object
        for scene2 in scenes:
            game_runtime_object.add_scene(scene2)

        # Set the first scene as the active/starting scene
        game_runtime_object.set_active_scene(scenes[0])
    
    # Return the fully loaded and initialized game object
    return game_runtime_object

# def link_script(game_object: go.GameObject, scene: go.Scene, obj_data):
#     script_file = open(obj_data["properties"]["script"], 'r')
#     game_object.script = go.Script(game_object)
#     content = script_file.read()
#     for i in range(len(content)):
#         if content[i]=='_':
#             if checkifinfo(content, i):
#                 json_content = extract_json(content, i)
    
#     json_content = json.loads(json_content)
#     game_object.script.script_function = json_content["main"]
