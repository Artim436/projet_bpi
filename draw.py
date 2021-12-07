#!/usr/bin/env python3

""" main program draw.py """


import sys
import subprocess
import approximate_pi

try:
    IMG_SIZE, NB_POINTS, PRECISION = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
except IndexError:
    print("Le nombre d'argument n'est pas valide")
    raise
except ValueError:
    print("Un des arguments n'est pas valide.")
    raise
if IMG_SIZE < 100:
    print("La taille de l'image doit être supérieur ou égal à 100")
    raise ValueError
if NB_POINTS < 100:
    print("le nombre de points doit être supérieur ou égal à 100")
    raise ValueError
if PRECISION < 1 or PRECISION > 5:
    print("Le nombre de chiffre après la virgule renseigné n'est pas entre 1 et 5")
    raise ValueError


IMG_SIZE = int(sys.argv[1]) #size of the image in pixel
NB_POINTS = int(sys.argv[2]) #number of points in the simulation
PRECISION = int(sys.argv[3]) #number of digit avec the comma

BLACK = '0 0 0'
RED = '1 0 0'
BLUE = '0 0 1'
WHITE = '1 1 1'

LENGH = IMG_SIZE//90

ITER_L = approximate_pi.draw_function(NB_POINTS) #[point, in_circle(point)]

def main():
    """ return image code"""
    cpt = 0
    img_code_list = [[WHITE for _ in range(IMG_SIZE)] for _ in range(IMG_SIZE)]  #all is white
    for img_nb in range(1, 11):
        for _ in range(NB_POINTS//10):
            cour = next(ITER_L)
            i = int((cour[0][0]+1)*IMG_SIZE/2) #transforme (-1,1) into [0, IMG_SIZE]
            j = int((cour[0][1]+1)*IMG_SIZE/2) #transforme (-1,1) into [0, IMG_SIZE]
            if cour[1]:
                cpt += 1
                img_code_list[i][j] = RED #red in the circle
            else:
                img_code_list[i][j] = BLUE #blue outside the circle
        inter_code_list = [[] for _ in range(IMG_SIZE)] #new img code
        for _ in range(IMG_SIZE):
            inter_code_list[_] = img_code_list[_].copy()
        pi_numbers = (4*cpt/(img_nb*(NB_POINTS//10)))*10**PRECISION
        pi_list = []
        for k_precision in range(PRECISION+1):
            pi_list.append(int((pi_numbers/10**(PRECISION-k_precision))%10))
            #pi_list = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3] if PRECISION = 17
        yield [inter_code_list, pi_list] #[image, pi]

ITER_10_LISTE = main()

def generate_ppm_file(image_number):
    """ generate image ppm type"""
    cour_img_pi = next(ITER_10_LISTE) #[inter_code_liste, pi_list]
    pi_number_list = cour_img_pi[1]  #[3,1,4,1,5]
    image_name = ''
    for i in range(1, len(pi_number_list)):
        image_name += str(pi_number_list[i]) #image_name = "1415"
    with open(f"img{image_number}_{pi_number_list[0]}-{image_name}.ppm",\
        "w", encoding='utf-8') as image: #"img0_3-1415.ppm"
        print('P3', file=image)
        print(f'{IMG_SIZE} {IMG_SIZE}', file=image)
        print('1', file=image) #better than 255 for the memory
        image_code = cour_img_pi[0]
        for k_pi_nb_list, pi_nb in enumerate(pi_number_list):
            number(pi_nb, k_pi_nb_list, image_code) #number(3, 0, image_code)
        point(image_code) #draw a point
        for abscisse in range(IMG_SIZE):
            for ordonee in range(IMG_SIZE-1):
                print(image_code[abscisse][ordonee], end="  ", file=image)
            print(image_code[abscisse][IMG_SIZE-1], file=image)



#f'bloblo{blabla:.{toto}f}tutu'


def point(img_code_list):
    """ generate the point for pi approximation"""
    abscisse_l = int(IMG_SIZE/2 - IMG_SIZE/3.5 + IMG_SIZE/16)
    abscisse_r = int(IMG_SIZE/2 - IMG_SIZE/4 + (IMG_SIZE/50 +IMG_SIZE/10))
    ordonnee = int(IMG_SIZE//2 + IMG_SIZE//16)
    abscisse_avg = (abscisse_l + abscisse_r)//2
    for _ in range(LENGH):
        for __ in range (LENGH):
            img_code_list[ordonnee+_][abscisse_avg+__] = BLACK


def vertical_line(ordonee_l, ordonee_h, abscisse, img_code_list):
    """ draw a vertical line"""
    for _ in range(ordonee_h, ordonee_l+LENGH):
        for __ in range(LENGH):
            img_code_list[_][abscisse + __] = BLACK

def horizontal_line(abscisse_l, abscisse_r, ordonee, img_code_list):
    """ draw an horizntal line"""
    for _ in range(abscisse_l, abscisse_r+LENGH):
        for __ in range(LENGH):
            img_code_list[ordonee + __][_] = BLACK


def number(number_to_create, position, img_code_list):
    """ generat code ppm for number"""
    if position == 0:
        ordonee_h = int(IMG_SIZE//2 - IMG_SIZE//16)
        ordonee_l = int(IMG_SIZE//2 + IMG_SIZE//16)
        abscisse_r = int(IMG_SIZE/2 - IMG_SIZE/3.5 + \
            IMG_SIZE/16 +position*(IMG_SIZE/50 +IMG_SIZE/10))
        abscisse_l = int(IMG_SIZE/2 - IMG_SIZE/3.5 + position*(IMG_SIZE/50 +IMG_SIZE/10))
        ordonee_avg = (ordonee_h + ordonee_l)//2
    else:
        ordonee_h = int(IMG_SIZE//2 - IMG_SIZE//16)
        ordonee_l = int(IMG_SIZE//2 + IMG_SIZE//16)
        abscisse_r = int(IMG_SIZE/2 - IMG_SIZE/4 + IMG_SIZE/16 +position*(IMG_SIZE/50 +IMG_SIZE/10))
        abscisse_l = int(IMG_SIZE/2 - IMG_SIZE/4 + position*(IMG_SIZE/50 +IMG_SIZE/10))
        ordonee_avg = (ordonee_h + ordonee_l)//2
    if number_to_create == 6:
        vertical_line(ordonee_l, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_avg, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 8:
        vertical_line(ordonee_l, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 0:
        vertical_line(ordonee_l, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
    elif number_to_create == 2:
        vertical_line(ordonee_l, ordonee_avg, abscisse_l, img_code_list)
        vertical_line(ordonee_avg, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 4:
        vertical_line(ordonee_avg, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 9:
        vertical_line(ordonee_avg, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 7:
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
    elif number_to_create == 3:
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)
    elif number_to_create == 1:
        vertical_line(ordonee_l, ordonee_h, abscisse_r, img_code_list)
    elif number_to_create == 5:
        vertical_line(ordonee_avg, ordonee_h, abscisse_l, img_code_list)
        vertical_line(ordonee_l, ordonee_avg, abscisse_r, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_h, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_l, img_code_list)
        horizontal_line(abscisse_l, abscisse_r, ordonee_avg, img_code_list)

for k in range(10):
    generate_ppm_file(k)

subprocess.run("convert -delay 200 *.ppm anime.gif", shell=True, check=True)
