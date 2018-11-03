import alert
import configparser
from datetime import datetime, timedelta
import getopt
import sys
import time

def wait(minutes):
    seconds = minutes * 60
    time.sleep(seconds)

# Produces from string the longest substring 
# that starts at index and is an integer
def get_contiguous_number(string, index):
    length = len(string)
    end = length
    while end > index:
        substring = string[index:end]
        if substring.isdigit():
            return substring
        end -= 1

    return ''

# Parses a timing pattern and returns a list of (char, int) tuples
# where the char is either 'w' for work or 'b' for break
def parse_pattern(raw_pattern):
    pattern = raw_pattern.replace(' ', '')
    length = len(pattern)
    index = 0
    output = []
    while index < length:
        next_char = pattern[index]
        if next_char == 'w' or next_char == 'b':
            # work period
            num_str = get_contiguous_number(pattern, index + 1)
            if len(num_str) == 0:
                raise ValueError(
                    'No number found after char {} at index {} in pattern {}'.format(
                        next_char,
                        index,
                        raw_pattern
                    )   
                )
            time = int(num_str)
            output.append((next_char, time))
            index += len(num_str) + 1
        else:
            raise ValueError(
                'Unexpected char {} at index {} in pattern {}'.format(
                    next_char,
                    index,
                    raw_pattern
                )
            )
    return output

# Cleans up a parsed timing pattern in the [('w'|'b', time)*] format
# Return type is the same
def clean_pattern(pattern):
    length = len(pattern)
    if length == 0 or length == 1:
        return pattern

    output = []

    last_type, last_time = pattern[0]
    for i in range(1, length):
        current_type, current_time = pattern[i]
        if current_type == last_type:
            last_time += current_time
        else:
            output.append((last_type, last_time))
            last_type = current_type
            last_time = current_time
    output.append((last_type, last_time))

    return output

def main():
    args = sys.argv[1:]
    options = 'ne:p:' # empty string to only accept long options
    long_options = [
        'no-email',
        'email-conf=',
        'pattern='
    ]

    config_vals = {
        'conf_path': 'email.conf',
        'pattern': None,
        'no-email': False
    }

    try:
        opt_vals, args = getopt.getopt(args, options, long_options)
    except getopt.GetoptError as err:
        print('Encountered option error!')
        print(str(err))
        sys.exit()

    #print(opt_vals)
    for opt, arg in opt_vals:
        if opt == '--no-email' or opt == '-n':
            config_vals['no-email'] = True
        if opt == '--email-conf' or opt == '-e':
            config_vals['conf_path'] = arg
        if opt == '--pattern' or opt == '-p':
            config_vals['pattern'] = arg

    if config_vals['pattern'] is None:
        print('Pymodoro requires a pattern!')
        sys.exit()

    try:
        parsed_pattern = parse_pattern(config_vals['pattern'])
        cleaned_pattern = clean_pattern(parsed_pattern)
    except Exception as err:
        print("Could not parse pattern!")
        print(str(err))
        sys.exit()

    conf_parser = configparser.ConfigParser()

    conf_path = r'email.conf'
    conf_parser.read(conf_path)

    from_address = conf_parser.get('email', 'fromAddress')
    to_address = conf_parser.get('email', 'toAddress')
    login = conf_parser.get('email', 'login')
    password = conf_parser.get('email', 'password')
    server = conf_parser.get('email', 'smtpserver')
    subject = 'Pymodoro Alert!'

    for task, duration in cleaned_pattern:
        task_string = ''
        if task == 'b':
            task_string = 'break period'
        elif task == 'w':
            task_string = 'work period'

        time = datetime.now()
        time_str = time.strftime('%H:%M')
        endtime = time + timedelta(minutes=duration)
        endtime_str = endtime.strftime('%H:%M')

        print('[{}] Beginning {} minute {} until {}!'.format(time_str, duration, task_string, endtime_str))
        wait(duration)
        time_str = datetime.now().strftime('%H:%M')
        print('[{}] Completed {}!'.format(time_str, task_string))
        alert.sendemail(
            from_addr = from_address,
            to_addr_list = [to_address],
            subject = subject,
            message = 'Your {} is complete!'.format(task_string),
            login = login,
            password = password,
            smtpserver = server
        )



if __name__ == '__main__':
    main()
