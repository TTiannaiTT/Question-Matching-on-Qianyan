import sys
sys.path.append('/home/aistudio/external-libraries')
import random
import pandas as pd
from pyhanlp import HanLP
from sklearn.utils import shuffle

random.seed(2021)

def get_keyword(content, keynum=2):
    """
    Get keywords from each question, the number of keywords is controlled by keynum.
    :param content: A sentence
    :return:
    """
    keywordList = HanLP.extractKeyword(content, keynum)
    return keywordList

def construct_synwords(cilinpath='./work/user_data/eda_data/cilin.txt'):
    """
    Construct a synonym table based on Harbin Institute of Technology's synonym forest (cilin.txt).
    The file is from https://github.com/TernenceWind/replaceSynbycilin/blob/master/cilin.txt
    :param cilinpath: Path to the synonym forest
    :return:
    """
    synwords = []
    with open(cilinpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip()
            split = temp.split(' ')
            bianhao = split[0]
            templist = split[1:]
            if bianhao[-1] == '=':
                synwords.append(templist)
    return synwords

def replace_synwords(content, synwords):
    """
    Replace keywords in content with synonyms.
    :param content: Sentence to replace synonyms, not the entire sample or dataset
    :param synwords: Synonym dictionary
    :return:
    """
    segmentationList = HanLP.segment(content)
    if len(set(segmentationList)) <= 2:
        keynum = 1
    elif len(segmentationList) > 2 and len(set(segmentationList)) <= 6:
        keynum = 2
    else:
        keynum = 4
    keywordList = get_keyword(content, keynum)  # Get keywords

    segmentationList = [term.word for term in segmentationList]
    replace_word = {}
    # Find synonyms of keywords in content
    for word in keywordList:
        if word in segmentationList:
            for syn in synwords:
                if word == syn[0]:
                    if len(syn) == 1:
                        continue
                    else:
                        if syn.index(word) == 0:
                            replace_word[word] = syn[1]
                        else:
                            replace_word[word] = syn[syn.index(word) - 1]
                else:
                    continue
        else:
            continue

    # Replace synonyms in content
    for i in range(len(segmentationList)):
        if segmentationList[i] in replace_word:
            segmentationList[i] = replace_word[segmentationList[i]]
        else:
            continue
    # Reassemble content into a sentence
    content_new = "".join(segmentationList)
    # Return the replaced content, i.e., new_content
    return content_new

def get_same_pinyin_vocabulary(same_pinyin_file):
    """
    Get a vocabulary with the same pinyin, the file is from https://github.com/shibing624/pycorrector/blob/master/pycorrector/data/same_pinyin.txt
    :param same_pinyin_file:
    :return: {"word1":samepinyin,"word2":samepinyin}
    """
    same_pinyin = {}
    with open(same_pinyin_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            temp = line.strip("\n")
            split_1 = temp.split('\t')
            word_index = split_1[0]  # Root word
            sameWords = ""
            for i in split_1[1:]:  # Concatenate same pinyin words
                sameWords += i
            same_pinyin[word_index] = list(sameWords)  # Put same pinyin words in the same list
    return same_pinyin

def get_word_freq(chinese_word_freq_file_path):
    """
    Read word, frequency, and construct a dictionary
    :param chinese_word_freq_file_path: Chinese word frequency file
    :return: {"word1":freq1,"word2":freq2}
    """
    word_freq_vocab = {}  # Word frequency dictionary, format is ["word":freq]
    with open(chinese_word_freq_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            word_freq = line.split(" ")
            if word_freq[0] not in word_freq_vocab:
                word_freq_vocab[word_freq[0]] = int(word_freq[1])  # Add "word":freq to the dictionary
            else:
                pass
    return word_freq_vocab

def replace_samePinyin(content, same_pinyin, word_freq_vocab, replace_num=1):
    """
    Replace keywords in content with homophones (the replacement rule is to replace the word with the highest frequency of occurrence among all homophones)
    :param content: Text to be replaced
    :param same_pinyin: Same pinyin vocabulary
    :param word_freq_vocab: Chinese word frequency table
    :param replace_num: Number to replace, here only one word is replaced
    :return: Text replaced with homophones
    """
    segmentationList = HanLP.segment(content)
    word_list_of_content = list(content)
    if len(set(segmentationList)) <= 2:
        keynum = 1
    elif len(segmentationList) > 2 and len(set(segmentationList)) <= 6:
        keynum = 2
    else:
        keynum = 4
    keywordList = get_keyword(content, keynum)  # Get keywords
    key_character = []
    for word in keywordList:  # Extract key characters from keywords
        key_character += list(word)
    key_character = list(set(key_character))  # Remove duplicate key characters
    key_character = [word for word in key_character if word in same_pinyin]  # Check if all characters in keywords appear in the same pinyin vocabulary
    word_freq = []
    for i in key_character:  # Count the frequency of key characters
        samePinyin_list = same_pinyin[i]  # Get all words with the same pinyin
        samePinyin_freq = []
        for j in samePinyin_list:
            if j in word_freq_vocab:
                samePinyin_freq.append(word_freq_vocab[j])
            else:
                samePinyin_freq.append(1)
        word_freq.append(samePinyin_list[samePinyin_freq.index(max(samePinyin_freq))])
    freq = []
    if len(word_freq) != 0:
        for i in word_freq:
            if i in word_freq_vocab:
                freq.append(word_freq_vocab[i])
            else:
                freq.append(1)
        same_pinyin_HighFreq_word = word_freq[freq.index(max(freq))]
        replace_word = key_character[freq.index(max(freq))]
        replace_index = word_list_of_content.index(replace_word)
        word_list_of_content[replace_index] = same_pinyin_HighFreq_word
        new_content = "".join(word_list_of_content)
        return new_content
    else:
        return content

def read_csvToDF(data_path):
    """
    Reads data from a CSV file and converts it to a DataFrame.
    :param data_path: Path to the data file
    :return: DataFrame
    """
    data = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            tmp_data = [i for i in line.rstrip().split("\t")]
            if len(tmp_data) != 3:
                continue
            data.append(tmp_data)
                
    df = pd.DataFrame(data, columns=['text_one', 'text_two', 'label'])
    # Adjust label type to int
    df['label'] = df['label'].astype(int)
    return df

def synword_and_samepinyin_data(data, cilin_path, same_pinyin_file, chinese_word_freq_file, replace_rule=True, 
                                columns_num=3, word_portition=0.2, pinyin_portition=0.15):
    """
    Take a certain proportion of samples from data for data augmentation.
    :param data: Dataset
    :param cilinpath: Synonym table file
    :param same_pinyin_file: Homophone table file
    :param chinese_word_freq_file: Chinese word frequency file
    :param repalce_rule: True to randomly select one from q1 and q2 in positive samples as the text to be replaced,
                         False to replace both q1 and q2 with synonyms
    :param portition: Proportion of samples to be replaced
    :return: Dataset after data augmentation
    """
    synonyms_list = construct_synwords(cilin_path)  # Get synonym table
    same_pinyin_vocab = get_same_pinyin_vocabulary(same_pinyin_file)  # Get same pinyin vocabulary
    word_freq_vocab = get_word_freq(chinese_word_freq_file)  # Get Chinese word frequency table
    if word_portition != 1:
        word_samples = data.sample(frac=word_portition, replace=False, random_state=2021)  # Randomly select a certain proportion of samples for data augmentation
    else:
        word_samples = data

    word_samples['text_one_word'] = word_samples['text_one'].apply(lambda x: replace_synwords(x, synonyms_list))
    word_samples['text_two_word'] = word_samples['text_two'].apply(lambda x: replace_synwords(x, synonyms_list))

    if pinyin_portition != 1:
        pinyin_sample = data.sample(frac=pinyin_portition, replace=False, random_state=1998)  # Randomly select a certain proportion of samples for data augmentation
    else:
        pinyin_sample = data

    pinyin_sample['text_one_pinyin'] = pinyin_sample['text_one'].apply(lambda x: replace_samePinyin(x, same_pinyin_vocab, word_freq_vocab))
    pinyin_sample['text_two_pinyin'] = pinyin_sample['text_two'].apply(lambda x: replace_samePinyin(x, same_pinyin_vocab, word_freq_vocab))

    return word_samples, pinyin_sample

def EDA_data(wordtmp, pinyintmp):
    """
    Concatenate datasets enhanced with synonyms and homophones.
    """
    wordtmp['word_similar_one'] = list(map(lambda x, y: 0 if x == y else 1, wordtmp['text_one'], wordtmp['text_one_word']))
    wordtmp['word_similar_two'] = list(map(lambda x, y: 0 if x == y else 1, wordtmp['text_two'], wordtmp['text_two_word']))
    wordtmp['similar_word'] = list(map(lambda x, y: 1 if x == 1 or y == 1 else 0, wordtmp['word_similar_one'], wordtmp['word_similar_two']))
    print(len(wordtmp[wordtmp['similar_word'] == 1]))
    word_eda = wordtmp[wordtmp['similar_word'] == 1]
    word_eda = word_eda[['text_one_word', 'text_two_word', 'label']]
    word_eda.rename(columns={'text_one_word': 'text_one', 'text_two_word': 'text_two'}, inplace=True)
    pinyintmp['pinyin_similar_one'] = list(map(lambda x, y: 0 if x == y else 1, pinyintmp['text_one'], pinyintmp['text_one_pinyin']))
    pinyintmp['pinyin_similar_two'] = list(map(lambda x, y: 0 if x == y else 1, pinyintmp['text_two'], pinyintmp['text_two_pinyin']))
    pinyintmp['similar_pinyin'] = list(map(lambda x, y: 1 if x == 1 or y == 1 else 0, pinyintmp['pinyin_similar_one'], pinyintmp['pinyin_similar_two']))
    pinyin_eda = pinyintmp[pinyintmp['similar_pinyin'] == 1]
    pinyin_eda = pinyin_eda[['text_one_pinyin', 'text_two_pinyin', 'label']]
    pinyin_eda.rename(columns={'text_one_pinyin': 'text_one', 'text_two_pinyin': 'text_two'}, inplace=True)
    eda_data = pd.concat([word_eda, pinyin_eda])
    return eda_data

def random_change(data):
    """
    Randomly swap 50% of the enhanced dataset to improve model robustness.
    """
    data = shuffle(data, random_state=2021)
    changedata = data[0:len(data) // 2]
    source_data = data[len(data) // 2:]
    tmp = pd.DataFrame()
    
    tmp['text_one'] = changedata['text_two']
    tmp['text_two'] = changedata['text_one']
    tmp['label'] = changedata['label']
    
    final_data = pd.concat([tmp, source_data])
    return final_data

if __name__ == "__main__":
    train = read_csvToDF('./work/raw_data/train.txt')
    gaiic = read_csvToDF('./work/user_data/eda_data/gaiic.tsv')
    data = pd.concat([train, gaiic])
    cilin_path = './work/user_data/eda_data/cilin.txt'
    same_pinyin_file = './work/user_data/eda_data/same_pinyin.txt'
    chinese_word_freq_file = './work/user_data/eda_data/chinese-words.txt'
    word_data, pinyin_data = synword_and_samepinyin_data(data, cilin_path, same_pinyin_file, chinese_word_freq_file, replace_rule=True,
                                                         columns_num=3, word_portition=0.2, pinyin_portition=0.15)
    word_data.to_csv('./work/user_data/eda_data/word_data.txt')
    pinyin_data.to_csv('./work/user_data/eda_data/pinyin_data.txt')

    eda_data = EDA_data(word_data, pinyin_data)
    final_data = random_change(eda_data)
    final_data.to_csv('./work/user_data/eda_data/word_pinyin.txt', sep='\t', header=None, index=False)

    # Read training data and concatenate the enhanced text with the original data
    train = read_csvToDF('./work/raw_data/train.txt')
    gaiic = read_csvToDF('./work/user_data/eda_data/gaiic.tsv')
    eda = read_csvToDF(data_path='./work/user_data/eda_data/word_pinyin.txt')
    gaiic_train_eda = pd.concat([gaiic, train, eda])
    gaiic_train_eda.to_csv('./work/user_data/eda_data/gaiic_train_augmented.txt', sep='\t', index=False, header=None)