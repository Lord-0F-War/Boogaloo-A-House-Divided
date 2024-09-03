
import Utility
from PygameManager import pygame
from pyvidplayer import Video
from json import load as json_load, dump as json_dump
import numpy as np
import os
import sys
from datetime import datetime
import copy
import random
import traceback
import time


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
	def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_GUI, CHARACTER_CREATION_SHEET, HOVER_OVER_BUTTON_SOUND, CLICK_BUTTON_SOUND, CHARACTER_BRAIN_SPRITE,
				CHARACTER_HEART_SPRITE, CHARACTER_LUNGS_SPRITE, CHARACTER_LIVER_SPRITE, CHARACTER_STOMACH_SPRITE, CHARACTER_KIDNEYS_SPRITE,
				CHARACTER_INTESTINE_SPRITE, CHARACTER_ORGANS_COLLIDER_SPRITE, CHARACTER_SILHOUETTE):

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

		self.CHARACTER_BRAIN_SPRITE 		= CHARACTER_BRAIN_SPRITE
		self.CHARACTER_HEART_SPRITE 		= CHARACTER_HEART_SPRITE
		self.CHARACTER_LUNGS_SPRITE 		= CHARACTER_LUNGS_SPRITE
		self.CHARACTER_LIVER_SPRITE 		= CHARACTER_LIVER_SPRITE
		self.CHARACTER_STOMACH_SPRITE 		= CHARACTER_STOMACH_SPRITE
		self.CHARACTER_KIDNEYS_SPRITE 		= CHARACTER_KIDNEYS_SPRITE
		self.CHARACTER_INTESTINE_SPRITE 	= CHARACTER_INTESTINE_SPRITE

		self.CHARACTER_ORGANS_COLLIDER_SPRITE 	= CHARACTER_ORGANS_COLLIDER_SPRITE
		self.CHARACTER_SILHOUETTE 				= CHARACTER_SILHOUETTE

		self.organ_to_draw = None
		self.character_organs_collider_colors = {
			'CHARACTER_BRAIN_SPRITE'		: (255,0,0),
			'CHARACTER_HEART_SPRITE'		: (255,216,0),
			'CHARACTER_LUNGS_SPRITE'		: (255,106,0),
			'CHARACTER_LIVER_SPRITE'		: (182,255,0),
			'CHARACTER_STOMACH_SPRITE'		: (0,255,33),
			'CHARACTER_KIDNEYS_SPRITE'		: (0,255,144),
			'CHARACTER_INTESTINE_SPRITE'	: (0,255,255)
		}

		self.organs_updated_color_dict = {
			'CHARACTER_BRAIN_SPRITE'		: None,
			'CHARACTER_HEART_SPRITE'		: None,
			'CHARACTER_LUNGS_SPRITE'		: None,
			'CHARACTER_LIVER_SPRITE'		: None,
			'CHARACTER_STOMACH_SPRITE'		: None,
			'CHARACTER_KIDNEYS_SPRITE'		: None,
			'CHARACTER_INTESTINE_SPRITE'	: None
		}
		self.organs_updated_image_dict = {
			'CHARACTER_BRAIN_SPRITE'		: None,
			'CHARACTER_HEART_SPRITE'		: None,
			'CHARACTER_LUNGS_SPRITE'		: None,
			'CHARACTER_LIVER_SPRITE'		: None,
			'CHARACTER_STOMACH_SPRITE'		: None,
			'CHARACTER_KIDNEYS_SPRITE'		: None,
			'CHARACTER_INTESTINE_SPRITE'	: None
		}				


		#############################################################################################################################################
		self.CHARACTER_CREATION_SHEET_SURFACE 				= pygame.Surface((self.CHARACTER_CREATION_SHEET.get_width(), self.CHARACTER_CREATION_SHEET.get_height()), pygame.SRCALPHA)
		self.CHARACTER_CREATION_SHEET_SURFACE.blit(			self.CHARACTER_CREATION_SHEET, (0, 0))

		self.CHARACTER_CREATION_SHEET_RECT = pygame.Rect(
													424 * self.FACTOR_X,                                       # START X
													14 * self.FACTOR_Y,                                        # START Y
													self.CHARACTER_CREATION_SHEET_SURFACE.get_width() + 15,    # WIDTH
													1000 * self.FACTOR_Y                                       # HEIGHT
													)		

		self.CHARACTER_CREATION_INFORMATION_SURFACE 		= pygame.Surface((self.CHARACTER_CREATION_SHEET.get_width(), self.CHARACTER_CREATION_SHEET.get_height()), pygame.SRCALPHA)
		
		self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE 	= pygame.Surface((350, 953), pygame.SRCALPHA)
		self.CHARACTER_CREATION_ORGANS_SURFACE 				= pygame.Surface((725, 953), pygame.SRCALPHA)


		self.CHARACTER_CREATION_SHEET_SCROLL_BAR 			= Utility.Scroll_Bar(423 * self.FACTOR_X, 13 * self.FACTOR_Y, 1053 * self.FACTOR_Y,
															self.CHARACTER_CREATION_SHEET.get_height() - 1000 * self.FACTOR_Y, (200,0,0), 17)

		#############################################################################################################################################


		#############################################################################################################################################
		self.CHARACTER_SELECTION_SURFACE 					= pygame.Surface((376, 2048), pygame.SRCALPHA)

		self.CHARACTER_SELECTION_RECT = pygame.Rect(
													33 * self.FACTOR_X,                                        # START X
													18 * self.FACTOR_Y,                                        # START Y
													self.CHARACTER_SELECTION_SURFACE.get_width(),    	   	   # WIDTH
													1000 * self.FACTOR_Y                                       # HEIGHT
													)

		self.CHARACTER_SELECTION_SCROLL_BAR 				= Utility.Scroll_Bar(13 * self.FACTOR_X, 13 * self.FACTOR_Y, 1053 * self.FACTOR_Y,
															1000 * self.FACTOR_Y, (200,0,0), 17)

		#############################################################################################################################################


		self.font20 = Utility.ScalableFont('Aldrich.ttf', 20)
		self.font16 = Utility.ScalableFont('Aldrich.ttf', 16)

		self.character_creation_image_offset_y = 0
		#------------------------------------------------------------------------- UTILITY ---------------------------------------------------------------------------#
		###############################################################################################################################################################	


		###############################################################################################################################################################
		#------------------------------------------------------------------------ LOAD JSON --------------------------------------------------------------------------#
		MAIN_FOLDER 				= os.path.dirname(sys.argv[0])
		SAVES_FOLDER				= os.path.join(MAIN_FOLDER, 'saves')
		SAVEFILE_BASELINE_PATH 		= os.path.join(SAVES_FOLDER, 'save_source.json')

		savefile_baseline_data 		= self.load_savefile_baseline(SAVEFILE_BASELINE_PATH)

		saved_file_path 			= self.save_file_with_sys_date(savefile_baseline_data, SAVES_FOLDER)

		self.load_save_file(saved_file_path)

		#------------------------------------------------------------------------ LOAD JSON --------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#------------------------------------------------------------------------ TEX BOXES --------------------------------------------------------------------------#
		self.receive_player_keybord_input 				= False
		self.variable_to_receive_player_keybord_input 	= None

		# ID
		self.ASSIGN_CHARACTER_NAME_BOX_RECT 			= pygame.Rect(88, 33, 453, 20)

		self.ASSIGN_CHARACTER_AGE_BOX_RECT 				= pygame.Rect(616, 82, 59, 20)

		self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT 			= pygame.Rect(107, 278, 59, 20)

		self.ASSIGN_CHARACTER_NATIONALITY_BOX_RECT 				= pygame.Rect(157, 75, 384, 32)

		self.ASSIGN_CHARACTER_LANGUAGES_FLUENCY_BOX_RECT 		= pygame.Rect(252, 124, 442, 32)

		self.ASSIGN_CHARACTER_CAREERS_BOX_RECT 					= pygame.Rect(120, 173, 574, 32)

		self.ASSIGN_CHARACTER_HOBBIES_BOX_RECT 					= pygame.Rect(120, 222, 574, 32)


		# TRAITS
		self.ASSIGN_CHARACTER_STRENGHT_BOX_RECT 		= pygame.Rect(858, 32, 38, 20)

		self.ASSIGN_CHARACTER_CONSTITUTION_BOX_RECT 	= pygame.Rect(1155, 32, 38, 20)

		self.ASSIGN_CHARACTER_AGILITY_BOX_RECT 			= pygame.Rect(1335, 32, 38, 20)

		self.ASSIGN_CHARACTER_CHARISMA_BOX_RECT 		= pygame.Rect(903, 339, 38, 20)

		self.ASSIGN_CHARACTER_INTELLIGENCE_BOX_RECT 	= pygame.Rect(1259, 339, 38, 20)

		self.ASSIGN_CHARACTER_EDUCATION_BOX_RECT 		= pygame.Rect(913, 565, 38, 20)

		#------------------------------------------------------------------------ TEX BOXES --------------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#

		#------------------------------------------------------------------------- BUTTONS ---------------------------------------------------------------------------#
		###############################################################################################################################################################

	def get_button_by_interaction(self, mouse_rect):
		if self.ASSIGN_CHARACTER_NAME_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_NAME'	
		
		elif self.ASSIGN_CHARACTER_AGE_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_AGE'
		
		elif self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_WEIGHT'

		
		elif self.ASSIGN_CHARACTER_STRENGHT_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_STRENGHT'
		
		elif self.ASSIGN_CHARACTER_CONSTITUTION_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_CONSTITUTION'	
		
		elif self.ASSIGN_CHARACTER_AGILITY_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_AGILITY'
		
		elif self.ASSIGN_CHARACTER_CHARISMA_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_CHARISMA'	
		
		elif self.ASSIGN_CHARACTER_INTELLIGENCE_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_INTELLIGENCE'
		
		elif self.ASSIGN_CHARACTER_EDUCATION_BOX_RECT.colliderect((mouse_rect[0] - 439, mouse_rect[1]+self.character_creation_image_offset_y - 13, 1, 1)):
			return 'ASSIGN_CHARACTER_EDUCATION'											
		
		else:
			return None

	def get_organ_by_interaction(self, mouse_pos):
		try:
			if self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_BRAIN_SPRITE']:
				return 'CHARACTER_BRAIN_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_HEART_SPRITE']:
				return 'CHARACTER_HEART_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_LUNGS_SPRITE']:
				return 'CHARACTER_LUNGS_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_LIVER_SPRITE']:
				return 'CHARACTER_LIVER_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_STOMACH_SPRITE']:
				return 'CHARACTER_STOMACH_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_KIDNEYS_SPRITE']:
				return 'CHARACTER_KIDNEYS_SPRITE'
			elif self.CHARACTER_ORGANS_COLLIDER_SPRITE.get_at((mouse_pos[0]-439, mouse_pos[1]-354 + self.character_creation_image_offset_y)) == self.character_organs_collider_colors['CHARACTER_INTESTINE_SPRITE']:
				return 'CHARACTER_INTESTINE_SPRITE'															
					
		except Exception as e:
			return None		

	def click_button(self, mouse_rect):
		clicked_button = self.get_button_by_interaction(mouse_rect)

		if clicked_button != None:
			if clicked_button == 'ASSIGN_CHARACTER_NAME':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_name']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_AGE':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_age']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_WEIGHT':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_weight']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()	


			elif clicked_button == 'ASSIGN_CHARACTER_STRENGHT':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_strenght']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_CONSTITUTION':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_constituion']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()	
			elif clicked_button == 'ASSIGN_CHARACTER_AGILITY':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_agility']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_CHARISMA':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_charisma']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()	
			elif clicked_button == 'ASSIGN_CHARACTER_INTELLIGENCE':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_intelligence']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()
			elif clicked_button == 'ASSIGN_CHARACTER_EDUCATION':
				self.receive_player_keybord_input = True

				self.variable_to_receive_player_keybord_input = self.selected_character['character_education']

				self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
				self.CLICK_BUTTON_SOUND.play()																				

		else:
			if self.CHARACTER_SELECTION_RECT.colliderect(mouse_rect):
				for index, character in enumerate(self.characters):
					rect = (33, 18 + index * 100 - self.character_selection_image_offset_y + (10 * index if index > 0 else 0), 376, 100)
					rect = pygame.Rect(rect)
					if rect.colliderect(mouse_rect):
						self.selected_character = character

						self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
						self.CLICK_BUTTON_SOUND.play()	

						return
				
				rect = (33, 18 + (index+1) * 100 - self.character_selection_image_offset_y + 10 * (index+1), 376, 100)
				rect = pygame.Rect(rect)
				if rect.colliderect(mouse_rect):
					self.characters.append(copy.deepcopy(self.blank_character_sheet))
					self.set_random_atributes_for_new_character(self.characters[-1])
					self.HOVER_OVER_BUTTON_SOUND.fadeout(150)
					self.CLICK_BUTTON_SOUND.play()


			self.receive_player_keybord_input = False
			self.variable_to_receive_player_keybord_input = None

	def hover_button(self, mouse_rect):
		hovered_button = self.get_button_by_interaction(mouse_rect)
		if hovered_button != None:
			if hovered_button != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()

				self.last_hovered_button = hovered_button
				self.hovered_button = self.last_hovered_button
		elif self.organ_to_draw == None and hovered_button == None:
			self.last_hovered_button = None
			self.hovered_button = self.last_hovered_button

	def hover_organs(self, mouse_rect):
		hovered_organ = self.get_organ_by_interaction(mouse_rect)
		if hovered_organ == 'CHARACTER_BRAIN_SPRITE':
			self.organ_to_draw = 'CHARACTER_BRAIN_SPRITE'
		elif hovered_organ == 'CHARACTER_HEART_SPRITE':
			self.organ_to_draw = 'CHARACTER_HEART_SPRITE'
		elif hovered_organ == 'CHARACTER_LUNGS_SPRITE':
			self.organ_to_draw = 'CHARACTER_LUNGS_SPRITE'
		elif hovered_organ == 'CHARACTER_LIVER_SPRITE':
			self.organ_to_draw = 'CHARACTER_LIVER_SPRITE'
		elif hovered_organ == 'CHARACTER_STOMACH_SPRITE':
			self.organ_to_draw = 'CHARACTER_STOMACH_SPRITE'
		elif hovered_organ == 'CHARACTER_KIDNEYS_SPRITE':
			self.organ_to_draw = 'CHARACTER_KIDNEYS_SPRITE'
		elif hovered_organ == 'CHARACTER_INTESTINE_SPRITE':
			self.organ_to_draw = 'CHARACTER_INTESTINE_SPRITE'																	
		else:
			self.organ_to_draw = None
		
		if self.organ_to_draw != None:
			if self.organ_to_draw != self.last_hovered_button:
				self.HOVER_OVER_BUTTON_SOUND.play()
				self.last_hovered_button = self.organ_to_draw
		elif self.hovered_button == None:
			self.last_hovered_button = None

	def received_player_keybord_input(self, key_name, keys, mods):
		if len(str(self.variable_to_receive_player_keybord_input['value'])) < self.variable_to_receive_player_keybord_input['maximum_size']:
			#########################################################################################################
			if self.variable_to_receive_player_keybord_input['content_type'] == 'str':
				if  len(key_name) == 1 and key_name.isalpha():
					# Check if either shift key is pressed to determine uppercase
					if mods & pygame.KMOD_SHIFT or mods & pygame.KMOD_CAPS:
						key_name = key_name.upper()                        
					self.variable_to_receive_player_keybord_input['value'] += key_name
					
			#########################################################################################################

			#########################################################################################################
			if self.variable_to_receive_player_keybord_input['content_type'] == 'int':
				if len(key_name) == 1 and key_name.isnumeric():
					self.variable_to_receive_player_keybord_input['value'] = str(self.variable_to_receive_player_keybord_input['value'])
					self.variable_to_receive_player_keybord_input['value'] += key_name
					self.variable_to_receive_player_keybord_input['value'] = int(self.variable_to_receive_player_keybord_input['value'])
				
				elif key_name.startswith('[') and key_name.endswith(']'):

					self.variable_to_receive_player_keybord_input['value'] = str(self.variable_to_receive_player_keybord_input['value'])
					self.variable_to_receive_player_keybord_input['value'] += key_name[1:-1]
					self.variable_to_receive_player_keybord_input['value'] = int(self.variable_to_receive_player_keybord_input['value'])					                                     

			#########################################################################################################

			#########################################################################################################
			if keys[pygame.K_SPACE] and self.variable_to_receive_player_keybord_input['content_type'] == 'str':
				self.variable_to_receive_player_keybord_input['value'] += ' ' 

			#########################################################################################################

		if keys[pygame.K_BACKSPACE]:
			self.variable_to_receive_player_keybord_input['value'] = str(self.variable_to_receive_player_keybord_input['value'])
			self.variable_to_receive_player_keybord_input['value'] = self.variable_to_receive_player_keybord_input['value'][:-1]
			if self.variable_to_receive_player_keybord_input['content_type'] == 'int':
				self.variable_to_receive_player_keybord_input['value'] = str(self.variable_to_receive_player_keybord_input['value'])
				if len(str(self.variable_to_receive_player_keybord_input['value'])) == 0:
					self.variable_to_receive_player_keybord_input['value'] = 0

	def received_player_mousewheel_input(self, wheel_movement, mouse_rect):

		if self.CHARACTER_CREATION_SHEET_RECT.colliderect(mouse_rect):
			if wheel_movement > 0:
				self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position -= wheel_movement * 30
				if self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position < 0:
					self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position = 0
			elif wheel_movement < 0:
				self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position += abs(wheel_movement) * 30
				if self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position > self.CHARACTER_CREATION_SHEET.get_height() - 1000 * self.FACTOR_Y:
					self.CHARACTER_CREATION_SHEET_SCROLL_BAR.scroll_position = self.CHARACTER_CREATION_SHEET.get_height() - 1000 * self.FACTOR_Y

		elif self.CHARACTER_SELECTION_RECT.colliderect(mouse_rect):
			if wheel_movement > 0:
				self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position -= wheel_movement * 30
				if self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position < 0:
					self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position = 0
			elif wheel_movement < 0:
				self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position += abs(wheel_movement) * 30
				if self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position > self.CHARACTER_SELECTION_SURFACE.get_height() - 1000 * self.FACTOR_Y:
					self.CHARACTER_SELECTION_SCROLL_BAR.scroll_position = self.CHARACTER_SELECTION_SURFACE.get_height() - 1000 * self.FACTOR_Y									 		

	def change_white_to_color(self, sprite, color):
		sprite_name = sprite[1]
		if self.organs_updated_color_dict[sprite_name] != color:
			self.organs_updated_color_dict[sprite_name] = color

			sprite = sprite[0]

			# Ensure the sprite has an alpha channel
			sprite = sprite.convert_alpha()
			
			# Create a new surface with the same size and alpha channel
			new_sprite = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
			
			# Convert the sprite's pixels to a NumPy array
			sprite_array = pygame.surfarray.array3d(sprite)
			alpha_array = pygame.surfarray.array_alpha(sprite)
			
			# Create a mask where the white pixels are (considering a tolerance for near-white)
			white_mask = (sprite_array[:, :, 0] >= 80) & (sprite_array[:, :, 1] >= 80) & (sprite_array[:, :, 2] >= 80) & (alpha_array > 0)
			
			# Apply the new color only to the white areas
			sprite_array[white_mask] = color
			
			# Copy the modified sprite_array and alpha_array to the new surface
			new_sprite_array = pygame.surfarray.pixels3d(new_sprite)
			new_alpha_array = pygame.surfarray.pixels_alpha(new_sprite)
			
			new_sprite_array[:, :, :] = sprite_array
			new_alpha_array[:, :] = alpha_array

			self.organs_updated_image_dict[sprite_name] = new_sprite			

			return new_sprite
		return self.organs_updated_image_dict[sprite_name]

	def get_color_from_health(self, health, max_health):
		# Ensure health is within bounds
		health = max(0, min(health, max_health))
		
		# Calculate the percentage of health
		health_percentage = health / max_health
		
		# Define the start and end colors
		color_dead = (127, 0, 0)  
		color_alive = (0, 127, 0)  
		
		# Interpolate between the two colors
		r = int(color_dead[0] * (1 - health_percentage) + color_alive[0] * health_percentage)
		g = int(color_dead[1] * (1 - health_percentage) + color_alive[1] * health_percentage)
		b = int(color_dead[2] * (1 - health_percentage) + color_alive[2] * health_percentage)
		
		return (r, g, b)

	def draw(self, SCREEN):

		self.CHARACTER_CREATION_SHEET_SCROLL_BAR.draw(SCREEN)
		self.CHARACTER_SELECTION_SCROLL_BAR.draw(SCREEN)


		###############################################################################################################################################################
		#----------------------------------------------------------------------- CHAR CREATION -----------------------------------------------------------------------#
		
		self.character_creation_image_offset_y = self.CHARACTER_CREATION_SHEET_SCROLL_BAR.get_scroll_position()			


		######  BACKGROUND  ######
		SCREEN.blit(self.MENU_GUI, (self.MENU_GUI_MIDDLE_X, self.MENU_GUI_MIDDLE_Y))


		######  HEALTH  ######
		brain_color 		= self.get_color_from_health(100, 100)
		heart_color 		= self.get_color_from_health(100, 100)
		kidneys_color 		= self.get_color_from_health(100, 100)
		stomach_color 		= self.get_color_from_health(100, 100)
		liver_color 		= self.get_color_from_health(100, 100)
		lungs_color 		= self.get_color_from_health(100, 100)
		instestine_color 	= self.get_color_from_health(100, 100)


		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(self.CHARACTER_SILHOUETTE, 																						(	0											
																																											,   340))		
		
		
		if 'CHARACTER_BRAIN_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_BRAIN_SPRITE, 'CHARACTER_BRAIN_SPRITE'), brain_color), 					(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_BRAIN_SPRITE, 'CHARACTER_BRAIN_SPRITE'), brain_color), 					(	0											
																																												,   340))
		
		if 'CHARACTER_HEART_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_HEART_SPRITE, 'CHARACTER_HEART_SPRITE'), heart_color), 					(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_HEART_SPRITE, 'CHARACTER_HEART_SPRITE'), heart_color), 					(	0											
																																												,   340))
		
		if 'CHARACTER_KIDNEYS_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_KIDNEYS_SPRITE, 'CHARACTER_KIDNEYS_SPRITE'), kidneys_color), 			(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_KIDNEYS_SPRITE, 'CHARACTER_KIDNEYS_SPRITE'), kidneys_color), 			(	0											
																																												,   340))
		
		if 'CHARACTER_STOMACH_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_STOMACH_SPRITE, 'CHARACTER_STOMACH_SPRITE'), stomach_color), 			(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_STOMACH_SPRITE, 'CHARACTER_STOMACH_SPRITE'), stomach_color), 			(	0											
																																												,   340))
		
		if 'CHARACTER_LIVER_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_LIVER_SPRITE, 'CHARACTER_LIVER_SPRITE'), liver_color), 					(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_LIVER_SPRITE, 'CHARACTER_LIVER_SPRITE'), liver_color), 					(	0											
																																												,   340))
		
		if 'CHARACTER_LUNGS_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_LUNGS_SPRITE, 'CHARACTER_LUNGS_SPRITE'), lungs_color), 					(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_LUNGS_SPRITE, 'CHARACTER_LUNGS_SPRITE'), lungs_color), 					(	0											
																																												,   340))
		
		if 'CHARACTER_INTESTINE_SPRITE' == self.organ_to_draw or self.organ_to_draw == None:
			self.CHARACTER_CREATION_ORGANS_SURFACE.blit(self.change_white_to_color((self.CHARACTER_INTESTINE_SPRITE, 'CHARACTER_INTESTINE_SPRITE'), instestine_color), 		(	0											
																																												,   340))
		else:
			self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.blit(self.change_white_to_color((self.CHARACTER_INTESTINE_SPRITE, 'CHARACTER_INTESTINE_SPRITE'), instestine_color), 		(	0											
																																												,   340))

		self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.set_alpha(80)


		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE, (0, 0))
		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(self.CHARACTER_CREATION_ORGANS_SURFACE, (0, 0))


		######  TEXT RENDERS  ######
		character_name_text_render 			= self.font20.render(	str(self.selected_character['character_name']['value']), 						True, 	(255,255,255))
		character_age_text_render 			= self.font20.render(	str(self.selected_character['character_age']['value']), 						True, 	(255,255,255))
		character_weight_text_render 		= self.font20.render(	str(self.selected_character['character_weight']['value']), 						True, 	(255,255,255))
		character_nationality_text_render 	= self.font20.render(	self.selected_character['character_nationality']['value'].capitalize(), 		True, 	(255,255,255))


		languages_list = list(self.selected_character['character_languages_fluency']['value'].keys())
		languages = ', '.join(str(language).capitalize() for language in languages_list)
		character_languages_fluency_text_render = self.font20.render(languages,  True, 	(255,255,255))
		
		max_length = len(languages)
		while character_languages_fluency_text_render.get_width() > 415:
			max_length -= 1
			languages = languages[:max_length - 3] + '...'
			character_languages_fluency_text_render = self.font20.render(languages,  True, 	(255,255,255))
	

		careers_list = list(self.selected_character['character_careers']['value'].keys())
		careers = ', '.join(str(career).capitalize() for career in careers_list)
		character_careers_text_render = self.font20.render(careers,  True, 	(255,255,255))
		
		max_length = len(careers)
		while character_careers_text_render.get_width() > 415:
			max_length -= 1
			careers = careers[:max_length - 3] + '...'
			character_careers_text_render = self.font20.render(careers,  True, 	(255,255,255))


		hobbies_list = list(self.selected_character['character_hobbies']['value'].keys())
		hobbies = ', '.join(str(hobbie).capitalize() for hobbie in hobbies_list)
		character_hobbies_text_render = self.font20.render(hobbies,  True, 	(255,255,255))
		
		max_length = len(hobbies)
		while character_hobbies_text_render.get_width() > 415:
			max_length -= 1
			hobbies = hobbies[:max_length - 3] + '...'
			character_hobbies_text_render = self.font20.render(hobbies,  True, 	(255,255,255))			


		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_name_text_render, 		(	self.ASSIGN_CHARACTER_NAME_BOX_RECT[0]				+ self.selected_character['character_name']['x_offset']											
																							,   self.ASSIGN_CHARACTER_NAME_BOX_RECT[1] 			+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_age_text_render, 		(	self.ASSIGN_CHARACTER_AGE_BOX_RECT[0] 				+ self.selected_character['character_age']['x_offset']		
																							,   self.ASSIGN_CHARACTER_AGE_BOX_RECT[1] 			+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_weight_text_render, 		(	self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT[0] 			+ self.selected_character['character_weight']['x_offset']		
																							,   self.ASSIGN_CHARACTER_WEIGHT_BOX_RECT[1] 		+ 1))				
		
		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_nationality_text_render, (	self.ASSIGN_CHARACTER_NATIONALITY_BOX_RECT[0] 		+ self.selected_character['character_nationality']['x_offset']		
																							,   self.ASSIGN_CHARACTER_NATIONALITY_BOX_RECT[1] 	+ 9))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_languages_fluency_text_render, 	(	self.ASSIGN_CHARACTER_LANGUAGES_FLUENCY_BOX_RECT[0] 	+ self.selected_character['character_languages_fluency']['x_offset']		
																									,   self.ASSIGN_CHARACTER_LANGUAGES_FLUENCY_BOX_RECT[1] 	+ 9))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_careers_text_render, 			(	self.ASSIGN_CHARACTER_CAREERS_BOX_RECT[0] 				+ self.selected_character['character_careers']['x_offset']		
																									,   self.ASSIGN_CHARACTER_CAREERS_BOX_RECT[1] 				+ 9))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_hobbies_text_render, 			(	self.ASSIGN_CHARACTER_HOBBIES_BOX_RECT[0] 				+ self.selected_character['character_hobbies']['x_offset']		
																									,   self.ASSIGN_CHARACTER_HOBBIES_BOX_RECT[1] 				+ 9))						


		character_strenght_text_render 		= self.font20.render(	str(self.selected_character['character_strenght']['value']), 		True, 	(255,255,255))
		character_constituion_text_render 	= self.font20.render(	str(self.selected_character['character_constituion']['value']), 	True, 	(255,255,255))
		character_agility_text_render 		= self.font20.render(	str(self.selected_character['character_agility']['value']), 		True, 	(255,255,255))			
		character_charisma_text_render 		= self.font20.render(	str(self.selected_character['character_charisma']['value']), 		True, 	(255,255,255))
		character_intelligence_text_render 	= self.font20.render(	str(self.selected_character['character_intelligence']['value']),	True, 	(255,255,255))
		character_education_text_render 	= self.font20.render(	str(self.selected_character['character_education']['value']), 		True, 	(255,255,255))	


		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_strenght_text_render, 		(	self.ASSIGN_CHARACTER_STRENGHT_BOX_RECT[0]			+ self.selected_character['character_strenght']['x_offset']											
																								,   self.ASSIGN_CHARACTER_STRENGHT_BOX_RECT[1] 		+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_constituion_text_render, 	(	self.ASSIGN_CHARACTER_CONSTITUTION_BOX_RECT[0] 		+ self.selected_character['character_constituion']['x_offset']		
																								,   self.ASSIGN_CHARACTER_CONSTITUTION_BOX_RECT[1] 	+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_agility_text_render, 		(	self.ASSIGN_CHARACTER_AGILITY_BOX_RECT[0] 			+ self.selected_character['character_agility']['x_offset']		
																								,   self.ASSIGN_CHARACTER_AGILITY_BOX_RECT[1] 		+ 1))
		
		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_charisma_text_render, 		(	self.ASSIGN_CHARACTER_CHARISMA_BOX_RECT[0]			+ self.selected_character['character_charisma']['x_offset']											
																								,   self.ASSIGN_CHARACTER_CHARISMA_BOX_RECT[1] 		+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_intelligence_text_render, 	(	self.ASSIGN_CHARACTER_INTELLIGENCE_BOX_RECT[0] 		+ self.selected_character['character_intelligence']['x_offset']		
																								,   self.ASSIGN_CHARACTER_INTELLIGENCE_BOX_RECT[1] 	+ 1))

		self.CHARACTER_CREATION_INFORMATION_SURFACE.blit(character_education_text_render, 		(	self.ASSIGN_CHARACTER_EDUCATION_BOX_RECT[0] 		+ self.selected_character['character_education']['x_offset']		
																								,   self.ASSIGN_CHARACTER_EDUCATION_BOX_RECT[1] 	+ 1))			


		if self.receive_player_keybord_input == True:
			current_time = pygame.time.get_ticks()
			visibility_duration = 250
			cycle_duration = visibility_duration * 2

			if (current_time % cycle_duration) < visibility_duration:
				variable_to_receive_player_keybord_input_rect = getattr(self, self.variable_to_receive_player_keybord_input['rect'])
				x = variable_to_receive_player_keybord_input_rect[0] + self.variable_to_receive_player_keybord_input['x_offset'] + self.font20.render(str(self.variable_to_receive_player_keybord_input['value']), True, (255,255,255)).get_width()
				y = variable_to_receive_player_keybord_input_rect[1]
				pygame.draw.rect(self.CHARACTER_CREATION_INFORMATION_SURFACE, (255,255,255), (x, y, 2, 18 * self.FACTOR_Y))


		######  SUBSURFACES  ######
		SCREEN.blit(self.CHARACTER_CREATION_SHEET_SURFACE.subsurface(				0,															# START X
																					self.character_creation_image_offset_y,						# START Y
																					self.CHARACTER_CREATION_SHEET_SURFACE.get_width(),			# WIDTH
																					1000 * self.FACTOR_Y),										# HEIGHT
																					(439 * self.FACTOR_X, 14 * self.FACTOR_Y))					# BLIT POS

		SCREEN.blit(self.CHARACTER_CREATION_INFORMATION_SURFACE.subsurface(			0,															# START X
																					self.character_creation_image_offset_y,						# START Y
																					self.CHARACTER_CREATION_INFORMATION_SURFACE.get_width(),	# WIDTH
																					1000 * self.FACTOR_Y),										# HEIGHT
																					(439 * self.FACTOR_X, 14 * self.FACTOR_Y))					# BLIT POS

		self.CHARACTER_CREATION_INFORMATION_SURFACE.fill((0, 0, 0, 0))
		self.CHARACTER_CREATION_ORGANS_SURFACE.fill((0, 0, 0, 0))
		self.CHARACTER_CREATION_ORGANS_TRANSPARENT_SURFACE.fill((0, 0, 0, 0))				


		#----------------------------------------------------------------------- CHAR CREATION -----------------------------------------------------------------------#
		###############################################################################################################################################################


		###############################################################################################################################################################
		#---------------------------------------------------------------------- CHAR SELECTION -----------------------------------------------------------------------#
		
		self.character_selection_image_offset_y = self.CHARACTER_SELECTION_SCROLL_BAR.get_scroll_position()


		for index, character in enumerate(self.characters):

			rect = (0, (index * 100) + 10 * index if index > 0 else 0, 376, 100)

			width = 4 if character is self.selected_character else 1
			color = (160,133,0) if character is self.selected_character else (170,127,127)			
			pygame.draw.rect(self.CHARACTER_SELECTION_SURFACE, color, rect, width)

			character_name_text_render = self.font16.render(str(character['character_name']['value']), 	True,  (255,255,255))

			self.CHARACTER_SELECTION_SURFACE.blit(character_name_text_render, (8, 10 + ((index * 100) + 10 * index if index > 0 else 0)))


		rect = (0, (index+1) * 100 + 10 * (index+1), 376, 30)
		pygame.draw.rect(self.CHARACTER_SELECTION_SURFACE, (91,127,0), rect, 2)


		new_character_text_render = self.font16.render('CREATE NEW CHARACTER', 	True,  (255,255,255))
		self.CHARACTER_SELECTION_SURFACE.blit(new_character_text_render, (188 - new_character_text_render.get_width()/2, 16 - new_character_text_render.get_height()/2 + (index+1) * 100 + 10 * (index+1)))			


		######  SUBSURFACES  ######
		SCREEN.blit(self.CHARACTER_SELECTION_SURFACE.subsurface(					0,															# START X
																					self.character_selection_image_offset_y,					# START Y
																					self.CHARACTER_SELECTION_SURFACE.get_width(),				# WIDTH
																					1000 * self.FACTOR_Y),										# HEIGHT
																					(33 * self.FACTOR_X, 18 * self.FACTOR_Y))					# BLIT POS

		self.CHARACTER_SELECTION_SURFACE.fill((0, 0, 0, 0))

		#---------------------------------------------------------------------- CHAR SELECTION -----------------------------------------------------------------------#
		###############################################################################################################################################################


		######  BUTTONS ######
		if self.hovered_button != None:
			pass
		else:
			self.HOVER_OVER_BUTTON_SOUND.fadeout(200)				

	def load_savefile_baseline(self, savefile_baseline_path):
		with open(savefile_baseline_path, 'r') as file:
			baseline_data = json_load(file)
		return baseline_data

	def save_file_with_sys_date(self, file_data_to_save, directory_to_save):
		current_date = datetime.now().strftime("%Y_%m_%d_%H_%M")
		filename = f"temp_save_{current_date}.json"
		saved_file_path = os.path.join(directory_to_save, filename)
		
		with open(saved_file_path, 'w') as file:
			json_dump(file_data_to_save, file, indent=4)
		
		return saved_file_path	

	def load_save_file(self, file_path):
		with open(file_path, 'r') as file:
			save_data = json_load(file)
		
		self.characters = save_data

		self.blank_character_sheet = copy.deepcopy(self.characters[0])

		self.selected_character = self.characters[0]

		self.set_random_atributes_for_new_character(self.selected_character)

	def set_random_atributes_for_new_character(self, character):
		MAIN_FOLDER 				= os.path.dirname(sys.argv[0])
		COMMON_FOLDER				= os.path.join(MAIN_FOLDER, 'common')
		CHARACTER_FOLDER			= os.path.join(COMMON_FOLDER, 'character')

		NATIONALITIES_PATH 			= os.path.join(CHARACTER_FOLDER, 'nationalities.json')
		NAMES_PATH 					= os.path.join(CHARACTER_FOLDER, 'names.json')

		with open(NATIONALITIES_PATH, 'r') as file:
			nationalities_data : dict = json_load(file)

		random_nationality = random.choice(list(nationalities_data.items()))
		character['character_nationality']['value'] = random_nationality[0]


		with open(NAMES_PATH, 'r') as file:
			names_data : dict = json_load(file)		

		character_name_culture = random_nationality[1]['culture']
		if character_name_culture in names_data:
			random_first_name = random.choice(names_data[character_name_culture][0])
			random_last_name = random.choice(names_data[character_name_culture][1])
			character['character_name']['value'] = random_first_name + ' ' + random_last_name


		character['character_age']['value'] 		= random.randint(17, 65)
		character['character_weight']['value'] 		= random.randint(70, 120)



		LANGUAGES_PATH 				= os.path.join(CHARACTER_FOLDER, 'languages.json')

		with open(LANGUAGES_PATH, 'r') as file:
			languages_data : dict = json_load(file)

		character_languages_fluency = random.choices(list(languages_data.items()), k = random.randint(1, len(list(languages_data.keys()))))

		character['character_languages_fluency']['value'] = dict(character_languages_fluency)



		CAREERS_PATH 				= os.path.join(CHARACTER_FOLDER, 'careers.json')

		with open(CAREERS_PATH, 'r') as file:
			careers_data : dict = json_load(file)	

		character_careers = random.choices(list(careers_data.items()), k = random.randint(1, len(list(careers_data.keys()))))

		character['character_careers']['value'] = dict(character_careers)



		HOBBIES_PATH 				= os.path.join(CHARACTER_FOLDER, 'hobbies.json')

		with open(HOBBIES_PATH, 'r') as file:
			hobbies_data : dict = json_load(file)	

		character_hobbies = random.choices(list(hobbies_data.items()), k = random.randint(1, len(list(hobbies_data.keys()))))

		character['character_hobbies']['value'] = dict(character_hobbies)							

	def save_to_file(self, file_path):
		save_data = [
			{
				"character_name": self.selected_character['character_name'],
				"character_age": self.selected_character['character_age'],
				"character_weight": self.selected_character['character_weight'],
				
				"character_strenght": self.selected_character['character_strenght'],
				"character_constituion": self.selected_character['character_constituion'],
				"character_agility": self.selected_character['character_agility'],
				"character_charisma": self.selected_character['character_charisma'],
				"character_intelligence": self.selected_character['character_intelligence'],
				"character_education": self.selected_character['character_education']
			}
		]
		
		with open(file_path, 'w') as file:
			json_dump(save_data, file, indent=4)		

#------------------------------------------------------------------------- NEW GAME---------------------------------------------------------------------------#
###############################################################################################################################################################
