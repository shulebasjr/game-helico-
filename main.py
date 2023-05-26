# 🌲 🌊 🚁 🟩 🔥 🏥 💛 🪣 🏨 ⚪ 🔵 ⬛

from clouds import Clouds
from map import Map
import time
import os
from helicopter import Helicopter as Helico
from pynput import keyboard
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDATE = 100
CLOUDS_UPDATE = 100
MAP_W, MAP_H = 20, 10



field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
#f -save game, g - load game
def process_key(key):
    global helico, tick, clouds, field
    c = key.char.lower()
    #movements of helicopter
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    #save game
    elif c == 'f':
        data = {"helicopter": helico.export_data(), 
                "clouds": clouds.export_data(), 
                "field": field.export_data(),
                  "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    #load game
    elif c =='g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            helico.impoer_data(data["helicopter"])
            tick = data["tick"] or 1
            field.import_data(data["field"])
            clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()



while True:
    os.system("cls")
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fire()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()