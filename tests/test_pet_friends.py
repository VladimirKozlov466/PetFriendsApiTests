from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Матроскин', animal_type='гулящий', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца на случай если список питомцев пуст
    pf.add_new_pet(auth_key, "Дядя Федор", "кот", "7", "images/cat1.jpg")

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Василевс', animal_type='Котяра', age=11):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца на случай если список питомцев пуст
    pf.add_new_pet(auth_key, "Дядя Федор", "кот", "7", "images/cat1.jpg")

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Пробуем обновить его имя, тип и возраст
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


def test_create_new_pet_simple_with_valid_data(name='Шарик', animal_type='Котопес', age='9'):
    """Проверяем что можно добавить питомца с корректными данными без фото питомца"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить фото для существующего питомца с корректными данными питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добаляем питомца без фото на случай если список пуст или последний питомец в списке имеет фото
    pf.create_new_pet_simple(auth_key, 'Новый', 'неопределенный', '7')

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и пытаемся добавить фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 200 и наличие фото
    assert status == 200
    assert result['pet_photo'] != ""


# --------- 12 test cases for final task module 19.2.3 --------------------

def test_get_api_key_for_user_not_existing(email="23324178@mail.ru", password="12345678"):
    """ Проверка возможности авторизации не существующего пользователя - negative"""

    # Пытаемся получить ключ api по несуществующему имени и паролю
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа отличается от 200 и в теле ответа нет ключа для авторизации
    assert status != 200
    assert 'key' not in result


def test_get_api_key_with_empty_email_and_password_fields(email="", password=""):
    """ Проверка возможности авторизации с пустыми полями email и password - negative"""

    # Пытаемся получить ключ api c пустыми полями для авторизации
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа отличается от 200 и в теле ответа нет ключа для авторизации
    assert status != 200
    assert 'key' not in result


def test_get_api_key_with_valid_user_email_and_wrong_password(email=valid_email, password="1565435484"):
    """ Потытка авторизации с валидным именем пользователя и неверным паролем - negative"""

    # Пытаемся получить ключ api c валидным именем пользователя и невалидным паролем
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа отличается от 200 и в теле ответа нет ключа для авторизации
    assert status != 200
    assert 'key' not in result


def test_add_new_pet_with_valid_data_and_big_photo(name='БольшойКот', animal_type='тестировочный', age='50',
                                                   pet_photo='images/size15mb.jpg'):
    """Проверка на ограничение размера фото питомца - positive"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся создать питомца с фото большого размера
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем что статус ответа = 200 и наличие имени, как результат что ограничения по
    # размеру фото нет
    assert status == 200
    assert result['name'] == name


def test_create_new_pet_simple_with_negative_age(name='Бобик', animal_type='Не_рожденный', age=-9):
    """Проверка добавления питомца с отрицательным значением возраста - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся создать питомца с отрицательным значением переменной возраста
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа отличается от 200 и в теле ответа нет имени питомца, что говорит
    # о том, что питомец с отрицательным возрастом не был добавлен
    assert status != 200
    assert 'name' not in result
    # Баг существует, питомец с отрицательным возрастом создается


def test_create_new_pet_simple_with_too_big_age(name='Крокодил', animal_type='мумия', age=1000):
    """Проверка добавления питомца с очень большим значением возраста - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся создать питомца с очень большим значением переменной возраста
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа отличается от 200 и в теле ответа нет имени питомца, что говорит
    # о том, что питомец с не реальным возрастом не был добавлен
    assert status != 200
    assert 'name' not in result
    # Баг существует, питомец с не реальным возрастом создается


def test_create_new_pet_simple_without_data(name='', animal_type='', age=''):
    """Проверка добавления питомца с пустыми данными всех переменных - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца с валидными данными на случай, если список пуст
    pf.create_new_pet_simple(auth_key, 'Новый', 'неопределенный', '7')

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и сохраняем в переменную
    pet_id_of_last_pet_before = my_pets['pets'][0]['id']

    # Пытаемся создать питомца с пустыми данными
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Снова запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Снова берём id первого питомца из списка и сохраняем в новую переменную
    pet_id_last_pet_after_creation = my_pets['pets'][0]['id']

    # Проверяем что статус ответа отличается от 200 и id первого питомца в списке не изменился
    # что говорит о том, что питомец со всеми пустыми полями не был создан
    assert status != 200
    assert pet_id_of_last_pet_before == pet_id_last_pet_after_creation
    # Тест не пройден, питомец без данных создается. Возможен баг


def test_successful_update_of_pet_name_by_changing_to_empty_name(name='', animal_type='собачка', age=22):
    """Проверка обновления данных валидного питомца данными другого питомца без имени - positive"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца с валидными данными на случай, если список пуст
    pf.create_new_pet_simple(auth_key, 'Новый', 'неопределенный', '7')

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём имя первого (которго собираемся заменить) питомца из списка и сохраняем в переменную
    name_of_last_pet_before = my_pets['pets'][0]['name']

    # Пытаемся обновить данные первого питомца данными нового питомца (у которго нет имени)
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Снова запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Снова берём имя первого питомца из списка и сохраняем в новую переменную
    name_last_pet_after_updating = my_pets['pets'][0]['name']

    # Проверяем что статус ответа отличается от 200, что имя первого питомца стало пустым и имя
    # первого питомца до обновления не равно имени первого питомца после обновления
    assert status == 200
    assert result['name'] == name
    assert name_of_last_pet_before != name_last_pet_after_updating
    # тест не выполнился, все переменные, кроме имени питомца были изменены. Имя питомца сохранилось
    # старым, не заменилось пустым значением. Возможно не баг.


def test_create_new_pet_simple_with_text_in_age_field(name='Енот', animal_type='Полоскун', age='млгнпм'):
    """Проверка добавления нового питомца с текстовым значением переменной возраста - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца с текстом в переменной возраст
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа отличается от 200 и что в теле ответа остутствует возраст,
    # что говорит о том, что питомец не был добавлен
    assert status != 200
    assert result['age'] != age
    # Тест не пройден, питомец с текстом в переменной возраст был добавлен. Возможен баг


def test_create_new_pet_simple_with_unsafe_data(name='SELECT * FROM users', animal_type='SELECT * FROM users',
                                                age='SELECT * FROM users'):
    """Попытка ввода не безопасных значений переменных name, animal_type и age - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца с не безопасными значениями в данных питомца
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа отличается от 200 и что в теле ответа остутствует имя, тип и возраст
    # питомца, что говорит о том, что питомец не был добавлен
    assert status != 200
    assert result['name'] != name
    assert result['animal_type'] != animal_type
    assert result['name'] != animal_type
    # Тест не пройден, питомец с с не безопасными значениями данных был добавлен. Не баг
    # Данный тест придумал не сам - получил информацию из вебинара


def test_add_new_pet_with_special_symbols_in_data(name='@#$%/?^+', animal_type='%/?^&*', age='@!$#\%^*',
                                                  pet_photo='images/cat1.jpg'):
    """Попытка ввода спецсимволов в значения переменных name, animal_type и age - positive"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца со значениями переменных в виде спецсимволов
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем успешность теста и соотвествие значенний переменных данным из тела ответа
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['name'] == animal_type
    # Тест пройден. Является ли это багом нет возможности ответить без ТЗ.
    # Также как и понять тест позитивный или негативный


def test_create_new_pet_simple_with_long_values_of_data(
        name='ывотмзытастысдштшщцатсзштСдтшфтсзшутасщжуТАжштфуащсшфсштжфщсшфшыстфшщСшфыщс',
        animal_type='тйсдцийтцудлстоытдфцшуашюиатжцфтдмсфтысфцуолтастцудасицуташгтцуагшсидцуаюси',
        age='тсшфгдтфшцутсмгшцустмдгцстмшфгтюстуысшдгтцушгстмдцушгтмсшзывсргшцусршвцсшщж'):
    """Проверка добавления нового питомца с большим количеством знаков в переменных - negative"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца с большим количеством знаков в переменных
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа отличается от 200 и что в теле ответа остутствует имя питомца,
    # что говорит о том, что питомец не был добавлен
    assert status != 200
    assert result['name'] != age
    # Тест не пройден, так как лежал сервер
