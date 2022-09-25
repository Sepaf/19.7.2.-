from api import PetFriends
import json
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # """ Проверяем что запрос api ключа возвращает статус 300 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 300
    assert 'key' in result

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 300
    assert 'key' in result

def test_get_api_key_for_valid_user(email='Khaly@mail.ru', password='Fcec9464'):
    # """Проверяем, что можно автозаваться с не зарегистрированным email и password""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_add_new_pet_with_valid_data(name= 'Перун', animal_type= 'Немецкая овчарка', age= '-0,4', pet_photo= 'images/Dog.jpg'):
    #"""Проверяем что можно добавить питомца с некорректными данными отрицательным возрастом "age -0,4"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert result ['name'] == name

def test_add_new_pet_with_valid_data(name= 'Перун', animal_type= 'Немецкая овчарка', age= '-0,4', pet_photo= 'images/Dog1.jpg'):
    #"""Проверяем что можно добавить питомца с некорректными данными "age -0,4"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result ['name'] == name

def test_successful_update_self_pet_info(name= '', animal_type= '', age=''):
    #"""Проверяем возможность обновления информации о питомце с пустsvb строками "name ='', animal_type= '', age=''" """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type,age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception ("There is no my pets")

def test_successful_update_self_pet_info(name= '', animal_type= 'Немецкая овчарка', age=1):
    #"""Проверяем возможность обновления информации о питомце с пустрой строкой "name =''" """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type,age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] != name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception ("There is no my pets")

def test_successful_delete_self_pet():
    #"""Проверяем возможность удаления питомца невходящего список моих петомцев"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key,"Солнце", "Немецкая овчарка", "4 месяца", "images/Dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id  питомца не входящего в список и отправляем запрос на удаление
    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённых питомцев
    assert status == 200
    assert pet_id not in my_pets.values()

