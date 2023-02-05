-- Verify how many rows it has
select count(*) as quantidade
from public."Billboard"
;

-- Shows first 100 rows
select *
from public."Billboard"
limit 100
;

-- If you state all your columns it is faster than using * since * asks for the database for the list os columns before querying.
select
"date",
"rank",
song,
artist,
"last-week",
"peak-rank",
"weeks-on-board"
from public."Billboard"
limit 100
;

-- you can use poorsql website to format your script
SELECT "date"
	,"rank"
	,song
	,artist
	,"last-week"
	,"peak-rank"
	,"weeks-on-board"
FROM PUBLIC."Billboard" limit 100;

-- gets every chuck berry music
SELECT 
	t1.song
	,t1.artist
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist = 'Chuck Berry'
;

-- counts how many times a music has appeared and groups it
--  by artist and song ordering it descending
SELECT t1.artist
	,t1.song
	,count(*) AS "#song"
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist = 'Chuck Berry'
group by t1.artist, t1.song
order by "#song" desc;

-- You can use lists for comparison
SELECT t1.artist
	,t1.song
	,count(*) AS "#song"
FROM PUBLIC."Billboard" AS t1
WHERE t1.artist in ('Chuck Berry','Frankie Vaughan')
group by t1.artist, t1.song
order by "#song" desc;

-- remove duplicates with distinct
SELECT distinct t1.artist
	,t1.song
FROM PUBLIC."Billboard" AS t1
order by t1.artist, t1.song
;

-- ranks artists from number of appearences
SELECT distinct t1.artist
	,count(*) as "#artist"
FROM PUBLIC."Billboard" AS t1
group by t1.artist
order by "#artist" desc
;

-- ranks songs for number of appearences
SELECT distinct t1.song
	,count(*) as "#song"
FROM PUBLIC."Billboard" AS t1
group by t1.song
order by "#song" desc
;

-- exercise left join with #artist and #song
SELECT DISTINCT t1.artist
	,t2."#artist"
	,t1.song
	,t3."#song"
FROM PUBLIC."Billboard" AS t1
LEFT JOIN (
	SELECT DISTINCT t1.artist
		,count(*) AS "#artist"
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY "#artist" DESC
	) AS t2 ON (t1.artist = t2.artist)
LEFT JOIN (
	SELECT DISTINCT t1.song
		,count(*) AS "#song"
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY "#song" DESC
	) AS t3 ON (t1.song = t3.song)
ORDER BY t1.artist
	,t1.song;

-- using ctes to enhance the code
with cte_artist as (
    SELECT DISTINCT t1.artist
		,count(*) AS "#artist"
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY "#artist" DESC
),

cte_song as (
    SELECT DISTINCT t1.song
		,count(*) AS "#song"
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY "#song" DESC
)

SELECT DISTINCT t1.artist
	,t2."#artist"
	,t1.song
	,t3."#song"
FROM PUBLIC."Billboard" AS t1
LEFT JOIN cte_artist as t2 ON (t1.artist = t2.artist)
LEFT JOIN cte_song as t3 ON (t1.song = t3.song)
ORDER BY t1.artist
	,t1.song;

-- row_number() applications
with cte_billboard as(
    SELECT distinct t1.artist
	    ,t1.song
    FROM PUBLIC."Billboard" AS t1
    order by t1.artist, t1.song
) select * 
-- creates a row counting like an index following the order by artist and song
,row_number() over(order by artist, song) as "row_number"
-- creates a row couting considering the repetition of the artist
,row_number() over(partition by artist order by artist, song) as "row_number_artist"
from cte_billboard;

-- discover first time an artist appeared
with cte_billboard as(
    SELECT distinct t1.artist
	    ,t1.song
        -- creates a row counting like an index following the order by artist and song
        ,row_number() over(order by artist, song) as "row_number"
        -- creates a row couting considering the repetition of the artist
        ,row_number() over(partition by artist order by artist, song) as "row_number_artist"
    FROM PUBLIC."Billboard" AS t1
    order by t1.artist, t1.song
) select * 
from cte_billboard
where "row_number_artist" = 1;

-- rank, lag, lead, first value
with cte_billboard as(
    SELECT distinct t1.artist
	    ,t1.song
    FROM PUBLIC."Billboard" AS t1
    order by t1.artist, t1.song
) select * 
-- creates a row counting like an index following the order by artist and song
,row_number() over(order by artist, song) as "row_number"
-- creates a row couting considering the repetition of the artist
,row_number() over(partition by artist order by artist, song) as "row_number_artist"
-- rank beheaves in this case as the row_number_artist
,rank() over(partition by artist order by artist, song) as "rank"
-- creates a lag where you can get the last row value. Using partition it turns null every time the artist changes.
,lag(song, 1) over(partition by artist order by artist, song) as "lag_song"
-- the oposite of lag
,lead(song, 1) over(partition by artist order by artist, song) as "lead_song"
-- returns the first song of the artist because of partition
,first_value(song) over(partition by artist order by artist, song) as "first_song"
-- for last value "range between unbounded preceding and unbounded following" must be used. If not, it will get the last loaded value and the result will be lame.
,last_value(song) over(partition by artist order by artist, song range between unbounded preceding and unbounded following) as "last_song"
from cte_billboard;

-- other useful functions: 
-- dense_rank, percent_rank
-- cume_dist: accumulative distance to the end of the list 
-- cume_dist_desc: accumulative distance to the start of the list
-- nth_value: gets the nth_value on the table
-- ntile: gets a value in a specific line