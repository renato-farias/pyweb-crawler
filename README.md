# pyweb-crawler

pyweb-crawler is a crawler developed to access every link inside an URL. It sweeps recursively the URLs and stores them in a queue where it will be accessed then the new ones will be discovered and stored too. .... and go on.... 

## Using
Edit the crawler.py replacing the following line with you personal settings:

    browser_url = 'http://www.mywebsite.com'
 
and

    for t in range(0, 50): # where 50 is the number of threads
    

... then, execute it

    python crawler.py
    
    
## TODO (not priorized)

* Parameterize all options like URL to Browse, Number of threads, Timeouts, etc
* Improve the logs
* Manage the threads not used
* Set the max number of URLs to be accessed
