#!/usr/bin/env python3
"""
Game Browser GUI for DeusLudi

A simple tkinter-based GUI that displays all available games
from the thagames directory.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from pathlib import Path

class GameBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("DeusLudi Game Browser")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            self.main_frame, 
            text="DeusLudi Game Browser", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Refresh button
        refresh_btn = ttk.Button(
            self.main_frame, 
            text="🔄 Refresh", 
            command=self.refresh_games
        )
        refresh_btn.grid(row=0, column=2, pady=(0, 20), padx=(10, 0))
        
        # Games listbox with scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create listbox and scrollbar
        self.games_listbox = tk.Listbox(
            list_frame, 
            font=("Arial", 12),
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.games_listbox.yview)
        self.games_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.games_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click event
        self.games_listbox.bind('<Double-Button-1>', self.on_game_double_click)
        
        # Game details frame
        details_frame = ttk.LabelFrame(self.main_frame, text="Game Details", padding="10")
        details_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        
        # Game details text widget
        self.details_text = tk.Text(
            details_frame, 
            height=20, 
            width=40, 
            font=("Consolas", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        details_text_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_text_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_text_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection change event
        self.games_listbox.bind('<<ListboxSelect>>', self.on_game_select)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Load games initially
        self.games = []
        self.refresh_games()
    
    def refresh_games(self):
        """Scan the thagames directory for .ludi.json files"""
        self.games_listbox.delete(0, tk.END)
        self.games = []
        
        thagames_dir = Path("thagames")
        if not thagames_dir.exists():
            self.status_var.set("Error: thagames directory not found")
            return
        
        # Find all .ludi.json files
        ludi_files = list(thagames_dir.glob("*.ludi.json"))
        
        if not ludi_files:
            self.status_var.set("No games found in thagames directory")
            return
        
        # Load and display games
        for ludi_file in ludi_files:
            try:
                with open(ludi_file, 'r') as f:
                    game_data = json.load(f)
                
                game_name = game_data.get('name', ludi_file.stem.replace('.ludi', ''))
                self.games.append({
                    'name': game_name,
                    'file_path': str(ludi_file),
                    'data': game_data
                })
                
                # Display in listbox
                self.games_listbox.insert(tk.END, game_name)
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading {ludi_file}: {e}")
                continue
        
        self.status_var.set(f"Found {len(self.games)} game(s)")
    
    def on_game_select(self, event):
        """Handle game selection change"""
        selection = self.games_listbox.curselection()
        if not selection:
            return
        
        selected_index = selection[0]
        if 0 <= selected_index < len(self.games):
            self.display_game_details(self.games[selected_index])
    
    def display_game_details(self, game):
        """Display detailed information about the selected game"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = f"Game: {game['name']}\n"
        details += f"File: {game['file_path']}\n"
        details += f"{'='*40}\n\n"
        
        # Display game data in a readable format
        game_data = game['data']
        for key, value in game_data.items():
            if key == 'scenes':
                details += f"Scenes:\n"
                if 'all_scenes' in value:
                    for i, scene in enumerate(value['all_scenes'], 1):
                        details += f"  {i}. {scene}\n"
            else:
                details += f"{key}: {value}\n"
        
        self.details_text.insert(1.0, details)
        self.details_text.config(state=tk.DISABLED)
    
    def on_game_double_click(self, event):
        """Handle double-click on a game to launch it"""
        selection = self.games_listbox.curselection()
        if not selection:
            return
        
        selected_index = selection[0]
        if 0 <= selected_index < len(self.games):
            game = self.games[selected_index]
            self.launch_game(game)
    
    def launch_game(self, game):
        """Launch the selected game using the main deusludi.py script"""
        try:
            import subprocess
            result = subprocess.run([
                'python', 'deusludi.py', game['file_path']
            ], cwd=os.getcwd(), capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Game '{game['name']}' launched successfully!")
            else:
                messagebox.showerror("Error", f"Failed to launch game:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game:\n{str(e)}")

def main():
    root = tk.Tk()
    app = GameBrowser(root)
    
    # Configure window close event
    def on_closing():
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
