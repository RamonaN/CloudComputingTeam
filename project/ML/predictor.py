import os
import re
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class MyPredictor(object):

    def __init__(self, model_users, model_items, ratings_matrix, books):

        self._model_users = model_users
        self._model_items = model_items
        self._ratings_matrix = ratings_matrix
        self._books = books

    def find_k_similar_users(self, user_id, k=10):
        loc = self._ratings_matrix.index.get_loc(user_id)
        distances, indices = self._model_users.kneighbors(self._ratings_matrix.iloc[loc, :].values.reshape(1, -1),
                                                          n_neighbors=k + 1)
        similarities = 1 - distances.flatten()

        return similarities, indices

    def predict_user_based(self, user_id, item_id, _ratings_matrix, k=10):
        prediction = 0
        user_loc = _ratings_matrix.index.get_loc(user_id)
        item_loc = _ratings_matrix.columns.get_loc(item_id)
        similarities, indices = self.find_k_similar_users(user_id, k)
        mean_rating = _ratings_matrix.iloc[user_loc, :].mean()
        sum_wt = np.sum(similarities) - 1
        product = 1
        wtd_sum = 0

        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] == user_loc:
                continue
            else:
                ratings_diff = _ratings_matrix.iloc[indices.flatten()[i], item_loc] - np.mean(
                    _ratings_matrix.iloc[indices.flatten()[i], :])
                product = ratings_diff * (similarities[i])
                wtd_sum = wtd_sum + product

        prediction = int(np.nan_to_num(round(mean_rating + (wtd_sum / sum_wt))))


        return prediction

    def find_k_similar_items(self, item_id, k=10):
        ratings = self._ratings_matrix.T
        loc = ratings.index.get_loc(item_id)

        distances, indices = self._model_items.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors=k + 1)
        similarities = 1 - distances.flatten()

        return similarities, indices

    def predict_item_based(self, user_id, item_id, _ratings_matrix, k=10):
        prediction = wtd_sum = 0
        item_id = int(item_id)
        user_loc = _ratings_matrix.index.get_loc(user_id)
        item_loc = _ratings_matrix.columns.get_loc(item_id)
        similarities, indices = self.find_k_similar_items(item_id, k)
        sum_wt = np.sum(similarities) - 1
        product = 1
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] == item_loc:
                continue
            else:
                product = _ratings_matrix.iloc[user_loc, indices.flatten()[i]] * (similarities[i])
                wtd_sum = wtd_sum + product
        prediction = int(np.nan_to_num(round(wtd_sum / sum_wt)))

        if prediction <= 0:
            prediction = 1
        elif prediction > 10:
            prediction = 10


        return prediction

    def recommend(self, user_id, k=10, item=True):
        if (user_id not in self._ratings_matrix.index.values) or type(user_id) is not int:
            print("User id should be a valid integer from this list :\n\n {} ".format(
                re.sub('[\[\]]', '', np.array_str(self._ratings_matrix.index.values))))
        else:

            prediction = []

            for i in range(self._ratings_matrix.shape[1]):
                if self._ratings_matrix[self._ratings_matrix.columns[i]][user_id] != 0:  # not rated already
                    if item:
                        prediction.append(
                            self.predict_item_based(user_id, self._ratings_matrix.columns[i], self._ratings_matrix))
                    else:
                        prediction.append(
                            self.predict_user_based(user_id, self._ratings_matrix.columns[i], self._ratings_matrix))
                else:
                    prediction.append(-1)

            prediction = pd.Series(prediction)
            prediction = prediction.sort_values(ascending=False)
            recommended = prediction[:k]
            return [str(self._books.isbn[recommended.index[i]]) for i in range(len(recommended))]


    def predict(self, instances, **kwargs):
        """Performs custom prediction.

        Preprocesses inputs, then performs prediction using the trained
        scikit-learn model.

        Args:
            instances: A list of prediction input instances.
            **kwargs: A dictionary of keyword args provided as additional
                fields on the predict request body.

        Returns:
            A list of outputs containing the prediction results.
        """
        
        if 'k' in kwargs.keys():
            k =int(kwargs['k'])
        else: 
            k= 10
            
        if 'item' in kwargs.keys():
            item = bool(kwargs['item'])
        else:
            item = True
                            
        outputs = [self.recommend(i,k,item) for i in instances ] 
        return outputs




def azureml_main(dataframe1 = None, dataframe2 = None):

    if dataframe2.empty:
        return pd.DataFrame(columns = ['close']),

    users_predict = dataframe2.Col1.dropna().astype('int32').unique().tolist()
    dataframe2.drop(['Col1'],axis=1,inplace=True)

    model_knn_users = NearestNeighbors(metric = 'cosine', algorithm = 'brute') 
    model_knn_users.fit(dataframe1)
    
    model_knn_items = NearestNeighbors(metric = 'cosine', algorithm = 'brute') 
    model_knn_items.fit(dataframe1.T)
    
    
    pred = MyPredictor(model_knn_users,model_knn_items,dataframe1,dataframe2)
    

    prediction = pred.predict(users_predict,k = len(dataframe2.index), item = False)

    print("the rezult is")
    print(prediction)
    
    return pd.DataFrame(prediction),
