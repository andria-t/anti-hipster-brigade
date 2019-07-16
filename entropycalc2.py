import numpy as np 
import pandas as pd 
import math
import matplotlib.pyplot as plt
import statistics

def entropy2(probs):
    """ Computes entropy of label distribution. """

    n_probs = len(probs)
    if n_probs <= 1:
        return 0

    ent = 0.
    # Compute entropy
    base = 2
    for i in probs:
        if i > 0:
            ent -= i * math.log(i, base)

    return ent

# Apply entropy function
def applyEntropy(df):
    """Apply entropy function to ALL businesses, given dataframe of probability vectors for each business."""
    ents = {}
    for v in df.iterrows():
        probs = v[1].tolist()
        #print(probs)
        ent = entropy2(probs)
        ents[v[0]] = ent

    entcol = pd.Series(ents, name = "entropy")
    entcol.index.set_names("business_id", inplace=True)
    rdf = pd.read_pickle("dataframes/allrestaurants.pkl")
    rdf = rdf.loc[:,['name', 'city','state', 'stars','address', 'is_open', 'latitude','longitude', 'categories', 'postal_code', 'review_count','RestaurantsPriceRange2','_ - attributes - RestaurantsAttire', '_ - attributes - Ambience']]
    edf = df.join([rdf, entcol], how = "inner")
    edf.to_pickle("./entropyframe.pkl")
    print(edf.head())
    
    
def showplot(df,city):
    data = np.array(df.loc[(df["city"]==city),"entropy"])
    plt.hist(data,bins=np.arange(min(data), max(data) + 0.01, 0.01))
    plt.title(city + " Restaurant Entropy Histogram")
    axes = plt.gca()
    axes.set_xlim([0.00, 2.00])
    plt.show()
    
df = pd.read_pickle("./entropyframe.pkl")


def makeboxes(df):
    """Plot all medians and variances in boxplot for all cities, sort by median"""
    df = df.pivot(columns = "city", values = "entropy")
    med = df.median().sort_values()
    df = df[med.index]
    df.plot.box(rot = 90)
    plt.title("Entropies of 54 Cities Sorted by Median")
    plt.ylabel("Entropy")
    plt.show()

makeboxes(df)








