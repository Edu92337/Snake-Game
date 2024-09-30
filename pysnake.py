import time
import curses
import random
#AS FUNÇÕES ESTÃO SEPARADAS EM FUNÇÕES GERAIS -> FUNÇÕES DE COBRA -> FUNÇÕES DE FRUTA 
def draw_screen(window):
    window.clear()
    window.border(0)

def select_difficulty(window):
    difficulty = {'1': 1000, '2': 500, '3': 150, '4': 90, '5': 35}
    while True:
        window.clear()
        window.addstr(0, 0, 'Selecione a dificuldade de 1 a 5: ')
        window.refresh()
        answer = window.getkey()  # Captura a string de entrada
        game_speed = difficulty.get(answer)
        if game_speed is not None:
            return game_speed
        else:
            window.addstr(1, 0, 'Escolha válida: 1 a 5')
            window.refresh()
            time.sleep(1)


def get_new_direction(window, timeout):
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]:
        return direction
    else:
        return None

def draw_actor(actor, window, char):#cria na posição actor[0],actor[1] o caracter char
    window.addch(actor[0], actor[1], char)

def move_actor(actor, direction):
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_RIGHT:
            actor[1] += 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case _:
            pass

def actor_hit_border(actor, window):
    altura, largura = window.getmaxyx()# recebe os limites da tela
    if actor[0] <= 0 or actor[0] >= altura - 1:#limite em y
        return True
    if actor[1] <= 0 or actor[1] >= largura - 1:#limite em x
        return True
    return False
#cobra
def draw_snake(snake, window):
    head = snake[0]#posição da cabeça da cobra
    draw_actor(actor=head, window=window, char='@')
    body = snake[1:]
    for body_part in body:
        draw_actor(actor=body_part, window=window, char='s')#desenha o resto da cobra nas suas respectivas posições

def move_snake(snake, direction,snake_ate_fruit):
    head = snake[0].copy()
    move_actor(actor=head, direction=direction)
    snake.insert(0, head)#insere o novo valor da posição da cabeça na cobra(MOVIMENTO DA COBRA)
    if not snake_ate_fruit:
        snake.pop()#remove o ultimo
    


def snake_hit_border(snake, window):#para saber se bateu na borda basta verificar se a cabeça bateu
    head = snake[0]
    return actor_hit_border(actor=head, window=window)

def snake_hit_itself(snake):# verifica se a cabeça da cobra,nesse instante tem a mesma posição da fruta ,se ela esta dentro da cobra
    head = snake[0]
    body = snake[1:]
    return head in body

def direction_is_opposite(direction,current_direction):# verifica se o usuario quer ir na direção oposta(não pode)
    match direction:
        case curses.KEY_UP:
            return current_direction==curses.KEY_DOWN
        case curses.KEY_LEFT:
            return current_direction==curses.KEY_RIGHT 
        case curses.KEY_RIGHT:
            return current_direction==curses.KEY_LEFT
        case curses.KEY_DOWN:
            return current_direction==curses.KEY_UP
        case _:
            pass

#fruta
def get_new_fruit(window):
    altura,comprimento = window.getmaxyx()
    return [random.randint(1,altura-2),random.randint(1,comprimento-2)]#cria uma posição aleatoria para gerar a fruta,dentro dos limites da tela

def snake_hit_fruit(snake,fruit):# faz a verificação especifica para snake
    return fruit in snake

def finish_game(score,window,game_speed):
    altura,comprimento=window.getmaxyx()
    s = f'Você perdeu! Coletou {score} frutas! na dificuldade:{game_speed}'
    y = int(altura/2)
    x = int((comprimento-len(s))/2)
    window.addstr(y,x,s)
    window.refresh()
    time.sleep(3)

def show_score(window, score):
    altura, largura = window.getmaxyx()  # Tamanho da janela
    window.addstr(0, largura - 10, f'Score: {score}')  # Exibe o score no topo direito da tela
    window.refresh()



def game_loop(window,game_speed):
    #SETUP
    curses.curs_set(0)# as coordenadas são contadas como uma matriz coordenadas das partes da cobra
    altura,comprimento = window.getmaxyx()
    snake = [[random.randint(1,altura-2),random.randint(1,comprimento-2)]] # IDEIA CENTRAL : TRATAR A COBRA COMO PONTOS NO ESPAÇO 
    fruit = get_new_fruit(window=window)
    current_direction = curses.KEY_DOWN
    snake_ate_fruit = False
    score = 0
     #LOOP DO JOGO
    while True:
        draw_screen(window)
        draw_snake(snake=snake, window=window)  
        draw_actor(actor=fruit,window=window,char=curses.ACS_DIAMOND)
        direction = get_new_direction(window=window, timeout=game_speed)#timeout da a taxa de atualização do mov da cobra
        show_score(window=window,score=score)

        if direction is None:
            direction = current_direction
        if direction_is_opposite(direction=direction,current_direction=current_direction):
            direction = current_direction
        move_snake(snake=snake, direction=direction,snake_ate_fruit=snake_ate_fruit)
        
        if snake_hit_border(snake=snake, window=window):
            break 
        if snake_hit_itself(snake=snake):
            break 
        if snake_hit_fruit(snake=snake,fruit=fruit):
            snake_ate_fruit = True
            score+=1
            fruit = get_new_fruit(window=window)
        else:
            snake_ate_fruit = False
        current_direction = direction

    finish_game(score=score,window=window,game_speed=game_speed)

if __name__ == '__main__':
    curses.wrapper(lambda window: game_loop(window, select_difficulty(window)))
