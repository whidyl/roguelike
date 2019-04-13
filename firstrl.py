#!/usr/bin/env python
import libtcodpy as tcod
 
# GLOBAL GAME SETTINGS
# Windows Controls
FULLSCREEN = False 
SCREEN_WIDTH = 130  # characters wide
SCREEN_HEIGHT = 60  # characters tall
LIMIT_FPS = 20  # 20 frames-per-second maximum

# Initialize new console to be used as a buffer
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)


# GAME OBJECTS
class GameObject:
    """ Represents a generic game object 
    Always viewed a character on screen."""
    # holds all game objects
    game_objects = []
    def __init__(self, x, y, char, color):
        self._x = int(x)
        self._y = int(y)
        self._char = char
        self._color = color
        self.game_objects.append(self)
    
    def move(self, dx, dy):
        """ move by the given amount """
        if not world_map[self._x + dx][self._y + dy].blocked:
            self._x += dx 
            self._y += dy
    
    def draw(self):
        """ draw object at its position with its color. """
        tcod.console_set_default_foreground(con, self._color)
        tcod.console_put_char(con, self._x, self._y, self._char, tcod.BKGND_NONE)
    
    def clear(self):
        """ erase the object's char from the screen """
        tcod.console_put_char(con, self._x, self._y, ' ', tcod.BKGND_NONE)
    
    @property
    def blocked_left(self):
        if world_map[self._x-1][self._y].blocked:
            return True
        return False
    
    @property
    def blocked_right(self):
        if world_map[self._x+1][self._y].blocked:
            return True
        return False
    
    @property
    def blocked_up(self):
        if world_map[self._x][self._y-1].blocked:
            return True
        return False
    
    @property
    def blocked_down(self):
        if world_map[self._x][self._y+1].blocked:
            return True
        return False

# MAP
MAP_WIDTH = 80
MAP_HEIGHT = 45
color_dark_wall = tcod.Color(0, 0, 100)
color_dark_ground = tcod.Color(50, 50, 150)
world_map = None

class Tile:
    """ Represents a tile of the map """
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        # by default, a blocked tile also blocks sight.
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

def make_map():
    global world_map

    # fill map with unblocked tiles.
    world_map = [
        [ Tile(False) for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
    world_map[30][22].blocked = True
    world_map[30][22].block_sight = True
    world_map[50][22].blocked = True
    world_map[50][22].block_sight = True


# INITIALIZATION

# Setup Font
font_filename = 'arial10x10.png'
tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
# Initialize screen
title = 'PHANTASY STAR ROGUE'
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
# Set FPS
tcod.sys_set_fps(LIMIT_FPS)
# Create player and NPC
player = GameObject(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', tcod.white)
npc = GameObject(SCREEN_WIDTH/2 + 6, SCREEN_HEIGHT/2 + 3, '@', tcod.yellow)
# make map
make_map()
# INPUT HANDALING

def get_key_event(turn_based=None):
    if turn_based:
        # Turn-based game play; wait for a key stroke
        key = tcod.console_wait_for_keypress(True)
    else:
        # Real-time game play; don't wait for a player's key stroke
        key = tcod.console_check_for_keypress()
    return key
 
 
def handle_keys():
    key = get_key_event(True)
 
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
 
    elif key.vk == tcod.KEY_ESCAPE:
        return True  # exit game
 
    # movement keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(0, -1)
 
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(0, 1)
 
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(-1, 0)
 
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.move(1, 0)

# Main Game Loop

def draw():
    for game_object in GameObject.game_objects:
        game_object.draw()
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if (world_map[x][y].block_sight):
                tcod.console_set_char_background(con, x, y, color_dark_wall, tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, color_dark_ground, tcod.BKGND_SET)
    
    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def clear():
    for game_object in GameObject.game_objects:
        game_object.clear()

def main():
    exit_game = False
    while not tcod.console_is_window_closed() and not exit_game:
        draw()
        tcod.console_flush()
        clear()
 
        exit_game = handle_keys()
 

main()