# Авторизация с помощью JWT Password Bearer

## Описание проекта

- Сервис для регистрации и авторизации пользователя
- Реализована выдача _access_ и _refresh_ токенов
- Реализован _refresh access_ токена
- Реализован с использованием _FastAPI_ и _SQLAlchemy_
- База данных _PostgreSQL_
- Сервис запускается с помощью _docker-compose_

---

## Функционал

### /auth/register/ (POST) Регистрация пользователя

```markdown
# Регистрация нового пользователя и добавление его в БД
---
    Params:
        - username: str
        - email: EmailStr
        - password: str
---
    Returns:
        {
            "message": "Пользователь с ID ... зарегистрирован!"
        }
```

##### Example:

Request URL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/auth/register/?username=test2&email=test2%40test2.com&password=test2' \
  -H 'accept: application/json' \
  -d ''
```

Response body:

```json
{
  "message": "Пользователь с ID 4 зарегистрирован!"
}
```

### /auth/login/ (POST) Авторизация пользователя

```markdown
# Авторизация пользователя (выдача access токена)
---
    Params:
        - username: str
        - password: str
        - client_id: optional field
        - client_secret: optional field
---
    Returns:
        Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )
```

##### Example:

Request URL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test2&password=test2'
```

Response body:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdDIiLCJ1c2VybmFtZSI6InRlc3QyIiwiZW1haWwiOiJ0ZXN0MkB0ZXN0Mi5jb20iLCJleHAiOjE3NTYyMDA3NTAsImlhdCI6MTc1NjIwMDU3MCwianRpIjoiMTFjZDVjNDUtZmU1My00ZTkzLTgxYTItYWYzZGM3ODg3OTYyIn0.kvB_Mad6A7vtqI4yln1C9jz8QXwuPJnaKf5HYk1P7yeC4opGKsC3_p2A2NRMUAf8Yd3jthv7P8iVzuJnN5Yb6Oi3-Gum7SfF5cC2FOSKTK7qiiRAKiP6j21-h63tvST6h9RC7sN6x-dpf5zUQvhtQU5fXTxvmS1KigdMyXZh8GYHAgt3hQ-VEGP8qVWutrJY59tG1DBaH3yiVFnxxK6Ix2iTZE2OVyK-1xvcjKxSry1Qgrz6F_j45A1jMSPUTPbNvRLGDPusYzpC6BSl1I-ZXbzBiqzTXnj3hF2LETMVK1cpdiJM9N4tsas4_oh_PG_yayBAp1Q4U_ao6s18ay_Uvg",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsInN1YiI6InRlc3QyIiwiZXhwIjoxNzU4NzkyNTcwLCJpYXQiOjE3NTYyMDA1NzAsImp0aSI6IjBhNDE4NzMxLTBkZWQtNDhmMy1hOGYyLTJmMWFmYjJhYTYyZCJ9.IFFCsHUkXaEX0YVqB7WcBdKjw2V6jh7SJbDcGuIUGkxlIOyLFxM1_Xkwb7LLW0mB8oAS_q0ufEmYruiQkF6Zj0w4VY-Dzz9Q7-6UeBGXRts3A2kVANuvuI2unL5HKuDqIAmYqsaxWLw83xqqRDwzuniGXIdxedtzheGY8JmnEdmB4L0FA1Kq2mDVrEC_1QuNenyVQNBl-ESW1Jj7YJ3uktjEMCgmyqtLc6TLmaNkgXjbqj0T40f64Z9nLuYmY8VXq7JCrne7pVUIAzMAfm6FJ1h5cnTlB1nCu1Ow4pweEs2_Jh6KP00gzuGmKZC96Y2SbgDvJ5GJUCs_qcTDyVGHyg",
  "token_type": "Bearer"
}
```

### /auth/refresh/ (POST) Refresh access токен

```markdown
# Refresh access токена
---
    Params:
        - refresh_token: header_field
---
    Returns:
        Token(
            access_token=access_token,
            token_type="Bearer",
        )
```

##### Example:

Request URL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/auth/refresh/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsInN1YiI6InRlc3QyIiwiZXhwIjoxNzU4NzkyNTcwLCJpYXQiOjE3NTYyMDA1NzAsImp0aSI6IjBhNDE4NzMxLTBkZWQtNDhmMy1hOGYyLTJmMWFmYjJhYTYyZCJ9.IFFCsHUkXaEX0YVqB7WcBdKjw2V6jh7SJbDcGuIUGkxlIOyLFxM1_Xkwb7LLW0mB8oAS_q0ufEmYruiQkF6Zj0w4VY-Dzz9Q7-6UeBGXRts3A2kVANuvuI2unL5HKuDqIAmYqsaxWLw83xqqRDwzuniGXIdxedtzheGY8JmnEdmB4L0FA1Kq2mDVrEC_1QuNenyVQNBl-ESW1Jj7YJ3uktjEMCgmyqtLc6TLmaNkgXjbqj0T40f64Z9nLuYmY8VXq7JCrne7pVUIAzMAfm6FJ1h5cnTlB1nCu1Ow4pweEs2_Jh6KP00gzuGmKZC96Y2SbgDvJ5GJUCs_qcTDyVGHyg' \
  -d ''
```

Response body:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdDIiLCJ1c2VybmFtZSI6InRlc3QyIiwiZW1haWwiOiJ0ZXN0MkB0ZXN0Mi5jb20iLCJleHAiOjE3NTYyMDA4NjMsImlhdCI6MTc1NjIwMDY4MywianRpIjoiODMwYWE5NTgtNmZmMi00ZWIwLTg0ZDktMzJkN2U4NzFmY2QwIn0.lB2ddh9BW5mCfITvWmxNYZ7fUEeuywfgDlTSHpukznkqBUB0ihtpR2f_0syKEr_4RIzBVWKS8r7ddoTMACYMhlK2nF5xvQKpoQIJU8k1C-GxOOlBHMmpaKr3ZBESA4-H8vkhH35DjhY_Gokl4zJMzUX0N45dHI5LiJyR7j-6buiIZRBVxOZI0tPthhXDMab3I-lA3qSkM9fhmDIbbNP0m3sAKIuaZF9XHKbvvxn845XpeVjUUUNc2tglSkCrt_mBaOyZAW4udRv8rCcVgPM-pkineHN2XIegDqru4Hrx1w3Z7yPmee4Ab9xK2dBX1WgEu6SWJw4Fx73yoVBxwGDiEA",
  "token_type": "Bearer"
}
```

### /auth/me/ (GET) Получить информацию о себе

```markdown
# Получение информации о себе (по переданному токену в заголовке запроса)
---
    Params:
        - access_token: header field
---
    Returns:
        {
          "id": User ID,
          "username": Username,
          "email": User E-mail,
          "password": User password,
          "active": Active or unactive
        }

##### Example:

Request URL:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8080/auth/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdDIiLCJ1c2VybmFtZSI6InRlc3QyIiwiZW1haWwiOiJ0ZXN0MkB0ZXN0Mi5jb20iLCJleHAiOjE3NTYyMDA4NjMsImlhdCI6MTc1NjIwMDY4MywianRpIjoiODMwYWE5NTgtNmZmMi00ZWIwLTg0ZDktMzJkN2U4NzFmY2QwIn0.lB2ddh9BW5mCfITvWmxNYZ7fUEeuywfgDlTSHpukznkqBUB0ihtpR2f_0syKEr_4RIzBVWKS8r7ddoTMACYMhlK2nF5xvQKpoQIJU8k1C-GxOOlBHMmpaKr3ZBESA4-H8vkhH35DjhY_Gokl4zJMzUX0N45dHI5LiJyR7j-6buiIZRBVxOZI0tPthhXDMab3I-lA3qSkM9fhmDIbbNP0m3sAKIuaZF9XHKbvvxn845XpeVjUUUNc2tglSkCrt_mBaOyZAW4udRv8rCcVgPM-pkineHN2XIegDqru4Hrx1w3Z7yPmee4Ab9xK2dBX1WgEu6SWJw4Fx73yoVBxwGDiEA'
```

Response body:

```json
{
  "id": 4,
  "username": "test2",
  "email": "test2@test2.com",
  "password": "$2b$12$giPWy3V1VhSuSlEJmivJ5u5A9bjy4TZFpjsU6R9rGiFgvzeUyR7fa",
  "active": true
}
```

---

## Запуск проекта

#### Для успешной работы проекта необходимо выполнить следующие шаги:

1. Установить _Docker_ на свой компьютер, если он еще не установлен: [_Get Started with Docker_](https://www.docker.com/get-started)

2. Склонировать данный репозиторий

```bash
git clone https://github.com/VadimBarinov/FastAPI-JWT-Auth.git
```

3. Перейти в директорию с проектом

```bash
cd FastAPI-JWT-Auth
```

4. Выполнить команды для создания пары приватного и публичного ключа
```bash
mkdir certs;
cd certs;
openssl genrsa -out jwt-private.pem 2048;
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem;
cd ..;
```

5. Запустить приложение

```bash
docker-compose up
```

#### После запуска приложения будут созданы необходимые таблицы: `./db/create_table.sql`

#### Для доступа к базе данных используются следующие параметры:

- Database : bearer_test_api
- User : admin
- Password : qwerty1234
- Host : db (также есть проброс на localhost:5432)
- Port : 5432

---

## Подключение к проекту

После выполнения подготовительных действий проект будет доступен по адресу

```bash
http://localhost:8080/
```

Проект также будет доступен по внутреннему _ip_ адресу вашего компьютера

---

## Swagger UI

Документация (Swagger UI) будет доступна по адресу:

```bash
http://localhost:8080/docs
```

Также доступ будет по внутреннему _ip_ адресу

---
