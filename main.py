import re
from colorama import *
from datetime import datetime


# init
just_fix_windows_console()
global res
res = ""


def collect(round: str):
    with open(f"./pgn_folder/{round}.pgn") as f:
        data = str(f.read())
        f.close()

    data = data.split('\n\n\n\n') # idk y 4 '\n's tbh


    first_w_moves1 = {}
    first_b_moves1 = {}

    termination = []
    wintermin = {}
    drawtermin = {}


    for i in data:
        i = i.split(']\n')
        termination.append(i[11])

        pgn = ''.join(i[12:]) # original move part
        pgn = re.sub('\d+\.\s|1-0|0-1|1/2-1/2', '', pgn) # processed pgn with no move number and results
        pgn = re.sub('\n', ' ', pgn) # get rid of useless new lines that are for making pgn readable

        moves = pgn.split()

        try:
            first_w_moves1[moves[0]] += 1 # {'d4': 1}
        except:
            first_w_moves1[moves[0]] = 1
            first_b_moves1[moves[0]] = {}

        try:
            first_b_moves1[moves[0]][moves[1]] += 1 # moves1['d4'] {'d4': {'Nf3': 1}}
        except:
            first_b_moves1[moves[0]][moves[1]] = 1


    print(termination)
    for j in termination:
        # wins
        if j.endswith('resignation"'):
            try:
                wintermin['by Resignation'] += 1
            except:
                wintermin['by Resignation'] = 1

        elif j.endswith('checkmate"'):
            try:
                wintermin['by Checkmate'] += 1
            except:
                wintermin['by Checkmate'] = 1

        elif j.endswith('on time"'):
            try:
                wintermin['on Time'] += 1
            except:
                wintermin['on Time'] = 1

        elif j.endswith('game abandoned"'):
            try:
                wintermin['by Abandonment'] += 1
            except:
                wintermin['by Abandonment'] = 1
        # draws
        elif j.endswith('agreement"'):
            try:
                drawtermin['by Agreement'] += 1
            except:
                drawtermin['by Agreement'] = 1

        elif j.endswith('repetition"'):
            try:
                drawtermin['by Repetition'] += 1
            except:
                drawtermin['by Repetition'] = 1

        elif j.endswith('stalemate"'):
            try:
                drawtermin['by Stalemate'] += 1
            except:
                drawtermin['by Stalemate'] = 1

        elif j.endswith('50-move rule"'):
            try:
                drawtermin['by 50 Move Rule'] += 1
            except:
                drawtermin['by 50 Move Rule'] = 1

        elif j.endswith('insufficient material"'):
            try:
                drawtermin['by Insufficient Material'] += 1
            except:
                drawtermin['by Insufficient Material'] = 1

        elif j.endswith('by timeout vs insufficient material"'):
            try:
                drawtermin['by Timeout VS Insufficient'] += 1
            except:
                drawtermin['by Timeout VS Insufficient'] = 1


# --------------------------------------------------------
    fwm1 = dict(sorted(first_w_moves1.items(), key=lambda item: item[1], reverse=True)) # sorted by games count in descending order
    global res

    res += f"\n\n    {round}\n    ---------------------------------------\n"
    res += "    Overall outcome:\n"
    res += "        Won:\n"

    for wins in wintermin:
        res += f"            {wins}: {wintermin[wins]} games\n"

    res += "        Drawn:\n"

    for draws in drawtermin:
        res += f"            {draws}: {drawtermin[draws]} games\n"

    res += "    Popular first moves:\n"

    for i in fwm1:
        res += f"        1.{i}: {fwm1[i]} games\n"

    res += "            Continuations:\n"

    for k in first_b_moves1[i]:
        fbm1 = dict(sorted(first_b_moves1[i].items(), key=lambda item: item[1], reverse=True))
    for j in fbm1:
        res += f"                1...{j}: {fbm1[j]} games\n"

collect('round_1')
collect('round_2')
collect('round_3')
collect('round_4')
collect('losers_round_1')
collect('losers_round_2')
collect('losers_round_3')

with open("README.md", "w") as f:
    f.write(res)
f.close()
