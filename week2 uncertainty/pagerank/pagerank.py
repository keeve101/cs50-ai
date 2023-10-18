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

    trying = transition_model(corpus, "1.html", DAMPING)
    print(trying)
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
    p_d = {}
    outgoing_links = len(corpus[page])
    random_probability = (1 - damping_factor)/len(corpus)


    for key in corpus.keys():
        p_d[key] = random_probability
        if key in corpus[page]:
            p_d[key] += damping_factor/outgoing_links
    
    return p_d


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pr_dict = {}
    pages_ls = list(corpus.keys())
    num_pages = len(pages_ls)
    p_d = transition_model(corpus, random.choice(pages_ls), damping_factor)
    p_d_list = list(p_d.values())
    random_probability = (1 - damping_factor)/num_pages

    for key in pages_ls:
        pr_dict[key] = 1/num_pages

    while n > 1:
        n -= 1
        page_sampled = random.choices(pages_ls, weights= p_d_list)[0]
        pr_dict[page_sampled] = random_probability 
        for i in corpus.keys():
            if page_sampled in corpus[i]:
                num_links = len(corpus[i])
                pr_dict[page_sampled] += damping_factor * (pr_dict[i]/num_links)
        
        p_d = transition_model(corpus, page_sampled, damping_factor)
        p_d_list = list(p_d.values())

    return pr_dict
    #bruh

        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr_dict = {}
    pages_ls = list(corpus.keys())
    num_pages = len(pages_ls)
    for key in pages_ls:
        pr_dict[key] = 1/num_pages


if __name__ == "__main__":
    main()
