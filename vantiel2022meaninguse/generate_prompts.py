import jsonlines
import pandas as pd
from tqdm import tqdm

json_out = []
CHARACTER_LIMIT = 32000

### Experiment 1: Verbal Probability Use
# This experiment corresponds to the "USE" study in the paper.
# Participants were presented with numeric probabilities and asked to describe them using verbal expressions (e.g., "likely", "unlikely").

# read a file
df = pd.read_csv("codedResults.csv")

# general task instructions
instructions = (
    "Thank you for participating in this experiment!\n"
    "In each trial, you will be presented with a display showing vases containing 100 randomlydistributed marbles which are either red or black.\n"
    "You will need to describe 25 randomly selected displays by freely completing the sentence frame:\n"
    "‘If you randomly take a marble from this vase,__ that it is red’.\n"
    "Please don't use numbers or percentages.\n\n"
)

# every trial instruction
trial_instruction = (
    "You see {probability} red marbles among 100 in total.\n"
    "Please describe the display by completing the sentence of the form:\n"
    "‘If you randomly take a marble from this vase,__ that it is red’.\n"
    "Your answer: If you randomly take a marble from this vase, <<{response}>> that it is red.\n"
)

# go over participants
for participant in tqdm(df.expId.unique()):
    # create a future json entry for the participant
    par_dict = {
        "text": instructions,
        "experiment": "vantiel2022meaninguse/exp1",
        "participant": str(participant)
    }

    # reindex and drop the old index
    par_df = df[df.expId == participant].reset_index(drop=True)

    # iterate over trials
    for _, row in par_df.iterrows():
        response = row["response"]
        probability = row["probability"]

        # fill the parameters to the trial outputs
        trial_text = trial_instruction.format(
            probability=probability,
            response=response
        )

        # append trial prompt to participant's recording
        par_dict["text"] += trial_text + "\n"

    # check that the prompt is not too long
    assert len(par_dict["text"]) < CHARACTER_LIMIT, f"Participant {participant} has too many characters."
    json_out.append(par_dict)


### Experiment 2: Numeric Probability Estimate
# This experiment corresponds to the "MEANING" study in the paper.
# Participants were given numeric probabilities and asked to assign a numerical estimate of likelihood.

# read a file
df = pd.read_csv("cleanedResults.csv")

# general task instructions
instructions = (
    "Thank you for participating in this experiment!\n"
    "In each trial, you will be presented with a display showing vases containing 100 randomlydistributed marbles which are either red or black.\n"
    "You will need to describe 25 randomly selected displays by moving a slider to indicate what percentage of the marbles you believe are red.\n"
    "Slider is initially set at 50%.\n\n"
)

# every trial instruction
trial_instruction = (
    "You see {probability} red marbles among 100 in total.\n"
    "Please move a slider to indicate what percentage of the marbles you believe are red.\n"
    "Your estimate: <<{estimate}>>\n"
)

# go over participants
for participant in tqdm(df.subject.unique()):
    # create a future json entry for the participant
    par_dict = {
        "text": instructions,
        "experiment": "vantiel2022meaninguse/exp2",
        "participant": str(participant)
    }

    # reindex and drop the old index
    par_df = df[df.subject == participant].reset_index(drop=True)

    # collect reaction times
    RTs = [int(rt) for rt in par_df["rt"]]

    # iterate over trials
    for _, row in par_df.iterrows():
        probability = row["probability"]
        estimate = row["estimate"]

        # fill the parameters to the trial outputs
        trial_text = trial_instruction.format(
            probability=probability,
            estimate=estimate
        )

        # append trial prompt to participant's recording
        par_dict["text"] += trial_text + "\n"

    # check that the prompt is not too long
    assert len(par_dict["text"]) < CHARACTER_LIMIT, f"Participant {participant} has too many characters."

    # append reaction times only for this experiment (since the other one doesn't have it)
    par_dict["RT"] = RTs
    json_out.append(par_dict)


# Save output to JSONL file
with jsonlines.open("prompts.jsonl", mode="w") as writer:
    writer.write_all(json_out)
