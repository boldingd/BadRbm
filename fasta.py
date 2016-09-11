#! /usr/bin/python3

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

class FastaFile:
    def __init__(self):
        self.records = []

    def add_from_stream(self, fstream):
        last_record = ""
        for line in file:
            line.strip()

            if len(line) < 1:
                continue

            if line[0] == '>' or line[0] == ';'
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
        

