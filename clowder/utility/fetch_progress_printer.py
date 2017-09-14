"""Fetch progress printer"""
from git import RemoteProgress

class FetchProgressPrinter(RemoteProgress):
    """Handler for printing git fetch progress"""
    def __init__(self):
        super().__init__()
        self.previous_op_mask = None

    def update(self, op_code, cur_count, max_count=None, message=''):
        # op_id = op_code & self.OP_MASK
        # print('BEGIN = ' + str(self.BEGIN))
        # print('END = ' + str(self.END))
        # print('OP_MASK = ' + str(self.OP_MASK))
        if self.previous_op_mask != self.OP_MASK:
            self.previous_op_mask = self.OP_MASK
            if op_code & self.BEGIN > 0 and op_code & self.END > 0:
                # One line output
                # print('NEQ ONE LINE')
                print(self._cur_line)
            elif op_code & self.BEGIN > 0:
                # New line output
                # print('NEQ BEGIN')
                print(self._cur_line, sep=' ', end='')
                # print('\n\n')
                # print_progress_bar(cur_count, max_count,
                #                    prefix='NEQ BEGIN     - ',
                #                    suffix='Complete', length=50)
            elif op_code & self.END > 0:
                # End line output
                # print('NEQ END')
                print(self._cur_line, sep=' ', end='', flush=True)
                # print_progress_bar(cur_count, max_count,
                #                    prefix='NEQ END     - ',
                #                    suffix='Complete', length=50)
                # print(self._cur_line)
            else:
                # Continue output
                # print('NEQ CONTINUE ')
                print(self._cur_line, sep=' ', end='', flush=True)
                # print_progress_bar(cur_count, max_count,
                #                    prefix='NEQ CONTINUE     - ',
                #                    suffix='Complete', length=50)
        else:
            if op_code & self.BEGIN > 0 and op_code & self.END > 0:
                # One line output
                # print('EQ ONE LINE')
                print(self._cur_line)
            elif op_code & self.BEGIN > 0:
                # New line output
                # print('EQ BEGIN')
                print(self._cur_line, sep=' ', end='')
                # print('\n\n')
                # print_progress_bar(cur_count, max_count,
                #                    prefix='EQ BEGIN     - ',
                #                    suffix='Complete', length=50)
            elif op_code & self.END > 0:
                # End line output
                # print('EQ END')
                print(self._cur_line, sep=' ', end='', flush=True)
                # print_progress_bar(cur_count, max_count,
                #                    prefix='EQ END     - ',
                #                    suffix='Complete', length=50)
                # print(self._cur_line)
            else:
                # Continue output
                # print('EQ CONTINUE ')
                print(self._cur_line, sep=' ', end='', flush=True)
                # print_progress_bar(cur_count, max_count,
                #                    prefix='EQ CONTINUE     - ',
                #                    suffix='Complete', length=50)
        # print(op_code, cur_count, max_count or 'UNKNOWN',
        #       cur_count / (max_count or 100.0))
        # print(self._cur_line)
        # print()

# Disable errors shown by pylint for too many arguments
# pylint: disable=R0913

def print_progress_bar(iteration, total, prefix='', suffix='',
                       decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    progress_bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, progress_bar, percent, suffix), end = '\r')
    # # Print New Line on Complete
    # if iteration == total:
    #     print()
