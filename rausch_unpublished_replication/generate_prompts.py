# Prepare the Rrausch_unpublished_replication dataset for Psych201
# Manuel Rausch 30.03.2025, manuel.rausch@ku.de

import pandas as pd
import jsonlines
import os

os.chdir('C:/Users/mru/KU2/Projekte/Psych-201')
dataset = 'ReplicationOfHoogeveenEtalByRausch.csv'
all_prompts = []


df = pd.read_csv(dataset)
participants = df['SbjID'].unique()
#df.Authors.unique()
for participant in participants:
    #participant = participants[0]
    print(participant)
    
    prompt = 'Thank you for agreeing to take part in this study!\n'
    prompt += 'You will be shown brief summaries of psychological studies.\n'
    prompt += 'Your task is to evaluate whether you think each study is replicable — that is, whether repeating the experiment would likely lead to the same results.\n'
    prompt += 'After making your judgment, you’ll also be asked how confident you are in your decision.\n'
    prompt += 'If a study summary is unclear or you do not understand it, you can check a box to skip it.'
    
    df_participant = df[df['SbjID'] == participant]
    num_trials = len(df_participant)
    # s
    
    for trial in range(num_trials):
        # Get the values for this trial
        Authors = df_participant.Authors.iloc[trial]
        correct = df_participant.correct.iloc[trial]
        replicated = df_participant.Replicated.iloc[trial]
        confidence = df_participant.confidence.iloc[trial]
        
        if Authors == 'Alter, Oppenheimer, Epley, and Eyre (2007)':
            prompt += "\n\nDo people’s logic skills improve if the concept of analytic thinking is active in their minds?\n"
            prompt += "Participants solved difficult logic problems. In one group, the logic problems were printed in a font that was hard to read (activating the analytical mindset). In the other group, the logic problems were printed in a font that was easy to read.\n"
            prompt += "If the logic problems were printed in a font that was hard to read, participants solved more of the logic problems correctly."
        elif Authors == 'Anderson, Kraus, Galinsky, and Keltner (2012)':
            prompt += "\n\nDo social comparisons influence people’s well-being?\n"
            prompt += "Participants read a description of a person and were instructed to think about similarities and differences between them. In one group, the person was described as respected and liked by all their social groups. In the other group, the person was described as not respected and liked in any of their social groups. Afterwards, participants answered questions about their well-being.\n" 
            prompt += "If participants compared themselves with a highly respected and liked person, participants reported lower well-being."
        elif Authors == 'Aviezer, Trope, and Todorov (2012)':
            prompt += "\n\nCan people distinguish between positive and negative emotions based on the body alone?\n" 
            prompt += "Participants looked at images of athletes that either just scored or just lost a point in a competition. Without seeing any facial expressions, they then judged whether the image depicted a positive or negative emotion.\n"
            prompt += "Participants correctly recognized the underlying emotions based on the image of the body alone. That is, they rated the images of winning athletes as more positive then the images of losing athletes."
        elif Authors == 'Balafoutas and Sutter (2012)':
            prompt += "\n\nDoes preferential treatment encourage women to enter competition with others?\n"
            prompt += "In a game, male and female participants chose whether they wanted to compete against each other, or whether they wanted to get judged based on their individual performance. In one group, women received a preferential treatment if they entered the competition, that is, one point was automatically added to their score. In the other group, women did not receive a preferential treatment.\n"
            prompt += "If women received a preferential treatment, then they would choose to enter a competition with others more often."
        elif Authors == 'Bauer, Wilkie, Kim, and Bodenhausen (2012)':
            prompt += "\n\nDo people with a “materialism mindset” trust others less?\n"
            prompt += "Participants read a dilemma about distributing resources related to water conservation. In one group, other parties involved in the water conservation problem were referred to as “consumers”. In the other group, these parties were referred to as 'individuals'. Afterwards, participants had to report their trust towards the other parties involved in the water conservation problem.\n"
            prompt += "If other parties involved in the water conservation problem were referred to as ‘consumers’, participants trusted these parties less."
        elif Authors == 'Critcher and Gilovich (2008)':
            prompt += "\n\nAre people’s estimations of numbers influenced by unrelated numbers that are incidentally present in the environment?\n"
            prompt += "Participants read a description about a new cell phone. In one group, the cell phone was called P17. In the other group, the cell phone was called P97. Afterwards, participants predicted its proportion of sales.\n"
            prompt += "If the cell phone was called P97, participants predicted a higher proportion of sales."
        elif Authors == 'Derex, Beugin, Godelle, and Raymond (2013)':
            prompt += "\n\nAre bigger groups characterized by more cultural diversity?\n"
            prompt += "A computer game was set up to be a multiplayer game, consisting of either 2, 4, 8, or 16 players. In this game the players had to collect points by either building arrowheads (a simple task), or building fishing nets (a difficult task).\n"
            prompt += "The more players were playing the game, the more likely it was that they increased the cultural diversity within the game (i.e., by building both items)."
        elif Authors == 'Duncan, Sadanand, and Davachi (2012)':
            prompt += "\n\nDoes the detection of new objects improve people’s ability to detect subtle changes in similar objects?\n"
            prompt += "Participants looked at a series of object images. Afterwards, they had to look again at a series of objects and judged whether they were ‘old’ (seen before), ‘new’, or ‘similar’ (looked like something seen before, but not the same).\n" 
            prompt += "If ‘new’ objects were shown before ‘similar’ objects, then more participants recognized the ‘similar’ objects correctly."
        elif Authors == 'Gervais and Norenzayan (2012)':
            prompt += "\n\nDoes analytic thinking trigger religious disbelief?\n"
            prompt += "Participants looked at an image. One group looked at an image of “The Thinker”, that is a sculpture of a person in a thinking position. The other group looked at an image which depicted a sculpture of a discus thrower. Afterwards, they answered questions about their religiosity.\n"
            prompt += "Participants who had seen “The Thinker” reported lower religious belief compared to people who had seen the sculpture of a discus thrower."
        elif Authors == 'Giessner and Schubert (2007)':
            prompt += "\n\nIs perceived power related to the vertical location of a person?\n"
            prompt += "Participants studied a schematic display of the hierarchy within an organization, including a manager and his team. In one group, the vertical line connecting the manager to the team was long (i.e., 7 cm). In the other group, the vertical line was short (i.e., 2 cm). Afterwards, participants estimated how much power they thought the manager held within the organization.\n"
            prompt += "If the vertical line connecting the manager to the team was long, participants estimated that the manager held more power within the organization."
        elif Authors == 'Gneezy, Keenan, and Gneezy (2014)':
            prompt += "\n\nDo people avoid charities that dedicate a high percentage of donations to administrative and fundraising costs?\n"
            prompt += "People chose between donating to either a drinking water charity, or a volunteering charity. One group was told that 50% of the donations to the water charity were used to cover administrative and fundraising costs. The other group was told that all costs for the water charity were already covered. If administrative and fundraising costs were covered, people were more likely to donate to the water charity than to the volunteering charity, compared to when the costs were not covered.\n"
            prompt += "If administrative and fundraising costs were covered, people were more likely to donate to the water charity than to the volunteering charity, compared to when the costs were not covered."
        elif Authors == 'Hauser, Rand, Peysakhovich, and Nowak (2014)':
            prompt += "\n\nDo people preserve common resources for future generations if they make collective decisions?\n"
            prompt += "In a game, participants chose how many resources they would extract from a pool, and how many they wanted to preserve for future game players. In one group, each participant made their own decision on how many resources they want to extract from the pool. In the other group, participants voted for the combined amount of resources they would extract.\n"
            prompt += "If people had to vote on the combined amount of resources they would extract from the pool, more resources were preserved for future generations of game players."
        elif Authors == 'Karpicke and Blunt (2011)':
            prompt += "\n\nIs the learning strategy ‘retrieval practice’ more efficient than the learning strategy ‘concept maping’?\n"
            prompt += "Participants studied a science text using a certain learning strategy. In one group, participants used the learning strategy ‘retrieval practice’, which consists of learning - testing - learning. In the other group, participants used the learning strategy ‘concept-mapping’, in which participants create a diagram with nodes and links to connect different concepts. One week later participants weretested on this text.\n"
            prompt += "If participants used the learning strategy ‘retrieval practice’, they performed better on a memory test."
        elif Authors == 'Kidd and Castano (2013)':
            prompt += "\n\nCan reading literary fiction improve people’s understanding of other people’s emotions?\n"
            prompt += "Participants read a short text passage. In one group, the text passage was literary fiction. In the other group, the text passage was non-fiction. Afterwards, participants had to identify people’s expressed emotion (e.g., happy, angry) based onnimages of the eyes only.\n" 
            prompt += "Participants were better at recognizing the correct emotion after reading literary fiction."
        elif Authors == 'Kovacs, Téglás, and Endress (2010)':
            prompt += "\n\nDo beliefs of others influence people’s actions, even if these beliefs are irrelevant?\n"
            prompt += "Participants watched a short cartoon. In the cartoon, a character places a ball behind a box, which then rolls away. Then, the character lifts the box and reveals the ball, which returned unexpectedly. Participants were instructed to press a button as soon as they detected the ball. In one group, the character saw the ball rolling away. In the other group, the character did not see the ball rolling away.\n"
            prompt += "If the character believed that the ball was behind the box, participants detected the ball faster."
        elif Authors == 'Lee and Schwarz (2010)':
            prompt += "\n\nDoes washing hands weaken people’s urge to justify their choice for a non-preferred item?\n"
            prompt += "Participants ranked 10 CDs based on how much they would like to own them. Then, the participants could choose to keep their 5th or 6th choice. After the choice, participants were asked to evaluate a soap and then to rank the CDs again. In one group, participants evaluated the soap after they washed their hands with it. In the other group, participants evaluated the soap without washing their hands with it.\n"
            prompt += "If participants evaluated the soap without washing their hands with it, they increased their preference for their chosen CD."
        elif Authors == 'Morewedge, Huh, and Vosgerau (2010)':
            prompt += "\n\nDo people want to eat less food, after they repeatedly imagined eating it?\n"
            prompt += "Participants had to imagine 33 repetitive actions, one at a time. In one group, participants imagined eating 30 M&Ms and then inserting 3 coins in a laundry machine. In the other group, participants imagined inserting 33 coins in a laundry machine. Afterwards, participants could eat from a bowl containing M&Ms.\n"
            prompt += "If participants imagined eating 30 M&Ms, they ate fewer M&Ms from the bowl."
        elif Authors == 'Nishi, Shirado, Rand, and Christakis (2015)':
            prompt += "\n\nAre groups less likely to reduce inequality if the group members know the wealth of each other?\n"
            prompt += "In a game, participants could share resources with co-players or keep it to themselves. At the start of the game, the resources were distributed unevenly between the players. In one group, participants saw the amount of resources of other players. In the other group, participants only saw their own resources.\n" 
            prompt += "If participants knew the amount of resources from other players, the inequality between the players remained higher."
        elif Authors == 'Pyc and Rawson (2010)':
            prompt += "\n\nWhen learning new words, does taking a test help people to remember links between the words and their meaning?\n"
            prompt += "Participants learned 48 Swahili words by writing down links between each Swahili word and its meaning. In one group, the learning strategy of the participants involved learning - testing - learning. In the other group, the learning strategy of the participants involved learning - relearning, without testing. One week later, participants did a memory test in which they got the instruction to write down the meaning of the Swahili word, and their self-generated link between theword and its meaning.\n"
            prompt += "If participants used a learning strategy that involved learning - testing - learning, they remembered more of their self-generated links between the words and their meaning."
        elif Authors == 'Risen and Gilovich (2008)':
            prompt += "\n\nDo people belief that tempting fate leads to negative consequences?\n"
            prompt += "Participants imagined a scenario in which they would come to a lecture in which the professor picks out one student to answer a difficult question in front of the entire class. In one group, participants imagined that they tempted fate by coming to the lecture unprepared. In the other group, participants imagined that they came to the lecture prepared. Afterwards, participants had to estimate how likely it was that they would get chosen.\n" 
            prompt += "If participants imagined that they tempted fate, they thought it was more likely that they would get chosen by the professor to answer a difficult question in front of the entire class."
        elif Authors == 'Shah, Mullainathan, and Shafir (2012)': 
            prompt += "\n\nDoes poverty drain people’s attention?\n"
            prompt += "Participants played the game 'Wheel ofFortune', a game in which people have to guess letters in word puzzles. In one group, participants were given 6 chances per round to guess letters (i.e., ‘poor’ players). In the other group, participants were given 20 chances per round to guess letters (i.e., ‘rich’ players). Afterwards, they completed an attention task.\n"
            prompt += "If participants were given few chances per round to guess letters, they performed worse in the subsequent attention task."
        elif Authors == 'Shafir (1993)':
            prompt += "\n\nDo people find positive characteristics more important in decisions in which they are awarding something, and find negative characteristics more important in decisions in which they are denying something?\n"
            prompt += "Participants imagined that they were members of a jury, who had to decide which parent would obtain custody for a child. One parent was described as having average features concerning, for instance, income, work-related absence, and relationship to the child. The other parent had both extreme positive characteristics (e.g., very close relationship to the child), but also extreme negative characteristics (e.g., much work-related absence). In one group, participants were asked to which parent they would award custody for the child. In the other group, participants were asked to which parent they would deny custody for the child.\n"
            prompt += "In both groups, participants selected the extreme parent more often than the average parent."
        elif Authors == 'Sparrow, Liu, and Wegner (2011)':
            prompt += "\n\nDo difficult questions activate the concepts of 'Google' and computers in people’s minds?\n"
            prompt += "Participants answered knowledge questions. In one group, participants answered difficult questions. In the other group, participants answered easy questions. Afterwards, they performed a reaction time task where they had to ignore computer-related words that were presented on the screen.\n"
            prompt += "If participants answered difficult questions, their reaction times were slower when computer-related words were present on the screen (which indicates that the concept of computers was active in their minds)."
        elif Authors == 'Tversky and Gati (1978)':
            prompt += "\n\nAre people’s judgements of how similar two concepts are influenced by the order in which they were mentioned?\n" 
            prompt += "Participants rated how similar two countries were to each other (e.g., “How similar is the USA to Lebanon?”). One of the countries was well-known to the participants (e.g., the USA). The other country was less familiar to the participants (e.g., Lebanon). In one group, the well-known country was mentioned first. In the other group, the less known country was mentioned first.\n"
            prompt += "If he well-known country was mentioned first, participants judged the two countries as less similar."
        elif Authors == 'Wilson et al. (2014)':
            prompt += "\n\nDo people enjoy doing nothing?\n"
            prompt += "Participants spent a short amount of time by themselves in an empty room. In one group, participants were instructed to spend their time on a non-social activity (e.g., listening to music, reading a book, surfing the Web). In the other group, participants were instructed to entertain themselves with their thoughts (without any external activity). Afterwards participants answered questions about how enjoyable this experience was.\n"
            prompt += "If participants had just their thoughts to entertain themselves, they enjoyed themselves less." 
        elif Authors == 'Zaval, Keenan, Johnson, and Weber (2014)':
            prompt += "\n\nDo people’s concerns about global warming change when the concept of heat or cold is active in their minds?\n" 
            prompt += "Participants performed a task in which they had to unscramble sentences. In one group, participants read sentences that contained words related to hot temperatures. In the other group, people read sentences that contained words related to cold temperatures. Afterwards, participants reported the degree in which they were concerned about global warming.\n"
            prompt += "If participants read sentences that contained words related to hot temperatures, participants were more concerned about global warming."
        elif Authors == 'Zhong and Liljenquist (2006)':
            prompt += "\n\nDoes feeling morally dirty increase people’s need to wash themselves?\n"
            prompt +=  "Participants hand copied a story written in the first person. In one group, participants rewrote an unethical short story about sabotaging a co-worker. In the other group, participants rewrote an ethical short story about helping a co-worker. Afterwards, participants expressed their desire for cleaning products (e.g., soap, toothpaste).\n"
            prompt +=  "If participants rewrote an unethical story, they had a higher desire for cleansing products."
         
        prompt += '\nDo you think that the study can be replicated?\n'

        # Check for NaN (missing response)
        if pd.isna(correct) or pd.isna(confidence):
            prompt += 'You respond <<skip>>\n'
        else:
            if replicated == "yes":
                if correct == 1:
                    prompt += 'You respond <<yes>>.\n'
                elif correct == 0:
                    prompt += 'You respond <<no>>.\n'
            elif replicated == "no":
                if correct == 1:
                    prompt += 'You respond <<no>>.\n'
                elif correct == 0:
                    prompt += 'You respond <<yes>>.\n'
            prompt += 'How confident are you about your response?\n'
            prompt += 'You respond <<' + str(round(confidence * 100)) + ">>% confident.\n"

        #print(prompt)
    all_prompts.append({'experiment': 'rausch_unpublished_replication', 'participant': str(participant), 'text': prompt})
  
with jsonlines.open('prompts.jsonl', 'w') as writer:
    writer.write_all(all_prompts)
