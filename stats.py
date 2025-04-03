
import jsonlines
from glob import glob
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns 
import pandas as pd

def safe_cast_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan

def safe_cast_to_float_array(value): 
    return pd.to_numeric(value, errors='coerce')

def cast_to_gender(value):
    if value == 'F':
        return 'female'
    if value == 'M':
        return 'male'
    if value == 'Female':
        return 'female'
    if value == 'Male':
        return 'male'
    if value == 'NB':
        return 'other'
    if value == 'no-specify':
        return 'other'
    if value == 'no-spe':
        return 'other'
    
    return value

def cast_to_diagnosis(value):
    if value == 'Depression':
        return 'depression'
    if value == 'Bipolar':
        return 'bipolar'
    if value == 'no-lesion-control':
        return 'Healthy'
    if value == 'non-PFC-lesion':
        return 'brain-lesion'

    return value

files = glob('*/*.jsonl')
print(files)
print(len(files))
total_choices = 0
total_participants = 0
total_length = 0
total_experiments = 0
l_symb = '<<'
r_symb = '>>'

# TODO length outliers: 
# pirrone_2018_dots/prompts.jsonl
# rutledge2023happiness/prompts.jsonl
# dubois2022value/prompts.jsonl
# braendle2023empowerment/prompts.jsonl
# witte_thalmann2024exploration/prompts.jsonl 
# castro_rodrigues2022twostep/prompts.jsonl
# TODO ADD PSYCH-101 here and remove added numbers at the bottom
# TODO ADD THE QUESTIONAIRES

stats = {
    'gender': [],
    'age': [],
    'nationality': [],
    'education': [],
    'iq': [],
    'diagnosis': [],
    'RTs': [],
    # 'condition': [], # TODO NEEDED?
}

for file in files:
    
    total_experiments += 1
    exp_participants = 0
    exp_choices = 0
    exp_max_len = -1

    with jsonlines.open(file) as reader:
        for obj in reader:
            if exp_participants == 0:
                print(obj.keys())

            # check that mandatory keys are there
            assert 'text' in obj.keys()
            assert 'participant' in obj.keys()
            assert 'experiment' in obj.keys()
            if 'RTs' in obj.keys():
                assert len(obj['RTs']) == obj['text'].count(l_symb), file + " " + str(exp_participants)
            
            if "sex" in obj.keys():
                obj["gender"] = obj.pop("sex")

            if "location" in obj.keys():
                obj["nationality"] = obj.pop("location")

            if "IQ" in obj.keys():
                obj["iq"] = obj.pop("IQ")

            for key in stats.keys():
                if key in obj.keys():
                    if (key == 'age') or (key == 'iq'):
                        stats[key].extend([safe_cast_to_float(obj[key])])
                    elif key == 'RTs':
                        stats[key].extend(safe_cast_to_float_array(obj[key]))
                    elif key == 'gender':
                        stats[key].extend([cast_to_gender(obj[key])])
                    elif key == 'diagnosis':
                        stats[key].extend([cast_to_diagnosis(obj[key])])
                    else: # nationality, education
                        stats[key].extend([obj[key]])


            if len(obj['text']) > exp_max_len:
                exp_max_len = len(obj['text'])
            exp_participants += 1
            exp_choices += obj['text'].count(l_symb)
            total_length += len(obj['text'])
            
    if exp_max_len > 0:
        print(file)
        print('Number of participants:', exp_participants)
        print('Number of choices:', exp_choices)
        print('Maximum prompt length:', exp_max_len)
        print()
    total_choices += exp_choices
    total_participants += exp_participants


fig1, f1_axes = plt.subplots(nrows=4, ncols=2, figsize=(20, 15))
f1_axes[0, 0].hist(stats['age'])
f1_axes[0, 1].hist(stats['iq'])
f1_axes[1, 0].hist(stats['gender'])
f1_axes[1, 1].hist(stats['nationality'])
f1_axes[2, 0].hist(stats['education'])
f1_axes[2, 1].hist(stats['diagnosis'])
#f1_axes[3, 0].hist(stats['RTs'])
f1_axes[3, 1].hist(stats['gender'])

plt.tight_layout()
sns.despine()
plt.show()

print(total_participants)
print(total_choices)
print(total_length)
print(total_experiments)
print()
print(total_choices + 10681650)
print(len(stats['RTs']))
print(total_participants + 60092)
