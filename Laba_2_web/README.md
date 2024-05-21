 Научиться использовать SQLite и Python: создавать базу данных, таблицы, наполнять таблицы информацией и выбирать данные.
 Создать базу данных для итогового проекта. Придумать запросы к ней.

 Вывести всех врачей и их специализацию работающих по понедельникам в алфавитном порядке

```sql
SELECT first_name, last_name, name_specialization 
FROM specialization inner join doctor USING(id_specialization)
										inner join work_day USING(id_doctor)
										inner join day USING(id_day)
WHERE name_day = “Понедельник”
ORDER BY 1, 2
```

Вывести имена и породы всех собак в возрасте от 2 до 5 лет? в порядке убывания их возраста, а также имена их хозяев.

```sql
SELECT name_dog, age_dog, name_breed_of_dog, first_name, last_name
FROM breed_of_dog inner join dog USING(id_breed_of_dog)
									inner join dog_owner USING(id_dog_owner)
WHERE age_dog ≥ 2 and age_dog < 5
ORDER BY age_dog DESC
```

- два запроса с группировкой и групповыми функциями;

Вывести максимальный возраст собаки для каждой породы

```sql
SELECT name_breed_of_dog, max(age_dog)
FROM breed_of_dog inner join dog USING(id_breed_of_dog)
GROUP BY name_breed_of_dog
```

Вывести для каждого дня недели количество работающих врачей

```sql
SELECT name_day, sum(id_doctor)
FROM work_day inner join day USING(id_day)
GROUP BY name_day
```

- два запроса со вложенными запросами или табличными выражениями;

Вывести день недели в который работает наибольшее число докторов

```sql
select max_table.name_day
from (select name_day, max(sum_doctor), id_day
			from (select name_day, sum(id_doctor) as sum_doctor, day.id_day
						from day inner join work_day using(id_day)
						group by id_day) as sum_table) as max_table inner join day using(id_day)
```

Вывести породу, у которой меньше всего собак

```sql
select min_table.name_breed_of_dog
from (select name_breed_of_dog, min(sum_dog), id_breed_of_dog
			from (select name_breed_of_dog, sum(id_dog) as sum_dog, breed_of_dog.id_breed_of_dog
						from breed_of_dog inner join dog using(id_breed_of_dog)
						group by id_breed_of_dog) as sum_table) as min_table inner join breed_of_dog using(id_breed_of_dog)
```

- два запроса корректировки данных (обновление, добавление, удаление и пр)

It is…
