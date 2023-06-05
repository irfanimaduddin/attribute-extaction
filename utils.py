import string
import pandas as pd

# Static constant variable
LABELS = [
    'O',
    'B-AGE', 'I-AGE', 'E-AGE', 'S-AGE', # As is
    # 'B-BENEFIT', 'I-BENEFIT', 'E-BENEFIT', 'S-BENEFIT',
    'B-BRAND', 'I-BRAND', 'E-BRAND', 'S-BRAND',
    # 'B-CLAIM', 'I-CLAIM', 'E-CLAIM', 'S-CLAIM',
    'B-FLAVOR', 'I-FLAVOR', 'E-FLAVOR', 'S-FLAVOR',
    'B-GENDER', 'I-GENDER', 'E-GENDER', 'S-GENDER', # As is
    'B-GIMMICK', 'I-GIMMICK', 'E-GIMMICK', 'S-GIMMICK',
    'B-INGRED', 'I-INGRED', 'E-INGRED', 'S-INGRED',
    'B-PACKAGE', 'I-PACKAGE', 'E-PACKAGE', 'S-PACKAGE',
    'B-PACKGRP', 'I-PACKGRP', 'E-PACKGRP', 'S-PACKGRP',
    'B-SEND', 'I-SEND', 'E-SEND', 'S-SEND' ,
    'B-SHAPE', 'I-SHAPE', 'E-SHAPE', 'S-SHAPE' ,
    'B-SIZE', 'I-SIZE', 'E-SIZE', 'S-SIZE',
    'B-TYPE', 'I-TYPE', 'E-TYPE', 'S-TYPE',
]

def title2features(sent, i):
    word = sent[i]
    features = {
        'bias': 1,
        'word_position': i,
        'word.lower()': word.lower(),
        'word[:2]': word[:2],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.anydigit': any(ch.isdigit() for ch in word),
        'word.ispunctuation': word in string.punctuation,
    }

    if i == 0:
        word_plus_1 = sent[i + 1] if i + 1 < len(sent) else None
        features.update({
            '-1:word.lower()': None,
            '-1:word.istitle()': None,
            '-1:word.isupper()': None,
            '-1:word.anydigit': None,
            '-1:word.ispunctuation': None,
            '+1:word.lower()': word_plus_1.lower() if word_plus_1 else None,
            '+1:word.istitle()': word_plus_1.istitle() if word_plus_1 else None,
            '+1:word.isupper()': word_plus_1.isupper() if word_plus_1 else None,
            '+1:word.anydigit': any(ch.isdigit() for ch in word_plus_1) if word_plus_1 else None,
            '+1:word.ispunctuation': word_plus_1 in string.punctuation if word_plus_1 else None,
            'BOS': True,
            'EOS': False,
        })
    elif i == len(sent)-1:
        word_min_1 = sent[i - 1] if i - 1 >= 0 else None
        features.update({
            '-1:word.lower()': word_min_1.lower() if word_min_1 else None,
            '-1:word.istitle()': word_min_1.istitle() if word_min_1 else None,
            '-1:word.isupper()': word_min_1.isupper() if word_min_1 else None,
            '-1:word.anydigit': any(ch.isdigit() for ch in word_min_1) if word_min_1 else None,
            '-1:word.ispunctuation': word_min_1 in string.punctuation if word_min_1 else None,
            '+1:word.lower()': None,
            '+1:word.istitle()': None,
            '+1:word.isupper()': None,
            '+1:word.anydigit': None,
            '+1:word.ispunctuation': None,
            'BOS': False,
            'EOS': True,
        })
    else:
        word_min_1 = sent[i - 1] if i - 1 >= 0 else None
        word_plus_1 = sent[i + 1] if i + 1 < len(sent) else None
        features.update({
            '-1:word.lower()': word_min_1.lower() if word_min_1 else None,
            '-1:word.istitle()': word_min_1.istitle() if word_min_1 else None,
            '-1:word.isupper()': word_min_1.isupper() if word_min_1 else None,
            '-1:word.anydigit': any(ch.isdigit() for ch in word_min_1) if word_min_1 else None,
            '-1:word.ispunctuation': word_min_1 in string.punctuation if word_min_1 else None,
            '+1:word.lower()': word_plus_1.lower() if word_plus_1 else None,
            '+1:word.istitle()': word_plus_1.istitle() if word_plus_1 else None,
            '+1:word.isupper()': word_plus_1.isupper() if word_plus_1 else None,
            '+1:word.anydigit': any(ch.isdigit() for ch in word_plus_1) if word_plus_1 else None,
            '+1:word.ispunctuation': word_plus_1 in string.punctuation if word_plus_1 else None,
            'BOS': False,
            'EOS': False,
        })

    if i <= 1:
        word1 = sent[i + 1] if i + 1 < len(sent) else None
        word2 = sent[i + 2] if i + 2 < len(sent) else None
        features.update({
            '-2:ngram': None,
            '+2:ngram': '{} {}'.format(word1, word2) if word1 and word2 else None,
        })
    elif i >= len(sent) - 2:
        word1 = sent[i - 1] if i - 1 >= 0 else None
        word2 = sent[i - 2] if i - 2 >= 0 else None
        features.update({
            '-2:ngram': '{} {}'.format(word1, word2) if word1 and word2 else None,
            '+2:ngram': None,
        })
    else:
        word1 = sent[i - 1] if i - 1 >= 0 else None
        word2 = sent[i - 2] if i - 2 >= 0 else None
        word3 = sent[i + 1] if i + 1 < len(sent) else None
        word4 = sent[i + 2] if i + 2 < len(sent) else None
        features.update({
            '-2:ngram': '{} {}'.format(word1, word2) if word1 and word2 else None,
            '+2:ngram': '{} {}'.format(word3, word4) if word3 and word4 else None,
        })

    return features

def lib2features(libs, tag):
    features = {}
    words = libs.split()
    if len(words) == 1:
        tagged_word = {}
        tagged_word['word_position'] = 0
        tagged_word['word.lower()'] = words[0].lower()
        tagged_word['tag'] = 'S-{}'.format(tag)
        features[0] = tagged_word
    else:
        for j, word in enumerate(words):
            tagged_word = {}
            tagged_word['word_position'] = j
            tagged_word['word.lower()'] = word.lower()
            if j == 0:
                tagged_word['tag'] = 'B-{}'.format(tag)
                tagged_word['+1:word.lower()'] = words[j+1].lower()
            elif j == len(words) - 1:
                tagged_word['tag'] = 'E-{}'.format(tag)
                tagged_word['-1:word.lower()'] = words[j-1].lower()
            else:
                tagged_word['tag'] = 'I-{}'.format(tag)
                tagged_word['-1:word.lower()'] = words[j-1].lower()
                tagged_word['+1:word.lower()'] = words[j+1].lower()
            features[j] = tagged_word

    return features

def libdict2libdf(libdict):
    # Initialize empty lists for each column
    key_1 = []
    word_position = []
    word_min_1 = []
    word_lower = []
    word_plus_1 = []
    tag = []

    # Iterate over the dictionary and extract values into lists
    for key, value in libdict.items():
        for sub_key, sub_value in value.items():
            key_1.append(key)
            word_position.append(sub_value['word_position'])
            word_min_1.append(sub_value.get('-1:word.lower()', None))
            word_lower.append(sub_value['word.lower()'])
            word_plus_1.append(sub_value.get('+1:word.lower()', None))
            tag.append(sub_value['tag'])

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'key_1': key_1,
        'word_position': word_position,
        'word_min_1': word_min_1,
        'word_lower': word_lower,
        'word_plus_1': word_plus_1,
        'tag': tag
    })

    # Rearrange the columns in the desired order
    df = df[['key_1', 'word_position', 'word_min_1', 'word_lower', 'word_plus_1', 'tag']]

    return df

def titles2df(titlesdict):
    # Initialize empty lists for each column
    title_num = []
    bias = []
    word_position = []
    word_lower = []
    char_2_first = []
    char_2_last = []
    word_isupper = []
    word_istitle = []
    word_isdigit = []
    word_anydigit = []
    word_ispunctuation = []
    word_min_1 = []
    word_min_1_istitle = []
    word_min_1isupper = []
    word_min_1_anydigit = []
    word_min_1_ispunctuation = []
    word_plus_1 = []
    word_plus_1_istitle = []
    word_plus_1_isupper = []
    word_plus_1_anydigit = []
    word_plus_1_ispunctuation = []
    BOS = []
    EOS = []
    word_min_2 = []
    word_plus_2 = []

    # Iterate over the dictionary and extract values into lists
    for key, value in titlesdict.items():
        for sub_key, sub_value in value.items():
            title_num.append(key)
            bias.append(sub_value['bias'])
            word_position.append(sub_value['word_position'])
            word_lower.append(sub_value['word.lower()'])
            char_2_first.append(sub_value['word[:2]'])
            char_2_last.append(sub_value['word[-2:]'])
            word_isupper.append(sub_value['word.isupper()'])
            word_istitle.append(sub_value['word.istitle()'])
            word_isdigit.append(sub_value['word.isdigit()'])
            word_anydigit.append(sub_value['word.anydigit'])
            word_ispunctuation.append(sub_value['word.ispunctuation'])
            word_min_1.append(sub_value['-1:word.lower()'])
            word_min_1_istitle.append(sub_value['-1:word.istitle()'])
            word_min_1isupper.append(sub_value['-1:word.isupper()'])
            word_min_1_anydigit.append(sub_value['-1:word.anydigit'])
            word_min_1_ispunctuation.append(sub_value['-1:word.ispunctuation'])
            word_plus_1.append(sub_value['+1:word.lower()'])
            word_plus_1_istitle.append(sub_value['+1:word.istitle()'])
            word_plus_1_isupper.append(sub_value['+1:word.isupper()'])
            word_plus_1_anydigit.append(sub_value['+1:word.anydigit'])
            word_plus_1_ispunctuation.append(sub_value['+1:word.ispunctuation'])
            BOS.append(sub_value['BOS'])
            EOS.append(sub_value['EOS'])
            word_min_2.append(sub_value['-2:ngram'])
            word_plus_2.append(sub_value['+2:ngram'])

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'title_num': title_num,
        'bias': bias,
        'word_position': word_position,
        'word_lower': word_lower,
        'char_2_first': char_2_first,
        'char_2_last': char_2_last,
        'word_isupper': word_isupper,
        'word_istitle': word_istitle,
        'word_isdigit': word_isdigit,
        'word_anydigit': word_anydigit,
        'word_ispunctuation': word_ispunctuation,
        'word_min_1': word_min_1,
        'word_min_1_istitle': word_min_1_istitle,
        'word_min_1isupper': word_min_1isupper,
        'word_min_1_anydigit': word_min_1_anydigit,
        'word_min_1_ispunctuation': word_min_1_ispunctuation,
        'word_plus_1': word_plus_1,
        'word_plus_1_istitle': word_plus_1_istitle,
        'word_plus_1_isupper': word_plus_1_isupper,
        'word_plus_1_anydigit': word_plus_1_anydigit,
        'word_plus_1_ispunctuation': word_plus_1_ispunctuation,
        'BOS': BOS,
        'EOS': EOS,
        'word_min_2': word_min_2,
        'word_plus_2': word_plus_2
    })

    # Rearrange the columns in the desired order
    df = df[['title_num', 'bias', 'word_position', 'word_lower', 'char_2_first', 'char_2_last', 'word_isupper', 'word_istitle', 'word_isdigit', 'word_anydigit', 'word_ispunctuation', 'word_min_1', 'word_min_1_istitle', 'word_min_1isupper', 'word_min_1_anydigit', 'word_min_1_ispunctuation', 'word_plus_1', 'word_plus_1_istitle', 'word_plus_1_isupper', 'word_plus_1_anydigit', 'word_plus_1_ispunctuation', 'BOS', 'EOS', 'word_min_2', 'word_plus_2']]

    return df

def tagging_titles(tag_df, title_df, tag_str):
    # Iterate over each row in brand_df
    for index, row in tag_df.iterrows():
        word_min_1 = row['word_min_1']
        word_lower = row['word_lower']
        word_plus_1 = row['word_plus_1']
        tag = row['tag']

        # Check the conditions and update the tag value to 'O' in title_df
        if word_min_1 is None and word_plus_1 is not None:
            condition = (title_df['word_lower'] == word_lower) & (title_df['word_plus_1'] == word_plus_1)
        elif word_plus_1 is None and word_min_1 is not None:
            condition = (title_df['word_lower'] == word_lower) & (title_df['word_min_1'] == word_min_1)
        elif word_min_1 is None and word_plus_1 is None:
            condition = (title_df['word_lower'] == word_lower)
        else:
            continue

        matching_rows = title_df[condition]
        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            if title_df.at[matching_index, 'tag'] == tag_str:
                title_df.at[matching_index, 'tag'] = tag
    
    return title_df