# %% [markdown]
# This script shows how to make an URL request and extract data fast using pandas

# %%
import requests
import pandas as pd
import collections

#url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil'
# url = sys.argv[1]

# %% [markdown]
# The module requests gets the http response from the link, to get the information you use the atribute "text"

# %%
# verify=False should only be used for testing. This does not verify the SSL ceritificate of the URL.
# This was made to avoid requests.exceptions.SSLError problem on caixa website.
r = requests.get(url, verify=False)

# %%
r.text
r_text = r.text

# %% [markdown]
# The text came with lots of end of carriage and new line strings. This should be removed.

# %%
r_text = r.text.replace('\\r\\n', '').replace('"\r\n}', '').replace('{\r\n "html": "', '')

# %% [markdown]
# Now you need to convert it to a dataframe

# %%
df = pd.read_html(r_text)

# %% [markdown]
# Note: This function returns a list of dataframes if more things are found. So we need to extract the only dataframe available in this list.

# %%
type(df)
type(df[0])

df=df[0].copy()

# %%
df

# %% [markdown]
# Several NaN values appeared caused by bad website formatting that causes null lines to be generated. To clear it you can simply filter these values.

# %%
df = df[df['Bola1'] == df['Bola1']]
df

# %% [markdown]
# You can check if it is correct matching the number of rows and the last Concurso value. If they are the same, everything is correct.

# %% [markdown]
# Now we are interested in quantifying how many times an even, odd and prime number are drawn. So for each we create a list containing all even, odd and primes in range 1 to 25.

# %%
# List of all possible numbers.
possible_numbers = list(range(1, 26))

# These three functions are created to apply a filter to the list containing all possible numbers.
def is_even(number):
    if (number % 2) == 0:
        return True
    else:
        return False

def is_odd(number):
    if (number % 2) != 0:
        return True
    else:
        return False

def is_prime(number):
    for i in range(2, number):
        if (number % i) == 0:
            return False
        else:
            pass
    return True

# Then filter is used to create three lists containing even, odd and prime numbers.
even_numbers = list(filter(is_even, possible_numbers))
odd_numbers = list(filter(is_odd, possible_numbers))
prime_numbers = list(filter(is_prime, possible_numbers))

# %% [markdown]
# We create a list containing the columns to be evaluated.

# %%
number_columns = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
              'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12',
              'Bola13', 'Bola14', 'Bola15']

# %% [markdown]
# Finally the values from column 'Bola 1' to 'Bola25' are considered floats, but should be integers.

# %%
df[number_columns] = df[number_columns].astype(int)

# %% [markdown]
# Now we iterate over every column to sum the frequency of unique values, odds, evens and primes.

# %%
comb = []
value_count = dict.fromkeys(possible_numbers, 0)

for column in number_columns:
    # For odds, evens and primes we apply filter functions and sum the total amount for each column
    # Then we create a string containing the combination of the sums as a unique string and append it to a list
    comb.append(str(df[column].apply(is_even).sum()) + 'even-' + str(df[column].apply(is_odd).sum()) + 'odds-'+str(df[column].apply(is_prime).sum())+'primes')
    # For number counting we apply a value counts to count for each unique value found.
    # Then an iteraction is made to sum every column unique value frequency into a dictionary of possible numbers.
    for key, value in df[column].value_counts().items():
        value_count[key] += value

# %% [markdown]
# Now we can count every equal combination using Counter. The we can create a dataframe from it and calculate the probability of each combination to happen.

# %%
counter = collections.Counter(comb)
result = pd.DataFrame(counter.items(), columns=['Combinacao', 'Frequencia'])
result['p_freq'] = result['Frequencia']/result['Frequencia'].sum()
result = result.sort_values(by='p_freq')

# %% [markdown]
# Finally we can sort the most frequent values

# %%
sorted_value_count = sorted(value_count.items(), key=lambda x:x[1])

# %%
most_frequent_value = sorted_value_count[-1]
least_frequent_value = sorted_value_count[0]

# %%
print(f'''
The most frequent value is: {most_frequent_value[0]}
The least frequent value is: {least_frequent_value[0]}
The most frequent combination of odds, evens and primes is: {result['Combinacao'].values[-1]} or {int((result['p_freq'].values[-1]*100)*100)/100}%
''')


