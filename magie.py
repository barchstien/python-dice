#!/bin/python

import sys

# ! Only for dice 10 !

def usage():
    print('''
    sys.argv[0] spell_difficulty num_of_dice [true|TRUE-1|mn|magie-noire]
    ''')

# min value to succeed spell
global at_least

# total count
global success
success = 0
# count set which give success
global cnt
cnt = 0

# track doubles, triples, etc
# stored as [doubles, triples, etc]
global n_ples
n_ples = []

DICE_T = 10


def simple():
    """First proto, 2 dice only, DEPRECATED"""
    print('Chance to get at least {} with {}d10'.format(at_least, num_of_dice))
    truth_table = []
    for i in range(1,11):
        truth_table.append([])
        for j in range(1,11):
          truth_table[-1].append(i+j)
          if i+j >= int(at_least):
              success += 1
          cnt += 1
    for l in truth_table:
        #print(l)
        print("{: >2} {: >2} {: >2} {: >2} {: >2} {: >2} {: >2} {: >2} {: >2} {: >2}".format(*l))
    print('chances {}'.format(success/cnt))


def recursive_fill(n_array_coord, depth, ttable, num_of_dice, magie_noire):
    global success
    global cnt

    for i in range(DICE_T):
        if depth <= 1:
            # reached the leaf, fill the sum
            leaf = sum(n_array_coord)
            if magie_noire:
                # remove the weakest dice, ie coord
                leaf -= min(n_array_coord)
            ttable.append(leaf)
            # total
            cnt += 1
            # bigger than target and not 1 to all dice
            if leaf >= at_least and leaf != num_of_dice:
                success += 1
            # doubles, triples, etc
            # debug only do doubles ------------------- TODO
            for n in range(2, num_of_dice + 1):
                pass
                #occurences = 0
                # for all possibles values with d{DICE_T}
                for v in range(1, 11):
                    occurences = 0
                    # check current dices values
                    #print('v {} coord {}'.format(v, n_array_coord))
                    for d in n_array_coord:
                        if v == d:
                            occurences += 1
                            #print("++++")
                    if occurences >= n:
                        n_ples[n-2] += 1
                #print('-------- n:{} occurences:{} n_ples:{}'.format(n, occurences, n_ples))
        else:
            ttable.append([])
            recursive_fill(n_array_coord, depth - 1, ttable[-1], num_of_dice, magie_noire)
        n_array_coord[-1*depth] += 1
    # rest coord to beginning of line
    n_array_coord[-1*depth] = 1

def n_array(num_of_dice, magie_noire):
    # truth table n-dimension(s), n = number of dice
    # contains the sum of dice (+/- magie noire if enabled)
    ttable = []
    # current truth table coordinate, n-dimension(s)
    # coordinates are also the values of dice thrown, ie in [1;DICE_T]
    n_array_coord = []
    
    # set coord at origin N * {1}
    for i in range(num_of_dice):
        n_array_coord.append(1)
    recursive_fill(n_array_coord, num_of_dice, ttable, num_of_dice, magie_noire)

if __name__ == '__main__':
    if len(sys.argv) < 3 :
        usage()
        sys.exit(51)
    # min number to succeed spell
    at_least = int(sys.argv[1])
    # number of dice
    num_of_dice = int(sys.argv[2])
    if num_of_dice < 2:
        print('Use at least 2 dice !')
        sys.exit(51)
    # "extra" dice with black magie, replaces a normal dice if better
    magie_noire = False
    if len(sys.argv) > 3 :
        magie_noire = sys.argv[3] in ['true', True, '1', 'mn', 'magie-noire']

    print('Chance to get at least {} with {}d{}'.format(at_least, num_of_dice, DICE_T))

    if magie_noire:
        print('-\_-={{magie noire}}=-_/-')
        print('  throw extra d{0}, replaces a lower d{0} result\n'.format(DICE_T))
        # add a dice to total, but that is removed later
        num_of_dice += 1

    # set to 0 chances to get double, triple, etc
    for i in range(2, num_of_dice + 1):
        n_ples.append(0)
    
    #simple()
    n_array(num_of_dice, magie_noire)

    print('---> {}\n'.format(success/cnt))
    #print('success {} cnt  {}'.format(success, cnt))

    #print('n_ples {}'.format(n_ples))
    print('Malédiction de Tzeench')
    print('doubles, triples, n-ples....')
    for i in range (2, num_of_dice + 1):
        print('  {}-ples {}'.format(i, n_ples[i-2]/cnt))

