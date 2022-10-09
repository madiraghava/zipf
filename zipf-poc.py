# The POC program will have the user supply a Discord server and will return the Zipf constant
# for the number of messages per user. In addition, it will publish the raw messages/user data to a file under
# the name (serverid).txt and chart the Pareto distribution

import pip._vendor.requests
import json
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import os

def messages_from_author(author_id, guild_id, authorization):
  header = {
    'authorization': authorization
  }
  url = "https://discord.com/api/v9/guilds/" + guild_id + "/messages/search?author_id=" + author_id
  r = pip._vendor.requests.get(url, headers = header)
  jsonn = json.loads(r.text)
  try:
    num = jsonn["total_results"]
    print(num)
    return num
  except:
    if jsonn['message'] == 'The resource is being rate limited.':
      print("RATE LIMITED. WAITING " + str(jsonn['retry_after'] + 20) + " SECONDS")
      time.sleep(jsonn['retry_after'] + 20)
      return messages_from_author(author_id, guild_id, authorization)
    else:
      print(str(jsonn))
      return 0

def collect_authors():
  har_file = input("HAR file path: ").replace("\"","") #Head to server, scroll through all users on sidebar, and enter developer tools, click on network and type cdn.discordapp.com/avatar. Then, settings and save HAR file
  har = open(har_file, "r")
  lines = har.read()
  authors = list(set(re.findall(r'https://cdn.discordapp.com/avatars/(\d*)', lines)))
  return authors


def display_zipf(nums):
  fig, axs = plt.subplots(2)
  vals = [*range(1, len(nums)+1, 1)]
  axs[0].loglog(list(vals), list(nums), 'o')
  axs[1].bar(list(vals), list(nums), color = "maroon", width = 0.3)
  plt.show()

def display_zipf_from_file(file):
  with open(str(file),'r') as inf:
    dict = eval(inf.read())
  nums = sorted(dict.values(), reverse = True)
  display_zipf(nums[8:])

def get_pareto_from_file(file):
  with open(str(file),'r') as inf:
    dict = eval(inf.read())
  nums = sorted(dict.values(), reverse = True)
  total_sum = 0
  for num in nums:
    total_sum += num
  nums_in_twenty_percent = len(nums)//5
  twenty_percent_sum = 0
  for i in range(nums_in_twenty_percent + 1):
    twenty_percent_sum += nums[i]
  rv = round(twenty_percent_sum/total_sum,2) * 100
  print("Twenty percent of the users account for " + str(rv) + " percent of the messages")
  return rv



def collect_messages_data(display):
  guild_id = input("guild-id:")
  authorization = "NzcxNjMyODMwOTE1ODA1MjI1.YclutA.yv2tQBQGoQ3cMg4LmEKfkp_Pi6g" # Search "How to get discord token"
  authors = collect_authors()
  print(authors)
  print("num_authors: " + str(len(authors)))
  print("est time: " + str(int(((len(authors) * 3)/60) + ((len(authors)//50) * 2))))
  dict = {}
  i = 1
  for author in authors:
    time.sleep(3)
    dict[author] = messages_from_author(author, guild_id, authorization)
    print(str(i) + "/" + str(len(authors)) + " " + str(author) + " " + str(dict[author]))
    i += 1
  print(dict)
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  f = open(str(guild_id) + ".txt", "w")
  f.write(str(dict))
  f.close()
  if display == True:
    display_zipf(sorted(dict.values(), reverse = True))
  

#get_pareto_from_file(r"C:\Users\madir\Documents\Miscellanious\Python\Zipf's Project\746696734473846796.txt")
#collect_messages_data(display = True)
display_zipf_from_file(r"C:\Users\madir\Documents\Miscellanious\Python\Zipf's Project\863391096461459457.txt")
#collect_authors()
#messages_from_author("776968841108520961", "880905845674745907", "NzcxNjMyODMwOTE1ODA1MjI1.YclutA.yv2tQBQGoQ3cMg4LmEKfkp_Pi6g")
