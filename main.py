from client_class import Client_DB
import psycopg2


if __name__ == '__main__':
    with psycopg2.connect(database='client_db', user='postgres', password='qazxswedc123') as db_con:
        with db_con.cursor() as curs:
            user = Client_DB(db_connector=db_con, cursor=curs)
            class_dict = {'1': user.create_db,
                          '2': user.new_client,
                          '3': user.add_number,
                          '4': user.update_client,
                          '5': user.delete_phone,
                          '6': user.delete_client,
                          '7': user.find_client}
            while (True):
                print()
                choice = str(input('Введите команду:\n'
                                   '1 - Создать структуру БД\n'
                                   '2 - Добавить нового клиента\n'
                                   '3 - Добавить телефон для существующего клиента\n'
                                   '4 - Изменить данные о клиенте\n'
                                   '5 - Удалить телефон для существующего клиента\n'
                                   '6 - Удалить существующего клиента\n'
                                   '7 - Найти клиента по его данным\n'
                                   '8 - Выйти из базы данных\n')
                             ).strip()
                if choice == '1':
                    class_dict['1']()
                if choice == '2':
                    class_dict['2']()
                if choice == '3':
                    class_dict['3']()
                if choice == '4':
                    class_dict['4']()
                if choice == '5':
                    class_dict['5']()
                if choice == '6':
                    class_dict['6']()
                if choice == '7':
                    class_dict['7']()
                if choice == '8':
                    break
                if choice not in class_dict.keys():
                    print('Команда введена некорректно. Попробуйте ещё раз')
                print()
