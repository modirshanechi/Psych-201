import random
import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
from utils import randomized_choice_options
sys.path.append("..")

json_out = []
CHARACTER_LIMIT = 120000

#Datasets

df1 = pd.read_csv("Data/Human_Deceits.csv")
df2 = pd.read_csv("Data/Deceits_prompts_seed0_examples0.csv")
df3 = pd.read_csv("Data/Human_Maxims.csv")
df4 = pd.read_csv("Data/Maxims_prompts_seed0_examples0.csv")
df5 = pd.read_csv("Data/Human_Humour.csv")
df6 = pd.read_csv("Data/Humour_prompts_seed0_examples0.csv")
df7 = pd.read_csv("Data/Human_CoherenceInference.csv")
df8 = pd.read_csv("Data/CoherenceInference_prompts_seed0_examples0.csv")
df9 = pd.read_csv("Data/Human_IndirectSpeech.csv")
df10 = pd.read_csv("Data/IndirectSpeech_prompts_seed0_examples0.csv")
df11 = pd.read_csv("Data/Human_Metaphor.csv")
df12 = pd.read_csv("Data/Metaphor_prompts_seed0_examples0.csv")
df13 = pd.read_csv("Data/Human_Irony.csv")
df14 = pd.read_csv("Data/Irony_prompts_seed0_examples0.csv")

# general task instructions
task = (
    "{text} {response}\n\n"
)
#go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics', "participant": str(participant)}
    # Correctness list
    correct_list = []

    ###Deceits

    #reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        #get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"]-1, "randomized_option_order"])
        #get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        #get the instructions
        text = df2.loc[trial["itemNum"]-1, "prompt"]

        #options finding
        one_idx=text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options=[text[(one_idx+3):two_idx], text[(two_idx+3):three_idx], text[(three_idx+3):four_idx], text[(four_idx+3):answer_idx]]

        #get the actual response
        response = options[response_idx]

        #shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)


        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4
        ) = randomized_choice_options(4)
        obj_list = [obj_1, obj_2, obj_3, obj_4]

        #replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        #get the new prompt
        new_text = text[:one_idx]+obj_1+": "+options[0]+obj_2+": "+options[1]+obj_3+": "+options[2]+obj_4+": "+options[3]+"Answer:"

        #fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        correct_list.append(trial["Correct"])



    ###Maxims

    # reindex and drop the old index
    par_df = df3[df3.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])

        #omit the discrepancy (no prompt number 13) in data
        itemNum = trial["itemNum"]
        if itemNum < 13:
            index = itemNum - 1
        elif itemNum > 13:
            index = itemNum - 2
        else:
            continue

        #get the list of how answers were scrumbled
        scrumbled_list = eval(df4.loc[index, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df4.loc[index, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4
        ) = randomized_choice_options(4)
        obj_list = [obj_1, obj_2, obj_3, obj_4]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + obj_3 + ": " + options[
            2] + obj_4 + ": " + options[3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        #add correctness
        correct_list.append(trial["Correct"])



    ###Humour

    # reindex and drop the old index
    par_df = df5[df5.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])

        # get the list of how answers were scrumbled
        scrumbled_list = eval(df6.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df6.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        five_idx = text.find("5)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):five_idx], text[(five_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4,
            obj_5
        ) = randomized_choice_options(5)
        obj_list = [obj_1, obj_2, obj_3, obj_4, obj_5]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)
        text = text.replace("5", obj_5, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + obj_3 + ": " + options[
            2] + obj_4 + ": " + options[3] + obj_5 + ": " + options[4] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        # append correctness
        correct_list.append(trial["Correct"])


    ###Coherence

    # reindex and drop the old index
    par_df = df7[df7.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the response Coherent|Incoherent
        coherent_response = trial["OptionChosen"]

        # covert "Coherent" to 1 and "Incoherent" to 2
        if coherent_response == "Coherent":
            index = 1
        else:
            index = 2

        # get the list of how answers were scrumbled
        scrumbled_list = eval(df8.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(index)
        # get the instructions
        text = df8.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2
        ) = randomized_choice_options(2)
        obj_list = [obj_1, obj_2]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    ###Indirect Speech

    # reindex and drop the old index
    par_df = df9[df9.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df10.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df10.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4
        ) = randomized_choice_options(4)
        obj_list = [obj_1, obj_2, obj_3, obj_4]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + obj_3 + ": " + options[
            2] + obj_4 + ": " + options[3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    ###Metaphor

    # reindex and drop the old index
    par_df = df11[df11.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df12.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df12.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        five_idx = text.find("5)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):five_idx], text[(five_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4,
            obj_5
        ) = randomized_choice_options(5)
        obj_list = [obj_1, obj_2, obj_3, obj_4, obj_5]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)
        text = text.replace("5", obj_5, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + obj_3 + ": " + options[
            2] + obj_4 + ": " + options[3] + obj_5 + ": " + options[4] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    ###Irony

    # reindex and drop the old index
    par_df = df13[df13.pKey == participant].reset_index(drop=True)
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df14.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df14.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # new response index
        new_resp_idx = options.index(response)

        # generate by-participant randomization of keys that correspond to the forced-choice options
        (
            obj_1,
            obj_2,
            obj_3,
            obj_4
        ) = randomized_choice_options(4)
        obj_list = [obj_1, obj_2, obj_3, obj_4]

        # replace digits with letters in the task instructions
        text = text.replace("1", obj_1, 1)
        text = text.replace("2", obj_2, 1)
        text = text.replace("3", obj_3, 1)
        text = text.replace("4", obj_4, 1)

        # response in the prompt:
        resp_prompt = obj_list[new_resp_idx]

        # get the new prompt
        new_text = text[:one_idx] + obj_1 + ": " + options[0] + obj_2 + ": " + options[1] + obj_3 + ": " + options[
            2] + obj_4 + ": " + options[3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    #append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)



#write to the jsonl file
with jsonlines.open("prompts.jsonl", "w") as writer:
    writer.write_all(json_out)




