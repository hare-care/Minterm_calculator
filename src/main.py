
def num_to_bin_array(num, size):
    """Return an array corresponding to the binary representation of a number.
    Input of desired number and size of array, if the size is larger than necessary bits
    it will be zero padded. If the size is too small the returned array will be cut short."""
    array = []
    bin_num = bin(num)
    count = 0

    # populate the array excluding "0b" with the binary representation
    # index 0 is the LSB
    for i in range(len(bin_num)-1,1, -1):
        array.append(int(bin_num[i]))
        count = count + 1

    # Pad with zeros according to the size given
    while count < size:
        array.append(0)
        count = count + 1
    return array

def scan_num_ones(array):
    """Given a binary array, return the number of 1s in it"""
    count = 0
    for digit in array:
        if (digit):
            count = count + 1
    return count




# minterm object
class minterm:
    def __init__(self, minterm_num, size):
        self.size = size
        self.array = num_to_bin_array(minterm_num, size)
        self.reduced_flag = 0
        self.number = minterm_num
        self.n_ones = scan_num_ones(self.array)

    def __str__(self):
        bin_str = bin(self.number)[2:]
        padding = ''
        for i in range(self.size - len(bin_str)):
            padding = padding + '0'
        return padding + bin_str

    def __repr__(self):
        return str(self)

def group_minterms(minterms):
    """Sort minterms into groups by number of ones in the minterms"""
    size = minterms[0].size
    array = []
    for i in range(size+1):
        array.append([])
    group = 0
    for term in sorted(minterms, key=lambda term:term.n_ones):
        if term.n_ones != group:
            group = group + 1
        array[group].append(term)
    return array



print(group_minterms([minterm(0,4), minterm(1,4), minterm(2,4), minterm(3,4), minterm(7,4), minterm(15,4)]))

# implication table object
class implication_table:
    def __init__(self, minterms):
        self.n_columns = 1
        self.columns = [group_minterms(minterms)]

    def add_column(self):
        self.n_columns = self.n_columns + 1
        self.columns.append([])

    def check_minterm(self):
        pass

        




