#! /usr/bin/python3

import random

# fasta_chars = "ANDRCGQEHILKMFPSTYWV"

codec = {
    "A": (0, 0, 0, 0, 0),
    "N": (0, 0, 0, 0, 1),
    "D": (0, 0, 0, 1, 0),
    "R": (0, 0, 0, 1, 1),
    "C": (0, 0, 1, 0, 0),
    "G": (0, 0, 1, 0, 1),
    "Q": (0, 0, 1, 1, 0),
    "E": (0, 0, 1, 1, 1),
    "H": (0, 1, 0, 0, 0),
    "I": (0, 1, 0, 0, 1),
    "L": (0, 1, 0, 1, 0),
    "K": (0, 1, 0, 1, 1),
    "M": (0, 1, 1, 0, 0),
    "F": (0, 1, 1, 0, 1),
    "P": (0, 1, 1, 1, 0),
    "S": (0, 1, 1, 1, 1),
    "T": (1, 0, 0, 0, 0),
    "Y": (1, 0, 0, 1, 0),
    "W": (1, 0, 0, 0, 1),
    "V": (1, 0, 0, 1, 1)
}

def get_fchar_for_code(code):
    for fc in codec:
        if codec[fc] == code:
            return fc

        return None

def get_fstr_for_codes(codeseq):
    if len(codeseq) % 5 != 0:
        raise Exception("codeseq must be a multiple of code width (which is 5)")

    res = list()
    for i in range(len(codeseq) // 5):
        cur_code = tuple( codeseq[i * 5 : (i+1) * 5] )

        cur_fchar = get_fchar_for_code(cur_code)
        if cur_fchar is not None:
            res.append(cur_fchar)
        else:
            res.append("-")

    return "".join(res)

#class _FastaCodeIterator:
#    def __init__(self, fasta_string, window):
#        if len(fasta_string) < window:
#            raise Exception("fasta_string must be long enough to form at least 1 window")
#
#        self.fasta_string = fasta_string
#        self.window = window
#
#        self.i = 0
#
#    def __next__(self):
#        if self.i > len(self.fasta_string) - self.window:
#            raise StopIteration
#
#        code = list()
#        for w in range(self.window):
#            c = self.fasta_string[self.i + w]
#            if c not in codec:
#                raise Exception("fasta string contained character not in codec")
#
#            for num in codec[c]:
#                code.append(num)
#
#        self.i += 1
#
#        return code

def get_code_iterator(fasta_string, window):
    for i in range( (len(fasta_string) - window) + 1):
        res = list()
        for w in range(window):
            c = fasta_string[i + w]
            if c not in codec:
                raise Exception("non-FASTA character in fasta string")

            for e in codec[c]:
                res.append(e)

        yield res

class FastaParser:
    def __init__(self):
        self.records = []

    def add_from_stream(self, fstream):
        last_record = ""
        for line in fstream:
            line.strip()

            if len(line) < 1:
                continue

            if line[0] == '>' or line[0] == ';':
                # store record if there is one
                if len(last_record) > 0:
                    self.records.append( last_record )
                    last_record = ""
                continue

            for char in line:
                if char in codec:
                    last_record += char

        if len(last_record) > 0:
            self.records.append( last_record )

    def add_from_file(self, filename):
        with open(filename, "r") as ifile:
            self.add_from_stream(ifile)

    def clear(self):
        self.records.clear()

#    def get_fasta_iterator(self, window):
#       fstring = random.choice(self.records)
#
#       return _FastaCodeIterator(fstring, window)
    
    def get_random_record(self):
        return random.choice(self.records)

    def get_iter_for_random_record(self, window):
        return get_code_iterator(random.choice(self.records), window)

