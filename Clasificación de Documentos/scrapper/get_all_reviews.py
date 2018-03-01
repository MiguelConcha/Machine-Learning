# -*- encoding: utf-8 -*-
# Scraping
from bs4 import BeautifulSoup
import urllib.request as urllib2
from random import randint
# Format
import csv
from datetime import datetime
import re
import time


def getPageSoup(url):
    """
        Obtiene el html de una página y lo regresa con BeautifulSoup
    """

    request = urllib2.Request(url)
    request.add_header(
        'User-Agent',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36' + 
        'KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    )
    opener = urllib2.build_opener()
    html_doc = opener.open(request).read()
    return BeautifulSoup(html_doc, "html.parser")


def getReview(review_box):
    """
        Obtiene una crítica de una caja de crítica de BeautifulSoup
    """

    try:
        # Score
        score_box = review_box.find(
            'li', attrs={'class':'review_product_score brief_critscore'}
        )
        score_span_box = score_box.find('span', attrs={'class' : 'metascore_w'})
        score = round(int(score_span_box.text.strip())/10)
        # Review
        review = review_box.text.strip() # strip() is used to remove starting and trailing
        review_url = review_box.find('li', attrs={'class':'full_review'}).find(
            'a', attrs={'class':'external'}
        ).get('href')

        print(review_url)
        soup_review = getPageSoup(review_url)
        all_p = soup_review.find('div' , attrs={'class':'article-body'}).find_all(
            'p',attrs={'class':''}
        )
        all_p_limpio = []
        for i in all_p:
            s = re.sub("(@+[A-Z]*)\w+", r'', i.get_text())
            s = s.replace('\n', ' ')
            # To reduce data that doesn's matter
            if s[:12] == "Mick LaSalle":
                break
            all_p_limpio.append(s)
            #all_p_limpio.append(re.sub(r'[^\x00-\x7f]',r'', s.encode('latin1','ignore')))
        return (score, ''.join(all_p_limpio))
    except Exception as e:
        print(e)


def getPageReviews(url):
    """
        Obtener todas la criticas en una url de una página.
        El url de la página debe de empezar con:
            'http://www.metacritic.com/critic/mick-lasalle?page='
    """
    
    soup = getPageSoup(url)

    review_boxes = soup.findAll('li', attrs={'class': 'review'})
    # A review is a tuple with score and review
    for review_box in review_boxes:
        try:
            yield getReview(review_box)
            # To avoid so multiple requests
            time.sleep(randint(2,5))
        except:
            pass


def getAllReviews():
    """
        Obtener todas las críticas de Mick LaSalle en Metacritic
    """

    url_base = 'http://www.metacritic.com/critic/mick-lasalle?'
    url_base += 'filter=movies&num_items=100&sort_options=date&page='
    for page in range(28):
        print('Page: ' + str(page))
        for review in getPageReviews(url_base + str(page)):
            yield review


def appendReviewsInfile(file_path):
    """
        Agregar las criticas al final de un archivo
    """

    # Para crear el archivo
    head = ['@relation criticas\n\n@attribute calificacion numeric\n@attribute critica string\n\n@data\n\n']

    with open(file_path, "a") as myfile:
        writer = csv.writer(myfile)
        writer.writerow(head)
        for review in getAllReviews():
            try:
                writer.writerow([str(review[0]), review[1]])
                print("Escrito en archivo")
            except Exception as e:
                print(e)


filename = 'criticas.arff'
appendReviewsInfile(filename)

