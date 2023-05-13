/*
Обязательная часть
Будем развивать схему для музыкального сервиса.

Ранее существовало ограничение, что каждый исполнитель поёт строго в одном жанре, пора его убрать. 
Исполнители могут петь в разных жанрах, как и одному жанру могут принадлежать несколько исполнителей.

Аналогичное ограничение было и с альбомами у исполнителей — альбом мог выпустить только один исполнитель. 
Теперь альбом могут выпустить несколько исполнителей вместе. Как и исполнитель может принимать участие во множестве альбомов.

С треками ничего не меняем, всё так же трек принадлежит строго одному альбому.

Но появилась новая сущность — сборник. Сборник имеет название и год выпуска. В него входят различные треки из разных альбомов.

Обратите внимание: один и тот же трек может присутствовать в разных сборниках.

Задание состоит из двух частей

Спроектировать и нарисовать схему, как в первой домашней работе. Прислать изображение со схемой.
Написать SQL-запросы, создающие спроектированную БД. Прислать ссылку на файл, содержащий SQL-запросы.
Примечание: можно прислать сначала схему, получить подтверждение, что схема верная, и после этого браться за написание запросов.
*/

drop table if exists album_tracks;
drop table if exists genres_artists;
drop table if exists artists_albums;
drop table if exists collection_tracks;
drop table if exists genres;
drop table if exists artists;
drop table if exists track;
drop table if exists album;
drop table if exists collection;

create table if not exists genres 
(
	id serial primary key,
	genre_name varchar(100)
);


create table if not exists artists 
(
	id serial primary key,
	"name" varchar(100),
	pseudo_name varchar(100)
);

create table if not exists genres_artists 
(
	artist_id int references artists(id),
	genre_id int references genres(id),
	primary key (artist_id, genre_id)
);

create table if not exists album 
(
	id serial primary key,
	"name" varchar(100),
	created_at date
);

create table if not exists artists_albums 
(
	artist_id int references artists(id),
	album_id int references album(id),
	primary key (artist_id, album_id)
);

create table if not exists track 
(
	track_id serial primary key,
	track_ordinal_number int,
	album_id int references album(id),
	"name" varchar(100),
	"length" time
);

create table if not exists collection 
( 
	id serial primary key,
	"name" varchar(100),
	released_at int check(1900 < released_at and released_at < 2024)
);

create table if not exists collection_tracks
( 
	collection_id int references collection(id),
	track_id  int references track(track_id),
	primary key(collection_id, track_id)
);
