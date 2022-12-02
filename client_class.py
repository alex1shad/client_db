class Client_DB:
    def __init__(self, db_connector, cursor):
        self.db_connector = db_connector
        self.cursor = cursor

    def check_string(self, prefix, postfix):
        while (True):
            var = str(input(prefix)).strip()
            if var.isalpha() and var != '':
                return var.capitalize()
            else:
                print(postfix)

    def check_id(self, prefix):
        def id_test(prefix):
            while (True):
                var = str(input(prefix)).strip()
                if var.isdigit() and var != '':
                    return int(var)
                else:
                    print('id должен состоять только из цифр')
        client_id = id_test(prefix)
        while (True):
            self.cursor.execute("""
                SELECT EXISTS(SELECT client_id FROM client_info
                    WHERE client_id = %s);
                    """, ([client_id]))
            check_client_id = self.cursor.fetchone()
            self.db_connector.commit()
            if not check_client_id[0]:
                print('Клиента с таким id не существует')
                client_id = id_test(prefix)
            else:
                return client_id

    def check_phone(self, prefix):
        def phone_test(prefix):
            while (True):
                var = str(input(prefix)).strip()
                if var.isdigit() and var != '':
                    return int(var)
                else:
                    print('Телефонный номер должен состоять только из цифр')
        phone = phone_test(prefix)
        while (True):
            self.cursor.execute("""
                SELECT EXISTS(SELECT phone_number FROM phone
                    WHERE phone_number = %s);
                    """, ([phone]))
            check_phone_number = self.cursor.fetchone()
            self.db_connector.commit()
            if check_phone_number[0]:
                print('Указанный телефонный номер занят')
                phone = phone_test(prefix)
            else:
                return phone

    def check_email(self, prefix):
        def email_test(prefix):
            while (True):
                var = str(input(prefix)).strip()
                if var != '':
                    return var.lower()
        email = email_test(prefix)
        while (True):
            self.cursor.execute("""
                SELECT EXISTS(SELECT email FROM client_info
                    WHERE email = %s);
                    """, ([email]))
            check_client_email = self.cursor.fetchone()
            self.db_connector.commit()
            if check_client_email[0]:
                print('Указанный email занят')
                email = email_test(prefix)
            else:
                return email

    def check_client(self, var_name, func_name, var_list):
        print(f'Вам {var_name} клиента:')
        choice = str(input('Введите "Да" или "Нет":\n')).strip().lower()
        while (True):
            if choice == 'нет':
                break
            elif choice == 'да':
                if func_name == 'phone':
                    while (True):
                        var = str(input(var_list[0])).strip()
                        if var.isdigit() and var != '':
                            return int(var)
                        else:
                            print(var_list[1])
                elif func_name == 'email':
                    while (True):
                        var = str(input(*var_list)).strip()
                        if var != '':
                            return var.lower()
                else:
                    return func_name(*var_list)
            else:
                print('Ответ введен некорректно. Попробуйте ещё раз')
                choice = str(input('Введите "Да" или "Нет":\n')).strip().lower()

    def create_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_info(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(20) NOT NULL,
                last_name VARCHAR(20) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL
                );
                """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                phone_number INTEGER UNIQUE NOT NULL,
                client_id INTEGER REFERENCES client_info(client_id) ON DELETE CASCADE
                );
                """)
        self.db_connector.commit()
        print('Таблицы созданы')
        print('________________')

    def new_client(self):
        first_name = self.check_string('Введите имя клиента:\n',
                                       'Имя должно состоять только из букв')
        last_name = self.check_string('Введите фамилию клиента:\n',
                                      'Фамилия должна состоять только из букв')
        email = self.check_email('Введите email клиента:\n')
        self.cursor.execute("""
            INSERT INTO client_info(first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING client_id;
                """, (first_name, last_name, email))
        client_id = self.cursor.fetchone()
        self.db_connector.commit()
        print('Хотите добавить телефонный номер для клиента?')
        phone_choice = str(input('Введите "Да" или "Нет":\n')).strip().lower()
        while (True):
            if phone_choice == 'нет':
                break
            elif phone_choice == 'да':
                phone_number = self.check_phone('Введите телефонный номер клиента:\n')
                self.cursor.execute("""
                    INSERT INTO phone(phone_number, client_id)
                        VALUES (%s, %s);
                        """, (phone_number, client_id))
                self.db_connector.commit()
                break
            else:
                print('Ответ введен некорректно. Попробуйте ещё раз')
                phone_choice = str(input('Введите "Да" или "Нет":\n')).strip().lower()
        print('Данные клиента внесены в базу')
        print('________________')

    def add_number(self):
        client_id = self.check_id('Введите id клиента:\n')
        phone_number = self.check_phone('Введите телефонный номер клиента:\n')
        self.cursor.execute("""
            INSERT INTO phone(phone_number, client_id)
                VALUES (%s, %s);
                """, (phone_number, client_id))
        self.db_connector.commit()
        print(f'Для клиента {client_id} добавлен телефонный номер {phone_number}')
        print('________________')

    def update_client(self):
        def update_first_name(client_id):
            new_first_name = self.check_string('Введите новое имя клиента:\n',
                                               'Имя должно состоять только из букв')
            self.cursor.execute("""
                UPDATE client_info SET first_name = %s
                    WHERE client_id = %s;
                    """, (new_first_name, client_id))
            self.db_connector.commit()

        def update_last_name(client_id):
            new_last_name = self.check_string('Введите новую фамилию клиента:\n',
                                              'Фамилия должна состоять только из букв')
            self.cursor.execute("""
                UPDATE client_info SET last_name = %s
                    WHERE client_id = %s;
                    """, (new_last_name, client_id))
            self.db_connector.commit()

        def update_email(client_id):
            new_email = self.check_email('Введите новый email клиента:\n')
            self.cursor.execute("""
                UPDATE client_info SET email = %s
                    WHERE client_id = %s;
                    """, (new_email, client_id))
            self.db_connector.commit()

        def update_phone(client_id):
            phone_id_list = []
            self.cursor.execute("""
                SELECT phone_id FROM phone
                    WHERE client_id = %s;
                    """, (client_id,))
            for el in self.cursor.fetchall():
                phone_id_list.append(el[0])
            if len(phone_id_list) == 0:
                print('Для указанного клиента нет телефонных номеров в базе данных\n')
                return
            new_number = self.check_phone('Введите новый телефонный номер клиента:\n')
            phone_id = str(input(f'Введите id телефонного номера, подлежащий изменению, из списка\n'
                                 f'{phone_id_list}\n')).strip()
            while (True):
                if phone_id.isdigit() and int(phone_id) in phone_id_list:
                    phone_id = int(phone_id)
                    break
                else:
                    print('id телефонного номера введен некорректно\n'
                          'Введите номер, подлежащий изменению, ещё раз')
                    phone_id = str(input(f'{phone_id_list}\n'))
            self.cursor.execute("""
                UPDATE phone SET phone_number = %s
                    WHERE client_id = %s AND phone_id = %s;
                    """, (new_number, client_id, phone_id))
            self.db_connector.commit()

        func_dict = {'1': update_first_name,
                     '2': update_last_name,
                     '3': update_email,
                     '4': update_phone}
        while (True):
            input_choice = str(input('Укажите, какие данные о клиенте Вы хотите изменить:\n'
                                     '1 - Имя клиента;\n'
                                     '2 - Фамилия клиента;\n'
                                     '3 - Email клиента;\n'
                                     '4 - Номер телефона клиента;\n'
                                     '5 - Выйти из режима редактирования\n')
                               ).strip()
            if input_choice == '5':
                break
            elif input_choice not in func_dict.keys():
                print('Команда введена некорректно, попробуйте ешё раз\n')
            else:
                client_id = self.check_id('Введите id клиента\n')
                func_dict[input_choice](client_id)
                print('Изменения внесены')
                print('________________')

    def delete_phone(self):
        phone_id_list = []
        client_id = self.check_id('Введите id клиента:\n')
        self.cursor.execute("""
            SELECT phone_id FROM phone
                WHERE client_id = %s;
                """, (client_id,))
        for el in self.cursor.fetchall():
            phone_id_list.append(el[0])
        if len(phone_id_list) == 0:
            print('Для указанного клиента нет телефонных номеров в базе данных\n')
            return
        phone_id = str(input(f'Введите id телефонного номера, подлежащий удалению, из списка\n'
                             f'{phone_id_list}\n')).strip()
        while (True):
            if phone_id.isdigit() and int(phone_id) in phone_id_list:
                phone_id = int(phone_id)
                break
            else:
                print('id телефонного номера введен некорректно\n'
                      'Введите номер, подлежащий удалению, ещё раз')
                phone_id = str(input(f'{phone_id_list}\n'))
        self.cursor.execute("""
            DELETE FROM phone
                WHERE phone_id = %s;
                """, (phone_id,))
        self.db_connector.commit()
        print('Телефонный номер удалён')
        print('________________')

    def delete_client(self):
        client_id = self.check_id('Введите id клиента:\n')
        self.cursor.execute("""
            DELETE FROM client_info
                WHERE client_id = %s;
                """, (client_id,))
        self.db_connector.commit()
        print('Сведения о клиенте удалены')
        print('________________')

    def find_client(self):
        print('Введите данные о клиенте:')
        first_name = self.check_client('известно имя', self.check_string,
                                       ['Введите имя клиента:\n',
                                        'Имя должно состоять только из букв'])
        last_name = self.check_client('известна фамилия', self.check_string,
                                      ['Введите фамилию клиента:\n',
                                       'Фамилия должно состоять только из букв'])
        email = self.check_client('известен email', 'email', ['Введите email клиента:\n'])
        phone_number = self.check_client('известен телефонный номер', 'phone',
                                         ['Введите телефонный номер клиента:\n',
                                          'Телефонный номер должен состоять только из цифр'])
        print()
        first_and = ''
        second_and = ''
        third_and = ''
        if first_name or last_name or email or phone_number:
            if first_name:
                first_name = f"first_name = '{first_name}'"
            else:
                first_name = ''
            if last_name:
                last_name = f"last_name = '{last_name}'"
            else:
                last_name = ''
            if email:
                email = f"email = '{email}'"
            else:
                email = ''
            if phone_number:
                phone_number = f"phone_number = {phone_number}"
            else:
                phone_number = ''
            if first_name and (last_name or email or phone_number):
                first_and = 'AND'
            if last_name and (email or phone_number):
                second_and = 'AND'
            if email and phone_number:
                third_and = 'AND'
            resp = 'SELECT ci.client_id, first_name, last_name, email, phone_number FROM client_info ci ' \
                        'LEFT JOIN phone p ON p.client_id = ci.client_id ' \
                            f'WHERE {first_name} {first_and} {last_name} {second_and} ' \
                                    f'{email} {third_and} {phone_number};'
            self.cursor.execute(f"""{resp}""")
            client_info_result = self.cursor.fetchall()
            self.db_connector.commit()
            id_list = set([el[0] for el in client_info_result])
            if len(id_list) == 1:
                print('Данные о клиенте')
                print('________________')
            elif len(id_list) > 1:
                print('Данные о клиентах')
                print('________________')
            else:
                print('Клиента с такими данными не найдено. '
                      'Проверьте корректность данных или сузьте критерии для поиска')
                print('________________')
            for client_id in id_list:
                phone_number_list = []
                for el in client_info_result:
                    if client_id == el[0]:
                        first_name = el[1]
                        last_name = el[2]
                        email = el[3]
                        phone_number_list.append(el[4])
                print(f'id клиента: {client_id}\n'
                      f'Имя клиента: {first_name}\n'
                      f'Фамилия клиента: {last_name}\n'
                      f'email клиента: {email}\n'
                      f'Телефонные номера клиента: {phone_number_list}')
                print('________________')
