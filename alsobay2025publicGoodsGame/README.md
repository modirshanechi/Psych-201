## Reference:
Alsobay, M., Rand, D. G., Watts, D. J., & Almaatouq, A. (2025). Integrative Experiments Identify How Punishment Impacts Welfare in Public Goods Games*

\*The article is under review. Below is from the manuscript which includes the extended description of the experiment and a statement regarding IRB approval.

### Abstract

Punishment as a mechanism for promoting cooperation has been studied extensively for more than two decades, but its effectiveness remains a matter of dispute. Here, we examine how punishment’s impact varies across cooperative settings through a large-scale integrative experiment. We vary 14 parameters that characterize public goods games, sampling 360 experimental conditions and collecting 147,618 decisions from 7,100 participants. Our results reveal striking heterogeneity in punishment effectiveness: while punishment consistently increases contributions, its impact on payoffs (i.e., efficiency) ranges from substantially positive to markedly negative depending on the cooperative context. To characterize these patterns, we developed predictive models that outperformed human forecasters (laypeople and domain experts) in predicting punishment outcomes in new settings. Communication emerged as the most predictive feature, followed by contribution framing (opt-out vs. opt-in), contribution type (variable vs. all-or-nothing), game length (number of rounds), peer outcome visibility (whether participants can see others’ earnings), and the availability of a reward mechanism. Interestingly, however, most of these features interact to influence punishment effectiveness rather than operating independently. For example, the extent to which longer games increase the effectiveness of punishment depends on whether groups can communicate. Together, our results refocus the debate over punishment from whether or not it “works” to the specific conditions under which it does and does not work. More broadly, our study demonstrates how integrative experiments can be combined with machine learning to uncover generalizable patterns, potentially involving interactions between multiple features, and help generate novel explanations in complex social phenomena.

### Materials and Methods

#### Participant Recruitment 

A total of 7,100 participants were recruited from a curated panel on Amazon Mechanical Turk (N=604) and Prolific (N=6,496) and randomly assigned to groups to play synchronous PGGs of varying design. Participants were monetarily incentivized to maximize their individual in-game earnings. Base pay, per round pay, and the conversion rate from in-game currency to USD were constant across all studies; other parameters that influence pay, such as the marginal per capita return, number of rounds, group size, and the cost and impact of punishment/reward, varied across games (see Table 1). Throughout the study, participants were only allowed to participate once.

The study was determined to be exempt under Category 3 (Benign Behavioral Intervention) by the Committee on the Use of Humans as Experimental Subjects at the Massachusetts Institute of Technology (Protocol #E-5462). All participants provided explicit consent. For details on recruitment materials and the incentive structure, see SI Section S5.

#### Experiment Implementation 
Our PGG is implemented as a series of rounds, where each round is composed of three consecutive stages: (1) In the contribution stage, players are each granted a per round endowment and decide how much of the endowment to contribute to the public fund. (2) In the redistribution stage, players are shown the coins contributed by each player, as well as the sum of all contributions, and the amount redistributed to each player. During this stage, players may punish and/or reward other players, as applicable to the configuration of the PGG. (3) In the round summary stage, players view a summary of their earnings, including their retained endowment, share of the public fund payoff, and punishments/rewards that were given/received; depending on the PGG configuration, they may also view this information for other players. No actions are taken during this stage. After the round summary stage is complete, another round begins starting from the contribution stage. 

Before entering a game, players complete an interactive walkthrough of the actual interface used in-game, with a question to check their comprehension after each stage’s explanation. To ensure active participation throughout the duration of the games, we also implement measures to detect and remove idle players—for details of the walkthrough and idle detection, please see SI Sections S5 and S6. As detailed in Table 1, 14 PGG parameters were actively manipulated throughout the study. Other factors were held constant across all PGG configurations, including the duration of all stages (45 seconds), the per round endowment (20 coins), and the details of the financial incentive structure (base pay, per round participation pay, lobby pay, and the conversion rate from coins to USD). For details on parameter definitions and their implications on the game’s mechanics and interface, please refer to SI Section S6. 

#### Table 1. Design space parameters

| **Parameter**              | **Description**                                                                 | **Values**                         |
|---------------------------|---------------------------------------------------------------------------------|------------------------------------|
| Group Size                | Number of players in the game                                                  | 2–20 players                       |
| Game Length               | Number of rounds in the game                                                   | 1–30 rounds                        |
| Contribution Type         | Whether players can contribute any amount or must choose between all or none  | {variable, all-or-nothing}        |
| Contribution Framing      | Whether each player’s endowment starts in their private account (opt-in) or in the public fund (opt-out) | {opt-in, opt-out} |
| MPCR                      | Marginal per capita return on contributions, defined as the fund multiplier divided by group size | 0.06–0.7         |
| Communication             | Whether players can communicate through a chat window during the game          | {enabled, disabled}               |
| Peer Outcome Visibility   | Whether players can see summaries of others’ earnings and punishments/rewards received in each round | {visible, hidden} |
| Actor Anonymity           | Whether the identity of players who punish or reward others is revealed        | {revealed, hidden}                |
| Horizon Knowledge         | Whether players are shown the total number of rounds and rounds remaining      | {known, unknown}                  |
| Punishment                | Whether players can impose costly penalties on others (focal treatment)        | {enabled, disabled}               |
| Peer Incentive Cost       | Number of coins a player must spend to impose one unit of punishment or grant one unit of reward | 1–4 coins          |
| Punishment Impact         | Number of coins deducted from the punished player per coin spent punishing     | 1–4 coins                          |
| Reward                    | Whether players can grant costly rewards to others                             | {enabled, disabled}               |
| Reward Impact             | Number of coins granted to the rewarded player per coin spent rewarding        | 0.5–1.5 coins                      |



## Data source:
https://osf.io/2d56w/files/osfstorage?view_only=d046c1c417024569a8f9fed9e6c8d4d1