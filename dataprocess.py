import pandas as pd 
import numpy as np 
import pickle


def cutframe(df,N):
    """Cuts users with less than N reviews from dataframe df"""
    print(len(df))
    vc = df["user_id"].value_counts() #Series of frequencies of each user
    todrop = [uid for uid in vc.index if vc[uid] < N] #list of users with less than N reviews.

    boolist = df["user_id"].isin(todrop) #Boolean list of whether user at each index has under N reviews.
    indlist = df.index[boolist].tolist() #List of indices of users with under N reviews (applied boolean list)
    df.drop(indlist, inplace = True) #Drop users!
    df.to_pickle("./baseframe2.pkl")
    print(len(df)) #Checking to see whether it worked
    vc = df["user_id"].value_counts()
    vc2 = vc.value_counts().head()
    print(vc2)
    return(df)

def getTotalUsers(df):
    """Calculate price range distribution across whole dataframe"""
    dfPRcount = df.groupby(["user_id", "pricerange"])["pricerange"].agg({"frequency": "count"})
    print(dfPRcount.head())
    dfPRcount.to_pickle("./allusers.pkl")
    return dfPRcount


def normalize(udf):
    """Row-wise normalization, dividing each row in dataframe udf by its row total"""
    # unstack if dataframe is multilevel. 
    if isinstance(udf.keys(), pd.core.indexes.multi.MultiIndex):
        udf = udf.unstack(level = -1, fill_value = 0)
    ndf = udf.div(udf.sum(axis=1), axis= 0)
    return ndf


def bizprobs(bdf): 
    """Given dataframe of users, businesses, and normalized user vectors,
     calculates probabilities for entropy function for each business (normalized vector sums of users)"""
    #BIGFRAME was created with PD.MERGE on user vectors and edgelist
    bdf = pd.read_pickle("BIGFRAME.pkl") #Edgelist of users and businesses with business data AND user vectors

    bizgroups = bdf.groupby("business_id")[[('frequency', 1),('frequency', 2), ('frequency', 3), ('frequency', 4)]].agg("sum")
    normed = normalize(bizgroups) 
    print(normed.tail())
    normed.to_pickle("NORMBIGFRAME.pkl")




