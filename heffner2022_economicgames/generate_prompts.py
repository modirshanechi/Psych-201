import pandas as pd
import jsonlines
import os

# Link to data hosted on GitHub
path = 'https://raw.githubusercontent.com/jpheffne/NC_emotion_classify/refs/heads/main/data/behavioral/'

datasets = ["ug_data.csv", "pd_data.csv", "pgg_data.csv"]


# prisoner's dilemma
prd = pd.read_csv('https://raw.githubusercontent.com/jpheffne/NC_emotion_classify/refs/heads/main/data/behavioral/pd_data.csv')
# public goods game
pgg = pd.read_csv('https://raw.githubusercontent.com/jpheffne/NC_emotion_classify/refs/heads/main/data/behavioral/pgg_data.csv')


ulg = pd.read_csv('https://raw.githubusercontent.com/jpheffne/NC_emotion_classify/refs/heads/main/data/behavioral/ug_data.csv')




################
# Ultimatum game
################

# Instructions for LLM
instructions = """You will be making real decisions that affect the monetary outcomes of YOURSELF and OTHERS.
 
You will be playing multiple rounds of a game with DIFFERENT partners every round. 

Your partner has been allotted $1.00. You will be paired with a different partner each round and your partner has already decided how much of their $1 to offer you. 

IMPORTANT: Your partner can split their $1 in any amount as long as it is in $0.05 increments. 

After observing your partner make an offer, you will be asked to determine the final monetary outcome of both your partner and yourself. These options are labeled below: 
 
Accept: Agree to the proposed offer and keep both you and your partner's money the same. 

Reject: Reject the offer and decrease both you and your partner's money to zero. 

Ultimately, you will decide how much money you and your partner actually receive.


"""

# Load data
ulg = pd.read_csv(path + "ug_data.csv")

# Initialize list to store prompts
all_prompts = []

# Get participant IDs
participant_ids = ulg["sub"].unique()

# Iterate over participants
for participant_id in participant_ids:

    # Get participant's choice and reshuffle
    choices = (
        ulg[ulg["sub"] == participant_id]
        .sample(frac=1, random_state=42)
        .reset_index(drop=True)
    )


    choices_as_text = ""

    # Iterate over participants' choices
    for _, row in choices.iterrows():

        decision = "accept" if row["choice"] == 0 else "reject"

        # Offer from partner ranges from $0.5 (fair) to $0.95 (unfair)
        keep = str(round(1 - row["unfairness"], 2))
        offer =  str(row["unfairness"])

        # Construct prompt for LLM
        choices_as_text += "Your partner keeps $"+keep+" and gives you $"+offer+". You chose to <<"+decision+">> the offer.\n"

    # Append prompt to list
    all_prompts.append({
        'text': instructions + choices_as_text, 
        'experiment': 'heffner2022economicgames/', 
        'participant': str(participant_id),
    })

# Get the absolute path of this Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the prompts.jsonl file in the same directory
filename = os.path.join(script_dir, 'prompts.jsonl')

# Write json file
with jsonlines.open(filename, 'w') as writer:
    writer.write_all(all_prompts)