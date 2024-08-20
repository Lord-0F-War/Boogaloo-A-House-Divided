
import sys
import os
from json import load as json_load
from PygameManager import pygame


MAIN_FOLDER = os.path.dirname(sys.argv[0])

with open(f'{MAIN_FOLDER}\_settings.txt', 'r') as file:
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


class GameLoader:
    def load_assets(self):
        GFX_FOLDER                          = os.path.join(MAIN_FOLDER,     'GFX')


        ###########################################################################################################################################################
        # -------------------------------------------------------------------- INTERFACE FOLDER ------------------------------------------------------------------#
        INTERFACE_FOLDER                    = os.path.join(GFX_FOLDER,      'INTERFACE')


        ###########################################################################################################################################################
        #--------------------------------------------------------------------------------------------------------------------------------------- MAIN MENU FOLDER #
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

        main_menu_UI_source 				= pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'main_menu_UI.png')).convert_alpha()
        global main_menu_UI
        main_menu_UI                        = pygame.transform.smoothscale_by(main_menu_UI_source, (FACTOR_X, FACTOR_Y))

        new_game_load_game_menu_UI_source 	= pygame.image.load(os.path.join(MAIN_MENU_FOLDER, 'new_game_load_game_menu_UI.png')).convert_alpha()
        global new_game_load_game_menu_UI
        new_game_load_game_menu_UI          = pygame.transform.smoothscale_by(new_game_load_game_menu_UI_source, (FACTOR_X, FACTOR_Y))        
        
        #--------------------------------------------------------------------------------------------------------------------------------------- MAIN MENU FOLDER #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #---------------------------------------------------------------------------------------------------------------------------------------- NEW GAME FOLDER # 
        NEW_GAME_MENU_FOLDER                = os.path.join(INTERFACE_FOLDER,      'NEW_GAME_MENU')

        new_game_menu_UI_source 	        = pygame.image.load(os.path.join(NEW_GAME_MENU_FOLDER, 'new_game_menu_UI.png')).convert_alpha()
        global new_game_menu_UI
        new_game_menu_UI                    = pygame.transform.smoothscale_by(new_game_menu_UI_source, (FACTOR_X, FACTOR_Y))

        character_creation_sheet_UI_source 	= pygame.image.load(os.path.join(NEW_GAME_MENU_FOLDER, 'character_creation_sheet.png')).convert_alpha()
        global character_creation_sheet_UI
        character_creation_sheet_UI         = pygame.transform.smoothscale_by(character_creation_sheet_UI_source, (FACTOR_X, FACTOR_Y))                 
        
        #---------------------------------------------------------------------------------------------------------------------------------------- NEW GAME FOLDER #
        ###########################################################################################################################################################                


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------ OPTIONS MENU FOLDER #
        OPTIONS_MENU_FOLDER                 = os.path.join(INTERFACE_FOLDER,      'OPTIONS_MENU')

        game_options_menu_source 			= pygame.image.load(os.path.join(OPTIONS_MENU_FOLDER, 'game_options_menu.png')).convert_alpha()
        global game_options_menu
        game_options_menu                   = pygame.transform.smoothscale_by(game_options_menu_source, (FACTOR_X, FACTOR_Y))

        #------------------------------------------------------------------------------------------------------------------------------------ OPTIONS MENU FOLDER #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #---------------------------------------------------------------------------------------------------------------------------------------- ESC MENU FOLDER #
        ESC_MENU_FOLDER                     = os.path.join(INTERFACE_FOLDER,      'ESC_MENU')

        esc_menu_background_source 		    = pygame.image.load(os.path.join(ESC_MENU_FOLDER, 'esc_menu_background.png')).convert_alpha()
        global esc_menu_background
        esc_menu_background 				= pygame.transform.smoothscale_by(esc_menu_background_source, (FACTOR_X, FACTOR_Y))

        #---------------------------------------------------------------------------------------------------------------------------------------- ESC MENU FOLDER #
        ###########################################################################################################################################################


        # -------------------------------------------------------------------- INTERFACE FOLDER ------------------------------------------------------------------#
        ###########################################################################################################################################################
        

        ###########################################################################################################################################################
        # ---------------------------------------------------------------------- SOUNDS FOLDER -------------------------------------------------------------------#
        SOUNDS_FOLDER = os.path.join(MAIN_FOLDER, 'SOUNDS')


        global generic_hover_over_button_sound
        generic_hover_over_button_sound 	= pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'generic_hover_over_button_sound.wav'))
        global generic_click_button_sound
        generic_click_button_sound 		    = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'generic_click_button_sound.wav'))

        # ---------------------------------------------------------------------- SOUNDS_FOLDER -------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        # ---------------------------------------------------------------------- MUSICS FOLDER -------------------------------------------------------------------#    
        global music_files_dic
        music_files_dic = self.load_music_files(os.path.join(MAIN_FOLDER, 'MUSICS'))

        # ---------------------------------------------------------------------- MUSICS FOLDER -------------------------------------------------------------------#
        ############################################################################################################################################################ 

    def load_music_files(self, musics_folder):
        music_files_dic:dict = {}

        for folder_name in os.listdir(musics_folder):
            folder_path = os.path.join(musics_folder, folder_name)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith(".wav") or filename.endswith(".ogg") or filename.endswith(".mp3"):
                        music_path = os.path.join(folder_path, filename)
                        image_name = os.path.splitext(filename)[0]
                        music_files_dic[image_name] = music_path
        
        return music_files_dic

    def set_variables(self):
        global RUNNING
        RUNNING = True 

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


        global is_options_menu_open
        is_options_menu_open = False
        global is_in_esc_menu
        is_in_esc_menu = False


        global is_in_main_menu_screen
        is_in_main_menu_screen = True
        
        global is_in_new_game_load_game_screen
        is_in_new_game_load_game_screen = False

        global is_in_new_game_screen
        is_in_new_game_screen = False        

    def create_classes(self):
        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------ SOUND MANAGER #
        import SoundManager

        global Sounds_Manager
        Sounds_Manager = SoundManager.Sound_Manager(generic_hover_over_button_sound, generic_click_button_sound)

        #------------------------------------------------------------------------------------------------------------------------------------------ SOUND MANAGER #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #-------------------------------------------------------------------------------------------------------------------------------------------------- MENUS #
        exec(open("MenuManager.py").read(), globals())


        global Main_Menu
        Main_Menu                               = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT, game_logo, python_logo, main_menu_background, main_menu_UI,                # type: ignore
                                                    Sounds_Manager.generic_hover_over_button_sound, Sounds_Manager.generic_click_button_sound)
        
        global New_Game_Load_Game_Menu
        New_Game_Load_Game_Menu                 = NewGameLoadGameMenu(SCREEN_WIDTH, SCREEN_HEIGHT, game_logo, python_logo, main_menu_background,                   # type: ignore
                                                    new_game_load_game_menu_UI, Sounds_Manager.generic_hover_over_button_sound,
                                                    Sounds_Manager.generic_click_button_sound)

        global New_Game_Menu
        New_Game_Menu                           = NewGameMenu(SCREEN_WIDTH, SCREEN_HEIGHT, new_game_menu_UI, character_creation_sheet_UI,                          # type: ignore
                                                            Sounds_Manager.generic_hover_over_button_sound,
                                                    Sounds_Manager.generic_click_button_sound)                   



        global Options_Menu
        Options_Menu                            = OptionsMenu(SCREEN_WIDTH, SCREEN_HEIGHT, game_options_menu, Sounds_Manager.generic_hover_over_button_sound,      # type: ignore
                                                    Sounds_Manager.generic_click_button_sound, Sounds_Manager, Main_Menu)
        
        global ESC_Menu
        ESC_Menu                                = ESCMenu(SCREEN_WIDTH, SCREEN_HEIGHT, esc_menu_background, Sounds_Manager.generic_hover_over_button_sound,        # type: ignore
                                                    Sounds_Manager.generic_click_button_sound)
        
        #-------------------------------------------------------------------------------------------------------------------------------------------------- MENUS #
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        import ScreenManager

        global Screen_Manager
        Screen_Manager = ScreenManager.Screen(SCREEN_WIDTH, SCREEN_HEIGHT, ESC_Menu, Options_Menu, Main_Menu, New_Game_Load_Game_Menu, New_Game_Menu)
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        ###########################################################################################################################################################

Loader = GameLoader()
Loader.load_assets()
Loader.set_variables()
Loader.create_classes()

pygame.event.clear()

while RUNNING:

    #------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
    CLOCK.tick(60)
    PYGAME_EVENTS = pygame.event.get()
    
    if is_options_menu_open == True:
        Options_Menu.hover_button(mouse_rect)
        Main_Menu.hovered_button = None
        
        for event in PYGAME_EVENTS:
            Options_Menu.interacting_with_UI_slides(event)            
    elif is_in_esc_menu == True:
        ESC_Menu.hover_button(mouse_rect) 
        Main_Menu.hovered_button = None  

    #------------------------------------------------------------------------------------------------------------------------------------------------------ MUSIC #
    if main_menu_music_started == False or pygame.mixer.music.get_busy() == False:
        main_menu_music_started = True
        pygame.mixer.music.load(music_files_dic['clock-ticking'])
        pygame.mixer.music.play()

    #------------------------------------------------------------------------------------------------------------------------------------------------------ MUSIC #        
    #------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#


    ###############################################################################################################################################################
    # MAIN MENU --------------------------------------------------------------------------------------------------------------------------------------------------#
    if is_in_main_menu_screen:
        
        ###########################################################################################################################################################
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        Screen_Manager.render_main_menu(Options_Menu.BRIGHTNESS_SLIDER.value, is_options_menu_open, is_in_esc_menu)

        #---------------------------------------------------------------------------------------------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
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
                if is_options_menu_open == True:
                    Options_Menu.click_button(mouse_rect)
                elif is_in_esc_menu == True:
                    ESC_Menu.click_button(mouse_rect)
                else:
                    Main_Menu.click_button(mouse_rect)

            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            #######################################################################################################################################################


        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        if is_options_menu_open == False and is_in_esc_menu == False:				
            Main_Menu.hover_button(mouse_rect)

        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        ###########################################################################################################################################################

    if is_in_new_game_load_game_screen:
        
        ###########################################################################################################################################################
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        Screen_Manager.render_new_game_load_game_menu(Options_Menu.BRIGHTNESS_SLIDER.value, is_options_menu_open, is_in_esc_menu)

        #---------------------------------------------------------------------------------------------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
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
                if is_options_menu_open == True:
                    Options_Menu.click_button(mouse_rect)
                elif is_in_esc_menu == True:
                    ESC_Menu.click_button(mouse_rect)
                else:
                    New_Game_Load_Game_Menu.click_button(mouse_rect)

            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            #######################################################################################################################################################


        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        if is_options_menu_open == False and is_in_esc_menu == False:				
            New_Game_Load_Game_Menu.hover_button(mouse_rect)

        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        ###########################################################################################################################################################

    # MAIN MENU --------------------------------------------------------------------------------------------------------------------------------------------------#
    ###############################################################################################################################################################


    ###############################################################################################################################################################
    # NEW GAME MENU ----------------------------------------------------------------------------------------------------------------------------------------------#
    if is_in_new_game_screen:
        
        ###########################################################################################################################################################
        #----------------------------------------------------------------------------------------------------------------------------------------- SCREEN MANAGER #
        Screen_Manager.render_new_game_menu(Options_Menu.BRIGHTNESS_SLIDER.value, is_options_menu_open, is_in_esc_menu)

        #---------------------------------------------------------------------------------------------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_pos, (1, 1))					

        for event in PYGAME_EVENTS:
            if event.type == QUIT_EVENT:
                RUNNING = False

            #######################################################################################################################################################
            #------------------------------------------------------------------------------------------------------------------------------------------- KEYBOARD # 
            keys = pygame.key.get_pressed()
            mods = pygame.key.get_mods()	

            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE]:
                    is_in_esc_menu = not is_in_esc_menu
                    is_options_menu_open = False
                
                if New_Game_Menu.receive_player_keybord_input == True:
                    key_name = pygame.key.name(event.key)

                    if len(New_Game_Menu.variable_to_receive_player_keybord_input['content']) < New_Game_Menu.variable_to_receive_player_keybord_input['maximum_size']:
                        #########################################################################################################
                        if New_Game_Menu.variable_to_receive_player_keybord_input['content_type'] == str:
                            if  len(key_name) == 1 and key_name.isalpha():
                                # Check if either shift key is pressed to determine uppercase
                                if mods & pygame.KMOD_SHIFT or mods & pygame.KMOD_CAPS:
                                    key_name = key_name.upper()                        
                                New_Game_Menu.variable_to_receive_player_keybord_input['content'] += key_name
                                
                        #########################################################################################################

                        #########################################################################################################
                        if New_Game_Menu.variable_to_receive_player_keybord_input['content_type'] == int:
                            if len(key_name) == 1 and key_name.isnumeric():
                                if New_Game_Menu.variable_to_receive_player_keybord_input['content'] == '0':
                                    New_Game_Menu.variable_to_receive_player_keybord_input['content'] = '' 

                                New_Game_Menu.variable_to_receive_player_keybord_input['content'] += key_name
                            elif key_name.startswith('[') and key_name.endswith(']'):
                                if New_Game_Menu.variable_to_receive_player_keybord_input['content'] == '0':
                                    New_Game_Menu.variable_to_receive_player_keybord_input['content'] = '' 

                                New_Game_Menu.variable_to_receive_player_keybord_input['content'] += key_name[1:-1]                                     

                        #########################################################################################################

                        #########################################################################################################
                        if keys[pygame.K_SPACE]:
                            New_Game_Menu.variable_to_receive_player_keybord_input['content'] += ' ' 

                        #########################################################################################################


                    if keys[pygame.K_BACKSPACE]:
                        New_Game_Menu.variable_to_receive_player_keybord_input['content'] = New_Game_Menu.variable_to_receive_player_keybord_input['content'][:-1]
                        if New_Game_Menu.variable_to_receive_player_keybord_input['content_type'] == int and len(New_Game_Menu.variable_to_receive_player_keybord_input['content']) == 0:
                            New_Game_Menu.variable_to_receive_player_keybord_input['content'] += '0'                                                                                                           

            #------------------------------------------------------------------------------------------------------------------------------------------- KEYBOARD #
            #######################################################################################################################################################


            #######################################################################################################################################################
            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            if event.type == pygame.MOUSEBUTTONUP and event.button < 4:	
                pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button < 4:
                if is_options_menu_open == True:
                    Options_Menu.click_button(mouse_rect)
                elif is_in_esc_menu == True:
                    ESC_Menu.click_button(mouse_rect)
                else:
                    New_Game_Menu.click_button(mouse_rect)
            
            elif event.type == pygame.MOUSEWHEEL:
                CHARACTER_CREATION_SHEET_RECT = pygame.Rect(
                                                            424 * New_Game_Menu.FACTOR_X,                                       # START X
                                                            14 * New_Game_Menu.FACTOR_Y,                                        # START Y
                                                            New_Game_Menu.CHARACTER_CREATION_SHEET_SURFACE.get_width() + 15,    # WIDTH
                                                            1000 * New_Game_Menu.FACTOR_Y                                       # HEIGHT
                                                            )
                
                if CHARACTER_CREATION_SHEET_RECT.colliderect(mouse_rect):
                    if event.y > 0:
                        New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position -= event.y * 30
                        if New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position < 0:
                            New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position = 0
                    elif event.y < 0:
                        New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position += abs(event.y) * 30
                        if New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position > New_Game_Menu.CHARACTER_CREATION_SHEET.get_height() - 1000 * New_Game_Menu.FACTOR_Y:
                            New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position = New_Game_Menu.CHARACTER_CREATION_SHEET.get_height() - 1000 * New_Game_Menu.FACTOR_Y

            #---------------------------------------------------------------------------------------------------------------------------------------------- MOUSE #
            #######################################################################################################################################################


        #--------------------------------------------------------------------- PYGAME EVENTS ---------------------------------------------------------------------#
        ###########################################################################################################################################################


        ###########################################################################################################################################################
        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        if is_options_menu_open == False and is_in_esc_menu == False:				
            New_Game_Menu.hover_button(mouse_rect)

            New_Game_Menu.CHARACTER_CREATION_SHEET_SCROLL_BAR.handle_event(PYGAME_EVENTS)

        #------------------------------------------------------------------------------------------------------------------------------------------- UPDATE CLASS #
        ###########################################################################################################################################################

    # NEW GAME MENU ----------------------------------------------------------------------------------------------------------------------------------------------#
    ###############################################################################################################################################################




pygame.quit()