token = "954927126:AAE1xG9bvK6DwczwY_H6lwUTUu0KEbl7uiU"

URL_VK_FEED = 'https://api.vk.com/method/wall.get?domain=digitaldes&count=10&filter=owner&access_token={INSERT_YOUR_TOKEN}'
URL_VK_ALBUMS = 'https://api.vk.com/method/photos.getAlbums?domain=digitaldes&count=10&access_token={INSERT_YOUR_TOKEN}'
URL_VK_PHOTOS = 'https://api.vk.com/method/photos.get?domain=digitaldes&count=50&&access_token={INSERT_YOUR_TOKEN}&album_id='
URL_VK_ALBUM = 'https://vk.com/album-126132_'
FILENAME_VK = 'last_known_id.txt'
BASE_POST_URL = 'https://vk.com/wall-126132_'
URL_INST_FEED = 'https://api.instagram.com/v1/users/self/media/recent/?access_token={INSERT_YOUR_TOKEN}&count=10'
URL_HH_LIST = 'https://api.hh.ru/vacancies/?employer_id=4745&order=employer_active_vacancies_order&per_page=40'
URL_HH_EMP = 'https://spb.hh.ru/employer/4745'
URL_HH_SPEC = 'https://api.hh.ru/specializations/'
DATABASE_NAME = 'DD-bot.db'
BUS_SCHEDULE = 'Утренние автобусы (от станции метро Приморская):' \
               '\n - 8:45' \
               '\n - 9:00' \
               '\n - 9:15' \
               '\n - 9:30' \
               '\n - 9:45' \
               '\n - 10:00' \
               '\nВечерние автобусы (от бизнес центра):' \
               '\n - 18:30' \
               '\n - 18:45' \
               '\n - 19:00' \
               '\n - 19:15' \
               '\n - 19:30' \
               '\n - 19:45' \
               '\n - 20:00' \
               '\n - 20:20'
HELP = '\nПомимо работы с меню, вы также можете использовать следующие команды:'    \
       '\nНовости (/news) - отображает последние новости с сайта компании.'    \
       '\nVK (/vk) - отображает новости из группы.'    \
       '\nГаллерея (/gallery) - отображает последние альбомы из группы в контакте.' \
       '\nИнстаграм (/inst) - отображает последние фотографии из аккаунта.' \
       '\nЖизнь (/life) - отображает случайные фотографии из жизни компании.' \
       '\nНайти DD (/dd) - позволяет узнать адрес, телефон и сайт компании.' \
       '\nВакансии (/hh) - отображает последние вакансии компании.' \
       '\nНаписать отзыв (/feedback) - позволяет написать отзыв о приложении.' \
       '\nПодписка (/sub) - позволяет управлять подпиской на новости и фотографии.'

MOSCOW_ADDRESS = "Адрес Московского офиса"
SPB_ADDRESS = "Адрес Санкт-петербургского офиса"
SARATOV_ADDRESS = "Адрес Саратовского офиса"

MOSCOW_TEL = "Телефон Московского офиса"
SPB_TEL = "Телефон Санкт-петербургского офиса"
SARATOV_TEL = "Телефон Саратовского офиса"