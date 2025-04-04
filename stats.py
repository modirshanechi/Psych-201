from datasets import load_dataset
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

dataset = load_dataset('json', data_files='psych201.jsonl')['train'].to_pandas()
#dataset = load_dataset('json', data_files='psych101/psych101_with_side_information.jsonl')['train'].to_pandas()

fig1, f1_axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))
keys = ['gender', 'age', 'nationality', 'education']
for k, key in enumerate(keys):
    column = dataset[dataset[key] != 'N/A'][key]
    print(np.unique(column))
    i = k // 2
    j = k % 2

    print(i)
    print(j)
    print()
    if key == 'age':
        f1_axes[i, j].hist(column.astype(float), bins = 25)
    else:
        f1_axes[i, j].hist(column, bins = 'auto')
    f1_axes[i, j].tick_params(axis='x', rotation=90)


plt.tight_layout()
sns.despine()
plt.show()