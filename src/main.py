
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
        if (digit == 1):
            count = count + 1
    return count




# minterm object
class minterm:
    def __init__(self, minterm_num, size, init_type = 'num'):
        self.size = size
        if init_type == 'num':
            self.array = num_to_bin_array(minterm_num, size)
        elif init_type == 'arr':
            self.array = minterm_num
        self.reduced_flag = 0
        self.number = minterm_num
        self.n_ones = scan_num_ones(self.array)

    def add_dc(self, pos):
        new_arr = self.array[:]
        new_arr[pos] = '-'
        new_min = minterm(new_arr, self.size, 'arr')
        return new_min

    def __str__(self):
        min_str = ''
        for char in self.array:
            min_str = min_str + str(char)
        return min_str
    

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

test = minterm(4,4)
print(minterm(4,4))

minterm_list = [minterm(0,4), minterm(1,4), minterm(2,4), minterm(3,4), minterm(7,4), minterm(15,4)]

print(group_minterms(minterm_list))

# implication table object
class implication_table:
    def __init__(self, minterms):
        self.n_columns = 1
        self.size = minterms[0].size + 1
        self.columns = [group_minterms(minterms)]

    def add_column(self, new_minterm_list):
        self.n_columns = self.n_columns + 1
        self.columns.append(group_minterms(new_minterm_list))

    def check_minterm(self, column_num):
        column = self.columns[column_num]
        min_size = self.size - 1
        new_minterms = []
        for i in range(self.size - 1):
            for term in column[i]:
                for adj_term in column[i+1]:
                    dif = 0
                    dif_loc = 0
                    print(f"term:{term} adj:{adj_term}")
                    for j in range(min_size):
                        print(f"term j:{term.array[j]} adj j:{adj_term.array[j]}")
                        if term.array[j] != adj_term.array[j]:
                            if term.array[j] == '-' or adj_term.array[j] == '-':
                                break
                            dif = dif + 1
                            if dif_loc > 1:
                                break
                            dif_loc = j
                    if dif == 1:
                        print(f"adding dc to pos {dif_loc}")
                        new_minterms.append(term.add_dc(dif_loc))
        return new_minterms
    
    def minimize_table(self):
        # next_col = self.check_minterm(0)
        # add_col with new minterms
        # repeat until the new minterms is empty list
        next_column = []
        done = 0
        column_num = 0
        while not done:
            next_column = self.check_minterm(column_num)
            if next_column == []:
                done = 1
                continue
            self.add_column(next_column)
            column_num = column_num + 1
    def __str__(self):
        table_str = ''
        return 'hello'

        


imp_table = implication_table(minterm_list)
return_list = imp_table.check_minterm(0)
print(return_list)
print(imp_table)







        




