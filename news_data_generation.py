from bs4 import BeautifulSoup
import urllib2
import sys
import os

from utils import utils
from utils import mongodb

def generate_bbc_news_json():
    """
    generate the news link and save to a csv file
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.abspath(
        os.path.join(current_directory, os.pardir)) 

    script_path = (current_directory + '/utils/' + 
                    'bbc_news.py')
    command = ('scrapy runspider ' + script_path + 
                ' -o /tmp/file.csv --nolog')
    print command
    out, err = utils.execute_shell(command)
    if err:
        print('Error: ' + err)
        # raise Exception('Could not set file privilege')


def get_news_content(link):
    """
    get news content of link
    """
    print('Fetching news data for %s ' % link)

    news_data = {}

    try:
        file = urllib2.urlopen(link)
    except urllib2.HTTPError, e:
        print 'link error'
        return None
    except Exception as e:
        return None
    
    soup = BeautifulSoup(file, "lxml")

    # 1. Get the page title by accessing the content of the <title> tag
    title = soup.title.get_text()

    # 2. Get the author name
    author = [item.attrs['content'] for item in soup('meta') \
                if item.has_attr('name') and \
                item.attrs['name'].lower()=='author']
    if author:
        author = author[0]
    else:
        author = None
   
    # 3. retrieve all content
    content = None
    try:
        contents = soup.find("div", {'class': 
                                'content__article-body from-content-api js-article__body'}).find_all('p')
        if contents:
            content = ' '.join([content.text for content in contents])
    except Exception as e:
        # content is empty
        content = None

    # replace following trailing characters
    if content: 
        content = content.replace('\n','. ')
        content = content.replace('\t','. ')
        content = content.replace('\r','. ')

    if link:
        link = link.replace('\n','')
        link = link.replace('\t','')
        link = link.replace('\r','')

    # news data for specific link
    news_data['link'] = link
    news_data['author'] = author
    news_data['title'] = title
    news_data['content'] = content
  
    return news_data


def main():
    list_news_data = []
    generate_bbc_news_json()
    if os.path.isfile('/tmp/file.csv'):
        with open('/tmp/file.csv', 'r') as infile:
            for line in infile:
                news_data =  get_news_content(line)
                if news_data:
                    print '*' * 100
                    print news_data
                    print '*' * 100
                    list_news_data.append(news_data)

    if list_news_data:
        for news in list_news_data:
            mongodb.main(news)

    # remove the news content added
    command = 'rm /tmp/file.csv'
    out, err = utils.execute_shell(command)

if '__main__' == __name__:
    main()
