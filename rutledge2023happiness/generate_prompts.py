import scipy.io
import sys
sys.path.append("..")
from utils import randomized_choice_options
import math
import jsonlines

def get_location(x):
    if  (x >=0) and (x <= 7):
        loc = 'United Kingdom'
    elif (x >=100) and (x <= 309):
        loc = 'Other Europe'
    elif x == 400:
        loc = 'USA'
    elif (x >=401) and (x <= 509):
        loc = 'Other North or South America'
    elif (x >=600) and (x <= 909):
        loc = 'Africa, Asia, Pacific'
    else:
        loc = 'Unknown'
    return loc

def get_life_satisfaction(x):
    return x

def get_education(x):
    if x == 0:
        edu = 'School (GCSE or similar)'
    elif x == 1:
        edu = 'School (A-levels, vocational, or similar)'
    elif x == 2:
        edu = 'University degree'
    elif x == 3:
        edu = 'Advanced degree (MA, PhD, etc)'
    return edu

def get_native_language(x):
    if x == 0:
        lang = 'Arabic'
    elif x == 1:
        lang = 'English'
    elif x == 2:
        lang = 'French'
    elif x == 3:
        lang = 'German'
    elif x == 4:
        lang = 'Hindi'
    elif x == 5:
        lang = 'Mandarin'
    elif x == 6:
        lang = 'Portuguese'
    elif x == 7:
        lang = 'Punjabi'
    elif x == 8:
        lang = 'Spanish'
    else:
        lang = 'Other'
    return lang

def get_age(x):
    if x == 1:
        age = '18-24'
    elif x == 2:
        age = '25-29'
    elif x == 3:
        age = '30-39'
    elif x == 4:
        age = '40-49'
    elif x == 5:
        age = '50-59'
    elif x == 6:
        age = '60-69'
    elif x == 7:
        age = '70+'
    else:
        age = 'unknown'
    return age

mat = scipy.io.loadmat('data/Rutledge_risk_and_happiness_task_2023/Rutledge_GBE_risk_data_TOD.mat')

datasets = ['depData', 'subjData']

all_prompts = []
for dataset in datasets:
    #('id', 'age', 'isFemale', 'location', 'lifeSatisfaction', 'education', 'nativeLanguage', 'deviceType', 'nPlays', 'timesPlayed', 'dayNumber', 'timeOfDay', 'designVersion', 'dataHdr', 'data', 'depStatus', 'depEpisodes', 'depYears', 'depMeds', 'depFamily', 'bdiDayNumber', 'bdiRaw', 'bdiTotal')
    column_names = mat[dataset].dtype.names
    num_participants = len(mat[dataset][0])
    print(column_names)
    print(num_participants)

    for participant in range(num_participants):
        RTs = []
        choice_options = randomized_choice_options(num_choices=2)

        prompt = 'You are taking part in a game in which you have to repeatedly choose between two options.\n'\
            'You can select an option by pressing the corresponding key.\n'\
            'There is always one safe option with a guaranteed outcome and one risky option with two possible outcomes.\n'\
            'Your goal is to accumulate as many points as possible.\n'\
            'In between, you will be asked several times how happy you are right now.\n'\
            'Please answer this question with a number between 0 (very unhappy) and 100 (very happy).\n\n'

        participant_data = mat[dataset][0][participant]

        id = participant_data[0].item()
        age = get_age(participant_data[1].item())
        gender = 'female' if participant_data[2].item() else 'male'
        location = get_location(participant_data[3].item())
        life_satisfaction = get_life_satisfaction(participant_data[4].item())
        education = get_education(participant_data[5].item())
        native_language = get_native_language(participant_data[6].item())

        if dataset == 'depData':
            dep_status = 'depression' if (participant_data[15].item() <= 2) else ''
            bdi_total = participant_data[22].item()

        num_sessions = len(participant_data[14][0])
        for session in range(num_sessions):
            session_data = participant_data[14][0][session]

            prompt += 'New session.\n'
            prompt += 'How happy are you right now?\n'
            prompt += 'You answer <<' + str(session_data[0, 9]) + '>>.\n\n'
            RTs.append(session_data[0, 11] * 1000)

            for trial in range(session_data.shape[0]):
                certain_value = session_data[trial, 2]
                win_value = session_data[trial, 3]
                lose_value = session_data[trial, 4]
                c = int(session_data[trial, 6])
                reward = session_data[trial, 7]
                rt_choice = session_data[trial, 8] * 1000
                happiness = session_data[trial, 9]
                rt_happiness = session_data[trial, 11] * 1000

                '''
                array(['nTrial']
                array(['riskySide']
                array(['certainValue']
                array(['winValue']
                array(['loseValue']
                array(['empty']
                array(['choseRisky']
                array(['outcome']
                array(['choiceRT']
                array(['happiness']
                array(['startValue']
                array(['happinessRT']
                array(['empty']
                array(['spinDuration']
                array(['spinAngle']
                '''

                prompt += 'Option ' + choice_options[0] + ': ' + str(certain_value) + ' points with 100%.\n'
                prompt += 'Option ' + choice_options[1] + ': ' + str(win_value) + ' points with 50% or ' + str(lose_value) + ' points with 50%.\n'
                prompt += 'You press <<' + str(choice_options[c]) + '>> and get ' + str(reward) + ' points.\n\n'
                RTs.append(rt_choice)

                if (trial > 0) and not math.isnan(happiness):
                    prompt += 'How happy are you right now?\n'
                    prompt += 'You answer <<' + str(happiness) + '>>.\n\n'
                    RTs.append(rt_happiness)

        if dataset == 'depData':
            if dep_status == 'depression':
                all_prompts.append({'text': prompt,
                    'experiment': 'rutledge2023happiness/' + dataset,
                    'participant': str(id),
                    'RTs': RTs,
                    'age': str(age),
                    'gender': str(gender),
                    'location': str(location),
                    'life_satisfaction': str(life_satisfaction),
                    'education': str(education),
                    'native_language': str(native_language),
                    'diagnosis': str(dep_status),
                    'BDI-II score': str(bdi_total),
                })
            else:
                all_prompts.append({'text': prompt,
                    'experiment': 'rutledge2023happiness/' + dataset,
                    'participant': str(id),
                    'RTs': RTs,
                    'age': str(age),
                    'gender': str(gender),
                    'location': str(location),
                    'life_satisfaction': str(life_satisfaction),
                    'education': str(education),
                    'native_language': str(native_language),
                    'BDI-II score': str(bdi_total),
                })
        else:
            all_prompts.append({'text': prompt,
                'experiment': 'rutledge2023happiness/' + dataset,
                'participant': str(id),
                'RTs': RTs,
                'age': str(age),
                'gender': str(gender),
                'location': str(location),
                'life_satisfaction': str(life_satisfaction),
                'education': str(education),
                'native_language': str(native_language),
            })

with jsonlines.open('prompts.jsonl', 'w') as writer:
    writer.write_all(all_prompts)
