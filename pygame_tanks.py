import pygame
from pygame.locals import *
import math
import sys
pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pygame Tank Trouble')

#define game variables
tile_size = 40

#load images
#sun_img = pygame.image.load('img/sun.png')
#bg_img = pygame.image.load('img/sky.png')

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



# Initialize Pygame
pygame.init()

# Define colors
GRAY = (169, 169, 169)

# Create a Pygame screen


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle,playerpick):
        super().__init__()
        
        self.radius = 5  # Radius of the circle
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        self.color = GRAY  # Color of the circle
        self.speed = 0.2
        self.x = x
        self.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        self.angle = math.radians(angle)  # Convert angle to radians
        self.playerpick = playerpick
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        
        self.rect.center = (x, y)
        
    def update(self):
        # Update the projectile's position based on its speed and angle

        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))
        self.x +=self.speed * math.cos(self.angle)
        self.y -=self.speed * math.sin(self.angle)
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        # This section allows me to use speeds below 1
        for wall in world.tile_list:
            if self.rect.colliderect(wall[1]):
                # Handle collision here
                # For example, reverse the x-velocity to bounce off horizontally
                self.speed = (-self.speed)

            if self.rect.colliderect(self.playerpick):
                sys.exit(f"{self.playerpick} wins")
            #if self.rect.colliderect(player2):
             #   print("Player1 wins")
                

class Player():
    def __init__(self, x, y, img):
        img = pygame.image.load(img)
        self.original_image = pygame.transform.scale(img, (35, 35))
        self.rect = self.original_image.get_rect()
        self.x = x  # Use float for position
        self.y = y
        self.speed = 0.2  # Adjust the speed as needed
        self.angle = 0
        self.angle_rot = 0.3
        self.width = self.rect.width
        self.height = self.rect.height
        self.shot = False
        self.name = "Player 1"
        # Pre-render images for different angles
        self.images = []
        for angle in range(0, 360, 2):  # Adjust the step as needed
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            self.images.append(rotated_image)
        self.image_index = 0  # Index of the current image
    def __str__(self):
        return self.name
    def update(self):
        # Update the player's position using floating-point coordinates
        keys = pygame.key.get_pressed()
        move_speed = self.speed

        # Calculate the movement in both x and y directions based on the angle
        x = move_speed * math.cos(math.radians(self.angle))
        y = move_speed * math.sin(math.radians(self.angle))
        dx = 0
        dy = 0
        dz = 0
        if keys[pygame.K_w]:
            dx -= x
            dy += y  # Reverse dy to move down
        if keys[pygame.K_s]:
            dx += x
            dy -= y  # Reverse dy to move up
        if keys[pygame.K_a]:
            self.angle += self.angle_rot
        if keys[pygame.K_d]:
            self.angle -= self.angle_rot
        if keys[pygame.K_SPACE] and self.shot == False:
        # Create a new projectile at the player's position, moving upwards
            new_projectile = Projectile(self.x+35, self.y+17.5, angle=self.angle-180,playerpick=player2)
            projectiles.add(new_projectile)
            self.shot = True
        if keys[pygame.K_SPACE]==False:
            self.shot = False
            #dx -= x
            #dy += y  # Reverse dy to move down
        
        self.angle %= 360

        # Limit the tank's position to the screen boundaries (optional)
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

        # Check for collision with tiles
        for tile in world.tile_list:
            if tile[1].colliderect(self.x+dx, self.y, self.width, self.height):
                # If a collision occurs, revert to the previous position
                dx = 0
            elif tile[1].colliderect(self.x, self.y+dy, self.width, self.height):
                dy = 0
                
        self.x += dx
        self.y += dy
        
        # Update the current image based on angle
        self.image_index = int(self.angle / 2)  # Adjust the divisor based on image angles

    def draw(self, screen):
        # Draw the tank at the rounded integer position
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        if 0 <= self.image_index < len(self.images):
            screen.blit(self.images[self.image_index], self.rect)

        projectiles.update()
        projectiles.draw(screen)
        #wpygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class Player2():
    def __init__(self, x, y, img):
        img = pygame.image.load(img)
        self.original_image = pygame.transform.scale(img, (35, 35))
        self.rect = self.original_image.get_rect()
        self.x = x  # Use float for position
        self.y = y
        self.speed = 0.2  # Adjust the speed as needed
        self.angle = 0
        self.angle_rot = 0.3
        self.width = self.rect.width
        self.height = self.rect.height
        self.shot = False
        self.name = "Player 2"
        # Pre-render images for different angles
        self.images = []
        for angle in range(0, 360, 2):  # Adjust the step as needed
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            self.images.append(rotated_image)
        self.image_index = 0  # Index of the current image
    def __str__(self):
        return self.name
        
        
        

    def update(self):
        # Update the player's position using floating-point coordinates
        keys = pygame.key.get_pressed()
        move_speed = self.speed

        # Calculate the movement in both x and y directions based on the angle
        x = move_speed * math.cos(math.radians(self.angle))
        y = move_speed * math.sin(math.radians(self.angle))
        dx = 0
        dy = 0
        dz = 0
        if keys[pygame.K_UP]:
            dx -= x
            dy += y  # Reverse dy to move down
        if keys[pygame.K_DOWN]:
            dx += x
            dy -= y  # Reverse dy to move up
        if keys[pygame.K_LEFT]:
            self.angle += self.angle_rot
        if keys[pygame.K_RIGHT]:
            self.angle -= self.angle_rot
        if keys[pygame.K_m] and self.shot == False:
        # Create a new projectile at the player's position, moving upwards
            new_projectile = Projectile(self.x+35, self.y+17.5, angle=self.angle-180,playerpick=player)
            projectiles.add(new_projectile)
            self.shot = True
        if keys[pygame.K_m]==False:
            self.shot = False
            #dx -= x
            #dy += y  # Reverse dy to move down
        
        self.angle %= 360

        # Limit the tank's position to the screen boundaries (optional)
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

        # Check for collision with tiles
        for tile in world.tile_list:
            if tile[1].colliderect(self.x+dx, self.y, self.width, self.height):
                # If a collision occurs, revert to the previous position
                dx = 0
            elif tile[1].colliderect(self.x, self.y+dy, self.width, self.height):
                dy = 0
                
        self.x += dx
        self.y += dy
        
        # Update the current image based on angle
        self.image_index = int(self.angle / 2)  # Adjust the divisor based on image angles

    def draw(self, screen):
        # Draw the tank at the rounded integer position
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        if 0 <= self.image_index < len(self.images):
            screen.blit(self.images[self.image_index], self.rect)
        projectiles.update()
        projectiles.draw(screen)
        #wpygame.draw.rect(screen, (255, 255, 255), self.rect, 2)







class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		black_img = pygame.image.load('black.jpg')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(black_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)

				col_count += 1
			row_count += 1

	def draw(self):
         for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1],2)
#need multiple maps and a random selection or picked by user


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1,1, 1, 0, 0, 0,0, 0, 0, 1, 1,1, 0, 0, 1, 0, 0], 
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
[1, 1, 0, 0, 1,1, 1, 0, 1, 0,0, 0, 0, 0, 0,1, 0, 0, 1, 1, 1], 
[1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1], 
[1, 1, 0, 0, 1,1, 1, 1, 1, 0,0, 0, 0, 1, 0,1, 0, 0, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 1, 0, 0, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
projectiles = pygame.sprite.Group()
player = Player(400, 400,"tank2.png")
player2 = Player2(450, 400,"tank2.png")

world = World(world_data)

running = True
while running:

    
    screen.fill("white")
    
    world.draw()
    player.update()
    player.draw(screen)
    player2.update()
    player2.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
    	    if event.type == pygame.QUIT:
	            running = False
    

pygame.quit()