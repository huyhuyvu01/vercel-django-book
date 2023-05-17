
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import os
import warnings
warnings.filterwarnings("ignore")

from main_app.models import Books, Ratings
from users.models import CustomUser
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count, Q
import datetime
import random

def NameOfBookByUser(UserIdInput):
    RatingAlowed = [7,8,9,10]
    GetBookName = pd.DataFrame(Ratings.objects.filter(Q(user_id=UserIdInput)&Q(rating__in=RatingAlowed)).values())
    GetFinalISBN = random.choice(list(GetBookName["ISBN"]))
    GetFinalName = Books.objects.filter(ISBN=GetFinalISBN).values("title")
    return GetFinalName

def NameOfBookByUnratedUser():
    RatingObj1 = Ratings.objects.values("ISBN")\
        .annotate(count=Count("ISBN")).filter(count__gt=50).values_list('ISBN',flat=True)
    RatingObj2 = pd.DataFrame(Ratings.objects.filter(ISBN__in=RatingObj1).values())
    BookObj = pd.DataFrame(Books.objects.filter(ISBN__in=RatingObj1).values())
    ratings_with_name = RatingObj2.merge(BookObj,on='ISBN')
    ratings_with_name.drop(columns=["ISBN","img_s","img_m"],axis=1,inplace=True)
    FinalNameDf = ratings_with_name[["title","rating"]].groupby("title").mean().sort_values(by="rating", ascending=False).reset_index().head(10)
    FinalName = list(FinalNameDf["title"])
    FinalName = random.choice(FinalName)
    return FinalName


def GetBestStarBooks(BookObj):
    ratings_with_title = BookObj[["title","author",'img_l','total_rating']].sort_values(by="total_rating",ascending=False).head(9)
    ratings_with_title.drop(columns=["total_rating"],inplace=True)
    data = []
    
    for i in ratings_with_title.values:
        item = []
        item.extend(i)
        data.append(item)
    return data




def recommend(booksDf, pt, similarity_score, book_name="Angelas Ashes"):
    index = np.where(pt.index==book_name)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1], reverse=True)[0:9]
    
    data = []
    
    for i in similar_books:
        item = []
        temp_df = booksDf[booksDf['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['img_l'].values))
        
        data.append(item)
    return data
    # title = []
    # author = []
    # imgl = []
    # for i in similar_books:
    #     temp_df = booksDf[booksDf['title'] == pt.index[i[0]]]
    #     title.append(temp_df.drop_duplicates('title')['title'].values[0])
    #     author.append(temp_df.drop_duplicates('title')['author'].values[0])
    #     imgl.append(temp_df.drop_duplicates('title')['img_l'].values[0])
        
    # return title, author, imgl

def GetData2Recommend():
    RatingObj1 = Ratings.objects.values("ISBN")\
        .annotate(count=Count("ISBN")).filter(count__gt=50).values_list('ISBN',flat=True)
    RatingObj2 = pd.DataFrame(Ratings.objects.filter(ISBN__in=RatingObj1).values())
    BookObj = pd.DataFrame(Books.objects.filter(ISBN__in=RatingObj1).values())
    ratings_with_name = RatingObj2.merge(BookObj,on='ISBN')
    ratings_with_name.drop(columns=["ISBN","img_s","img_m"],axis=1,inplace=True)
    pt = ratings_with_name.pivot_table(index='title',columns='user_id'
                          ,values='rating')
    pt.fillna(0,inplace=True)
    similarity_score = cosine_similarity(pt)
    return BookObj, pt, similarity_score

def loadData():
    RatingObj = Ratings.objects.values("ISBN")\
        .annotate(count=Count("ISBN")).filter(count__gt=50).values_list('ISBN',flat=True)
    BookObj = Books.objects.filter(ISBN__in=RatingObj)
    #print(BookDf.info())
    # ratings_with_name = RatingsDf.merge(BookDf,on='ISBN')
    # ratings_with_name.drop(columns=["ISBN","img_s","img_m"],axis=1,inplace=True)
    # CustomUserDf.rename(columns={"id":"user_id"}, inplace=True)
    # ratings_with_name["user_id"] = ratings_with_name["user_id"].astype('int')
    # complete_df = ratings_with_name.merge(CustomUserDf, on="user_id")
    # x = complete_df.groupby('user_id').count()['rating']>200
    # knowledgable_users = x[x].index
    # filtered_rating = complete_df[complete_df['user_id'].isin(knowledgable_users)]
    # y = filtered_rating.groupby('title').count()['rating']>=50
    # famous_books = y[y].index
    # final_ratings =  filtered_rating[filtered_rating['title'].isin(famous_books)]
    # final_ratings = final_ratings.to_dict(orient='records')
    return BookObj

