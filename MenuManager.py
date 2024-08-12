
import Utility
from PygameManager import pygame
from pyvidplayer import Video


#---------------------------------------------------------------------- UTILITY MENUS ------------------------------------------------------------------------#

class ESC_Menu:
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
		
	def get_button_by_interaction(self, mouse_rect):
		if self.OPTIONS_BUTTON.rect.colliderect(mouse_rect):
			return 'options'
		elif self.MAIN_MENU_BUTTON.rect.colliderect(mouse_rect):
			return 'main_menu'
		elif self.QUIT_BUTTON.rect.colliderect(mouse_rect):
			return 'quit'		
		else:
			return None

	def get_clicked_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			self.hover_over_button_sound.fadeout(150)
			self.click_menu_sound.play()
		return clicked_button

	def get_hovered_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if self.hovered_button != None:
			if self.hovered_button != self.last_hovered_button:
				self.hover_over_button_sound.play()
				self.last_hovered_button = self.hovered_button
		else:
			self.last_hovered_button = None
		
		return hovered_button

	def draw(self, surface_alfa):
		surface_alfa.blit(self.esc_menu_background, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))

		if self.hovered_button != None:
			if self.hovered_button == 'options':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.OPTIONS_BUTTON.rect[0]-1, self.OPTIONS_BUTTON.rect[1]-1, self.OPTIONS_BUTTON.rect[2]+2, self.OPTIONS_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'main_menu':
				pygame.draw.rect(surface_alfa, (23, 255, 23), (self.MAIN_MENU_BUTTON.rect[0]-1, self.MAIN_MENU_BUTTON.rect[1]-1, self.MAIN_MENU_BUTTON.rect[2]+2, self.MAIN_MENU_BUTTON.rect[3]+2), 4)
			elif self.hovered_button == 'quit':
				pygame.draw.rect(surface_alfa, (255, 23, 23), (self.QUIT_BUTTON.rect[0]-1, self.QUIT_BUTTON.rect[1]-1, self.QUIT_BUTTON.rect[2]+2, self.QUIT_BUTTON.rect[3]+2), 4)			

class Options_Menu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, options_menu_background, generic_hover_over_button_sound, generic_click_menu_sound, Sounds_Manager, Main_Menu) -> None:

		self.Sounds_Manager = Sounds_Manager
		self.Main_Menu = Main_Menu

		self.hover_over_button_sound, self.click_menu_sound = generic_hover_over_button_sound, generic_click_menu_sound
		self.hovered_button = None
		self.last_hovered_button = None		

		reference_SCREEN_size_x = 1920
		reference_SCREEN_size_y = 1080
		self.FACTOR_X = SCREEN_WIDTH / reference_SCREEN_size_x
		self.FACTOR_Y = SCREEN_HEIGHT / reference_SCREEN_size_y		

		self.options_menu_background = pygame.transform.smoothscale_by(options_menu_background, (self.FACTOR_X,self.FACTOR_Y))			

		MENU_GUI_WIDTH = self.options_menu_background.get_width()
		MENU_GUI_HEIGHT = self.options_menu_background.get_height()
		
		self.options_MENU_GUI_MIDDLE_X = (SCREEN_WIDTH/2 - MENU_GUI_WIDTH/2)
		self.options_MENU_GUI_MIDDLE_Y = (SCREEN_HEIGHT/2 - MENU_GUI_HEIGHT/2)		


		back_button_width = 371 * self.FACTOR_X
		back_button_height = 34 * self.FACTOR_Y
		back_button_x_offset = 63 * self.FACTOR_X
		back_button_y_offset = 887 * self.FACTOR_Y
		self.back_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + back_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + back_button_y_offset, back_button_width, back_button_height)	
		
		resolutions_button_width = 371 * self.FACTOR_X
		resolutions_button_height = 34 * self.FACTOR_Y
		resolutions_button_x_offset = 62 * self.FACTOR_X
		self.resolution_2560x1440_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + 100 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1920x1080_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + 145 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1600x900_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + 190 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1440x900_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + 235 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)	
		self.resolution_1280x1024_button = Utility.Button(self.options_MENU_GUI_MIDDLE_X + resolutions_button_x_offset, self.options_MENU_GUI_MIDDLE_Y + 280 * self.FACTOR_Y,
												resolutions_button_width, resolutions_button_height)										

		self.clicked_resolution_button = f'resolution_{SCREEN_WIDTH}x{SCREEN_HEIGHT}'


		self.brightness_slider = Utility.Slide(self.options_MENU_GUI_MIDDLE_X + 457* self.FACTOR_X, self.options_MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y, 374* self.FACTOR_X, 10* self.FACTOR_Y, 0, 180, 0)
		
		self.music_slider = Utility.Slide(self.options_MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.options_MENU_GUI_MIDDLE_Y + 135* self.FACTOR_Y, 374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 10)
		self.sound_slider = Utility.Slide(self.options_MENU_GUI_MIDDLE_X + 852* self.FACTOR_X, self.options_MENU_GUI_MIDDLE_Y + 270* self.FACTOR_Y, 374* self.FACTOR_X, 10* self.FACTOR_Y, 0, max_value = 100, initial_value = 50)
		
		pygame.mixer.music.set_volume(self.music_slider.value/100)	
		self.Sounds_Manager.change_volume(self.sound_slider.value/100)

		self.Main_Menu.main_menu_intro_video.set_volume(self.sound_slider.value/100)		

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

	def get_clicked_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			self.hover_over_button_sound.fadeout(150)
			self.click_menu_sound.play()
			self.clicked_resolution_button = clicked_button
		return clicked_button

	def get_hovered_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if self.hovered_button != None:
			if self.hovered_button != self.last_hovered_button:
				self.hover_over_button_sound.play()
				self.last_hovered_button = self.hovered_button
		else:
			self.last_hovered_button = None
		
		return hovered_button	

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
		surface_alfa.blit(self.options_menu_background, (self.options_MENU_GUI_MIDDLE_X, self.options_MENU_GUI_MIDDLE_Y))

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


#------------------------------------------------------------------------ MAIN MENU---------------------------------------------------------------------------#

class Main_Menu:
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, game_logo, python_logo, main_menu_backgound, menu_gui, hover_over_button_sound, click_menu_sound):

		self.hovered_button = None
		self.last_hovered_button =None

		self.hover_over_button_sound = hover_over_button_sound
		self.click_menu_sound = click_menu_sound
		
		self.is_in_new_game_menu = False
		
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

		# NEW GAME / LOAD SAVE  MENU
		'''
		new_game_button_width = 371 * self.FACTOR_X
		new_game_button_height = 34 * self.FACTOR_Y
		new_game_button_x_offset = 59 * self.FACTOR_X
		new_game_button_y_offset = 28 * self.FACTOR_Y
		self.new_game_button = Utility.Button(self.new_game_menu_background_middle_x + new_game_button_x_offset, self.new_game_menu_background_middle_y + new_game_button_y_offset, new_game_button_width, new_game_button_height)

		load_save_button_width = 371 * self.FACTOR_X
		load_save_button_height = 34 * self.FACTOR_Y
		load_save_button_x_offset = 59 * self.FACTOR_X
		load_save_button_y_offset = 79 * self.FACTOR_Y
		self.load_save_button = Utility.Button(self.new_game_menu_background_middle_x + load_save_button_x_offset, self.new_game_menu_background_middle_y + load_save_button_y_offset, load_save_button_width, load_save_button_height)

		back_button_width = 371 * self.FACTOR_X
		back_button_height = 34 * self.FACTOR_Y
		back_button_x_offset = 59 * self.FACTOR_X
		back_button_y_offset = 162 * self.FACTOR_Y
		self.back_button = Utility.Button(self.new_game_menu_background_middle_x + back_button_x_offset, self.new_game_menu_background_middle_y + back_button_y_offset, back_button_width, back_button_height)
		'''
		self.main_menu_intro_video = Video("game_intro.mp4", size=(936 * self.FACTOR_X, 378 * self.FACTOR_Y))
		self.main_menu_intro_video.set_volume(0)

	def get_button_by_interaction(self, mouse_rect):
		if self.start_button.rect.colliderect(mouse_rect):
			return 'start'
		elif self.QUIT_BUTTON.rect.colliderect(mouse_rect):
			return 'quit'
		elif self.OPTIONS_BUTTON.rect.colliderect(mouse_rect):
			return 'options'
		#elif self.new_game_button.rect.colliderect(mouse_rect):
		#	return 'new_game'
		#elif self.load_save_button.rect.colliderect(mouse_rect):
		#	return 'load_save'
		#elif self.back_button.rect.colliderect(mouse_rect):
		#	return 'back'		
		else:
			return None

	def get_clicked_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)
		if clicked_button != None:
			if self.is_in_new_game_menu == False:
				self.hover_over_button_sound.fadeout(150)
				self.click_menu_sound.play()	
			else:
				if clicked_button == 'new_game':
					self.hover_over_button_sound.fadeout(150)
					self.click_menu_sound.play()
				elif clicked_button == 'load_save':
					self.hover_over_button_sound.fadeout(150)
					self.click_menu_sound.play()
				elif clicked_button == 'back':		
					self.hover_over_button_sound.fadeout(150)
					self.click_menu_sound.play()								

		return clicked_button

	def get_hovered_button(self, mouse_rect):
		self.hovered_button = self.get_button_by_interaction(mouse_rect)
		if self.is_in_new_game_menu == False:
			if self.hovered_button != self.last_hovered_button and self.hovered_button not in ['new_game', 'load_save', 'back'] and self.hovered_button != None:
				self.hover_over_button_sound.play()
				self.last_hovered_button = self.hovered_button
				return self.hovered_button
			elif self.hovered_button != None:
				return self.last_hovered_button
			else:
				self.last_hovered_button = None
				return None
		else:
			if self.hovered_button != self.last_hovered_button and self.hovered_button in ['new_game', 'load_save', 'back'] and self.hovered_button != None:
				self.hover_over_button_sound.play()
				self.last_hovered_button = self.hovered_button
				return self.hovered_button
			elif self.hovered_button != None:
				return self.last_hovered_button
			else:
				self.last_hovered_button = None
				return None				

	def draw(self, SCREEN):
		SCREEN.blit(self.main_menu_backgound, (0, 0))

		SCREEN.blit(self.python_logo, (0, self.SCREEN_HEIGHT - self.python_logo.get_height()))

		SCREEN.blit(self.game_logo, (60 * self.FACTOR_X, 20 * self.FACTOR_Y))	
		
		if self.is_in_new_game_menu == False:
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
		else:
			#SCREEN.blit(self.new_game_menu_background, (self.new_game_menu_background_middle_x, self.new_game_menu_background_middle_y))
			if self.hovered_button != None:
				if self.hovered_button == 'new_game':
					SCREEN.blit(self.hovered_green_button_menu_image, self.new_game_button.rect)
				elif self.hovered_button == 'load_save':
					SCREEN.blit(self.hovered_green_button_menu_image, self.load_save_button.rect)
				elif self.hovered_button == 'back':
					SCREEN.blit(self.hovered_red_button_menu_image, self.back_button.rect)										
			else:
				self.hover_over_button_sound.fadeout(200)


#-------------------------------------------------------------------------- #### -----------------------------------------------------------------------------#