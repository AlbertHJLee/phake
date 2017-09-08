"""
Utils for facebook post retriever
Make sure to be using newest version of facebook-sdk from github. Stable version does not have full functionality.
"""

import os
import sys
import facebook
import json



def getposts(token):

    """
    Placeholder function for testing Facebook SDK queries
    """

    graph = facebook.GraphAPI(access_token=token, version="2.10")

    users = graph.search(type='user', q='Keanu Reeves')
    user = users[u'data'][0]

    pages = graph.search(type='page', q='news')
    page = pages[u'data'][0]

    posts = graph.get_connections(id=page[u'id'], connection_name='posts')
    
    info = graph.get_object(id=posts[u'data'][0][u'id'], fields='link,description,message,name,place,picture')

    print page
    print posts
    print info
    
    print info[u'message']

    return True
    


    
def scrape(token, seed='news', pagelimit=1000, postlimit=100):

    """
    Get list of pages and posts
    """

    graph = facebook.GraphAPI(access_token=token, version="2.10")
    pages = graph.search(type='page', q=seed, limit=pagelimit)

    allposts = []
    #allinfo = []
    
    print "Looping over pages..."
    
    for page in pages[u'data']:
        
        posts = graph.get_connections(id=page[u'id'], connection_name='posts', limit=postlimit)
        #allposts += posts[u'data']

        for post in posts[u'data']:
            
            info = graph.get_object(id=post[u'id'], fields='link,description,message,name,created_time,from')
            allposts += [info]

    print "Done"
    
    return pages, allposts




def save(pages,posts):

    """
    Save scraped data to json files
    """

    print "Saving files..."
    
    with open('data/pages.json','w') as outfile:
        json.dump(pages,outfile)

    with open('data/posts.json','w') as outfile:
        json.dump(posts,outfile)

    print "Saved"

    return True





def safeScrape(token, seed='news', pagelimit=1000, postlimit=100, verbose=1):

    """
    Get list of pages and posts
    Save while scraping (to avoid losing data to query limits)
    """

    if verbose >= 1:
        print "Starting scrape..."
    graph = facebook.GraphAPI(access_token=token, version="2.10")
    pages = graph.search(type='page', q=seed, limit=pagelimit)

    if verbose >= 1:
        print "Saving pages..."
    with open('data/pages.json','w') as outfile:
        json.dump(pages,outfile)

    allposts = []
    
    print "Looping over pages..."
    
    for page in pages[u'data']:
        
        posts = graph.get_connections(id=page[u'id'], connection_name='posts', limit=postlimit)

        for post in posts[u'data']:
            
            info = graph.get_object(id=post[u'id'], fields='link,description,message,name,created_time,from')
            allposts += [info]

        with open('data/posts.json','w') as outfile:
            if verbose >= 1:
                print "Saving posts for " + page[u'name'] + "..."
            json.dump(allposts,outfile)

    print "Done"
    
    return pages, allposts

    




if __name__ == "__main__":

    """
    Scrapes news sites and saves json files of results.
    First argument must be OAuth token.
    """
    
    token = sys.argv[0]

    [pages,posts] = safeScrape(token,seed='news',pagelimit=50,postlimit=50)

    #save(pages,posts)
