from datasets import load_dataset
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import scienceplots

dataset = load_dataset('json', data_files='psych201.jsonl')['train'].to_pandas()
#dataset = load_dataset('json', data_files='psych101/psych101_with_side_information.jsonl')['train'].to_pandas()
print(dataset)
plt.style.use(['nature'])

questionaires = [
    'STAI-T',
    'STAI-S',
    'STICSA-T somatic',
    'STICSA-T cognitive',
    'GAD-7',
    'PSWQ',
    'SDS',
    'BDI-II',
    'PHQ-8',
    'PHQ-9',
    'BIS-11',
    'BAS Drive',
    'BAS Fun Seeking',
    'BAS Reward Responsiveness',
    'DAST',
    'AUDIT',
    'OCI',
    'IUS',
    'RRQ',
]

# C0 Anxiety
# C1 Depression
# C2 Substance Use
# C3 Reward & Impulsivity
# C4 Miscellaneous

questionnaire_lookup = {
    'STICSA-T somatic': 'C0',
    'STICSA-T cognitive': 'C0',
    'STAI-S': 'C0',
    'STAI-T': 'C0',
    'PSWQ': 'C0',
    'GAD-7': 'C0',
    'PHQ-9': 'C1',
    'PHQ-8': 'C1',
    'BDI-II': 'C1',
    'SDS': 'C1',
    'AUDIT': 'C2',
    'DAST': 'C2',
    'BAS Drive': 'C3',
    'BAS Fun Seeking': 'C3',
    'BAS Reward Responsiveness': 'C3',
    'BIS-11': 'C3',
    'IUS': 'C4',
    'RRQ': 'C4',
    'OCI': 'C4',
}
questionaires_participants = []
colors = []
for questionaire in questionaires:
    questionaires_participants.append(len(dataset[dataset[questionaire] != 'N/A']))
    colors.append(questionnaire_lookup[questionaire])
    

fig1, f1_axes = plt.subplots(nrows=3, ncols=2, figsize=(5.5, 5.5))
keys = ['age', 'nationality', 'education']
for k, key in enumerate(keys):
    column = dataset[dataset[key] != 'N/A'][key]
    i = (k+2) // 2
    j = (k+2) % 2
    if key == 'age':
        f1_axes[i, j].hist(column.astype(float), bins = 30)
    else:
        counts = column.value_counts()
        sorted_counts = counts.sort_values(ascending=False)[:30]
        print(counts.shape)
        sorted_counts.plot(kind='bar', color='C0', ax=f1_axes[i, j])
        #f1_axes[i, j].hist(column, bins = 'auto')
    f1_axes[i, j].tick_params(axis='x', rotation=90)

f1_axes[2, 1].bar(questionaires, questionaires_participants, color=colors)
f1_axes[2, 1].tick_params(axis='x', rotation=90)

plt.tight_layout()
sns.despine()
plt.show()