#--------------------------------------------------------------------------------------
# #Filename: IRIS_StudentClassification_Views_CL_2.py
#Description: This python code K-Means cluster classification for course and level
#with cluster size as 3
#--------------------------------------------------------------------------------------

import numpy as np
from matplotlib import pyplot as plt
from sklearn import cluster
from sklearn import preprocessing

import os

from src import SQLLite_LoadData as db

le = preprocessing.LabelEncoder()

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

def loadData() :

    #Read Data
    df = db.loadData("user_course_views")
    df.head()

    # select only first 5 columns
    df = df.iloc[:,0:5]

    # remove author handle and view date columns
    df = df.drop(['view_date','author_handle'], 1)
    df.head()

    # Convert the string data to numeric series
    df["course_id"] = le.fit_transform(df["course_id"])
    df["level"] = le.fit_transform(df["level"])

    # remove duplicates
    df = df.drop_duplicates(subset=['user_handle', 'course_id','level'], keep=False)
    return(df)

    # Remove header row
    df = df.iloc[1:]

def prepareModel(df) :
    # prepare model classifier
    x = df['course_id']
    y = df['level']
    X = np.array(list(zip(x,y)))

    k_means = cluster.KMeans(n_clusters=3)
    model = k_means.fit(X)

    centroids = k_means.cluster_centers_
    labels = k_means.labels_
    return(model,x,y)

def generatePlot(model,x,y) :
    # generate plot:
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.title('User Course Views Classification by Course Ids')
    plt.xlabel("course_id")
    plt.ylabel("level")
    plt.scatter(x, y, c=model.labels_.astype(float))
    #plt.show()

    # Now, save the plot to directory
    image_filename = "./../img/IRIS_StudentClassification_Views_UL_1.png"

    ## if image file exists, delete it ##
    if os.path.isfile(image_filename):
        os.remove(image_filename)

    fig.savefig(image_filename)  # save the figure to file
    plt.close()
    return (image_filename)

def classify_CL():

    print("Running  - IRIS_StudentClassification_Views_CL_2.py")

    df = loadData()
    model,x,y = prepareModel(df)
    image_filename = generatePlot(model,x,y)
    return(image_filename)
