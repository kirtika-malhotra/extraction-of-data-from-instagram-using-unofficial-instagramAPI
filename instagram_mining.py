#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password
import requests
import pickle
import time
import numpy as np
from InstagramAPI import InstagramAPI
import imageio
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import operator
api = InstagramAPI(username="YOUR-USERNAME", password="YOUR PASSWORD")
if (api.login()):
    api.getSelfUserFeed()  # get self user feed
    encoded = str.encode("utf-8", errors='ignore')
    print("Login success!")
    api.getProfileData()
    result = api.LastJson.keys()
    my_id = api.LastJson['user']['pk']    #[u'username', u'phone_number', u'has_anonymous_profile_picture', u'hd_profile_pic_versions', u'gender', u'show_conversion_edit_entry', u'birthday', u'external_lynx_url', u'profile_pic_url', u'profile_pic_id', u'biography', u'full_name', u'pk', u'hd_profile_pic_url_info', u'is_verified', u'email', u'is_private', u'external_url']
    print("My Id: "+str(my_id))
    api.getUsernameInfo(my_id)

   
    #to get media
    n_media = api.LastJson['user']['media_count']
    print("Number of posts: "+str(n_media))
    
    #to get media feeds
    media_ids = []
    max_id = ''
    
    for i in range(int(n_media)):
        api.getUserFeed(usernameId=my_id, maxid = max_id)
        media_ids += api.LastJson['items']
        print(str(media_ids[i]['pk']))
        
        if api.LastJson['more_available']==False:
            print ("no more avaliable")            
            break
        max_id = api.LastJson['next_max_id']
        
        print (str(i)+" next media id = "+ str(max_id)+"  "+str(len(media_ids)))
        time.sleep(3)           
    
      
    #We will go throw all media and collect media likers:
    likers = []
    m_id = 0

    #the loop will take some time to run
    for i in range(len(media_ids)):
        print("Waiting...")
        m_id = media_ids[i]['id']
        api.getMediaLikers(m_id)
        likers += [api.LastJson]
        time.sleep(2)
    print ("done!")


    #sort users and count all likes of unique user:
    users = []
    for i in likers:
        users += map(lambda x: i['users'][x]['username'],range(len(i['users'])))
        #print("users: "+str(users))
    users_set = set(users)
    print ("all users = "+ str(len(users))+" unique users = "+ str(len(users_set)))


    #GETTING USERS FOLLOWERS AND USER FOLLWING
    api.getUserFollowings(my_id)
    print ("User followings: "+str(len(api.LastJson['users'])))
    following_list=api.LastJson['users']
    for i in range(len(following_list)):
        following=following_list[i]['full_name']
        print("Following: "+str(following.encode('utf8')))

    api.getUserFollowers(my_id)
    print ("Users Followers: "+str(len(api.LastJson['users'])))
    followers_list=api.LastJson['users']
    for i in range(len(followers_list)):
        follower=followers_list[i]['full_name']
        print("Followers: "+str(follower.encode('utf8')))



    followers   = []
    next_max_id = True
    while next_max_id:
        print (next_max_id)
    #first iteration hack
        if next_max_id == True:
            next_max_id=''
            _ = api.getUserFollowers(my_id,maxid=next_max_id)
            followers.extend ( api.LastJson.get('users',[]))
            next_max_id = api.LastJson.get('next_max_id','')
            time.sleep(1) 
    
    followers_list=followers


    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    print ("Number of Following: "+str(len(following_set)))

    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    print ("Number of Followers: "+str(len(followers_set)))


    #Make a dict with information of likes per user:
    l_dict = {}
    for user in users_set:
   #l_dict structure - {username:number_of_liked_posts}
        l_dict[user] = users.count(user)
 


    #to plot the graph for only top 10 users
    all_pairs = sorted(l_dict.items(), key=operator.itemgetter(1))
    n_users = 10        # top 10 users
    pairs = all_pairs[-n_users:]
    print(pairs)
    


    y = list(map(lambda y: pairs[y][1], range(len(pairs))))
    x = list(map(lambda y: pairs[y][0], range(len(pairs))))
    fig = plt.figure()
    plt.xkcd()
    plt.xticks(range(len(pairs)), x, rotation='vertical')
    plt.ylim([0, 160])
    width=1/1.5
    plt.bar(range(len(y)), y, width, color='red')
    plt.xlabel('USERS')
    plt.ylabel('number of liked posts')
    plt.show()
else:
    print("Can't login!")


