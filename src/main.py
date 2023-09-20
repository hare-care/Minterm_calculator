from tabulate import tabulate


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
        for i in range(len(self.array)-1, -1, -1):
            min_str = min_str + str(self.array[i])
        return min_str
    

    def __repr__(self):
        return str(self)


def create_minterm_list(number_list, size):
    min_list = []
    for number in number_list:
        min_list.append(minterm(number, size))
    return min_list

def create_primes_list(primes_list, size):
    prime_list = []
    for prime in primes_list:
        prime_list.append(minterm(prime, size, 'arr'))
    return prime_list

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


minterm_list = [minterm(0,4), minterm(4,4), minterm(5,4), minterm(6,4), 
                minterm(7,4), minterm(8,4), minterm(9,4), minterm(10,4), 
                minterm(13,4), minterm(15,4)]

# implication table object
class implication_table:
    def __init__(self, minterms, print_steps=False):
        self.n_columns = 1
        self.size = minterms[0].size + 1
        self.columns = [group_minterms(minterms)]
        self.print_steps_flag = print_steps
        if self.print_steps_flag: print(self)

    def print_steps(self, bool=True):
        self.print_steps_flag = bool

    def add_column(self, new_minterm_list):
        self.n_columns = self.n_columns + 1
        self.columns.append(group_minterms(new_minterm_list))
        if self.print_steps_flag: print(self)

    def check_minterm(self, column_num):
        column = self.columns[column_num]
        min_size = self.size - 1
        new_minterms = []
        for i in range(self.size - 1):
            for term in column[i]:
                for adj_term in column[i+1]:
                    dif = 0
                    dif_loc = 0
                    for j in range(min_size):
                        if term.array[j] != adj_term.array[j]:
                            if term.array[j] == '-' or adj_term.array[j] == '-':
                                dif = 0
                                break
                            dif = dif + 1
                            if dif_loc > 1:
                                break
                            dif_loc = j
                    if dif == 1:
                        new_minterms.append(term.add_dc(dif_loc))
                        term.reduced_flag = 1
                        adj_term.reduced_flag = 1
        return new_minterms
    
    def minimize_table(self):
        # next_col = self.check_minterm(0)
        # add_col with new minterms
        # repeat until the new minterms is empty list
        next_column = []
        done = 0
        column_num = 0
        prime_imps = []
        if self.print_steps_flag: print(self)
        while not done:
            next_column = self.check_minterm(column_num)
            if next_column == []:
                done = 1
                continue
            self.add_column(next_column)
            column_num = column_num + 1
        for col in self.columns:
            for group in col:
                for term in group:
                    if not term.reduced_flag:
                        prime_imps.append(term)
    def __str__(self):
        table_str = ''
        for i, column in enumerate(self.columns):
            table_str = table_str + str(column) + "\n"
        return "Implication Table\n" + tabulate(self.columns, showindex=True, tablefmt="simple_grid") + "\n" # table_s
    
    def __repr__(self) -> str:
        return str(self)


def create_matrix(prime_imps, minterms):
    array = []
    size = minterms[0].size
    for i, term in enumerate(minterms):
        array.append([])
        for k, prime in enumerate(prime_imps):
            mismatch = 0
            for j in range(size):
                if term.array[j] != prime.array[j] and prime.array[j] != '-':
                    mismatch = 1
            if mismatch == 0:
                array[i].append(1)
            else:
                array[i].append('')
    return array

mins_list = [minterm(0, 3), minterm(2, 3), minterm(3,3), minterm(7, 3), minterm(4, 3)]
primes_list = [minterm(['-', 1, 0], 3, 'arr'), minterm([0, '-', 0], 3, 'arr'), 
               minterm([0, 0, '-'], 3, 'arr'), minterm([1, 1, '-'], 3, 'arr')]



# impl_table = implication_table(mins_list)
# impl_table.print_steps()
# impl_table.minimize_table()


class min_cover_matrix:
    def __init__(self, prime_imps, minterms, print_steps=False):
        self.num_cols = len(prime_imps)
        self.num_rows = len(minterms)
        self.matrix = create_matrix(prime_imps, minterms)
        self.essential_primes = []
        self.primes = prime_imps[:]
        self.mins = minterms[:]
        self.empty = 0
        self.no_operation_cnt = 0
        self.print_steps_flag = print_steps
        if self.print_steps_flag: print(self)

    def remove_row(self, index):
        self.matrix.pop(index)
        self.mins.pop(index)
        self.num_rows = self.num_rows - 1
        self.no_operation_cnt = 0
        if self.num_rows == 0:
            self.empty = 1
        if self.print_steps_flag: print(self)
    
    def print_steps(self, bool=True):
        self.print_steps_flag=bool
    
    def remove_column(self, index):
        for i in range(self.num_rows):
            self.matrix[i].pop(index)
        self.primes.pop(index)
        self.num_cols = self.num_cols - 1
        self.no_operation_cnt = 0
        if self.num_cols == 0:
            self.empty = 1
        if self.print_steps_flag: print(self)
    
    def find_essential_primes(self):
        times_covered = 0
        return_val = 0
        prime_index = 0
        min_index = 0
        j = 0
        if self.print_steps_flag: print(self)
        if self.empty: return
        while j < self.num_rows:
            times_covered = 0
            row = self.matrix[j]
            for i, col in enumerate(row):
                if col == 1:
                    times_covered = times_covered + 1
                    prime_index = i
                    min_index = j
            if times_covered == 1:
                return_val = return_val + 1
                offset = self.add_prime(prime_index)

                j = j - offset
                if j < 0: j = -1
            j = j + 1

    def add_prime(self, index):
        self.essential_primes.append(self.primes[index])
        i = 0
        rows_removed = 0
        while i < self.num_rows:
            if self.matrix[i][index] == 1:
                self.remove_row(i)
                rows_removed = rows_removed + 1
                i = i - 1
            i = i + 1
        self.remove_column(index)
        return rows_removed
    
    def eliminate_dom_rows(self):
        i = 0
        i_dominances = 0
        j_dominances = 0
        if self.num_rows == 1: return
        while i < self.num_rows:
            row_i = self.matrix[i]
            j = i + 1
            while j < self.num_rows:
                row_j = self.matrix[j]
                i_dominances = 0
                j_dominances = 0
                for k,col_i in enumerate(row_i):
                    col_j = row_j[k]
                    if col_i != col_j:
                        if col_j == 1:
                            j_dominances = j_dominances + 1
                        else:
                            i_dominances = i_dominances + 1
                if j_dominances > 0 and i_dominances == 0:
                    self.remove_row(j)
                    j = j - 1
                elif i_dominances > 0 and j_dominances == 0:
                    self.remove_row(i)
                    break
                j = j + 1
            i = i + 1

    def eliminate_non_dom_cols(self):
        i = 0
        i_dominances = 0
        j_dominances = 0
        if self.num_cols == 1: return
        while i < self.num_cols:
            j = i + 1
            while j < self.num_cols:
                i_dominances = 0
                j_dominances = 0
                for k in range(self.num_rows):
                    row_i = self.matrix[k][i]
                    row_j = self.matrix[k][j]
                    if row_j != row_i:
                        if row_j == 1:
                            j_dominances = j_dominances + 1
                        else:
                            i_dominances = i_dominances + 1
                if j_dominances > 0 and i_dominances == 0:
                    self.remove_column(i)
                    break
                elif i_dominances > 0 and j_dominances == 0:
                    self.remove_column(j)
                    j = j - 1
                j = j + 1
            i = i + 1

    def minimize_matrix(self):
        while self.no_operation_cnt < 3:
            self.no_operation_cnt = self.no_operation_cnt + 1
            self.find_essential_primes()
            self.eliminate_dom_rows()
            self.eliminate_non_dom_cols()
        if self.empty:
            print("good job")
            print(self.essential_primes)
        else:
            print("cyclic core")
            print(self.essential_primes)
            print(self.matrix)



    def __str__(self):
        return "Minimum Cover Matrix\n" + tabulate(self.matrix, headers=self.primes, showindex=self.mins, tablefmt="simple_grid") + "\n"

# test_mat = min_cover_matrix(primes_list, mins_list)
# test_mat.print_steps()

# test_mat.find_essential_primes()

row_primes = [minterm(['-','-', 0], 3, 'arr'), minterm([1,0,'-'], 3, 'arr'), minterm(['-',1,0], 3, 'arr')]
row_mins = [minterm(0, 3), minterm(1,3), minterm(2,3)]


test_row_dom = min_cover_matrix(row_primes, row_mins)
# test_row_dom.print_steps()
test_row_dom.minimize_matrix()









        




