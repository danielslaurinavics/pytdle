# pytdle source code
# Made by Daniels Laurinavičs dl22029
# University of Latvia, Faculty of Computing

# Definition of constants
SCREEN_X, SCREEN_Y = 800, 600
GRID_COLS, GRID_ROWS = 6, 6
SQUARE_SIZE = (SCREEN_X // 3) // GRID_COLS
SQUARE_MARGIN = SCREEN_X // 100

GRID_WIDTH = GRID_COLS * (SQUARE_SIZE + SQUARE_MARGIN) - SQUARE_MARGIN
GRID_X_OFFSET = (SCREEN_X - GRID_WIDTH) // 2
GRID_Y_OFFSET = 50

# Setting colour constants
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (150, 0, 0)
COLOUR_GREEN = (0, 150, 0)
COLOUR_ORANGE = (190, 150, 0)
COLOUR_BLUE = (0, 0, 150)
COLOUR_GRAY = (125, 125, 125)

# Setting file path constants
CORRECT_SOUND_PATH = './sounds/high_beep.wav'
MISPLACED_SOUND_PATH = './sounds/middle_beep.wav'
WRONG_SOUND_PATH = './sounds/low_beep.wav'
GENERAL_SOUND_PATH = './sounds/generic_beep.wav'
INTRO_SOUND_PATH = './sounds/intro.wav'
INTRO_FADE_SOUND_PATH = './sounds/fade.wav'
WIN_MUSIC_PATH = './sounds/win_music.wav'
LOSE_MUSIC_PATH = './sounds/lose_music.wav'
FONT_PATH = './files/SpaceMono-Regular.ttf'
WORDS_FILE_PATH = './files/words'
STATS_FILE_PATH = './files/stats'
CONFIG_FILE_PATH = './files/config'
GAME_ICON_PATH = './files/icon.png'

'''
    FILE_CHECK - List of files to check for their existance in their 
    directory paths before starting the game. (required files)
    All files except STATS_FILE_FATH, CONFIG_FILE_PATH and GAME_ICON_PATH are checked
'''
FILE_CHECK = [CORRECT_SOUND_PATH, MISPLACED_SOUND_PATH, WRONG_SOUND_PATH, GENERAL_SOUND_PATH, INTRO_SOUND_PATH, INTRO_FADE_SOUND_PATH, WIN_MUSIC_PATH, LOSE_MUSIC_PATH, FONT_PATH, WORDS_FILE_PATH]

# Importing libraries
import pygame
import pygame.mixer
import random
import os
import sys

# Checking that all required files exist
not_found = []
for file in FILE_CHECK:
    if os.path.exists(file) == False:
        all_files_exist = False
        not_found.append(file)
    else: all_files_exist = True

'''
    In case if a required file is missing, an error will be displayed on the console,
    showing the missing files and requesting to press ENTER, after which
    the application will close.
'''    
if all_files_exist == False:
    print('\nThe game has failed to start due to missing game files.')
    print('Please check that the following files exist:\n')
    for fail in not_found:
        print(fail)
    print()
    input('Press ENTER to exit')
    sys.exit()

# Creation of a player statistics file if it does not exist.
if os.path.exists(STATS_FILE_PATH) == False:
    try:
        with open(STATS_FILE_PATH, 'x') as file:
            file.write('pytdle user stats file\n')
            print('No user stats file was found - a new one has been created.')
    except FileExistsError:
        print('User stats file already exists')
    input("Press ENTER to continue")

'''
    Creation of the configuration file if it does not exist.
    The application will do its first-time setup on the console,
    with user setting the application's configuration and saving it
    to the config file.
'''
if os.path.exists(CONFIG_FILE_PATH) == False:
    try:
        with open(CONFIG_FILE_PATH, 'x') as config:
            config.write('pytdle configuration file\nThis file is used for setting jumpers affecting gameplay.\n')
            print('No config file was found - a new one has been created.')
            print('Please do the first-time setup - answer the questions')
            while True:
                skip_intro_jumper = input('Should the intro be displayed every time the game is launched? [y/n]: ')
                if skip_intro_jumper == 'n':
                    config.write('1\n')
                    break
                elif skip_intro_jumper == 'y':
                    config.write('0\n')
                    break
                else: continue
            
            while True:
                skip_rules_jumper = input('Should the game rules be displayed every time the game is played? [y/n]: ')
                if skip_rules_jumper == 'n':
                    config.write('1\n')
                    break
                elif skip_rules_jumper == 'y':
                    config.write('0\n')
                    break
                else: continue
                
            while True:
                skip_rules_jumper = input('Should animations be disabled? [y/n]: ')
                if skip_rules_jumper == 'y':
                    config.write('1\n')
                    break
                if skip_rules_jumper == 'n':
                    config.write('0\n')
                    break
                else: continue
            print('First-time setup complete')
            input('Press ENTER to continue')
    except FileExistsError:
        print('Config file already exists')
        input("Press ENTER to continue")

'''
    Reading the configuration file for setting values
    Only rows 3, 4 and 5 contains config jumpers
'''
config_jumpers = []    
with open(CONFIG_FILE_PATH, 'r') as config:
    for i, line in enumerate(config, 1):
        if 3 <= i <= 5:
            config_jumpers.append(line[0])

'''
    Setting the setting jumpers according to their value in
    the configuration file.
        SKIP_INTRO_JUMPER - if true, skip the game splash (intro) screen
        SKIP_RULES_JUMPER - if true, skip the pre-game (game rules) screen 
        NO_ANIM_JUMPER - if true, disable smooth animations.
'''
skip_intro_jumper = True if config_jumpers[0] == '1' else False
skip_rules_jumper = True if config_jumpers[1] == '1' else False
no_anim_jumper = True if config_jumpers[2] == '1' else False

# Initializing the pygame library and pygame.mixer library for music playback 
pygame.init()
pygame.mixer.init()

# Setting the game window, caption, and icon (if exists)
# If the icon file is not found, it will use pygame's default icon
Screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('Pytdle')
icon = pygame.image.load(GAME_ICON_PATH) if os.path.exists(GAME_ICON_PATH) else None
if icon: pygame.display.set_icon(icon)

# Initializing sound files and fonts
if all_files_exist:
    correct_sound = pygame.mixer.Sound(CORRECT_SOUND_PATH)
    misplaced_sound = pygame.mixer.Sound(MISPLACED_SOUND_PATH)
    wrong_sound = pygame.mixer.Sound(WRONG_SOUND_PATH)
    general_sound = pygame.mixer.Sound(GENERAL_SOUND_PATH)
    intro_music = pygame.mixer.Sound(INTRO_SOUND_PATH)
    intro_fade_sound = pygame.mixer.Sound(INTRO_FADE_SOUND_PATH)
    win_music = pygame.mixer.Sound(WIN_MUSIC_PATH)
    lose_music = pygame.mixer.Sound(LOSE_MUSIC_PATH)

    font_single = pygame.font.Font(FONT_PATH, SQUARE_SIZE)
    font_half = pygame.font.Font(FONT_PATH, SQUARE_SIZE // 2)
    font_double = pygame.font.Font(FONT_PATH, SQUARE_SIZE * 2)
    font_onefive = pygame.font.Font(FONT_PATH, 3 * SQUARE_SIZE // 2)

'''
    check_word_letters(guess, secret_word):
    Function check_word_letters(guess, secret_word) - checks the letters of the word guess 
    and compares them with secret_word.
    Returns the designation of letters of the guess word as a string.
        2 - the letter is in correct position
        1 - the letter is present, but misplaced
        0 - the letter is not present
'''
def check_word_letters(guess, secret_word):
    # The string for designation of letters in the guess word
    correct = []
    matched_indices = set()
    for i in range(0, len(secret_word)):
        if guess[i] == secret_word[i]:
            correct.append('2')
            matched_indices.add(i)
        elif guess[i] in secret_word and secret_word.index(guess[i]) not in matched_indices:
            correct.append('1')
            matched_indices.add(secret_word.index(guess[i]))
        else:
            correct.append('0')
    return correct

'''
    delay(length):
    Function delay(time) - delays the code by 'time' miliseconds.
    Arguments:
        time - time of delay in miliseconds
    Used as a substitute for pygame function pygame.time.delay
    due to stability issues
'''
def delay(time):
    for _ in range(time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(1)
    return

'''
    fill_screen(colour):
    Function fill_screen(colour) - fills the screen
    Arguments:
        colour - colour of the screen after execution
'''
def fill_screen(colour):
    Screen.fill(colour)
    pygame.display.update()
    return

'''
    draw_grid(colour, rows, cols):
    Function draw_grid(colour, rows, cols) - draws a grid, which contains
    rows x cols squares.
    Arguments:
        colour - colour of the squares
        rows - amount of squares on the y axis
        cols - amount of squaes on the x axis
'''
def draw_grid(colour, rows, cols):

    for j in range(0, rows):
        for i in range(0, cols):
            xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            ypos = GRID_Y_OFFSET + j * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
            pygame.display.update()
            delay(2000 // (rows * cols))
    return

'''
    draw_letters():
    Function draw_letters() - draws the letters on the squares.
    Used for only for the game intro sequence.
'''
def draw_letters():
    intro_letters = list("PERSONSYSTEMPYTHONBRIDLEGORBLEDEMOTE")
    for j in range(0, GRID_ROWS):
        for i in range(0, GRID_COLS):
            xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            ypos = GRID_Y_OFFSET + j * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            current_letter = intro_letters[j * GRID_COLS + i]
            letter = font_single.render(current_letter, True, COLOUR_WHITE)
            letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos + SQUARE_SIZE // 2 - letter.get_height() // 2))
            Screen.blit(letter, letter_rect)
            pygame.display.update()
            general_sound.play()
            delay(3500 // (GRID_COLS * GRID_ROWS))
    return
 
'''
    correct_letters():
    Function correct_letters() - draws the colour of the squares.
    Used for only for the game intro sequence.
''' 
def correct_letters():
    intro_letters = list("PERSONSYSTEMPYTHONBRIDLEGORBLEDEMOTE")
    intro_correct_letters = list("212000020010222000010222002022100002")
    for j in range(0, GRID_ROWS):
        for i in range(0, GRID_COLS):
            xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            ypos = GRID_Y_OFFSET + j * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
            current_letter = intro_letters[j * GRID_COLS + i]
            
            if intro_correct_letters[j * GRID_COLS + i] == '2': colour = COLOUR_GREEN
            elif intro_correct_letters[j * GRID_COLS + i] == '1': colour = COLOUR_ORANGE
            else: colour = COLOUR_RED
            pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
            letter = font_single.render(current_letter, True, COLOUR_WHITE)
            letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos + SQUARE_SIZE // 2 - letter.get_height() // 2))
            Screen.blit(letter, letter_rect)
            pygame.display.update()
            if colour == COLOUR_GREEN: correct_sound.play()
            elif colour == COLOUR_ORANGE: misplaced_sound.play()
            else: wrong_sound.play()
            delay(3500 // (GRID_COLS * GRID_ROWS))
    return

'''
    draw_title():
    Function draw_title() - draws the game's title.
    Used for only for game intro sequence.
'''
def draw_title():
    intro_music.play()
    title_font = pygame.font.Font(FONT_PATH, SQUARE_SIZE * 4)
    subtitle_font = pygame.font.Font(FONT_PATH, SQUARE_SIZE // 2)
    title_text = 'PYTDLE'
    subtitle_text = 'Made by Daniels Laurinavics'
    title_width = len(title_text) * (SQUARE_SIZE * 4 - 3 * SQUARE_SIZE // 2)
    title_x_offset = (SCREEN_X - title_width) // 2
    title_y_offset = SCREEN_Y - 280
    
    delay(500)
    
    for i in range(0, len(title_text)):
            xpos = title_x_offset + i * (SQUARE_SIZE * 4 - 3 * SQUARE_SIZE // 2)
            ypos = title_y_offset
            title = title_font.render(title_text[i], True, COLOUR_BLACK)
            title_rect = title.get_rect(topleft=(xpos, ypos))
            Screen.blit(title, title_rect)
            pygame.display.update()
            delay(500)
            
    for i in range(0, len(title_text)):
            xpos = title_x_offset + i * (SQUARE_SIZE * 4 - 3 * SQUARE_SIZE // 2)
            ypos = title_y_offset
            title = title_font.render(title_text[i], True, COLOUR_RED)
            title_rect = title.get_rect(topleft=(xpos, ypos))
            Screen.blit(title, title_rect)
            pygame.display.update()
            delay(500 // len(title_text))
            
    delay(1000)
    
    subtitle = subtitle_font.render(subtitle_text, True, COLOUR_BLACK)
    subtitle_rect = subtitle.get_rect(center=(SCREEN_X // 2, ypos + SQUARE_SIZE * 4 + 50))
    Screen.blit(subtitle, subtitle_rect)
    pygame.display.update()
    return

'''
    transition(colour, type, duration):
    Function transition(colour, type, duration) - makes an transition animation by filling the screen with lines.
    Arguments:
        colour - colour of lines - a tuple with colour RGB settings or if a string 'random' - the lines will have a random colour
        type - type of animation - 'one-side', 'two-side', 'two-centre'
        duration - duration of the animation in miliseconds
    For painting the screen without animation, use function fill_screen(colour)
'''
def transition(colour, type, duration):
    # Using a animationless function in case if 'disable animations'
    # jumper is enabled in the configuration file.
    if no_anim_jumper == True:
        if colour != 'random': fill_screen(colour)
        else: colour = COLOUR_BLACK
    # Set of colours for random backgrounds
    if colour == 'random': colours = [(30, 30, 30), (30, 0, 0), (0, 30, 0), (0, 0, 30), (50, 30, 0), (30, 50, 0), (0, 30, 50), (0, 50, 30)]
    if type == 'one-side':      # One-side transition, from top to bottom.
        for y in range(0, SCREEN_Y + 1):
            if colour == 'random': pygame.draw.line(Screen, random.choice(colours), (0, y), (SCREEN_X, y), 1)
            else: pygame.draw.line(Screen, colour, (0, y), (SCREEN_X, y), 1)
            pygame.display.update()
            delay(duration // (SCREEN_Y + 1))
    
    elif type == 'two-side':       # Two-side transition, from top+bottom to centre
        for y in range(0, SCREEN_Y // 2 + 1):
            if colour == 'random':
                pygame.draw.line(Screen, random.choice(colours), (0, y), (SCREEN_X, y), 1)
                pygame.draw.line(Screen, random.choice(colours), (0, SCREEN_Y-y), (SCREEN_X, SCREEN_Y-y), 1)
            else:
                pygame.draw.line(Screen, colour, (0, y), (SCREEN_X, y), 1)
                pygame.draw.line(Screen, colour, (0, SCREEN_Y-y), (SCREEN_X, SCREEN_Y-y), 1)
            pygame.display.update()
            delay(duration // (SCREEN_Y // 2 + 1))
    
    elif type == 'two-centre':     # Two-from-centre transition, from centre to top/bottom
        for y in range(0, SCREEN_Y // 2 + 1):
            if colour == 'random':
                pygame.draw.line(Screen, random.choice(colours), (0, SCREEN_Y // 2 - y), (SCREEN_X, SCREEN_Y // 2 - y), 1)
                pygame.draw.line(Screen, random.choice(colours), (0, SCREEN_Y // 2 + y), (SCREEN_X, SCREEN_Y // 2 + y), 1)
            else:
                pygame.draw.line(Screen, colour, (0, SCREEN_Y // 2 - y), (SCREEN_X, SCREEN_Y // 2 - y), 1)
                pygame.draw.line(Screen, colour, (0, SCREEN_Y // 2 + y), (SCREEN_X, SCREEN_Y // 2 + y), 1)
            pygame.display.update()
            delay(duration // (SCREEN_Y // 2 + 1))
            
    return

'''
    intro()
    Function intro() - display the intro sequence
''' 
def intro():
    fill_screen(COLOUR_WHITE)
    delay(1000)
    draw_grid(COLOUR_BLACK, GRID_ROWS, GRID_COLS)
    delay(1000)
    draw_letters()
    correct_letters()   
    delay(1000)
    draw_title()
    delay(5000)
    intro_fade_sound.play()
    transition(COLOUR_BLACK, 'two-side', 1000)
    return

'''
    titlebar(colour, text_colour, text):
    Function titlebar(colour, text_colour, text) - draws a title bar on top of the page.
    Arguments:
        colour - colour of the title bar
        text_colour - colour of text in the title bar
        text - text to be shown on the title bar
'''
def titlebar(colour, text_colour, text):
    pygame.draw.rect(Screen, colour, (0, 0, SCREEN_X, 2 * SQUARE_SIZE // 3 ))
    title = font_half.render(text, True, text_colour)
    title_rect = title.get_rect(center=(SCREEN_X // 2, SQUARE_SIZE // 4))
    Screen.blit(title, title_rect)
    pygame.display.update()
    return

'''
    draw_keyboard(letters, correct, hard):
    Function draw_keyboard(letters, correct, hard) - displays the keyboard.
    Colour of key depends on is the letter correct, misplaced or wrong.
    Arguments:
        letters - string of letters
        correct - string of flags (0, 1, 2), which determine their correctness
        hard - bool, flag used for hard game mode
'''
def draw_keyboard(letters, correct, hard):
    # Setting up keyboard keys
    row1 = list('QWERTYUIOP')
    row2 = list('ASDFGHJKL')
    row3 = list('ZXCVBNM')
    
    # Setting the x-axis offset, in order for the key rows to be centred
    row1_width = len(row1) * (SQUARE_SIZE + SQUARE_MARGIN) - SQUARE_MARGIN
    row2_width = len(row2) * (SQUARE_SIZE + SQUARE_MARGIN) - SQUARE_MARGIN
    row3_width = len(row3) * (SQUARE_SIZE + SQUARE_MARGIN) - SQUARE_MARGIN
    
    row1_x_offset = (SCREEN_X - row1_width) // 2
    row2_x_offset = (SCREEN_X - row2_width) // 2
    row3_x_offset = (SCREEN_X - row3_width) // 2
    
    # Setting the y-axis offset
    row1_y_offset = SCREEN_Y - (SCREEN_Y // 3)
    row2_y_offset = row1_y_offset + (SQUARE_SIZE + SQUARE_MARGIN)
    row3_y_offset = row1_y_offset + 2 * (SQUARE_SIZE + SQUARE_MARGIN)
    
    # Determining which keys are correct, misplaced or wrong
    correct_keys = []
    misplaced_keys = []
    wrong_keys = []
    for i in range(0, max(len(letters), len(correct))):
        if correct[i] == '0': wrong_keys.append(letters[i])
        elif correct[i] == '1': misplaced_keys.append(letters[i])
        elif correct[i] == '2': correct_keys.append(letters[i])
    
    # Drawing the keyboard's keys
    for i in range(0, len(row1)):
        colour = COLOUR_GRAY
        if row1[i] in wrong_keys and hard == False: colour = COLOUR_RED
        if row1[i] in misplaced_keys and hard == False: colour = COLOUR_ORANGE
        if row1[i] in correct_keys: colour = COLOUR_GREEN
        xpos = row1_x_offset + i * (SQUARE_SIZE + SQUARE_MARGIN)    # Key location on the X axis
        ypos = row1_y_offset    # Key location on the Y axis
        pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
        letter = font_single.render(row1[i], True, COLOUR_WHITE)
        # Placing the key's letter to the middle of the key square
        letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos - letter.get_width() // 2))
        Screen.blit(letter, letter_rect)
    
    for i in range(0, len(row2)):
        colour = COLOUR_GRAY
        if row2[i] in wrong_keys and hard == False: colour = COLOUR_RED
        if row2[i] in misplaced_keys and hard == False: colour = COLOUR_ORANGE
        if row2[i] in correct_keys: colour = COLOUR_GREEN
        xpos = row2_x_offset + i * (SQUARE_SIZE + SQUARE_MARGIN)    # Key location on the X axis
        ypos = row2_y_offset        # Key location on the Y axis
        pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
        letter = font_single.render(row2[i], True, COLOUR_WHITE)
        # Placing the key's letter to the middle of the key square
        letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos - letter.get_width() // 2))
        Screen.blit(letter, letter_rect)
    
    for i in range(0, len(row3)):
        colour = COLOUR_GRAY
        if row3[i] in wrong_keys and hard == False: colour = COLOUR_RED
        if row3[i] in misplaced_keys and hard == False: colour = COLOUR_ORANGE
        if row3[i] in correct_keys: colour = COLOUR_GREEN
        xpos = row3_x_offset + i * (SQUARE_SIZE + SQUARE_MARGIN)    # Key location on the X axis
        ypos = row3_y_offset        # Key location on the Y axis
        pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
        letter = font_single.render(row3[i], True, COLOUR_WHITE)
        # Placing the key's letter to the middle of the key square
        letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos - letter.get_width() // 2))
        Screen.blit(letter, letter_rect)
    
    pygame.display.flip()
    return

'''
    play(hard, skip_jumper):
    Function play(hard, skip_jumper) - game logic
    Arguments:
        hard - bool value for enabling hard mode_title
        skip_jumper - bool value for skipping the pre-game (game explanation) scene
''' 
def play(hard, skip_jumper):
    # Transition animation.
    pygame.display.flip()
    intro_fade_sound.play()
    
    if hard: 
        transition(COLOUR_RED, 'two-side', 500)
        transition(COLOUR_BLACK, 'two-centre', 500)
    else: 
        transition(COLOUR_WHITE, 'two-side', 500)
        transition(COLOUR_BLACK, 'two-centre', 500)

    delay(500)
    
    # If 'skip rules screen' jumper is enabled, it skips the game's rules section,
    # going straight to the game
    if skip_jumper == False:
        # Game explanation (rule) scene.
        if hard:
            transition((50, 0, 0), 'two-side', 1000)
            titlebar(COLOUR_RED, COLOUR_WHITE, 'pytdle HARD MODE')
        else:
            transition((0, 0, 50), 'two-side', 1000)
            titlebar(COLOUR_BLUE, COLOUR_WHITE, 'pytdle NORMAL MODE')
            
        delay(1000)
        
        # Text for the introduction text depends on mode
        if hard: text = ["BORED OF NORMAL MODE? OKAY THEN...","IT'S TIME FOR A PROPER CHALLENGE!","READ THE RULES BELOW..."]
        else: text = ["Prepare your brain,","it's time to guess the secret word.","Read the rules below..."]
        
        # Drawing the introduction text.
        current_line = 0
        for line in text:
            letter_width_margin = SQUARE_SIZE // 5
            line_x_offset = SCREEN_X // 16
            line_y_offset = SCREEN_Y // 4
            for i in range (0, len(line)):
                xpos = line_x_offset + i * ((SQUARE_SIZE // 2) - letter_width_margin)
                ypos = line_y_offset + current_line * (2 * SQUARE_SIZE // 3)
                letter = font_half.render(line[i], True, COLOUR_WHITE)
                letter_rect = letter.get_rect(topleft=(xpos, ypos))
                Screen.blit(letter, letter_rect)
                pygame.display.update()
                if line[i] != ' ':
                    if hard: wrong_sound.play()
                    else: general_sound.play()
                if line[i] in [',', '?', '!']: delay(500)
                else: delay(70)
            current_line += 1
            delay(500)
        
        # Drawing the rules section
        if hard: rule1 = font_half.render(f'You have {GRID_COLS - 2} tries to guess the secret word', True, COLOUR_WHITE)
        else: rule1 = font_half.render(f'You have {GRID_COLS} tries to guess the secret word', True, COLOUR_WHITE)
        rule2 = font_half.render('When you enter the word, press ENTER,', True, COLOUR_WHITE)
        rule3 = font_half.render('Then you will be able to see the correct letters', True, COLOUR_WHITE)      
        
        rule1_rect = rule1.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 2 - 35))
        rule2_rect = rule1.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 2 - 35 + (SQUARE_SIZE // 2 + 10)))
        rule3_rect = rule1.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 2 - 35 + 2 * (SQUARE_SIZE // 2 + 10)))
        
        Screen.blit(rule1, rule1_rect)
        Screen.blit(rule2, rule2_rect)
        Screen.blit(rule3, rule3_rect)
        
        pygame.draw.rect(Screen, COLOUR_GREEN, (SCREEN_X // 16, SCREEN_Y // 2 + 2 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if not hard: pygame.draw.rect(Screen, COLOUR_ORANGE, (SCREEN_X // 16, SCREEN_Y // 2 + 2 * SQUARE_SIZE + (SQUARE_SIZE + 10), SQUARE_SIZE, SQUARE_SIZE))
        if hard: pygame.draw.rect(Screen, COLOUR_GRAY, (SCREEN_X // 16, SCREEN_Y // 2 + 2 * SQUARE_SIZE + (SQUARE_SIZE + 10), SQUARE_SIZE, SQUARE_SIZE))
        else: pygame.draw.rect(Screen, COLOUR_RED, (SCREEN_X // 16, SCREEN_Y // 2 + 2 * SQUARE_SIZE + 2 * (SQUARE_SIZE + 10), SQUARE_SIZE, SQUARE_SIZE))
        
        box_correct = font_half.render('This letter is in correct position', True, COLOUR_WHITE)
        box_misplaced = font_half.render('This letter is present, but misplaced', True, COLOUR_WHITE)
        box_wrong = font_half.render('This letter is not present', True, COLOUR_WHITE)
        box_wrong2 = font_half.render('This letter is not present or is misplaced', True, COLOUR_WHITE)
        
        box_correct_rect = box_correct.get_rect(topleft=(SCREEN_X // 16 + SQUARE_SIZE + 10, SCREEN_Y // 2 + 2 * SQUARE_SIZE))
        if not hard: box_misplaced_rect = box_misplaced.get_rect(topleft=(SCREEN_X // 16 + SQUARE_SIZE + 10, SCREEN_Y // 2 + 2 * SQUARE_SIZE + (SQUARE_SIZE + 10)))
        if hard: box_wrong2_rect = box_wrong2.get_rect(topleft=(SCREEN_X // 16 + SQUARE_SIZE + 10, SCREEN_Y // 2 + 2 * SQUARE_SIZE + (SQUARE_SIZE + 10)))
        else: box_wrong_rect = box_wrong.get_rect(topleft=(SCREEN_X // 16 + SQUARE_SIZE + 10, SCREEN_Y // 2 + 2 * SQUARE_SIZE + 2 * (SQUARE_SIZE + 10)))
        
        Screen.blit(box_correct, box_correct_rect)
        if not hard: Screen.blit(box_misplaced, box_misplaced_rect)
        if hard: Screen.blit(box_wrong2, box_wrong2_rect)
        else: Screen.blit(box_wrong, box_wrong_rect)
        pygame.display.update()
        
        delay(3000)
        
        wait_text = font_half.render('Press any key to continue.', True, COLOUR_WHITE)
        wait_text_rect = wait_text.get_rect(center=(SCREEN_X // 2, SCREEN_Y - SQUARE_SIZE // 2))
        Screen.blit(wait_text, wait_text_rect)
        pygame.display.update()
        if hard: wrong_sound.play()
        else: general_sound.play()
        
        # Waiting for input or click of 'Close' button.
        running = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                        running = False
           
            if running == False:
                pygame.display.flip()
                break
    
    # Opening the words file,gathering all words which comply with requirements and choosing the secret word.
    # Requirements: 6 letters long, only letters allowed.
    # All gathered words are converted to upper-case.
    with open(WORDS_FILE_PATH, 'r', encoding='utf-8') as file:
        words = [word.strip().upper() for word in file.readlines() if word.strip().isalpha() and len(word.strip()) == 6]
    secret_word = random.choice(words)
    
    # Drawing the game screen
    if hard:
        transition(COLOUR_BLACK, 'two-side', 500)
        transition((50,0,0), 'two-centre', 500)
    else:
        transition((COLOUR_BLACK), 'two-side', 500)
        transition((0,0,50), 'two-centre', 500)
        
    titlebar(COLOUR_BLUE, COLOUR_WHITE, 'Get ready!')
    # Drawing the grid
    if hard: draw_grid(COLOUR_GRAY, GRID_COLS - 2, GRID_COLS)
    else: draw_grid(COLOUR_GRAY, GRID_ROWS, GRID_COLS)
    
    # Defining the list for submitted guesses
    if hard: guesses = [list('      '), list('      '), list('      '), list('      ')]
    else: guesses = [list('      '), list('      '), list('      '), list('      '), list('      '), list('      ')]
    # Defining the list for correct letter designation.
    if hard: correct = [list('      '), list('      '), list('      '), list('      ')]
    else: correct = [list('      '), list('      '), list('      '), list('      '), list('      '), list('      ')]

    guess_input = []    # Letters of the guess not yet submitted
    
    max_attempts = 4 if hard else 6     # Setting the maximum number of attempts
    attempt_no = 0      # Current attempt number
    
    # Game loop begins
    running = True      # Flag for continuation of game loop
    game_won = False    # Flag for checking if game is won
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            # Keypresses are allowed only when the game is not over yet.
            if event.type == pygame.KEYDOWN and attempt_no < max_attempts and game_won == False:
                # If any of the letter keys (A-Z) has been pressed, it is added to guess_input,,
                # and then draws the letter on the screen
                # The letter is added only if the length of current guess input is not 6
                if pygame.K_a <= event.key <= pygame.K_z and len(guess_input) < GRID_COLS:
                    letter = chr(event.key).upper()
                    guess_input.append(letter)
                    if len(guess_input) > 0:
                        for i in range(0, len(guess_input)):
                            xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                            ypos = GRID_Y_OFFSET + attempt_no * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                            current_letter = guess_input[i]
                            letter = font_single.render(current_letter, True, COLOUR_WHITE)
                            letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos + SQUARE_SIZE // 2 - letter.get_height() // 2))
                            Screen.blit(letter, letter_rect)
                        pygame.display.update()
                # When BACKSPACE has been pressed, the last letter of guess_input is being deleted,
                # if the list is not empty, and then a grid rectangle overwrites the drawing of the old letter
                if event.key == pygame.K_BACKSPACE:
                    if len(guess_input) > 0:
                        guess_input.pop()
                        xpos = GRID_X_OFFSET - SQUARE_MARGIN + len(guess_input) * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                        ypos = GRID_Y_OFFSET + attempt_no * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                        pygame.draw.rect(Screen, COLOUR_GRAY, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
                        pygame.display.update()
                    else: wrong_sound.play()
                # When ENTER has been pressed, at first if the length of the input is 6 and such word exists
                # in the words file and has not been already used as a guess.
                if event.key == pygame.K_RETURN:
                    if len(guess_input) == 6 and ''.join(guess_input) in words and guess_input not in guesses:
                        # Checking is the word correct to set up the correct word flag
                        for i in range (0, 6):
                            guesses[attempt_no][i] = guess_input[i]
                        for j in range(0, 6):
                            correct[attempt_no][j] = check_word_letters(''.join(guess_input), secret_word)[j]
                        word_correct = False
                        for z in range(0, 6):
                            if correct[attempt_no][z] == '2': word_correct = True
                            else:
                                word_correct = False
                                break
                                
                        if word_correct == True: game_won = True    # Setting the won game flag.
                        
                        # Drawing the coloured rectangles, representing the correctness of letters.
                        for i in range(0, GRID_COLS):
                            xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                            ypos = GRID_Y_OFFSET + attempt_no * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                            current_letter = guesses[attempt_no][i]
                            # Choice of colour
                            if hard:
                                if correct[attempt_no][i] == '2': colour = COLOUR_GREEN
                                else: colour = COLOUR_GRAY
                            else:
                                if correct[attempt_no][i] == '2': colour = COLOUR_GREEN
                                elif correct[attempt_no][i] == '1': colour = COLOUR_ORANGE
                                elif correct[attempt_no][i] == '0': colour = COLOUR_RED
                                else: colour = COLOUR_GRAY
                            pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
                            letter = font_single.render(current_letter, True, COLOUR_WHITE)
                            letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos + SQUARE_SIZE // 2 - letter.get_height() // 2))
                            Screen.blit(letter, letter_rect)
                            if colour == COLOUR_GREEN: correct_sound.play()
                            elif colour == COLOUR_ORANGE: misplaced_sound.play()
                            else: wrong_sound.play()
                            pygame.display.update()
                            delay(250)
                        
                        guess_input.clear() # Clearing the current guess input list
                        attempt_no += 1 # Iterating the attempt number
                    
                    # If the guess input is not 6 letters long, it displays an error
                    elif len(guess_input) != 6:
                        wrong_sound.play()
                        titlebar(COLOUR_RED, COLOUR_WHITE, 'The word is not 6 letters long!')
                        delay(1000)
                    # If the guess input is not in the word list, it displays an error
                    elif ''.join(guess_input) not in words:
                        wrong_sound.play()
                        titlebar(COLOUR_RED, COLOUR_WHITE, 'The word written is not in the word list!')
                        delay(1000)
                    # If the guess input is already used, it displays an error
                    elif guess_input in guesses:
                        wrong_sound.play()
                        titlebar(COLOUR_RED, COLOUR_WHITE, 'You already used this word!')
                        delay(1000)
        
        # Drawing the keyboard
        draw_keyboard(''.join(''.join(guess) for guess in guesses), ''.join(''.join(corr) for corr in correct), hard)
        
        if attempt_no == 0: titlebar(COLOUR_BLUE, COLOUR_WHITE, 'Write your FIRST guess!')
        elif attempt_no < max_attempts and game_won == False: titlebar(COLOUR_BLUE, COLOUR_WHITE, f'Attempt {attempt_no+1} out of {max_attempts}')
        # In case of a lose, a 'you lose' message is shown and losing record is 
        # written to the statistics file, and then player returns to main menu
        if attempt_no == max_attempts and game_won == False: 
            titlebar(COLOUR_RED, COLOUR_WHITE, f'You lost! The correct word was {secret_word}.')
            delay(200)
            lose_music.play()
            running = False

            # Writing to the stats file
            # 'L - lose in normal mode, 'Lh' - lose in hard mode
            with open(STATS_FILE_PATH, 'a') as stats:
                if hard: stats.write('Lh\n')
                else: stats.write('L\n')
            
            delay(7000)
            intro_fade_sound.play()
            transition(COLOUR_RED, 'two-side', 500)
            transition(COLOUR_BLACK, 'two-centre', 500)
            
            return main_menu() # Returning to the main menu
        
        # In case of a win, a 'you win' message is shown and winning record is 
        # written to the statistics file, and then player returns to main menu
        if game_won == True:
            titlebar(COLOUR_GREEN, COLOUR_WHITE, f'You won! The correct word was {secret_word}.')
            delay(200)
            win_music.play()
            running = False
            
            # Writing to the stats file
            # 'W - win in normal mode, 'Wh' - win in hard mode
            with open(STATS_FILE_PATH, 'a') as stats:
                if hard: stats.write('Wh\n')
                else: stats.write('W\n')
            
            delay(7000)
            intro_fade_sound.play()
            transition(COLOUR_GREEN, 'two-side', 500)
            transition(COLOUR_BLACK, 'two-centre', 500)
            
            return main_menu() # Returning to the main menu
        
        # Drawing coloured grid rectangles and their letters
        # for guesses already made.
        for j in range(0, max_attempts):
            if j == attempt_no: continue
            for i in range(0, GRID_COLS):
                xpos = GRID_X_OFFSET - SQUARE_MARGIN + i * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                ypos = GRID_Y_OFFSET + j * (SQUARE_SIZE + SQUARE_MARGIN) + SQUARE_MARGIN
                current_letter = guesses[j][i]
                if hard:
                    if correct[j][i] == '2': colour = COLOUR_GREEN
                    else: colour = COLOUR_GRAY
                else:
                    if correct[j][i] == '2': colour = COLOUR_GREEN
                    elif correct[j][i] == '1': colour = COLOUR_ORANGE
                    elif correct[j][i] == '0': colour = COLOUR_RED
                    else: colour = COLOUR_GRAY
                pygame.draw.rect(Screen, colour, (xpos, ypos, SQUARE_SIZE, SQUARE_SIZE))
                letter = font_single.render(current_letter, True, COLOUR_WHITE)
                letter_rect = letter.get_rect(topleft=(xpos + SQUARE_SIZE // 2 - letter.get_width() // 2, ypos + SQUARE_SIZE // 2 - letter.get_height() // 2))
                Screen.blit(letter, letter_rect)
                
        pygame.display.update()

'''
    statistics():
    Function statistics() - shows the statistics screen and its content.
'''
def statistics():
    # Transition animation.
    pygame.display.flip()
    intro_fade_sound.play()
    transition(COLOUR_BLUE, 'two-side', 500)
    transition(COLOUR_BLACK, 'two-centre', 500)
    delay(500)
    
    # Drawing the screen background, title bar, and heading.
    transition((0,0,50), 'two-side', 1000)
    titlebar(COLOUR_BLUE, COLOUR_WHITE, 'pytdle player statistics')
    mode_title = font_onefive.render('Player statistics', True, COLOUR_WHITE)
    mode_title_rect = mode_title.get_rect(center=(SCREEN_X // 2, (SCREEN_Y // 4) // 2))
    Screen.blit(mode_title, mode_title_rect)
    pygame.display.update()
    
    # Opening the statistics file and gathering information about the player's statistics.
    # Only lines whose length is 2 charactes or less and gathered: this is because the
    # statistics values used are 'W', 'L', 'Wh' or 'Lh'
    with open(STATS_FILE_PATH, 'r') as file:
        stats = [stat.strip() for stat in file.readlines() if stat.strip().isalpha() and len(stat.strip()) <= 2]
    
    # Calculating all statistics attributes.
    times_played = len(stats)    
    times_played_hard = 0
    for i in range(0, times_played):
        if stats[i] == 'Wh' or stats[i] == 'Lh': times_played_hard += 1   
    wins = 0
    for i in range(0, times_played):
        if stats[i] == 'W' or stats[i] == 'Wh': wins += 1
    wins_hard = 0
    for i in range(0, times_played):
        if stats[i] == 'Wh': wins_hard += 1
    loses = times_played - wins
    loses_hard = times_played_hard - wins_hard
    
    # Drawing the statistical attributes.
    text_played = font_half.render(f'Total games played: {times_played}', True, COLOUR_WHITE)
    text_played_hard = font_half.render(f'out of them in HARD MODE: {times_played_hard}', True, COLOUR_RED)
    text_wins = font_half.render(f'Times won: {wins}', True, COLOUR_WHITE)
    text_wins_hard = font_half.render(f'out of them in HARD MODE: {wins_hard}', True, COLOUR_RED)
    text_loses = font_half.render(f'Times lost: {loses}', True, COLOUR_WHITE)
    text_loses_hard = font_half.render(f'out of them in HARD MODE: {loses_hard}', True, COLOUR_RED)
    
    text_played_rect = text_played.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 0 * (2 * SQUARE_SIZE // 3) ))
    text_played_hard_rect = text_played_hard.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 1 * (2 * SQUARE_SIZE // 3)))
    text_wins_rect = text_wins.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 3 * (2 * SQUARE_SIZE // 3)))
    text_wins_hard_rect = text_wins_hard.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 4 * (2 * SQUARE_SIZE // 3)))
    text_loses_rect = text_loses.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 6 * (2 * SQUARE_SIZE // 3)))
    text_loses_hard_rect =  text_loses_hard.get_rect(topleft=(SCREEN_X // 16, SCREEN_Y // 3 + 7 * (2 * SQUARE_SIZE // 3)))
    
    delay(500)
    
    for t, tr in zip([text_played, text_wins, text_loses, text_played_hard, text_wins_hard, text_loses_hard],
                     [text_played_rect, text_wins_rect, text_loses_rect, text_played_hard_rect, text_wins_hard_rect, text_loses_hard_rect]):
        Screen.blit(t, tr)
        pygame.display.update()
        general_sound.play()
        delay(300)
    
    win_music.play()
    delay(5000)
    general_sound.play()
    wait_text = font_half.render('Press ENTER to return to the main menu.', True, COLOUR_WHITE)
    wait_text_rect = wait_text.get_rect(center=(SCREEN_X // 2, SCREEN_Y - SCREEN_Y // 8))
    Screen.blit(wait_text, wait_text_rect)
    pygame.display.update()    
    
    # Waiting until player presses ENTER.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
        
        pygame.display.update()
    
    # Transition animation.
    intro_fade_sound.play()
    transition(COLOUR_BLUE, 'two-centre', 500)
    transition(COLOUR_BLACK, 'two-side', 500)
    delay(100)
    
    return main_menu()     # Returning to the main menu.

'''
    options():
    Function options() - displays the options menu, allowing to change game's configuration
'''   
def options():
    # Transition animation.
    pygame.display.flip()
    intro_fade_sound.play()
    transition(COLOUR_ORANGE, 'two-side', 500)
    transition(COLOUR_BLACK, 'two-centre', 500)
    delay(1000)
    
    # Drawing the title bar, heading and other non-dynamic UI elements.
    titlebar(COLOUR_BLUE, COLOUR_WHITE, 'pytdle options')
    screen_title = font_onefive.render('Game options', True, COLOUR_WHITE)
    screen_title_rect = screen_title.get_rect(center=(SCREEN_X // 2, (SCREEN_Y // 4) // 2))
    Screen.blit(screen_title, screen_title_rect)
    
    restart = font_half.render('NOTE: Changes will not take into effect', True, COLOUR_WHITE)
    restart2 = font_half.render('until the game is restarted.', True, COLOUR_RED)
    restart_rect = restart.get_rect(topleft=(SCREEN_X // 32, (SCREEN_Y // 3) + (3 * SQUARE_SIZE)))
    restart2_rect = restart2.get_rect(topleft=(SCREEN_X // 32, (SCREEN_Y // 3) + (3 * SQUARE_SIZE) + (SQUARE_SIZE // 2) + 5))
    Screen.blit(restart, restart_rect)
    Screen.blit(restart2, restart2_rect)
    
    bottom_text = ['Use arrow keys to navigate and change options','Press ENTER to save changes', 'Press ESC to return to the main menu']
    ypos = SCREEN_Y - SCREEN_Y // 5
    for text in bottom_text:
        text = font_half.render(text, True, COLOUR_WHITE)
        text_rect = text.get_rect(center=(SCREEN_X // 2, ypos))
        Screen.blit(text, text_rect)
        ypos += 2 * SQUARE_SIZE // 3
    pygame.display.update()

    option_settings = config_jumpers    # Copying the configuration jumpers to another list
    changes_saved = True    # Flag for checking are the changes saved.
    selected_option = 0     # Currently selected (active) option
    options = ["Don't show the intro sequence","Don't show the rules screen","Disable animations"]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Pressing ESCAPE will return the user to the main menu.
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Pressing up/down arrow keys will change the selected option.
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                    general_sound.play()
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                    general_sound.play()
                # Pressing left/right arrow keys will change their values.
                elif event.key == pygame.K_LEFT:
                    if option_settings[selected_option] == '1':
                        general_sound.play()
                        option_settings[selected_option] = '0'
                        changes_saved = False
                    else: wrong_sound.play()
                elif event.key == pygame.K_RIGHT:
                    if option_settings[selected_option] == '0':
                        general_sound.play()
                        option_settings[selected_option] = '1'
                        changes_saved = False
                    else: wrong_sound.play()
                elif event.key == pygame.K_RETURN:
                    # Pressing ENTER will write changes to the config file.
                    with open(CONFIG_FILE_PATH, 'r') as config:
                        lines = config.readlines()
                    for i in range(2, len(config_jumpers) + 2):
                        lines[i] = f'{option_settings[i-2]}\n'
                    with open(CONFIG_FILE_PATH, 'w') as config:
                        config.writelines(lines)
                    changes_saved = True
                    correct_sound.play()
                    titlebar(COLOUR_GREEN, COLOUR_WHITE, 'Game configuration successfully saved')
                    delay(2000)
                    general_sound.play()
                    titlebar(COLOUR_ORANGE, COLOUR_WHITE, "Don't forget to restart the game for changes to take effect!")
                    
                   
        # Transition to the main menu if ESCAPE has been pressed
        if running == False:
            intro_fade_sound.play()
            transition(COLOUR_ORANGE, 'two-centre', 500)
            transition(COLOUR_BLACK, 'two-side', 500)
            
            return main_menu()
        
            # Displaying the options
            # The option selected for change is coloured orange
        ypos = SCREEN_Y // 3
        for i, item in enumerate(options):
            if i == selected_option: colour = COLOUR_ORANGE
            else: colour = COLOUR_GRAY
            menu_text = font_half.render(item, True, colour)
            menu_text_rect = menu_text.get_rect(topleft=(SCREEN_X // 32, ypos + i * SQUARE_SIZE))
            Screen.blit(menu_text, menu_text_rect)
        pygame.display.flip()
        
        # Checks the jumpers and shows is it enabled or not.
        ypos = SCREEN_Y // 3
        for jumper in option_settings:
            if jumper == '1':
                text = 'YES'
                colour = COLOUR_GREEN
            else:
                text = ' NO'
                colour = COLOUR_RED
            jumper_text = font_half.render(text, True, colour, COLOUR_BLACK)
            jumper_rect = jumper_text.get_rect(topleft=(SCREEN_X - SCREEN_X // 10, ypos))
            Screen.blit(jumper_text, jumper_rect)
            ypos += SQUARE_SIZE
        pygame.display.flip()
        
        # Reminder to save changes if changes are not saved
        if changes_saved == False:
            remind = font_half.render('YOU HAVE UNSAVED CHANGES!', True, COLOUR_RED)
            remind_rect = remind.get_rect(center=(SCREEN_X // 2, (SCREEN_Y - (SCREEN_Y // 4))))
            Screen.blit(remind, remind_rect)
            pygame.display.update()
        else:
            pygame.draw.rect(Screen, COLOUR_BLACK, (0, (SCREEN_Y - SCREEN_Y // 4) - SQUARE_SIZE // 2, SCREEN_X, SQUARE_SIZE))
            pygame.display.update()

'''
    main_menu():
    Function main_menu() - displays the game's main menu.
'''
def main_menu():
    # Transititon animation
    pygame.display.flip()
    transition('random', 'two-centre', 1000)
    
    # Displaying the titlebar, heading and controls text
    titlebar(COLOUR_BLUE, COLOUR_WHITE, 'pytdle, made by Daniels Laurinavics')
    
    menu_heading = font_double.render('Main Menu', True, COLOUR_WHITE)
    menu_heading_rect = menu_heading.get_rect(center=(SCREEN_X // 2, (SCREEN_Y // 4) // 2))
    Screen.blit(menu_heading, menu_heading_rect)
    pygame.display.update()
    
    controls = font_half.render('Use arrow keys to navigate. Press ENTER to choose.', True, COLOUR_WHITE)
    controls_rect = controls.get_rect(center=(SCREEN_X // 2, SCREEN_Y - (SCREEN_Y // 20)))
    Screen.blit(controls, controls_rect)
    pygame.display.update()
    
    menu_items = ['Play','Play HARD MODE','Statistics', 'Options','Quit']   # All options available
    selected_item = 0   # Currently selected item
    
    # Waiting for player to press 'Close' or press
    # up/down arrow keys or ENTER
    running = True
    selected = False    # If true, an option has been already selected
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN and selected == False:
                # In case of pressing up/down arrow keys, the current selection changes
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    general_sound.play()
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)  
                    general_sound.play()
                # Action if ENTER key has been pressed
                # Depends on the option selected
                elif event.key == pygame.K_RETURN:
                    general_sound.play()
                    if selected_item == 0:
                        selected = True
                        running = False
                        return play(False, skip_rules_jumper)  # Starting the game in normal mode
                    elif selected_item == 1:
                        selected = True
                        running = False
                        return play(True, skip_rules_jumper) # Starting the game in hard mode
                    elif selected_item == 2:
                        selected = True
                        running = False
                        return statistics()    # Moving to the statistics screen
                    elif selected_item == 3:
                        selected = True
                        running = False
                        return options()       # Moving to the options menu
                    elif selected_item == 4:
                        pygame.quit()
                        sys.exit()
        
        # Displaying the menu options
        if selected == False:
            for i, item in enumerate(menu_items):
                # Determining the colour of the menu item
                # Option for the hard mode, if selected, has a different colour
                if i == selected_item and selected_item != 1: colour = COLOUR_ORANGE
                elif i == selected_item and selected_item == 1: colour = COLOUR_RED
                else: colour = COLOUR_GRAY
                menu_text = font_onefive.render(item, True, colour)
                menu_text_rect = menu_text.get_rect(center=(SCREEN_X // 2, (6 * SCREEN_Y // 10) // 2 + i * (8 * SQUARE_SIZE // 5)))
                Screen.blit(menu_text, menu_text_rect)
        pygame.display.flip()

# If all required game files exists, launch the intro sequence     
if all_files_exist == True:
    if skip_intro_jumper == False: intro()
    main_menu()

pygame.quit()