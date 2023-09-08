import pygame
from PIL import Image
import sys
pygame.init()

screen_width = 800
screen_height = 800


# Create a purple image
width, height = 200, 200  # Specify the width and height of the image
purple_colour = (128, 0, 128)  # RGB color for purple
green_colour = (0, 128, 0)
# Create a new image with the specified size and fill it with the purple color
endgoal = Image.new("RGB", (width, height), purple_colour)
image2 = Image.new("RGB", (width, height), green_colour)
# Save the image to a file
endgoal.save("purple_image.png")
image2.save("green_img.png")


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pygame maze')

#define game variables
tile_size = 40


game_over = False # preset the game as running
#load images
#sun_img = pygame.image.load('img/sun.png')
#bg_img = pygame.image.load('img/sky.png')

def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
    def __init__(self,x,y,img):
        img = pygame.image.load(img)
        self.color = (0, 128, 0)  # RGB color for purple
        self.rect = pygame.Rect(x, y, 35, 35)
        self.image = pygame.transform.scale(img, (35, 35))
        self.x = x  # Use float for position
        self.y = y
        self.speed = 0.2  
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def update(self):
        # Update the player's position 
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            
        # Limit the tank's position to the screen boundaries (optional) will probs remove this
        self.x = max(0, min(self.x, screen_width - self.rect.width))
        self.y = max(0, min(self.y, screen_height - self.rect.height))
        
        for tile in world.tile_list:
            if tile.colliderect(self.x+dx,self.y,self.width,self.height):  
                # Adjust player's position to prevent overlapping
                dx = 0
            elif tile.colliderect(self.x,self.y+dy,self.width,self.height):#
                dy = 0
            elif pygame.sprite.spritecollide(self, end_square, False):
                sys.exit()
             #pygame.quit()
        
        self.x +=dx
        self.y +=dy
            
    def draw(self, screen):

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect,2)
 


class World():
	def __init__(self, data):
		self.tile_list = []
        
		#load images

		wall_colour = (0,0,0)
        
                      #      rect = pygame.Rect(col_count * tile_size,row_count * tile_size,tile_size,tile_size) 
                    #pygame.draw.rect(screen, wall_color, rect)
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					rect = pygame.Rect(col_count * tile_size,row_count * tile_size,tile_size,tile_size)
					self.tile_list.append(rect)
				if tile == 3:
					end = End(col_count * tile_size, row_count * tile_size)
					end_square.add(end)
                    
                    
                    

				col_count += 1
			row_count += 1
            
	def draw(self):
         for tile in self.tile_list:
            wall_colour = (0,0,0)
            pygame.draw.rect(screen, wall_colour, tile)
            pygame.draw.rect(screen, (255, 255, 255), tile,2)
#need multiple maps and a random selection or picked by user
class End(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('purple_image.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = pygame.Rect(tile_size, tile_size,tile_size,tile_size)
		self.rect.x = x
		self.rect.y = y


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
end_square = pygame.sprite.Group()
player = Player(40, 40,"green_img.png")
world = World(world_data)
#pygame.draw.circle(screen, "red", (400,400), 20)

# 3 Main functions
def create_world():
    screen.fill("white")
    world.draw()
def create_player():
    player.update()
    player.draw(screen)
def create_end_point():
    end_square.draw(screen)
    pygame.display.update()
def main():


    running = True
    while running:
     
        create_world()
        create_player()
        create_end_point()
   
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        

    pygame.quit()

if __name__ == "__main__":
    main()