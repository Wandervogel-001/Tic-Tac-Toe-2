from Settings import*
import traceback

class GameManager:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen_center_x = self.screen_width // 2
        self.screen_center_y = self.screen_height // 2
        self.size = SIZE

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Tic Tac Toe')
        self.clock = pygame.time.Clock()
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.set_screen()
        pygame.mouse.set_visible(False)

        self.set_imgs()

        self.click_sound = load_audio('click.wav')
        bg_music = load_audio('music.ogg')
        bg_music.set_volume(MUSIC_VOLUME)
        bg_music.play(loops=-1)

        self.lose_sound = load_audio('lose.wav')
        self.win_sound = load_audio('victory.wav')
        self.play_sound = True

        self.option = False

        self.fade_start_time = None
        self.fade_duration = 1000
        self.fade_alpha = 0
        self.fade_in_active = True
        self.fade_out_active = True

        self.startup = True
        self.startup_time = None

        self.menu = 1
        self.mode = 1
        self.game_active = False
        self.menu_active = True
        self.name = None
        self.current_player = 1
        self.board = [' '] * 9
        self.difficulty = None
        self.computer_symbol = None
        self.player_symbol = None
        self.thinking_delay = THINKING_DELAY

        self.fullscreen = False

    def set_screen(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

    def set_imgs(self):
        try:
            alpha = [
            self.window_img.get_alpha(),
            self.window_img_2.get_alpha(),
            self.window_img_3.get_alpha(),
            self.window_img_4.get_alpha(),
            self.board_img.get_alpha(),
            ]
        except:
            alpha = [0,0,0,0,0]
        
        px = self.size

        self.font = Font("images/font.png", self.size, '#d1a67e')

        self.menu_image = load_image('menu.png', self.size)
        self.menu_rect = self.menu_image.get_rect()
        self.menu_rect.center = [self.screen_center_x,self.screen_center_y]

        max_size = self.monitor_size[1] / 114
        nb = 0.8 * (self.size - 5) / (max_size - 5)
        self.cursor_image = load_image("cursor.png", self.size-(2.2 + nb))

        self.window_img = load_image('window.png', self.size)
        self.window_rect = self.window_img.get_rect()
        self.window_center_x = self.window_img.get_width() // 2
        self.window_rect.center = [self.screen_center_x,self.screen_center_y + (4*px)]
        self.window_img.set_alpha(alpha[0])

        self.window_img_2 = load_image('window_2.png', self.size)
        self.window_rect_2 = self.window_img_2.get_rect()
        self.window2_center_x = self.window_img_2.get_width() // 2
        self.window_rect_2.center = [self.screen_center_x,self.screen_center_y + (7*px)]
        self.window_img_2.set_alpha(alpha[1])

        self.window_img_3 = self.window_img.copy()
        self.window_img_3.set_alpha(alpha[2])
        self.window_img_4 = self.window_img.copy()
        self.window_img_4.set_alpha(alpha[3])

        self.board_img = load_image('board.png', self.size)
        self.board_rect = self.board_img.get_rect()
        self.board_rect.center = [self.screen_center_x,self.screen_center_y]
        self.board_img.set_alpha(alpha[4])

        self.rectangle_img = load_image('rectangle.png', self.size)
        self.board_rects = [
            self.rectangle_img.get_rect(center=(self.screen_center_x-(19*px), self.screen_center_y+(25.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x, self.screen_center_y+(25.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x+(19*px), self.screen_center_y+(25.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x-(19*px), self.screen_center_y+(6.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x, self.screen_center_y+(6.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x+(19*px), self.screen_center_y+(6.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x-(19*px), self.screen_center_y-(12.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x, self.screen_center_y-(12.6*px))),
            self.rectangle_img.get_rect(center=(self.screen_center_x+(19*px), self.screen_center_y-(12.6*px))),
        ]

        self.x_img = load_image('x.png',self.size)
        self.o_img = load_image('o.png',self.size)

        self.ryo_surface = load_image("RYO.png", 5.7)
        self.ryo_rect = self.ryo_surface.get_rect(center=(self.screen_center_x, self.screen_center_y-45))
        self.made_by_pygame = load_image("pygame.png", 4.7)
        self.made_by_pygame_rect = self.made_by_pygame.get_rect(center=(self.screen_center_x, self.screen_height-50))

        self.init_buttons()

    def init_buttons(self):
        px = self.size
        self.play_button = Button('play', (self.screen_center_x +(0.4*px), self.screen_center_y + px), self.size, True)
        self.quit_button = Button('quit', (self.screen_center_x +(0.4*px), self.screen_center_y + ((10*px)+px)), self.size, True)
        self.play1_button = Button('play', ((self.window_rect.width//2), (self.window_rect.height//2)-(4*px)), self.size)
        self.quit1_button = Button('quit', ((self.window_rect.width//2), (self.window_rect.height//2)+(5*px)), self.size)
        self.pvc_button = Button('Vs Ai', ((self.window_rect.width//2), (self.window_rect.height//2)-(4*px)), self.size)
        self.pvp_button = Button('PVP', ((self.window_rect.width//2), (self.window_rect.height//2)+(5*px)), self.size)
        self.easy_button = Button('easy', ((self.window_rect_2.width//2), (self.window_rect_2.height//2)-(13*px)), self.size)
        self.med_button = Button('Med', ((self.window_rect_2.width//2), (self.window_rect_2.height//2)-(4*px)), self.size)
        self.tuff_button = Button('Tuff', ((self.window_rect_2.width//2), (self.window_rect_2.height//2)+(5*px)), self.size)
        self.hard_button = Button('Hard', ((self.window_rect_2.width//2), (self.window_rect_2.height//2)+(14*px)), self.size)
        self.x_button = Button('X', ((self.window_rect.width//2), (self.window_rect.height//2)-(4*px)), self.size)
        self.o_button = Button('O', ((self.window_rect.width//2), (self.window_rect.height//2)+(5*px)), self.size)

    def fade_out_surface(self, surface, rect):
        if self.fade_out_active:
            self.fade_out(surface)
            if surface.get_alpha() == 0:
                self.fade_out_active = False

        if surface.get_alpha() > 0:
            self.screen.blit(surface, rect)

    def fade_in_surface(self, surface, rect):
        if self.fade_in_active:
            self.fade_in(surface)
            if surface.get_alpha() == 255:
                self.fade_in_active = False

        if surface.get_alpha() > 0:
            self.screen.blit(surface, rect)

    def fade_out(self, surface):
        if self.fade_start_time is None:
            self.fade_start_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - self.fade_start_time
        if elapsed_time >= self.fade_duration:
            self.fade_start_time = None
            self.fade_alpha = 0
            surface.set_alpha(self.fade_alpha)
            return

        self.fade_alpha = 255 - int((elapsed_time / self.fade_duration) * 255)
        surface.set_alpha(self.fade_alpha)

    def fade_in(self, surface):
        if self.fade_start_time is None:
            self.fade_start_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - self.fade_start_time
        if elapsed_time >= self.fade_duration:
            self.fade_start_time = None
            self.fade_alpha = 255
            surface.set_alpha(self.fade_alpha)
            return

        self.fade_alpha = int((elapsed_time / self.fade_duration) * 255)
        surface.set_alpha(self.fade_alpha)

    def draw_startup(self):
        if self.startup_time is None:
            self.startup_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - self.startup_time

        self.screen.fill("#654053")
        self.fade_in_surface(self.ryo_surface, self.ryo_rect)
        self.fade_in_surface(self.made_by_pygame, self.made_by_pygame_rect)
        if elapsed_time > 1800:
            self.fade_out_surface(self.ryo_surface, self.ryo_rect)
            self.fade_out_surface(self.made_by_pygame, self.made_by_pygame_rect)
            if self.ryo_surface.get_alpha() == 0:
                self.fade_duration = FADE
                self.startup = False

    def draw_start_menu(self):
        self.play_button.update(self.screen, self.font)
        self.quit_button.update(self.screen, self.font)
        if not self.option:
            self.fade_out_surface(self.window_img,self.window_rect)

    def draw_mode_menu(self):
        px = self.size
        self.font.render(self.window_img, 'Play', (self.window_center_x,(5*px)))
        self.pvc_button.update(self.window_img,self.font, (self.screen,self.window_rect))
        self.pvp_button.update(self.window_img,self.font, (self.screen,self.window_rect))
        self.fade_in_surface(self.window_img,self.window_rect)
        if self.mode == 1:
            self.fade_out_surface(self.board_img, self.board_rect)
        elif self.mode == 2:
            self.fade_out_surface(self.window_img_2,self.window_rect_2)

    def draw_difficulty_menu(self):
        px = self.size
        self.font.render(self.window_img_2, 'Vs AI', (self.window_center_x,(5*px)))
        self.easy_button.update(self.window_img_2,self.font, (self.screen,self.window_rect_2))
        self.med_button.update(self.window_img_2,self.font, (self.screen,self.window_rect_2))
        self.tuff_button.update(self.window_img_2,self.font, (self.screen,self.window_rect_2))
        self.hard_button.update(self.window_img_2,self.font, (self.screen,self.window_rect_2))
        self.fade_in_surface(self.window_img_2,self.window_rect_2)
        self.fade_out_surface(self.window_img_3, self.window_rect)

    def draw_symbol_menu(self):
        px = self.size
        self.window_img_3 = load_image('window.png', self.size)
        self.font.render(self.window_img_3, self.name, (self.window_center_x,(5*px)))
        self.x_button.update(self.window_img_3,self.font, (self.screen,self.window_rect))
        self.o_button.update(self.window_img_3,self.font, (self.screen,self.window_rect))
        self.fade_in_surface(self.window_img_3, self.window_rect)
        self.fade_out_surface(self.board_img, self.board_rect)

    def draw_rectangles(self):
        mouse_pos = pygame.mouse.get_pos()
        for rect in self.board_rects:
            if rect.collidepoint(mouse_pos):
                self.screen.blit(self.rectangle_img, rect)

    def draw_board(self):
        px = self.size
        self.fade_in_surface(self.board_img, self.board_rect)
        self.draw_rectangles()
        for i, symbol in enumerate(self.board):
            if symbol == 'X':
                self.screen.blit(self.x_img, self.board_rects[i])
            elif symbol == 'O':
                self.screen.blit(self.o_img, self.board_rects[i])
        if self.mode == 1:
            if self.current_player == 1:
                self.font.render(self.screen,"X Turn",(self.screen_center_x,self.screen_center_y-(31.6*px)))
            else:
                self.font.render(self.screen,"O Turn",(self.screen_center_x,self.screen_center_y-(31.6*px)))

    def draw_win_menu(self):
        px = self.size
        winner = check_winner(self.board)
        if self.mode == 2:
            if self.play_sound:
                if winner == self.player_symbol:
                    self.win_sound.play()
                    self.play_sound = False
                elif winner == self.computer_symbol:
                    self.lose_sound.play()
                    self.play_sound = False
        elif self.mode == 1:
            if self.play_sound and not(check_winner(self.board) == None):
                self.win_sound.play()
                self.play_sound = False

        if winner == 'X':
            winner = "X Won!"
        elif winner == 'O':
            winner = "O Won!"
        else:
            winner = "Draw!"

        self.screen.blit(self.board_img, self.board_rect)
        for i, symbol in enumerate(self.board):
            if symbol == 'X':
                self.screen.blit(self.x_img, self.board_rects[i])
            elif symbol == 'O':
                self.screen.blit(self.o_img, self.board_rects[i])

        if not self.fade_in_active and not self.fade_out_active:
            self.fade_in_active = True
            self.fade_out_active = True

        self.window_img_4 = load_image('window.png', self.size)
        self.font.render(self.window_img_4, winner, (self.window_center_x,(5*px)))
        self.play1_button.update(self.window_img_4,self.font, (self.screen,self.window_rect))
        self.quit1_button.update(self.window_img_4,self.font, (self.screen,self.window_rect))
        self.fade_in_surface(self.window_img_4,self.window_rect)

    def draw_menu(self):
        if self.menu == 1:
            self.draw_start_menu()
        elif self.menu == 2:
            self.draw_mode_menu()
        elif self.menu == 3:
            self.draw_difficulty_menu()
        elif self.menu == 4:
            self.draw_symbol_menu()

    def activate(self, button, mode=False, game_active=False):
        self.menu += 1
        if mode: self.mode = mode
        self.fade_out_active = False
        self.fade_in_active = True
        button.pressed = not button.pressed
        if game_active:
            self.menu_active = False
            self.game_active = True

    def deactivate(self, menu):
        self.menu_active = True
        self.menu = menu
        self.board = [' '] * 9
        self.current_player = 1
        self.fade_out_active = True
        self.fade_in_active = False
        self.game_active = False

    def reset_board(self):
        self.board = [' '] * 9
        self.current_player = 1

    def reset_game(self):
        if not self.menu_active and not self.game_active:
            self.reset_board()
            if self.quit1_button.pressed:
                self.game_active = False
                self.menu_active = True
                self.quit1_button.pressed = False
                self.window_img.set_alpha(0)
                self.window_img_2.set_alpha(0)
                self.window_img_3.set_alpha(0)
                self.window_img_4.set_alpha(0)
                self.board_img.set_alpha(0)
                self.mode = 1
                self.name = None
                self.difficulty = None
                self.computer_symbol = None
                self.player_symbol = None
                self.menu = 1
                self.play_sound = True
                self.option = True
            else:
                self.menu_active = False
                self.game_active = True

            self.fade_out_active = True
            self.fade_in_active = False
            if self.mode == 2 and self.player_symbol == 'O':
                self.current_player = 2
            else:
                self.current_player = 1

    def handle_moves(self, event):
        for i, rect in enumerate(self.board_rects):
            if self.mode == 1:
                if rect.collidepoint(event.pos) and self.board[i] == ' ':
                    self.board[i] = 'X' if self.current_player == 1 else 'O'
                    self.current_player = 3 - self.current_player
            if self.mode == 2:
                if self.current_player == 1:
                    if rect.collidepoint(event.pos) and self.board[i] == ' ':
                        self.board[i] = 'X' if self.player_symbol == 'X' else 'O'
                        self.current_player = 3 - self.current_player

    def handle_escape(self):
        if self.menu != 1:
            self.play_sound = True
            self.option = False
            if not self.menu_active:
                if self.menu == 5:
                    self.deactivate(4)
                else:
                    self.deactivate(2)
            else:
                self.menu -= 1
                self.fade_out_active = True
                self.fade_in_active = False

    def handle_buttons(self):
        if self.quit_button.pressed:
                pygame.quit()
                sys.exit()

        if self.play_button.pressed:
            self.menu += 1
            self.play_button.pressed = not self.play_button.pressed
            self.fade_out_active = False
            self.fade_in_active = True

        if self.pvc_button.pressed:
            if self.window_img.get_alpha() == 255:
                self.activate(self.pvc_button,2)
        if self.pvp_button.pressed:
            if self.window_img.get_alpha() == 255:
                self.activate(self.pvp_button,1,True)

        if self.easy_button.pressed:
            if self.window_img_2.get_alpha() == 255:
                self.activate(self.easy_button)
                self.name = 'Easy'
                self.difficulty = 1
        if self.med_button.pressed:
            if self.window_img_2.get_alpha() == 255:
                self.activate(self.med_button)
                self.name = 'Med'
                self.difficulty = 2
        if self.tuff_button.pressed:
            if self.window_img_2.get_alpha() == 255:
                self.activate(self.tuff_button)
                self.name = 'Tuff'
                self.difficulty = 3
        if self.hard_button.pressed:
            if self.window_img_2.get_alpha() == 255:
                self.activate(self.hard_button)
                self.name = 'Hard'
                self.difficulty = 4

        if self.x_button.pressed:
            if self.window_img_3.get_alpha() == 255:
                self.activate(self.x_button, game_active=True)
                self.player_symbol , self.computer_symbol = 'X', 'O'
                self.computer = Computer(self.player_symbol, self.computer_symbol, self.difficulty)
        if self.o_button.pressed:
            if self.window_img_3.get_alpha() == 255:
                self.activate(self.o_button, game_active=True)
                self.player_symbol , self.computer_symbol = 'O', 'X'
                self.computer = Computer(self.player_symbol, self.computer_symbol, self.difficulty)
                self.current_player = 2

        if self.play1_button.pressed:
            if self.window_img_4.get_alpha() == 255:
                self.reset_game()
                self.fade_out_active = False
                self.play1_button.pressed = False
                self.play_sound = True

        if self.quit1_button.pressed:
            if self.window_img_4.get_alpha() == 255:
                self.reset_game()

    def handle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen_width = self.monitor_size[0]
            self.screen_height = self.monitor_size[1]
            self.screen_center_x = self.screen_width // 2
            self.screen_center_y = self.screen_height // 2
            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
            self.size = min(self.screen_width / 64, self.screen_height / 114)
            self.set_imgs()
        else:
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
            self.screen_center_x = self.screen_width // 2
            self.screen_center_y = self.screen_height // 2
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            self.size = min(self.screen_width / 64, self.screen_height / 114)
            self.set_imgs()

    def handle_videoresize(self, event):
        if not self.fullscreen:
            self.screen_width, self.screen_height = event.size
            self.screen_center_x = self.screen_width // 2
            self.screen_center_y = self.screen_height // 2
            self.size = min(self.screen_width / 64, self.screen_height / 114)
            if self.size < 5:
                self.screen_width, self.screen_height = (SCREEN_WIDTH,SCREEN_HEIGHT)
                self.screen_center_x = self.screen_width // 2
                self.screen_center_y = self.screen_height // 2
                self.size = 5
                self.set_screen()
            self.set_imgs()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.handle_escape()

                if event.key == pygame.K_f:
                    if not self.startup:
                        self.handle_fullscreen()

            if event.type == pygame.VIDEORESIZE:
                self.handle_videoresize(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click_sound.play()
                if self.game_active:
                    self.handle_moves(event)

            self.handle_buttons()

    def draw_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            self.screen.blit(self.cursor_image, mouse_pos)

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f}'
        self.font.render(self.screen, fps, (35, 25))

    def update_screen(self):
        if self.startup:
            self.draw_startup()
        else:
            self.screen.fill("#654053")
            self.screen.blit(self.menu_image, self.menu_rect)
            
            if self.menu_active:
                self.draw_menu()
            else:
                if self.game_active:
                    if check_winner(self.board) or ' ' not in self.board[0:]:
                        self.game_active = False

                    self.draw_board()

                    if self.mode == 2 and self.current_player == 2 and self.thinking_delay > 0:
                        self.thinking_delay -= 1
                    elif self.mode == 2 and self.current_player == 2 and self.thinking_delay == 0:
                        if ' ' in self.board[0:] and not check_winner(self.board):
                            self.thinking_delay = THINKING_DELAY
                            self.computer.update(self.board)
                            self.current_player = 3 - self.current_player
                else:
                    self.draw_win_menu()
            #self.draw_fps()
            self.draw_cursor()
        
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.handle_events()
            self.update_screen()

# Instantiate the Game class and run the game
if __name__ == "__main__":
    game = GameManager()
    game.run()
    
