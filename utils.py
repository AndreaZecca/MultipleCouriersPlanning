import os
import signal
import sys
import time

import multiprocessing as mp

class DoneException(Exception):
    pass

def run_with_timeout(f, seconds_before_timeout, *args, **kwargs):
    def sig_usr1_handler(signum, frame):
        raise DoneException

    parent_pid = os.getpid()

    queue = mp.Queue()

    new_pid = os.fork()
    if new_pid == 0:
        def add_result(result):
            queue.put(result)
        final_output = f(add_result, *args, **kwargs)
        queue.put(final_output)
        
        os.kill(parent_pid, signal.SIGUSR1)
        sys.exit(0)
    else:
        old_handler = signal.signal(signal.SIGUSR1, sig_usr1_handler)

        try:
            time.sleep(seconds_before_timeout)
            os.kill(new_pid, signal.SIGKILL)
            completed = False
        except DoneException:
            # we receive a KeyboardInterrupt when the child process is done
            completed = True
        finally:
            signal.signal(signal.SIGUSR1, old_handler)
            time.sleep(1)
            result = None
            while not queue.empty():
                result = queue.get()

            if result is None:
                return None
            if result == "unsat":
                return "unsat"
            else:
                # The result might already contain whether it's optimal
                if isinstance(result, tuple):
                    return result[0], result[1] and completed
                return result, completed

