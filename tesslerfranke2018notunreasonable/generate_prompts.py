import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
sys.path.append("")

json_out = []
CHARACTER_LIMIT = 32000


   ###Experiment 1


df = pd.read_csv("Data/expt1-filtered.csv")

# general task instructions
task_instructions = (
    "Thank you for participating in this experiment!\n"
    "There will be 16 trials of the same task.\n"
    "In each task trial you will read a statement introducing a person.\n"
    "Your task is to rate the character on a scale introduced in the task by moving a slider.\n"
    "Try to be as accurate as possible.\n\n"
)

#every trial instruction
instructions_trial= (
    "Your friend tells you about their friend: {name}.\n"
    "\"{name} is {adjective}.\"\n"
    "Where would you place {name} on the scale from 0 to 1?\n"
    "Where 0 - the {low} person \n"
    "and 1 - the {high} person.\n"
    "Your answer: {response}.\n"
)

#go over participants
for participant in tqdm(df.workerid.unique()):
    # create a future json entry for the participant
    par_dict = {"text": task_instructions, "experiment": 'tesslerfranke_2018_not_unreasonable/exp1.csv', "participant": str(participant)}
    RT = []
    #reindex and drop the old index
    par_df = df[df.workerid == participant].reset_index(drop=True)
    # iterate over trials, construct interpretation and production instructions
    for _, trial in par_df.iterrows():
        # retrieve the endpoints of the scale, response, name, reaction time and the adjective under consideration
        response = trial["response"]
        name = trial["name"]
        high = trial["endpoint_high"]
        low = trial["endpoint_low"]
        adjective = trial["adjective"]
        RT.append(trial["rt"])

        #fill the parameters to the trial outputs
        trial_instuction = instructions_trial.format(
            name=name,
            high=high,
            low=low,
            adjective=adjective,
            response=f"<<{response}>>"
        )

        # append trial prompt to participant's recording
        par_dict["text"] += trial_instuction + "\n"

    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    # append reaction times
    par_dict["RTs"] = RT

    json_out.append(par_dict)






        ###Experiment 2

df = pd.read_csv("Data/expt2-filtered.csv")

# general task instructions A
task_instructions_1 = (
    "Thank you for participating in this experiment!\n"
    "There will be 12 trials of the same task.\n"
    "In each task trial you will read a statement introducing a person.\n"
    "Your task is to rate the character on a scale introduced in the task by moving a slider.\n"
    "Try to be as accurate as possible.\n\n"
)

# every trial instruction A
instructions_trial_1 = (
    "Your friend tells you about their friend: {name}.\n"
    "\"{name} is {adjective}.\"\n"
    "Where would you place {name} on the scale from 0 to 1?\n"
    "Where 0 - {low} person in the world\n"
    "and 1 - {high} person in the world.\n"
    "Your answer: {response}.\n"
)

# general task instructions B
task_instructions_2 = (
    "Thank you for participating in this experiment!\n"
    "There will be 12 trials of the same task.\n"
    "In each task trial you will read statements introducing 4 people.\n"
    "Your task is to rate the characters on a scale introduced in the task by moving a slider.\n"
    "Try to be as accurate as possible.\n\n"
)

# every trial instruction B
instructions_trial_2 = (
    "Your friend tells you about four friends of theirs.\n"
    "For each of them, where would you place them on the following scale?\n"
    "Where 0 - {low} person in the world\n"
    "and 1 - {high} person in the world.\n"
)

# for each of the people
person_trial_2 = (
    "\"{name} is {adjective}.\"\n"
    "Your answer: {response}.\n"
)

#go over participants
for participant in tqdm(df.workerid.unique()):
    # create a future json entry for the participant depending ob the experiment
    if participant < 600:
        par_dict = {"text": task_instructions_1, "experiment": 'tesslerfranke_2018_not_unreasonable/exp2.csv', "participant": str(participant)}
    else:
        par_dict = {"text": task_instructions_2, "experiment": 'tesslerfranke_2018_not_unreasonable/exp2.csv', "participant": str(participant)}
        mark=0
    RT = []
    #reindex and drop the old index
    par_df = df[df.workerid == participant].reset_index(drop=True)
    # iterate over trials, construct interpretation and production instructions
    for _, trial in par_df.iterrows():
        # for single utterance
        if participant < 600:
            # retrieve the endpoints of the scale
            high_br = trial["endpoint_high"]
            idx_high_br = high_br.find("<br>")
            high = high_br[:idx_high_br]
            low_br = trial["endpoint_low"]
            idx_low_br = low_br.find("<br>")
            low = low_br[:idx_low_br]
            # retrieve the reaction time, response, name and adjective under consideration
            RT.append(trial["rt"])
            response = trial["response"]
            name = trial["name"]
            adjective = trial["adjective"]

            #fill the parameters to the trial outputs
            trial_instruction_1 = instructions_trial_1.format(
                name=name,
                high=high,
                low=low,
                adjective=adjective,
                response=f"<<{response}>>"
            )
            # append trial prompt to participant's recording
            par_dict["text"] += trial_instruction_1 + "\n"
        # if it is a first iteration for the participant in multiple utterances
        elif mark==0:
            # retrieve the endpoints of the scale
            high_br = trial["endpoint_high"]
            idx_high_br = high_br.find("<br>")
            high = high_br[:idx_high_br]
            low_br = trial["endpoint_low"]
            idx_low_br = low_br.find("<br>")
            low = low_br[:idx_low_br]
            # retrieve the reaction time, response, name and adjective under consideration
            RT.append(trial["rt"])
            response = trial["response"]
            name = trial["name"]
            adjective = trial["adjective"]
            # fill the parameters to the trial outputs
            trial_instruction_2 = instructions_trial_2.format(
                high=high,
                low=low
            )
            # fill the parameters for the first person
            trial_person_2 = person_trial_2.format(
                name=name,
                adjective=adjective,
                response=f"<<{response}>>"
            )
            # append trial prompt to participant's recording
            par_dict["text"] += trial_instruction_2 + trial_person_2
            # go to the next iteration
            mark+=1
        # if it is a multiple utterances experiment but the iteration is not first
        else:
            # retrieve the response, name and adjective under consideration
            response = trial["response"]
            name = trial["name"]
            adjective = trial["adjective"]
            # fill the parameters for the (markth*) person
            trial_person_2 = person_trial_2.format(
                name=name,
                adjective=adjective,
                response=f"<<{response}>>"
            )
            # append trial prompt to participant's recording
            par_dict["text"] += trial_person_2
            # if fourth iteration drop mark to 0
            if mark == 3:
                mark = 0
                par_dict["text"] += "\n"
            # otherwise iterate inside this task
            else:
                mark += 1


    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    # append reaction times
    par_dict["RTs"] = RT

    json_out.append(par_dict)




# Save output to JSONL file
with jsonlines.open("prompts.jsonl", "w") as writer:
    writer.write_all(json_out)

