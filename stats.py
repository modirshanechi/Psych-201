from datasets import load_dataset
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D
import scienceplots
import matplotlib.gridspec as gridspec

dataset = load_dataset('json', data_files='psych201.jsonl')['train'].to_pandas()
#dataset = load_dataset('json', data_files='psych101/psych101_with_side_information.jsonl')['train'].to_pandas()
print(dataset)
print(dataset['clinical diagnosis'].unique())
print(dataset['education'].unique())
print(dataset['nationality'].unique())

plt.style.use(['nature'])

plt.rcParams.update({
    'xtick.labelsize': 6,
})

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
    'BIS-10',
    'BIS-11',
    'BAS Drive',
    'BAS Fun Seeking',
    'BAS Reward Responsiveness',
    'AUDIT',
    'OCI',
    'DAST',
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
    'AUDIT': 'C3',
    'DAST': 'C3',
    'BAS Drive': 'C2',
    'BAS Fun Seeking': 'C2',
    'BAS Reward Responsiveness': 'C2',
    'BIS-11': 'C2',
    'BIS-10': 'C2',
    'IUS': 'C3',
    'RRQ': 'C3',
    'OCI': 'C3',
}
questionaires_participants = []
colors = []
for questionaire in questionaires:
    questionaires_participants.append(len(dataset[dataset[questionaire] != 'N/A']))
    colors.append(questionnaire_lookup[questionaire])
    

fig1 = plt.figure(figsize=(5.5, 7.5))
gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1])  # Equal row heights

# Create axes using gs[i, j]
f1_axes = np.empty((3, 2), dtype=object)
for i in range(3):
    for j in range(2):
        f1_axes[i, j] = fig1.add_subplot(gs[i, j])

keys = ['age', 'nationality', 'education']
for k, key in enumerate(keys):
    column = dataset[dataset[key] != 'N/A'][key]
    i = (k+2) // 2
    j = (k+2) % 2
    if key == 'age':
        f1_axes[i, j].hist(column.astype(float), bins = 30, rwidth=1)
        f1_axes[i, j].set_xlabel('Age')
    else:
        counts = column.value_counts()
        sorted_counts = counts.sort_values(ascending=False)[:20]
        print(counts.shape)
        sorted_counts.plot(kind='bar', width=0.75, color='C0', ax=f1_axes[i, j])
        f1_axes[i, j].set_xlabel('')
        #f1_axes[i, j].hist(column, bins = 'auto')
    f1_axes[i, j].tick_params(axis='x', rotation=90)
    f1_axes[i, j].set_ylabel('Number of participants')
    f1_axes[i, j].set_title(key.capitalize())

custom_lines_r2 = [
        Line2D([0], [0], color='C0', alpha=0.8, linewidth=5, markersize=3),
        Line2D([0], [0], color='C1', alpha=0.8, linewidth=5, markersize=3),
        Line2D([0], [0], color='C2', alpha=0.8, linewidth=5, markersize=3),
        Line2D([0], [0], color='C3', alpha=0.8, linewidth=5, markersize=3),
        ]

f1_axes[2, 1].bar(questionaires, questionaires_participants, color=colors)
f1_axes[2, 1].tick_params(axis='x', rotation=90)
f1_axes[2, 1].set_ylabel('Number of participants')
f1_axes[2, 1].set_title('Questionaire responses')
f1_axes[2, 1].legend(custom_lines_r2, ['Anxiety', 'Depression', 'Reward sensitivity', 'Miscellaneous'], frameon=False, handlelength=0.5,  loc="upper right", borderaxespad=0, ncol=2)
f1_axes[2, 1].set_ylim(0, 4100)

# sources: https://journals.sagepub.com/doi/full/10.1177/2515245919838781?utm_source=chatgpt.com
# https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2823295
f1_axes[0, 0].bar(['Normal study', 'Mega-study', 'Psych-101', 'Psych-201'], [0.195, 15.715, 60.92, 211.964], color=colors)
f1_axes[0, 0].set_ylabel('Number of participants\n(in thousands)')
f1_axes[0, 0].set_title('Participants')
f1_axes[0, 0].tick_params(axis='x', rotation=90)

colors = ['C0', 'C1']

data = np.load('embeddings.npz')
labels = 1 - data['arr_1']
x = data['arr_0']
# Scatter each group with a label
for i in np.unique(labels):
    f1_axes[0, 1].scatter(x[labels == i, 0], x[labels == i, 1], color=colors[i], label=f'Group {i}')

f1_axes[0, 1].set_xlabel('Embedding dimension 1')
f1_axes[0, 1].set_ylabel('Embedding dimension 2')
f1_axes[0, 1].legend(['Psych-101', 'Psych-201'], loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.5), frameon=False)
f1_axes[0, 1].set_title('Task embeddings')


plt.tight_layout()
sns.despine()
plt.savefig('fig1.pdf', bbox_inches='tight')
plt.savefig('fig1.png', bbox_inches='tight')
plt.show()