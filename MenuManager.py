
import Utility
from PygameManager import pygame
from pyvidplayer import Video
from json import load as json_load, dump as json_dump

import traceback


###############################################################################################################################################################
#---------------------------------------------------------------------- UTILITY MENUS ------------------------------------------------------------------------#
class ESCMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, ESC_MENU_BACKGROUND, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND) -> None:

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= ESC_MENU_BACKGROUND.get_width()
		MENU_GUI_HEIGHT:int 				= ESC_MENU_BACKGROUND.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.HOVER_OVER_BUTTON_SOUND 		= HOVER_OVER_BUTTON_SOUND
		self.CLICK_BUTTON_SOUND 			= CLICK_BUTTON_SOUND
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.ESC_MENU_BACKGROUND 			= ESC_MENU_BACKGROUND

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
			global is_in_esc_menu
			global is_options_menu_open
			global is_in_main_menu_screen
			global is_in_new_game_load_game_screen
			global is_in_new_game_screen
			global RUNNING
			global Main_Menu
			global Options_Menu			

			if clicked_button == 'options':
				is_in_esc_menu = False	

				is_options_menu_open = True

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'main_menu' and is_in_main_menu_screen == False:
				is_in_esc_menu = False

				is_in_main_menu_screen = True

				is_in_new_game_load_game_screen = False

				is_in_new_game_screen = False

				Main_Menu.main_menu_intro_video.toggle_pause()

				Options_Menu.MUSIC_SLIDER.value = 0
				Options_Menu.MUSIC_SLIDER.update()
				pygame.mixer.music.set_volume(Options_Menu.MUSIC_SLIDER.value/100)				

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'quit':
				RUNNING = False	
				
				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()								
		return clicked_button

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, surface_alfa):
		surface_alfa.blit(self.ESC_MENU_BACKGROUND, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'options':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.OPTIONS_BUTTON.rect[0]-1, self.OPTIONS_BUTTON.rect[1]-1, self.OPTIONS_BUTTON.rect[2]+2, self.OPTIONS_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'main_menu':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.MAIN_MENU_BUTTON.rect[0]-1, self.MAIN_MENU_BUTTON.rect[1]-1, self.MAIN_MENU_BUTTON.rect[2]+2, self.MAIN_MENU_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'quit':
				pygame.draw.rect(surface_alfa, (255, 23, 23), (self.QUIT_BUTTON.rect[0]-1, self.QUIT_BUTTON.rect[1]-1, self.QUIT_BUTTON.rect[2]+2, self.QUIT_BUTTON.rect[3]+2), 4)			

class OptionsMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, OPTIONS_MENU_BACKGROUND, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND, Sounds_Manager, Main_Menu) -> None:

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= OPTIONS_MENU_BACKGROUND.get_width()
		MENU_GUI_HEIGHT:int 				= OPTIONS_MENU_BACKGROUND.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.HOVER_OVER_BUTTON_SOUND 		= HOVER_OVER_BUTTON_SOUND
		self.CLICK_BUTTON_SOUND 			= CLICK_BUTTON_SOUND
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.OPTIONS_MENU_BACKGROUND 		= OPTIONS_MENU_BACKGROUND

		self.Sounds_Manager 				= Sounds_Manager
		self.Main_Menu 						= Main_Menu

		self.clicked_resolution_button 		= f'resolution_{SCREEN_WIDTH}x{SCREEN_HEIGHT}'

		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################			


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		BACK_BUTTON_WIDTH 					= 371 * self.FACTOR_X
		BACK_BUTTON_HEIGHT 					= 34 * self.FACTOR_Y
		BACK_BUTTON_X_OFFSET 				= 63 * self.FACTOR_X
		BACK_BUTTON_Y_OFFSET 				= 887 * self.FACTOR_Y
		self.BACK_BUTTON 					= Utility.Button(self.MENU_GUI_MIDDLE_X + BACK_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + BACK_BUTTON_Y_OFFSET,
												BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)	
		

		RESOLUTIONS_BUTTON_WIDTH 			= 371 * self.FACTOR_X
		RESOLUTIONS_BUTTON_HEIGHT 			= 34 * self.FACTOR_Y
		RESOLUTIONS_BUTTON_X_OFFSET 		= 62 * self.FACTOR_X

		self.RESOLUTION_2560x1440_BUTTON 	= Utility.Button(self.MENU_GUI_MIDDLE_X + RESOLUTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + 100 * self.FACTOR_Y,
												RESOLUTIONS_BUTTON_WIDTH, RESOLUTIONS_BUTTON_HEIGHT)	
		self.RESOLUTION_1920x1080_BUTTON 	= Utility.Button(self.MENU_GUI_MIDDLE_X + RESOLUTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + 145 * self.FACTOR_Y,
												RESOLUTIONS_BUTTON_WIDTH, RESOLUTIONS_BUTTON_HEIGHT)	
		self.RESOLUTION_1600x900_BUTTON 	= Utility.Button(self.MENU_GUI_MIDDLE_X + RESOLUTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + 190 * self.FACTOR_Y,
												RESOLUTIONS_BUTTON_WIDTH, RESOLUTIONS_BUTTON_HEIGHT)	
		self.RESOLUTION_1440x900_BUTTON 	= Utility.Button(self.MENU_GUI_MIDDLE_X + RESOLUTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + 235 * self.FACTOR_Y,
												RESOLUTIONS_BUTTON_WIDTH, RESOLUTIONS_BUTTON_HEIGHT)	
		self.RESOLUTION_1280x1024_BUTTON 	= Utility.Button(self.MENU_GUI_MIDDLE_X + RESOLUTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + 280 * self.FACTOR_Y,
												RESOLUTIONS_BUTTON_WIDTH, RESOLUTIONS_BUTTON_HEIGHT)										

		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#------------------------------------------------------------------------- SLIDERS ---------------------------------------------------------------------------#
		self.BRIGHTNESS_SLIDER 				= Utility.Slide(self.MENU_GUI_MIDDLE_X + 457* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, 180, 0)
		
		self.MUSIC_SLIDER 					= Utility.Slide(self.MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 0)
		self.SOUND_SLIDER 					= Utility.Slide(self.MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 270* self.FACTOR_Y,
												374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 40)
		
		#------------------------------------------------------------------------- SLIDERS ---------------------------------------------------------------------------#
		###############################################################################################################################################################		

		
		###############################################################################################################################################################
		#-------------------------------------------------------------------------- SETERS ---------------------------------------------------------------------------#
		pygame.mixer.music.set_volume(self.MUSIC_SLIDER.value/100)	
		self.Sounds_Manager.change_volume(self.SOUND_SLIDER.value/100)
		self.Main_Menu.main_menu_intro_video.set_volume(self.SOUND_SLIDER.value/100)

		#-------------------------------------------------------------------------- SETERS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.BACK_BUTTON.rect.colliderect(mouse_rect):
			return 'back'
		elif self.RESOLUTION_2560x1440_BUTTON.rect.colliderect(mouse_rect):
			return 'resolution_2560x1440'	
		elif self.RESOLUTION_1920x1080_BUTTON.rect.colliderect(mouse_rect):
			return 'resolution_1920x1080'
		elif self.RESOLUTION_1600x900_BUTTON.rect.colliderect(mouse_rect):
			return 'resolution_1600x900'
		elif self.RESOLUTION_1440x900_BUTTON.rect.colliderect(mouse_rect):
			return 'resolution_1440x900'
		elif self.RESOLUTION_1280x1024_BUTTON.rect.colliderect(mouse_rect):
			return 'resolution_1280x1024'
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		
		if clicked_button != None:
			global is_options_menu_open
			global MAIN_FOLDER			

			if clicked_button == 'back':
				is_options_menu_open = False

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()

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
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def interacting_with_UI_slides(self, key_event):
		self.BRIGHTNESS_SLIDER.dragging_slide(key_event)
		self.MUSIC_SLIDER.dragging_slide(key_event)
		self.SOUND_SLIDER.dragging_slide(key_event)		

		self.BRIGHTNESS_SLIDER.update()
		self.MUSIC_SLIDER.update()
		self.SOUND_SLIDER.update()

		self.Main_Menu.main_menu_intro_video.set_volume(self.SOUND_SLIDER.value/100)

		pygame.mixer.music.set_volume(self.MUSIC_SLIDER.value/100)
		self.Sounds_Manager.change_volume(self.SOUND_SLIDER.value/100)

	def draw(self, surface_alfa):
		surface_alfa.blit(self.OPTIONS_MENU_BACKGROUND, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		self.BRIGHTNESS_SLIDER.draw(surface_alfa)
		self.MUSIC_SLIDER.draw(surface_alfa)
		self.SOUND_SLIDER.draw(surface_alfa)

		if self.hovered_button != None:
			if self.hovered_button == 'back':
				pygame.draw.rect(surface_alfa, (255, 23, 23), (self.BACK_BUTTON.rect[0]-1, self.BACK_BUTTON.rect[1]-1, self.BACK_BUTTON.rect[2]+2,
																self.BACK_BUTTON.rect[3]+2), 4)			

			elif self.hovered_button == 'resolution_2560x1440':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_2560x1440_BUTTON.rect[0]-1, self.RESOLUTION_2560x1440_BUTTON.rect[1]-1,
																self.RESOLUTION_2560x1440_BUTTON.rect[2]+2, self.RESOLUTION_2560x1440_BUTTON.rect[3]+2), 4)	
			elif self.hovered_button == 'resolution_1920x1080':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1920x1080_BUTTON.rect[0]-1, self.RESOLUTION_1920x1080_BUTTON.rect[1]-1,
																self.RESOLUTION_1920x1080_BUTTON.rect[2]+2, self.RESOLUTION_1920x1080_BUTTON.rect[3]+2), 4)	
			elif self.hovered_button == 'resolution_1600x900':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1600x900_BUTTON.rect[0]-1, self.RESOLUTION_1600x900_BUTTON.rect[1]-1,
																self.RESOLUTION_1600x900_BUTTON.rect[2]+2, self.RESOLUTION_1600x900_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'resolution_1440x900':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1440x900_BUTTON.rect[0]-1, self.RESOLUTION_1440x900_BUTTON.rect[1]-1,
																self.RESOLUTION_1440x900_BUTTON.rect[2]+2, self.RESOLUTION_1440x900_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'resolution_1280x1024':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1280x1024_BUTTON.rect[0]-1, self.RESOLUTION_1280x1024_BUTTON.rect[1]-1,
																self.RESOLUTION_1280x1024_BUTTON.rect[2]+2, self.RESOLUTION_1280x1024_BUTTON.rect[3]+2), 4)

		if self.clicked_resolution_button == 'resolution_2560x1440':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_2560x1440_BUTTON.rect[0]-1, self.RESOLUTION_2560x1440_BUTTON.rect[1]-1,
																self.RESOLUTION_2560x1440_BUTTON.rect[2]+2, self.RESOLUTION_2560x1440_BUTTON.rect[3]+2), 4)	
		elif self.clicked_resolution_button == 'resolution_1920x1080':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1920x1080_BUTTON.rect[0]-1, self.RESOLUTION_1920x1080_BUTTON.rect[1]-1,
																self.RESOLUTION_1920x1080_BUTTON.rect[2]+2, self.RESOLUTION_1920x1080_BUTTON.rect[3]+2), 4)	
		elif self.clicked_resolution_button == 'resolution_1600x900':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1600x900_BUTTON.rect[0]-1, self.RESOLUTION_1600x900_BUTTON.rect[1]-1,
																self.RESOLUTION_1600x900_BUTTON.rect[2]+2, self.RESOLUTION_1600x900_BUTTON.rect[3]+2), 4)		
		elif self.clicked_resolution_button == 'resolution_1440x900':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1440x900_BUTTON.rect[0]-1, self.RESOLUTION_1440x900_BUTTON.rect[1]-1,
																self.RESOLUTION_1440x900_BUTTON.rect[2]+2, self.RESOLUTION_1440x900_BUTTON.rect[3]+2), 4)		
		elif self.clicked_resolution_button == 'resolution_1280x1024':
			pygame.draw.rect(surface_alfa, (23, 255, 23), (self.RESOLUTION_1280x1024_BUTTON.rect[0]-1, self.RESOLUTION_1280x1024_BUTTON.rect[1]-1,
																self.RESOLUTION_1280x1024_BUTTON.rect[2]+2, self.RESOLUTION_1280x1024_BUTTON.rect[3]+2), 4)		

#---------------------------------------------------------------------- UTILITY MENUS ------------------------------------------------------------------------#
###############################################################################################################################################################


###############################################################################################################################################################
#------------------------------------------------------------------------ MAIN MENU---------------------------------------------------------------------------#
class MainMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LOGO, PYTHON_LOGO, MAIN_MENU_BACKGROUND, MENU_GUI, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND):

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= MENU_GUI.get_width()
		MENU_GUI_HEIGHT:int 				= MENU_GUI.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/5)			

		self.HOVER_OVER_BUTTON_SOUND 		= HOVER_OVER_BUTTON_SOUND
		self.CLICK_BUTTON_SOUND 			= CLICK_BUTTON_SOUND
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.MAIN_MENU_BACKGROUND 			= MAIN_MENU_BACKGROUND
		self.MENU_GUI 						= MENU_GUI
		self.GAME_LOGO 						= GAME_LOGO
		self.PYTHON_LOGO 					= PYTHON_LOGO

		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################	


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		START_BUTTON_WIDTH 					= 371 * self.FACTOR_X
		START_BUTTON_HEIGHT 				= 34 * self.FACTOR_Y
		START_BUTTON_X_OFFSET 				= 49 * self.FACTOR_X
		START_BUTTON_Y_OFFSET 				= 459 * self.FACTOR_Y
		self.START_BUTTON 					= Utility.Button(self.MENU_GUI_MIDDLE_X + START_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + START_BUTTON_Y_OFFSET,
												START_BUTTON_WIDTH, START_BUTTON_HEIGHT)	

		QUIT_BUTTON_WIDTH 					= 371 * self.FACTOR_X
		QUIT_BUTTON_HEIGHT 					= 34 * self.FACTOR_Y
		QUIT_BUTTON_X_OFFSET 				= 516 * self.FACTOR_X
		QUIT_BUTTON_Y_OFFSET 				= 459 * self.FACTOR_Y
		self.QUIT_BUTTON 					= Utility.Button(self.MENU_GUI_MIDDLE_X + QUIT_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + QUIT_BUTTON_Y_OFFSET,
												QUIT_BUTTON_WIDTH, QUIT_BUTTON_HEIGHT)	

		OPTIONS_BUTTON_WIDTH 				= 371 * self.FACTOR_X
		OPTIONS_BUTTON_HEIGHT 				= 34 * self.FACTOR_Y
		OPTIONS_BUTTON_X_OFFSET 			= 516 * self.FACTOR_X
		OPTIONS_BUTTON_Y_OFFSET 			= 403 * self.FACTOR_Y
		self.OPTIONS_BUTTON 				= Utility.Button(self.MENU_GUI_MIDDLE_X + OPTIONS_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + OPTIONS_BUTTON_Y_OFFSET,
												OPTIONS_BUTTON_WIDTH, OPTIONS_BUTTON_HEIGHT)				
		
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#----------------------------------------------------------------------- VIDEO INTRO -------------------------------------------------------------------------#
		self.main_menu_intro_video = Video("game_intro.mp4", size=(936 * self.FACTOR_X, 378 * self.FACTOR_Y))
		self.main_menu_intro_video.set_volume(0)

		#----------------------------------------------------------------------- VIDEO INTRO -------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.START_BUTTON.rect.colliderect(mouse_rect):
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
			global Options_Menu
			global is_in_main_menu_screen
			global is_in_new_game_load_game_screen
			global is_options_menu_open	
			global RUNNING			

			if clicked_button == 'start':
				self.main_menu_intro_video.toggle_pause()

				Options_Menu.MUSIC_SLIDER.value = 60
				Options_Menu.MUSIC_SLIDER.update()
				pygame.mixer.music.set_volume(Options_Menu.MUSIC_SLIDER.value/100)

				is_in_main_menu_screen = False

				is_in_new_game_load_game_screen = True

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'options':
				is_options_menu_open = True	

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'quit':	
				RUNNING = False	

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, SCREEN):
		SCREEN.blit(self.MAIN_MENU_BACKGROUND, (0, 0))

		SCREEN.blit(self.PYTHON_LOGO, (0, self.SCREEN_HEIGHT - self.PYTHON_LOGO.get_height()))

		SCREEN.blit(self.GAME_LOGO, (60 * self.FACTOR_X, 20 * self.FACTOR_Y))	
		
		self.main_menu_intro_video.draw(SCREEN, (self.MENU_GUI_MIDDLE_X + 2 * self.FACTOR_X, self.MENU_GUI_MIDDLE_Y + 2 * self.FACTOR_Y))

		if self.main_menu_intro_video.frames >= 608:
			self.main_menu_intro_video.restart()	

		SCREEN.blit(self.MENU_GUI, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'start':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.START_BUTTON.rect[0]-1, self.START_BUTTON.rect[1]-1, self.START_BUTTON.rect[2]+2,
															self.START_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'quit':
				pygame.draw.rect(SCREEN, (255, 23, 23), (self.QUIT_BUTTON.rect[0]-1, self.QUIT_BUTTON.rect[1]-1, self.QUIT_BUTTON.rect[2]+2,
															self.QUIT_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'options':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.OPTIONS_BUTTON.rect[0]-1, self.OPTIONS_BUTTON.rect[1]-1, self.OPTIONS_BUTTON.rect[2]+2,
															self.OPTIONS_BUTTON.rect[3]+2), 4)
		else:
			self.HOVER_OVER_BUTTON_SOUND.fadeout(200)

class NewGameLoadGameMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LOGO, PYTHON_LOGO, MAIN_MENU_BACKGROUND, MENU_GUI, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND):

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= MENU_GUI.get_width()
		MENU_GUI_HEIGHT:int 				= MENU_GUI.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.HOVER_OVER_BUTTON_SOUND 		= HOVER_OVER_BUTTON_SOUND
		self.CLICK_BUTTON_SOUND 			= CLICK_BUTTON_SOUND
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.MAIN_MENU_BACKGROUND 			= MAIN_MENU_BACKGROUND

		self.MENU_GUI 						= MENU_GUI

		self.GAME_LOGO 						= GAME_LOGO

		self.PYTHON_LOGO 					= PYTHON_LOGO

		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################	


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		NEW_GAME_BUTTON_WIDTH 				= 371 * self.FACTOR_X
		NEW_GAME_BUTON_HEIGHT 				= 34 * self.FACTOR_Y
		NEW_GAME_BUTON_X_OFFSET 			= 59 * self.FACTOR_X
		NEW_GAME_BUTON_Y_OFFSET 			= 28 * self.FACTOR_Y
		self.NEW_GAME_BUTON 				= Utility.Button(self.MENU_GUI_MIDDLE_X + NEW_GAME_BUTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + NEW_GAME_BUTON_Y_OFFSET,
												NEW_GAME_BUTTON_WIDTH, NEW_GAME_BUTON_HEIGHT)

		LOAD_GAME_BUTTON_WIDTH 				= 371 * self.FACTOR_X
		LOAD_SAVE_BUTON_HEIGHT 				= 34 * self.FACTOR_Y
		LOAD_SAVE_BUTON_X_OFFSET 			= 59 * self.FACTOR_X
		LOAD_SAVE_BUTON_Y_OFFSET 			= 79 * self.FACTOR_Y
		self.LOAD_SAVE_BUTTON 				= Utility.Button(self.MENU_GUI_MIDDLE_X + LOAD_SAVE_BUTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + LOAD_SAVE_BUTON_Y_OFFSET,
												LOAD_GAME_BUTTON_WIDTH, LOAD_SAVE_BUTON_HEIGHT)

		BACK_BUTTON_WIDTH 					= 371 * self.FACTOR_X
		BACK_BUTTON_HEIGHT 					= 34 * self.FACTOR_Y
		BACK_BUTTON_X_OFFSET 				= 59 * self.FACTOR_X
		BACK_BUTTON_Y_OFFSET 				= 162 * self.FACTOR_Y
		self.BACK_BUTTON 					= Utility.Button(self.MENU_GUI_MIDDLE_X + BACK_BUTTON_X_OFFSET, self.MENU_GUI_MIDDLE_Y + BACK_BUTTON_Y_OFFSET,
												BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)						
		
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.NEW_GAME_BUTON.rect.colliderect(mouse_rect):
			return 'new_game'
		elif self.LOAD_SAVE_BUTTON.rect.colliderect(mouse_rect):
			return 'load_save'
		elif self.BACK_BUTTON.rect.colliderect(mouse_rect):
			return 'back'	
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			global Main_Menu
			global Options_Menu
			global is_in_main_menu_screen
			global is_in_new_game_load_game_screen
			global is_in_new_game_screen

			if clicked_button == 'new_game':
				is_in_new_game_screen = True
				is_in_new_game_load_game_screen = False

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'load_save':
				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'back':
				Main_Menu.main_menu_intro_video.toggle_pause()

				Options_Menu.MUSIC_SLIDER.value = 0
				Options_Menu.MUSIC_SLIDER.update()
				pygame.mixer.music.set_volume(Options_Menu.MUSIC_SLIDER.value/100)

				is_in_main_menu_screen = True

				is_in_new_game_load_game_screen = False

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, SCREEN):
		SCREEN.blit(self.MAIN_MENU_BACKGROUND, (0, 0))

		SCREEN.blit(self.PYTHON_LOGO, (0, self.SCREEN_HEIGHT - self.PYTHON_LOGO.get_height()))

		SCREEN.blit(self.GAME_LOGO, (60 * self.FACTOR_X, 20 * self.FACTOR_Y))	

		SCREEN.blit(self.MENU_GUI, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'new_game':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.NEW_GAME_BUTON.rect[0]-1, self.NEW_GAME_BUTON.rect[1]-1, self.NEW_GAME_BUTON.rect[2]+2,
															self.NEW_GAME_BUTON.rect[3]+2), 4)
			elif self.hovered_button == 'load_save':
				pygame.draw.rect(SCREEN, (23, 255, 23), (self.LOAD_SAVE_BUTTON.rect[0]-1, self.LOAD_SAVE_BUTTON.rect[1]-1, self.LOAD_SAVE_BUTTON.rect[2]+2,
															self.LOAD_SAVE_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'back':
				pygame.draw.rect(SCREEN, (255, 23, 23), (self.BACK_BUTTON.rect[0]-1, self.BACK_BUTTON.rect[1]-1, self.BACK_BUTTON.rect[2]+2,
															self.BACK_BUTTON.rect[3]+2), 4)
		else:
			self.HOVER_OVER_BUTTON_SOUND.fadeout(200)

#------------------------------------------------------------------------ MAIN MENU---------------------------------------------------------------------------#
###############################################################################################################################################################


###############################################################################################################################################################
#------------------------------------------------------------------------- NEW GAME---------------------------------------------------------------------------#
class NewGameMenu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_GUI, CHARACTER_CREATION_SHEET, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND):

		###############################################################################################################################################################
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		self.SCREEN_WIDTH:int               = SCREEN_WIDTH
		self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
		self.REFERENCE_SCREEN_SIZE_X:int    = 1920
		self.REFERENCE_SCREEN_SIZE_y:int    = 1080
		self.FACTOR_X:float                 = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
		self.FACTOR_Y:float                 = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y

		MENU_GUI_WIDTH:int 					= MENU_GUI.get_width()
		MENU_GUI_HEIGHT:int 				= MENU_GUI.get_height()
		self.MENU_GUI_MIDDLE_X:int 			= int(SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.MENU_GUI_MIDDLE_Y:int 			= int(SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)			

		self.HOVER_OVER_BUTTON_SOUND 		= HOVER_OVER_BUTTON_SOUND
		self.CLICK_BUTTON_SOUND 			= CLICK_BUTTON_SOUND
		self.hovered_button 				= None
		self.last_hovered_button 			= None		

		self.MENU_GUI 						= MENU_GUI
		self.CHARACTER_CREATION_SHEET 		= CHARACTER_CREATION_SHEET


		self.CHARACTER_CREATION_SHEET_SURFACE 			= pygame.Surface((self.CHARACTER_CREATION_SHEET.get_width(), self.CHARACTER_CREATION_SHEET.get_height()), pygame.SRCALPHA)
		self.CHARACTER_CREATION_SHEET_SURFACE.blit(self.CHARACTER_CREATION_SHEET, (0, 0))

		self.CHARACTER_CREATION_INFORMATION_SURFACE 	= pygame.Surface((self.CHARACTER_CREATION_SHEET.get_width(), self.CHARACTER_CREATION_SHEET.get_height()), pygame.SRCALPHA)


		self.CHARACTER_CREATION_SHEET_SCROLL_BAR 		= Utility.Scroll_Bar(423 * self.FACTOR_X, 13 * self.FACTOR_Y, 1053 * self.FACTOR_Y,
															self.CHARACTER_CREATION_SHEET.get_height() - 1000 * self.FACTOR_Y, (200,0,0), 17)


		self.font20 = Utility.ScalableFont('Aldrich.ttf', 20)

		self.image_offset_y = 0
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################	


		###############################################################################################################################################################
		#------------------------------------------------------------------------ TEX BOXES --------------------------------------------------------------------------#
		self.receive_player_keybord_input 				= False
		self.variable_to_receive_player_keybord_input 	= None

		self.ASSIGN_CHARACTER_NAME_BOX_RECT 			= pygame.Rect(88, 33, 453, 20)
		self.character_name 							=  {	
																'content' 		: '',
																'rect' 			: self.ASSIGN_CHARACTER_NAME_BOX_RECT,
																'maximum_size' 	: 34,
																'content_type' 	: str,
																'x_offset' 		: 4
															}

		self.ASSIGN_CHARACTER_AGE_BOX_RECT 				= pygame.Rect(616, 82, 59, 20)
		self.character_age 								=  {	
																'content' 		: '0',
																'rect' 			: self.ASSIGN_CHARACTER_AGE_BOX_RECT,
																'maximum_size' 	: 3,
																'content_type' 	: int,
																'x_offset' 		: 19
															}

		self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT 			= pygame.Rect(107, 278, 59, 20)
		self.character_weight 							=  {	
																'content' 		: '95',
																'rect' 			: self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT,
																'maximum_size' 	: 3,
																'content_type' 	: int,
																'x_offset' 		: 25
															}	

		#------------------------------------------------------------------------ TEX BOXES --------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#

		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.ASSIGN_CHARACTER_NAME_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_NAME'	
		elif self.ASSIGN_CHARACTER_AGE_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_AGE'
		elif self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_WEIGHT'					
		else:
			return None

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			if clicked_button == 'ASSIGN_CHARACTER_NAME':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.character_name

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_AGE':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.character_age

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_WEIGHT':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.character_weight

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()								
		else:
			self.receive_player_keybord_input = False
			self.variable_to_receive_player_keybord_input = None

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		else:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def draw(self, SCREEN):
		try:
			self.image_offset_y = self.CHARACTER_CREATION_SHEET_SCROLL_BAR.get_scroll_position()			


			self.CHARACTER_CREATION_SHEET_SCROLL_BAR.draw(SCREEN)


			######  BACKGROUND  ######
			SCREEN.blit(self.MENU_GUI, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))


			######  TEXT RENDERS  ######
			character_name_text_render 			= self.font20.render(	str(self.character_name['content']), 		True, 	(255,255,255))
			character_age_text_render 			= self.font20.render(	str(self.character_age['content']), 		True, 	(255,255,255))
			character_weight_text_render 		= self.font20.render(	str(self.character_weight['content']), 		True, 	(255,255,255))	

			self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_name_text_render, 	(	self.character_name['rect'][0]			+ self.character_name['x_offset']											
																							,   self.character_name['rect'][1] 		+ 1))

			self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_age_text_render, 	(	self.character_age['rect'][0] 			+ self.character_age['x_offset']		
																							,   self.character_age['rect'][1] 		+ 1))

			self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_weight_text_render, 	(	self.character_weight['rect'][0] 		+ self.character_weight['x_offset']		
																							,   self.character_weight['rect'][1] 	+ 1))				
			

			if self.receive_player_keybord_input == True:
				current_time = pygame.time.get_ticks()
				visibility_duration = 250
				cycle_duration = visibility_duration * 2

				if (current_time % cycle_duration) < visibility_duration:
					x = self.variable_to_receive_player_keybord_input['rect'][0] + self.variable_to_receive_player_keybord_input['x_offset'] + self.font20.render(str(self.variable_to_receive_player_keybord_input['content']), True, (255,255,255)).get_width()
					y = self.variable_to_receive_player_keybord_input['rect'][1]
					pygame.draw.rect(self.CHARACTER_CREATION_INFORMATION_SURFACE, (255,255,255), (x, y, 2, 18 * self.FACTOR_Y))


			######  SUBSURFACES  ######
			SCREEN.blit(self.CHARACTER_CREATION_SHEET_SURFACE.subsurface(				0,															# START X
																						self.image_offset_y,										# START Y
																						self.CHARACTER_CREATION_SHEET_SURFACE.get_width(),			# WIDTH
																						1000 * self.FACTOR_Y),										# HEIGHT
																						(439 * self.FACTOR_X, 14 * self.FACTOR_Y))					# BLIT POS

			SCREEN.blit(self.CHARACTER_CREATION_INFORMATION_SURFACE.subsurface(			0,															# START X
																						self.image_offset_y,										# START Y
																						self.CHARACTER_CREATION_INFORMATION_SURFACE.get_width(),	# WIDTH
																						1000 * self.FACTOR_Y),										# HEIGHT
																						(439 * self.FACTOR_X, 14 * self.FACTOR_Y))					# BLIT POS

			self.CHARACTER_CREATION_INFORMATION_SURFACE.fill((0, 0, 0, 0))				


			######  BUTTONS ######
			if self.hovered_button != None:
				pass
			else:
				self.HOVER_OVER_BUTTON_SOUND.fadeout(200)
		except Exception as e:
			print("An error occurred:")
			traceback.print_exc()
#------------------------------------------------------------------------- NEW GAME---------------------------------------------------------------------------#
###############################################################################################################################################################
