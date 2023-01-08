"""0011.

Revision ID: 0011
Revises: 0003
Create Date: 2022-12-29 20:53:17.945284+00:00

"""
from alembic import op

revision = "0011"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        sqltext="""
        INSERT INTO rector(rector_id, last_name, first_name, middle_name)
         VALUES (1, 'Пономаренко', 'Володимир', 'Степанович');
         """
    )
    op.execute(
        sqltext="""
        INSERT INTO university(
        university_id, university_name, short_university_name, rector_id
        ) VALUES (
        1,
        'Харківський національний економічний університет імені Семена Кузнеця',
        'ХНЕУ ім. С. Кузнеця',
         1
         );
        """
    )
    op.execute(sqltext="""
    INSERT INTO role(role_name) VALUES ('Студент');
    INSERT INTO role(role_name) VALUES ('Адміністратор');
    INSERT INTO role(role_name) VALUES ('Супер Адміністратор');

    INSERT INTO service(service_name) VALUES ('Поселення в гуртожиток');

    INSERT INTO status(status_id, status_name) VALUES (1, 'Схвалено');
    INSERT INTO status(status_id, status_name) VALUES (2, 'Відхилено');
    INSERT INTO status(status_id, status_name) VALUES (3, 'Розглядається');
    INSERT INTO status(status_id, status_name) VALUES (4, 'Скасовано');

    INSERT INTO dean(last_name, first_name, middle_name)
    VALUES ('Коц', 'Григорій', 'Павлович');
    INSERT INTO dean(last_name, first_name, middle_name)
     VALUES ('Птащенко', 'Олена', 'Валеріївна');
    INSERT INTO dean(last_name, first_name, middle_name)
     VALUES ('Шталь', 'Тетяна', 'Валеріївна');
    INSERT INTO dean(last_name, first_name, middle_name)
     VALUES ('Проноза', 'Павло', 'Володимирович');
    INSERT INTO dean(last_name, first_name, middle_name)
     VALUES ('Вовк', 'Володимир', 'Анатолійович');
    INSERT INTO dean(last_name, first_name, middle_name)
     VALUES ('Бріль', 'Михайло', 'Сергійович');

    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Інформаційних технологій', 'ІТ', 1, 1);
    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Міжнародних відносин і журналістики', 'МВЖ', 1, 2);
    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Міжнародної економіки і підприємництва', 'МЕП', 1, 3);
    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Фінансів і обліку', 'ФіО', 1, 4);
    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Менеджмента і маркетингу', 'МіМ', 1, 5);
    INSERT INTO faculty(name, shortname, university_id, dean_id)
    VALUES ('Економіки і права', 'ЕіП', 1, 6);

    INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (1, '0.75');
    INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (2, '1');
    INSERT INTO bed_place(bed_place_id, bed_place_name) VALUES (3, '1.5');

    INSERT INTO course(course_id, value) VALUES (1, 1);
    INSERT INTO course(course_id, value) VALUES (2, 2);
    INSERT INTO course(course_id, value) VALUES (3, 3);
    INSERT INTO course(course_id, value) VALUES (4, 4);
    INSERT INTO course(course_id, value) VALUES (5, 5);
    INSERT INTO course(course_id, value) VALUES (6, 6);

    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Ляшко', 'Надія', 'Михайлівна', '380577107851');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Любченко', 'Володимир', 'Віталійович', '380577792654');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Колосова', 'Олена', 'Іванівна', '380573368350');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Марченко', 'Тетяна', 'Федорівна', '380573367757');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Рилова', 'Лариса', 'Миколаївна', '380577021194');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Голубєва', 'Надія', 'Олександрівна', '380573401082');
    INSERT INTO commandant(last_name, first_name, middle_name, telephone_number)
    VALUES ('Піпенко', 'Світлана', 'Миколаївна', '380573910283');

    INSERT INTO hostel(
    university_id, number, name, city, street, build, commandant_id, month_price
    ) VALUES (1, 1, 'Геліос', 'Харків', 'просп. Ювілейний', '52', 1, 800.00);
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    instagram
    ) VALUES (
    1,
    2,
    'Полюс',
    'Харків',
    'вул. Луї Пастера',
    '177',
    2,
    800.00,
    'https://www.instagram.com/_polus2_khneu/?igshid=YmMyMTA2M2Y='
    );
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    instagram) VALUES (
    1,
    3,
    'ІТ',
    'Харків',
    'вул. Цілиноградська',
    '40',
    3,
    800.00,
    'https://www.instagram.com/hostelit3_hneu/?igshid=YmMyMTA2M2Y%3D'
    );
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    instagram,
    telegram
    ) VALUES (
    1,
    4,
    'Міжнародний',
    'Харків',
    'вул. Цілиноградська',
    '30',
    4,
    800.00,
    'https://www.instagram.com/4etverka_style/?igshid=YmMyMTA2M2Y%3D',
    'https://t.me/+UtvxydkWGlb3Vt9x'
    );
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    instagram
    ) VALUES (
    1,
    5,
    'П''ятірочка',
    'Харків',
    'пров. Інженерний',
    '4',
    5,
    800.00,
    'https://www.instagram.com/fivetirochka_2.0/?igshid=YmMyMTA2M2Y%3D'
    );
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    instagram
    ) VALUES (
    1,
    6,
    'Сінергія',
    'Харків',
    'вул. Клочківська',
    '216а',
    6,
    800.00,
    'https://www.instagram.com/sinergia.house.6/?igshid=YmMyMTA2M2Y%3D');
    INSERT INTO hostel(
    university_id,
    number,
    name,
    city,
    street,
    build,
    commandant_id,
    month_price,
    telegram
    ) VALUES (
    1,
    7,
    'Академічний',
    'Харків',
    'вул. Ак. Філіппова',
    '42',
    7,
    800.00,
    'https://t.me/+Sp1tojwYbLaCvGJG'
    );

    INSERT INTO requisites(
    requisites_id,
    iban,
    university_id,
    organisation_code,
    service_id,
    payment_recognition
    ) VALUES (
    1,
    'UA826482364382748327483',
    1,
    'ЄДРПОУ 753485385',
    1,
    'Призначення платежу: За проживання в гуртожитку. Назва Гуртожитку. ПІБ студента.'
    );
    """
               )
    op.execute(
        """
    INSERT INTO service_document(
    service_document_id, service_id, university_id, documents
    ) VALUES (1, 1, 1, '{
    "1": "Паспорт громадянина України (оригінал)",
    "2": "6 фотокарток 3х4",
    "3": "Результат флюрографії, з терміном видач до одного року (оригінал)",
    "4": "Квитанція про сплату за проживання не менше ніж за 4 місяці (копія)"
    }'::JSON);

    INSERT INTO speciality(faculty_id, code, name) VALUES (1, 051, 'Економіка');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 121, 'Інженерія програмного забезпечення');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 122, 'Комп''ютерні науки');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 124, 'Системний аналіз');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 125, 'Кібербезпека');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 126, 'Інформаційні системи та технології');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (1, 186, 'Видавництво та поліграфія');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (6, 051, 'Економіка');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (6, 053, 'Психологія');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (6, 081, 'Право, освітня програма');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (6, 232, 'Соціальне забезпечення');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (6, 281, 'Публічне управління та адміністрування');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (5, 073, 'Менеджмент');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (5, 075, 'Маркетинг');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (5, 022, 'Дизайн');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (4, 072, 'Фінанси, банківська справа та страхування');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (4, 071, 'Облік і оподаткування');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (2, 011, 'Освітні, педагогічні науки');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (2, 052, 'Політологія');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (2, 061, 'Журналістика');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (2, 073, 'Менеджмент');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (
    2, 291, 'Міжнародні відносини, суспільні комунікації та регіональні студії'
    );
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (2, 292, 'Міжнародні економічні відносини');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (3, 051, 'Економіка');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (3, 073, 'Менеджмент');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (3, 076, 'Підприємництво, торгівля та біржова діяльність');
    INSERT INTO speciality(faculty_id, code, name)
    VALUES (3, 241, 'Готельно-ресторанна справа');
    INSERT INTO speciality(faculty_id, code, name) VALUES (3, 242, 'Туризм');
    """
    )


def downgrade() -> None:
    pass
