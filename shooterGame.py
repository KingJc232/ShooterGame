import pygame
import random

"""
	Things Todo:
		- Delete the bullets once they pass a certain position
		- Add sprites So the game looks Nicer
		- Add Collision Detection AABB ??
		- Add States To have a start Menu ?? (Use a stack to hold the states)
		- Button Class For Main Menu ???
		- Make it so that if a fruit Touches the floor you lose
		
"""

pygame.init() #Initializing all modules in pygam e

#RGB
WHITE = (255,255,255)
PURPLE = (200, 100, 250)
BLUE = (0, 100, 200)

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


class Player(pygame.Surface):
	def __init__(self, screenW, screenH, width = 40, height = 80):
		super().__init__((width,height))

		#Saving the Screens Dimensions
		self.screenW = screenW
		self.screenH = screenH

		self.fill(BLUE)
		self.speed = 2
		#left top width height
		self.playerRect = pygame.Rect(screenW/2, screenH - self.get_height(),self.get_width(), self.get_height())

		#List that Holds all bullets of the Player
		self.bullets = [] #Initially None

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
		pass
	def _movePlayer(self, keys, dt):

		#Move Left
		if keys[pygame.K_a]:
			self.playerRect.left -= self.speed * dt
		#move Right
		if keys[pygame.K_d]:
			self.playerRect.left += self.speed * dt

		if keys[pygame.K_SPACE ]:
			self.bullets.append(Bullet(self.playerRect.left, self.playerRect.top)) #Creating Bullets
		pass

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

	def __init__(self, width = 1000, height = 800):
		self.__screen = pygame.display.set_mode((width, height))
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
