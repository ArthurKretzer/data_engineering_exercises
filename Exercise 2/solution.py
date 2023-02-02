# %% [markdown]
# # API access exercise
# 
# This script tests API requests for currency quotations and also exception handling using backoff as a function decorator

# %%
import requests
import json

# %%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
ret = requests.get(url)

# %%
if ret:
    print(f"Requisição concluída com código {ret}")
    print(ret.text)
else:
    print(f"Requisição falhou! Código {ret}")

# %%
json.loads(ret.text)

# %%
def quote(value:float, pair:str):
    '''
        Converts a value in currency 1 to the currency 2 on the pair.
        :param value: Value in currency 1 to be converted
        :param pair: String containing a pair. Ex: USD-BRL (currency1-currency2)
    '''
    url = f'https://economia.awesomeapi.com.br/json/last/{pair}'
    ret = requests.get(url)
    currency_1 = json.loads(ret.text)[f'{pair.replace("-", "")}']
    print(f"{value} {pair[:3]} costs {float(currency_1['bid']) * value} {pair[4:]} today")

# %%
quote(20, 'USD-BRL')

# %%
quote(20, 'JPY-BRL')

# %%
quote(20, 'Arthur')

# %% [markdown]
# You can treat exceptions

# %%
try:
    quote(20, 'Arthur')
except Exception as e:
    print(e)
else:
    print("OK")

# %%
list_currencies_pairs = [
    "USD-BRL",
    "EUR-BRL",
    "BTC-BRL",
    "CRE-BRL" # republican credits to BRL
]

# %%
for currency_pair in list_currencies_pairs:
    try:
        quote(20, currency_pair)
    except:
        print(f"Failed to get pair: {currency_pair}")

# %%
def multi_quote(value:float, pair_list:list):
    '''
        Converts a value in currency 1 to the currency 2 on the pair.
        :param value: Value in currency 1 to be converted
        :param pair_list: List of strings containing pairs. Ex: ["USD-BRL","EUR-BRL","BTC-BRL"] (currency1-currency2)
    '''
    for currency_pair in pair_list:
        try:
            quote(value, currency_pair)
        except:
            print(f"Failed to get pair: {currency_pair}")

# %%
multi_quote(20, list_currencies_pairs)

# %% [markdown]
# Creating a decorator for error check

# %%
def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

# %%
@error_check
def quote(value:float, pair:str):
    '''
        Converts a value in currency 1 to the currency 2 on the pair.
        :param value: Value in currency 1 to be converted
        :param pair: String containing a pair. Ex: USD-BRL (currency1-currency2)
    '''
    url = f'https://economia.awesomeapi.com.br/json/last/{pair}'
    ret = requests.get(url)
    currency_1 = json.loads(ret.text)[f'{pair.replace("-", "")}']
    print(f"{value} {pair[:3]} costs {float(currency_1['bid']) * value} {pair[4:]} today")

# %%
def multi_quote(value:float, pair_list:list):
    '''
        Converts a value in currency 1 to the currency 2 on the pair.
        :param value: Value in currency 1 to be converted
        :param pair_list: List of strings containing pairs. Ex: ["USD-BRL","EUR-BRL","BTC-BRL"] (currency1-currency2)
    '''
    for currency_pair in pair_list:
        quote(value, currency_pair)

# %%
multi_quote(20, list_currencies_pairs)

# %% [markdown]
# Creating a decorator for treating several error could be time consuming. Module backoff has some helpful functions

# %%
import backoff

# %% [markdown]
# An example here is to demonstrate the usage of a backoff decorator

# %%
import random

#This receives a delay between tries, expo defines an exponential delay, then a list of exception triggers for backoff, then maximum tryouts.
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f'''
        RND: {rnd}
        args: {args if args else "no args"}
        kargs: {kargs if kargs else "no kargs"}
    ''')

    if rnd < .2:
        raise ConnectionAbortedError('Connection terminated.')
    if rnd < .4:
        raise ConnectionRefusedError('Connection refused.')
    if rnd < .6:
        raise TimeoutError('Connection timeout.')
    else:
        return "OK!"

# %%
test_func()

# %%
test_func(10, name="testing")

# %%
import logging

# %% [markdown]
# Creates a logger with level DEBUG and a formatter for the logging message

# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# %% [markdown]
# Now creates a stream handler for the logging messages using the declared formatter and sets it as the log handler

# %%
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %% [markdown]
# Now we can use it instead of print to give meaningful messages

# %%
import random

#This receives a delay between tries, expo defines an exponential delay, then a list of exception triggers for backoff, then maximum tryouts.
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'no args'}")
    log.info(f"kargs: {kargs if kargs else 'no kargs'}")

    if rnd < .2:
        log.error('Connection terminated.')
        raise ConnectionAbortedError('Connection terminated.')
    if rnd < .4:
        log.error('Connection refused.')
        raise ConnectionRefusedError('Connection refused.')
    if rnd < .6:
        log.error('Connection timeout.')
        raise TimeoutError('Connection timeout.')
    else:
        return "OK!"

# %%
test_func()

# %% [markdown]
# My log formatting.
# 
# This implementation has colors, bold font and also process, thread, timestamp, module and line logging.
# 
# This is also saved on a .log file automatically

# %%
import logging
import os
# Color number definition
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}

# Special function used to ease a message formatting edition


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

# Format log level name color accordinly


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

# Logger class used in all logging operations


class log(logging.Logger):
    # Message format with collors \033[1;35m = Magenta
    FORMAT = '\033[35m%(asctime)s\033[0m [$BOLD%(levelname)-18s$RESET]\033[35m [%(processName)s][%(threadName)s][%(module)s]\033[0m %(message)s - $BOLDLine:%(lineno)d$RESET'
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name='my_logger'):
        # Create logger with debug level
        logging.Logger.__init__(self, name, logging.DEBUG)

        # create console handler and set level to debug
        if not self.handlers:
            color_formatter = ColoredFormatter(self.COLOR_FORMAT)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # add formatter to ch
            ch.setFormatter(color_formatter)
            # add ch to logger
            self.addHandler(ch)

            log_file = logging.FileHandler(
                filename=os.getcwd()+f'/logs/{name}.log', mode='w+', encoding='utf8')
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)-18s][%(processName)s][%(threadName)s][%(module)s] %(message)s - %(lineno)d')
            log_file.setFormatter(formatter)
            log_file.setLevel(logging.DEBUG)
            self.addHandler(log_file)


# %%
log = log('my_log')

# %%
test_func()

# %%



