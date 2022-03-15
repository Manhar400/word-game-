import requests
import json
import time


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
