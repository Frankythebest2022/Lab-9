""" 
Description: 
  Graphical user interface that displays select information about a 
  user-specified Pokemon fetched from the PokeAPI 

Usage:
  python poke_info_viewer.py
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests

# PokeAPI URL
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'


def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

# Event handler for the Get Info button
def get_info_button_click():
    # Get the Pokemon name from the user input
    pokemon_name = name_entry.get()
    
    # Get Pokemon information from the PokeAPI
    poke_info = get_pokemon_info(pokemon_name)
    
    if poke_info:
        # Display Pokemon type(s)
        types = ', '.join(type_info['type']['name'] for type_info in poke_info['types'])
        types_label.config(text=f"Type(s): {types}")
        
        # Display Pokemon stats
        hp_bar['value'] = poke_info['stats'][0]['base_stat']
        attack_bar['value'] = poke_info['stats'][1]['base_stat']
        defense_bar['value'] = poke_info['stats'][2]['base_stat']
        special_attack_bar['value'] = poke_info['stats'][3]['base_stat']
        special_defense_bar['value'] = poke_info['stats'][4]['base_stat']
        speed_bar['value'] = poke_info['stats'][5]['base_stat']

        # Display Pokemon height and weight
        height_label.config(text=f"Height: {poke_info['height']} dm")
        weight_label.config(text=f"Weight: {poke_info['weight']} hg")
    else:
        # Show error message if Pokemon not found
        messagebox.showerror("Error", f"Unable to fetch the information for {pokemon_name.capitalize()} from the PokeAPI")
        # Clear the Info and Stats areas
        types_label.config(text="Type(s):")
        hp_bar['value'] = 0
        attack_bar['value'] = 0
        defense_bar['value'] = 0
        special_attack_bar['value'] = 0
        special_defense_bar['value'] = 0
        speed_bar['value'] = 0
        height_label.config(text="Height:")
        weight_label.config(text="Weight:")

# Create the main window
root = Tk()
root.title("Pokemon Information")  

input_frame = ttk.Frame(root)

# Create the user input frame
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

# Create and place widgets for the user input frame
ttk.Label(input_frame, text="Pokemon Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(input_frame)

name_entry.grid(row=0, column=1, padx=5, pady=5)
get_info_button = ttk.Button(input_frame, text="Get Info", command=get_info_button_click)
get_info_button.grid(row=0, column=2, padx=5, pady=5)


# Create the Info frame
info_frame = ttk.Frame(root)
info_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# Create labels to display Height, Weight, and Type(s) information
height_label = ttk.Label(info_frame, text="Height:")
weight_label = ttk.Label(info_frame, text="Weight:")
types_label = ttk.Label(info_frame, text="Type(s):")

height_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
weight_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
types_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Create the Stats frame
stats_frame = ttk.Frame(root)
stats_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Create labels for Stats and Info frames
stats_label = ttk.Label(root, text="Stats", font=("Arial", 14, "bold"))
info_label = ttk.Label(root, text="Info", font=("Arial", 14, "bold"))

# Grid layout for frames
input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
info_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
stats_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Grid layout for frames and labels
#stats_label.grid(row=1, column=1, padx=10, pady=5, sticky="nw")
#info_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
#input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
#info_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
#stats_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Create labels to display Pokemon stats
hp_label = ttk.Label(stats_frame, text="HP:")
attack_label = ttk.Label(stats_frame, text="Attack:")
defense_label = ttk.Label(stats_frame, text="Defense:")
special_attack_label = ttk.Label(stats_frame, text="Special Attack:")
special_defense_label = ttk.Label(stats_frame, text="Special Defense:")
speed_label = ttk.Label(stats_frame, text="Speed:")

hp_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
attack_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
defense_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
special_attack_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
special_defense_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
speed_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

# Create and place the progress bars for each stat
hp_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')
attack_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')
defense_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')
special_attack_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')
special_defense_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')
speed_bar = ttk.Progressbar(stats_frame, orient=HORIZONTAL, length=200, mode='determinate')

hp_bar.grid(row=0, column=1, padx=5, pady=5, sticky="w")
attack_bar.grid(row=1, column=1, padx=5, pady=5, sticky="w")
defense_bar.grid(row=2, column=1, padx=5, pady=5, sticky="w")
special_attack_bar.grid(row=3, column=1, padx=5, pady=5, sticky="w")
special_defense_bar.grid(row=4, column=1, padx=5, pady=5, sticky="w")
speed_bar.grid(row=5, column=1, padx=5, pady=5, sticky="w")

root.mainloop()