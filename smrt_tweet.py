from twython import Twython
# import networkx as nx
# import text_utils as tu
# from nltk.corpus import stopwords
from matplotlib import pyplot as plt
import json

# http://stackoverflow.com/questions/19320197/twython-search-api-with-next-results/21644346#21644346
# https://twython.readthedocs.org/en/latest/usage/special_functions.html

API_KEY = 'ZCJvGQklUkXjbTvPRZbMMfij6'
API_SECRET = 'T31bAxymp6jLOtvM4HGt0uY9u5Z5DZyZ6JCxsoODbehzFpOCgL'

ACCESS_TOKEN = '1373167224-SZabBx6OG0uTqwtqR99HPOtzDPVr01aB42eXwqb'
ACCESS_TOKEN_SECRET = 'l1Z8gJ68jMdNpBnpNwHP8C28HdKne75olMNVuxiS0'


twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# words_to_remove = """with some your just have from it's /via &amp; that they your there this into providing system services sales"""
query='#SMRT'
# cachedStopWords = set(stopwords.words("english"))


tweets                          =   []
MAX_ATTEMPTS                    =   10
COUNT_OF_TWEETS_TO_BE_FETCHED   =   1000

for i in range(0,MAX_ATTEMPTS):
    # print i, "max_attempt"

    if(COUNT_OF_TWEETS_TO_BE_FETCHED < len(tweets)):
        break # we got 500 tweets... !!

    if(0 == i):
        # Query twitter for data. 
        results = twitter.search(q=query,count='100')
    else:
        # After the first call we should have max_id from result of previous call. Pass it in query.
        results = twitter.search(q=query,include_entities='true',max_id=next_max_id)

    # STEP 2: Save the returned tweets
    # print json.dumps(results['statuses'][0], sort_keys=True, indent =4)


    for result in results['statuses']:
        tweet_date = result['created_at']
        tweet_text = result['text'].encode('utf8')
        # tweets.append(tweet_text)

        tweet_dict = {'text':tweet_text, 'created_at':tweet_date}
        tweets.append(tweet_dict)

    # print len(tweets), 'length of tweets this page', i    


    # STEP 3: Get the next max_id
    try:
        # Parse the data returned to get max_id to be passed in consequent call.
        next_results_url_params  = results['search_metadata']['next_results']
        next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
        # print next_max_id
    except:
        # No more next pages
        break

print len(tweets), "number of tweets dict."
for item in tweets:
    print item['text'], item['created_at']


#u need the zero to tell the variable to store content of json as dict n not list. 
#tweet_dict is now a dictionary





# print tweet_dict['text']


# print tweet_list[:15]

# remove = tu.removal_set(words_to_remove, query)
# # remove = tu.removal_set(cachedStopWords, query)
# lines = tu.lines_cleanup([tweet.encode('utf-8') for tweet in tweets], remove=remove)
# words = '\n'.join(lines).split()

# wf = tu.word_freq(words)
# sorted_wf = tu.sort_freqs(wf)

# tu.summarize_freq_hist(sorted_wf)
# n_words = 10
# tu.plot_word_histogram(sorted_wf, n_words,"Frequencies for %s most frequent words" % n_words);

# n_nodes = 10
# popular = sorted_wf[-n_nodes:]
# pop_words = [wc[0] for wc in popular]
# co_occur = tu.co_occurrences(lines, pop_words)
# wgraph = tu.co_occurrences_graph(popular, co_occur, cutoff=1)
# wgraph = list(nx.connected_component_subgraphs(wgraph))[0]

# centrality = nx.eigenvector_centrality_numpy(wgraph)
# tu.summarize_centrality(centrality)

# for tweet in tweets:
#     print tweet

# print "Graph visualization for query:", query
# tu.plot_graph(wgraph, tu.centrality_layout(wgraph, centrality), plt.figure(figsize=(8,8)),
#     title='Centrality and term co-occurrence graph2, q="%s"' % query)
# plt.show()









