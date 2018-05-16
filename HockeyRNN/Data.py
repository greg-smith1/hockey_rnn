


SOS_token = 0
EOS_token = 1


class Data:
    def __init__(self, name):
        self.name = name
        self.value_index = {}
        self.value_count = {}
        self.index_to_values = {0: "SOS", 1: "EOS"}
        self.n_values = 2

    def addSequence(self, sequence):
        for val in sequence.split(' '):
            self.addValue(val)

    def addValue(self, value):
        if word not in self.value2index:
            self.value_index[value] = self.n_values
            self.value_count[value] = 1
            self.index_to_values[self.n_values] = value
            self.n_values += 1
        else:
            self.value_count[value] += 1

    def read_lines(self, data):
        pass

    def filter_pairs(self, input):
        pass

