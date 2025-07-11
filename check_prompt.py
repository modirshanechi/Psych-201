import jsonlines

with jsonlines.open('holton2024goalcommitment/prompts.jsonl') as reader:

    num_choices = 0
    max_choices = 0
    max_length = 0
    for k, obj in enumerate(reader):
        if k == 999999:
            break
        num_choices += obj['text'].count('<<')
        if k == 10:
            print(obj['text'])
            print(obj['experiment'])

        if len(obj['text']) > max_length:
            max_length = len(obj['text'])

    #print('Maximum number of choices: ' + str(max_choices))
    print(obj.keys())
    print('Maximum token length in tokens: ' + str(max_length / 4))
    print('Number of participants: ' +  str(k+1))
    print('Number of choices: ' +  str(num_choices))
    print()
