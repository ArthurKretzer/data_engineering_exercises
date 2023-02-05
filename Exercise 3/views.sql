-- gets first time the artist appears in the list by its rank in the billboard and creates a new table
create table tb_web_site as (
with cte_dedup_artist as (
SELECT "date"
	,"rank"
	,artist
    ,row_number() over(partition by artist order by artist, "date") as "dedup"
FROM PUBLIC."Billboard"
order by artist, "date"
    )
SELECT "date"
	,"rank"
	,artist
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from tb_web_site

-- table containing each time an artist was included in the billboard
create table tb_artist as (
SELECT "date"
	,"rank"
	,artist
   ,song
from public."Billboard" as t1
where t1.artist = 'AC/DC'
order by t1.artist, t1.song, t1."date"
)
drop table tb_artist;

select * from tb_artist

-- creates a view for the first time an artist entered the billboard and its rank
create view vw_artist as(
with cte_dedup_artist as (
SELECT "date"
	,"rank"
	,artist
    ,row_number() over(partition by artist order by artist, "date") as "dedup"
FROM tb_artist
order by artist, "date"
    )
SELECT "date"
	,"rank"
	,artist
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from vw_artist

-- inserts elvis and variates into tb_artist
insert into tb_artist(
    SELECT "date"
    ,"rank"
    ,artist
    ,song
from public."Billboard" as t1
-- like searches for similar strings.
-- % is used to consider "anything" before (%string) or after (string%) the string
-- any string starting with Elvis
where t1.artist like 'Elvis%'
order by t1.artist, t1.song, t1."date"
);

-- You can now see how the view has changed
select * from vw_artist;

--  creates a view containing first time a song from an artist from tb_artist entered in bilboard
create view vw_song as(
with cte_dedup_artist as (
SELECT "date"
	,"rank"
	,artist
    ,song
    ,row_number() over(partition by artist, song order by artist, song, "date") as "dedup"
FROM tb_artist
order by artist, song, "date"
    )
SELECT "date"
	,"rank"
	,artist
    ,song
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from vw_song

-- inserts adele and variates into tb_artist
insert into tb_artist(
    SELECT "date"
    ,"rank"
    ,artist
    ,song
from public."Billboard" as t1
where t1.artist like 'Adele%'
order by t1.artist, t1.song, t1."date"
);

select * from vw_artist;
select * from vw_song

-- you can alter a view by replace
create or replace view vw_song as(
with cte_dedup_artist as (
SELECT "date"
	,"rank"
	,artist
    ,song
    ,row_number() over(partition by song order by song, "date") as "dedup"
FROM tb_artist
order by song, "date"
    )
SELECT "date"
	,"rank"
    ,artist
    ,song
from cte_dedup_artist as t1
where t1.dedup = 1
);
select * from vw_song

-- but when you have to change numbe of columns you should drop and create again
drop view vw_song

-- song view without artists
create view vw_song as(
with cte_dedup_artist as (
SELECT "date"
	,"rank"
    ,song
    ,row_number() over(partition by song order by song, "date") as "dedup"
FROM tb_artist
order by song, "date"
    )
SELECT "date"
	,"rank"
    ,song
from cte_dedup_artist as t1
where t1.dedup = 1
);
select * from vw_song