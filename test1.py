import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(autouse=True)
def DriverChrome():
    pytest.driver = webdriver.Chrome(r"C:\Chromedriver\chromedriver.exe")
    pytest.driver.implicitly_wait(5)
    pytest.driver.maximize_window()
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


# Авторизация и переход к Моим питомцам
@pytest.fixture()
def login_and_open_my_pets():
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    pytest.driver.find_element(By.ID, 'email').send_keys('petmyfriends@mail.ru')
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
    pytest.driver.find_element(By.ID, 'pass').send_keys('petmyfriends')
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located([By.CSS_SELECTOR, 'button[''type="submit"]']))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()


# Получение информации о питомцах
@pytest.fixture()
def get_pets():
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))
    pet_list = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    returned_list = []
    for pets in pet_list:
        pet = pets.text.split()
        if type(pet) is not None:
            if len(pet) > 3:
                returned_list.append({'name': pet[0], 'breed': pet[1], 'age': pet[2]})
            else:
                returned_list.append({'name': 1, 'breed': 1, 'age': 1})
    yield returned_list


# Получение фото
@pytest.fixture()
def get_pets_photos():
    count = 0
    photo = pytest.driver.find_elements(By.XPATH, "//tbody/tr/th/img")
    for i in range(len(photo)):
        if 'data' in photo[i].get_dom_attribute('src'):
            count += 1
    yield count


# 1 Проверка на наличие всех все питомцев
def test_all_animals_are_present(login_and_open_my_pets, get_pets):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    pet_stat = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    quantity = int(pet_stat[0].text.split('\n')[1].split(' ')[1])
    assert quantity == len(get_pets)


# 2 Проверка на наличие у всех питомцев имени, возраста и породы
def test_pets_have_name_age_breed(login_and_open_my_pets, get_pets):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    for pet in get_pets:
        assert pet['name'] != '' and pet['age'] != '' and pet['breed'] != ''


# 3 Проверка на наличие фото у половины питомцев
def test_pets_have_photos(login_and_open_my_pets, get_pets, get_pets_photos):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    assert get_pets_photos >= len(get_pets) / 2


# 4 Проверка на наличии повторов в имени
def test_pets_names_no_duplicate(login_and_open_my_pets, get_pets):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    pets_name = []
    for pet in get_pets:
        if pet['name'] in pets_name:
            print("Contains")
        else:
            pets_name.append(pet)
    assert len(get_pets) == len(pets_name)


# 5 Проверка на наличии заполненных карточек питомцев (фото, возраст, имя и порода)
def test_check_pet_full_info(login_and_open_my_pets, get_pets, get_pets_photos):
    pytest.driver.implicitly_wait(5)
    images = pytest.driver.find_elements('css selector', '.card-deck .card-img-top')
    names = pytest.driver.find_elements('css selector', '.card-deck .card-img-top')
    descriptions = pytest.driver.find_elements('css selector', '.card-deck .card-img-top')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


# 6 Проверка на отсутствие повторяющихся питомцев
def test_pets_no_duplicate(login_and_open_my_pets, get_pets):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    pets = []
    for pet in get_pets:
        if pet not in pets:
            pets.append(pet)

    assert len(get_pets) == len(pets)


# 7 Проверка таблицы питомцев с ожиданием
def test_check_table_of_animals_with_waiting(login_and_open_my_pets, get_pets):
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    pet_stat = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    quantity = int(pet_stat[0].text.split('\n')[1].split(' ')[1])

    assert quantity == len(get_pets)
