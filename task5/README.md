# Задание 5: Builder + Decorator для HttpRequest

## Что было сделано

В этом задании я убрал два проблемы в коде:

- **Telescoping Constructor** у `HttpRequest`
- **Primitive Obsession** в системе middleware

---

## Что изменил

### 1. Builder для `HttpRequest`

Я вынес создание запроса в отдельный класс **`HttpRequestBuilder`**.

Теперь объект создается не через длинный конструктор, а через понятную цепочку методов:

- `method()`
- `header()`
- `headers()`
- `body()`
- `timeout()`
- `retries()`
- `auth_token()`
- `proxy()`
- `ssl_verify()`
- `follow_redirects()`
- `cache_ttl()`
- `compression()`
- `build()`

### Что это дает

- код стал читаемее
- не нужно помнить порядок 12 параметров
- проверка данных выполняется в `build()`
- проще добавлять новые поля

---

### 2. Decorator для middleware

Я заменил битовые флаги на отдельные middleware-классы.

Добавлены такие классы:

- `LoggingMiddleware`
- `AuthMiddleware`
- `CacheMiddleware`
- `RetryMiddleware`
- `CompressMiddleware`

Каждый middleware оборачивает следующий и может работать независимо от остальных.

### Что это дает

- middleware можно комбинировать в любом порядке
- легко добавлять новые обработчики
- код не нужно переписывать при расширении
- логика стала понятнее

---

### 3. Null Object

Я добавил **`NullMiddleware`**, чтобы не проверять значения на `None`.

### Что это дает

- меньше лишних проверок
- код проще
- цепочка middleware работает стабильно даже без дополнительных обработчиков

---

## Что получилось в итоге

Теперь система работает так:

1. `HttpRequestBuilder` создает и валидирует запрос
2. middleware собираются в цепочку
3. запрос проходит через нужные декораторы
4. код можно расширять без изменения старой логики

---

## Пример использования

```python
request = (
    HttpRequestBuilder("https://example.com/api")
    .method("POST")
    .header("Accept", "application/json")
    .body('{"name": "test"}')
    .timeout(20)
    .retries(2)
    .auth_token("secret-token")
    .compression("gzip")
    .build()
)

pipeline = build_pipeline(
    LoggingMiddleware,
    AuthMiddleware,
    CacheMiddleware,
    RetryMiddleware,
    CompressMiddleware,
)

response = pipeline.execute(request)