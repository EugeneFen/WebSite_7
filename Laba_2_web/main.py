import sqlite3

con = sqlite3.connect("Pet.db")
cur = con.cursor()
cur.execute("PRAGMA table_info('dog_owner')")
print(cur.fetchall())

#ывести всех врачей и их специализацию работающих по понедельникам в алфавитном порядке
cur.execute("""
SELECT first_name, last_name, name_specialization
FROM specialization inner join doctor USING(id_specialization)
										inner join work_day USING(id_doctor)
										inner join day USING(id_day)
WHERE name_day = 'Понедельник'
ORDER BY 1, 2
""")
print(cur.fetchall())

#Вывести имена и породы всех собак в возрасте от 2 до 5 лет? в порядке убывания их возраста, а также имена их хозяев.
cur.execute("""
SELECT name_dog, age_dog, name_breed_of_dog, first_name, last_name
FROM breed_of_dog inner join dog USING(id_breed_of_dog)
									inner join dog_owner USING(id_dog_owner)
WHERE age_dog >= 2 and age_dog < 5
ORDER BY age_dog DESC
""")
print(cur.fetchall())

#Вывести максимальный возраст собаки для каждой породы
cur.execute("""
SELECT name_breed_of_dog, max(age_dog)
FROM breed_of_dog inner join dog USING(id_breed_of_dog)
GROUP BY name_breed_of_dog
""")
print(cur.fetchall())

#Вывести для каждого дня недели количество работающих врачей
cur.execute("""
SELECT name_day, sum(id_doctor)
FROM work_day inner join day USING(id_day)
GROUP BY name_day
""")
print(cur.fetchall())

#Вывести день недели в который работает наибольшее число докторов
cur.execute("""
select max_table.name_day
from (select name_day, max(sum_doctor), id_day
			from (select name_day, sum(id_doctor) as sum_doctor, day.id_day
						from day inner join work_day using(id_day)
						group by id_day) as sum_table) as max_table inner join day using(id_day)
""")
print(cur.fetchall())

#Вывести породу, у которой меньше всего собак
cur.execute("""
select min_table.name_breed_of_dog
from (select name_breed_of_dog, min(sum_dog), id_breed_of_dog
			from (select name_breed_of_dog, sum(id_dog) as sum_dog, breed_of_dog.id_breed_of_dog
						from breed_of_dog inner join dog using(id_breed_of_dog)
						group by id_breed_of_dog) as sum_table) as min_table inner join breed_of_dog using(id_breed_of_dog)
""")
print(cur.fetchall())

con.commit()
con.close()