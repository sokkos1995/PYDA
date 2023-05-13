/*
Задание 2
Написать SELECT-запросы, которые выведут информацию согласно инструкциям ниже.

Внимание: результаты запросов не должны быть пустыми, учтите это при заполнении таблиц.

Название и год выхода альбомов, вышедших в 2018 году.
Название и продолжительность самого длительного трека.
Название треков, продолжительность которых не менее 3,5 минут.
Названия сборников, вышедших в период с 2018 по 2020 год включительно.
Исполнители, чьё имя состоит из одного слова.
Название треков, которые содержат слово «мой» или «my».
*/

select "name", date_part('year', created_at) as created_at_year
from album a 
where date_part('year', created_at) = 2018

select "name", "length"
from track t 
order by "length" desc
limit 1  -- можно и через агрегацию, остановился на лимит так как это было в теме урока

select "name"
from track t 
where "length" >= '00:03:30'

select "name"
from collection c 
where released_at between 2018 and 2020

select pseudo_name 
from artists a 
where pseudo_name not like '% %'

select "name"
from track t 
where "name" ilike '%my%'