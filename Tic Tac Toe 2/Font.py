import pygame

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path, size, rep_color=False):
        self.default_color = rep_color
        self.spacing = 5
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','.','?','!',',','[',']',':']
        font_img = pygame.image.load(path).convert_alpha()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())

                new_img = pygame.Surface(char_img.get_size(), pygame.SRCALPHA).convert_alpha()

                # Loop through each pixel in the image
                for x in range(char_img.get_width()):
                    for y in range(char_img.get_height()):
                        # Get the color of the current pixel
                        color = char_img.get_at((x, y))

                        # Check if the current pixel is black
                        if color != (0, 0, 0, 255):  # RGB value for fully opaque black
                            # Copy the non-black pixel to the new image
                            new_img.set_at((x, y), self.default_color if self.default_color else color)

                # Use the new image for further processing or display
                char_img = new_img

                self.characters[self.character_order[character_count]] = pygame.transform.scale_by(char_img.copy(), size)
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width() - 15

    def render(self, surf, text, loc, color=None):
        char_surfaces = []  # List to store individual character surfaces

        x_offset = 0
        for char in text:
            if char != ' ':
                char_img = self.characters[char.upper()]
                if color:
                   char_img = self.change_color(char_img, color)
                char_surfaces.append(char_img)  # Append each character surface to the list
                x_offset += char_img.get_width() + self.spacing
            else:
                char_surfaces.append(' ')
                x_offset += self.space_width + self.spacing

        # Calculate the dimensions of the rendered text
        text_width = x_offset - self.spacing
        text_height = max(char.get_height() for char in char_surfaces if char != ' ')

        # Create the text surface with the final dimensions
        text_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA).convert_alpha()

        # Blit each character surface onto the text surface
        x_offset = 0
        for char_surface in char_surfaces:
            if char_surface != ' ':
                text_surface.blit(char_surface, (x_offset, 0))
                x_offset += char_surface.get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

        text_rect = text_surface.get_rect(center=(loc[0], loc[1]))

        # Blit the text surface onto the screen
        surf.blit(text_surface, text_rect)

    def change_color(self, img, color):
        new_img = img.copy()
        mask = pygame.mask.from_surface(new_img).to_surface()
        mask.set_colorkey((0, 0, 0))
        colored = pygame.Surface(new_img.get_size())
        colored.fill(color)
        mask.blit(colored, (0, 0), None, pygame.BLEND_RGBA_MULT)
        return mask
