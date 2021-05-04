"# Python_Telegram_Bot" 

Назначение проекта: создание телеграм бота, 
который предоставляет информацию о максимальных 
курсах покупки USD в Беларусбанке по стране. 

Как установить: установить Python 3, установить 
все необходимые модули.

Как запустить: запустить бота двойным кликом по 
файлу main.py

Обратите внимание! Файл с секретным токеном 
Secret Token должен 
быть в папке проекта. Туда вы можете поместить 
секретный токен для телеграм бота.

Краткое описание алгоритма на текущий момент:

при запуске телеграм бота и введении комманды 
/currency в поле сообщений бота,
бот запрашивает информацию с сайта Беларусбанк, 
выбирает максимальный курс покупки USD а так же
все отделения, которые покупают доллар 
по макимальному курсу. Эту информацию он и выводит 
пользователю.
В случае, если сервис Беларусбанк не доступен, бот 
рекомендует попробовать снова через некоторое время.
В алгоритме реализовано тривиальное кэширование при помощи SQL запросов.
