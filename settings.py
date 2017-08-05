import os

"""
user specified settings
"""

"""
data
"""
file_path = '/home/bunge/bguerra/Desktop/git/cdips/data'

var_training_data = os.path.join(file_path, 'training_variants')
text_training_data = os.path.join(file_path, 'training_text')

var_test_data = os.path.join(file_path, 'test_variants')
text_test_data = os.path.join(file_path, 'test_text')

"""
preprocessed data
"""
var_training_prep = os.path.join(file_path, 'training_variants_prep.csv')
text_training_prep = os.path.join(file_path, 'training_text_prep.csv')

var_test_prep = os.path.join(file_path, 'test_variants_prep.csv')
text_test_prep = os.path.join(file_path, 'test_text_prep.csv')
#feed into main:
train = os.path.join(file_path, 'train.csv')
test = os.path.join(file_path, 'test.csv')

"""
data variable names
"""
var_colname = 'Variation'
gene_colname = 'Gene'
text_colname = 'Text'
id_colname = 'ID'
y = 'Class'


"""
bio_dicts
"""
gene_fam_data = os.path.join(file_path, 'gene_fam.txt')

sub_dict= {'A': 'Neu', #'alanine'
           'R': 'Pos', #'arginine'
           'N': 'Neu', #'asparagine'
           'D': 'Neg', #'aspartic acid'
           'B': 'Neu', #'asparagine|aspartic acid'
           'C': 'Neu', #'cysteine'
           'E': 'Neg', #'glutamic acid'
           'Q': 'Neu', #'glutamine'
           'Z': 'Neu', #'glutamine|glutamic acid'
           'G': 'Neu', #'glycine'
           'H': 'Pos', #'histidine'
           'I': 'Neu', #'isoleucine'
           'L': 'Neu', #'leucine'
           'K': 'Pos', #'lysine'
           'M': 'Neu', #'methionine'
           'F': 'Neu', #'phenylalanine'
           'P': 'Neu', #'proline'
           'S': 'Neu', #'serine'
           'T': 'Neu', #'threonine'
           'W': 'Neu', #'tryptophan'
           'Y': 'Neu', #'tyrosine'
           'V': 'Neu' #'valine'
          }

var_dict = {'del|silencing|hypermethylation': 'Deletion',
            'ins' : 'Insertion',
            'trunc' : 'Truncation',
            'dup' : 'Duplication',
            'fusion|fs': 'Fusion',
            'spli': 'Splice'
            }

"""
text
"""
academic_words = ['abstract', 'introduction', 'method', 'methods','results',
                  'discussion', 'fig', 'figure','table', 'supplementary', 'mm',
                  'sample', 'data', 'et','al', 'findings', 'specimen', 'laboratory']
