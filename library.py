################ library #######################
def readFullDataset(dataSetFilePath):  

	header = ['user_id', 'item_id', 'rating', 'timestamp']  
	return pd.read_csv(dataSetFilePath, sep='\t', names=header)

def _read_raw_data(path):      


	with zipfile.ZipFile(path) as datafile:
		return datafile.read('ml-100k/u.user').decode(errors='ignore').split('\n') 

def readMovieSet(movieSetFilePath):  
	df_ids_titles = pd.read_csv(movieSetFilePath, sep="|", header=None, encoding='latin-1', names=['itemId', 'title'],usecols=[0, 1])  


	ids_titles = np.empty(1682, dtype=np.object)  

	for line in df_ids_titles.itertuples():  
		ids_titles[line[0]] = line[2]  
	return ids_titles  

def insertNewUserRatings(ids_titles, fullDataSet, newUserID, timestamp, known_positives, mySelMovies):  
	i=0  
	j=20  
	f=0  


	while(f < 10):  
		userList = []             
		for x in range(i,j):  
	
			userList.append({x%20+1: ids_titles[randint(0, 1681)]})  
	
	print('\n')        
	
	for p in userList:  
		print(p)  
	print('\n')    


	while(True): 
		try:  
			var = int(input("Choose a movie, or press -1 to change movieset: "))  
		except ValueError:  
			print("Wrong input, please insert an integer")  
			continue  
		if((var<-1 or var>20) and var ==0):  
			print("Value must be -1 OR between 1 and 20. Please insert a valid integer")  
		
			continue  
		if(1<=var and 20>=var):  
		
			selMovie = str(ids_titles.tolist().index(userList[var - 1][var]) + 1)  
		
			if selMovie in mySelMovies:  
		
				print("You have already selected that movie, please choose another movie")  
		
				continue 
			mySelMovies.append(str(ids_titles.tolist().index(userList[var-1][var])+1))  
			break 
		if (var == -1):               
			if ((1681 - j) >= 20):  
				i = j  
				j += 20                
			elif ((1681 - j) > 0):  
				i = j  
				j = 1682               
			else:  
				i = 0  
				j = 20  
			continue  
		else:  
			print('\n')  

			print("You selected the movie: " + userList[var-1][var] + " with ID: " + str(ids_titles.tolist().index(userList[var-1][var])+1))  
			
			print('\n')                
			while (True):                 
				try:  
					rating = int(input("Rate the movie: "))  
				except ValueError:  

					print("Wrong input, please insert an integer")  
					
					continue  
					
					if (rating < 1 or rating > 5):  
					
						print("Value must be between 1 and 5. Please insert a valid integer")  
      					continue  
      				break  
      		known_positives.append(ids_titles.tolist().index(userList[var - 1][var]) + 1)  
      		fullDataSet.loc[len(fullDataSet)] = [newUserID, ids_titles.tolist().index(userList[var - 1][var]) + 1, rating, timestamp]  
      		f = f + 1  84               
      		while(f < 10):                   
      			while (True):                        
      				try:  
      					ch = int(input("To change the movieset press -1, to keep press 1: "))  
      				except ValueError:  
      					print("Wrong input, please insert an integer")  
      					continue  
      				if (ch != 1 and ch != -1):  
      					print("Value must be 1 or -1. Please insert a valid integer")  
      					continue  
      				break  
      				if(int(ch) == -1):  
      					break  
      			    else:  
      			    	print('\n')  
      			    	for p in userList:  
      			    		print(p)  
      			    	print('\n')  
      			        while (True):  
      			        	try:  
      			        		var = int(input("Choose a movie: "))  


      			        	except ValueError:  
      			        		print("Wrong input, please insert an integer")  

      			        		continue  
      			            if ((var < -1 or var > 20)):

      			            	print("Value must be between 1 and 20. Please insert a valid integer")  
      			            	continue  
      			            selMovie = str(ids_titles.tolist().index(userList[var - 1][var]) + 1)  
      			            if selMovie in mySelMovies:  

      			            	print("You have already selected that movie, please choose another movie")  

      			            	continue  
      			            mySelMovies.append(str(ids_titles.tolist().index(userList[var - 1][var]) + 1))  
      			            break  

      			        print('\n')  

      			        print("You selected the movie: " + userList[var - 1][var] + " with ID: " + str( ids_titles.tolist().index(userList[var - 1][var]) + 1))  

      			        print('\n')  

      			        while (True):  
      			        	try:  
      			        		rating = int(input("Rate the movie: ")) 

      			        	except ValueError:  

      			        		print("Wrong input, please insert an integer")  

      			        		continue  

      			        		if (rating < 1 or rating > 5):

      			        			print("Value must be between 1 and 5. Please insert a valid integer")  

      			        			continue  
      			        		break  


      			        	known_positives.append(ids_titles.tolist().index(userList[var - 1][var]) + 1)  
      			        	fullDataSet.loc[len(fullDataSet)] = [newUserID, ids_titles.tolist().index(userList[var - 1][var]) + 1, rating, timestamp]  
      			        	f = f + 1  134              
	    if((1681-j) >= 20):  
	    	i = j  

	    	j += 20  137 
	    elif((1681-j) > 0):  
	    	
	    	i = j  
	    	j = 1682
	    else:  
	    	
	    	i = 0  
	    	j = 20  
	
	print('\n')  
return fullDataSet 


def numberOfUsers(fullDataSet):
	n_users = fullDataSet.user_id.unique().shape[0]
	
	return n_users 

def numberOfMovies(fullDataSet):
	n_items = fullDataSet.item_id.unique().shape[0]
	
	return n_items 

def getUserItemMatrix(n_users, n_items, fullDataSet):
	user_item_matrix = np.zeros((n_users, n_items))
	
	for line in fullDataSet.itertuples():
	
		user_item_matrix[line[1] - 1, line[2] - 1] = line[3]
	return user_item_matrix 

def calculateUsersPearsonCorrelation(user_item_matrixTrain):
    user_similarityPearson = 1 - pairwise_distances(user_item_matrixTrain, metric='correlation') #943*943
    
    user_similarityPearson[np.isnan(user_similarityPearson)] = 0
    return user_similarityPearson 

def predict_Top_K_no_Bias(ratings, similarity, k=40):
	
	pred = np.zeros(ratings.shape)
	
	user_bias = ratings.mean(axis=1)
	
	ratings = (ratings - user_bias[:, np.newaxis]).copy()
	for i in range(ratings.shape[0]):
		top_K_users = [np.argsort(similarity[:,i])[:-k-1:-1]]
		
		for j in range(ratings.shape[1]):
		
			pred[i,j] = similarity[i, :][top_K_users].dot(ratings[:, j][top_K_users])
		
			pred[i,j] /= np.sum(np.abs(similarity[i, :][top_K_users]))
	
	pred += user_bias[:, np.newaxis]
	return pred 



import numpy as np

import pandas as pd

import library

from sklearn.metrics.pairwise import pairwise_distances

from random import randint 

newUserID = 944 # new user's id

timestamp = '883446543' 

known_positives = []

mySelMovies = []

ids_titles = readMovieSet('u.item')

fullDataSet = readFullDataset('u.data')

fullDataSetNewUser = insertNewUserRatings(ids_titles, fullDataSet, newUserID, timestamp, known_positives, mySelMovies)

n_users = numberOfUsers(fullDataSetNewUser)
n_items = numberOfMovies(fullDataSetNewUser)

user_item_matrix = getUserItemMatrix(n_users, n_items, fullDataSetNewUser)
user_similarityPearson = calculateUsersPearsonCorrelation(user_item_matrix)

user_prediction_User = predict_Top_K_no_Bias(user_item_matrix,
user_similarityPearson, k=40)

def printPredictedMoviesUserBased(user, n):
	
	user = user - 1
	
	n = n - 1
	
	pred_indexes = [i + 1 for i in np.argsort(-user_prediction_User[user])]
	
	pred_indexes = [item for item in pred_indexes if item not in known_positives]
	
	movies_ids_titles = pd.read_csv('u.item', sep="|",header=None, encoding='latin-1', names=['itemId', 'title'],usecols=[0, 1])
	pd_pred_indexes = pd.DataFrame(pred_indexes, columns=['itemId'])
	
	pred_movies = pd.merge(pd_pred_indexes, movies_ids_titles,on='itemId')
	print('\n')
	print("*******************user-based collaborative filtering(Top-K neigbors and Bias-subtracted)*******************************")
	print(pred_movies.loc[:n])
	printPredictedMoviesUserBased(944, 10) 