# 1. packages
import re
import os
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm

# 2. consonants
## genres
genres = ['Academic', 'Fiction', 'News']
# filenames
filenames = []
for path in os.listdir()[:-1]:
    for home, dirs, files in os.walk(path):
        filenames.append(files) 

# 3. functions
def check_mismatch(all_information):
    '''
    check if the information extracted matched in length (PoS and metaphor tags)
    '''
    mismatches = []
    for information in all_information[1:]: # do not check the first title line
        if len(information[1]) != len(information[2]) or \
        len(information[1]) != len(information[3]):
            mismatches.append(information)
    
    # check and print
    if len(mismatches) != 0:
        print([mismatch[0] for mismatch in mismatches])
    else:
        print('\nNo mismatch')        

    return mismatches

def save_to_file(file_name, contents):
    '''
    write the contents into a file
    '''
    fh = open(file_name, 'w', newline='', encoding='utf-8-sig')
    writer = csv.writer(fh)
    for row in contents:
        writer.writerow(row)
    fh.close()
      
def get_sentence_information(title, example, genre):
    '''
    Create sequences from labelled sentences
    :param example: labelled sentences
    :return: information: a list of following information: 
             > index: the index of the sentence: document title + sentence number
             > text: the text of the sentence: a list of words
             > pos_tags: a list of Part-of-Speech tags for words in text
             > funtions: a list of metaphor label: 0 for literal, 1 for metaphor
    '''
    # 1. index
    pattern_index = re.compile(r'\d\d\d\d') 
    index = title + '_' + pattern_index.findall(example)[0]
    
    # 2. text
    soup = BeautifulSoup(example, 'html.parser')
    text = soup.text.strip().split()
    
    # 3. pos tags
    pattern_pos = re.compile(r'POS=".*?"')
    pos_tags = [pos[5:].split('"')[0] for pos in pattern_pos.findall(example)]
    
    # 4. metaphor-related information
    pattern_seg = re.compile(r'<seg function="mrw".*?>')
    functions = []
    for word in example.split('\r\n')[1:]:
        if len(pattern_seg.findall(word)) == 0:
            functions.append(0)

        else:
            functions.append(1)
   
    # integrate into a list
    information = [index, text, pos_tags, functions, genre]
      
    return information

def get_labelled_sequence(genre, filename):
    '''
    read PSUCMC data and extract information
    :param genre: genre of source text
    :param filename: name of the PSUCMC data file
    :return: sentences_information: a list of lists of sentence information
    '''
    # read data
    path = genre + '_txt/' + filename 
    with open(path, 'rb') as f:
        data = f.read().decode('utf-8')
    
    # split into paragraphs
    data_paragraph = data.split('<p>')
    
    # split into sentences
    data_sentence = []
    for paragraph in data_paragraph:
        data_sentence.extend(paragraph.split('</s>'))
    data_sentence = [sentence.strip() for sentence in data_sentence 
                     if len(re.findall('<s n="....">', sentence)) != 0]
    
    # get information 
    sentences_information = []
    for sentence in data_sentence:
        sentence_information = get_sentence_information(filename, sentence, genre)
        sentences_information.append(sentence_information)
    
    return sentences_information

def get_classification_data(labelling_data):
    '''
    get sequence classifiction data from sequence labelling data
    :param labelling data: a list of lists, each list consist of five items
                           - index: sentence index
                           - text: tokenized sentence
                           - PoS: Part-of-Speech tag lists of the tokenized sentence
                           - metaphor: metaphorical tag lists of the tokenized sentence
                                       > binary: metaphor (1) or literal (0)
                           - genres: genre of the source text
                                     > trinary: 'Academic', 'Fiction', 'News'
    :return: classification data: a list of lists, each list consist of six items
                           - sent_index: sentence index
                           - sent_txt: tokenized sentence
                           - verb: the verb in the sentence
                           - verb_index: position of the verb
                           - metaphor: metaphorical tag lists of the tokenized sentence
                                       > binary: metaphor (1) or literal (0)
                           - genres: genre of the source text
                                     > trinary: 'Academic', 'Fiction', 'News'
    '''
    classification = [['sent_index', 'sent_txt', 'verb', 'verb_index',
                       'metaphor', 'genre', 'sent_tokenized']]
    for line in tqdm(labelling_data[1:]):
        for i in range(len(line[2])):
            if line[2][i] in ['v', 'vg', 'vd', 'vn']:
                new_line = []
                new_line.append(line[0]) # sentence index 
                new_line.append(''.join(line[1])) 
                new_line.append(line[1][i]) # verb
                new_line.append(i + 1) # verb index
                new_line.append(line[3][i]) # metaphor label
                new_line.append(line[4]) # genre
                new_line.append(line[1]) # tokenized sentence
                classification.append(new_line)
    return classification
        
   
# 4. commands
# get all information 
all_information = [['index', 'text', 'PoS', 'metaphor', 'genres']]
for i in range(3):
    for filename in filenames[i]:
        sentences_information = get_labelled_sequence(genres[i], filename)
        all_information.extend(sentences_information)
# Check
mismatches = check_mismatch(all_information)
# save to file (sequence data)
save_to_file('PSUCMC_sequence.csv', all_information)
# calssification data
classification_data = get_classification_data(all_information)
# save to file (calssification data)
save_to_file('PSUCMC_classification.csv', classification_data)   


    



