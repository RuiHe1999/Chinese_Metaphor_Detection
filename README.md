# Mono- and cross-lingual metaphro detection

Data and codes for my master thesis (TFM). The core model is a BiLSTM + CRF recurrent neural network using (concatenated) pretrained word embeddings as the feature. 

## Table of Contents
- [folder intro](#basics)
- [Data](#data)
- [Embeddings](#embeddings)
- [Codes](#codes)
- [Predictions](#predictions)

## Basics
Brief intro to each folder:
- data: formatted version of each corpus

## Data
We used two metaphor datasets here, VU Amsterdam Metaphor Corpus for English and PSU Chinese Metaphor Corpus for Chinese (Mandarin). 

**Dataset format**:

All Datasets are endcoded with UTF-8. The datasets we shared here are not original ones but formatted into 5 or 8 columns. Below the table we provided the links to original datasets respectively. 

| Column Title            | Meaning                   | Note                                     |
| ------------            | -----------------------   | ---------------------------------------- |
| sent_index              | Sentence Index            |                                          |
| sent_txt                | Original Sentence         |                                          |
| pos_seq                 | POS tag sequence          |                                          |
| metaphor_seq            | metaphor label sequence   | binary, 0 for literal and 1 for metaphor |
| genre                   | source text genre         | news, fiction, academic, conversation (conversation only in VUA) |
| sent_txt_tokenized      | orignial tokenization     | sentence to a list of words              |
| sent_bert_tokens        | bert tokenization         |                                          |
| sent_txt_tokenized_bert | bert tokenization         | sentence to a list of lists, each inner list for a Bert tokenized word     |
| BIO_seq                 | BIO tag sequence          | trinary, B for begining of metaphor, I for inside metaphor and O for outside metaphor (i.e. literal) |
| split                   | subset label              | trinary, train/test/val                  |

### VUA
VUA dataset is an English metaphor dataset obtained from [Shared Task on Metaphor Detection](<https://github.com/EducationalTestingService/metaphor/tree/master/VUA-shared-task>). 

### PSUCMC
The PSU Chinese Metaphor Corpus is published by Dr. Xiaofei Lu on his [personal webset](<http://www.personal.psu.edu/xxl13/downloads/cmc.html>).

There are some errors in the original corpus which we fixed them manually

- fiction\_10\_v.4.txt: 0013  
This is resulted from a blank space which is not recognized by the html parser. As the blank space here is not grammatically suitable in Chinese, I deleted it in the corpus. 

- news\_10\_v.4.txt: 0077  
This is resulted from the omission of > in the original corpus, I added it.

- news\_17\_v.4.txt: 0025  
This is due to a bad format in the original corpus (additional blank line), I changed it.

- news\_20\_v.4.txt: 0021  
This is due to a lack of </s\> in the original corpus, I added it.


## Embeddings
We provided the codes for embedding sentence but the embeddings we trained on our data could not be released here (too large to be uploaded on GitHub). If needed, please contact me by [email](<mailto: h.r-rui@outlook.com>). The embedding ares stored in h5 files. 

- FastText: We used the official package and pretrained model published by Facebook to generate the embeddings for both English and Chinese data. These embeddings are trained on bert tokenized sentences. 

- Elmo: These embeddings are trained on bert tokenized sentences. 
    - English: we used allennlp.modules.token_embedders.elmo_token_embedder to embed the sentence using the Elmo model published by allennlp.
    - Chinese: we used the elmo trained by HIT which is shared by henryhust. Click here to [download](https://pan.baidu.com/s/1RNKnj6hgL-2orQ7f38CauA?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=).The github repo of this project could be found on [henryhust/elmo_chinese](https://github.com/henryhust/elmo_chinese) (find an example model to train elmo on Chinese data) and [HIT-SCIR/ELMoForManyLangs](https://github.com/HIT-SCIR/ELMoForManyLangs)(the source code of elmoformanylangs published by HUST). 

- BERT: We used and recommended [bert-as-service](<https://github.com/hanxiao/bert-as-service>) for Bert embeddings. It is super easy and fast to generate bert embeddings. 
    - English: we used the [uncased BERT model published by Google](<https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip>) for English data. 
    - Chinese: we did not use the Chinese BERT model published by Google but RoBERTa-wwm-ext by HIT and iFLYTEK (an improved Bert for Chinese). Detailed information could be found on [Chinese BERT with Whole Word Masking](https://github.com/ymcui/Chinese-BERT-wwm/blob/master/README_EN.md#chinese-bert-with-whole-word-masking). 
(Not used at last)

- Baseline: Baseline embeddings are generated with torch.nn.embeddings. THe vocabulary was generated from the dataset itself and made into a token2idx dictionary. These embeddings are trained on bert tokenized sentences. (Not used at last)

## Codes
We provided our codes for BiLSTM+Attention and BiLSTM+Attention+CRF models on mono- and cross-lingual metaphor detection tasks. It was created and run on Google Colab. You need to change the file paths before you run these codes. 

## Predictions
Here stores our result of sequencial metaphor detection. 
