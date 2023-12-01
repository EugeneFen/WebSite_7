import sqlite3
import pandas as pd
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("library.sqlite")
# открываем файл с дампом базой двнных
f_damp = open('library.db','r', encoding ='utf-8-sig')
# читаем данные из файла
damp = f_damp.read()
# закрываем файл с дампом
f_damp.close()
# запускаем запросы
con.executescript(damp)
# сохраняем информацию в базе данных
con.commit()
# создаем курсор
cursor = con.cursor()
# выбираем и выводим записи из таблиц author, reader

print("Индивидуальное. Задание 1:")
cursor.execute('''
    select IIF(available_numbers < 3, 'Мало', IIF(available_numbers>2, IIF(available_numbers<5, 'Достаточно', 'Много'), 'Мало')) as 'Наличие',
    title as 'Название', genre.genre_name as 'Жанр', available_numbers as 'Количество'
    from book inner join genre using(genre_id)
    where title in (select title
                        from book
                        where title not like "% %")
    ''')
print(cursor.fetchall())

print("Задание 2:")
cursor.execute('''
    select genre_name as 'Жанр', count(title) as 'Количество'
    from book inner join genre using(genre_id)
    where available_numbers = 0
    group by genre_id
    union all
    select genre_name as 'Жанр', 'Нет' as 'Количество'
    from genre
    where genre_name not in (
        select genre_name
        from genre inner join book using(genre_id)
        group by genre_id
        )
    order by genre_name 
    ''')
print(cursor.fetchall())

print("Задание 3:")
cursor.execute('''
with Table_max as (
        select genre_id, max(sum_book) as sum_book_max
        from (select genre_id, sum(Table_count.count_book) as sum_book
            from (select book_id, count(borrow_date) as count_book
                from book_reader
                group by book_id
                ) as Table_count inner join book using(book_id)
            group by genre_id) as Table_two
)
select title
from book inner join Table_max using(genre_id)
    ''')
print(cursor.fetchall())

print("Популярный жанр задания 3:")
cursor.execute('''
select genre_name, max(sum_book) as sum_book_max
        from (select genre_id, sum(Table_count.count_book) as sum_book
            from (select book_id, count(borrow_date) as count_book
                from book_reader
                group by book_id
                ) as Table_count inner join book using(book_id)
            group by genre_id) as Table_two inner join genre using(genre_id)
''')
print(cursor.fetchall())

print("Задание 4:")
cursor.execute('''
    with Table_ins as (
                    select book_id, reader_id
                    from reader, book inner join book_author using(book_id)
                        inner join author using(author_id)
                    where author.author_name = "Пушкин А.С." and
                            book.title = "Поэмы" and
                            reader.reader_name = "Абрамова А.А."
    )
    insert into book_reader (book_id, reader_id, borrow_date)
    values ((select book_id from Table_ins), (select reader_id from Table_ins), DATE());
''')

cursor.execute('''
    select *
    from book_reader
    order by borrow_date desc
''')
print(cursor.fetchall())

print("Таблицы для проерки изменяемости числа книг задания 4:")
cursor.execute('''
with Table_ins as (
                    select book_id
                    from book inner join book_author using(book_id)
                        inner join author using(author_id)
                    where author.author_name = "Пушкин А.С." and
                            book.title = "Поэмы"
    )
    select * from book where book_id = (select book_id from Table_ins)
''')
print(cursor.fetchall())
"""
cursor.execute('''
    with Table_ins as (
                    select book_id
                    from book inner join book_author using(book_id)
                        inner join author using(author_id)
                    where author.author_name = "Пушкин А.С." and
                            book.title = "Поэмы"
    )
    update book set available_numbers = available_numbers - 1 where book_id = (select book_id from Table_ins)
''')
"""
cursor.execute('''
with Table_ins as (
                    select book_id
                    from book inner join book_author using(book_id)
                        inner join author using(author_id)
                    where author.author_name = "Пушкин А.С." and
                            book.title = "Поэмы"
    )
    select * from book where book_id = (select book_id from Table_ins)
''')
print(cursor.fetchall())

"""
cursor.execute('''
insert into book (title, genre_id, publisher_id, year_publication, available_numbers)
values("One night", 2, 1, "2020", 8)
''')
"""

print("Задание 5:")
cursor.execute('''
with Table_max_num as(
        select distinct publisher_id, max(available_numbers) over(PARTITION BY publisher_id) as avail_max
        from book
    )
select publisher_name, title, available_numbers
from Table_max_num, book inner join publisher using(publisher_id)
where available_numbers = avail_max and Table_max_num.publisher_id = book.publisher_id
order by publisher_name, available_numbers desc, title
''')
print(cursor.fetchall())

cursor.execute('''
select distinct max(available_numbers) over(PARTITION BY publisher_id) as avail_max, publisher_name, publisher_id
        from publisher inner join book using(publisher_id)
''')
print(cursor.fetchall())
print()

print("Лабораторная. Задание 1:")
cursor.execute("SELECT * FROM author")
print(cursor.fetchall())
cursor.execute("SELECT * FROM reader")
print(cursor.fetchall())

print("Задание 2:")
cursor.execute('''
 SELECT
 title,
 publisher_name,
 year_publication
 FROM book
 JOIN genre USING (genre_id)
 JOIN publisher USING (publisher_id)
 WHERE genre_name = :p_genre AND year_publication > :p_year
''',{"p_genre": "Детектив", "p_year": 2016})
print(cursor.fetchall())

print("Задание 3:")
df = pd.read_sql('''
 SELECT
 title AS Название,
 publisher_name AS Издательство,
 year_publication AS Год
 FROM book
 JOIN genre USING (genre_id)
 JOIN publisher USING (publisher_id)
 WHERE genre_name = :p_genre AND year_publication > :p_year
''', con, params={"p_genre": "Роман", "p_year": 2016})
print(df)

# закрываем соединение с базой
con.close()

"""
Для каждой книги, название которой состоит из одного слова, указать информацию о ее наличии в библиотеке 
(столбец available_numbers). Если количество доступных книг меньше 3 - вывести "мало", если количество в интервале от 
3 до 5 - вывести "достаточно", если больше 5 - вывести "много". Для каждой книги также указать ее жанр и количество 
книг в наличии. Столбцы назвать Название, Жанр, Количество, Наличие. Информацию отсортировать сначала по возрастанию 
количества книг, а потом по названию в обратном алфавитном порядке.

select title
from book
where like '% %'

select IIF(available_numbers < 3, 'Мало', IIF(available_numbers>2, IIF(available_numbers<5, 'Достаточно', 'Много'), 'Мало')) as 'Наличие',
title as 'Название', genre.genre_name as 'Жанр', available_numbers as 'Количество'
from book inner join genre using(genre_id)
where title in (select title
                    from book
                    where title not like '% %')
"""
"""
Вывести все жанры, имеющие хотя бы одну книгу, все экземпляры которой на руках у читателей 
(значение available_numbers равно 0), указать название жанра и количество таких книг. В результирующую таблицу 
также включить жанры, книги которых не представлены в библиотеке. Для этих книг вместо количества указать "нет".
Столбцы назвать Жанр и Количество. Информацию отсортировать по жанрам в алфавитном порядке.

select genre_name as 'Жанр', count(title) as 'Количество'
from book inner join genre using(genre_id)
where available_numbers = 0
group by genre_id
union all
select genre_name as 'Жанр', 'Нет' as 'Количество'
from genre
where genre_name not in (
    select genre_name
    from genre inner join book using(genre_id)
    group by genre_id
)
order by genre_name 

"""
"""
Найти самые популярные жанры 
(книги, относящиеся к которым чаще всего брали читатели) и 
вывести все книги, которые относятся к этим жанрам.

select book_id, count(borrow_date) as Количество
from book_reader
group by book_id

select genre_id, sum(Table_count.count_book) as sum_book
from (select book_id, count(borrow_date) as count_book
    from book_reader
    group by book_id
    ) as Table_count inner join book using(book_id)
group by genre_id

select max(sum_book) as max_sum_book
from (select genre_id, sum(Table_count.count_book) as sum_book
    from (select book_id, count(borrow_date) as count_book
        from book_reader
        group by book_id
        ) as Table_count inner join book using(book_id)
    group by genre_id) as table_first
    
select genre_id
from (select book_id, count(borrow_date) as count_book
    from book_reader
    group by book_id
    ) as Table_count inner join book using(book_id)
group by genre_id
having sum(Table_count.count_book) = (select max(sum_book) as max_sum_book
                        from (select genre_id, sum(Table_count.count_book) as sum_book
                            from (select book_id, count(borrow_date) as count_book
                                from book_reader
                                group by book_id
                                ) as Table_count inner join book using(book_id)
                            group by genre_id) as table_first)
    
select *
from book inner join (select genre_id, sum(Table_count.count_book) as sum_book
                        from (select book_id, count(borrow_date) as count_book
                                from book_reader
                                group by book_id
                                ) as Table_count inner join book using(book_id)
                        group by genre_id) as table_first) as table_max using(genre_id)
where 
                    
                    
    (select max(sum_book) as max_sum_book
            from (select genre_id, sum(Table_count.count_book) as sum_book
                from (select book_id, count(borrow_date) as count_book
                    from book_reader
                    group by book_id
                    ) as Table_count inner join book using(book_id)
                group by genre_id) as table_first) as table_max
                
select title
from book 
where genre_id = (select genre_id
                    from (select book_id, count(borrow_date) as count_book
                        from book_reader
                        group by book_id
                        ) as Table_count inner join book using(book_id)
                    group by genre_id
                    having sum(Table_count.count_book) = (select max(sum_book) as max_sum_book
                                            from (select genre_id, sum(Table_count.count_book) as sum_book
                                                from (select book_id, count(borrow_date) as count_book
                                                    from book_reader
                                                    group by book_id
                                                    ) as Table_count inner join book using(book_id)
                                                group by genre_id) as table_first))

                                                
with Table_max as (
            select genre_id, sum(Table_count.count_book) as sum_book
            from (select book_id, count(borrow_date) as count_book
                from book_reader
                group by book_id
                ) as Table_count inner join book using(book_id)
            group by genre_id
)
select title
from book inner join Table_max using(genre_id)
where sum_book = max(sum_book)
"""

"""
Читатель Абрамова А.А. берет книгу "Поэмы", автор книги - Пушкин А.С.. Необходимо актуализировать базу данных, для этого:

    занести новую запись в таблицу book_reader, в качестве даты получения книги (borrow_date) установить текущую дату;
    уменьшить количество доступных экземпляров книги "Поэмы", автора Пушкин А.С. на 1.
Пояснение. В запросах использовать Фамилии И.О. читателя и автора, а также название книги, а не id этих значений.

name_reader = "Абрамова А.А"
name_book = "Поэмы"
name_author = "Пушкин А.С"

with Table_ins as (
                select book_id, reader_id
                from reader inner join book_reader using(reader_id)
                    inner join book using(book_id)
                    inner join book_author using(book_id)
                    inner join author using(author_id)
                where author_name = name_author and
                        title = name_book and
                        reader_name = name_reader
                    
)
insert into book_reader (book_id, reader_id, borrow_date)
value(Table_ins, CURDATE())

insert into reader (book_id, reader_id, borrow_date)
values ("Поэмы", "Абрамова А.А", CURDATE())
"""

"""
Для каждого издательства найти три книги, количество доступных экземпляров которых максимально. 
Учитывать только те книги, количество доступных экземпляров не равно 0. 
Если у четвертой и далее книг количество экземпляров такое же, как у третьей, то вывести их всех, 
если книг всего две или одна - вывести только их. 

Вывести название издательства, название книги, доступное количество экземпляров. 

Информация должна быть отсортирована по названию издательства в алфавитном порядке, 
затем по убыванию количества доступных книг и, наконец, по названию книг в алфавитном порядке.

Примечание. Для решения задания № 5 использовать оконные функции.

with Table_max_num as(
        select max(available_numbers) as avail_max, publisher_id
        from book
        group by publisher_id
        having available_numbers > 0
    )
select publisher_name, title, available_numbers
from Table_max_num, book inner join publisher using(publisher_id)
where available_numbers = avail_max and Table_max_num.publisher_id = book.publisher_id
order by publisher_name, available_numbers desc, title


"""
