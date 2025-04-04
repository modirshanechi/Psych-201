
import jsonlines
from glob import glob
import numpy as np
import pandas as pd
from utils import * 
import math

files = glob('*/*.jsonl')
print(files)
print(len(files))

l_symb = '<<'
r_symb = '>>'

# TODO ADD PSYCH-101 here and remove added numbers at the bottom
# TODO ADD THE QUESTIONAIRES
# TODO MAKE ALL 0 and neg rts nan

full_data = []
total_experiments = 0
for file in files:
    
    total_experiments += 1
    exp_participants = 0
 
    if True:
        with jsonlines.open(file) as reader:
            for obj in reader:
                if exp_participants == 0:
                    print(obj.keys())

                # check that mandatory keys are there
                assert 'text' in obj.keys()
                assert 'participant' in obj.keys()
                assert 'experiment' in obj.keys()
                # check that RTs match number of choices

                if 'RTs' in obj.keys():
                    if len(obj['RTs']) > 0:
                        assert len(obj['RTs']) == obj['text'].count(l_symb), (obj['experiment'], obj['participant'])
                
                # rename sex to gender
                if "sex" in obj.keys():
                    obj["gender"] = obj.pop("sex")

                # rename location to nationality
                if "location" in obj.keys():
                    obj["nationality"] = obj.pop("location")

                dict_partcipants = {
                    'text': obj['text'],
                    'experiment': str(obj['experiment']), 
                    'participant': str(obj['participant']),
                }

                if ('RTs' in obj.keys()) and (len(obj['RTs']) > 0):
                    dict_partcipants['RTs'] = safe_cast_to_float_array(obj['RTs'])
                else:
                    dict_partcipants['RTs'] = obj['text'].count(l_symb) * [math.nan]

                
                if 'gender' in obj.keys():
                    dict_partcipants['gender'] = cast_to_gender(obj['gender'])
                else:
                    dict_partcipants['gender'] = 'N/A'

                if 'age' in obj.keys():
                    dict_partcipants['age'] = safe_cast_to_float(obj['age'])
                else:
                    dict_partcipants['age'] = 'N/A'

                if 'nationality' in obj.keys():
                    dict_partcipants['nationality'] = cast_to_nationality(obj['nationality'])
                else:
                    dict_partcipants['nationality'] = 'N/A'

                if 'education' in obj.keys():
                    dict_partcipants['education'] = cast_to_education(obj['education'])
                else:
                    dict_partcipants['education'] = 'N/A'

                if 'diagnosis' in obj.keys():
                    dict_partcipants['diagnosis'] = cast_to_diagnosis(obj['diagnosis'])
                else:
                    dict_partcipants['diagnosis'] = 'N/A'
                

                full_data.append(dict_partcipants)
                exp_participants += 1
        
print('Number of participants:', len(full_data))
  
    
# save all data sets
with jsonlines.open('psych201.jsonl', 'w') as writer:
    writer.write_all(full_data)