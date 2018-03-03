# -*- encoding: utf-8 -*-
import csv


def change_score():

	original = open('pass-prueba.txt', 'r')
	nuevo = open("reviews.txt", "w")
	for line in original:
            a = line.split(',')
            num = int(a[0])
            if num == 0:
                num = 0
            elif num == 2:
                num = 0
            elif num == 5:
                num = 0
            elif num == 6:
                num = 0
            elif num == 8:
                num = 1
            elif num == 9: 
                num = 1
            elif num == 10:
                num = 1

            line_aux = '"' + line[len(a[0])+1:len(line)-1].replace('"', '') + '",' + str(num) + '\n'
            nuevo.write(line_aux)

	original.close()
	nuevo.close()

change_score()
