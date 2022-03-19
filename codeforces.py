import requests
import json
import time

class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
    
    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1
        
    def dfs(self, node, prefix):
        """Depth-first traversal of the trie
        
        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
        
    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of 
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root
        
        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []
        
        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)


def search_problems(rating, userlist, tags):
    user_data = []

    for i in userlist:
        url = 'https://codeforces.com/api/user.status?handle=' + i + '&from=1&count=2000'  # all solved questions by the  user
        r = requests.get(url).content
        data = json.loads(r)
        user_data.append(data)


    solved = set()

    a = open("solved.txt", "r").read().split(" ")
    for i in a:
        solved.add(i)
    for i in user_data:
        for j in range(len(i['result'])):
            solved.add(str(i['result'][j]['problem']['contestId']) + str(
                i['result'][j]['problem']['index']))  # appending all the solved question by users in set
    lst = []
    url = " https://codeforces.com/api/problemset.problems?"  # downloding all the problems form codeforces
    if tags:  # not working need to fix this
        url += ';'.join(tags)
    r = requests.get(url).content
    itr = json.loads(r)

    rate = {}  # for storing the ratings for questions

    for i in itr['result']['problems']:
        res = str(i['contestId']) + "/" + str(i['index'])
        try:
            rate[res] = i['rating']
        except:
            pass

    for i in itr['result']['problemStatistics']:
        lst.append(i)
    lst = sorted(lst, key=lambda i: i['solvedCount'],
                 reverse=True)  # sorting the problems based on number of solved count
    return_list = []
    for k in rating:
        for i in lst:
            if str(i['contestId']) + str(
                    i['index']) not in solved:  # checking if any of the user has solved this problem
                res = str(i['contestId']) + "/" + i['index']
                try:
                    if rate[res] == k:  # matching the rating.
                        solved.add(str(i['contestId']) + str(i['index']))
                        return_list.append("https://codeforces.com/problemset/problem/" + res)
                        break
                except:
                    pass
    return return_list

# send_mess("******************************START**********************************")
userlist = ['Manhar_11','bugabooset']
rating = [800,900,1000,1100,1200]

lst = search_problems(rating, userlist, [])
for i in lst:
    print(i)
