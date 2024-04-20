-- migrate:up

insert into api_data.owners (first_name, last_name, passport)
values 
	('Демид', 'Кузнецов', 123456),
	('Иван', 'Петров', 123879),
	('Алиса', 'Лебедева', 123466);

insert into api_data.hcs (name, phone, address, capital)
values
	('Домовик', '+79508883412', 'г. Сочи, ул. Западная, д. 13', 120000000),
	('RAB', '+79003451233', 'г. Самара, ул. Пригодная, д. 25', 300000);


insert into api_data.properties (address, square, price, hcs_id)
values
	('г. Невинномысск, Пролетарская ул., д. 4', 145, 2320000, (select id from api_data.hcs where name = 'Домовик')),
	('г. Копейск, Интернациональная ул., д. 14', 200, 5000000, (select id from api_data.hcs where name = 'Домовик')),
	('г. Новошахтинск, Полесская ул., д. 15', 725, 12000000000, (select id from api_data.hcs where name = 'Домовик')),
	('г. Санкт-Петербург, Дачная ул., д. 10', 100, 1500000, (select id from api_data.hcs where name = 'Домовик'));

insert into api_data.owners_properties (owners_id, properties_id)
values
	(
		(select id from api_data.owners where first_name = 'Демид'),
		(select id from api_data.properties where address = 'г. Невинномысск, Пролетарская ул., д. 4')
	),
	(
		(select id from api_data.owners where first_name = 'Демид'),
		(select id from api_data.properties where address = 'г. Копейск, Интернациональная ул., д. 14')
	),
	(
		(select id from api_data.owners where first_name = 'Алиса'),
		(select id from api_data.properties where address = 'г. Новошахтинск, Полесская ул., д. 15')
	),
	(
		(select id from api_data.owners where first_name = 'Алиса'),
		(select id from api_data.properties where address = 'г. Невинномысск, Пролетарская ул., д. 4')
	);

-- migrate:down
