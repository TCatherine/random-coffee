from db import RandomCoffeeDB
from itertools import combinations
import transformers
import torch 
from sklearn.metrics.pairwise import cosine_similarity

db = RandomCoffeeDB('random_coffee.db')
data = db.get_all_data()
print(data)
# pairs = []

# tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
# model = transformers.BertModel.from_pretrained('bert-base-uncased')

# def get_score(tokenizer, model, sentence1, sentence2):
#     tokens1 = tokenizer.tokenize(sentence1)
#     tokens2 = tokenizer.tokenize(sentence2)
#     # Convert tokens to input IDs
#     input_ids1 = torch.tensor(tokenizer.convert_tokens_to_ids(tokens1)).unsqueeze(0)  # Batch size 1
#     input_ids2 = torch.tensor(tokenizer.convert_tokens_to_ids(tokens2)).unsqueeze(0)  # Batch size 1

#     # Obtain the BERT embeddings
#     with torch.no_grad():
#         outputs1 = model(input_ids1)
#         outputs2 = model(input_ids2)
#         embeddings1 = outputs1.last_hidden_state[:, 0, :]  # [CLS] token
#         embeddings2 = outputs2.last_hidden_state[:, 0, :]  # [CLS] token

#     # Calculate similarity
#     similarity_score = cosine_similarity(embeddings1, embeddings2)
#     return similarity_score[0][0]

# for pair in combinations(data.keys(), 2):
#     format = 0
#     if data[pair[0]]["format"].lower()==data[pair[1]]["format"].lower():
#         format = 100
#     elif data[pair[0]]["format"].lower()=='both' or data[pair[1]]["format"].lower()=='both':
#         format = 50
     
#     motivation = 0
#     if data[pair[0]]["motivation"].lower()==data[pair[1]]["motivation"].lower():
#         motivation = 100
#     elif data[pair[0]]["motivation"].lower()=='50' or data[pair[1]]["motivation"].lower()=='50':
#         motivation = 50
    
#     similarity_hobby=get_score(tokenizer, model, data[pair[0]]["hobby"], data[pair[1]]["hobby"])
#     similarity_work=get_score(tokenizer, model, data[pair[0]]["job_area"], data[pair[1]]["job_area"])
#     pairs.append(
#         {
#             "id1": pair[0],
#             "id2": pair[1],
#             "format": format,
#             "motivation": motivation,
#             "hobby_score": similarity_hobby,
#             "work_score": similarity_work
#         }
#     )

# print(pairs)