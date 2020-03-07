import pygame 
import random 

"""
	Things Todo: 
		- Delete the bullets once they pass a certain position 
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
		self.speed = 20
		#left top width height 
		self.playerRect = pygame.Rect(screenW/2, screenH - self.get_height(),self.get_width(), self.get_height())

		#List that Holds all bullets of the Player 
		self.bullets = [] #Initially None

	def draw(self, screen):
		screen.blit(self,(self.playerRect.left, self.playerRect.top))
		#Drawing all the bullets of the player 
		for bullet in self.bullets:
			bullet.draw(screen) #Drawing the bullet 

	def update(self, keys):

		self._movePlayer(keys)
		self._check_boundaries()

		#Checking the boundaries of the bullet before updating them 


		#Updating the Bullets 
		for bullet in self.bullets:
			bullet.update()
		pass
	def _movePlayer(self, keys):

		#Move Left
		if keys[pygame.K_a]:
			self.playerRect.left -= self.speed
		#move Right
		if keys[pygame.K_d]:
			self.playerRect.left += self.speed

		if keys[pygame.K_SPACE ]:
			self.bullets.append(Bullet(self.playerRect.left, self.playerRect.top)) #Creating Bullets 
		pass 

	def _check_boundaries(self): 

		posX = self.playerRect.left

		if posX >= self.screenW: 
			self.playerRect.left = self.playerRect.width

		if posX <= 0: 
			self.playerRect.left = self.screenW 


		pass 


class Game:

	def __init__(self, width = 800, height = 600): 
		self.__screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Shooter Game")

		self.main_player = Player(self.__screen.get_width(), self.__screen.get_height()) #Creating the Main Player 
		pass

	def start(self):
			
		isOver = False
		while not isOver:
			
			#Event Loop Handler 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					isOver = True

			self.__screen.fill(WHITE)

			self.update() #Updating all Components in the Game 

			self.draw() #Drawing all components in the Game 

			pygame.display.update() #Updating all display modules 

		pygame.quit() #Quit Pygame 
		pass

	def draw(self):
		#Drawing the Main Player 
		self.main_player.draw(self.__screen)
		pass
	def update(self):
		#Updating the Main Player
		keys = pygame.key.get_pressed() #Getting a List of all boolean values of all keys  
		self.main_player.update(keys)

	pass



def main():
	shooterGame = Game()
	shooterGame.start() 
	pass 


if __name__ == "__main__":
	main()