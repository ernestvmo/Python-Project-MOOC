import turtle
# from CONFIGS import *

# Les valeurs ci-dessous définissent les couleurs des cases du plan
COULEUR_CASES = 'white'
COULEUR_MUR = 'grey'
COULEUR_OBJECTIF = 'yellow'
COULEUR_PORTE = 'orange'
COULEUR_OBJET = 'green'
COULEUR_VUE = 'wheat'

# Couleur et dimension du personnage
COULEUR_PERSONNAGE = 'red'
RATIO_PERSONNAGE = 0.9  # Rapport entre diamètre du personnage et dimension des cases
POSITION_DEPART = (0, 1)  # Porte d'entrée du château

# Désignation des fichiers de données à utiliser
fichier_plan = 'plan_chateau.txt'
fichier_questions = 'dico_portes.txt'
fichier_objets = 'dico_objets.txt'


def turtle_setup():
    turtle.title("Escape the Maze!")
    turtle.setup(500, 500)
    turtle.bgcolor("white")
    turtle.pencolor("black")
    turtle.up()
    draw_annonce_box()
    turtle.goto(0, 165)
    turtle.write("Bienvenue dans le labyrinthe!", align="center", font=("Calibri", 12, "bold"))
    # draw inventory
    draw_inventory_box()
    turtle.up()
    # draw castle
    draw_castle()
    turtle.up()
    turtle.goto(-215, 145)


def draw_annonce_box():
    turtle.goto(-230, 202)
    turtle.fillcolor("white")
    turtle.begin_fill()
    turtle.down()
    turtle.goto(230, 202)
    turtle.goto(230, 152)
    turtle.goto(-230, 152)
    turtle.goto(-230, 202)
    turtle.end_fill()
    turtle.up()


def draw_inventory_box():
    turtle.fillcolor("white")
    turtle.begin_fill()
    turtle.goto(28, 120)
    turtle.down()
    turtle.goto(230, 120)
    turtle.goto(230, -202)
    turtle.goto(28, -202)
    turtle.goto(28, 120)
    turtle.end_fill()
    turtle.up()
    turtle.goto(50, 80)
    turtle.write("Inventaire:", move=False, align="left", font=("Calibri", 12, "bold"))


def draw_castle():
    x, y = -230, 120

    #     turtle.goto(-230, 150)
    #     turtle.goto(-218, 150)
    #     turtle.goto(-218, 138)
    #     turtle.goto(-230, 138)
    #     turtle.goto(-230, 150)
    turtle.goto(x, y)
    for r in castle_map:
        turtle.down()
        for i in r:
            if i == 0:
                turtle.fillcolor(COULEUR_CASES)
            elif i == 1:
                turtle.fillcolor(COULEUR_MUR)
            elif i == 2:
                turtle.fillcolor(COULEUR_OBJECTIF)
            elif i == 3:
                turtle.fillcolor(COULEUR_PORTE)
            elif i == 4:
                turtle.fillcolor(COULEUR_OBJET)

            turtle.begin_fill()
            turtle.goto(x, y)
            turtle.down()
            x += tile_size
            turtle.goto(x, y)
            y -= tile_size
            turtle.goto(x, y)
            x -= tile_size
            turtle.goto(x, y)
            y += tile_size
            turtle.goto(x, y)
            x += tile_size
            turtle.end_fill()
        turtle.up()
        x = -230
        y -= tile_size
        turtle.goto(x, y)


def lire_matrice(fichier_encodage):
    with open(fichier_encodage, encoding='utf-8') as fichier_in:
        return [[int(colonne) for colonne in ligne.split()] for ligne in fichier_in]


def create_object_dict(fichier):
    obj_dict = {}
    file = open(fichier)
    lines = file.readlines()

    for i in lines:
        if "\"" in i:
            index = i.index("\"")
        else:
            index = i.index("\'")
        sub1 = i[:index - 2].strip()
        sub2 = i[index:].strip()
        obj_dict[sub1] = sub2
    return obj_dict


def create_porte_dict(filename):
    porte_dict = {}

    file = open(filename)
    lines = file.readlines()

    for i in lines:
        sub1 = i[:i.index("(", 6)]
        sub2 = i[i.index("(", 6):]

        sub1 = sub1.strip()
        sub1 = sub1[:len(sub1) - 1]

        sub2 = sub2.strip()
        sub2 = sub2[1:len(sub2) - 1]

        porte_dict[sub1] = sub2

    return porte_dict


def start_game():
    global position
    turtle.up()
    turtle.goto(-212, 114)
    turtle.dot(tile_size * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)
    turtle.listen()  # Déclenche l’écoute du clavier
    position = POSITION_DEPART
    turtle.onkeypress(deplacer_gauche, "Left")  
    turtle.onkeypress(deplacer_droite, "Right")
    turtle.onkeypress(deplacer_haut, "Up")
    turtle.onkeypress(deplacer_bas, "Down")
    turtle.mainloop()


def update_annonce_box(text, old_location):
    draw_annonce_box()
    turtle.goto(-215, 167)
    turtle.write(text, move=False, align="left", font=("Calibri", 10, "bold"))
    turtle.goto(old_location[0], old_location[1])


def update_inventory_box(old_location):
    draw_inventory_box()
    turtle.up()
    turtle.goto(50, 50)
    # turtle.down()
    count = 1
    for i in inventory:
        turtle.write("\u2116" + str(count) + " : " + str(i), move=False, align="left", font=("Calibri", 10, "normal"))
        turtle.goto(turtle.xcor(), turtle.ycor() - 20)
        count += 1
    turtle.goto(old_location[0], old_location[1])


def deplacer(goto_x, goto_y):
    paint_trail(turtle.pos())
    turtle.goto(goto_x, goto_y)
    paint_current_tile(turtle.pos())


def move(directed_tile, diff_x, diff_y):
    global position
    global inventory

    deplacer(turtle.xcor() + diff_x, turtle.ycor() + diff_y)
    position = directed_tile

    if check_is_object(directed_tile):
        stop_movement()
        inventory.append(add_item_to_inventory(directed_tile))
        update_inventory_box(turtle.pos())
    
    start_movement()

def stop_movement():
    turtle.onkeypress(None, "Left")
    turtle.onkeypress(None, "Right")
    turtle.onkeypress(None, "Up")
    turtle.onkeypress(None, "Down")

def start_movement():
    turtle.onkeypress(deplacer_gauche, "Left")  
    turtle.onkeypress(deplacer_droite, "Right")
    turtle.onkeypress(deplacer_haut, "Up")
    turtle.onkeypress(deplacer_bas, "Down")
    

def win():
    stop_movement()
    update_annonce_box("Bravo! Vous vous \xeates \xe9chapp\xe9.", turtle.pos())


def deplacer_gauche():
    global inventory
    global position
    turtle.onkeypress(None, "Left")
    directed_tile = (position[0], position[1] - 1)

    if not check_is_wall(directed_tile):
        if check_is_exit(directed_tile):
            move(directed_tile, -tile_size, 0)
            win()
            return
        elif check_is_gate(directed_tile):
            if ask_question(directed_tile):
                # if correct
                move(directed_tile, -tile_size, 0)
        else:
            turtle.onkeypress(None, "Left")
            move(directed_tile, -tile_size, 0)
    turtle.onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    global position
    turtle.onkeypress(None, "Right")
    directed_tile = (position[0], position[1] + 1)

    if not check_is_wall(directed_tile):
        if check_is_exit(directed_tile):
            move(directed_tile, tile_size, 0)
            win()
            return
        elif check_is_gate(directed_tile):
            if ask_question(directed_tile):
                # if correct
                move(directed_tile, tile_size, 0)
        else:
            turtle.onkeypress(None, "Right")
            move(directed_tile, tile_size, 0)
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    global inventory
    global position
    turtle.onkeypress(None, "Up")
    directed_tile = (position[0] - 1, position[1])

    if not check_is_wall(directed_tile):
        if check_is_exit(directed_tile):
            move(directed_tile, 0, tile_size)
            win()
            return
        elif check_is_gate(directed_tile):
            if ask_question(directed_tile):
                # if correct
                move(directed_tile, 0, tile_size)
        else:
            turtle.onkeypress(None, "Up")
            move(directed_tile, 0, tile_size)
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    global inventory
    global position
    turtle.onkeypress(None, "Down")
    directed_tile = (position[0] + 1, position[1])

    if not check_is_wall(directed_tile):
        if check_is_exit(directed_tile):
            move(directed_tile, 0, -tile_size)
            win()
            return
        elif check_is_gate(directed_tile):
            if ask_question(directed_tile):
                # if correct
                move(directed_tile, 0, -tile_size)
        else:
            turtle.onkeypress(None, "Down")
            move(directed_tile, 0, -tile_size)
    turtle.onkeypress(deplacer_bas, "Down")


def check_is_wall(direction):
    if castle_map[direction[0]][direction[1]] == 1:
        return True
    else:
        return False


def check_is_object(direction):
    if castle_map[direction[0]][direction[1]] == 4:
        return True
    else:
        return False


def check_is_gate(direction):
    if castle_map[direction[0]][direction[1]] == 3:
        return True
    else:
        return False


def check_is_exit(direction):
    if castle_map[direction[0]][direction[1]] == 2:
        return True
    else:
        return False


def paint_trail(trail_position):
    turtle.goto(trail_position[0] - (tile_size / 2), trail_position[1] + (tile_size / 2))
    turtle.down()
    turtle.fillcolor(COULEUR_VUE)
    turtle.begin_fill()
    x, y = turtle.position()
    turtle.goto(x + tile_size, y)
    turtle.goto(x + tile_size, y - tile_size)
    turtle.goto(x, y - tile_size)
    turtle.goto(x, y)
    turtle.end_fill()
    turtle.up()
    turtle.goto(x + (tile_size / 2), y - (tile_size / 2))


def paint_current_tile(current_tile):
    paint_trail(current_tile)
    turtle.dot(tile_size * RATIO_PERSONNAGE, "red")


def add_item_to_inventory(tile_location):
    global castle_map
    to_return = object_dict[str(tile_location)]
    update_annonce_box(f"Vous avez trouv\xe9: {object_dict[str(tile_location)]}", turtle.pos())
    del object_dict[str(tile_location)]
    castle_map[tile_location[0]][tile_location[1]] = 0
    return to_return


def ask_question(tile_location):
    global castle_map
    question, answer = split_quest_ans(portes_dict[str(tile_location)])
    reply = turtle.textinput("Question", question)
    turtle.listen()

    if reply is None:
        update_annonce_box("Cette porte est fermée.", turtle.pos())
        return False
    elif reply.lower().strip() == answer.lower():
        del portes_dict[str(tile_location)]
        castle_map[tile_location[0]][tile_location[1]] = 0
        update_annonce_box("La porte s'est ouverte. Bien jou\xe9!", turtle.pos())
        return True
    else:
        update_annonce_box("Mauvaise r\xe9ponse. La porte reste ferm\xe9e.", turtle.pos())
        return False


def split_quest_ans(text):
    if "', '" in text:
        index = text.index("', '")
    elif "\", '" in text:
        index = text.index("\", '")
    else:
        index = text.index("', \"")

    quest = text[:index + 1]
    ans = text[index + 2:]

    quest = quest.strip()
    quest = quest[1:len(quest) - 1]
    ans = ans.strip()
    ans = ans[1:len(ans) - 1]

    return quest, ans


turtle.hideturtle()
turtle.speed(0)

position = (0, 1)
inventory = []
tile_size = 12
object_dict = create_object_dict(fichier_objets)
portes_dict = create_porte_dict(fichier_questions)
castle_map = lire_matrice(fichier_plan)

turtle_setup()
start_game()
