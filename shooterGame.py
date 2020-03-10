import pygame
import random

"""
	Things Todo:
		- Finish a Enemy Class to beat the game 
			- Add the sprites to the enemy class 
			- make it so that enemy class spits out little enemies 
			- add collision detection to the game 
		- Make it so that The player has to reload etc ... 
		- Add sprites So the game looks Nicer (Kinda Done) Need to do it for the player as well 
		- Make it so that if a alien Touches the floor you lose
		- Add Collision Detection AABB ?? I think there is a built in collision detection 
		- Add States To have a start Menu ?? (Use a stack to hold the states)
		- Button Class For Main Menu ???
		
"""

pygame.init() #Initializing all modules in pygam e

#RGB
WHITE = (255,255,255)
PURPLE = (200, 100, 250)
BLUE = (0, 100, 200)
GREEN = (0,255,100)

#This will be my animation class 
class Animation: 

	#Default constructor 
	def __init__(self, entity ,picList = [pygame.image.load("default.jpg")]):
		#left, top, width, height 
		self.animationRect = pygame.Rect(entity.playerRect.left, entity.playerRect.top, picList[0].get_width(), picList[0].get_height())
		#Determines what position the Player is currently Facing 
		self.left = False
		self.right = False 
		self.idle = True #Default the player is Idle 
		

	#Might delete these later dont know how I want to set up the animation 
	def draw(self, screen, entity):
		pass

	def update(self, keys, dt):
		pass


class Bullet(pygame.Surface):
	def __init__(self, playerX, playerY, width = 10, height = 10):

		super().__init__((width, height))
		self.bulletRect = pygame.Rect(playerX, playerY, width, height)

		red = random.randint(0, 255)
		green = random.randint(0,255)
		blue = random.randint(0,255)


		self.fill((red,green,blue)) #Purple Bullets
		self.speed = 10 #Speed of the bullets
		self.active = True #Determines if the Bullet should be active or not

	#Draws the Bullet onto the screen
	def draw(self, screen):
		screen.blit(self, (self.bulletRect.left, self.bulletRect.top))
		pass

	#Updates the Bullets
	def update(self):
		self._check_boundaries() #Checking if its still within boundary

		if self.active:
			self._moveBullets() #Moving the Bullets Up

		pass

	#Checks if the bullet has passed a certain boundary
	def _check_boundaries(self):
		posY = self.bulletRect.top

		if posY <= 0:
			#STOP
			self.active = False #Turn it off

		pass

	#Moves the Bullets Up
	def _moveBullets(self):
		self.bulletRect.top -= self.speed
		pass

	pass

class Enemy(pygame.Surface):
	def __init__(self, screenW, screenH, image, width = 200, height = 200):
		self.screenW = screenW #Saving the Dimensions of the screen 
		self.screenH = screenH 
		#left top width height 
		startPosX = 0
		startPosY = 0 
		self.image = pygame.image.load(image) #Saving the Image in the object variable 

		self.playerRect = pygame.Rect(startPosX, startPosY, width, height)

	def update(self):
		pass 

	def draw(self, screen):

		#Drawing the Animation to the Surface 
		self.blit(self.image, (self.playerRect.left, self.playerRect.top))

		#Drawing the surface to the screen 
		screen.blit(self, (self.playerRect.left, self.playerRect.top))
	 

class Player(pygame.Surface):
	def __init__(self, screenW, screenH, width = 40, height = 80):
		super().__init__((width,height))

		#Saving the Screens Dimensions
		self.screenW = screenW
		self.screenH = screenH
		self.fixY = screenH - (height *2)

		self.fill(GREEN)
		self.speed = 2
		#left top width height
		self.playerRect = pygame.Rect(screenW/2, self.fixY,self.get_width(), self.get_height())

		#List that Holds all bullets of the Player
		self.bullets = [] #Initially None
		self.isJump = False
		self.jumpCount = 10 

	def draw(self, screen):
		screen.blit(self,(self.playerRect.left, self.playerRect.top))
		#Drawing all the bullets of the player
		for bullet in self.bullets:
			bullet.draw(screen) #Drawing the bullet

	def update(self, keys, dt):

		self._movePlayer(keys, dt)
		self._check_boundaries()

		#Checking the boundaries of the bullet before updating them


		#Updating the Bullets 
		for bullet in self.bullets:
				bullet.update()	
		#Checking if we need to delete the bullets I DONT LIKE THIS SOLUTION BUT IT WORKS :(
		for bullet in self.bullets:
			if bullet.active == False:
				self.bullets.remove(bullet) #Remove this bullet 
			break 

		pass
	def _movePlayer(self, keys, dt):

		#Adding Jumping with key SPACE
		#Move Left
		if keys[pygame.K_a]:
			self.playerRect.left -= self.speed * dt
		#move Right
		if keys[pygame.K_d]:
			self.playerRect.left += self.speed * dt

		if keys[pygame.K_b ]:
			self.bullets.append(Bullet(self.playerRect.left, self.playerRect.top)) #Creating Bullets

		#IF Player is not jumping  NO DOUBLE JUMPS 
		if not (self.isJump):

			#Reset their Y position back down just in case 
			self.playerRect.top = self.fixY

			#Checking if they want to jump 
			if keys[pygame.K_SPACE]:
				self.isJump = True #Player wants to jump 

		#Else Player Hit the Jump Key
		else:
			if self.jumpCount >= -10:
				neg = 1
				if self.jumpCount < 0:
					neg = -1 
				self.playerRect.top -= (self.jumpCount ** 2) * 0.5 * neg
				self.jumpCount -= 1 #Counter 
			else:
				#Resetting the Variables 
				self.isJump = False
				self.jumpCount = 10 

	def _check_boundaries(self):

		posX = self.playerRect.left

		#If the player is on the right of the screen STOP DONT MOVE 
		if posX >= self.screenW - self.get_width():
			self.playerRect.left = self.screenW - self.get_width()
			#self.playerRect.left = self.playerRect.width

		#If the Player is on the Left of the Screen STOP DONT MOVE 
		if posX <= 0:
			self.playerRect.left = 0
			#self.playerRect.left = self.screenW


		pass


class Game:

	def __init__(self, width = 1280, height = 720):
		self.__screen = pygame.display.set_mode((width, height))
		self.__backgroundImage = pygame.image.load("background.png")
		pygame.display.set_caption("Shooter Game")

		self.main_player = Player(self.__screen.get_width(), self.__screen.get_height()) #Creating the Main Player
		pass

	def start(self):

		isOver = False
		clock = pygame.time.Clock()
		while not isOver:

			dt = clock.tick(60) #COntrols the Speed of the Game
			#Event Loop Handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					isOver = True

			self.__screen.fill(WHITE)

			self.update(dt) #Updating all Components in the Game

			self.draw() #Drawing all components in the Game

			pygame.display.update() #Updating all display modules

		pygame.quit() #Quit Pygame
		pass

	def draw(self):
		#Drawomg the Background of the game 
		self.__screen.blit(self.__backgroundImage, (0,0))
		#Drawing the Main Player
		self.main_player.draw(self.__screen)
		pass
	def update(self, dt):
		#Updating the Main Player
		keys = pygame.key.get_pressed() #Getting a List of all boolean values of all keys
		self.main_player.update(keys, dt)

	pass



def main():
	shooterGame = Game()
	shooterGame.start()
	pass


if __name__ == "__main__":
	main()
