from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise import accuracy
import streamlit as st
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import random
import seaborn as sns
import numpy as np # linear algebra
import warnings
warnings.filterwarnings('ignore')

st.title("영화 추천")
st.markdown('''

Data source: [kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
''')


# 평가의 개수가 m 이상인 영화들만 데이터 프레임에 포함
m = 200
movie_df_wr = pd.read_csv("movies_metadata.csv")
movie_df_wr = movie_df_wr[movie_df_wr["vote_count"]>=m]

# C는 데이터 프레임의 모든 영화의 평균 평
C = np.nanmean(movie_df_wr["vote_average"])

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return ((v/(v+m) * R) + (m/(m+v) * C))/2

def get_weighted_rating(mov_id):
    return movie_df_wr[movie_df_wr["id"]==str(mov_id)].loc[:,"wr"].values[0]

movie_df_wr["wr"] = movie_df_wr.apply(weighted_rating, axis=1)

movie_df = pd.read_csv("movies_metadata.csv")
movie_keywords = pd.read_csv("keywords.csv")
movie_credits = pd.read_csv("credits.csv")

movie_df = movie_df[movie_df["vote_count"]>=m]

movie_df = movie_df[['id','original_title','overview','genres']]

movie_df["title"] = movie_df["original_title"].copy()
movie_df.reset_index(inplace=True, drop=True)

movie_df["id"] = movie_df["id"].astype(int)
df = pd.merge(movie_df, movie_keywords, on="id")
df = pd.merge(df, movie_credits, on="id")

df.isna().sum()

df["overview"] = df["overview"].fillna("[]")

# 장르와 키워드, 배우 정보를 띄어쓰기로 구분하여 정리
df["genres"] = df["genres"].apply(lambda x: [i["name"] for i in eval(x)])
df["genres"] = df["genres"].apply(lambda x: ' '.join([i.replace(" ","") for i in x]))
df["keywords"] = df["keywords"].apply(lambda x: [i["name"] for i in eval(x)])
df["keywords"] = df["keywords"].apply(lambda x: ' '.join([i.replace(" ","") for i in x]))
df["director"] = df["crew"].apply(literal_eval).apply(lambda x: [i["name"] for i in x if i["job"]=="Director"])
df["director"] = df["director"].apply(lambda x: ' '.join([i.replace(" ","") for i in x]))
df["cast"] = df["cast"].apply(lambda x: [i["name"][:5] for i in eval(x)])
df["cast"] = df["cast"].apply(lambda x: ' '.join([i.replace(" ","") for i in x]))

table = df.copy()

st.dataframe(df)

# crew 삭제 
df.drop("crew", axis=1, inplace=True)

# 태그로 사용할 태그 열 추가 및 태그를 제외한 다른 열 제거
df["tags"] = df["overview"] + " " + df["genres"] + " " + df["original_title"] + " " + df["keywords"] + " " + df["cast"] + " " + df["director"] + " " +  df["director"] + " " + df["director"]
df.drop(columns=["overview", "genres", "original_title", "keywords", "cast", "director"], axis=1, inplace=True)

df.isnull().sum()
df.drop(df[df["tags"].isnull()].index, inplace=True)
df.drop_duplicates(inplace=True)

# 데이터 vectorize
tfidf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
vectorized_df = tfidf.fit_transform(df["tags"])

# 코사인 유사도 사용
cosine_sim = cosine_similarity(vectorized_df)

# 태그를 통한 영화 추천 함수
def recommendation_content(title):
    id_recom = df[df["title"]==title].index[0]
    distances = cosine_sim[id_recom]
    top_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:10]
    movie_list = []
    ids = []
    for i in top_list:
        movie_list.append(df.iloc[i[0]].title)
        ids.append(df.iloc[i[0]].id)
    return movie_list, ids

def recommendation_content2(title):
    id_recom = df[df["title"]==title].index[0]
    distances = cosine_sim[id_recom]
    top_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:50]
    movie_list = []
    ids = []
    for i in top_list:
        movie_list.append(df.iloc[i[0]].title)
        ids.append(df.iloc[i[0]].id)
    return movie_list, ids

# 취향을 추천에 반영하기 위한 평가 유저 정보 포함 구현 
ratings_df = pd.read_csv("ratings.csv")

movie_ids = [int(x) for x in df["id"].values]
ratings_df = ratings_df[ratings_df["movieId"].isin(movie_ids)]
ratings_df.reset_index(inplace=True, drop=True)

# 트레이닝set
reader = Reader()
data = Dataset.load_from_df(ratings_df[["userId", "movieId", "rating"]], reader=reader)
trainset = data.build_full_trainset()

# SVD 모델 학습
svd = SVD()
svd.fit(trainset)

# 유저정보 기반 추천 함수
def get_recommendations(data, movie_md, user_id, top_n, algo):
    recommendations = []
    
    user_movie_interactions = data.pivot(index='userId', columns='movieId', values='rating')
    
    non_interacted_movies = user_movie_interactions.loc[user_id][user_movie_interactions.loc[user_id].isnull()].index.tolist()
    
    for item_id in non_interacted_movies:
        
        est = algo.predict(user_id, item_id).est
        
        movie_name = movie_md[movie_md['id']==str(item_id)]['title'].values[0]
        recommendations.append((movie_name, est))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations[:top_n] 

# 태그 + 유저 정보 기반 추천

def hybrid_pred(userId, title):
    title_recom, ids = recommendation_content(title)
    score = []
    wr = [get_weighted_rating(x) for x in ids]
    for i in range(len(ids)):
        score.append(svd.predict(userId, ids[i]).est + wr[i]*0.1)
    return [x for (_, x) in sorted(zip(score, title_recom), reverse=True)][:10]

def hybrid_pred2(userId, title):
    title_recom, ids = recommendation_content2(title)
    score = []
    wr = [get_weighted_rating(x) for x in ids]
    for i in range(len(ids)):
        score.append(svd.predict(userId, ids[i]).est + wr[i]*0.2)
    return [score, title_recom]

hybrid_pred(5, "Inception")

recommendation_content("Inception")

ratings_df = pd.read_csv("ratings.csv")
ratings_df.drop("timestamp", inplace=True, axis=1)

def find_movieids(title_lst):
    return [int(movie_df[movie_df["original_title"]==x].id.values[0]) for x in title_lst]

def similar_user(user_input):
    user_inputId = find_movieids(user_input)
    print(user_inputId)

    ratings_new = ratings_df.copy()
    user_score = {}
    for x in user_inputId:
        cur_movie = ratings_df[ratings_df["movieId"] == x]
        for u, r in zip(cur_movie["userId"], cur_movie["rating"]):
            user_score[u] = user_score.get(u, 0) + r
    max_user, rating = ratings_df['userId'][0], 0
    for u in user_score:
        if user_score[u] > rating:
            max_user, rating = u, user_score[u]
    return max_user

def generate_recommendation_userid(user_input, userId=1):
    score_lst = []
    title_lst = []
    for x in user_input:
        result = hybrid_pred2(userId, x)
        for y in range(len(result[0])):
            if result[1][y] not in title_lst:
                title_lst.append(result[1][y])
                score_lst.append(result[0][y])
    recommended_title = pd.Series(title_lst, index=score_lst).sort_index(ascending=False)
    recommended_title = recommended_title.values
    unique_check_lst = []
    if len(np.unique(title_lst)) > 10:
        result = []
        for i in range(10):
            if recommended_title[i] not in unique_check_lst:
                result.append(recommended_title[i])
                unique_check_lst.append(recommended_title[i])
        return result
    else:
        result = []
        for i in range(len(np.unique(title_lst))):
            if recommended_title.iloc[i,0] not in unique_check_lst:
                result.append(recommended_title[i])
                unique_check_lst.append(recommended_title[i])
        return result

def generate_recommendation(user_input):
    if len(user_input) > 5:
        user_input = random.choices(user_input_test, k=5)
    return generate_recommendation_userid(user_input, similar_user(user_input))

selected_movie = st.selectbox(label="title",options=table['original_title'].unique())

submitted = st.button("Submit")

user_input_test = ["Toy Story"]

result_test = generate_recommendation_userid(user_input_test, 1)

find_movieids(user_input_test)

show = result_test
show


# table = netflix.groupby("genres")['title']
#st.dataframe(table)


if submitted:
     user_input_test = ["{seleceted_movie}"]
     result_test = generate_recommendation_userid(user_input_test)
     find_movieids(user_input_test)
     show = result_test
     show