#! python2
import random, datetime, time, sys, os
from os import path

N = 10
PATTERN = 2
MEM_TIME = 5
N_TESTS = 10
is_noise_test = False
exclusion = ['0', 'O', '1', 'I', 'L', 'U', 'V']


def get_list_of_chars():
    lst = list(range(48, 48+10))
    lst.extend(range(65, 65+26))
    ret = [chr(c) for c in lst]
    for ch in exclusion:
        ret.remove(ch)
    return ret


LIST_OF_CHARS = get_list_of_chars()


def response_test(N):
    global fileObj
    rand_list = get_rand_list(N)
    rand_str = ' '.join(str(n) for n in rand_list)
    os.system('cls')
    print('You will have ' + str(MEM_TIME) + ' secs to memorize the following string:')
    print('*'*78)
    sys.stdout.write(rand_str)
    sys.stdout.flush()
    time.sleep(MEM_TIME)
    # sys.stdout.write("\b"*len(rand_str))
    os.system('cls')
    fileObj.write(''.join(str(n) for n in rand_list))
    fileObj.write(',')
    fileObj.write(str(MEM_TIME))
    fileObj.write(',')  

    get_response(N)
    
def get_rand_list(N):
    # rand_list = [random.randint(0,9) for n in range(N)]

    # rand_list = []
    # for i in range (N):
    #     rand_num = random.randint(0,9)
    #     while (rand_num in rand_list[-PATTERN:]):
    #         rand_num = random.randint(0,9)

    #     rand_list.append(rand_num)
    #     prev_num = rand_num

    #rand_list = [LIST_OF_CHARS[random.randint(0,len(LIST_OF_CHARS)-1)] for n in range(N)]
    
    rand_list = []
    for i in range(N):
        rand_char = LIST_OF_CHARS[random.randint(0,len(LIST_OF_CHARS)-1)]
        while (rand_char in rand_list[-PATTERN:]):
            rand_char = LIST_OF_CHARS[random.randint(0,len(LIST_OF_CHARS)-1)]
            
        rand_list.append(rand_char)

    return rand_list

def get_response(N):
    global fileObj
    start = time.time()
    input_str = raw_input('Recall and enter the string you just saw. You do not need to type the spaces. You can type letters in either capital or lower case. Press enter to submit.\nAnswer:\t')
    end = time.time()
    fileObj.write(input_str)
    fileObj.write(',')
    # response_nums = process_response_nums(input_str)
    # fileObj.write(''.join(str(n) for n in response_nums))
    fileObj.write("".join(process_response_alphanums(input_str)))
    fileObj.write(',')
    fileObj.write(''.join(str(end-start)))
    fileObj.write(',')

    if is_noise_test:
        fileObj.write('True')
    else:
        fileObj.write('False')

    fileObj.write('\n')
    print("Your response:")
    print_response(input_str)
    print("Recorded in "+filename)


def print_response(s):
    for ch in s:
        if ch.isalpha():
            sys.stdout.write(ch.upper())
        else:
            sys.stdout.write(ch)
        sys.stdout.write(' ')
    sys.stdout.write('\n')


def process_response_nums(input_str):
    response_nums = []
    for s in input_str:
        if (s.isdigit()):
            response_nums.append(int(s))
        if (len(response_nums) == N):
            return response_nums
    return response_nums

def process_response_alphanums(input_str):
    response = []
    for s in input_str:
        if (s.isdigit()):
            response.append(s)
        elif (s.isalpha()):
            response.append(s.upper())
        if (len(response) == N):
            return response
    return response


def get_yes_no(prompt):
    s = raw_input(prompt).lower()
    if len(s) > 0:
        return s[0] == "y"
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[len(sys.argv)-1] == "noNoise":
            is_noise_test = False
        elif sys.argv[len(sys.argv)-1] == "noise":
            is_noise_test = True
        else:
            print("Invalid arguments provided: ")
            print(sys.argv)
            is_noise_test = get_yes_no("Is this test done with noise?(y/n): ")
    else:
        try:
            tmpFile = open("noise.tmp", "r")
            tmpFileContent = tmpFile.read().lower().strip()
            if tmpFileContent == "true":
                is_noise_test = True
            elif tmpFileContent == "false":
                is_noise_test = False
            else:
                print("Could not parse temporary file content: {}".format(tmpFileContent))
                is_noise_test = get_yes_no("Is this test done with noise?(y/n): ")
        except FileNotFoundError:
            print("Please provide the following information: ")
            is_noise_test = get_yes_no("Is this test done with noise?(y/n): ")

    if is_noise_test:
        filenameFormatStr = "test_Noise_%Y_%m_%d_%H_%M_%S.csv"
    else:
        filenameFormatStr = "test_NoNoise_%Y_%m_%d_%H_%M_%S.csv"

    filename = datetime.datetime.now().strftime(filenameFormatStr)
    try:
        fileObj = open(filename, 'w')
    except PermissionError:
        fullFilepath = path.join(path.abspath(path.dirname(__file__)), filename)
        fileObj = open(fullFilepath, 'w')
    fileObj.write('prompt_numbers,memorization_time,entered_string,processed_string,reaction_time,noise\n')
    print('There will be '+str(N_TESTS)+' tests; during each test you will be given '+str(MEM_TIME)+' seconds to memorize the string.')
    print('Note: You do not need to type the spaces. You can type letters in either capital or lower case.')
    for i in range(N_TESTS):
        print("\nTest {} of {}:".format(i+1, N_TESTS))
        raw_input("Press enter to start")
        response_test(N)
    fileObj.close()
