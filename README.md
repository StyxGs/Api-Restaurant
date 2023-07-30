<h2>ДЗ №1</h2>

<p>Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.</p>
<p>Зависимости:</p>
<ul>
<li>У меню есть подменю, которые к ней привязаны.</li>
<li>У подменю есть блюда.</li>
</ul>
<p>Условия:</p>
<ul>
<li>Блюдо не может быть привязано напрямую к меню, минуя подменю.</li>
<li>Блюдо не может находиться в 2-х подменю одновременно.</li>
<li>Подменю не может находиться в 2-х меню одновременно.</li>
<li>Если удалить меню, должны удалиться все подменю и блюда этого меню.</li>
<li>Если удалить подменю, должны удалиться все блюда этого подменю.</li>
<li>Цены блюд выводить с округлением до 2 знаков после запятой.</li>
<li>Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.</li>
<li>Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.</li>
<li>Во время запуска тестового сценария БД должна быть пуста.</li>
</ul>

<h3>Инструкция по запуску приложения:</h3>

<ol>
<li>Клонировать репозиторий: git clone https://github.com/StyxGs/Y_lab.git</li>
<li>Перейти в папку куда скопирован проект, там должен находить файл docker-compose.yml</li>
<li>Выполнить команду docker-compose up -d</li>
<li>Апи будет доступно по адресу: http://localhost:8000</li>
</ol>

<h3>Тестирование. Инструкция по запуску.</h3>
<p>Для тестов я создал отдельный yml файл.</p>
<ol>
<li>Перейти в папку куда скопирован проект, там должен находить файл docker-compose-test.yml</li>
<li>Команда для запуска тестов: docker-compose -f docker_compose_test.yml up -d</li>
<li>Для того чтобы посмотреть логи о прохождение тестов: docker-compose -f docker_compose_test.yml logs -f api_test</li>
</ol>