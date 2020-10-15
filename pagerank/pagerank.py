import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    distribution = {}
    links_q = len(corpus[page])
    pages_q = len(corpus)


    if links_q == 0:
        for link in corpus:
            distribution[link] = 1 / pages_q
    else:
        for link in corpus:
            distribution[link] = ((1 - damping_factor) / pages_q)
        
        for link in corpus[page]:
            distribution[link] += damping_factor * (1/links_q)
        

    return distribution

    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    spagerank = {}
    current_page = random.choice(list(corpus.keys()))
    tm = transition_model(corpus,current_page,damping_factor)
    
    for page in corpus:
        spagerank[page] = 0
    
    #for the first page
    spagerank[current_page] += 1
    

    #loop for n times
    for i in range(n-1):
        current_page = choose(tm)
        spagerank[current_page] += 1


    #take the proportion of number of times / n
    for page in spagerank:
        spagerank[page] = spagerank[page] / n
    
    
    return spagerank
    
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ipagerank = {}
    ipagerank_old = {}
    N = len(corpus)
    
    #start with pagerank value for each page 1/N
    for page in corpus:
        ipagerank[page] = 1 / N
        ipagerank_old[page] = 1 / N

    loop = True
    
    while loop:

        for page in ipagerank:
            ipagerank_old[page] = ipagerank[page]
        
        for page in ipagerank:
            sumpr = 0


            for page_i in corpus:
                #calculating a page’s PageRank based on the PageRanks of all pages that link to it
                if page in corpus[page_i]:
                    sumpr += ipagerank_old[page_i] / len(corpus[page_i])
                
                #A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if len(corpus[page_i]) == 0:
                    sumpr += ipagerank_old[page_i] / len(corpus)


            total = (1 - damping_factor) / N + damping_factor * sumpr

            ipagerank[page] = total
        
            
        #This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values.
        for page in ipagerank:
            if math.isclose(ipagerank[page], ipagerank_old[page], abs_tol=0.001):
                loop = False
                


    return ipagerank
  
def choose(dist):
    r = random.random()
    sum = 0.0
    keys = dist.keys()
    for k in keys:
        sum += dist[k]
        if sum > r:
            return k
    return keys[-1]

if __name__ == "__main__":
    main()
