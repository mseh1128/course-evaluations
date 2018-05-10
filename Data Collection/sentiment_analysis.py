# reading json
import requests
import re
from textblob import TextBlob as tb

def sentiment_analysis(comment):
	blob = tb(comment)
	return blob.sentiment

id = 520630
numOfReviews = 132
url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid=' + str(id) + '&page=1'
page_html = requests.get(url)
temp_json = page_html.json()
sums = 0
subjectivity = 0
ratings = temp_json['ratings']
latest_review = ratings[0]['rDate']
for review in ratings:
	sums += sentiment_analysis(review['rComments']).polarity
	subjectivity += sentiment_analysis(review['rComments']).subjectivity
	print(sentiment_analysis(review['rComments']))
i = 2

while temp_json['remaining'] != 0:
	url = 'http://www.ratemyprofessors.com/paginate/professors/ratings?tid=' + str(id) + '&page=' + str(i)
	page_html = requests.get(url)
	temp_json = page_html.json()
	ratings = temp_json['ratings']	
	for review in ratings:
		polarity = sentiment_analysis(review['rComments']).polarity
		sums += polarity
		subjectivity += subjectivity
		print(sentiment_analysis(review['rComments']))
	i+=1 

initial_review = temp_json['ratings'][-1]['rDate']
yearsTeaching = int(re.search('\d{4}$',latest_review).group(0)) -  int(re.search('\d{4}$',initial_review).group(0))
print(yearsTeaching)
print(sums/numOfReviews)
print(subjectivity/numOfReviews)
