import pygame
import random

"""
	Use Neuro Symbolic AI IN game to play and beat the game 
	Things Todo:
		- Finish a Enemy Class to beat the game  

		- Delete the little enemies when they touch the floor end game (END THE GAME )

		- Make the game fully work (End game if enemy hit floor or if main_enemy health 0 )

		- Add the Ai so that it can play the game using NEAT (Neuro Evolution of Augmenting Toplogies)

		- Make it so that The player has to reload etc ...
		- Add sprites So the game looks Nicer (Kinda Done) Need to do it for the player as well 
		- Make it so that if a alien Touches the floor you lose
		- Add States To have a start Menu ??  (Use a stack to hold the states) win, lost etc 
		- REASON I was getting a weird error when I was displaying my enemy class 
		is because i didnt initialize the super class (pygame.Surface)

"""

pygame.init() #Initializing all modules in pygam e

#RGB
WHITE = (255,255,255)
PURPLE = (200, 100, 250)
BLUE = (0, 100, 200)
GREEN = (0,255,100)
RED = (255, 0,0)
BLACK = (0,0,0)


#Simple Collision Detector 
class CollisionDetection:
	
	def __init__(self, first, second):
		self.first = first
		self.second = second
		pass
		#First surface to check for 
	#Second surface to check for 
	def checkForCollision(self):
		
		isColliding = False #Initially False 

		#Getting the positions of the first and second surfaces 
		firstX = self.first.playerRect.left
		firstY = self.first.playerRect.top

		secondX = self.second.playerRect.left
		secondY = self.second.playerRect.top

		#Getting HalfSizes of first and second Surfaces 
		firstHalfSize = (self.first.get_width()  / 2, self.first.get_height() / 2)
		secondHalfSize = (self.second.get_width() /2, self.second.get_height()/ 2)


		#Getting the Center of the Surfaces 
		firstCenter = (firstX - firstHalfSize[0], firstY - firstHalfSize[1])
		secondCenter = (secondX - secondHalfSize[0], secondY - secondHalfSize[1])

		#Calculating the Distance between both centers 
		deltaX = abs(firstCenter[0] - secondCenter[0])
		deltaY = abs(firstCenter[1] - secondCenter[1])

		intersectX = deltaX - (firstHalfSize[0] + secondHalfSize[0])
		intersectY = deltaY - (firstHalfSize[1] + secondHalfSize[1])

		#If these statements true then colliding 
		if intersectX < 0 and intersectY < 0:
			isColliding = True

		return isColliding 
	pass

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
		self.playerRect = pygame.Rect(playerX, playerY, width, height)

		red = random.randint(0, 255)
		green = random.randint(0,255)
		blue = random.randint(0,255)


		self.fill((red,green,blue)) #Purple Bullets
		self.speed = 20 #Speed of the bullets
		self.active = True #Determines if the Bullet should be active or not

	#Draws the Bullet onto the screen
	def draw(self, screen):
		screen.blit(self, (self.playerRect.left, self.playerRect.top))
		pass

	#Updates the Bullets
	def update(self):
		self._check_boundaries() #Checking if its still within boundary

		if self.active:
			self._moveBullets() #Moving the Bullets Up

		pass

	#Checks if the bullet has passed a certain boundary
	def _check_boundaries(self):
		posY = self.playerRect.top

		if posY <= 0:
			#STOP
			self.active = False #Turn it off

		pass

	#Moves the Bullets Up
	def _moveBullets(self):
		self.playerRect.top -= self.speed
		pass

	pass

#Creating the enemy class its going to be a space ship 
#The surface is going to be the hitbox for the image 
#GOING TO USE THIS SAME CLASS FOR THE LITTLE ENEMIES :) 
class Enemy(pygame.Surface):
	def __init__(self, screenW, screenH, image,hurtImage, direction = "SIDE", width = 150, height = 150, speed = 1, health = 1000):

		#Very important 
		super().__init__((width,height))

		#Saving the Dimensions of the screen 
		self.screenW = screenW 
		self.screenH = screenH 

		#left top width height 
		startPosX = random.randint(0,screenW) #Randomly Selecting the X Position 
		startPosY = 0
		self.image = image #Saving the Image in the object variable #Which is the actual enemy 
		self.hurtImage = hurtImage #Saving the Hurt Image 

		self.image = pygame.transform .scale(self.image,(width,height))
		self.hurtImage = pygame.transform.scale(self.hurtImage, (width, height))

		#Saving the info of the enemy in a playerRect 
		self.playerRect = pygame.Rect(startPosX, startPosY, width, height)

		#Speed of the Enemy 
		self.__speed = speed
		self.isRight = True #Initially the Direction of the Enemy is Right 

		self.health = health #Health of the enemy To win the game 
		self.currentlyHit = False #Determines if we should switch animation when hit 
		self.direction = direction #Saving the direction in which we want to move the enemy 

		self.active = True #Dertermines if the Enemy should be alive or not 

	def draw(self, screen):

		#Displaying the Surface to the screen 
		screen.blit(self,(self.playerRect.left, self.playerRect.top))

		if self.currentlyHit == False: 
			#Displaying the Sprite on to the this->surface 
			screen.blit(self.image,(self.playerRect.left, self.playerRect.top))
		elif self.currentlyHit == True:
			#Displaying the Hurt animation on to the this->surface 
			screen.blit(self.hurtImage,(self.playerRect.left, self.playerRect.top))
			self.currentlyHit = False 
		pass
	#Will update the 
	def update(self, dt):
		#Calling the Move Method 
		self.__move(dt)
		#Checking the Boundaries and determining the direction 
		self.__checkBoundaries()
		pass 
	#Move the Enemy Right to left Every second increase its Speed 
	def __move(self, dt):

		if self.direction == "SIDE":
			#If the direction of the enemy is to the right move the enemy to the right 
			if self.isRight == True: 
				self.playerRect.left += self.__speed * dt
				#Else the direction is to the left 
			else:
				self.playerRect.left -= self.__speed * dt 
		
		#Move Enemy DOWN 
		elif self.direction == "DOWN":
			#Move the enemy down 
			self.playerRect.top += self.__speed * dt

		pass
	#Determines the direction of the Enemy based on its position 
	def __checkBoundaries(self):
		if self.direction == "SIDE":
			if self.playerRect.left > (self.screenW - self.playerRect.width):
				self.isRight = False #Go Left
			if self.playerRect.left <= 0: 
				self.isRight = True #Go Right

		elif self.direction == "DOWN":
			if self.playerRect.top >= self.screenH - self.playerRect.width:
				self.active = False #Kill the enemy 

	#Methods Runs when Enemy Hit 
	def hit(self):
		self.health -= 1 #Subbing one from the enemies health 
		self.currentlyHit = True #Currently Hit 

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
		#Checking if we need to delete the bullets
		for bullet in self.bullets:
			if bullet.active == False:
				self.bullets.remove(bullet) #Remove this bullet  

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
		
		#Creating the Main Enemy 
		self.main_enemy = Enemy(self.__screen.get_width(), self.__screen.get_height(), pygame.image.load("spaceship.png"), pygame.image.load("red.png"))
		
		#Creating the Score board of the game 
		self.__font = pygame.font.Font("FreeSansBold.ttf", 64)
		#Color, background color = 
		self.__score = self.__font.render(str(self.main_enemy.health), True,PURPLE, BLACK)
		self.__scorePos = (1100,300)

		self.__enemies = [] #Empty List Initially 
		self.__enemyTimer = 500 #Spawn enemies Every 3 Seconds 

		self.__enemyCounter = 0.0 #Helps keep track of how many enemies spawning 
		self.__seconds = 0.0 #Keeps track of the number of seconds that passed 

		self.__enemySpeed = .1 #Speed of the little enemies 
		pass

	def start(self):

		isOver = False
		clock = pygame.time.Clock()

		start_ticks=pygame.time.get_ticks() #starter tick


		while not isOver:
			dt = clock.tick(60) #COntrols the Speed of the Game
			#Event Loop Handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					isOver = True

			self.__screen.fill(WHITE)

			#self.__seconds = (pygame.time.get_ticks()-start_ticks)/1000 #Keeps track of the seconds that passed
			self.__enemyCounter += dt

			self.collisionDetection() #Checking if Collision is Occuring
			self.update(dt) #Updating all Components in the Game
			self.spawnEnemies() #Spawns the Enemies 
			self.draw() #Drawing all components in the Game

			pygame.display.update() #Updating all display modules

		pygame.quit() #Quit Pygame
		pass

	def draw(self):
		#Drawing the Background of the game 
		self.__screen.blit(self.__backgroundImage, (0,0))
		#Drawing the Main Player
		self.main_player.draw(self.__screen)

		#Drawing the Main Enemy 
		self.main_enemy.draw(self.__screen)

		#Drawing the Score onto the screen 
		self.__screen.blit(self.__score,self.__scorePos)

		#Drawing all the enemies to the screen 
		for enemy in self.__enemies:
			enemy.draw(self.__screen)
		pass
	def update(self, dt):
		#Updating the Main Player
		keys = pygame.key.get_pressed() #Getting a List of all boolean values of all keys

		#Updating the Main player 
		self.main_player.update(keys, dt)

		#Updating the Main Enemy 
		self.main_enemy.update(dt)

		#Updates the Score 
		self.__score = self.__font.render(str(self.main_enemy.health), True, PURPLE, BLACK) 

		#Updating all the Enemies to the screen 
		for enemy in self.__enemies:
			enemy.update(dt)
			#Checking if we need to delete the little Enemies 
			if enemy.health <= 0:
				self.__enemies.remove(enemy) #Delete the little Enemy its health is 

		#

	#Spawns the Little Enemies to the screen 
	def spawnEnemies(self):
		if self.__enemyCounter >= self.__enemyTimer:
			#Spawn Enemy 
			self.__enemies.append(Enemy(self.__screen.get_width(), self.__screen.get_height(), pygame.image.load("spaceship.png"), pygame.image.load("red.png"), "DOWN", 40,40, self.__enemySpeed, 1))
			self.__enemyCounter = 0.0 #Resetting the Counter 

		pass

	#Checks if anything is colliding with another thing 
	def collisionDetection(self):
		#Checking if the bullets are colliding with the enemy 
		for bullet in self.main_player.bullets:
			detector = CollisionDetection(bullet, self.main_enemy)
			if detector.checkForCollision():
				bullet.active = False #Deleting the Bullet 
				self.main_enemy.hit() #Telling the Enemy it got hit
				pass
			#Collision Detection for Little Enemies and Bullet  NESTED FORLOOP 
			for enemy in self.__enemies: 
				enemyDetector = CollisionDetection(enemy, bullet)
				#Active Bullet
				if bullet.active == True and enemyDetector.checkForCollision() == True:
					bullet.active = False #Deleting the Bullet 
					enemy.hit() #Telling the Enemy it got hit 



			pass
		 



def main():
	shooterGame = Game()
	shooterGame.start()
	pass 


if __name__ == "__main__":
	main()
