import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
sys.path.append("")

json_out = []
CHARACTER_LIMIT = 32000

  ###Experiment


df = pd.read_csv("results_prereg_final_tidy.csv")
df_help = pd.read_csv("results_prereg_tidy_final_zScored_long.csv")

# general task instructions
task_instructions = (
    "Thank you for participating in this experiment!\n"
    "You will have 76 trials of the same task.\n"
    "Some of them will be attention checkers where you will be explicitly informed what to do.\n"
    "In each trial you will read a short story and see a sentence in the blue box.\n"
    "Then you will need to answer the question by adjusting the slider on the scale from 0 to 100, \n"
    "Where 0 means that the sentence in the box is certainly false and 100 - certainly true.\n"
    "Try to be as accurate as possible.\n\n"
)

#every trial instruction
instructions_trial= (
    "Story: {story}\n"
    "Sentence in the blue box: \"{sentence}\"\n"
    "{question}\n"
    "Your answer: {response}.\n"
)

#go over participants
for participant in tqdm(df.submission_id.unique()):
    # create a future json entry for the participant
    par_dict = {"text": task_instructions, "experiment": 'tsvilodub-2023xorsome', "participant": str(participant)}
    z_scored_rating =[]
    RT = []
    #reindex and drop the old index
    par_df = df[df.submission_id == participant].reset_index(drop=True)
    # iterate over trials, construct interpretation and production instructions
    for _, trial in par_df.iterrows():
        # retrieve the endpoints of the scale, response, name, reaction time and the adjective under consideration
        response = trial["response"]
        story = trial["QUD"]
        if isinstance(trial["critical_question"], str):
            crit_quest = trial["critical_question"]
        else:
            crit_quest = ""

        prompt = trial["prompt"]
        question = trial["question"]
        condition = trial["condition"]
        RT.append(trial["RT"])
        trial_number = trial["trial_number"]

        font_inx = question.find("</font>")
        new_question = question[15:font_inx]

        b_inx = prompt.find("</b>")
        prompt = prompt[3:b_inx]

        if crit_quest:
            b_inx = crit_quest.find("</b>")
            crit_quest = crit_quest[3:b_inx]

        story+=" " + crit_quest

        if condition == "critical":
            z_scores = df_help.loc[(df_help['submission_id'] == participant) & (df_help['trial_number'] == trial_number), 'response_centered']
            z_scored_rating.append(z_scores.iloc[0])
        else:
            z_scored_rating.append(0)

        #fill the parameters to the trial outputs
        trial_instuction = instructions_trial.format(
            story=story,
            sentence = prompt,
            question = new_question,
            response=f"<<{response}>>"
        )

        # append trial prompt to participant's recording
        par_dict["text"] += trial_instuction + "\n"

    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"
    # append reaction times and z scores
    par_dict["RTs"] = RT
    par_dict["z_scored_ratings"] = z_scored_rating

    json_out.append(par_dict)




# Save output to JSONL file
with jsonlines.open("prompts.jsonl", "w") as writer:
    writer.write_all(json_out)


