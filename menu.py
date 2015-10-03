from retrogamelib.util import *
from retrogamelib import clock
from retrogamelib import button
from retrogamelib.constants import *
from game import *
from retrogamelib import dialog
from retrogamelib import font
from retrogamelib import display
from levels import *


def run_menu():
    timer = 0
    play_music("data/title.ogg")
    game = Game()
    set_global_sound_volume(0.75)
    while True:
        clock.tick()
        button.handle_input()

        # If we pressed start, begin the game
        if button.is_pressed(START):

            play_music("data/algar-orka.xm", -1)
            # Creates text box
            whitefont = font.Font(GAMEBOY_FONT, GB_SCREEN_COLOR)
            box = dialog.DialogBox((152, 46), (50, 50, 50),
                GB_SCREEN_COLOR, whitefont)
            box.set_dialog([
                "Spin to \
                win.",
                "- Garen 2008"
            ])
            # Updates box when Z is pressed
            box.set_scrolldelay(2)
            while not box.over():
                clock.tick()
                button.handle_input()
                if button.is_pressed(A_BUTTON):
                    box.progress()
                screen = display.get_surface()
                screen.fill(GB_SCREEN_COLOR)
                screen.blit(game.background, (0, 0))
                box.draw(screen, (4, 4))
                display.update()

            game.won = True
            game.level = 1
            game.lives = 3
            game.score = 0

            #Play each level
            for lvl in LEVELS:
                game.startLevel(lvl)
                game.level += 1
                game.loop()
                #if not game.player.alive():
                #    break

        screen = display.get_surface()
        screen.fill(GB_SCREEN_COLOR)
        screen.blit(load_image("data/bg.png"), (0, 0))
        ren = game.font.render("Press Start")
        timer += 1
        timer = timer % 30
        if timer < 15:
            screen.blit(ren, (80-ren.get_width()/2,
                104-ren.get_height()/2))
        display.update()