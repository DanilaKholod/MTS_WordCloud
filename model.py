import pandas as pd
import numpy as np
from navec import Navec
import pymorphy3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from collections import Counter


punctuation_marks = ['!', ',', '(', ')', ':', '-', '?', '.', '..', '...', '—']
stop_words = stopwords.words("russian")
morph = pymorphy3.MorphAnalyzer()

def preprocess(text, stop_words, punctuation_marks, morph):
    tokens = word_tokenize(text.lower())
    preprocessed_text = []
    for token in tokens:
        if token not in punctuation_marks:
            lemma = morph.parse(token)[0].normal_form
            if lemma not in stop_words:
                preprocessed_text.append(lemma)
    return preprocessed_text

def question_to_vec(question, embeddings, tokenizer, dim=300):
    """
        question: строка
        embeddings: наше векторное представление
        dim: размер любого вектора в нашем представлении

        return: векторное представление для вопроса
    """
    num_question_words = 0 # we wanna count wors in question, cuz
    quest_vectorized = np.zeros(shape = dim)
    for word in tokenizer(question, stop_words, punctuation_marks, morph):
        if word in embeddings: #case existance of word: if it is absent we do not find embedding of word
            quest_vectorized += embeddings[word]
            num_question_words +=1
    if num_question_words > 0:
      return quest_vectorized/ num_question_words

    return quest_vectorized

def most_common_word(group):
    # Создаем набор слов, чтобы учесть только уникальные
    unique_words = set()
    for item in group:
        unique_words.update(item)
    # Подсчитываем частоту слов
    word_counts = Counter(unique_words)
    # Находим самое частое слово
    if word_counts:
        return word_counts.most_common(1)[0][0]
    else:
        None

def model(file_buffer):
    feedbacks = pd.read_csv(file_buffer, sep=';')
    feedbacks = feedbacks.dropna(how='any')
    feedbacks.columns.values[0] = 'Отзывы'
    navec = Navec.load('navec_hudlit_v1_12B_500K_300d_100q.tar')

    feedbacks['emb'] = [navec['<pad>']] * len(feedbacks)
    feedbacks['decompos'] = [''] * len(feedbacks)

    decomp = []
    emb = []
    for i in range(len(feedbacks)):
        decomp.append(preprocess(feedbacks['Отзывы'][i], stop_words, punctuation_marks, morph));
        emb.append(question_to_vec(feedbacks['Отзывы'].iloc[i], navec, preprocess));
    feedbacks['decompos'] = decomp
    feedbacks['emb'] = emb


    vectors = np.array(feedbacks['emb'].tolist())

    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(X = vectors)
    feedbacks['stand_emb'] = pd.DataFrame(embeddings_scaled).apply(lambda row: row.tolist(), axis=1)
    feedbacks = pd.concat([feedbacks, pd.DataFrame(embeddings_scaled)], axis=1)

    clustering = DBSCAN(eps=5.5, min_samples=1, n_jobs = -1).fit(feedbacks.iloc[:,4:304])
    cluster_labels = clustering.fit_predict(feedbacks.iloc[:,4:304])

    feedbacks['label'] = cluster_labels
    result = feedbacks[['label','decompos']].groupby('label')['decompos'].apply(most_common_word).reset_index()
    result.columns = ['label', 'most_common_word']
    result['most_common_word'] = np.where(result['label'] == -1, 'другое', result['most_common_word'] )

    feedbacks = pd.merge(feedbacks, result, on='label', how='left')

    word_counts = feedbacks['most_common_word'].value_counts().to_dict()
    return word_counts