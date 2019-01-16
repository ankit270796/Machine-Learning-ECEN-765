# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KE1cFjARL_TemdSLzih1Fgeo7i07cIfw
"""

### imports ###
###############

import random
import numpy as np
import pandas as pd 
import zipfile
import requests

from numpy import array
from sklearn.metrics.pairwise import pairwise_distances
from random import randint 
from scipy.stats import pearsonr

### Downloading the Database ###
#url = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
#r = requests.get(url, allow_redirects=True)
#open('ml-100k.zip', 'wb').write(r.content)


#opener, mode = tarfile.open, 'r:zip'
#cwd = os.getcwd()

### Funtions ###
def readUserDataset(FilePath):
  head=['UserId','ItemId','Rating','Timestamp']
  return pd.read_csv(FilePath, sep='\t', names=head)

def NumUsers(Dataset):
  return Dataset.UserId.unique().shape[0]

def NumMovies(MovieDataset):
  return MovieDataset.ItemId.unique().shape[0]

def CreateUserItemMat(NumUsers,NumItems,Dataset):
  matrix=np.zeros((NumUsers, NumItems))
  for rating in Dataset.itertuples():
    
    matrix[rating[1]-1,rating[2]-1]=rating[3]    ### storing a rating corresponding to a user
  return matrix

def PearsonCorrelation(UserItemMatrix):
  similarity=1-pairwise_distances(UserItemMatrix, metric='correlation')
  
  similarity[np.isnan(similarity)]=0
  return similarity

def CalculateSimilarity(test, train, num_test, num_train):
  similarity=np.zeros((num_test,num_train))
  
  for i in range(0,num_test):
    for j in range(0,num_train):
      [p,r]=pearsonr(test[i,:],train[j,:])
      similarity[i,j]=p 
      similarity[np.isnan(similarity)] = 0
      
  return similarity

def InitialRecRandom(test_ratings,num_movies,num_movies_rate):
  #### ratings given by the user to presented movies ####
  final=np.zeros(test_ratings.shape)
  for i in range(test_ratings.shape[0]):
    
    random_rec=random.sample(range(0, num_movies), num_movies_rate)
    for j in random_rec:
      final[i,j]=test_ratings[i,j]
  
  return final
  

def Predict(train_ratings, test_ratings, similarity, k):  ### predicts with no bias term
  pred = np.zeros(test_ratings.shape)
  test_user_bias= test_ratings.mean(axis=1)
  train_user_bias= train_ratings.mean(axis=1)
  
  train_ratings=(train_ratings-train_user_bias[:,np.newaxis]).copy()
  
  for i in range(test_ratings.shape[0]):
    
    KTopUsers=[np.argsort(similarity[:,i])[:-k-1:-1]]
    
    for j in range(test_ratings.shape[1]):
      pred[i,j]=similarity[i,:][KTopUsers].dot(train_ratings[:,j][KTopUsers])
      pred[i,j]/=np.sum(np.abs(similarity[i,:][KTopUsers]))
      
  pred+= test_user_bias[:,np.newaxis]
  return pred


#### supporting functions for the demographics #####
def ReadDemography(path):  
    with zipfile.ZipFile(path) as datafile:  
      return datafile.read('ml-100k/u.user').decode(errors='ignore').split('\n') 
    
def CreateMetadeta(rawDemo, users_age, users_occup,users_meta_data):
  for user in rawDemo:
    if not user: 
      continue
      
    splt=user.split('|')
    userid=int(splt[0])
    age = int(splt[1])
    gender = splt[2]
    occup = splt[3] 
    
    i=0
    for m in users_age:
      if(age <= int(m)):
        break ##user belongs to this group
      else:
        i=i+1
    
    if(gender=='M'):
      j=8
    else:
      j=9
    
    k=10
    for temp in users_occup:
      if(occup==temp):
        temp
      else:
        k=k+1
        
    s= str(userid)+"|"
    for l in range (0,31):
      if(l==i or l==j or l==k):
        s=s+"1|"
      else:
        s=s+"0|"
        
    s=s[:-1]
    users_meta_data.append(s)
    
  return users_meta_data 
    
def DemMatrix(users_meta,num_users):
  dem_matrix=np.zeros((num_users,30))
  i=0
  
  for user in users_meta:
    splt=user.split('|')
    
    for j in range (1,31):
      dem_matrix[i,j-1]=int(splt[j])
    i=i+1
    
  return dem_matrix

def InitialRec(train_ratings, test_ratings, similarity, k, num_movies_rate): #### demographic similarity
  pred = np.zeros(test_ratings.shape)
  #test_user_bias= test_ratings.mean(axis=1)
  #train_user_bias= train_ratings.mean(axis=1)
  #train_ratings=(train_ratings-train_user_bias[:,np.newaxis]).copy()
  
  for i in range(test_ratings.shape[0]):
    
    KTopUsers=[np.argsort(similarity[:,i])[:-k-1:-1]]
    for j in range(test_ratings.shape[1]):
      
      pred[i,j]=similarity[i,:][KTopUsers].dot(train_ratings[:,j][KTopUsers])
      pred[i,j]/=np.sum(np.abs(similarity[i,:][KTopUsers]))
  #pred+= test_user_bias[:,np.newaxis]
  
  #### ratings given by the user to presented movies ####
  final=np.zeros(test_ratings.shape)
  for i in range(test_ratings.shape[0]):
    topKrec=[np.argsort(pred[:,i])[:-num_movies_rate-1:-1]]
    
    for j in topKrec:
      final[i,j]=test_ratings[i,j]
      
  final[np.isnan(final)] = 0
  return final

def CalcRMSE(V1,V2):
  temp=0
  V1[np.isnan(V1)] = 0
  V2[np.isnan(V2)] =0
  
  for i in range(0,V1.shape[0]):
    for j in range(0,V1.shape[1]):
      temp=temp+pow(V1[i,j]-V2[i,j],2)
      
  temp=temp/(V1.shape[0]*V1.shape[1])
  rmse=pow(temp,1/2)
  return rmse

def HitRate(test_ratings, predicted, k):
  total_ratings=(test_ratings.shape[0])*k
  miss=0
  for i in range(test_ratings.shape[0]):
    topK=[np.argsort(predicted[i,:])[:-k-1:-1]]
    zero_els = np.count_nonzero(test_ratings[i,topK]==0)
    miss=miss+zero_els 
  
  hit_rate=1-miss/total_ratings
  return hit_rate

##### Basic Part #####
#### reading the dataset #######
Dataset=readUserDataset("u.data")

#UserDataset.tail()  
#UserDataset.head()  

num_users=NumUsers(Dataset)
num_movies=NumMovies(Dataset)

#### creating the user item matrix ####
user_item_mat=CreateUserItemMat(num_users,num_movies,Dataset)

#### Splitting the dataset into 80:20 training vs test dataset ####
num_test_users=round(0.2*num_users)
num_train_users=num_users-num_test_users



k=[10,50,100,150] ###### Neighborhood size
movie_set_size=[15,30,45,60] ##### Number of Movies shown to the user
#### to store the result #####
basic_result=np.zeros((4,4))
basic_hitrate=np.zeros((4,4))

i=0
for group_size in k:
  j=0
  for num_movies2rate in movie_set_size:
    temp_rmse=0
    hit_rate=0
    for iter in range(0,1):
      seperator=random.sample(range(0, num_users), num_users)
      
      #### grouping the users into test and training sets
      test_users=array(seperator[:num_test_users])
      train_users=array(seperator[num_test_users:])
      
      #### creating test and train user item matrix ####
      test_user_item=user_item_mat[test_users,:]
      train_user_item=user_item_mat[train_users,:]
      
      ##### creating similarity matrix #####
      similarity=CalculateSimilarity(test_user_item, train_user_item, int(num_test_users), int(num_train_users))
      
      ##### Initial set of movies for ask2rate approach
      ask2rate=InitialRecRandom(test_user_item, num_movies, num_movies2rate)
      
      ##### calculating the predictions #####
      predictions=Predict(train_user_item, ask2rate, similarity, group_size)
      
      #temp_rmse=temp_rmse + CalcRMSE(predictions,test_user_item)
      
      hit_rate=hit_rate+HitRate(test_user_item, predictions, num_movies2rate)
    
    print("Group size: {0}, No of Movies to rate: {1} Hit-Rate: {2}".format(group_size,num_movies2rate,hit_rate))  
    #basic_result[i,j]=temp_rmse
    
    basic_hitrate[i,j]=hit_rate
    j=j+1
  i=i+1
    
    
print(basic_result)

##### Demography Based #####
demography=ReadDemography("ml-100k.zip")

#### reading the dataset #######
Dataset=readUserDataset("u.data")

Dataset.tail()  
Dataset.head()  

num_users=NumUsers(Dataset)
num_movies=NumMovies(Dataset)



##### create metadata for the demographics #####
users_age = ['18', '24', '30', '40', '50', '61', '70', '100'] 
users_occup = ['administrator', 'artist', 'doctor', 'educator', 'engineer', 'entertainer', 'executive', 'healthcare', 'homemaker','lawyer', 'librarian', 'marketing', 'none', 'other', 'programmer', 'retired', 'salesman', 'scientist', 'student', 'technician', 'writer']
users_combined_features = ['18|0', '24|1', '30|2', '40|3', '50|4', '61|5', '70|6', '100|7', 'm|8', 'f|9', 'administrator|10', 'artist|11', 'doctor|12', 'educator|13', 'engineer|14', 'entertainer|15', 'executive|16', 'healthcare|17', 'homemaker|18', 'lawyer|19', 'librarian|20', 'marketing|21', 'none|22', 'other|23', 'programmer|24', 'retired|25', 'salesman|26', 'scientist|27', 'student|28', 'technician|29', 'writer|30'] 

users_meta=[]
users_meta = CreateMetadeta(demography,users_age,users_occup, users_meta)

DemVectors=DemMatrix(users_meta,num_users)

#print(DemVectors[354,:])

#### creating the user item matrix ####
user_item_mat=CreateUserItemMat(num_users,num_movies,Dataset)

#### Splitting the dataset into 80:20 training vs test dataset ####
num_test_users=round(0.2*num_users)
num_train_users=num_users-num_test_users

k=[10,50,100,150] ###### Neighborhood size
movie_set_size=[15,30,45,60] ##### Number of Movies shown to the user

#### to store the result #####
dem_result=np.zeros((4,4))
basic_hitrate=np.zeros((4,4))

i=0
for group_size in k:
  j=0
  for num_movies2rate in movie_set_size:
    temp_rmse=0
    
    hit_rate=0
    for iter in range(0,1):
      
      seperator=random.sample(range(0, num_users), num_users)
      
      #### grouping the users into test and training sets
      test_users=array(seperator[:num_test_users])
      train_users=array(seperator[num_test_users:])
      
      #### creating test and train user item matrix ####
      test_user_item=user_item_mat[test_users,:]
      train_user_item=user_item_mat[train_users,:]
      
      #### dividing demographic data ####
      test_dem=DemVectors[test_users,:]
      train_dem=DemVectors[train_users,:]
      
      #### Calculating the demographic similarity ####
      DemSim=CalculateSimilarity(test_dem, train_dem, int(num_test_users), int(num_train_users))
      
      k=group_size #users considered.
      movies2rate=num_movies2rate
      
      #### Asked to rate based rating from user ####
      ask2ratings=InitialRec(train_user_item, test_user_item, DemSim, k, movies2rate) 
      
      #### Collaborative filtering ####
      similarity=CalculateSimilarity(ask2ratings, train_user_item, int(num_test_users), int(num_train_users))
      FinalRecommendation=Predict(train_user_item, ask2ratings, similarity, k)
      
      ##temp_rmse=temp_rmse + CalcRMSE(FinalRecommendation,test_user_item)/8
      hit_rate=hit_rate+HitRate(test_user_item, predictions, num_movies2rate)
    print("Group size: {0}, No of Movies to rate: {1} Hit-Rate: {2}".format(group_size,num_movies2rate,hit_rate))  
    #basic_result[i,j]=temp_rmse
    basic_hitrate[i,j]=hit_rate
    
    j=j+1
  i=i+1
  
print(basic_result)

##### based on popularity
#### reading the dataset #######
Dataset=readUserDataset("u.data")

num_users=NumUsers(Dataset)
num_movies=NumMovies(Dataset)

#### creating the user item matrix ####
user_item_mat=CreateUserItemMat(num_users,num_movies,Dataset)
user_item_mat_copy=user_item_mat

#### most popular movie calculation ####
locations=np.where(user_item_mat_copy>0)
user_item_mat_copy[locations]=1
final_sum=user_item_mat_copy.sum(axis=1)

#### Splitting the dataset into 80:20 training vs test dataset ####
num_test_users=round(0.2*num_users)
num_train_users=num_users-num_test_users

k=[10,50,100,150] ###### Neighborhood size
movie_set_size=[15,30,45,60] ##### Number of Movies shown to the user
#### to store the result #####

famous_hitrate=np.zeros((4,4))

i=0
for group_size in k:
  j=0
  for num_movies2rate in movie_set_size:
    temp_rmse=0
    hit_rate=0
    for iter in range(0,1):
      
      seperator=random.sample(range(0, num_users), num_users)
      
      #### grouping the users into test and training sets
      test_users=array(seperator[:num_test_users])
      train_users=array(seperator[num_test_users:])
      
      #### creating test and train user item matrix ####
      test_user_item=user_item_mat[test_users,:]
      train_user_item=user_item_mat[train_users,:]
      
      k=group_size #users considered.
      movies2rate=num_movies2rate
      
      #### Asked to rate based rating from user based on popularity ####
      ask2ratings=np.zeros(test_user_item.shape)
      topK=[np.argsort(final_sum)[:-num_movies2rate-1:-1]]
     
     
      for l in range(0,test_user_item.shape[0]):
        for m in topK:
          ask2ratings[l,m]=test_user_item[l,m]
         
      
      #### Collaborative filtering ####
      similarity=CalculateSimilarity(ask2ratings, train_user_item, int(num_test_users), int(num_train_users))
      FinalRecommendation=Predict(train_user_item, ask2ratings, similarity, k)
      
      ##temp_rmse=temp_rmse + CalcRMSE(FinalRecommendation,test_user_item)/8
      hit_rate=hit_rate+HitRate(test_user_item, FinalRecommendation, num_movies2rate)
    
    print("Group size: {0}, No of Movies to rate: {1} Hit-Rate: {2}".format(group_size,num_movies2rate,hit_rate))  
    #basic_result[i,j]=temp_rmse
    famous_hitrate[i,j]=hit_rate
    
    j=j+1
  i=i+1
  
print(famous_hitrate)
