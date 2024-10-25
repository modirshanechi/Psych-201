# Psych-201

Psych-201 is a collaborative data set currently under construction. It extends [Psych-101](https://huggingface.co/datasets/marcelbinz/Psych-101), a large-scale data set containing natural language transcriptions of human psychology experiments.
We aim to collect a data set 10x the size of Psych-101, meaning that Psych-201 would cover 100,000,000 human choices from nearly 1,000,000 participants. 

We will summarize this new data set in a paper for the NeurIPS 2025 Datasets and Benchmarks Track (or a similar venue). Every contributor will be eligible for co-authorship on this paper. If you want to contribute, please follow the instructions below. In case you are unsure whether the experiment you have in mind is suitable for Psych-201, please [reach out](mailto:marcel.binz@helmholtz-munich.de) first.

## Repository structure

If you want to contribute an experiment, please make a pull request. To do so, first create a new folder with a meaningful name. This folder should contain:

* a README.md file with a paper reference and a link to the original data.
* a prompts.jsonl file where each line corresponds to one participant. Each line should have the following three fields:
    - "text": Natural language transcription of the experiment.
    - "experiment": Identifier for the experiment.
    - "participant": Identifier for the participant.
* a generate_prompts.py file that reads in the original data and produces prompts.jsonl  

Please do not upload the original data files to this repository.

[This folder](https://github.com/marcelbinz/Psych-201/tree/main/binz2022heuristics) provides an example for structuring.

## Prompt formatting

* Each prompt corresponds to an entire experiment from one participant.
* It should contain data on a trial-by-trial level and start with the instructions.
* Use the cover story and instructions from the original paper if possible.
* 32K tokens per participant is the length limit.
* Mark the parts that should be finetuned (i.e., human choices) with “<<“ and “>>”. Do not use these symbols for other parts of the prompt.
* For discrete choice options, randomize the names of choice options for each participant [binz2022heuristics/generate_prompts.py](https://github.com/marcelbinz/Psych-201/tree/main/binz2022heuristics/generate_prompts.py).

Example prompt:

~~~
You will be visiting different planets on which you repeatedly have to predict a winner in an athletic competition between two aliens, labelled A and V.
In each round, you have to indicate the winner by pressing the corresponding key.
Your goal is to be as accurate as possible.
To aid your decision process, you are provided with two attributes of the two aliens.
You receive feedback telling you which alien won after you have made a choice.
You have to make ten predictions per planet.
For each prediction, you encounter a new pair of aliens.
You are beamed to a new planet after making ten predictions, where you have to make predictions about a new and different athletic competition.

Planet 1:
Alien A scores 2.02 higher on attribute 1. Alien A scores 3.36 higher on attribute 2. You press <<A>>. Alien A wins.
Alien A scores 2.21 higher on attribute 1. Alien A scores 0.46 higher on attribute 2. You press <<A>>. Alien A wins.
Alien A scores 1.21 higher on attribute 1. Alien V scores 0.53 higher on attribute 2. You press <<V>>. Alien A wins.
Alien A scores 0.48 higher on attribute 1. Alien V scores 1.14 higher on attribute 2. You press <<A>>. Alien A wins.
Alien A scores 0.93 higher on attribute 1. Alien V scores 2.85 higher on attribute 2. You press <<V>>. Alien A wins.
Alien V scores 1.82 higher on attribute 1. Alien A scores 0.09 higher on attribute 2. You press <<V>>. Alien V wins.
Alien A scores 0.33 higher on attribute 1. Alien A scores 0.54 higher on attribute 2. You press <<A>>. Alien A wins.
Alien V scores 0.39 higher on attribute 1. Alien V scores 0.27 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 0.33 higher on attribute 1. Alien V scores 0.91 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 3.12 higher on attribute 1. Alien V scores 1.08 higher on attribute 2. You press <<V>>. Alien V wins.

Planet 2:
Alien A scores 0.74 higher on attribute 1. Alien A scores 0.28 higher on attribute 2. You press <<A>>. Alien V wins.
Alien V scores 0.04 higher on attribute 1. Alien A scores 0.49 higher on attribute 2. You press <<V>>. Alien A wins.
Alien V scores 1.02 higher on attribute 1. Alien V scores 2.08 higher on attribute 2. You press <<V>>. Alien A wins.
Alien A scores 1.14 higher on attribute 1. Alien A scores 0.99 higher on attribute 2. You press <<V>>. Alien V wins.
Alien A scores 1.18 higher on attribute 1. Alien A scores 1.74 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 0.33 higher on attribute 1. Alien V scores 1.32 higher on attribute 2. You press <<A>>. Alien A wins.
Alien A scores 0.08 higher on attribute 1. Alien A scores 1.15 higher on attribute 2. You press <<V>>. Alien A wins.
Alien V scores 3.02 higher on attribute 1. Alien V scores 3.11 higher on attribute 2. You press <<A>>. Alien A wins.
Alien V scores 1.8 higher on attribute 1. Alien V scores 1.67 higher on attribute 2. You press <<A>>. Alien A wins.
Alien V scores 0.06 higher on attribute 1. Alien A scores 0.69 higher on attribute 2. You press <<A>>. Alien A wins.

...

Planet 30:
Alien V scores 0.24 higher on attribute 1. Alien A scores 1.1 higher on attribute 2. You press <<A>>. Alien V wins.
Alien V scores 0.8 higher on attribute 1. Alien V scores 1.12 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 1.22 higher on attribute 1. Alien A scores 0.47 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 0.25 higher on attribute 1. Alien V scores 0.74 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 1.61 higher on attribute 1. Alien V scores 0.39 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 1.72 higher on attribute 1. Alien V scores 0.03 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 2.06 higher on attribute 1. Alien V scores 1.09 higher on attribute 2. You press <<V>>. Alien V wins.
Alien A scores 0.24 higher on attribute 1. Alien V scores 0.48 higher on attribute 2. You press <<V>>. Alien A wins.
Alien V scores 0.7 higher on attribute 1. Alien V scores 1.43 higher on attribute 2. You press <<V>>. Alien V wins.
Alien V scores 0.7 higher on attribute 1. Alien A scores 0.39 higher on attribute 2. You press <<A>>. Alien A wins.
~~~
  
