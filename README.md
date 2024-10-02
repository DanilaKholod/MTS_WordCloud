# Nuclear IT Hack 2024
Задача  **"МТС Линк. Использование ИИ в продукте"**
## Состав команды WISH NYA
1. Холод Данила - python-разработчик, ML-разработчик
2. Кондратьев Матвей - NLP-разработчик
3. Мельников Вадим - python-разработчик
4. Китаев Степан - NLP-разработчик
## Описание задачи
При проведении опросов важно не только собрать ответы, но и качественно проанализировать их, чтобы понять реальные мотивы ипредпочтения людей.
Представим, чтосотрудники отвечают на вопрос: **«Что мотивирует вас работать больше?»**

Ответы могут быть самыми разными: _«команда»_, _«коллеги»_, _«зарплата»_, _«бабосики»_, _«шеф»_, _«атмосфера»_,_«амбициозные задачи»_ и т.д. Сырые данные зачастую избыточны и включают множество синонимов, просторечий или даже нецензурной лексики
## Задача
Разработать систему на основе ИИ, которая анализирует список пользовательских ответов возвращает понятное и интерпретируемое облако слов.
## Описание решения
```
├── model.py - Модели NLP с препроцессингом, токенизациеЙ, векторизацией и кластеризацией отзывов
├── mts_bot.py - Чат-бот, который использует разработанную модель и строит облако слов
├── reviews_GPT.ipynb - JupyterNotebook, где был создан генератор отзывов
└── data - Сгенерированные ChatGPT отзывы, которые использовались для тестов
```
### 0. Цель
Целью данного проекта является создание модели для кластеризации текстовых данных отзывов с использованием методов обработки естественного языка (NLP). Мы стремимся разделить отзывы на группы по ключевым темам-причинам, которые мотивируют работников. Задача представляет собой кластеризацию усреднённых ембеддингов строк в многомерном пространстве, с последующим называнием кластера наиболее репрезентативным словом.

Целевое слово выбрано как **самое частотное**.

### 1. Входные данные
Датасет, используемый в проекте, представляет собой CSV-файл, содержащий строки размером от 3 до 12 слов и состоящий примерно из 2000 записей. Эти записи представляют собой разнообразные отзывы, которые могут быть полезны для анализа мнений пользователей, улучшения продуктов или услуг, а также для тренировки машинных моделей. 

![10ea067fabd87b4764661ba723213066](https://github.com/user-attachments/assets/2e6b3602-3ce9-4d7a-8a2f-f6acf60e1dc6)

Поскольку стояла задача создать уникальный и актуальный набор данных, было решено использовать `API OpenAI` для генерации отзывов. Этот подход позволил получить материалы, которые отражают различные аспекты пользовательского опыта и исключают дублирование, обеспечивая свежесть и разнообразие контента. Генератор отзывов был настроен так, чтобы создавать тексты, охватывающие различные тематики и стили, таким образом, каждая запись была индивидуальной и содержательной.

Однако из-за того, что `API OpenAI` является платным, а из России его купить невозможно, мы исхитрились и использовали библиотеку `g4f`, которая использует провайдеры сайтов, которые используют модели `chatGPT`, отправляют им запрос и ответ заносится в файл csv.

### 2. Препроцессинг
Была произведена стандартная подготовка данных. На препроцессинге слова были приведены к нижнему регистру, были убраны числовые символы, знаки пунктуации и стоп-слова. Также произведена токенизация полученных отзывов.

### 3. Векторизация
Векторизация предложений произведена с помощью усреднённых эмбеддингов слов с помощью модуля `Navec`, который предоставляет удобные и лёгкие эмбеддинги русских слов, что было оптимальным решением для нашей задачи. 

![togcc85ufq3b9rmshkwxvmqdnqo](https://github.com/user-attachments/assets/b986f560-80aa-485e-abae-9fe7449be058)

### 4. Кластеризация
Для кластеризации была выбрана модель `DBSCAN`, которая кластеризует объекты на основе плотностей распределения их в многомерном пространстве, а также хорошо определяет аномалии. Для оптимального параметра расстояния eps проведена кластеризация методом как средних для того же значения параметра К, что и в `DBSCAN`. Построен график дистанции между классами от количества объединённых классов, значение eps - координата по оси У точки излома графика. После этого было было выбрано самое частотное слово внутри кластера и количество которое оно встречалось. Для визуализации получившийся словарь передаётся дальше для построения облака слов.

![DBSCAN-Illustration svg](https://github.com/user-attachments/assets/ce5a6055-f8b0-4cca-9a72-83f946fbb5e4)

### 5. Облако слов
В процессе разработки чат-бота была выбрана библиотека `wordcloud` в Python для создания визуализаций текстовых данных. Она предлагает удобные методы для генерации облаков слов с возможностью настройки шрифтов, цветов и размеров. Учитывая корпоративный стиль МТС, мы использовали красные и белые оттенки, что позволило создать визуально привлекательные графики. Для улучшения семантической нагрузки облака слов применялись методы обработки естественного языка, такие как удаление стоп-слов.

### 6. Написание чат-бота
Разработка чат-бота осуществлялась с использованием библиотеки `telebot`. Для начала был получен токен для нашего бота в Telegram, после чего с помощью методов библиотеки были реализованы ключевые функции. Бот отвечает пользователям на текстовые сообщения, поддерживает загрузку файлов и предотвращает возможность одновременной загрузки нескольких файлов, чтобы избежать перегрузки системы. Кроме того, была интегрирована специализированная модель, позволяющая выводить облако слов пользователям в виде изображения формата PNG.

### 7. Запуск сервера
Запуск сервера для чат-бота на платформе `Beget` оказался достаточно простым и удобным процессом. После регистрации и выбора подходящего тарифа мы получили доступ к панели управления, где можно легко управлять настройками хостинга. Сначала мы загрузили все необходимые файлы бота, включая его код и зависимости, а затем настроили окружение для запуска. Beget поддерживает установку необходимых библиотек прямо из панели, что значительно облегчает процесс настройки.

![image](https://github.com/user-attachments/assets/d9460e48-1813-49d8-bdd2-20cb3637c204)

Мы также настроили автоматический запуск скрипта бота в фоновом режиме, чтобы обеспечить его постоянную доступность. Благодаря удобному интерфейсу и возможности выполнять команды через SSH, мы смогли быстро адаптировать конфигурацию под наши нужды.

### 8. Потенциальные улучшения
Потенциальные направления для улучшения:
- Увеличить размер данных
- Использовать более продвинутые методы векторизации, такие как FastText или BERT
  
## Результаты
[Генератор отзывов](https://colab.research.google.com/drive/1sV8wNab51B1PtvpeBL1pihr5jbn9spCC?usp=sharing#scrollTo=xp5SOVXZK_Sh) в GoogleColab, с помощью которого мы быстро получали различные отзывы

[Чат-бот](https://t.me/MTS_Word_Bot) в Telegram для загрузки в него файла csv с отзывами сотрудников, который на основе обученной ИИ модели генерирует облако слов.

**Пример 1**

![photo_2024-10-02_22-47-58](https://github.com/user-attachments/assets/7bc1b101-7fe2-4a5c-8dd0-97e635c0cc8a)

**Пример 2**

![photo_2024-10-02_22-46-04](https://github.com/user-attachments/assets/ced33eb0-2236-45ec-b770-450e0077ffc1)

**Пример 3**

![photo_2024-10-02_22-46-33](https://github.com/user-attachments/assets/4c27641d-93c6-42d7-a311-820b032766ad)


## Ресурсы
- Документация по [scikit-learn](https://scikit-learn.org/)
- Статья о TF-IDF: [TF-IDF Explanation](https://en.wikipedia.org/wiki/Tf–idf)
- Библиотека Наташа, обработка естественного языка на примере шоу ЧТО БЫЛО ДАЛЬШЕ: [YouTube](https://www.youtube.com/watch?v=cGrreUMhOk4)
- Ссылка с русскими эмбедингами НАТАША: [GitHub](https://github.com/natasha/navec)
- Колаб с тестированием разных моделей на сгенерированном датасете: [GoogleColab](https://colab.research.google.com/drive/1JPeCYjxRHlTYkp5-wS--CpBFDsqYg-uf?usp=sharing#scrollTo=rUDR2fy_9jfv)
