from datasets import load_dataset
from collections import defaultdict
import numpy as np 

psych201 = load_dataset("json", data_files="psych201.jsonl")
print(psych201)

participant_counters = defaultdict(int)
choice_counters = defaultdict(int)


def reindex(example):
    exp = example["experiment"]
    new_id = participant_counters[exp]
    in_eval = (new_id < 100) or (choice_counters[exp] < 10000)

    participant_counters[exp] += 1
    choice_counters[exp] += example["text"].count("<<")

    return {"participant": str(new_id), "in_eval": in_eval}

psych201 = psych201.map(reindex, num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "demircan2024evaluatingcategory", num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "demircan2024evaluatingreward", num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "feher2020humans", num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "xu2021novelty", num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "singh2022representing", num_proc=8)
psych201 = psych201.filter(lambda example: example['study'] != "jansen2021logic", num_proc=8)

print(psych201)
psych201.push_to_hub("marcelbinz/Psych-201-devel")

psych201eval = psych201.filter(lambda example: example['in_eval'], num_proc=8)

print(psych201eval)
psych201eval.push_to_hub("marcelbinz/Psych-201-eval")


'''
for feature in psych201['train'].features:
    print(feature)
    if (feature != 'text') and (feature != 'RTs'):
        print(np.unique(psych201['train'][feature]))
'''