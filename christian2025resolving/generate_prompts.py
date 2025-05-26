import pandas as pd
from ast import literal_eval
import numpy as np

# Load both files
decisions = pd.read_csv('FeynmanStudyData.csv')
samples = pd.read_csv('FeynmanStudySamplesObserved.csv')

# Convert the 'Sample Data Observed' column from string representation of lists to actual lists
samples['Sample Data Observed'] = samples['Sample Data Observed'].apply(literal_eval)

# Change the name of the 'Subject' column in both DataFrames to 'Participant'
samples.rename(columns={'Subject': 'Participant'}, inplace=True)
decisions.rename(columns={'Subject': 'Participant'}, inplace=True)

for decision, sample in zip(decisions[decisions['Night'] == 0].iterrows(), samples.iterrows()):
    assert decision[1]['Participant'] == sample[1]['Participant'], f"Participant mismatch: {decision[1]['Participant']} vs {sample[1]['Participant']}"
    assert decision[1]['Total Nights'] == sample[1]['Total Nights'], f"Total Nights mismatch: {decision[1]['Total Nights']} vs {sample[1]['Total Nights']}"
    assert decision[1]['Distribution'] == sample[1]['Distribution'], f"Distribution mismatch: {decision[1]['Distribution']} vs {sample[1]['Distribution']}"
    assert decision[1]['clamp'] == sample[1]['clamp'], f"Clamp mismatch: {decision[1]['clamp']} vs {sample[1]['clamp']}"


# Identify any participants who made "mistakes" and flag them for removal from analysis.
# We will do this by checking for all rows in decisions with "Action" == "Mistake" and collecting their "Participant" id numbers.

mistakes = decisions[decisions['Action'] == 'Mistake']
mistake_participants = mistakes['Participant'].unique()
print(f"Participants with mistakes: {mistake_participants} ({len(mistake_participants)} total)")



# Identify participants who failed the quiz three or more times.

quiz_failures = decisions[decisions['quiz_failures'] >= 3]
quiz_failure_participants = quiz_failures['Participant'].unique()
print(f"Participants with quiz failures: {quiz_failure_participants} ({len(quiz_failure_participants)} total)")

# Identify specifically the participants who did not make mistakes but failed the quiz three or more times.
quiz_failures_no_mistakes = quiz_failures[~quiz_failures['Participant'].isin(mistake_participants)]
quiz_failure_no_mistakes_participants = quiz_failures_no_mistakes['Participant'].unique()
print(f"Participant with quiz failures but no mistakes: {quiz_failure_no_mistakes_participants} ({len(quiz_failure_no_mistakes_participants)} total)")




# Identify the participants who observed != 3 sets of samples.

wrong_number_of_sample_participants = []

# We need to do this by looping through the samples and checking the len() of the "Sample Data Observed" column.
# Iterate over the samples DataFrame
for index, row in samples.iterrows():
    # Check if the "Sample Data Observed" column is a list and its length is not equal to 3
    sample_data = row['Sample Data Observed']
    if len(sample_data) != 3:
        wrong_number_of_sample_participants.append(row['Participant'])
        print(f"Participant {row['Participant']} has {len(sample_data)} sets of samples.")



# The participant IDs that we want are the ones who did not make mistakes, did not fail the quiz three or more times, and have 3 sets of samples.
# We can do this by checking the intersection of the three sets of participants.

# Create a set of participants who did not make mistakes
no_mistakes_participants = set(decisions[~decisions['Participant'].isin(mistake_participants)]['Participant'].unique())
# Create a set of participants who did not fail the quiz three or more times
no_quiz_failures_participants = set(decisions[~decisions['Participant'].isin(quiz_failure_participants)]['Participant'].unique())
# Create a set of participants who have 3 sets of samples
three_samples_participants = set(samples[~samples['Participant'].isin(wrong_number_of_sample_participants)]['Participant'].unique())

# Find the intersection of the three sets
valid_participants = no_mistakes_participants.intersection(no_quiz_failures_participants).intersection(three_samples_participants)
print(f"Valid participants: {len(valid_participants)}")


def randomized_choice_options(num_choices):
    choice_options = list(map(chr, range(65, 91)))
    return np.random.choice(choice_options, num_choices, replace=False)

def initial_prompt(participant_samples):
    total_nights = participant_samples["Total Nights"]
    samples = list(participant_samples["Sample Data Observed"])

    bonus_threshold = (50 * total_nights)  # Average rating of 50 points
    bonus_rate = 0.002  # Number of $ per point over the bonus threshold
    bonus_cap = "{:.2f}".format(5.00)  # in USD. This is the maximum we will actually pay.

    def compute_bonus(points):
        bonus = max((points - bonus_threshold), 0) * bonus_rate
        bonus = min(bonus, float(bonus_cap))
        return "{:.2f}".format(bonus)

    text = f"""
# Instructions

Welcome! In this experiment we will ask you to make some simple decisions about restaurants.

You will receive a number of points for each decision. Your goal is to get as many points in total as you can.

You will receive a bonus based on your final total number of points.


# Restaurants in a New City

Imagine that you are going to be living for some period of time in a city in a foreign country.

Every restaurant in the city has a quality rating that is randomly distributed, with the average restaurant rating being 50. It is possible (though rare) that two restaurants could have the exact same rating.

Important: You don't learn the quality of a restaurant until you visit it for the first time! The restaurant's quality will not change, however, if you decide to revisit it.


# Deciding Where to Eat

Each night during your time in this city, you have a choice for where to go out to dinner.

You can decide to try a new restaurant (which will reveal its rating), or you can decide to go back any of the restaurants you've eaten at previously (which will always award the same number of points as before).

Please press ENTER key to continue.


# Number of Dinners and Bonus Payment

At the start of the experiment, we provide you a total of {total_nights} dinners. (The number of dinners remaining will be displayed.)

Your goal is to get as many total points as you can after eating all {total_nights} dinners.

You will receive a cash bonus after the completion of the experiment according to your final total score. Visiting restaurants at random will produce an average score of (50 points × {total_nights} dinners) = {bonus_threshold} points in total, so you will receive 1¢ for every {1/(bonus_rate * 100)} points over {bonus_threshold}. For instance, if your total is {70 * total_nights} points, you will receive ${compute_bonus(70 * total_nights)}. If your total is {90 * total_nights} points, you will receive ${compute_bonus(90 * total_nights)}.


# Sample Ratings

You will now see the sample ratings of the restaurants in three different nearby cities, to give you an idea of what sorts of ratings you can expect.

Here are the ratings from the restaurants in the first city:
{samples[0]}

Here are the ratings from the restaurants in the second city:
{samples[1]}

Here are the ratings from the restaurants in the third city:
{samples[2]}

Now the experiment will begin.


# Experiment

On each night, you will be asked to make a decision about where to eat. You can either choose to "Explore" (press {explore_button}) a new restaurant or "Exploit" (press {exploit_button}) by returning to the best of the restaurants you've already eaten at. You will be asked to make this decision for each of the {total_nights} dinners.
"""
    return text




def decision_prompt(participant_decision, total_rating):
    number_of_dinners_eaten = participant_decision["Night"]
    number_of_dinners_remaining = participant_decision["Total Nights"] - number_of_dinners_eaten
    night = participant_decision["Night"] + 1 # 1-indexed
    text = f"""
On night {night}, you have eaten {number_of_dinners_eaten} {"dinner" if number_of_dinners_eaten == 1 else "dinners"}, with a total score of {total_rating} {"point" if total_rating == 1 else "points"}. You have {number_of_dinners_remaining} {"dinner" if number_of_dinners_remaining == 1 else "dinners"} remaining. Do you want to eat at a new restaurant ("explore," press {explore_button}) or return to the highest-scoring restaurant you've already eaten at ("exploit," press {exploit_button})? You press <<{explore_button if participant_decision["Action"].lower() == 'explore' else exploit_button}>> and decide to {participant_decision["Action"].lower()}, receiving a score of {participant_decision["Reward"]} {"point" if participant_decision["Reward"] == 1 else "points"}.
"""
    return text


# For .jsonl export
import json

with open('prompts.jsonl', 'w') as f:
    for participant in valid_participants:
        participant_samples = samples[samples['Participant'] == participant]
        participant_decisions = decisions[decisions['Participant'] == participant]
        explore_button, exploit_button = randomized_choice_options(2)

        assert len(participant_samples) == 1, f"Expected one sample set for participant {participant}, found {len(participant_samples)}"
        participant_samples = participant_samples.iloc[0]

        assert len(participant_decisions) == participant_samples["Total Nights"], f"Expected {participant_samples['Total Nights']} decisions for participant {participant}, found {len(participant_decisions)}"

        text = initial_prompt(participant_samples)

        total_rating = 0
        for decision_row in participant_decisions.iterrows():
            text += decision_prompt(decision_row[1], total_rating)
            total_rating += decision_row[1]["Reward"]
        
        # return a JSON object with the participant ID and the text
        participant_json = {
            "text": text,
            "experiment": "christian2025resolving",
            "participant": str(participant),
            "nationality": "US",
        }
        f.write(json.dumps(participant_json) + '\n')




