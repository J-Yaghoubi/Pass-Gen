
from itertools import product
import argparse, logging, random, string, time

class PassGenerator:

    """
        Password generator that can be use to create password-list file
    """

    def __init__(self, seq: list, length: int, count:int, prefix: str, path: str, mode= str) -> None:
        """initializing the script"""

        self.seq = seq if seq else string.ascii_letters + string.punctuation + string.digits
        self.length = length
        self.prefix = prefix
        self.count = count
        self.path = path
        self.mode = mode
        self.start = time.perf_counter_ns()

        self._logging_init()
        self._debug_log(msg = 'Script has been initialized and is ready to do his job')
        self.all_mode() if self.mode == 'all' else self.random_mode()

    def _logging_init(self):
        """Initializing logging module"""

        fm = "%(asctime)-20s - %(levelname)-8s : %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=fm, filename='log.txt', \
                                            filemode='a', encoding='utf-8')  

    def _save_to_file(self, data: list):
        """saving data to the file"""

        try:
            with open (self.path, "w") as f:
                f.write("\n".join(map("".join, data)))
                self._debug_log(msg = f'Data has been saved to: {self.path}')

        except Exception:
            logging.error(f'Data has not been saved!')
            exit()

    def _debug_log(self, situation: str = None, msg: str = None) -> None:
        """
            Logging the process
        """
        if not msg:
            if situation == 'start':
                msg = f'{self.mode} mode=> length:{self.length}, seq:{self.seq}, prefix:{self.prefix or "None"}, path:{self.path}'
            else:
                msg = f'Job has been done in: {time.perf_counter_ns() - self.start} nano-secund'
        
        print(msg)
        logging.debug(msg)

    def all_mode(self):
        """
            Generate all possible combination based on user customization
        """
        self._debug_log('start')
        data = [0] * (len(self.seq)**(self.length))
        
        if self.prefix:
            for idx, p in enumerate(product(self.seq, repeat=self.length)):
                data[idx] = self.prefix + ''.join(p)
        else:
            for idx, p in enumerate(product(self.seq, repeat=self.length)):
                data[idx] = ''.join(p)

        self._debug_log('end')
        self._save_to_file(data)    

    def random_mode(self) -> None:
        """
            Generate some random password based on user customization
        """
        self._debug_log('start')

        data = [0] * self.count
        seq = list(self.seq)
        random.shuffle(seq)

        for p in range(self.count):
            password = [0] * self.length
            for l in range(self.length):
                password[l] = random.choice(seq)

            random.shuffle(password)
            data[p] = self.prefix + "".join(password)

        self._debug_log('end')           
        self._save_to_file(data)    


if __name__ == '__main__':

    # CMD 
    parser = argparse.ArgumentParser(description="Create customized pass-list file")

    parser.add_argument("-s", "--sequence", help="characters to use in password generation")
    parser.add_argument("-l", "--length", type=int, default=5, choices=range(1,30), help="the length of password")   
    parser.add_argument("-p", "--prefix", default='', help = "the prefix for using in the password")   
    parser.add_argument("-o", "--output", default='passwords.txt', help="path to save the pass-list")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--all", action="store_true", help="generate all possible definition")
    group.add_argument("-r", "--random", type=int, default=5, help="generate limited random combination")

    args = parser.parse_args()

    # Run Pass-generator    
    mode = 'all' if args.all else 'rnd'
    PassGenerator(args.sequence, args.length, args.random, args.prefix, args.output, mode)
