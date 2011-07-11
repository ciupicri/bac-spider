#!/usr/bin/env python
import cPickle as pickle
import logging
import os
import random
import time
import urllib
import urlparse

OUTPUT_DIR = 'data'


class MyFancyUrlOpener(urllib.FancyURLopener):
    version ='paianjenul gigi (%s)' % (urllib.FancyURLopener.version,)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise IOError('http error', errcode)


def dump_remaining_pages(pages):
    logging.info("Dumping remaining pages")
    with open('pages.pickle', 'wb') as f:
        return pickle.dump(pages, f)

def load_remaining_pages():
    logging.info("loading pages from pages.pickle")
    with open('pages.pickle', 'rb') as f:
        return pickle.load(f)

def generate_pages():
    logging.info("generating pages")
    page_pattern = r'''http://bacalaureat.edu.ro/%(year)d/rapoarte/rezultate/alfabetic/page_%(no)d.html'''
    pages = [page_pattern % {'year': 2011, 'no': i} for i in range(1, 21277+1)]
    random.shuffle(pages)
    return pages

def get_pages():
    if os.path.exists('pages.pickle'):
        return load_remaining_pages()
    return generate_pages()


def create_destination(page):
    global OUTPUT_DIR

    ignore, page_netloc, page_path, ignore, ignore = urlparse.urlsplit(page)
    page_path = page_path[1:] # without the first /
    page_path_head, page_path_tail = page_path.rsplit('/', 1)
    dst_dir = os.path.join(OUTPUT_DIR, page_netloc, page_path_head)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    dst = os.path.join(dst_dir, page_path_tail)
    return dst


def main():
    logging.info("getting pages")
    pages = get_pages()
    myurlopener = MyFancyUrlOpener()
    page = None # UnboundLocalError: local variable 'page' referenced before assignment
    try:
        while pages:
            page = pages.pop()
            dst = create_destination(page)
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
