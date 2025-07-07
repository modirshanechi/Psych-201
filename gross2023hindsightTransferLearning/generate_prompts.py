#!/usr/bin/env python3
import os
import pandas as pd
import jsonlines


all_prompts = []
data = pd.read_csv("gross2023hindsightTransferLearning/data/gross2023exp_psych201.csv")

instr_control = "This experiment consists of five different phases.\n"\
"In Phase 1, you should provide an estimate of the population size of 46 different countries.\n"\
"In Phase 2, you read a short text with trivia information, which are not related to the estimation task.\n"\
"In Phase 3, you are presented with the same 46 countries as in Phase 1. For each country, you should recall your estimate from Phase 1.\n"\
"In Phase 4, you should provide an estimate of the population size of 46 new countries, which were not presented in Phase 1.\n"\
"In Phase 5, you should provide an estimate of the population size of the 46 different countries from Phase 1 again.\n\n"

instr_concurrent = "The experiment consists of five different phases.\n"\
"In Phase 1, you should provide an estimate of the population size of 46 different countries.\n"\
"In Phase 2, you read a short text with trivia information, which are not related to the estimation task.\n"\
"In Phase 3, you are presented with the same 46 countries as in Phase 1. For each country, you should recall your estimate from Phase 1.\n"\
"For half of the countries, you will simultaneously be presented with the true population size.\n"\
"In Phase 4, you should provide an estimate of the population size of 46 new countries, which were not presented in Phase 1.\n"\
"In Phase 5, you should provide an estimate of the population size of the 46 different countries from Phase 1 again.\n\n"

instr_preceding = "The experiment consists of five different phases.\n"\
"In Phase 1, you should provide an estimate of the population size of 46 different countries.\n"\
"In Phase 2, you will be presented with the true population size for half of the countries from Phase 1.\n"\
"In Phase 3, you are presented with the same 46 countries as in Phase 1. For each country, you should recall your estimate from Phase 1.\n"\
"In Phase 4, you should provide an estimate of the population size of 46 new countries, which were not presented in Phase 1.\n"\
"In Phase 5, you should provide an estimate of the population size of the 46 different countries from Phase 1 again.\n\n"

# Subject loop
for subject, df_subject in data.groupby("subject"):

    condition = df_subject["cond"].iloc[0]  # Extract condition (same for all rows of this subject)

    if condition == 1:

        prompt = instr_control

        # Phase 1
        prompt+="Phase 1.\n"

        df_phase1 = df_subject[df_subject["phase"] == 1]  # Extract Phase 1 trials
        min_seq = df_phase1["sequence"].min()
        max_seq = df_phase1["sequence"].max()

        #print(f"  Sequence range: {min_seq} to {max_seq}")

        ## Loop through the sequence range dynamically
        for seq in range(min_seq, max_seq + 1):

            df_trial = df_phase1[df_phase1["sequence"] == seq]  # Filter for the specific sequence
            if not df_trial.empty:  # Ensure the trial exists
                trial_data = df_trial.iloc[0]  # Get the first matching row
                prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

        # Phase 2
        prompt+="Phase 2.\n"

        prompt+="You read a short text with trivia information, which are unrelated to the estimation task.\n"

        # Phase 3
        prompt+="Phase 3.\n"

        df_phase3 = df_subject[df_subject["phase"] == 3]  # Extract Phase 1 trials
        min_seq = df_phase3["sequence"].min()
        max_seq = df_phase3["sequence"].max()

        #print(f"  Sequence range: {min_seq} to {max_seq}")

        ## Loop through the sequence range dynamically
        for seq in range(min_seq, max_seq + 1):

            df_trial = df_phase3[df_phase3["sequence"] == seq]  # Filter for the specific sequence
            if not df_trial.empty:  # Ensure the trial exists
                trial_data = df_trial.iloc[0]  # Get the first matching row
                prompt+=f"How many people live in {trial_data['item']}? What was your ORIGINAL answer? Your response is <<{trial_data['response']}>>.\n"

        # Phase 4
        prompt+="Phase 4.\n"

        df_phase4 = df_subject[df_subject["phase"] == 4]  # Extract Phase 1 trials
        min_seq = df_phase4["sequence"].min()
        max_seq = df_phase4["sequence"].max()

        #print(f"  Sequence range: {min_seq} to {max_seq}")

        ## Loop through the sequence range dynamically
        for seq in range(min_seq, max_seq + 1):

            df_trial = df_phase4[df_phase4["sequence"] == seq]  # Filter for the specific sequence
            if not df_trial.empty:  # Ensure the trial exists
                trial_data = df_trial.iloc[0]  # Get the first matching row
                prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

        # Phase 5
        prompt+="Phase 5.\n"

        df_phase5 = df_subject[df_subject["phase"] == 5]  # Extract Phase 1 trials
        min_seq = df_phase5["sequence"].min()
        max_seq = df_phase5["sequence"].max()

        #print(f"  Sequence range: {min_seq} to {max_seq}")

        ## Loop through the sequence range dynamically
        for seq in range(min_seq, max_seq + 1):

            df_trial = df_phase5[df_phase5["sequence"] == seq]  # Filter for the specific sequence
            if not df_trial.empty:  # Ensure the trial exists
                trial_data = df_trial.iloc[0]  # Get the first matching row
                prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

    else:
        if condition == 2:

            prompt = instr_concurrent

            # Phase 1
            prompt+="Phase 1.\n"

            df_phase1 = df_subject[df_subject["phase"] == 1]  # Extract Phase 1 trials
            min_seq = df_phase1["sequence"].min()
            max_seq = df_phase1["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically

            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase1[df_phase1["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

            # Phase 2
            prompt+="Phase 2.\n"

            prompt+="You read a short text with trivia information, which are unrelated to the estimation task.\n"

            # Phase 3
            prompt+="Phase 3.\n"

            df_phase3 = df_subject[df_subject["phase"] == 3]  # Extract Phase 1 trials
            min_seq = df_phase3["sequence"].min()
            max_seq = df_phase3["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase3[df_phase3["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    if trial_data["itemtype"] == 0: # control
                        prompt += f"How many people live in {trial_data['item']}? What was your ORIGINAL answer? Your response is <<{trial_data['response']}>>.\n"
                    elif trial_data["itemtype"] == 1: # experimental
                        prompt += f"How many people live in {trial_data['item']}? True population: {trial_data['population']}. What was your ORIGINAL answer? Your response is <<{trial_data['response']}>>.\n"

            # Phase 4
            prompt+="Phase 4.\n"

            df_phase4 = df_subject[df_subject["phase"] == 4]  # Extract Phase 1 trials
            min_seq = df_phase4["sequence"].min()
            max_seq = df_phase4["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase4[df_phase4["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

            # Phase 5
            prompt+="Phase 5.\n"

            df_phase5 = df_subject[df_subject["phase"] == 5]  # Extract Phase 1 trials
            min_seq = df_phase5["sequence"].min()
            max_seq = df_phase5["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase5[df_phase5["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"


        else:

            prompt = instr_preceding

            # Phase 1
            prompt+="Phase 1.\n"

            df_phase1 = df_subject[df_subject["phase"] == 1]  # Extract Phase 1 trials
            min_seq = df_phase1["sequence"].min()
            max_seq = df_phase1["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase1[df_phase1["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

            # Phase 2
            prompt+="Phase 2.\n"

            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase1[df_phase1["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    if trial_data["itemtype"] == 1: # experimental
                        prompt+=f"{trial_data['population']} people live in {trial_data['item']}.\n"

            # Phase 3
            prompt+="Phase 3.\n"

            df_phase3 = df_subject[df_subject["phase"] == 3]  # Extract Phase 1 trials
            min_seq = df_phase3["sequence"].min()
            max_seq = df_phase3["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase3[df_phase3["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? What was your ORIGINAL answer? Your response is <<{trial_data['response']}>>.\n"

            # Phase 4
            prompt+="Phase 4.\n"

            df_phase4 = df_subject[df_subject["phase"] == 4]  # Extract Phase 1 trials
            min_seq = df_phase4["sequence"].min()
            max_seq = df_phase4["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):

                df_trial = df_phase4[df_phase4["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"

            # Phase 5
            prompt+="Phase 5.\n"

            df_phase5 = df_subject[df_subject["phase"] == 5]  # Extract Phase 1 trials
            min_seq = df_phase5["sequence"].min()
            max_seq = df_phase5["sequence"].max()

            #print(f"  Sequence range: {min_seq} to {max_seq}")

            ## Loop through the sequence range dynamically
            for seq in range(min_seq, max_seq + 1):
                df_trial = df_phase5[df_phase5["sequence"] == seq]  # Filter for the specific sequence
                if not df_trial.empty:  # Ensure the trial exists
                    trial_data = df_trial.iloc[0]  # Get the first matching row
                    prompt+=f"How many people live in {trial_data['item']}? Your response is <<{trial_data['response']}>>.\n"


    all_prompts.append({'text': prompt ,
                        'experiment': 'gross2023hindsightTransferLearning' ,
                        'participant': subject ,
                        })

# Write this record as a JSON line.
with jsonlines.open('prompts.jsonl', 'w') as writer:
    writer.write_all(all_prompts)
