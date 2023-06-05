import json
from utils import *

INPUTPATH_TITLE = "./data/unilever_test_title.csv"
# INPUTPATH_BRAND = "./data/brand_input.txt"
# INPUTPATH_INGRED = "./data/ingredients.txt"

OUTPUTPATH = "./data/dataset_test.txt"

INPUTPATH_BRAND = "./data/brand_output.json"
INPUTPATH_INGRED = "./data/ingred_output.json"

with open(INPUTPATH_TITLE, 'r', encoding="utf8") as f:
    titles = f.readlines()
with open(INPUTPATH_BRAND, 'r') as f:
    brands_dict = json.load(f)
with open(INPUTPATH_INGRED, 'r') as f:
    ingreds_dict = json.load(f)

titles_dict = {}
for i, title in enumerate(titles):
    chars = '\\`*{},-[]|()>#$"/'
    for c in chars:
        title = title.replace(c, '')
    tokens = title.split()
    title_features = {}
    for j, token in enumerate(tokens):
        features = title2features(tokens, j)
        title_features[j] = features

    titles_dict[i] = title_features

titles_df = titles2df(titles_dict)
brand_df = libdict2libdf(brands_dict)
ingreds_df = libdict2libdf(ingreds_dict)

# Create an empty 'tag' column in titles_df
titles_df['tag'] = 'O'

# print(titles_df['title_num'].max())
titles_df = titles_df[titles_df['title_num'] < 1000]

titles_df = tagging_titles(brand_df, titles_df, 'O')
titles_df = tagging_titles(ingreds_df, titles_df, 'O')

# Group the rows by 'title_num'
grouped = titles_df.groupby('title_num')

# Iterate over the groups and print the values
with open(OUTPUTPATH, 'w', encoding="utf8") as f:
    for _, group in grouped:
        for _, row in group.iterrows():
            f.write(f"{row['word_lower']}\t{row['tag']}\n")
        f.write("\n")    

# titles_df.to_csv('./data/dataset_test.csv', index=False)
