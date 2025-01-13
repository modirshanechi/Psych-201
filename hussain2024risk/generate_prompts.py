import pandas as pd
import json
import zipfile

# Load the risk rating data
risk = pd.read_csv('risk_individual.csv')

# Define high-level prompt components
risk_instructs = 'Dear participant, thank you for your interest in our study. This study aims to investigate how people perceive various potential sources of risk. You will be asked to judge the riskiness of 100 of these potential risk sources. The study will take about 9 minutes.\n'
risk_item = 'On a scale from -100 (Safe) to 100 (Risky), how risky is the following?: '
experiment = 'riskRatings'

# Iterate over participants to generate prompts
all_prompts = []
for participant_i in range(len(risk)):
    dat_i = risk.iloc[participant_i]

    # Get ordered risk stimuli
    ordered_risks_1 = dat_i['Multi-Choice Hack 1 - Display Order'].split('|')
    ordered_risks_2 = dat_i['Multi-Choice Hack 2 - Display Order'].split('|')
    block_randomizer = dat_i['FL_26 - Block Randomizer - Display Order'].split('|')
    if block_randomizer == 'FL_47|FL_48':
        ordered_stimuli = ordered_risks_1 + ordered_risks_2
    else:
        ordered_stimuli = ordered_risks_2 + ordered_risks_1

    # Extract text and RT data
    text, RTs = [], []
    for stimulus in ordered_stimuli:
        rating = dat_i[
            f'[Field-counter] / 100 Questions Complete   How safe or risky is the following?:    [Field-1] - {stimulus} - 1'
        ]
        RT = dat_i[f'Timing - {stimulus} - Timing - Page Submit']
        text.append(risk_item + stimulus + '. ' + f'<<{int(rating)}>>.')
        RTs.append(RT)
    text = '\n'.join(text)  # Joining each line
    text = risk_instructs + '\n' + text

    # Extract participant data
    participant = f'riskRatings{participant_i}'
    age = dat_i['Age']
    nationality = dat_i['Nationality']

    # Append to all_prompts
    all_prompts.append({
        'text': text,
        'participant': participant,
        'RTs': RTs,
        'age': age,
        'nationality': nationality,
        'experiment': experiment,
    })

# Save all_prompts to a JSONL file
with open("prompts.jsonl", "w", encoding="utf-8") as f:
    for prompt in all_prompts:
        json.dump(prompt, f, ensure_ascii=False)
        f.write("\n")

# Compress the JSONL file into a ZIP file
with zipfile.ZipFile("prompts.jsonl.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write("prompts.jsonl")