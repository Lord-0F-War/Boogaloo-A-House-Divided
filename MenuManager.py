
import Utility
from PygameManager import pygame
from pyvidplayer import Video
from json import load as json_load, dump as json_dump


###############################################################################################################################################################
#---------------------------------------------------------------------- UTILITY MENUS ------------------------------------------------------------------------#
class ESCMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, esc_menu_background, generic_hover_over_button_sound, generic_click_menu_sound) -> None:

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= esc_menu_background.get_width()
		MENU_GUI_HEIGHT:int 				= esc_menu_background.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.hover_over_button_sound 		= generic_hover_over_button_sound
		self.click_menu_sound 				= generic_click_menu_sound
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.esc_menu_background 			= esc_menu_background

		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################	


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		OPTIONS_BUTTON_WIDTH 				= 371 * self.FACTOR_X
		OPTIONS_BUTTON_HEIGHT 				= 34 * self.FACTOR_Y
		OPTIONS_BUTTON_X_OFFSET 			= 59 * self.FACTOR_X
		OPTIONS_BUTTON_Y_OFFSET 			= 101 * self.FACTOR_Y
		self.OPTIONS_BUTTON 				= Utility.Button(self.MENU_GUI_MIDDLE_X + OPTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + OPTIONS_BUTTON_Y_OFFSET, OPTIONS_BUTTON_WIDTH, OPTIONS_BUTTON_HEIGHT)
		
		MAIN_MENU_BUTTON_WIDTH 				= 371 * self.FACTOR_X
		MAIN_MENU_BUTTON_HEIGHT 			= 34 * self.FACTOR_Y
		MAIN_MENU_BUTTON_X_OFFSET 			= 59 * self.FACTOR_X
		MAIN_MENU_BUTTON_Y_OFFSET 			= 420 * self.FACTOR_Y
		self.MAIN_MENU_BUTTON 				= Utility.Button(self.MENU_GUI_MIDDLE_X + MAIN_MENU_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + MAIN_MENU_BUTTON_Y_OFFSET, MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT)
		
		QUIT_BUTTON_WIDTH 					= 371 * self.FACTOR_X
		QUIT_BUTTON_HEIGHT 					= 34 * self.FACTOR_Y
		QUIT_BUTTON_X_OFFSET 				= 59 * self.FACTOR_X
		QUIT_BUTTON_Y_OFFSET 				= 465 * self.FACTOR_Y
		self.QUIT_BUTTON 					= Utility.Button(self.MENU_GUI_MIDDLE_X + QUIT_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + QUIT_BUTTON_Y_OFFSET, QUIT_BUTTON_WIDTH, QUIT_BUTTON_HEIGHT)						
		
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.OPTIONS_BUTTON.rect.colliderect(mouse_rect):
			return 'options'
		elif self.MAIN_MENU_BUTTON.rect.colliderect(mouse_rect):
			return 'main_menu'
		elif self.QUIT_BUTTON.rect.colliderect(mouse_rect):
			return 'quit'		
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			self.hover_over_button_sound.fadeout(150)
			self.click_menu_sound.play()
		return clicked_button

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.hover_over_button_sound.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, surface_alfa):
		surface_alfa.blit(self.esc_menu_background, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'options':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.OPTIONS_BUTTON.rect[0]-1, self.OPTIONS_BUTTON.rect[1]-1, self.OPTIONS_BUTTON.rect[2]+2, self.OPTIONS_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'main_menu':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.MAIN_MENU_BUTTON.rect[0]-1, self.MAIN_MENU_BUTTON.rect[1]-1, self.MAIN_MENU_BUTTON.rect[2]+2, self.MAIN_MENU_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'quit':
				pygame.draw.rect(surface_alfa, (255, 23, 23), (self.QUIT_BUTTON.rect[0]-1, self.QUIT_BUTTON.rect[1]-1, self.QUIT_BUTTON.rect[2]+2, self.QUIT_BUTTON.rect[3]+2), 4)			

class OptionsMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, options_menu_background, generic_hover_over_button_sound, generic_click_menu_sound, Sounds_Manager, Main_Menu) -> None:

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= options_menu_background.get_width()
		MENU_GUI_HEIGHT:int 				= options_menu_background.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.hover_over_button_sound 		= generic_hover_over_button_sound
		self.click_menu_sound 				= generic_click_menu_sound
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.options_menu_background 		= options_menu_background

		self.Sounds_Manager 				= Sounds_Manager
		self.Main_Menu 						= Main_Menu

		self.clicked_resolution_button 		= f'resolution_{SCREEN_WIDTH}x{SCREEN_HEIGHT}'

		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################			


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		back_button_width 					= 371 * self.FACTOR_X
		back_button_height 					= 34 * self.FACTOR_Y
		back_button_x_offset 				= 63 * self.FACTOR_X
		back_button_y_offset 				= 887 * self.FACTOR_Y
		self.back_button 					= Utility.Button(self.MENU_GUI_MIDDLE_X + back_button_x_offset, self.MENU_GUI_MIDDLE_Y + back_button_y_offset,
												back_button_width, back_button_height)	
		
		resolutions_button_width 			= 371 * self.FACTOR_X
		resolutions_button_height 			= 34 * self.FACTOR_Y
		resolutions_button_x_offset 		= 62 * self.FACTOR_X

		self.resolution_2560x1440_button 	= Utility.Button(self.MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.MENU_GUI_MIDDLE_Y + 100 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1920x1080_button 	= Utility.Button(self.MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.MENU_GUI_MIDDLE_Y + 145 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1600x900_button 	= Utility.Button(self.MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.MENU_GUI_MIDDLE_Y + 190 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1440x900_button 	= Utility.Button(self.MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.MENU_GUI_MIDDLE_Y + 235 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1280x1024_button 	= Utility.Button(self.MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.MENU_GUI_MIDDLE_Y + 280 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)										

		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#------------------------------------------------------------------------- SLIDERS ---------------------------------------------------------------------------#
		self.brightness_slider 				= Utility.Slide(self.MENU_GUI_MIDDLE_X + 457* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, 180, 0)
		
		self.music_slider 					= Utility.Slide(self.MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 10)
		self.sound_slider 					= Utility.Slide(self.MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 270* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 50)
		
		#------------------------------------------------------------------------- SLIDERS ---------------------------------------------------------------------------#
		###############################################################################################################################################################		

		
		###############################################################################################################################################################
		#-------------------------------------------------------------------------- SETERS ---------------------------------------------------------------------------#
		pygame.mixer.music.set_volume(self.music_slider.value/100)	
		self.Sounds_Manager.change_volume(self.sound_slider.value/100)
		self.Main_Menu.main_menu_intro_video.set_volume(self.sound_slider.value/100)

		#-------------------------------------------------------------------------- SETERS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.back_button.rect.colliderect(mouse_rect):
			return 'back'
		elif self.resolution_2560x1440_button.rect.colliderect(mouse_rect):
			return 'resolution_2560x1440'	
		elif self.resolution_1920x1080_button.rect.colliderect(mouse_rect):
			return 'resolution_1920x1080'
		elif self.resolution_1600x900_button.rect.colliderect(mouse_rect):
			return 'resolution_1600x900'
		elif self.resolution_1440x900_button.rect.colliderect(mouse_rect):
			return 'resolution_1440x900'
		elif self.resolution_1280x1024_button.rect.colliderect(mouse_rect):
			return 'resolution_1280x1024'
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		
		if clicked_button != None:
			if clicked_button == 'back':
				global is_options_menu_open
				is_options_menu_open = False

				self.hover_over_button_sound.fadeout(150)
				self.click_menu_sound.play()

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
				global MAIN_FOLDER
				with open(f'{MAIN_FOLDER}\_settings.txt', 'r') as file:
					configs = json_load(file)

				configs["screen_width"], configs["screen_height"] = resolution_to_save

				with open(f'{MAIN_FOLDER}\_settings.txt', 'w') as file:
					json_dump(configs, file)				
				
				self.clicked_resolution_button = clicked_button
		
		return clicked_button

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.hover_over_button_sound.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def interacting_with_UI_slides(self, key_event):
		self.brightness_slider.dragging_slide(key_event)
		self.music_slider.dragging_slide(key_event)
		self.sound_slider.dragging_slide(key_event)		

		self.brightness_slider.update()
		self.music_slider.update()
		self.sound_slider.update()

		self.Main_Menu.main_menu_intro_video.set_volume(self.sound_slider.value/100)

		pygame.mixer.music.set_volume(self.music_slider.value/100)
		self.Sounds_Manager.change_volume(self.sound_slider.value/100)

	def draw(self, surface_alfa):
		surface_alfa.blit(self.options_menu_background, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		self.brightness_slider.draw(surface_alfa)
		self.music_slider.draw(surface_alfa)
		self.sound_slider.draw(surface_alfa)

		if self.hovered_button != None:
			if self.hovered_button == 'back':
				pygame.draw.rect(surface_alfa, (255, 23, 23), (self.back_button.rect[0]-1, self.back_button.rect[1]-1, self.back_button.rect[2]+2, self.back_button.rect[3]+2), 4)			

			elif self.hovered_button == 'resolution_2560x1440':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_2560x1440_button.rect[0]-1, self.resolution_2560x1440_button.rect[1]-1, self.resolution_2560x1440_button.rect[2]+2, self.resolution_2560x1440_button.rect[3]+2), 4)	
			elif self.hovered_button == 'resolution_1920x1080':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1920x1080_button.rect[0]-1, self.resolution_1920x1080_button.rect[1]-1, self.resolution_1920x1080_button.rect[2]+2, self.resolution_1920x1080_button.rect[3]+2), 4)	
			elif self.hovered_button == 'resolution_1600x900':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1600x900_button.rect[0]-1, self.resolution_1600x900_button.rect[1]-1, self.resolution_1600x900_button.rect[2]+2, self.resolution_1600x900_button.rect[3]+2), 4)
			elif self.hovered_button == 'resolution_1440x900':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1440x900_button.rect[0]-1, self.resolution_1440x900_button.rect[1]-1, self.resolution_1440x900_button.rect[2]+2, self.resolution_1440x900_button.rect[3]+2), 4)
			elif self.hovered_button == 'resolution_1280x1024':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1280x1024_button.rect[0]-1, self.resolution_1280x1024_button.rect[1]-1, self.resolution_1280x1024_button.rect[2]+2, self.resolution_1280x1024_button.rect[3]+2), 4)

		if self.clicked_resolution_button == 'resolution_2560x1440':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_2560x1440_button.rect[0]-1, self.resolution_2560x1440_button.rect[1]-1, self.resolution_2560x1440_button.rect[2]+2, self.resolution_2560x1440_button.rect[3]+2), 4)	
		elif self.clicked_resolution_button == 'resolution_1920x1080':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1920x1080_button.rect[0]-1, self.resolution_1920x1080_button.rect[1]-1, self.resolution_1920x1080_button.rect[2]+2, self.resolution_1920x1080_button.rect[3]+2), 4)	
		elif self.clicked_resolution_button == 'resolution_1600x900':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1600x900_button.rect[0]-1, self.resolution_1600x900_button.rect[1]-1, self.resolution_1600x900_button.rect[2]+2, self.resolution_1600x900_button.rect[3]+2), 4)		
		elif self.clicked_resolution_button == 'resolution_1440x900':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1440x900_button.rect[0]-1, self.resolution_1440x900_button.rect[1]-1, self.resolution_1440x900_button.rect[2]+2, self.resolution_1440x900_button.rect[3]+2), 4)		
		elif self.clicked_resolution_button == 'resolution_1280x1024':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.resolution_1280x1024_button.rect[0]-1, self.resolution_1280x1024_button.rect[1]-1, self.resolution_1280x1024_button.rect[2]+2, self.resolution_1280x1024_button.rect[3]+2), 4)		

#---------------------------------------------------------------------- UTILITY MENUS ------------------------------------------------------------------------#
###############################################################################################################################################################


###############################################################################################################################################################
#------------------------------------------------------------------------ MAIN MENU---------------------------------------------------------------------------#
class MainMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, game_logo, python_logo, main_menu_backgound, menu_gui, hover_over_button_sound, click_menu_sound
		):

		self.hovered_button = None
		self.last_hovered_button =None

		self.hover_over_button_sound = hover_over_button_sound
		self.click_menu_sound = click_menu_sound

		
		self.SCREEN_WIDTH = SCREEN_WIDTH
		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		reference_SCREEN_size_x = 1920
		reference_SCREEN_size_y = 1080
		self.FACTOR_X = SCREEN_WIDTH / reference_SCREEN_size_x
		self.FACTOR_Y = SCREEN_HEIGHT / reference_SCREEN_size_y

		self.factor = self.FACTOR_X * self.FACTOR_Y

		self.main_menu_backgound = main_menu_backgound
		self.python_logo = python_logo
		self.game_logo = game_logo
		self.menu_gui = menu_gui

		
		MENU_GUI_WIDTH = self.menu_gui.get_width()
		MENU_GUI_HEIGHT = self.menu_gui.get_height()
		
		self.MENU_GUI_MIDDLE_X = (SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y = (SCREEN_HEIGHT/1.35 - MENU_GUI_HEIGHT/2)	

		
		start_button_width = 371 * self.FACTOR_X
		start_button_height = 34 * self.FACTOR_Y
		start_button_x_offset = 49 * self.FACTOR_X
		start_button_y_offset = 459 * self.FACTOR_Y
		self.start_button = Utility.Button(self.MENU_GUI_MIDDLE_X + start_button_x_offset, self.MENU_GUI_MIDDLE_Y + start_button_y_offset, start_button_width, start_button_height)	

		QUIT_BUTTON_WIDTH = 371 * self.FACTOR_X
		QUIT_BUTTON_HEIGHT = 34 * self.FACTOR_Y
		QUIT_BUTTON_X_OFFSET = 516 * self.FACTOR_X
		QUIT_BUTTON_Y_OFFSET = 459 * self.FACTOR_Y
		self.QUIT_BUTTON = Utility.Button(self.MENU_GUI_MIDDLE_X + QUIT_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + QUIT_BUTTON_Y_OFFSET, QUIT_BUTTON_WIDTH, QUIT_BUTTON_HEIGHT)	

		OPTIONS_BUTTON_WIDTH = 371 * self.FACTOR_X
		OPTIONS_BUTTON_HEIGHT = 34 * self.FACTOR_Y
		OPTIONS_BUTTON_X_OFFSET = 516 * self.FACTOR_X
		OPTIONS_BUTTON_Y_OFFSET = 403 * self.FACTOR_Y
		self.OPTIONS_BUTTON = Utility.Button(self.MENU_GUI_MIDDLE_X + OPTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + OPTIONS_BUTTON_Y_OFFSET, OPTIONS_BUTTON_WIDTH, OPTIONS_BUTTON_HEIGHT)


		self.main_menu_intro_video = Video("game_intro.mp4", size=(936 * self.FACTOR_X, 378 * self.FACTOR_Y))
		self.main_menu_intro_video.set_volume(0)

	def get_button_by_interaction(self, mouse_rect):
		if self.start_button.rect.colliderect(mouse_rect):
			return 'start'
		elif self.OPTIONS_BUTTON.rect.colliderect(mouse_rect):
			return 'options'
		elif self.QUIT_BUTTON.rect.colliderect(mouse_rect):
			return 'quit'	
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			if clicked_button == 'start':
				self.main_menu_intro_video.toggle_pause()

				global Options_Menu
				Options_Menu.music_slider.value = 60
				Options_Menu.music_slider.update()
				pygame.mixer.music.set_volume(Options_Menu.music_slider.value/100)

				global is_in_main_menu_screen
				is_in_main_menu_screen = False

				self.hover_over_button_sound.fadeout(150)
				self.click_menu_sound.play()
			elif clicked_button == 'options':
				self.hover_over_button_sound.fadeout(150)
				self.click_menu_sound.play()

				global is_options_menu_open
				is_options_menu_open = True
			elif clicked_button == 'quit':		
				self.hover_over_button_sound.fadeout(150)
				self.click_menu_sound.play()
				
				global RUNNING
				RUNNING = False								

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.hover_over_button_sound.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, SCREEN):
		SCREEN.blit(self.main_menu_backgound, (0, 0))

		SCREEN.blit(self.python_logo, (0, self.SCREEN_HEIGHT - self.python_logo.get_height()))

		SCREEN.blit(self.game_logo, (60 * self.FACTOR_X, 20 * self.FACTOR_Y))	
		
		self.main_menu_intro_video.draw(SCREEN, (self.MENU_GUI_MIDDLE_X + 2 * self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 2 * self.FACTOR_Y))

		if self.main_menu_intro_video.frames >= 608:
			self.main_menu_intro_video.restart()	

		SCREEN.blit(self.menu_gui, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'start':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.start_button.rect[0]-1, self.start_button.rect[1]-1, self.start_button.rect[2]+2, self.start_button.rect[3]+2), 4)
			elif self.hovered_button == 'quit':
				pygame.draw.rect(SCREEN, (255, 23, 23), (self.QUIT_BUTTON.rect[0]-1, self.QUIT_BUTTON.rect[1]-1, self.QUIT_BUTTON.rect[2]+2, self.QUIT_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'options':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.OPTIONS_BUTTON.rect[0]-1, self.OPTIONS_BUTTON.rect[1]-1, self.OPTIONS_BUTTON.rect[2]+2, self.OPTIONS_BUTTON.rect[3]+2), 4)
		else:
			self.hover_over_button_sound.fadeout(200)

#------------------------------------------------------------------------ MAIN MENU---------------------------------------------------------------------------#
###############################################################################################################################################################