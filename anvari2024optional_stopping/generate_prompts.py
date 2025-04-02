import os
import sys
import pandas as pd
import jsonlines

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load data
script_dir = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_dir, "optional_stopping_2023-04-28_out.csv")
file2 = os.path.join(script_dir, "optional_stopping_2023-06-02_out.csv")
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df_all = pd.concat([df1, df2], ignore_index=True)

# Group the data by participant and session
groups = df_all.groupby(["participant.code", "session.code"])

# Fixed instructions text for the Optional Stopping Task with Recall
instructions = (
    "In each block of this task, you will search for rewards among 20 different boxes. "
    "You can open a box by clicking on it, which reveals how much it's worth. Each box has a randomly determined value between 0 and 10. "
    "However, every time you open a box you pay a cost ranging from 0.05 to 0.4 points depending on the block you are in.\n\n"
    "After opening a box, you can either settle on the highest value among the opened boxes—thereby ending that block—or keep opening more boxes (up to a maximum of 20).\n\n"
    "The costs for opening boxes, as well as the rewards, change from one block to the next. At the end of each block, "
    "you will receive the highest value you have discovered minus the total cost incurred from opening boxes.\n\n"
    "The first block is for practice, but the earnings of the remaining 8 blocks will be added up and used to calculate your bonus. "
    "For this task, you will be paid a bonus of 2 pence (£0.02) per point.\n\n"
    "Note: You can recall the best option encountered so far when deciding to stop."
)

all_prompts = []

# Process each experimental session
for (participant_code, session_code), df_session in groups:
    # Sort trials by block then by trial number
    df_session = df_session.sort_values(by=["block", "trial"])
    
    # Begin building the prompt text with the instructions
    prompt_text = instructions + "\n\n"
    
    # Global list for reaction times (one list per block)
    RTs_per_session = []
    
    # Iterate over each unique block (Block 1: Practice; Blocks 2-9: Incentivized)
    for block in sorted(df_session["block"].unique()):
        df_block = df_session[df_session["block"] == block]
        # Filter out rows with no valid chest selection
        df_block = df_block[pd.notna(df_block["player.chest_selection"])]
        
        if block == 1:
            prompt_text += "Practice Block:\n\n"
        else:
            cost_per_box = df_block.iloc[0]["player.cost_order"]
            prompt_text += f"Incentivized Block {block - 1} (Cost per box: {cost_per_box} points):\n\n"
        
        # Initialize a list to collect reaction times for this block
        rt_list = []
        
        # Iterate over the (filtered) trials in the block
        for _, row in df_block.iterrows():
            trial_num = int(row["trial"])
            chest_selection = row["player.chest_selection"]
            chest_payoff = row["player.chest_payoff"]
            accumulated_cost = row["player.accumulated_cost"]
            current_best = row["player.current_best_payoff"]
            submission_time = row["player.submission_times"]
            rt_list.append(submission_time)
            
            # Convert chest_selection to an integer (if valid), add 1, and format as "box X"
            if pd.notna(chest_selection):
                sel_int = int(chest_selection)
                sel_str = f"{sel_int + 1}"
            else:
                sel_str = "nan"
            
            # Format numbers for payoff, current best, and accumulated cost
            payoff_str = f"{chest_payoff:.2f}" if pd.notna(chest_payoff) else "nan"
            best_str = f"{current_best:.2f}" if pd.notna(current_best) else "nan"
            acc_cost_str = f"{accumulated_cost:.2f}" if pd.notna(accumulated_cost) else "nan"
            
            trial_line = (
                f"Trial {trial_num}: You opened box <<{sel_str}>> revealing {payoff_str} points. "
                f"Current best: {best_str} points. Accumulated cost: {acc_cost_str} points.\n"
            )
            prompt_text += trial_line
        
        # Append a "NaN" for the final decision reaction time (as no submission time is recorded for stopping)
        rt_list.append("NaN")
        
        # Add a summary of the stopping decision:
        final_row = df_block.iloc[-1]
        final_trial = int(final_row["trial"])
        if final_trial < 20:
            net_payout = final_row["player.current_best_payoff"] - final_row["player.accumulated_cost"]
            prompt_text += (
                f"At trial {final_trial}, you decided to stop opening boxes, settling on your best option. "
                f"Your net payoff for this block is {net_payout:.2f} points.\n\n"
            )
        else:
            prompt_text += "You opened all 20 boxes.\n\n"
        
        RTs_per_session.append(rt_list)
    
    prompt_text += "End of session.\n"
    
    # Create the prompt dictionary and add the RTs as a separate field
    prompt_dict = {
        "text": prompt_text,
        "experiment": "optional_stopping_with_recall",
        "participant": participant_code,
        "session": session_code,
        "RTs": RTs_per_session
    }
    all_prompts.append(prompt_dict)

output_file = os.path.join(script_dir, "prompts.jsonl")
with jsonlines.open(output_file, mode='w') as writer:
    writer.write_all(all_prompts)

print(f"Created {len(all_prompts)} prompt(s) in {output_file}.")