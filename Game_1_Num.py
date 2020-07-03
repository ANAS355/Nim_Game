import random
import datetime
import json
from os import listdir
from os.path import isfile, join
import MatrixV355 as Mat


def dig_to_bin(dig_number):
    bin_number = bin(dig_number).replace("0b", "")[::-1]
    list_bin_number = []
    for x in bin_number:
        list_bin_number.append(int(x))
    return list_bin_number


def bin_num_matrix(list_numbers):
    if type(list_numbers) == list:
        len_list_numbers = len(dig_to_bin(max(list_numbers)))
        binary_numbers_matrix = Mat.Matrix.generate_matrix(n, len_list_numbers, 0)
        for x in range(n):
            p = dig_to_bin(list_numbers[x])
            while len(p) < len_list_numbers:
                p.append(0)
            binary_numbers_matrix.overwrite_row(x, Mat.Matrix([p]))
        return binary_numbers_matrix
    else:
        return 'bin_num_matrix function input must be a list of numbers'


def safe_zone(binary_numbers_matrix):
    if type(binary_numbers_matrix) == Mat.Matrix:
        temp_list = []
        for x in range(binary_numbers_matrix.columns):
            if binary_numbers_matrix.sum_column_values(x) % 2 == 0 or binary_numbers_matrix.sum_column_values(x) == 0:
                temp_list.append(1)
            else:
                temp_list.append(0)
        return temp_list
    else:
        return 'safe_zone function input must be a matrix type'


def check_safe(safe_list):
    safe_condition = True
    for x in safe_list:
        if x == 0:
            safe_condition = False
            break
    return safe_condition


def bin_to_dig(bin_num):
    count = 0
    for x in range(len(bin_num)):
        if bin_num[x] == 1:
            count += 2 ** x
    return abs(count)


def get_safe(bin_num_list, x):
    safe_list = safe_zone(bin_num_matrix(bin_num_list))
    check_list_1 = dig_to_bin(bin_num_list[x])
    check_list_2 = bin_num_list[x]
    while len(check_list_1) < len(safe_list):
        check_list_1.append(0)
    for j in range(len(safe_list)):
        if safe_list[j] == 0:
            if check_list_1[j] == 0:
                check_list_1[j] = 1
            elif check_list_1[j] == 1:
                check_list_1[j] = 0
    return bin_to_dig(check_list_1), check_list_2


def go_safe(safe_list):
    for x in range(len(safe_list)):
        safe_l, safe_num = get_safe(safe_list, x)
        if safe_num > safe_l:
            return safe_num - safe_l, x
    return 1, safe_list.index(max(safe_list))


def input_bot(list_p, name_bot):
    print('Turn', name_bot)
    data_replay.append('Turn ' + str(name_bot) + '\n')
    c, x = go_safe(list_p)
    print('Cell number : ', x + 1)
    data_replay.append('Cell number : ' + str(x + 1) + '\n')
    print('Cell minus : ', c)
    data_replay.append('Cell minus : ' + str(c) + '\n')
    list_p[x] -= c
    print(list_p)
    data_replay.append(str(list_p) + '\n')
    return list_p


def input_p(list_p, name_p):
    print('Turn', name_p)
    data_replay.append('Turn ' + name_p + '\n')
    number_place = int(input('Cell number : '))
    if number_place == 0:
        save_game(list_p, name_p, list_p_names, '')
    data_replay.append('Cell number : ' + str(number_place) + '\n')
    number_minus = int(input('Cell minus : '))
    if number_minus == 0:
        save_game(list_p, name_p, list_p_names, '')
    data_replay.append('Cell minus : ' + str(number_minus) + '\n')
    if 0 < number_place <= len(list_p) and list_p[number_place - 1] >= number_minus > 0:
        list_p[number_place - 1] -= number_minus
        print(list_p)
        data_replay.append(str(list_p) + '\n')
    else:
        print('invalid input')
        data_replay.append('invalid input' + '\n')
        input_p(list_p, name_p)
    return list_p


def save_game(save_play_list, save_turn, save_list_turns, save_name):
    print('Saveing ...')
    data = {'play list': save_play_list, 'turn': save_turn, 'list turns': save_list_turns}
    with open('save/{0}_{1}.json'.format(save_name, date), 'w') as save_data:
        json.dump(data, save_data, indent=4)
    print('Game saved')


def save_replay(data, data_name):
    print('Saving ...')
    file = 'Replays/replay_{0}_{1}.txt'.format(data_name, date)
    replay = open('Replays/replay_{0}_{1}.txt'.format(data_name, date), 'w')
    replay.writelines(data)
    replay.close()
    print('File saved_replay: ' + file)


def load_replay(replay_name):
    print('Loading ...')
    print('-----------------------Playing replay( {0} )-----------------------'.format(replay_name))
    with open('Replays/' + replay_name) as re:
        contents = re.read()
    print(contents)
    print('-----------------------Replay( {0} )ended-----------------------  '.format(replay_name))
    return


global date
date = str(datetime.datetime.now())
for i in range(len(date)):
    if date[i] in './-?"|:* ':
        date = date.replace(date[i], '_')
while True:
    print('1:New Game\n2:Load Replay\n3:Exit Game')
    chose = int(input())
    if chose == 1:
        global data_replay
        data_replay = []
        n = int(input('number of cells = '))
        data_replay.append('number of cells = ' + str(n) + '\n')
        r = int(input('range of cells from 1 to : '))
        data_replay.append('range of cells from 1 to : ' + str(r) + '\n')
        num_of_rounds = int(input('Number of rounds = '))
        data_replay.append('Number of rounds = ' + str(num_of_rounds) + '\n')
        num_p = int(input('Number of players = '))
        data_replay.append('Number of players = ' + str(num_p) + '\n')
        play_list = [random.randint(1, r) for i in range(n)]
        print('If you want to add bots write the name like this (bot_name)')
        print('The order of the input names will be the order of the playing turns')
        global zero_list
        zero_list = [0 for i in range(n)]
        list_p_names = []
        for i in range(num_p):
            print('Name of player', i + 1, end=" : ")
            list_p_names.append(input())
        for i in range(len(list_p_names)):
            data_replay.append('Name of player ' + str(i + 1) + ' : ' + list_p_names[i] + '\n')
        round_list = {}
        score_list = {}
        for i in range(len(list_p_names)):
            score_list[list_p_names[i]] = 0
        for round_num in range(1, num_of_rounds + 1):
            global play_l
            play_l = [random.randint(1, r) for i in range(n)]
            print('round', round_num)
            data_replay.append('round ' + str(round_num) + '\n')
            print(play_l)
            data_replay.append(str(play_l) + '\n')
            while play_l != zero_list:
                for i in range(len(list_p_names)):
                    if list_p_names[i][:4] == 'bot_':
                        input_bot(play_l, list_p_names[i])
                        if play_l == zero_list:
                            print(list_p_names[i], 'Wins')
                            data_replay.append(list_p_names[i] + ' Wins' + '\n')
                            round_list['round_' + str(round_num)] = list_p_names[i]
                            score_list[list_p_names[i]] += 1
                            break
                    else:
                        input_p(play_l, list_p_names[i])
                        if play_l == zero_list:
                            print(list_p_names[i], 'Wins')
                            data_replay.append(list_p_names[i] + 'Wins' + '\n')
                            round_list['round_' + str(round_num)] = list_p_names[i]
                            score_list[list_p_names[i]] += 1
                            break
        print('rounds results:')
        data_replay.append('rounds results:\n')
        for i in round_list:
            print(str(i) + '    ' + str(round_list[i]))
            data_replay.append(str(i) + '    ' + str(round_list[i]) + '\n')
        print('Scores:')
        data_replay.append('Scores:\n')
        for i in score_list:
            print(str(i) + '    ' + str(score_list[i]))
            data_replay.append(str(i) + '    ' + str(score_list[i]) + '\n')
        print(datetime.datetime.now())
        data_replay.append(str(datetime.datetime.now()))
        print('Do you want to save replay\n1:Yes     2:No')
        chose = int(input())
        if chose == 1:
            name_of_replay = input('Name of the replay : ')
            save_replay(data_replay, name_of_replay)
    elif chose == 2:
        replay_files = [f for f in listdir('Replays') if isfile(join('Replays', f))]
        print('List of replays:')
        for i in range(len(replay_files)):
            print(i + 1, ':', replay_files[i])
        replay_chose = int(input('load replay no:'))
        load_replay(replay_files[replay_chose - 1])
    elif chose == 3:
        print('Closing...')
        break
    else:
        print('please enter a valid chose')
