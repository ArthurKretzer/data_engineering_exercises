# %%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db').connect()

# %%
sql = '''select * from vw_artist;'''

# %%
df_artist = pd.read_sql_query(text(sql), engine)
df_artist

# %%
df_song = pd.read_sql_query(text('select * from vw_song'), engine)
df_song

# %%
sql_insert = '''
insert into tb_artist(
    SELECT "date"
    ,"rank"
    ,artist
    ,song
from public."Billboard" as t1
where t1.artist like 'Nirvana%'
order by t1.artist, t1.song, t1."date"
);
'''

# %%
engine.execute(text(sql_insert))


