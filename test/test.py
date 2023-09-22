import sys

list_flag = 0
print_pass_flag = 0
test_output_path = sys.argv[1]
correct_output_path = sys.argv[2]

for i in range(len(sys.argv)):
    match sys.argv[i]:
        case "-s": list_flag = 0

        case "-l": list_flag = 1

        case "-p": print_pass_flag = 1

if list_flag:
    1
else:
    test_file = open(test_output_path, 'r')
    correct_file = open(correct_output_path, 'r')
    test_lines = test_file.readlines()
    correct_lines = correct_file.readlines()
    for i, line in enumerate(test_lines):
        if test_lines[i] == correct_lines[i]:
            if print_pass_flag:
                print(f"test PASSED: {test_lines[i][0:-1]} == {correct_lines[i][0:-1]}")
        else:
            print(f"test FAILED: {test_lines[i][0:-1]} != {correct_lines[i][0:-1]}")
    test_file.close()
    correct_file.close()
    





            
