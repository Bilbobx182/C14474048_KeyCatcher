#!/usr/bin/python
import praw
import os

#variables used
r = praw.Reddit(user_agent = "bilbobx182 crawler")
r.login("NAME","PASS")
sub ="subreddit"
limit =5
combo = 0
switch = False
key = ""
keylist=[]

#Checking to see if I replied to it
if not os.path.isfile("posts_replied_to.txt"):
    repliedposts = []
else:
    with open("posts_replied_to.txt", "r") as u:
        repliedposts = u.read()
        repliedposts = repliedposts.split("\n")
        repliedposts = filter(None, repliedposts)

subreddit = r.get_subreddit(sub)
for submission in subreddit.get_new(limit=limit):

   # print(submission.title)
    contents = submission.selftext.split()
   # print(contents)
    for word in contents:
        if (combo < 9):
            if(combo == 5):
                if(word != "-"):
                    break

            if word != "-" and switch == False:
                key = key + word
                combo += 1
                switch = True
            elif "-" == word and switch == True:
                key = key + word
                combo += 1
                switch = False
            else:
                combo = 0
                key = ""
                switch=False

    if(combo==5 or combo ==9):
        if (key not in keylist):
            keylist.append(key)
            if(submission.id not in repliedposts):
                print("Bot replying to : ", submission.title)
                submission.add_comment("I detected a plain text key!")
                submission.delete()
                print(keylist)

with open("posts_replied_to.txt", "a") as f:
    for post_id in repliedposts:
        f.write(post_id + "\n")