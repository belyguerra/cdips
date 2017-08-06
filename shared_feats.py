import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder

class GetFeatures(object):
    """get features from the preprocessed data that can be inc in model.py"""
    def __init__(self):
        pass

    def lblencoder(self, df_in, colname):
        lbl = LabelEncoder()
        df = df_in.copy()
        encoded_col = colname + '_enc'
        df[encoded_col] = lbl.fit_transform(df[colname].values)
        return df

    def get_word_count(self, df_in, colname):
        df = df_in.copy()
        df['Word_count'] = df[colname].str.len()
        return df

    def var_in_text_count(self, df_in, varcol, textcol):
        df = df_in.copy()
        newcol = varcol + '_in_text'
        df[newcol] = df.apply(lambda row: row[textcol].count(row[varcol].lower()), axis=1)
        return df

    def merge_dfs(self, df1, df2, joincol):
        df1 = pd.read_csv(df1)
        df2 = pd.read_csv(df2)
        df = pd.merge(df1,df2, on = [joincol])
        return df

    """
    Extract first set of features
    """

def main():
    feat = GetFeatures()

    data_files = [
        (settings.var_training_prep, settings.text_training_prep, settings.train),
        (settings.var_test_prep, settings.text_test_prep, settings.test)
    ]

    for input_var, input_text, output_file in data_files:
        df = feat.merge_dfs(input_var, input_text, settings.id_colname)
        df = feat.var_in_text_count(df, settings.gene_colname, settings.text_colname)
        df = feat.var_in_text_count(df, settings.var_colname, settings.text_colname)
        df = feat.get_word_count(df, settings.text_colname)
        df = feat.lblencoder(df, 'Gene_type')
        df = feat.lblencoder(df, 'Variation_type')
        df.to_csv(output_file, index=False)
        
if __name__ == '__main__':
    main()