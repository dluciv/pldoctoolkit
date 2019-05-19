#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import difflib
import re
import itertools

# testing
import unittest
from textwrap import dedent
import cProfile
from pstats import Stats

__author__ = "Victor Dolotov, Dmitry Luciv"
__copyright__ = "Copyright 2018+, The DocLine Project"
__credits__ = ["Victor Dolotov", "Dmitry Luciv"]
__license__ = "LGPL"
__version__ = "1.0.1"
__maintainer__ = "Dmitry Luciv"
__email__ = "yogiman1996@gmail.com"  # Victor Dolotov
__status__ = "Alpha"


def archetype_search(group):
    # Форматирование повторов
    work_group = group.copy()
    for i in range(len(work_group)):
        work_group[i] = work_group[i].lower()
        work_group[i] = re.sub(r'(\W*)(\w+)(\W*)', r'\1 \2 \3', work_group[i])
        work_group[i] = re.sub(r'([^\s\w])([^\s\w])', r'\1 \2', work_group[i])
        work_group[i] = re.sub(r'\s+', r' ', work_group[i])
        work_group[i] = re.sub(r'^ | $', r'', work_group[i])
    indexes = [0]
    for i in range(1, len(work_group)):
        if work_group[i - 1] != work_group[i]:
            indexes.append(i)
    #

    # Исключение точных групп и повторов
    work_group = [work_group[i] for i in indexes]
    num_dup = len(work_group)
    if num_dup == 1:
        return [[(0, len(dup))] for dup in group]
    #

    # Получение перестановок
    max_num_perms = max(120, num_dup + 1)
    M = 0
    num_perms = 1
    while M <= num_dup and num_perms < max_num_perms:
        num_perms *= num_dup - M
        M += 1
    M -= 1
    work_group = [dup.split(' ') for dup in work_group]
    perms = list(itertools.permutations(work_group, M))
    #

    # Поиск архетипа
    archetype = []
    for perm in perms:
        archetype_p = []
        if M == 1:
            for j in range(num_dup):
                if not perm.__contains__(work_group[j]):
                    archetype_p = alg(perm[0], work_group[j])
                    break
        else:
            archetype_p = alg(perm[0], perm[1])
        for j in range(2, M):
            archetype_p = alg(archetype_p, perm[j])
            if len(archetype_p) == 0:
                break
        for j in range(num_dup):
            if not perm.__contains__(work_group[j]):
                archetype_p = alg(archetype_p, work_group[j])
            if len(archetype_p) == 0:
                break
        if (len(archetype) < len(archetype_p)) | (
                (len(archetype) == len(archetype_p)) & (len(archetype.__str__()) < len(archetype_p.__str__()))):
            archetype = archetype_p

        # SequenceMatcher
        if M == 1:
            for j in range(num_dup):
                if not perm.__contains__(work_group[j]):
                    archetype_p = diffalg(perm[0], work_group[j])
                    break
        else:
            archetype_p = diffalg(perm[0], perm[1])
        for j in range(2, M):
            archetype_p = diffalg(archetype_p, perm[j])
            if len(archetype_p) == 0:
                break
        for j in range(num_dup):
            if not perm.__contains__(work_group[j]):
                archetype_p = diffalg(archetype_p, work_group[j])
            if len(archetype_p) == 0:
                break
        if (len(archetype) < len(archetype_p)) | (
                (len(archetype) == len(archetype_p)) & (len(archetype.__str__()) < len(archetype_p.__str__()))):
            archetype = archetype_p
        #
    #

    # Преобразование результата
    result = [[] for i in range(num_dup)]
    start = [0] * num_dup
    end = [0] * num_dup
    current_index = [0] * num_dup
    gr = [group[i].lower() for i in indexes]
    for i in range(len(work_group)):
        while work_group[i][current_index[i]] != archetype[0]:
            word = re.sub(r'([.?+*[\]\\^${}|()])', r'\\\1', work_group[i][current_index[i]])
            start[i] = re.search(word, gr[i][end[i]:]).end() + end[i]
            end[i] = start[i]
            current_index[i] += 1
        word = re.sub(r'([.?+*[\]\\^${}|()])', r'\\\1', work_group[i][current_index[i]])
        start[i] = re.search(word, gr[i][end[i]:]).start() + end[i]
        end[i] += re.search(word, gr[i][end[i]:]).end()
        current_index[i] += 1
    is_arc = True
    for arc in range(1, len(archetype)):
        for i in range(len(work_group)):
            if work_group[i][current_index[i]] != archetype[arc]:
                is_arc = False
                break
        for i in range(len(work_group)):
            if is_arc:
                word = re.sub(r'([.?+*[\]\\^${}|()])', r'\\\1', work_group[i][current_index[i]])
                end[i] += re.search(word, gr[i][end[i]:]).end()
                current_index[i] += 1
            else:
                result[i].append((start[i], end[i]))
                while work_group[i][current_index[i]] != archetype[arc]:
                    word = re.sub(r'([.?+*[\]\\^${}|()])', r'\\\1', work_group[i][current_index[i]])
                    start[i] = re.search(word, gr[i][end[i]:]).end() + end[i]
                    end[i] = start[i]
                    current_index[i] += 1
                word = re.sub(r'([.?+*[\]\\^${}|()])', r'\\\1', work_group[i][current_index[i]])
                start[i] = re.search(word, gr[i][end[i]:]).start() + end[i]
                end[i] += re.search(word, gr[i][end[i]:]).end()
                current_index[i] += 1
        is_arc = True
    for i in range(len(work_group)):
        result[i].append((start[i], end[i]))

    if num_dup < len(group):
        res = [[] for i in range(len(group))]
        for i in range(len(indexes)):
            res[indexes[i]] = result[i]
        for i in range(len(res)):
            if not res[i]:
                res[i] = res[i - 1]
        result = res
    #
    return result


def alg(duplicate_a, duplicate_b):
    mulct = -1
    num_words = max(len(duplicate_a), len(duplicate_b))

    matrix_score = [[0] * (len(duplicate_a) + 1) for i in range(len(duplicate_b) + 1)]
    for i in range(1, len(duplicate_a) + 1):
        matrix_score[0][i] = mulct * i
    for i in range(1, len(duplicate_b) + 1):
        matrix_score[i][0] = mulct * i
    for i in range(1, len(duplicate_b) + 1):
        for j in range(1, len(duplicate_a) + 1):
            diag = 0
            if duplicate_a[j - 1] == duplicate_b[i - 1]:
                diag = 10
            M = matrix_score[i - 1][j - 1] + num_words * diag * len(duplicate_b[i - 1])
            D = matrix_score[i - 1][j] + mulct
            I = matrix_score[i][j - 1] + mulct
            matrix_score[i][j] = max(M, D, I)

    res = []
    i = len(duplicate_b)
    j = len(duplicate_a)
    while i > 0 and j > 0:
        score = matrix_score[i][j]
        score_left = matrix_score[i][j - 1]
        score_up = matrix_score[i - 1][j]
        if score == score_up + mulct:
            i = i - 1
        else:
            if score == score_left + mulct:
                j = j - 1
            else:
                if duplicate_a[j - 1] == duplicate_b[i - 1]:
                    res.append(duplicate_a[j - 1])
                i = i - 1
                j = j - 1
    res.reverse()
    return res


def diffalg(a, b):
    seq = difflib.SequenceMatcher()
    seq.set_seqs(a, b)
    string = []
    for block in seq.get_matching_blocks():
        ai = block[0]
        if block[2] != 0:
            for i in range(block[2]):
                string.append(a[ai + i])
    return string


def permutations_first_volatile(rank: 'int', n_cover: 'int' = 3):
    """
    Generate subset of all possible permutations with first values changing more frequently
    :param rank: Permutations are tuples of [0, ..., rank)
    :param n_cover: number of first permutation elements to take all possible values
    :return: iterable of permutations
    """
    initial = list(reversed(range(rank)))
    initial_s = set(initial)

    for c in itertools.combinations(initial, n_cover):
        pf = tuple(reversed(c))
        yield pf + tuple(initial_s.difference(pf))

@functools.lru_cache(maxsize=None)
def two_tuples_lcs(w1: 'tuple[str]', w2: 'tuple[str]') -> 'tuple[str]':
    sm = difflib.SequenceMatcher(None, w1, w2, False)
    matches = sm.get_matching_blocks()
    return tuple(itertools.chain(*[ w1[match.a: match.a + match.size] for match in matches ]))


@functools.lru_cache(maxsize=None)
def possible_n_tuples_lcs(ws: 'iterable[tuple[str]]') -> 'tuple[str]':
    # operator.reduce is a kind of foldl
    return functools.reduce(two_tuples_lcs, ws)

@functools.lru_cache(maxsize=None)
def best_n_tuples_lcs(strings: 'list[tuple[str]]') -> 'tuple[str]':
    best_archetype = ()
    for p in permutations_first_volatile(len(strings)):
        permuted_strings = tuple(strings[i] for i in p)
        archetype = possible_n_tuples_lcs(permuted_strings)
        if len(archetype) > len(best_archetype):
            best_archetype = archetype
    return best_archetype

@functools.lru_cache(maxsize=None)
def get_variative_element(clones: 'module', group: 'clones.FuzzyCloneGroup' ) -> 'clones.VariativeElement':
    try:
        archetype: 'list[list[tuple[int, int]]]' = archetype_search(group.instancetexts)
        fuzzy_offsets = [b for n, b, e in group.instances]
        group_archetypes = list(map(list, zip(*archetype)))  # transpose

        groups = [
            clones.ExactCloneGroup(0, 1, [
                (
                    0,  # file №
                    o + b, o + e - 1 # -1 from Dolotov =)
                )
                for ((b, e), o) in zip(ginsts, fuzzy_offsets)
            ]) for ginsts in group_archetypes
        ]

        return clones.VariativeElement(groups)
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        return None

def get_html(clones: 'module', group, archetype):
    source = ''
    delimiter = '\n\n' + '-' * 200 + '\n\n'
    for dup in group:
        source += dup + delimiter
    source = source[:len(source) - len(delimiter)]
    file = open('Archetype\Duplicates.txt', "w", encoding='utf-8')
    file.write(source)
    file.close()
    clones.inputfiles = [clones.InputFile('Archetype\Duplicates.txt')]
    CloneGroups = [clones.ExactCloneGroup(0, 1, [(0, (0, 0), (0, 0))]) for i in range(len(archetype[0]))]
    for clone_group in CloneGroups:
        clone_group.instances = [0] * len(archetype)
    start = 0
    file = open('Archetype\Variable_points.txt', "w", encoding='utf-8')
    for i in range(len(archetype)):
        for j in range(len(archetype[i])):
            if j != len(archetype[i]) - 1:
                file.write(group[i][archetype[i][j][1]:archetype[i][j + 1][0]] + '\n')
            CloneGroups[j].instances[i] = (0, start + archetype[i][j][0], start + archetype[i][j][1] - 1)
        start += len(group[i]) + len(delimiter)
        file.write(delimiter[2:len(delimiter) - 1])
    file.close()
    var = clones.VariativeElement(CloneGroups)
    import util
    util.write_variative_report(clones, [var], r'Archetype\archetype.html')



class TestStringMethods(unittest.TestCase):
    def __init__(self, t):
        super().__init__(t)  # what is t here? =)

    def setUp(self):
        return
        """init each test"""
        self.pr = cProfile.Profile()
        self.pr.enable()
        print("\n<<<---")

    def tearDown(self):
        return
        """finish any test"""
        p = Stats(self.pr)
        p.strip_dirs()
        p.sort_stats('cumtime')
        p.print_stats()
        print("\n--->>>")

    def test_001_small_common(self):
        a = archetype_search([
            "Я пошёл позавчера за хлебом",
            "Я пошёл вчера за хлебом",
            "Я пошёл сегодня за хлебом",
            "Я пойду завтра за хлебом"
        ])
        print(a)
        self.assertEqual(
            a,
            [[(0, 4), (7, 8), (17, 27)], [(0, 4), (7, 8), (13, 23)], [(0, 4), (7, 8), (15, 25)], [(0, 4), (7, 8), (14, 24)]],
            "Small common failed"
        )

    def test_002_small_common_lists(self):
        return
        a = archetype_search([
            ["Я", "пошёл", "позавчера", "за", "хлебом"],
            ["Я", "пошёл", "вчера", "за", "хлебом"],
            ["Я", "пошёл", "сегодня", "за", "хлебом"],
            ["Я", "пойду", "завтра", "за", "хлебом"]
        ])
        print(a)

    def test_003_perm_order(self):
        self.assertEqual(
            [(2, 3, 4, 0, 1), (1, 3, 4, 0, 2), (0, 3, 4, 1, 2), (1, 2, 4, 0, 3), (0, 2, 4, 1, 3), (0, 1, 4, 2, 3),
             (1, 2, 3, 0, 4), (0, 2, 3, 1, 4), (0, 1, 3, 2, 4), (0, 1, 2, 3, 4)],
            list(permutations_first_volatile(5))
        )

    def test_004_two_tuples_lcs(self):
        w1 = ("ab", "xx", "cd",       "ee", "ff", "gh", "ij", "kl")
        w2 = ("ab",       "34", "yy", "ee", "ff", "78", "ij", "kl")
        self.assertEqual(
            two_tuples_lcs(w1, w2),
            ('ab', 'ee', 'ff', 'ij', 'kl')
        )

    def test_004_best_n_tuples_lcs(self):
        w1 = ("ab", "xx", "cd",       "ee", "ff", "gh", "ij", "kl")
        w2 = ("ab",       "34", "yy", "ee", "ff", "78", "ij", "kl")
        w3 = ("ab", "xx", "34", "yy", "ee", "**", "78", "ij", "kl")
        self.assertEqual(
            best_n_tuples_lcs((w1, w2, w3)),
            ('ab', 'ee', 'ij', 'kl')
        )


if __name__ == '__main__':
    unittest.main()
    # raise Exception("This is not an entry point")
