import re
import string

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

# Example usage:
product_titles = [
"Birth Beyond Calming Oil 100ml",
# "Lab On Hair Anti Hair Fall Shampoo 300 ML - Shampo Perawatan Rambut Anti Rontok with Redensyl + eMortal Pep + Ginger + Ginseng",
"NATUR Natural Extract Shampoo | Shampoo Herbal | Olive Oil | Gingseng | 140 ML"
]

if __name__ == "__main__":
    import json

    INPUTPATH_BRAND = "./data/brand_input.txt"
    # INPUTPATH_INGRED = "./data/ingredients.txt"

    OUTPUTPATH_BRAND = "./data/brand_output.json"
    # OUTPUTPATH_INGRED = "./data/ingred_output.json"

    with open(INPUTPATH_BRAND, 'r', encoding="utf8") as f:
        brands = f.readlines()
    # with open(INPUTPATH_INGRED, 'r', encoding="utf8") as f:
    #     ingreds = f.readlines()

    titles_dict = {}
    for i, title in enumerate(product_titles):
        clean_title = title.replace("|", "")
        tokens = clean_title.split()
        title_features = {}
        for j, token in enumerate(tokens):
            features = title2features(tokens, j)
            title_features[j] = features

        titles_dict[i] = title_features

    brands_dict = {}
    for i, brand in enumerate(brands):
        features = lib2features(brand, tag='BRAND')
        brands_dict[i] = features

    # ingreds_dict = {}
    # for i, ingred in enumerate(ingreds):
    #     features = lib2features(ingred, tag='INGRED')
    #     ingreds_dict[i] = features

    # with open(OUTPUTPATH_BRAND, 'w') as f_out:
    #     json.dump(brands_dict, f_out)
    # with open(OUTPUTPATH_INGRED, 'w') as f_out:
    #     json.dump(ingreds_dict, f_out)

# print(brands_dict)
