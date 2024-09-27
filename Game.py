import pygame
from math import sqrt
from pygame.draw import * # type: ignore
from random import randint
pygame.init()


#   Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

DARKSLATEBLUE = (72,61,139)
LIGHT_GREY= (211,211,211)

colors=[DARKSLATEBLUE,RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


#   Screen   # Параметры начального окна
WIDTH = 1100
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # размер окна
pygame.display.set_caption("Поймай шарик")   # Название окна
screen.fill(LIGHT_GREY)  # 
pygame.display.update()  # обнолние окна


#   Text    # Функция отрисовки текста
font = pygame.font.Font(None, 36)    # Задание размера текста

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))   #отрисовка текста на экране


#   Timer
timer_duration = 30000  # 30 sec 
start_time = pygame.time.get_ticks()  # начало отсчета таймера


#  Start score
score = 0         # Общее кол-во очков
score_star = 0    # Кол-во пойманых зввезд


# Class Ball
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):     # Начальные параметры
        global radius_ball
        
        pygame.sprite.Sprite.__init__(self)
        self.x_ball = randint(100, WIDTH-100)   # позиция по х
        self.y_ball = randint(100, HEIGHT-100)  # позиция по y
        self.radius_ball = randint(25, 80)      # радиус 
        self.color_ball = colors[randint(0, 6)] # цвет 
        self.speed_x_ball = randint(2,8)        # скорость по х
        self.speed_y_ball = randint(3,10)       # скорость по y
        
        radius_ball=self.radius_ball
         
    def update(self):      # Функция движения 
        global x_ball, y_ball, speed_x_ball, speed_y_ball
        # Движение 
        self.x_ball += self.speed_x_ball
        self.y_ball += self.speed_y_ball
        # Отталкивание от стен
        if self.x_ball < self.radius_ball or self.x_ball > WIDTH - self.radius_ball:
            self.speed_x_ball *= -1
        if self.y_ball < self.radius_ball or self.y_ball > HEIGHT - self.radius_ball:
            self.speed_y_ball *= -1
            
        x_ball= self.x_ball
        y_ball= self.y_ball
        speed_x_ball= self.speed_x_ball
        speed_y_ball= self.speed_y_ball
    
    # Отрисовка на экране
    def draw(self):
        pygame.draw.circle(screen,
                           self.color_ball,
                           (self.x_ball, self.y_ball),
                           self.radius_ball )
    
    # Обновление после нажатия
    def reset(self):
        ball.__init__() # основные параметров
        ball.draw()     # отрисовка
        ball.update()   # движение

# Создание списка из 3 шаров
balls=[Ball() for _ in range(3)]


# CLASS STAR
class Star(pygame.sprite.Sprite):
    
    def __init__(self):   # Начальные параметры
        global x_star, y_star
        
        # Параметры звезды
        pygame.sprite.Sprite.__init__(self)
        self.X_star = randint(100, WIDTH-100)   # позиция по х
        self.y_star = randint(100, HEIGHT-100)  # позиция по y
        self.color_star = YELLOW                # цвет
        # координаты 
        self.point_star =[
             (self.X_star   , self.y_star    ),
             (self.X_star+10, self.y_star+40 ),
             (self.X_star+50, self.y_star+40 ),
             (self.X_star+15, self.y_star+55 ),
             (self.X_star+25, self.y_star+100),
             (self.X_star   , self.y_star+70 ),
             (self.X_star-25, self.y_star+100),
             (self.X_star-15, self.y_star+55 ),
             (self.X_star-50, self.y_star+40 ),
             (self.X_star-10, self.y_star+40 )
             ]
            
        x_star = self.X_star
        y_star = self.y_star
  
     # Отрисовка на экране       
    def draw(self): 
        pygame.draw.polygon(screen,self.color_star,self.point_star)
        
    def reset(self):  # 
        star.__init__()

star= Star()


def click(event):
    global score, score_star, mx,my, spawn_star
    
    (mx, my) = pygame.mouse.get_pos()
 
#       Star cllick
    s_star = sqrt((mx-x_star)**2+(my-y_star-42)**2)  
    if s_star < 43:
        score +=3
        score_star +=1
        star.reset()  
        spawn_star = not spawn_star  



### START MENU
# меню начала игры 
def start_menu():
    global W_r, H_r

    W_r= WIDTH * 1/ 3   
    H_r= HEIGHT* 1/ 3

    # Отображение кнопки наала
    pygame.draw.rect(screen, (119,136,153), ((W_r, H_r,W_r*2-W_r, H_r*2-H_r )))
    
    # Отобржение текста
    font = pygame.font.Font(None, 120)
    draw_text(screen,'SPACE', font, BLACK, W_r+W_r/16, H_r+ H_r/3)
    
    pygame.display.flip()


### START GAME
time_star=pygame.USEREVENT +1   # создание собственного события
pygame.time.set_timer(time_star, 500)    #Отсчет таймера появления звезды
spawn_star = True

# начало игры
def game():
    global game_status,current_time, ball, score, spawn_star
    
    current_time = pygame.time.get_ticks() # получение текущего времени    
    
    for ball in balls:   # обращение к 3м элементам из списка
        ball.draw()      # отрисовка
        ball.update()    # движение
        if event.type == pygame.MOUSEBUTTONDOWN:       # проверка нажатия на обьект
            s_ball = sqrt((mx-x_ball)**2+(my-y_ball)**2)
            if s_ball < radius_ball:
                ball.reset()    # обновление шара/ перезапуск
                score +=1    

    if spawn_star:
        star.draw()        
    
    
###      TIMER            
    if current_time - start_time >= timer_duration: 
        # изменение игрового статуса в случае окончания таймера
        game_status = 'end_game'

    remaining_time = (timer_duration - (current_time - start_time)) // 1000 + 1  
    draw_text(screen, f"Осталось времени: {remaining_time}",font, BLACK,WIDTH/2-130,10)

###       SCORES
    draw_text(screen, f'Очки: {score}', font, BLACK, 10, 10)
    

    pygame.display.flip()  # обновление экрана



# Меню окончания игры и вывод очков на экран
def end_game():
    
    W_r = WIDTH*1/7
    H_r = HEIGHT-HEIGHT/5
    # Отоброжение кнопки
    pygame.draw.rect (screen, (119,136,153), ((W_r, H_r,W_r*6-W_r,150)))
    # текст кнопки выхода
    font = pygame.font.Font(None, 120)
    draw_text(screen,'SPACE TO QUIT', font, BLACK, W_r+55,685 )
    
    # Отоброжение полученных очков
    font = pygame.font.Font(None, 90)
    draw_text(screen, f"Поймано шаров: {score-(score_star*3)} ", font, BLACK, W_r,200)
    draw_text(screen, f"Поймано звезд: {score_star} x 3 ", font, BLACK, W_r,300)
    draw_text(screen, f"Всего очков: {score} ", font, BLACK, W_r,400)
    
    pygame.display.flip()    
    

# Игровой статус
game_status = 'start_menu'

clock = pygame.time.Clock()

running = True
# основной цикл программы
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # выход из программы
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
            
        elif event.type == time_star:
            spawn_star = not spawn_star
            star.reset()
            
    clock.tick(200)
      
    screen.fill(LIGHT_GREY)  
    
    # Проверка статуса игры
    if game_status == 'start_menu':
        start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            # изменение игрового статуса в случае нажатия на SPACE
            if event.type == pygame.KEYDOWN:
               game_status = 'game'
                
    if game_status == 'game':
        game()
        
    if game_status == 'end_game':
        end_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
    
# обновление экрана
    pygame.display.flip()
# Заавершение цикла
pygame.quit()
