import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
sys.path.append("")

json_out = []
CHARACTER_LIMIT = 50000


  ###Experiment


df = pd.read_csv("results_prereg_final_tidy.csv")
df_help = pd.read_csv("results_prereg_tidy_final_zScored_long.csv")

# general task instructions
task_instructions = (
    "Thank you for participating in this experiment!\n"
    "In the following, you will be presented with 16 short stories.\n"
    "Please read them very carefully, even if they appear to be repeated and you think that you remember them well enough.\n"
    "We ask you to rate statements about each short story.\n"
    "Please indicate, using an adjustable slider, how likely it is that a statement is true based on what you've read.\n"
    "Notice that there will also be simple attention checking trials.\n"
    "You will recognize them immediately when you read the important text on each trial carefully - those trials contain instructions for you to move the slider in a certain way.\n"
    "Please follow those instructions.\n"
    "The story is given at the top.\n"
    "The statement to be rated is given in a blue box below.\n"
    "On some trials, you will see an additional sentence in a pink box.\n"
    "Please read this sentence carefully before rating the statements in the boxes.\n\n"

)

#every trial instruction
instructions_trial= (
    "Please provide a rating of how likely it is that the statement is true, given the provided story.\n"
    "Story: {story}\n"
    "{crit_question}"
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
    # iterate over trials
    for _, trial in par_df.iterrows():
        # retrieve the response and the story
        response = trial["response"]
        story = trial["QUD"]

        #retrieve the additional information if available
        if isinstance(trial["critical_question"], str):
            crit_quest = trial["critical_question"]
        else:
            crit_quest = ""

        #retrive the prompt, the question, the condition, the reaction time and the trial number
        prompt = trial["prompt"]
        question = trial["question"]
        condition = trial["condition"]
        RT.append(trial["RT"])
        trial_number = trial["trial_number"]

        #adjust the question
        font_inx = question.find("</font>")
        new_question = question[15:font_inx]

        #adjust the prompt
        b_inx = prompt.find("</b>")
        prompt = prompt[3:b_inx]

        #adjust the additional information if available
        if crit_quest:
            b_inx = crit_quest.find("</b>")
            crit_quest = crit_quest[3:b_inx]
            crit_quest = "Sentence in the pink box: " + crit_quest+"\n"

        # add z-scores
        if condition == "critical":
            z_scores = df_help.loc[(df_help['submission_id'] == participant) & (df_help['trial_number'] == trial_number), 'response_centered']
            z_scored_rating.append(z_scores.iloc[0])
        else:
            z_scored_rating.append(None)

        #fill the parameters to the trial outputs
        trial_instuction = instructions_trial.format(
            story=story,
            crit_question=crit_quest,
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


