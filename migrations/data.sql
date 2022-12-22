INSERT INTO rector(rector_id, last_name, first_name, middle_name) VALUES (1, 'Пономаренко', 'Володимир', 'Степанович');

INSERT INTO university(university_name, short_university_name, rector_id)
VALUES ('Харківський національний економічний університет імені Семена Кузнеця',
        'ХНЕУ ім. С. Кузнеця', 1);

INSERT INTO role(role_name) VALUES ('Студент');
INSERT INTO role(role_name) VALUES ('Адміністратор');
INSERT INTO role(role_name) VALUES ('Супер Адміністратор');

INSERT INTO service(service_id, service_name) VALUES (1, 'Поселення в гуртожиток');

INSERT INTO user_request_status(id, name) VALUES (1, 'Схвалено');
INSERT INTO user_request_status(id, name) VALUES (2, 'Відхилено');
INSERT INTO user_request_status(id, name) VALUES (3, 'Розглядається');
INSERT INTO user_request_status(id, name) VALUES (4, 'Скасовано');

INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (1, 'Коц', 'Григорій', 'Павлович');
INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (2, 'Птащенко', 'Олена', 'Валеріївна');
INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (3, 'Шталь', 'Тетяна', 'Валеріївна');
INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (4, 'Проноза', 'Павло', 'Володимирович');
INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (5, 'Вовк', 'Володимир', 'Анатолійович');
INSERT INTO dean(dean_id, last_name, first_name, middle_name) VALUES (6, 'Бріль', 'Михайло', 'Сергійович');

INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (1, 'Інформаційних технологій', 'ІТ', 1, 1);
INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (2, 'Міжнародних відносин і журналістики', 'МВЖ', 1, 2);
INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (3, 'Міжнародної економіки і підприємництва', 'МЕП', 1, 3);
INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (4, 'Фінансів і обліку', 'ФіО', 1, 4);
INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (5, 'Менеджмента і маркетингу', 'МіМ', 1, 5);
INSERT INTO faculty(faculty_id, name, shortname, university_id, dean_id) VALUES (6, 'Економіки і права', 'ЕіП', 1, 6);

INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (1, '0.75');
INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (2, '1');
INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (3, '1.5');

INSERT INTO course(course_id, value) VALUES (1, 1);
INSERT INTO course(course_id, value) VALUES (2, 2);
INSERT INTO course(course_id, value) VALUES (3, 3);
INSERT INTO course(course_id, value) VALUES (4, 4);
INSERT INTO course(course_id, value) VALUES (5, 5);
INSERT INTO course(course_id, value) VALUES (6, 6);

INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (1, 'Ляшко', 'Надія', 'Михайлівна', '380577107851');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (2, 'Любченко', 'Володимир', 'Віталійович', '380577792654');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (3, 'Колосова', 'Олена', 'Іванівна', '380573368350');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (4, 'Марченко', 'Тетяна', 'Федорівна', '380573367757');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (5, 'Рилова', 'Лариса', 'Миколаївна', '380577021194');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (6, 'Голубєва', 'Надія', 'Олександрівна', '380573401082');
INSERT INTO commandant(commandant_id, last_name, first_name, middle_name, telephone_number) VALUES (7, 'Піпенко', 'Світлана', 'Миколаївна', '380573910283');

INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price) VALUES (1, 1, 1, 'Геліос', 'Харків', 'просп. Ювілейний', '52', 1, 800.00);
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, instagram) VALUES (2, 1, 2, 'Полюс', 'Харків',  'вул. Луї Пастера', '177', 2, 800.00, 'https://www.instagram.com/_polus2_khneu/?igshid=YmMyMTA2M2Y=');
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, instagram) VALUES (3, 1, 3, 'ІТ', 'Харків', 'вул. Цілиноградська', '40', 3, 800.00, 'https://www.instagram.com/hostelit3_hneu/?igshid=YmMyMTA2M2Y%3D');
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, instagram, telegram) VALUES (4, 1, 4, 'Міжнародний', 'Харків', 'вул. Цілиноградська', '30', 4, 800.00, 'https://www.instagram.com/4etverka_style/?igshid=YmMyMTA2M2Y%3D', 'https://t.me/+UtvxydkWGlb3Vt9x');
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, instagram) VALUES (5, 1, 5, 'П''ятірочка', 'Харків', 'пров. Інженерний', '4', 5, 800.00, 'https://www.instagram.com/fivetirochka_2.0/?igshid=YmMyMTA2M2Y%3D');
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, instagram) VALUES (6, 1, 6, 'Сінергія', 'Харків',  'вул. Клочківська', '216а', 6, 800.00, 'https://www.instagram.com/sinergia.house.6/?igshid=YmMyMTA2M2Y%3D');
INSERT INTO hostel(hostel_id, university_id, number, name, city, street, build, commandant_id, month_price, telegram) VALUES (7, 1, 7, 'Академічний', 'Харків',  'вул. Ак. Філіппова', '42', 7, 800.00, 'https://t.me/+Sp1tojwYbLaCvGJG');

INSERT INTO requisites(requisites_id, iban, university_id, organisation_code, service_id, payment_recognation)
VALUES (1, 'UA826482364382748327483', 1, 'ЄДРПОУ 753485385', 1, 'Призначення платежу: За проживання в гуртожитку. Назва Гуртожитку. ПІБ студента.');

INSERT INTO service_document(service_document_id, service_id, university_id, documents)
VALUES(1, 1, 1, '{"1": "Паспорт громадянина України (оригінал)",
                "2": "6 фотокарток 3х4",
                "3": "Результат флюрографії, з терміном видач до одного року (оригінал)",
                "4": "Квитанція про сплату за проживання не менше ніж за 4 місяці (копія)"}'::JSON);

INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (1, 1, 051, 'Економіка');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (2, 1, 121, 'Інженерія програмного забезпечення');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (3, 1, 122, 'Комп''ютерні науки');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (4, 1, 124, 'Системний аналіз');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (5, 1, 125, 'Кібербезпека');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (6, 1, 126, 'Інформаційні системи та технології');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (7, 1, 186, 'Видавництво та поліграфія');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (8, 6, 051, 'Економіка');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (9, 6, 053, 'Психологія');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (10, 6, 081, 'Право, освітня програма');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (11, 6, 232, 'Соціальне забезпечення');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (12, 6, 281, 'Публічне управління та адміністрування');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (13, 5, 073, 'Менеджмент');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (14, 5, 075, 'Маркетинг');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (15, 5, 022, 'Дизайн');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (16, 4, 072, 'Фінанси, банківська справа та страхування');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (17, 4, 071, 'Облік і оподаткування');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (18, 2, 011, 'Освітні, педагогічні науки');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (19, 2, 052, 'Політологія');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (20, 2, 061, 'Журналістика');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (21, 2, 073, 'Менеджмент');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (22, 2, 291, 'Міжнародні відносини, суспільні комунікації та регіональні студії');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (23, 2, 292, 'Міжнародні економічні відносини');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (24, 3, 051, 'Економіка');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (25, 3, 073, 'Менеджмент');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (26, 3, 076, 'Підприємництво, торгівля та біржова діяльність');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (27, 3, 241, 'Готельно-ресторанна справа');
INSERT INTO speciality(speciality_id, faculty_id, code, name) VALUES (28, 3, 242, 'Туризм');
