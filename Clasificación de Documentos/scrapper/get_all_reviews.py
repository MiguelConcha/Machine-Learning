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
        Gets the page html and returns it with BeautifulSoup
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
        Gets review from a review box of with BeatifulSoup
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
        Gets all reviews in the page's url.
        The page's url must begin with:
            'http://www.metacritic.com/critic/mick-lasalle?page='
    """
    
    soup = getPageSoup(url)

    review_boxes = soup.findAll('li', attrs={'class': 'review'})
    # A review is a tuple with score and review
    reviews = []
    for review_box in review_boxes:
        try:
            reviews.append(getReview(review_box))
            # To avoid so multiple requests
            time.sleep(randint(2,5))
        except:
            pass
    return reviews


def getAllReviews():
    """
        Gets all Mick LaSalle reviews in Metacritic
    """
    url_base = 'http://www.metacritic.com/critic/mick-lasalle?'
    url_base += 'filter=movies&num_items=100&sort_options=date&page='
    reviews = []
    for page in range(28):
        print('Page: ' + str(page))
        reviews += (getPageReviews(url_base + str(page)))

    return reviews


def appendReviewsInfile(file_path, reviews):
    """
        Append Reviews in file
    """

    open(file_path, 'w').close
    with open(file_path, "a") as myfile:
        for review in reviews:
            myfile.write(str(review[0]) + '////' + review[1] + '\n')

filename = 'reviews.txt'

reviews = getAllReviews()
appendReviewsInfile(filename, reviews)

