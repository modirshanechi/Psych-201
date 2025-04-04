import os
import sys
import pandas as pd
import jsonlines
import math

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import randomized_choice_options

script_dir = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_dir, "sampling_paradigm_2023-04-28_out.csv")
file2 = os.path.join(script_dir, "sampling_paradigm_2023-06-02_out.csv")
df1 = pd.read_csv(file1, low_memory=False)
df2 = pd.read_csv(file2, low_memory=False)
df_all = pd.concat([df1, df2], ignore_index=True)

# Group the data by participant and session
groups = df_all.groupby(["participant.code", "session.code"])

# Fixed instructions text for the Sampling Paradigm task
instructions = (
    "In this task you'll see two buttons on your screen. Each button has some probability of paying out a certain number of points and zero points otherwise. "
    "Your task in each block is to decide which button you prefer to be paid out from.\n\n"
    "Before deciding, you can sample from each button by clicking on it to reveal what it would have paid out if you had chosen it. "
    "You must sample from each button at least once before making your final decision, but you can keep sampling from the two buttons (up to a maximum of 100 times) until you're confident enough to decide.\n\n"
    "You can make a final choice by toggling the grey button below the two options and then pressing \"Next\". You can move the toggle to the left or right to choose the option on the left or right, respectively. "
    "Once you choose a button, you'll see how many points you earned from it and the block will end.\n\n"
    "Note that after each click the system needs about one second to process your entry.\n\n"
    "The average payout from each button remains the same within each block, but may change from one block to the next.\n\n"
    "The first block will be for practice, but the points you earn from the remaining 5 blocks will be used to determine your bonus payment for this task. "
    "You'll be paid a bonus of 5 pence (£0.05) per point.\n"
)

all_prompts_with_RTs = []

# Process each experimental session
for (participant_code, session_code), df_session in groups:
    # Sort trials by block then by trial number
    df_session = df_session.sort_values(by=["block", "trial"])
    
    # Randomize button names for the two options in this session
    button_options = randomized_choice_options(num_choices=2)
    
    # Begin building the prompt text with the instructions
    prompt_text = instructions + "\n"
    
    # Flat list to collect reaction times for the entire session
    RTs_per_session = []
    
    # Iterate over each block (Block 1: practice; Blocks 2-6: incentivized)
    blocks = sorted(df_session["block"].unique())
    for block in blocks:
        df_block = df_session[df_session["block"] == block]
        
        # Label block appropriately
        if block == 1:
            prompt_text += "Practice Block:\n\n"
        else:
            prompt_text += f"Incentivized Block {block - 1}:\n\n"
        
        # Determine sampling trials versus final decision trial
        if (df_block["player.selection"] == 0).any():
            df_sampling = df_block[df_block["player.selection"] != 0]
            final_row = df_block[df_block["player.selection"] == 0].iloc[0]
        else:
            df_sampling = df_block
            final_row = df_block.iloc[-1]
        
        # For each sampling trial, document the sampled button and observed payout.
        for i, (_, row) in enumerate(df_sampling.iterrows()):
            trial_num = int(row["trial"])
            sampling_selection = row["player.selection"]
            sampler_payoff = row["player.sampler_payoff"]
            
            try:
                sampled_button = button_options[int(sampling_selection) - 1]
            except (IndexError, ValueError):
                sampled_button = f"Option{sampling_selection}"
            
            trial_line = (
                f"Trial {trial_num}: You sampled button <<{sampled_button}>> and observed a payout of {sampler_payoff} points.\n"
            )
            prompt_text += trial_line
            
            RTs_per_session.append(row["player.submission_times"] * 1000)
        
        # Process the final decision trial.
        final_decision = final_row["player.final_choice"]
        final_payout = final_row["player.payoff"]
        
        # Map the final decision to the randomized button name.
        if final_decision == final_row["player.option_1_probability"]:
            final_button = button_options[0]
        elif final_decision == final_row["player.option_2_probability"]:
            final_button = button_options[1]
        else:
            try:
                final_index = int(final_decision) - 1
                final_button = button_options[final_index]
            except (IndexError, ValueError):
                final_button = f"Option{final_decision}"
        
        final_line = (
            f"You chose <<{final_button}>> as your final decision. Final payout: {final_payout} points.\n"
        )
        prompt_text += final_line + "\n"
        
        # Append reaction time for the final decision trial (recorded as NaN)
        RTs_per_session.append(float('nan'))
    
    prompt_text += "End of session.\n"
    
    prompt_dict = {
        "text": prompt_text,
        "experiment": "sampling_paradigm",
        "participant": participant_code,
        "session": session_code,
        "RTs": RTs_per_session
    }
    all_prompts_with_RTs.append(prompt_dict)

output_file = os.path.join(script_dir, "prompts.jsonl")
with jsonlines.open(output_file, mode='w') as writer:
    writer.write_all(all_prompts_with_RTs)

print(f"Created {len(all_prompts_with_RTs)} prompt(s) in {output_file}.")