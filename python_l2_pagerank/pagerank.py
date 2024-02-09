import os
import random
import re
import sys

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

### Test ###
#corpus = crawl("corpus0")
#print(f'################corpus content {corpus}')
#page="4.html"
damping_factor = DAMPING


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #print('############ transition function ##############')
    N = len(corpus)
    numlinks_i = len(corpus[page])
    #print(f'numlinks_i: {numlinks_i}')
    new_prob = dict()
    
    #Iterate over all html pages
    for pr in corpus:
        new_prob[pr] = ((1 - damping_factor) / N)
        #Iterate over all linkes within a html page
        for link in corpus[page]:
            #If there is a link for page x add probability
            if link == pr:
                new_prob[pr] += (damping_factor / numlinks_i)
        new_prob[pr] = round(float(new_prob[pr]), 4)
    return new_prob

### Test ###
#transition = transition_model(corpus, page, damping_factor)
#print("################# transition output example 2.html#########")
#print(transition)
n = SAMPLES

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print("############### iteration ##############")
    # Chose random page as starting point
    random_page = random.choice(list(corpus.keys()))
    # Initialize object to iteratively update it
    new_page = random_page
    # Initialize dictionary and set values to zero
    output = {key: 0 for key in corpus}
    
    # loop over number of samples
    for p in range(n):
        # get probabilites depending on page
        tr = transition_model(corpus, new_page, damping_factor)
        population = tr.keys()
        weights = tr.values()
        # choose next page randomly given probabilities for each page depending on which page we are currently
        choice = random.choices(list(population), weights, k = 1)
        #print(f' choice from loop:  {choice}')
        # update new page given by the result of choice
        new_page = choice[0]
        # add 1 to the output dictionary. This dict count how often a page was visited
        output[choice[0]] += 1
        result = {key: round(value / n, 3) for key, value in output.items()}
    return result

### Test ###
#print(f'n: {n}')
#s = sample_pagerank(corpus, damping_factor, n)
#print(f'output: {s}')

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print("################iterate_pagerank ###########")
    diff_check = False
    j = 0
    # Set initial probablities equally distributed
    N = len(corpus)
    pr_p = {key: 1/N for key in corpus}
    # Start while loop until difference between current and new probability is less than 0.001
    
    while diff_check is not True and j < 44442:
        j += 1
        new_pr_p = dict()
        
        # iterate over pages P in corpus
        for page in corpus:
            #print(f' probabilites: {pr_p}')
            #print(f'length corpus: {len(corpus)}')
            #print(f'damping factor: {damping_factor}')
            #print(f'current page as example: {page}')
            # Welche linkpages hat die current page
            # Anzahl links der page
            
            # iterate over pages i within page P, check if P is in i and get number of links within i
            page_i = dict()
            for key, value in corpus.items():
                numLinks_i = len(value)
                for i in value:
                    #print(i)
                    if i == page:
                        #print("###########")
                        #print(f' key from pages: {key}')
                        #print(f' values from pages: {value}')
                        #print(f'nbr of links from current page {numLinks_i}')
                        #print(f'Found link from page: {i}')
                        page_i[key] = numLinks_i
                #print(f'page_i: {page_i}')
            #print(f' page i: {page_i}')

            # get sum of values: Probabilty(i) / numberofLinks
            pr_i_divby_numLinks_i = {key: pr_p[key] / page_i[key] for key in set(pr_p) & set(page_i)}
            sum_of_pr_i_divby_numLinks_i = sum(pr_i_divby_numLinks_i.values())

            #print(f'sums: {sum_of_pr_i_divby_numLinks_i}')
            #pr_p[page] = ((1 - damping_factor) / len(corpus)) + damping_factor * (page_i["1.html"] / page_i.values())
            
            #Get new Probability for page P
            new_pr_p[page] = round(((1 - damping_factor) / N) + damping_factor * sum_of_pr_i_divby_numLinks_i, 3)
            
        # Check if the absolute difference between values is less than 0.001
        check_difference = all(round(abs(pr_p[key] - new_pr_p[key]), 3) <= 0.001 for key in set(pr_p) & set(new_pr_p))
            
        # if check_difference is true, return probabilites and stop while loop
        if check_difference:
            #print('No diff more than 0.001')
            diff_check = True
            return pr_p
        #print(f'check difference: {check_difference}')
        
        # update pr_p with new probabilities
        pr_p = new_pr_p
        #print(f' new probabilies:  {pr_p}')
                
#b = iterate_pagerank(corpus, damping_factor)

if __name__ == "__main__":
    main()
