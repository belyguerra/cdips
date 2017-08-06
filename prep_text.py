from nltk.corpus import stopwords
import nltk
import settings
import pandas as pd
import re

class PrepText(object):
    """
    PrepText: tokenizing, normalize, stem
    """
    def __init__(self):
        pass

    def remove_stop(self, text, stopw_dict):
        return [word for word in text if word not in stopw_dict]

    def remove_symbols(self, text):
        pattern = re.compile("^[A-Za-z0-9_-]*$")
        return [word for word in text if word and re.match(pattern, word) and not word.isdigit()]

    def stem_words(self, text, stemmer):
        return [stemmer.stem(word) for word in text]

    def toke(self, df_in, colname):
        df = df_in.copy()
        df[colname] = df[colname].apply(nltk.word_tokenize)
        return df

    def normalize_text(self, df_in, colname, stopw_dict):
        df = df_in.copy()
        df[colname]= df[colname].apply(lambda x: self.remove_stop(x, stopw_dict))
        df[colname]= df[colname].apply(lambda x: self.remove_symbols(x))
        return df

    def stem_text(self, df_in, colname, stemmer):
        df = df_in.copy()
        df[colname]= df[colname].apply(lambda x: self.stem_words(x, stemmer))
        return df


def main():
    """
    remember you need nltk dependencies for first use:
    nltk.download('punkt')  #tokenizer
    nltk.download('stopwords')
    """
    prep = PrepText()

    stemmer = nltk.SnowballStemmer('english')
    stop = stopwords.words('english')
    stop = stop + settings.academic_words

    data_files = [
        (settings.text_training_data, settings.text_training_prep),
        (settings.text_test_data, settings.text_test_prep)
    ]
    data_cols = [settings.id_colname, settings.text_colname]


    for input_file, output_file in data_files:
        df = pd.read_csv(input_file, sep='\|\|',skiprows=1, engine='python', names=data_cols)
        df[settings.text_colname] = df[settings.text_colname].str.lower()
        df = prep.toke(df, settings.text_colname)
        df = prep.normalize_text(df, settings.text_colname, stop)
        df = prep.stem_text(df, settings.text_colname, stemmer)
        df.to_csv(output_file, index=False)
        
if __name__ == '__main__':
    main()
