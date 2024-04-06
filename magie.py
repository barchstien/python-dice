#!/bin/python

import sys, yaml

DICE_T = 10

def usage():
    print('''
    {} <spell difficulty> <num of d{}>
    '''.format(sys.argv[0], DICE_T))


class Warhammer_spell_probability:
    # success count
    success = 0
    # total count
    cnt = 0
    # doubles, triples, etc
    # stored as [doubles, triples, etc]
    n_ples = []

    def recursive_fill(self, n_array_coord_cursor, depth, ttable, num_of_dice, magie_noire):
        for i in range(DICE_T):
            if depth <= 1:
                # reached the leaf, fill the sum
                leaf = sum(n_array_coord_cursor)
                if magie_noire:
                    # remove the weakest dice, ie coord
                    leaf -= min(n_array_coord_cursor)
                ttable.append(leaf)
                # total
                self.cnt += 1
                # bigger than target and not 1 to all dice
                if leaf >= self.target and leaf != num_of_dice:
                    self.success += 1
                # doubles, triples, etc
                for n in range(2, num_of_dice + 1):
                    pass
                    #occurences = 0
                    # for all possibles values with d{DICE_T}
                    for v in range(1, DICE_T+1):
                        occurences = 0
                        # check current dices values
                        for d in n_array_coord_cursor:
                            if v == d:
                                occurences += 1
                                #print("++++")
                        if occurences >= n:
                            self.n_ples[n-2] += 1
            else:
                ttable.append([])
                self.recursive_fill(n_array_coord_cursor, depth - 1, ttable[-1], num_of_dice, magie_noire)
            n_array_coord_cursor[-1*depth] += 1
        # rest coord to beginning of line
        n_array_coord_cursor[-1*depth] = 1

    def make_n_array_and_recurse(self, num_of_dice, magie_noire, target):
        # truth table n-dimension(s), n = number of dice
        # contains the sum of dice (+/- magie noire if enabled)
        ttable = []

        # set to 0 chances to get double, triple, etc
        self.n_ples = []
        # minimum 2 dices
        for i in range(num_of_dice - 1):
            self.n_ples.append(0)
            
        self.success = 0
        self.cnt = 0
        self.target = target
        
        # current truth table coordinate, n-dimension(s)
        # coordinates are also the values of dice thrown, ie in [1;DICE_T]
        n_array_coord_cursor = []
        # set coord at origin N * {1}
        for i in range(num_of_dice):
            n_array_coord_cursor.append(1)
        self.recursive_fill(n_array_coord_cursor, num_of_dice, ttable, num_of_dice, magie_noire)

    
    def probability_success(self, target, num_of_dice):
        """
        @param target target value tu succeed spell
        @param num_of_dice ie thrown
        """
        self.make_n_array_and_recurse(num_of_dice, False, target)
        ret = {
            'Target': target,
            'Using': '{}d{}'.format(num_of_dice, DICE_T),
            'Success %': self.success/self.cnt * 100,
            'Malédiction de Tzeench': {}
        }
        cnt = 2
        for i in self.n_ples:
            ret['Malédiction de Tzeench']['{}-ples'.format(cnt)] = i/self.cnt
            cnt += 1
        
        # Magie Noire
        self.make_n_array_and_recurse(num_of_dice+1, True, target)
        ret['Magie Noire'] = {
            'Success %': self.success/self.cnt * 100,
            'Malédiction de Tzeench': {}
        }
        cnt = 2
        for i in self.n_ples:
            ret['Magie Noire']['Malédiction de Tzeench']['{}-ples'.format(cnt)] = i/self.cnt
            cnt += 1
        return ret

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

    #print('Chance to get at least {} with {}d{}'.format(at_least, num_of_dice, DICE_T))

    #if magie_noire:
    #    print('-\_-={{magie noire}}=-_/-')
    #    print('  throw extra d{0}, replaces a lower d{0} result\n'.format(DICE_T))
    #    # add a dice to total, but that is removed later
    #    num_of_dice += 1

    wsp = Warhammer_spell_probability()
    ret = wsp.probability_success(at_least, num_of_dice)
    
    print(yaml.dump(ret, allow_unicode=True, default_flow_style=False, sort_keys=False))

    

