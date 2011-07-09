#!/usr/bin/env python
import cPickle as pickle
import logging
import os
import random
import time
import urllib

class MyFancyUrlOpener(urllib.FancyURLopener):
    version ='paianjenul gigi (%s)' % (urllib.FancyURLopener.version,)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise IOError('http error', errcode)

def dump_remaining_page_numbers(page_numbers):
    logging.info("Dumping remaining page numbers")
    with open('pages.pickle', 'wb') as f:
        return pickle.dump(page_numbers, f)

def load_remaining_page_numbers():
    with open('pages.pickle', 'rb') as f:
        return pickle.load(f)

def generate_page_numbers():
    page_numbers = range(1, 21009+1)
    random.shuffle(page_numbers)
    return page_numbers

def get_page_numers():
    if os.path.exists('pages.pickle'):
        return load_remaining_page_numbers()
    return generate_page_numbers()

def main():
    logging.info("getting page numbers")
    page_numbers = get_page_numers()
    myurlopener = MyFancyUrlOpener()
    try:
        while page_numbers:
            i = page_numbers.pop()
            src = r'''http://bacalaureat.edu.ro/2010/rapoarte/rezultate/alfabetic/page_%d.html''' % (i,)
            dst = r'''data/2010/rapoarte/rezultate/alfabetic/page_%d.html''' % (i,)
            logging.info("Retrieving %s" % (src,))
            myurlopener.retrieve(src, dst)
            logging.info("Pausing")
            time.sleep(random.random()*0.25)
    except:
        dump_remaining_page_numbers(page_numbers + [i])
        raise

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s',
                        level=logging.DEBUG)
    main()
