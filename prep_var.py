import pandas as pd
import settings
import os

class PrepVar(object):
    """
    mainly recodes instances of the gene/variants into their classes
    needs all bio_dicts (see settings)
    """
    def __init__(self):
        pass

    def get_gene_class(self, gene_data):
        gene_class_dict = {}
        with open(gene_data) as f:
            # skip headers
            f.readline()
            for line in f:
                data = line.rstrip('\r\n').split('\t')
                app_symbol = data[0]
                syn = data[4]
                prev_symbols = data[2]
                fam_id = data[6]

                if len(fam_id) == 0:
                    continue

                app_symb_all = app_symbol.split('|')
                syn_all = [s.strip() for s in syn.split(',')]
                prev_symbols_all = [p.strip() for p in prev_symbols.split(',')]
                fam_id_all = fam_id.split('|')

                for f in fam_id_all:
                    for a in app_symb_all:
                        gene_class_dict[a] = f
                    for s in syn_all:
                        gene_class_dict[s] = f
                    for p in prev_symbols_all:
                        gene_class_dict[p] = f
        return gene_class_dict


    def prep_recode(self, df_in, colname, bio_dict):
        df = df_in.copy()
        recoded_colname = colname + '_type'
        for key, val in bio_dict.items():
            df.loc[df[colname].str.contains(key, case=False), recoded_colname] = val
        return df

    def prep_recode_special(self, df_in, colname):
        df = df_in.copy()
        recoded_colname = colname + '_type'
        #darn some entires have del/ins with all sorts of patterns
        df.loc[(df[colname].str.contains('del', case=False) & df[colname].str.contains('ins', case=False)), recoded_colname] = 'InDel'
        return df

    def subs_recode(self, df_in, colname, bio_dict):
        df = df_in.copy()
        recoded_colname = colname + '_type'
        sub_pattern= '^[A-Z]\d+[A-Z\*]$|^(null)\d+[A-Z\*]$'
        sub_specific_pattern = '^[A-Z]\d+[A-Z]$'
        #captures all the sub patterns
        df[recoded_colname] = df[colname].str.replace(sub_pattern, 'Substitution')
        #maps amino acid to polarity
        df['am1'] = df.loc[df[colname].str.match(sub_specific_pattern)][colname].str[:1]
        df['am2'] = df.loc[df[colname].str.match(sub_specific_pattern)][colname].str[-1:]
        #specifies the polarity change type
        df['am1'].replace(bio_dict, inplace=True)
        df['am2'].replace(bio_dict, inplace=True)
        df['sub_type'] = df['am1'] + df['am2']
        #add to df
        df.loc[df.sub_type.notnull(), recoded_colname] = df.sub_type
        df.drop(['am1', 'am2', 'sub_type'], axis=1, inplace=True)
        return df

    """
    Prep variables:
    """
    def prep_variants(self, df_in):
        df = df_in.copy()
        colname = settings.var_colname
        #order matters
        df = self.subs_recode(df, colname, settings.sub_dict)
        df = self.prep_recode(df, colname, settings.var_dict)
        df = self.prep_recode_special(df, colname)
        return df

    def prep_genes(self, df_in):
        df = df_in.copy()
        colname = settings.gene_colname
        gene_dict = self.get_gene_class(settings.gene_fam_data)
        df = self.prep_recode(df, colname, gene_dict)
        return df

def main():
    prep = PrepVar()
    data_files = [
        (settings.var_training_data, settings.var_training_prep),
        (settings.var_test_data, settings.var_test_prep)
    ]

    for input_file, output_file in data_files:
        df = pd.read_csv(input_file)
        df = prep.prep_variants(df)
        df = prep.prep_genes(df)
        df.to_csv(output_file, index=False)
        
if __name__ == '__main__':
    main()
