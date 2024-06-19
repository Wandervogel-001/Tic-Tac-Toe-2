from Font import*

class Button(pygame.sprite.Sprite):
	def __init__(self, name, loc, size, add_line=False):
		super().__init__()
		self.add_line = add_line
		self.size = size
		self.name = name
		self.width = 25 * size
		self.height = 7 * size
		self.x_pos = loc[0]
		self.y_pos = loc[1]
		self.color = '#d1a67e'
		self.pressed = False

	def draw(self, surface, font, move=False):
		px = self.size
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill('#654053')
		self.rect = self.image.get_rect()
		self.rect.center = [self.x_pos, self.y_pos]
		surface.blit(self.image, self.rect)
		
		if self.add_line:
			pygame.draw.line(surface, '#654053', (self.x_pos - (self.width//2), self.rect.bottom + (self.size+2)), (self.x_pos + (self.width//2), self.rect.bottom + (self.size+2)), int(self.size))
		
		font.render(surface,self.name, (self.rect.centerx, self.rect.centery + (0.6*px)), self.color)
		
		if move:
			subsurface1 = move[0].subsurface(move[1])
			subsurface2 = subsurface1.subsurface(self.rect)
			relative_pos = subsurface2.get_abs_offset()
			self.rect = self.rect.move_to(topleft=(relative_pos[0], relative_pos[1]))

	def hover(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.color = '#865f60'
		else:
			self.color = '#d1a67e'

	def click(self):
		mouse_button = pygame.mouse.get_pressed()
		if mouse_button[0] == 1:
			mouse_pos = pygame.mouse.get_pos()
			if self.rect.collidepoint(mouse_pos):
				self.pressed = True

	def update(self, surface, font, move=False):
		self.draw(surface, font, move)
		self.hover()
		self.click()