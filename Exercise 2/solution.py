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


