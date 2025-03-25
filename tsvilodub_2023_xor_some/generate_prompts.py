import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
sys.path.append("")

json_out = []
CHARACTER_LIMIT = 32000

  ###Experiment 1


df = pd.read_csv("results_73_xor-some-Prolific-main_N275_anonym.csv")

# general task instructions
task_instructions = (
    "Thank you for participating in this experiment!\n"
    "First you will be exposed to 4 example trials of the task.\n"
    "Then you will have 76 trials without the instructions.\n"
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
    par_dict = {"text": task_instructions, "experiment": 'tsvilodub_2023_xor_some', "participant": str(participant)}
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

        if condition == "example":
            story = story[7:]

            font_inx = question.find("</font>")
            new_question = question[16:font_inx]
            start_ind = question.find("8B0000\">")
            end_inx = question.find("</i>")
            new_question+="\n"+question[(start_ind+8):end_inx]
        else:
            font_inx = question.find("</font>")
            new_question = question[15:font_inx]

            b_inx = prompt.find("</b>")
            prompt = prompt[3:b_inx]

            if crit_quest:
                b_inx = crit_quest.find("</b>")
                crit_quest = crit_quest[3:b_inx]
        story+=" " + crit_quest

        #fill the parameters to the trial outputs
        trial_instuction = instructions_trial.format(
            story=story,
            sentence = prompt,
            question = new_question,
            response=f"<<{response}>>"
        )

        # append trial prompt to participant's recording
        par_dict["text"] += trial_instuction + "\n"

    """# check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"""
    # append reaction times
    par_dict["RTs"] = RT

    json_out.append(par_dict)




# Save output to JSONL file
with jsonlines.open("prompts.jsonl", "w") as writer:
    writer.write_all(json_out)


