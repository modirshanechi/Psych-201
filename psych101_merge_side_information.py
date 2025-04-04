
import jsonlines
from datasets import load_dataset
from utils import * 

datasets = ['training', 'testing_t1']

side_information = {}
for dataset in datasets:
    file = 'psych101_side_information_' + dataset + '.jsonl'
    with jsonlines.open(file) as reader:
        for obj in reader:
            dict_partcipants = {}
            dict_partcipants['experiment'] = obj['experiment']
            dict_partcipants['participant'] = obj['participant']

            if 'RTs' in obj.keys():
                dict_partcipants['RTs'] = safe_cast_to_float_array(obj['RTs'])
            else:
                dict_partcipants['RTs'] = []

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

            if 'location' in obj.keys():
                dict_partcipants['location'] = cast_to_location(obj['location'])
            else:
                dict_partcipants['location'] = 'N/A'

            if 'education' in obj.keys():
                dict_partcipants['education'] = cast_to_education(obj['education'])
            else:
                dict_partcipants['education'] = 'N/A'

            if 'diagnosis' in obj.keys():
                dict_partcipants['diagnosis'] = cast_to_diagnosis(obj['diagnosis'])
            else:
                dict_partcipants['diagnosis'] = 'N/A'
                
            side_information[(obj['experiment'], obj['participant'])] = dict_partcipants

full_data = []
for dataset in datasets:
    file = 'psych101_' + dataset + '.jsonl'
    with jsonlines.open(file) as reader:
        for obj in reader:
            if (str(obj['experiment']), str(obj['participant'])) in side_information.keys():
                full_data.append({
                    'text': obj['text'], 
                    'experiment': str(obj['experiment']), 
                    'participant': str(obj['participant']),
                    'RTs': side_information[(str(obj['experiment']), str(obj['participant']))]['RTs'],
                    'gender': side_information[(str(obj['experiment']), str(obj['participant']))]['gender'],
                    'age': side_information[(str(obj['experiment']), str(obj['participant']))]['age'],
                    'nationality': side_information[(str(obj['experiment']), str(obj['participant']))]['nationality'],
                    'location': side_information[(str(obj['experiment']), str(obj['participant']))]['location'],
                    'education': side_information[(str(obj['experiment']), str(obj['participant']))]['education'],
                    'diagnosis': side_information[(str(obj['experiment']), str(obj['participant']))]['diagnosis'],
                })
            else:
                full_data.append({
                    'text': obj['text'], 
                    'experiment': str(obj['experiment']), 
                    'participant': str(obj['participant']),
                    'RTs': [],
                    'gender': 'N/A',
                    'age': 'N/A',
                    'nationality': 'N/A',
                    'location': 'N/A',
                    'education': 'N/A',
                    'diagnosis': 'N/A',
                })


print(len(full_data))
with jsonlines.open('psych101/psych101_with_side_information.jsonl', 'w') as writer:
    writer.write_all(full_data)

    

'''
rts_training = []

for folder in with_rt:
    psych101_subset = dataset['train'].filter(lambda example: example['experiment'].startswith(folder))
    train_participants = psych101_subset['participant']
    train_experiments = psych101_subset['experiment']
    zipped_part_exp = list(zip(train_participants, train_experiments))
    # save to jsonl
    with jsonlines.open(folder + '/rts.jsonl') as reader:
        for obj in reader:
            if (str(obj['participant']), str(obj['experiment'])) in zipped_part_exp:
                rts_training.append({'RTs': obj['RTs'], 'experiment': str(obj['experiment']), 'participant': str(obj['participant'])})

# save all data sets
with jsonlines.open('0_full_data/rts_training.jsonl', 'w') as writer:
    writer.write_all(rts_training)'''