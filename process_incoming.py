import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np 
import joblib

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed" ,json = {
        "model" : "bge-m3",
        "input" : text_list
    })

    embedding = r.json()["embeddings"]
    return embedding

def inference(promt):
     r = requests.post("http://localhost:11434/api/generate" ,json = {
        "model" : "llama3.2",
        "prompt" : prompt,
        "stream" : False
    })
     

     response = r.json()
     print(response)
     return response


df = joblib.load("embeddings.joblib")


incoming_query = input("Ask a question :")
question_embedding = create_embedding([incoming_query])[0]

# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding'].shape))

similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 10
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)

new_df = df.loc[max_indx]
# print(new_df[["text", "number" ,"text"]])

prompt = f''' Here are video chunks containing title , number , text:


{new_df[["title","number", "start" , "end", "text"]].to_json(orient= "records")}
------------------------------------------
{incoming_query}
User ask this question related to video chunks , you have to answer in human way (don't mention the above foramt its just form you) where and how much content is taught where (in which video and at what timestamp)
and guide the user to go to that particular video
'''

with open("prompt.txt", "w") as f:
     f.write(prompt)

response = inference(prompt)["response"]
print(response)

with open("response.txt", "w") as f:
     f.write(response)
# for index,item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"] , item["end"])

