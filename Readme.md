# SPbLitGuide 1999–2020
![alt text](https://github.com/mary-lev/litgid/blob/master/static/logo.png "Logo")

СПбЛитГид — это основные события петербургской литературной жизни в рассылке Дарьи Суховей, которую она ведет с мая 1999 года. В течение нескольких лет выпуски СПбЛитГида размещались на сайте http://levin.rinet.ru, с 2010 по 2015 год — на сайте книжной ярмарки ДК Крупской, с 2015 года — на сайте [«Своего издательства»](https://isvoe.ru). Все двадцать лет несколько раз в месяц подписчики рассылки получали анонсы литературных мероприятий Санкт-Петербурга (о [принципах составления рассылки](http://isvoe.ru/spblitgid/sample-page/)).

## Задача проекта

Сейчас на сайте «Своего издательства» выложены все найденные письма — это 1255 выпусков, и регулярно добавляются новые. Теоретически это позволяет использовать встроенный в Wordpress поиcк, если нужно найти персонажа или событие, на практике это не слишком удобно. Интересно было посмотреть, что можно сделать с частично структурированной текстовой информацией с помощью инструментов обработки текста.

1. Сначала с помощью (канувшего в Лету) скрипта на Python были прочитаны все (в том числе и довольно битые) eml-файлы рассылки и выгружены на сайт на Wordpress.

2. К октябрю 2019 года, когда была проведена эта операция, рассылка включала 1157 выпусков. Регулярными выражениями и здравым смыслом из них были извлечены непосредственно анонсы мероприятий: в этот массив текстов не вошли рубрики "Новости", обзоры прошедших литературных вечеров, анонсы вышедших книг и другие литературные новости, которые составляют важную часть рассылки. Для дальнейших экспериментов оставлена информация о каждом событии: 
* дата,
* время,
* место,
* адрес,
* описание.

3. Благодаря структурированности рассылки и постоянству Дарьи Суховей на протяжении 20 лет распарсить выпуски, то есть разделить события и поля внутри каждого события, было не слишком трудно. С небольшими вариациями тексты анонсов выглядят так:
```
	29.09.05 четверг 18:00 Музей Ахматовой
	Десант "НЛО": творческий отчет о проделанной работе. Издательский дом 
	<Новое литературное обозрение> представляет спецпроекты последних лет. Вечер ведет
	главный редактор Ирина Дмитриевна Прохорова.
```
Однако непросто оказалось привести к единому знаменателю названия тех мест, в которых проходили мероприятия, и их адреса, поскольку и адреса могли быть обозначены в десятке вариаций, и в названиях мест встречались опечатки и разночтения. В результате чистки данных c помощью pandas и difflib получилась база данных, включающая 14 990 литературных событий (по октябрь 2019 года), 862 мест их проведения и 817 адресов (по одному адресу могли одновременно или последовательно размещаться разные более или менее культурные точки: сменяли друг друга бары, театры, кафе, книжные магазины; они же неоднократно переезжали с места на место).

4. Под базу данных и дальнейшие эксперименты развернута Django (c REST framework для API и пижонства).
![alt text](https://github.com/mary-lev/litgid/blob/master/static/screenshot.png "Screeshot")

5. На основе полученных данных можно нарисовать любопытную картину — или карту — литературной жизни Петербурга за 20 последних лет: изучить в динамике активность тех или иных "литературных мест" и их типов (к ним относятся библиотеки, музеи, факультеты и школы, бары и клубы, книжные магазины, театры, художественные галереи, концертные залы, улицы и воды города и его пригородов). Для этого я планирую установить координаты всех "событийных мест" и нарисовать карту литературного Петербурга (с помощью, видимо, GeoDjango).

6. Календарное представление событий, помогающее передать насыщенность литературной жизни, реализовано на основе стандартного модуля calendar, немного доработанного для общей симпатичности.

7. Интересно было бы составить граф персонажей, принимавших участие в мероприятиях за последние 20 лет. Это тривиальная задача, не имеющая тем не менее пока тривиального решения: из текстов нужно извлечь (named entity recognition) имена и фамилии людей и привести к единообразию варианты их написания. Пока я пытаюсь решить эту задачу с помощью нейронной сети от [deeppavlov](https://github.com/deepmipt/DeepPavlov). Хотела было использовать [natasha](), но, хотя извлекает она не хуже, работать с выходными результатами на порядок сложнее.

8. Гипотеза, которую хочется проверить, имеет отношение к социологии литературной жизни и модному сетевому анализу всего подряд. Граф литературной жизни Петербурга, который планируется нарисовать, основан на связности персонажей, выявляемое через совместное участие в мероприятиях и/или через участие в разных мероприятиях в одном месте-организаторе (в зависимости от степени "всеядности" упомянутого места). Интересно было бы выявить группировки персонажей-участников, центральных персонажей и персонажей-посредников и т. д.  

## Links
* [СПбЛитГид](http://isvoe.ru/spblitgid/)