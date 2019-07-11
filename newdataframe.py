import numpy as np 
import pandas as pd 
from scipy import sparse
import pickle 
"""
#Read data, create pickle for speed - DONE
df = pd.read_csv("business.csv") 
df.to_pickle("./allrestaurants.pkl")
"""
#Read pickle - restaurants for top 54 cities, all of them have price range data. 
rdf = pd.read_pickle("allrestaurants.pkl")

#Opening reviews file, chunks of size 1000
r_reader = pd.read_json("data/review.json", lines = True, chunksize = 1000) 
count = 0 #Counter for tracking time/making sure function is running
users = {} #dict to access user indices
bizs = {} #dict to access biz indices
u_ind = []
b_ind = []
bizids = rdf.get('business_id')
for chunk in r_reader: #Loop thru reviews
        inlist = chunk['business_id'].isin(bizids) #Boolean series of whether biz id is in precalculated list\n",
        for x in chunk[inlist].itertuples(): #iterate through chunk, each review is a tuple
                biz = str(x[1]) #Retrieve user and business IDs
                user = str(x[-1]) 
                uindex = users.setdefault(user, len(users)) #adds user to users dictionary and/or returns position
                u_ind.append(uindex) #appends index of user ID to index list
                bindex = bizs.setdefault(biz, len(bizs))
                b_ind.append(bindex)
                count+=1
                print(count)

#array of ones for data, of length of index lists
data = np.ones(len(u_ind), dtype = int)
#Constructing sparse matrix - rows are users, columns are businesses. 
mat = sparse.coo_matrix((data, (u_ind, b_ind)))
#Pickling (saving) matrix for later. 
sparse.save_npz("basematrix", mat) 
#Saving dictionaries.
with open('userindex.p', 'wb') as up:
        pickle.dump(users,up, protocol = pickle.HIGHEST_PROTOCOL)
with open('bizindex.p','wb') as bp: 
        pickle.dump(bizs, bp, protocol=pickle.HIGHEST_PROTOCOL)