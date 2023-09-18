import tkinter as tk
import random
from enum import Enum
import time

class Estado(Enum):
    CERO = 0
    UNO = 1
    DOS = 2
    TRES = 3
    CUATRO = 4
    CINCO = 5
    SEIS = 6
    SIETE = 7
    OCHO = 8
    BOMBA = 9

def init_estados(estados, revelado):

    # inicializamos el array estados
    for row in range(rows):
        estados_row = []
        revelados_row = []
        for col in range(cols):
            estados_row.append(Estado.CERO)
            revelados_row.append(False)
        estados.append(estados_row)
        revelado.append(revelados_row)
    
    # Colocamos las bombas en posiciones aleatorias
    global bombas
    while len(bombas) < num_bombas:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if (row, col) not in bombas:
            bombas.append((row, col))
            estados[row][col] = Estado.BOMBA
    
    # Actualizamos los estados de los botones adyacentes a las bombas
    for row in range(rows):
        for col in range(cols):
            if estados[row][col] == Estado.BOMBA:
                continue
            count = 0
            for i in range(row-1, row+2):
                for j in range(col-1, col+2):
                    if i < 0 or i >= rows or j < 0 or j >= cols:
                        continue
                    if estados[i][j] == Estado.BOMBA:
                        count += 1
            estados[row][col] = Estado(count)

def cambiar_estado(i, j, event):
    #si el juego ha finalizado o el cuadrado ya ha sido revelado no hace nada
    if not gameActive or revelado[i][j]:
        return
    if event.num == 1:
        actualizar_boton(i, j)
    elif event.num == 3:

        if contador_bombas > 0 and botones[i][j]['text'] != "X":
            botones[i][j].config(bg="gray", font=("TkDefaultFont", 10, "bold"), text="X")
            actualizar_contador_bombas(-1)
        elif botones[i][j]['text'] != "":
            botones[i][j].config(bg="gray", font=("TkDefaultFont", 10, "bold"), text="", relief="solid")
            actualizar_contador_bombas(1)


def actualizar_boton(i, j):
    global rows, cols, gameActive

    revelado[i][j] = True
    if estados[i][j] == Estado.BOMBA:
        botones[i][j].config(bg="red", fg=textColor(estados[i][j]), font=("TkDefaultFont", 10, "bold"), text="X")
        if gameActive:
            gameActive = False
            revelaBombas()
            gameover()
    elif estados[i][j] == Estado.CERO:
        botones[i][j].config(bg="white", fg=textColor(estados[i][j]), font=("TkDefaultFont", 10, "bold"), text="")
        # revela los adyacentes
        for l in range(i-1, i+2):
            for m in range(j-1, j+2):
                if l < 0 or l >= rows or m < 0 or m >= cols:
                    continue
                if (revelado[l][m]):
                    continue
                actualizar_boton(l,m)   
    else:
        botones[i][j].config(bg="white", fg=textColor(estados[i][j]), font=("TkDefaultFont", 10, "bold"), text=str(estados[i][j].value))

    if gameActive and IsGameWin():
        gameActive = False
        gameWinLabel()

def textColor(estado):
    if estado == Estado.UNO:
        return 'blue'
    elif estado == Estado.DOS:
        return 'green'
    elif estado == Estado.TRES:
        return 'red'
    elif estado == Estado.CUATRO:
        return 'blue'
    elif estado == Estado.CINCO:
        return 'red'
    elif estado == Estado.SEIS:
        return 'blue'
    elif estado == Estado.SIETE:
        return 'green'
    elif estado == Estado.OCHO:
        return 'purple'
    else:
        return 'black'
    
def revelaBombas():
    global bombas
    for bomba in bombas:
        if not revelado[bomba[0]][bomba[1]]:
            time.sleep(0.1)
            actualizar_boton(bomba[0], bomba[1])
            root.update()
            
def IsGameWin():
    global rows, cols, num_bombas ,revelado

    cont = 0
    for rowRevelado in revelado:
        for isRevelado in rowRevelado:
            if isRevelado:
                cont += 1
    if cont == rows*cols - num_bombas:
        return True 

    return False

def gameWinLabel():

    global timer
    root.after_cancel(timer)

    # Crear un widget Label transparente para mostrar el texto
    label = tk.Label(root, text="", font=("Arial", 25), bg="black")
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    label.config(bg=root.cget('bg'))
    
    # Función para mostrar cada letra del texto con un retardo de 100ms entre cada una
    def show_text(text):
        if text:
            label.config(text=label.cget("text") + text[0])
            label.after(100, lambda: show_text(text[1:]))
    
    # Mostrar el texto "GAME OVER"
    show_text("YOU WIN THE GAME!!")

def gameover():

    global timer
    root.after_cancel(timer)

    # Crear un widget Label transparente para mostrar el texto
    label = tk.Label(root, text="", font=("Arial", 25), bg="black")
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    label.config(bg=root.cget('bg'))
    
    # Función para mostrar cada letra del texto con un retardo de 100ms entre cada una
    def show_text(text):
        if text:
            label.config(text=label.cget("text") + text[0])
            label.after(100, lambda: show_text(text[1:]))
    
    # Mostrar el texto "GAME OVER"
    show_text("GAME OVER")

def load_game():
    print("Cargar juego!")

def save_game():
    print("Guardar juego!")

def setDifficultAndRestart(difficult):
    setDifficult(difficult)
    restart_game()

def setDifficult(difficult):
    global num_bombas, rows, cols
    if difficult == 'Easy':
        num_bombas = 10
        rows = 6
        cols = 8
    elif difficult == 'Medium':
        num_bombas = 50
        rows, cols = 18, 24
    elif difficult == 'Difficult':
        num_bombas = 100
        rows, cols = 24, 32
    else:
        num_bombas = 50
        rows, cols = 18, 24
    restart_game()

def restart_game():
    global bombas, botones, estados, revelado, gameActive, timer_id, contador_bombas, num_bombas
    global etiqueta_contador_bombas, contador_tiempo, etiqueta_contador_tiempo, timer

    timer_id = None
    contador_bombas = num_bombas
    etiqueta_contador_bombas = num_bombas
    contador_tiempo = 0
    etiqueta_contador_tiempo = 0
    timer = None

    bombas = []
    botones = []
    estados = []
    revelado = []
    gameActive = True
    for widget in root.winfo_children():
        widget.destroy()
    init_game()
    init_estados(estados, revelado)

def init_game():

    global rows, cols, contador_bombas, etiqueta_contador_bombas, contador_tiempo, etiqueta_contador_tiempo

    menubar = tk.Menu(root)

    settingsmenu = tk.Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Easy", command=lambda: setDifficultAndRestart('Easy'))
    settingsmenu.add_command(label="Medium", command=lambda:setDifficultAndRestart('Medium'))
    settingsmenu.add_command(label="Difficult", command=lambda:setDifficultAndRestart('Difficult'))
    menubar.add_cascade(label="Settings", menu=settingsmenu)

    menubar.add_command(label="Restart", command=restart_game)
    menubar.add_command(label="Load", command=load_game)
    menubar.add_command(label="Save", command=save_game)
    

    # Mostrar el menú
    root.config(menu=menubar)

    contador_bombas = num_bombas
    etiqueta_contador_bombas = tk.Label(root, text="Bombas restantes: " + str(contador_bombas))
    etiqueta_contador_bombas.grid(row=0, column=0, columnspan=cols//2, sticky=tk.W)

    etiqueta_contador_tiempo = tk.Label(root, text="Tiempo: " + str(contador_tiempo))
    etiqueta_contador_tiempo.grid(row=0, column=cols//2, columnspan=cols//2, sticky=tk.E)

    init_timer()

    for i in range(rows):
        fila = []            
        for j in range(cols):
            boton = tk.Button(root, width=2, height=1, bg="gray", font=("TkDefaultFont", 10, "bold"), text="", relief="solid")
            boton.bind("<Button-1>", lambda event, i=i, j=j: cambiar_estado(i, j, event))
            boton.bind("<Button-3>", lambda event, i=i, j=j: cambiar_estado(i, j, event))
            boton.grid(row=i+1, column=j)
            fila.append(boton)
        botones.append(fila)

def init_timer():
    global contador_tiempo, timer_id
    contador_tiempo = 0
    etiqueta_contador_tiempo.config(text="Tiempo: " + str(contador_tiempo))
    if timer_id:
        root.after_cancel(timer_id)
    update_timer()

def update_timer():
    global contador_tiempo, timer_id
    contador_tiempo += 1
    etiqueta_contador_tiempo.config(text="Tiempo: " + str(contador_tiempo))
    timer_id = root.after(1000, update_timer)

def actualizar_contador_bombas(valor):
    global contador_bombas, etiqueta_contador_bombas
    contador_bombas += valor
    etiqueta_contador_bombas.config(text="Bombas restantes: " + str(contador_bombas))

## INIT GAME ##
root = tk.Tk()
root.title("Buscaminas")

timer_id = None
contador_bombas = 40
etiqueta_contador_bombas = 40
contador_tiempo = 0
etiqueta_contador_tiempo = 0
timer = None


setDifficult('Medium')
restart_game()
root.mainloop()
