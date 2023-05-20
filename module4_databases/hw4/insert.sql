/*
Задание 1
Заполните базу данных из предыдущего домашнего задания. В ней должно быть:

не менее 8 исполнителей,
не менее 5 жанров,
не менее 8 альбомов,
не менее 15 треков,
не менее 8 сборников.
Внимание: должны быть заполнены все поля каждой таблицы, в том числе таблицы связей исполнителей с жанрами
, исполнителей с альбомами, сборников с треками.
*/

insert into artists (pseudo_name, "name") values
('Eminem', 'Marshall Bruce Mathers'),
('Miley Cyrus', 'Destiny Hope Cyrus'),
('Rammstein', ''),
('Nirvana', ''),
('Lady Gaga', 'Stefani Joanne Angelina Germanotta'),
('Lana Del Rey', 'Elizabeth Woolridge Grant'),
('Ed Sheeran', 'Edward Christopher Sheeran'),
('Sting', 'Gordon Matthew Thomas Sumner')
;

insert into genres (genre_name) values 
('rock'),
('jazz'),
('reggae'),
('hip hop'),
('pop')
;

insert into album ("name", created_at) values
('The Eminem Show', '2002.05.01'),
('Breakout', '2008.07.22'),
('Mutter', '2001.04.02'),
('Nevermind', '1991.09.24'),
('Born This Way', '2011.05.23'),
('Born to Die', '2012.01.27'),
('+', '2011.09.09'),
('The Soul Cages', '1991.01.21'),
('Kamikaze', '2018.08.31')
;

insert into artists_albums values
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(1, 9)
;

insert into genres_artists values
(1, 4),
(2, 5),
(3, 1),
(4, 1),
(5, 5),
(6, 5),
(7, 5),
(7, 1),
(8, 2)
;

insert into track (track_ordinal_number, album_id, "name", "length") values
(1, 1, 'Curtains Up (Skit)', '00:00:30'),
(2, 1, 'White America', '00:05:24'),
(3, 1, 'Business', '00:04:11'),
(4, 1, 'Cleanin Out My Closet', '00:04:57'),
(5, 1, 'Square Dance', '00:05:23'),
(6, 1, 'The Kiss (Skit)', '00:01:15'),
(7, 1, 'Soldier', '00:03:46'),
(8, 1, 'Say Goodbye Hollywood', '00:04:32'),
(9, 1, 'Drips',	'00:04:45'),
(10, 1,	'Without Me', '00:04:50'),
(12, 1,	'Sing for the Moment', '00:05:39'),
(13, 1, 'Superman', '00:05:50'),
(14, 1, 'Hailie Song', 	'00:05:20'),
(16, 1, 'When the Music Stops', '00:04:29'),
(1, 9, 'The Ringer', '00:05:37'),
(2, 9, 'Greatest', '00:03:46'),
(3, 9, 'Lucky You', '00:04:04'),
(5, 9, 'Normal', '00:03:42'),
(7, 9, 'Stepping Stone', '00:05:09'),
(8, 9, 'Not Alike',	'00:04:48'),
(9, 9, 'Kamikaze', '00:03:36'),
(10, 9, 'Fall', '00:04:22'),
(11, 9, 'Nice Guy', '00:02:30'),
(12, 9, 'Good Guy', '00:02:22'),
(13, 9, 'Venom', '00:04:29'),
(1, 2, 'Breakout', '00:03:25'),
(2, 2, '7 Things', '00:03:34'),
(3, 2, 'The Driveway', '00:03:42'),
(4, 2, 'Girls Just Wanna Have Fun', '00:03:07'),
(5, 2, 'Full Circle', '00:03:15'),
(6, 2, 'Fly on the Wall', '00:02:32'),
(7, 2, 'Bottom of the Ocean', '00:03:15'),
(8, 2, 'Wake Up America', '00:02:45'),
(9, 2, 'These Four Walls', '00:03:26'),
(10, 2, 'Simple Song', '00:03:33'),
(11, 2, 'Goodbye', '00:03:53'),
(12, 2, 'See You Again (Rock Mafia Remix)', '00:03:17'),
(1, 3, 'Mein Herz brennt', '00:04:39'),
(2, 3, 'Links 2 3 4', '00:03:36'),
(3, 3, 'Sonne', '00:04:32'),
(4, 3, 'Ich will', '00:03:37'),
(5, 3, 'Feuer frei!', '00:03:11'),
(6, 3, 'Mutter', '00:04:32'),
(7, 3, 'Spieluhr', '00:04:46'),
(8, 3, 'Zwitter', '00:04:17'),
(9, 3, 'Rein raus', '00:03:09'),
(10, 3, 'Adios', '00:03:49'),
(11, 3, 'Nebel', '00:04:54'),
(1, 4, 'Smells Like Teen Spirit', '00:05:01'),
(2, 4, 'In Bloom', '00:04:14'),
(3, 4, 'Come as You Are', '00:03:39'),
(4, 4, 'Breed', '00:03:03'),
(5, 4, 'Lithium', '00:04:17'),
(6, 4, 'Polly', '00:02:57'),
(7, 4, 'Territorial Pissings', '00:02:22'),
(8, 4, 'Drain You', '00:03:43'),
(9, 4, 'Lounge Act', '00:02:36'),
(10, 4, 'Stay Away', '00:03:32'),
(11, 4, 'On a Plain', '00:03:16'),
(12, 4, 'Something in the Way', '00:03:52'),
(13, 4, 'Endless, Nameless', '00:06:43'),
(1, 5, 'Marry the Night', '00:04:25'),
(2, 5, 'Born This Way', '00:04:20'),
(3, 5, 'Government Hooker', '00:04:14'),
(4, 5, 'Judas', '00:04:09'),
(5, 5, 'Americano', '00:04:07'),
(6, 5, 'Hair', '00:05:08'),
(7, 5, 'Scheiße', '00:03:46'),
(8, 5, 'Bloody Mary', '00:04:05'),
(9, 5, 'Bad Kids', '00:03:51'),
(10, 5, 'Highway Unicorn (Road to Love)', '00:04:16'),
(11, 5, 'Heavy Metal Lover', '00:04:13'),
(12, 5, 'Electric Chapel', '00:04:12'),
(13, 5, 'You and I', '00:05:07'),
(14, 5, 'The Edge of Glory', '00:05:21'),
(1, 6, 'Born to Die', '00:04:46'),
(2, 6, 'Off to the Races', '00:05:00'),
(3, 6, 'Blue Jeans', '00:03:30'),
(4, 6, 'Video Games', '00:04:42'),
(5, 6, 'Diet Mountain Dew', '00:03:43'),
(6, 6, 'National Anthem', '00:03:51'),
(7, 6, 'Dark Paradise', '00:04:03'),
(8, 6, 'Radio', '00:03:34'),
(9, 6, 'Carmen', '00:04:08'),
(10, 6, 'Million Dollar Man', '00:03:51'),
(11, 6, 'Summertime Sadness', '00:04:25'),
(12, 6, 'This Is What Makes Us Girls', '00:03:58'),
(1, 7, 'The A Team', '00:04:18'),
(2, 7, 'Drunk', '00:03:20'),
(3, 7, 'U.N.I.', '00:03:48'),
(4, 7, 'Grade 8', '00:02:59'),
(5, 7, 'Wake Me Up', '00:03:49'),
(6, 7, 'Small Bump', '00:04:19'),
(7, 7, 'This', '00:03:15'),
(8, 7, 'The City', '00:03:54'),
(9, 7, 'Lego House', '00:03:05'),
(10, 7, 'You Need Me, I Dont Need You', '00:03:40'),
(11, 7, 'Kiss Me', '00:04:40'),
(1, 8, 'Island of Souls', '00:06:41'),
(2, 8, 'All This Time', '00:04:54'),
(3, 8, 'Mad About You', '00:03:53'),
(4, 8, 'Jeremiah Blues (Part 1)', '00:04:54'),
(5, 8, 'Why Should I Cry for You', '00:04:46'),
(6, 8, 'Saint Agnes and the Burning Train', '00:02:43'),
(7, 8, 'The Wild Wild Sea', '00:06:41'),
(8, 8, 'The Soul Cages', '00:05:51'),
(9, 8, 'When the Angels Fall', '00:07:48')
;

insert into collection ("name", released_at) values 
('best songs of 1991', 1991),
('best songs of 2001', 2001),
('best songs of 2008', 2008),
('best songs of 2011', 2011),
('best songs of 2012', 2012),
('best songs of 2018', 2018),
('best songs of 90s', 1999),
('best songs of 00s', 2009),
('best songs of 10s', 2019)
;

insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 1991
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 1991) t
;

insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 2001
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 2001) t
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 2008
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 2008) t
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 2011
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 2011) t
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 2012
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 2012) t
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) = 2018
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at = 2018) t
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) between 1990 and 1999
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at between 1990 and 1999) t
where collection_id > 6
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) between 2000 and 2009
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at between 2000 and 2009) t
where collection_id > 6
;
insert into collection_tracks
with ids as ( 
	select track_id
	from track t 
	left join album a on t.album_id = a.id 
	where date_part('year', created_at) between 2010 and 2019
	order by "length" desc
	limit 10
)
select collection_id, track_id
from ids 
cross join (select id collection_id
			from collection
			where released_at between 2010 and 2019) t
where collection_id > 6
;