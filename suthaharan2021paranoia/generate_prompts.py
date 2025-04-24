import os
import sys
import numpy as np
import pandas as pd
import jsonlines
from tqdm import trange

sys.path.append("..")
from utils import randomized_choice_options

# ≃ 32K tokens soft limit
CHARACTER_LIMIT = 32000 * 4

def generate_prompts_reversal(path_prefix: str,
                              datasets: list[str],
                              output_file: str = "prompts_reversal.jsonl",
                              verbose: bool = False):
    """
    Generates one full-session prompt per subject for a three-armed
    probabilistic reversal learning task. Marks subject responses with <<…>>.
    """
    all_prompts = []

    for ds in datasets:
        df = pd.read_csv(ds)
        subjects = df['subject'].unique()

        for subj_idx in trange(len(subjects), desc=f"Dataset {ds}"):
            subject_id = subjects[subj_idx]
            df_sub = df[df['subject'] == subject_id]
            labels = randomized_choice_options(num_choices=3)

            # --- Richer instruction paragraph ---
            prompt = (
                "In this experiment you will repeatedly choose between three slot machines, "
                f"labeled {labels[0]}, {labels[1]}, and {labels[2]}. On each trial, select one machine "
                "by pressing its corresponding key. Each machine pays out points probabilistically. "
                "In the first two blocks the machines pay out with probabilities [0.9, 0.5, 0.1], "
                "and in later blocks these shift to [0.8, 0.5, 0.2]. "
                "Whenever you select the currently best machine ten times in a row, the reward probabilities "
                "will reverse: the high‐paying machine becomes low, and vice versa. "
                "Your goal is to earn as many points as possible by adapting your choices to these changes. "
                "You will receive immediate feedback after each choice, showing how many points you earned.\n\n"
            )

            for game in sorted(df_sub['game'].unique()):
                df_game = df_sub[df_sub['game'] == game]
                n_trials = int(df_game['trial'].max()) + 1
                prompt += f"Block {int(game)+1}  —  {n_trials} trials:\n"
                for t in range(n_trials):
                    row = df_game[df_game['trial'] == t].iloc[0]
                    choice_idx = int(row['choice'])
                    rew = row['reward']
                    chosen = labels[choice_idx]
                    prompt += f"Trial {t+1}: You press <<{chosen}>> and receive {rew} points.\n"
                prompt += "\n"

            prompt = prompt.rstrip()

            if verbose:
                length = len(prompt)
                print(f"[{subject_id}] length={length:,} chars")
                assert length < CHARACTER_LIMIT, (
                    f"Prompt too long ({length} > {CHARACTER_LIMIT})"
                )

            all_prompts.append({
                'text': prompt,
                'experiment': os.path.join(path_prefix, os.path.basename(ds)),
                'participant': subject_id
            })

    with jsonlines.open(output_file, 'w') as w:
        w.write_all(all_prompts)
    print(f"Wrote {len(all_prompts)} prompts → {output_file}")


if __name__ == "__main__":
    datasets = ["exp_Reed_2020.csv", 'exp_Suthaharan_2021.csv']
    generate_prompts_reversal(
        path_prefix="suthaharan2021paranoia/",
        datasets=datasets,
        output_file="prompts.jsonl",
        verbose=True
    )
