import settings
import prep_var
import prep_text
import shared_feat
import model

"""
Here you can put the steps you want to run...
"""

def main():
    prep_var.main()
    prep_text.main()
    shared_feat.main()
    model.main()
    pass

if __name__ == '__main__':
    main()
