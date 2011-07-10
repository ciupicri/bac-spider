#!/usr/bin/env python
import cPickle as pickle
import logging
import os
import random
import time
import urllib
import urlparse

class MyFancyUrlOpener(urllib.FancyURLopener):
    version ='paianjenul gigi (%s)' % (urllib.FancyURLopener.version,)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise IOError('http error', errcode)

def dump_remaining_pages(pages):
    logging.info("Dumping remaining pages")
    with open('pages.pickle', 'wb') as f:
        return pickle.dump(pages, f)

def load_remaining_pages():
    with open('pages.pickle', 'rb') as f:
        return pickle.load(f)

def generate_pages():
    page_pattern = r'''http://bacalaureat.edu.ro/%(year)d/rapoarte/rezultate/alfabetic/page_%(no)d.html'''
    pages = [page_pattern % {'year': 2010, 'no': i} for i in range(1, 21009+1)]
    random.shuffle(pages)
    return pages

def get_pages():
    if os.path.exists('pages.pickle'):
        return load_remaining_pages()
    return generate_pages()

def main():
    logging.info("getting pages")
    pages = get_pages()
    myurlopener = MyFancyUrlOpener()
    page = None # UnboundLocalError: local variable 'page' referenced before assignment
    try:
        while pages:
            page = pages.pop()
            ignore, netloc, path, ignore, ignore = urlparse.urlsplit(page)
            dst = os.path.join('data', netloc, path[1:]) # without the first /
            logging.info("Retrieving %s" % (page,))
            myurlopener.retrieve(page, dst)
            logging.info("Pausing")
            time.sleep(random.random()*0.25)
    except:
        dump_remaining_pages(pages + [page])
        raise

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s',
                        level=logging.DEBUG)
    main()
