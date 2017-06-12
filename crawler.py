#!/usr/bin/env python

import time
import thread
from re import match
from requests import get, packages
from BeautifulSoup import BeautifulSoup, SoupStrainer

# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
packages.urllib3.disable_warnings()

browser_url = 'http://www.mywebsite.com'

class AccessQueue:

    def __init__(self):
        self.items        = ['/']
        self.browsed_urls = ['/']

    def isEmpty(self):
        return self.items == []

    def put(self, item):
        if item not in self.browsed_urls:
            self.browsed_urls.append(item)
            self.items.insert(0,item)

    def get(self):
        try:
            return self.items.pop()
        except:
            return None

    def size(self):
        return len(self.items)

    def total_mapped(self):
        return len(self.browsed_urls)


def url_handling(url):
    if match(r'^%s' % browser_url, url):
        return url.replace(browser_url, '')
    return url


def is_internal_url(url):
    if match(r'^\/', url):
        return True
    return False


def sweep_response(response):
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_key('href'):
            _url = url_handling(link['href'])
            if is_internal_url(_url):
                q.put(_url)


def exec_thread(thread_name):
    while True:
        # if q.size() == 0:
        #     print "Hurray, no urls available to access. Let's drink some beer"
        #     break
        queue_get = q.get()
        if queue_get is not None:
            url = '%s%s' % (browser_url, queue_get)
            try:
                print "[Thread-%d] accessing %s" % (thread_name, url)
                resp = get(url, verify=False)
                sweep_response(resp.text)
            except:
                continue
        else:
            break


q = AccessQueue()

# Replace 10 for the number of threads 
for t in range(0, 10):
    print "Starting new Thread [%d]" % t
    thread.start_new_thread(exec_thread,(t,))
    time.sleep(5)


while True:
    print 'Queued Urls: %d' % int(q.size())
    print 'Mapped Urls: %d' % int(q.total_mapped())
    if q.size() == 0:
        print "Hurray, no urls available to access. Let's drink some beer"
        break
    time.sleep(10)
    pass
