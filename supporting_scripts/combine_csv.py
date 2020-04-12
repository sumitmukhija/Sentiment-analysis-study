import os
import glob
import pandas as pd
os.chdir(os.getcwd()+"/data/soldiers")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv("combined_soldiers.csv", index=False, encoding='utf-8-sig')
