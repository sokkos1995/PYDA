/*
Написать SELECT-запросы, которые выведут информацию согласно инструкциям ниже.

Внимание: результаты запросов не должны быть пустыми, при необходимости добавьте данные в таблицы.

Количество исполнителей в каждом жанре.
Количество треков, вошедших в альбомы 2019–2020 годов.
Средняя продолжительность треков по каждому альбому.
Все исполнители, которые не выпустили альбомы в 2020 году.
Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
Наименования треков, которые не входят в сборники.
Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, 
— теоретически таких треков может быть несколько.
Названия альбомов, содержащих наименьшее количество треков.

*/

--Количество исполнителей в каждом жанре.
select g.genre_name , count(ga.artist_id)
from genres g 
left join genres_artists ga on g.id = ga.genre_id 
group by 1;

--Количество треков, вошедших в альбомы 2019–2020 годов.
select count(track_id)
from track t 
join album a on t.album_id = a.id 
where date_part('year', created_at) between 2019 and 2020;

--Средняя продолжительность треков по каждому альбому.
select a."name"  , avg(length)
from track t 
join album a on t.album_id = a.id 
group by a."name"  ;

--Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT a.pseudo_name  /* Получаем имена исполнителей */
FROM artists a  /* Из таблицы исполнителей */
WHERE a.pseudo_name NOT IN ( /* Где имя исполнителя не входит в вложенную выборку */
    SELECT a.pseudo_name /* Получаем имена исполнителей */
    FROM artists a /* Из таблицы исполнителей */
    JOIN artists_albums aa ON a.id = aa.artist_id  /* Объединяем с промежуточной таблицей */
    JOIN album a2 ON a2.id = aa.album_id /* Объединяем с таблицей альбомов */
    WHERE date_part('year', a2.created_at) = 2020 /* Где год альбома равен 2020 */
);

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
select c."name" 
from collection c 
join collection_tracks ct on c.id = ct.collection_id 
join track t on t.track_id = ct.track_id 
join artists_albums aa on aa.album_id = t.album_id 
join artists a on a.id = aa.artist_id 
where a.pseudo_name = 'Eminem'
group by 1;

--Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT distinct a."name"  /* Получаем ТОЛЬКО уникальные имена альбомов. Другие данные в выводе не нужны */
FROM album a /* Из таблицы альбомов */
JOIN artists_albums aa on a.id = aa.album_id /* Объединяем альбомы с промежуточной таблицей между альбомами и исполнителями */
JOIN genres_artists ga on aa.artist_id = ga.artist_id  /* Объединяем промежуточную таблицу выше с промежуточной таблицей между исполнителями и жанрами */
GROUP BY a."name", aa.artist_id  /* Группируем по айди альбомов и айди исполнителей из промежуточной таблицы между исполнителями и жанрами */
HAVING COUNT(genre_id) > 1; /* Где количество id жанров из промежуточной таблицы больше 1 */

--Наименования треков, которые не входят в сборники.
select t."name" 
from collection c 
join collection_tracks ct on c.id = ct.collection_id 
full join track t on t.track_id = ct.track_id 
where c."name" is null;

--Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков 
--может быть несколько.

select a.pseudo_name 
from track t
left join artists_albums aa on t.album_id = aa.album_id 
join artists a on a.id = aa.artist_id 
where "length" = (select min("length") from track t );

--Названия альбомов, содержащих наименьшее количество треков.
with album_track_count as (
select album_id, count(track_id) track_counter
from track t 
group by album_id 
)
select a."name" 
from album_track_count atc
join album a on a.id = atc.album_id
where track_counter = (select min(track_counter) from album_track_count);

--альтернативный вариант
SELECT a."name"  /* Названия альбомов */
FROM album a JOIN track t ON a.id = t.album_id /* Объединяем альбомы и треки */
GROUP BY a."name" /* Группируем по айди альбомов */
HAVING COUNT(track_id) = ( /* Где количество треков равно вложенному запросу, в котором получаем наименьшее количество треков в одном альбоме */
    SELECT COUNT(track_id) FROM track t /* Получаем поличество айди треков из таблицы треков*/
    GROUP BY album_id /* Группируем по айди альбомов */
    ORDER BY 1 /* Сортируем по первому столбцу */
    LIMIT 1 /* Получаем первую запись */
);