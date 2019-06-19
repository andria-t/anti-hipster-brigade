import numpy as np 
import pandas as pd 
import networkx as nx #Importing libraries

#Opening business info. Indicates multiple json objects, and that it must be read in chunks
b_reader = pd.read_json("business.json", lines=True, chunksize = 1000) 
b_ids = pd.Series() #empty series for storing biz ids
for chunk in b_reader: #Loop through chunks in business info
    #print(chunk[['business_id','categories']]) #Print categories and biz ids
    cat = chunk['categories'].str.contains("Restaurants") #Series of booleans of whether "restaurants" is one of the categories
    goodcats = chunk['categories'].notna() #Series of businesses where "category" is not empty
    city = chunk['city'] == "Phoenix" #Series of booleans of whether the city is Phoenix
    b_ids = b_ids.append(chunk[city & cat & goodcats]['business_id'], ignore_index=True) #If restaurant AND not null AND in phoenix, add to biz id list
    #print(chunk[goodcats & cat]['categories'])

with open('biznodes', 'w') as f:
    for item in b_ids:
        f.write("biz_" + str(item) + "\n")


#print(len(b_ids))
#Opening reviews file, chunks of size 1000
r_reader = pd.read_json("review.json", lines = True, chunksize = 1000) 

count = 0
efile = open('edge','w') 
for i, chunk in enumerate(r_reader): #Loop thru reviews
    inlist = chunk['business_id'].isin(b_ids) #Boolean list of whether biz id is in precalculated list\n",
    print(i)
    for x in chunk[inlist].itertuples(): #iterate through chunk, each review is a tuple
        s1 = "biz_" + str(x[1]) #Convert user and biz id from tuple to string
        s2 = "user_" + str(x[-1])
        efile.write(s1 + " " + s2 + "\n") #write to file
        print(count)
        count+=1
efile.close()

