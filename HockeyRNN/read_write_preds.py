import csv
import pandas as import pd
from time import strftime


print('-------------------------------------')
print('---                               ---')
print('---    Predicting future years    ---')
print('---                               ---')
print('-------------------------------------')


df = pd.read_csv('all_current_players.csv')
with open ('current_players_2019.csv', 'a+') as doesthiswork:
    doesthiswork.write('\n')
    for name in df['Full_Name'].unique():
        G = df[df.Full_Name == name]['G']
        _G = df[df.Full_Name == name]['GP']
        team = df[df.Full_Name == name]['Team'][-1:]
        position = df[df.Full_Name == name]['Pos'][-1:]
        age = df[df.Full_Name == name]['Age'][-1:]
        team = team.to_string(index=False)
        position = position.to_string(index=False)
        age = round(float(age.to_string(index=False)))
        goals = []
        games = []
        gpg = []
        for i in G:
            if i == 0:
                goals.append(0)
            else:
                goals.append(i)
        for i in _G:
                games.append(i)
        for j in range(0, len(goals)):
            if games[j] < 30:
                gpg.append(goals[j]*2)
            elif goals[j] == 0:
                gpg.append(0)
            else:
                gpg.append(round((goals[j]/games[j])*82))
        if len(gpg) == 1:
            gpg.append(gpg[0])
        if len(gpg) == 2:
            gpg.append(gpg[1])

        #print(name, gpg)
        player_career = gpg
        current_year = 2018
        for _ in range(0, 5):
            input_sequence = list(map(str, player_career))
            prediction = predictor.predict(input_sequence)
            string = '{name}: {input_sequence}{prediction}'.format(name=name, input_sequence=input_sequence, prediction=prediction)
            print(string)
            player_career.append(prediction[0])
            new_csv_line = ",12,{age},{name},{prediction},82,12,{position},{current_year},{team}".format(age=age, name=name, prediction=prediction[0], position=position, current_year=current_year, team=team)
            doesthiswork.write('{new_csv_line}\n'.format(new_csv_line=new_csv_line))
            current_year += 1
            age += 1


with open('accuracy_test.txt', 'w+') as acc:
    with open('NHL_GPG_edit.txt', 'r') as gpg:
        count = 0
        for i, line in enumerate(gpg):
            if count % 200 == 0:
                pct_done = round(((float(count)/23000)*100), 3)
                print('Predicted {count} values.... {pct_done}% Finished...'.format(count=count, pct_done=pct_done))
            line = line.split('\t')
            input_seq = line[0].split()
            target = (line[1].split())[0]
            pred_value = predictor.predict(input_seq)
            acc.write('{pred_value} {target}\n'.format(pred_value=pred_value[0], target=target))
            count += 1

    print('---------------------------------')
    print('---                           ---')
    print('---     Accuracy logged:      ---')
    print('---           see             ---')
    print('---     accuracy_test.txt     ---')
    print('---                           ---')
    print('---------------------------------')

_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
with open('epoch_log.txt', 'a+') as elog:
    elog.write('\nNew Test Finished: {_time}\n'.format(_time=_time))
    elog.write('Completed {num_epochs} epochs\n'.format(num_epochs=num_epochs))
    elog.write('Use timestamp to find final checkpoint')

print('\n')
print('Measured Accuracy:')

total_accuracy = 0
num_off_by = 0
total_lines = 0

with open('accuracy_test.txt', 'r') as acc:
    for i, line in enumerate(acc):
        if '<eos>' in line:
            line = '1 1'
            #line.replace('<eos>', '1')
        line = line.split()
        line = [int(i) for i in line]
        if line[0] == 0:
            line[0] = 1
        if line[1] == 0:
            line[1] = 1
        accuracy = min(line)/max(line)
        off_by = max(line)-min(line)
        total_accuracy += accuracy
        num_off_by += off_by
        total_lines += 1
accuracy_final = float(total_accuracy)/float(total_lines)
off_by_final = num_off_by/total_lines
with open('epoch_log.txt', 'a+') as elog:
    elog.write('\n')
    elog.write('Measured Accuracy: {accuracy_final}\n'.format(accuracy_final=accuracy_final))
    elog.write('Average Off By: {off_by_final}\n'.format(off_by_final=off_by_final))
print(accuracy_final, off_by_final, '\n')