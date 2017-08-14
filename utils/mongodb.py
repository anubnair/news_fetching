import pymongo
import ssl
import sys

URL = ("mongodb://anu:welcome1@aws-us-east-1-portal.27.dblayer.com:22051," +
       "aws-us-east-1-portal.28.dblayer.com:22051/newsdb?ssl=true")


def connect_to_db():
    """
    connect to mongo db
    """
    try:
        client = pymongo.MongoClient(URL, ssl_cert_reqs=ssl.CERT_NONE)
        db = client.get_default_database()
    except Exception as e:
        print 'error while connecting to db'
        print 'error %s' % str(e)
        sys.exit(0)
    return db


def check_data_in_newscollection(url, db):
    """
    check whether the same news is available in db before inserting.
    """
    try:
        print("Checking data in database link: %s" % url)

        data_in_db = db.newscollection.find({"link": url})
        return data_in_db
    except Exception as e:
        print 'error while checking data in news collection'
        print 'error %s' % str(e)
        sys.exit(0)


def insert_data_to_newscollection(collection, data):
    """
    insert the given data to db
    """
    try:
        collection.insert_one(data)

    except Exception as e:
        print 'error while inserting to db'
        print 'error %s' % str(e)
        sys.exit(0)


def grep_news_using_regex(db, search_word):
    """
    grep the search word in news content
    """
    try:
        print('Searching news related to %s ' % search_word)
        search_word = '.*' + search_word + '.*'
        data = list(db.newscollection.find({'content':
                    {'$regex': search_word}}))
        return data

    except Exception as e:
        print 'error while searching in db'
        print 'error %s' % str(e)
        sys.exit(0)


def main(data):
    """
    mongo db module starts here
    """
    db = connect_to_db()
    collection = db['newscollection']

    # check the link is already in database
    data_in_db = list(check_data_in_newscollection(data['link'], db))
    if data_in_db:
        print 'Already the news content is available in database'
        return
    else:
        print 'Inserting link  %s details to database ' % (data['link'])
        insert_data_to_newscollection(collection, data)
