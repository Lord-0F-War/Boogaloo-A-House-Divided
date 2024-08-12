
import sys
import os
from json import load as json_load, dump as json_dump
from PygameManager import pygame


MAIN_FOLDER = os.path.dirname(sys.argv[0])

with open(f'{MAIN_FOLDER}\settings.txt', 'r') as file:
    CONFIGURATIONS:dict     = json_load(file)
    SCREEN_WIDTH:int        = CONFIGURATIONS.get('screen_width')
    SCREEN_HEIGHT:int       = CONFIGURATIONS.get('screen_height')


import PygameManager
Pygame_Manager = PygameManager.Pygame(SCREEN_WIDTH, SCREEN_HEIGHT)

Pygame_Manager.start_pygame()
Pygame_Manager.config_pygame()

CLOCK                           = Pygame_Manager.get_time_variables()
QUIT_EVENT                      = Pygame_Manager.get_event_variables()

REFERENCE_SCREEN_SIZE_X:int     = 1920
REFERENCE_SCREEN_SIZE_y:int     = 1080
FACTOR_X:int                    = SCREEN_WIDTH / REFERENCE_SCREEN_SIZE_X
FACTOR_Y:int                    = SCREEN_HEIGHT / REFERENCE_SCREEN_SIZE_y


def load_assets():
    GFX_FOLDER                          = os.path.join(MAIN_FOLDER,     'GFX')


    ###########################################################################################################################################################
    # -------------------------------------------------------------------- INTERFACE_FOLDER ------------------------------------------------------------------#


    ###########################################################################################################################################################
    #--------------------------------------------------------------------------------------------------------------------------------------- MAIN_MENU_FOLDER #
    INTERFACE_FOLDER                    = os.path.join(GFX_FOLDER,      'INTERFACE')


    MAIN_MENU_FOLDER                    = os.path.join(INTERFACE_FOLDER,      'MAIN_MENU')

    main_menu_background_source 	    = pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'main_menu_background.png')).convert_alpha()
    global main_menu_background
    main_menu_background 	            = pygame.transform.smoothscale(main_menu_background_source, (SCREEN_WIDTH, SCREEN_HEIGHT))

    python_logo_source 					= pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'python_logo.png')).convert_alpha()
    global python_logo
    python_logo 						= pygame.transform.smoothscale_by(python_logo_source, (FACTOR_X, FACTOR_Y))

    game_logo_source 					= pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'game_logo.png')).convert_alpha()
    global game_logo
    game_logo                           = pygame.transform.smoothscale_by(game_logo_source, (FACTOR_X, FACTOR_Y))

    main_menu_UI_source 				= pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'menu_UI.png')).convert_alpha()
    global main_menu_UI
    main_menu_UI                        = pygame.transform.smoothscale_by(main_menu_UI_source, (FACTOR_X, FACTOR_Y))
    
    #--------------------------------------------------------------------------------------------------------------------------------------- MAIN_MENU_FOLDER #
    ###########################################################################################################################################################


    ###########################################################################################################################################################
    #------------------------------------------------------------------------------------------------------------------------------------ OPTIONS_MENU_FOLDER #
    OPTIONS_MENU_FOLDER                 = os.path.join(INTERFACE_FOLDER,      'OPTIONS_MENU')

    game_options_menu_source 			= pygame.image.load(os.path.join(OPTIONS_MENU_FOLDER, 'game_options_menu.png')).convert_alpha()
    global game_options_menu
    game_options_menu                   = pygame.transform.smoothscale_by(game_options_menu_source, (FACTOR_X, FACTOR_Y))

    #------------------------------------------------------------------------------------------------------------------------------------ OPTIONS_MENU_FOLDER #
    ###########################################################################################################################################################


    ###########################################################################################################################################################
    #---------------------------------------------------------------------------------------------------------------------------------------- ESC_MENU_FOLDER #
    ESC_MENU_FOLDER                     = os.path.join(INTERFACE_FOLDER,      'ESC_MENU')

    esc_menu_background_source 		    = pygame.image.load(os.path.join(ESC_MENU_FOLDER, 'esc_menu_background.png')).convert_alpha()
    global esc_menu_background
    esc_menu_background 				= pygame.transform.smoothscale_by(esc_menu_background_source, (FACTOR_X, FACTOR_Y))

    #---------------------------------------------------------------------------------------------------------------------------------------- ESC_MENU_FOLDER #
    ###########################################################################################################################################################


    # -------------------------------------------------------------------- INTERFACE_FOLDER ------------------------------------------------------------------#
    ###########################################################################################################################################################
    

    ###########################################################################################################################################################
    # ---------------------------------------------------------------------- SOUNDS_FOLDER -------------------------------------------------------------------#
    SOUNDS_FOLDER = os.path.join(MAIN_FOLDER, 'Sounds')


    global generic_hover_over_button_sound
    generic_hover_over_button_sound 	= pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'generic_hover_over_button_sound.wav'))
    global generic_click_button_sound
    generic_click_button_sound 		    = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'generic_click_button_sound.wav'))

    # ---------------------------------------------------------------------- SOUNDS_FOLDER -------------------------------------------------------------------#
    ###########################################################################################################################################################

def create_classes():
    ###########################################################################################################################################################
    #------------------------------------------------------------------------------------------------------------------------------------------ SOUND MANAGER #
    import SoundManager

    global Sounds_Manager
    Sounds_Manager = SoundManager.Sound_Manager(generic_hover_over_button_sound, generic_click_button_sound)

    #------------------------------------------------------------------------------------------------------------------------------------------ SOUND MANAGER #
    ###########################################################################################################################################################


    ###########################################################################################################################################################
    #-------------------------------------------------------------------------------------------------------------------------------------------------- MENUS #
    import MenuManager

    global Main_Menu
    Main_Menu = MenuManager.Main_Menu(SCREEN_WIDTH, SCREEN_HEIGHT, game_logo, python_logo, main_menu_background, main_menu_UI,
        Sounds_Manager.generic_hover_over_button_sound, Sounds_Manager.generic_click_button_sound)

    global Options_Menu
    Options_Menu = MenuManager.Options_Menu(SCREEN_WIDTH, SCREEN_HEIGHT, game_options_menu, Sounds_Manager.generic_hover_over_button_sound,
        Sounds_Manager.generic_click_button_sound, Sounds_Manager, Main_Menu)
    
    global ESC_Menu
    ESC_Menu = MenuManager.ESC_Menu(SCREEN_WIDTH, SCREEN_HEIGHT, esc_menu_background, Sounds_Manager.generic_hover_over_button_sound,
        Sounds_Manager.generic_click_button_sound)
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------- MENUS #
    ###########################################################################################################################################################


    ###########################################################################################################################################################
    #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
    import ScreenManager

    global Screen_Manager
    Screen_Manager = ScreenManager.Screen(Main_Menu, ESC_Menu, Options_Menu, SCREEN_WIDTH, SCREEN_HEIGHT)
    #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
    ###########################################################################################################################################################

def set_variables():
    global screen_center
    screen_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()
    global mouse_rect
    mouse_rect = pygame.Rect(mouse_pos, (1, 1))

    global clicked_button
    clicked_button = None
    global hovered_button
    hovered_button = None

    global main_menu_music_started
    main_menu_music_started = False

    global RUNNING
    RUNNING = True 

    global is_options_menu_open
    is_options_menu_open = False

    global is_in_esc_menu
    is_in_esc_menu = False

    global is_in_main_menu_screen
    is_in_main_menu_screen = True

    global is_in_scenario_selection_screen
    is_in_scenario_selection_screen = False

    global is_in_country_selection_screen
    is_in_country_selection_screen = False

    global is_in_game_screen
    is_in_game_screen = False

    global to_draw
    to_draw = True

def game_utility_menu(mouse_rect):
    global is_options_menu_open
    global clicked_button

    ###########################################################################################################################################################
    #----------------------------------------------------------------------------------------------------------------------------------------------- ESC MENU #
    if is_in_esc_menu == True:
        clicked_button = ESC_Menu.get_clicked_button(mouse_rect)

    #----------------------------------------------------------------------------------------------------------------------------------------------- ESC MENU #
    ###########################################################################################################################################################
    

    ###########################################################################################################################################################
    #------------------------------------------------------------------------------------------------------------------------------------------- OPTIONS MENU #
    elif is_options_menu_open == True:
        clicked_button = Options_Menu.get_clicked_button(mouse_rect)

        if clicked_button == 'back':
            is_options_menu_open = False

        resolution_to_save = None
        if clicked_button == 'resolution_2560x1440':
            resolution_to_save = (2560,1440)
        elif clicked_button == 'resolution_1920x1080':
            resolution_to_save = (1920,1080)
        elif clicked_button == 'resolution_1600x900':
            resolution_to_save = (1600,900)
        elif clicked_button == 'resolution_1440x900':
            resolution_to_save = (1440,900)
        elif clicked_button == 'resolution_1280x1024':
            resolution_to_save = (1280,1024)

        if resolution_to_save != None:
            with open(f'{MAIN_FOLDER}\\settings.txt', 'r') as file:
                configs = json_load(file)

            configs["screen_width"], configs["screen_height"] = resolution_to_save

            with open(f'{MAIN_FOLDER}\\settings.txt', 'w') as file:
                json_dump(configs, file) 

    #------------------------------------------------------------------------------------------------------------------------------------------- OPTIONS MENU #
    ###########################################################################################################################################################

load_assets()
create_classes()
set_variables()
pygame.event.clear()

while RUNNING:

    ###############################################################################################################################################################
    #------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
    CLOCK.tick(60)
    PYGAME_EVENTS = pygame.event.get()
    
    if is_options_menu_open == True:
        hovered_button = Options_Menu.get_hovered_button(mouse_rect)
        Options_Menu.hovered_button = hovered_button
        Main_Menu.hovered_button = None
        for event in PYGAME_EVENTS:
            Options_Menu.interacting_with_UI_slides(event)            
    elif is_in_esc_menu == True:
        hovered_button = ESC_Menu.get_hovered_button(mouse_rect)
        ESC_Menu.hovered_button = hovered_button 
        Main_Menu.hovered_button = None  

    #------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
    ###############################################################################################################################################################
    

    ###############################################################################################################################################################
    #------------------------------------------------------------------------ MAIN MENU --------------------------------------------------------------------------#
    if is_in_main_menu_screen == True:
        
        ###########################################################################################################################################################
        #-------------------------------------------------------------------------------------------------------------------------------------------------- MUSIC #
        #if main_menu_music_started == False or pygame.mixer.music.get_busy() == False:
            #main_menu_music_started = True
            #pygame.mixer.music.load(music_files_dic['clock-ticking'])
            #pygame.mixer.music.play()

        #-------------------------------------------------------------------------------------------------------------------------------------------------- MUSIC #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        Screen_Manager.render_main_menu(Options_Menu.brightness_slider.value, is_options_menu_open, is_in_esc_menu)

        #---------------------------------------------------------------------------------------------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------ PYGAME EVENTS #
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_pos, (1, 1))					

        for event in PYGAME_EVENTS:
            if event.type == QUIT_EVENT:
                RUNNING = False

            #######################################################################################################################################################
            #------------------------------------------------------------------------------------------------------------------------------------------- KEYBOARD # 
            keys = pygame.key.get_pressed()	

            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE]:
                    is_in_esc_menu = not is_in_esc_menu
                    is_options_menu_open = False                						

            #------------------------------------------------------------------------------------------------------------------------------------------- KEYBOARD #
            #######################################################################################################################################################


            #######################################################################################################################################################
            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            if event.type == pygame.MOUSEBUTTONUP:	
                pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_options_menu_open == True or is_in_esc_menu == True:
                    game_utility_menu(mouse_rect)

                else:
                    clicked_button = Main_Menu.get_clicked_button(mouse_rect)
                    if clicked_button != 'none':
                        if Main_Menu.is_in_new_game_menu == False:
                            if clicked_button == 'start':
                                pygame.time.delay(50)
                                Main_Menu.is_in_new_game_menu = True
                                Main_Menu.main_menu_intro_video.toggle_pause()
                                Options_Menu.music_slider.value = 60
                                Options_Menu.music_slider.update()
                                pygame.mixer.music.set_volume(Options_Menu.music_slider.value/100)
                            elif clicked_button == 'quit':
                                RUNNING = False
                            elif clicked_button == 'options':
                                pygame.time.delay(50)
                                is_options_menu_open = True
                        else:
                            if clicked_button == 'new_game':
                                is_in_scenario_selection_screen = True
                                is_in_main_menu_screen = False
                                Main_Menu.is_in_new_game_menu = False
                            elif clicked_button == 'load_save':
                                Main_Menu.is_in_new_game_menu = False
                            elif clicked_button == 'back':		
                                Main_Menu.is_in_new_game_menu = False
                                Main_Menu.main_menu_intro_video.toggle_pause()
                                Options_Menu.music_slider.value = 10
                                Options_Menu.music_slider.update()
                                pygame.mixer.music.set_volume(Options_Menu.music_slider.value/100)                    

            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            #######################################################################################################################################################


        #------------------------------------------------------------------------------------------------------------------------------------------ PYGAME EVENTS #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        if is_options_menu_open == False and is_in_esc_menu == False:				
            hovered_button = Main_Menu.get_hovered_button(mouse_rect)
            Main_Menu.hovered_button = hovered_button

        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        ###########################################################################################################################################################


    #------------------------------------------------------------------------ MAIN MENU --------------------------------------------------------------------------#
    ###############################################################################################################################################################








pygame.quit()