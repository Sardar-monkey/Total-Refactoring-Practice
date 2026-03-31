from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Protocol, Callable, Optional
from urllib.parse import urlparse
import timeit


# -------------------------
# Value objects
# -------------------------

@dataclass(frozen=True)
class HttpRequest:
    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    timeout: int = 30
    retries: int = 3
    auth_token: Optional[str] = None
    proxy: Optional[str] = None
    ssl_verify: bool = True
    follow_redirects: bool = True
    cache_ttl: int = 0
    compression: Optional[str] = None


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: str = ""
    headers: dict[str, str] = field(default_factory=dict)


# -------------------------
# Builder
# -------------------------

class HttpRequestBuilder:
    _allowed_methods = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}

    def __init__(self, url: str):
        self._url = url
        self._method = "GET"
        self._headers: dict[str, str] = {}
        self._body: Optional[str] = None
        self._timeout = 30
        self._retries = 3
        self._auth_token: Optional[str] = None
        self._proxy: Optional[str] = None
        self._ssl_verify = True
        self._follow_redirects = True
        self._cache_ttl = 0
        self._compression: Optional[str] = None

    def method(self, method: str) -> "HttpRequestBuilder":
        self._method = method.upper()
        return self

    def header(self, key: str, value: str) -> "HttpRequestBuilder":
        self._headers[key] = value
        return self

    def headers(self, headers: dict[str, str]) -> "HttpRequestBuilder":
        self._headers.update(headers)
        return self

    def body(self, body: str) -> "HttpRequestBuilder":
        self._body = body
        return self

    def timeout(self, seconds: int) -> "HttpRequestBuilder":
        self._timeout = seconds
        return self

    def retries(self, count: int) -> "HttpRequestBuilder":
        self._retries = count
        return self

    def auth_token(self, token: str) -> "HttpRequestBuilder":
        self._auth_token = token
        return self

    def proxy(self, proxy_url: str) -> "HttpRequestBuilder":
        self._proxy = proxy_url
        return self

    def ssl_verify(self, enabled: bool) -> "HttpRequestBuilder":
        self._ssl_verify = enabled
        return self

    def follow_redirects(self, enabled: bool) -> "HttpRequestBuilder":
        self._follow_redirects = enabled
        return self

    def cache_ttl(self, seconds: int) -> "HttpRequestBuilder":
        self._cache_ttl = seconds
        return self

    def compression(self, codec: str) -> "HttpRequestBuilder":
        self._compression = codec
        return self

    def build(self) -> HttpRequest:
        parsed = urlparse(self._url)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Invalid URL: {self._url!r}")

        if self._method not in self._allowed_methods:
            raise ValueError(f"Unsupported HTTP method: {self._method}")

        if self._timeout <= 0:
            raise ValueError("timeout must be positive")

        if self._retries < 0:
            raise ValueError("retries cannot be negative")

        if self._cache_ttl < 0:
            raise ValueError("cache_ttl cannot be negative")

        if self._body is not None and self._method in {"GET", "HEAD"}:
            raise ValueError(f"{self._method} request should not contain a body")

        return HttpRequest(
            url=self._url,
            method=self._method,
            headers=deepcopy(self._headers),
            body=self._body,
            timeout=self._timeout,
            retries=self._retries,
            auth_token=self._auth_token,
            proxy=self._proxy,
            ssl_verify=self._ssl_verify,
            follow_redirects=self._follow_redirects,
            cache_ttl=self._cache_ttl,
            compression=self._compression,
        )


# -------------------------
# Request execution
# -------------------------

class RequestHandler(Protocol):
    def execute(self, req: HttpRequest) -> HttpResponse: ...


def send_http(req: HttpRequest) -> HttpResponse:

    return HttpResponse(
        status_code=200,
        body=f"OK: {req.method} {req.url}",
        headers={"Content-Type": "text/plain"},
    )


class HttpSender:
    def execute(self, req: HttpRequest) -> HttpResponse:
        return send_http(req)


# -------------------------
# Null Object
# -------------------------

class NullMiddleware:

    def __init__(self, inner: RequestHandler | None = None):
        self._inner = inner or HttpSender()

    def execute(self, req: HttpRequest) -> HttpResponse:
        return self._inner.execute(req)


# -------------------------
# Decorators
# -------------------------

class MiddlewareDecorator:
    def __init__(self, inner: RequestHandler):
        self._inner = inner

    def execute(self, req: HttpRequest) -> HttpResponse:
        return self._inner.execute(req)


class LoggingMiddleware(MiddlewareDecorator):
    def execute(self, req: HttpRequest) -> HttpResponse:
        print(f"[LOG] {req.method} {req.url}")
        result = self._inner.execute(req)
        print(f"[LOG] -> {result.status_code}")
        return result


class AuthMiddleware(MiddlewareDecorator):
    def execute(self, req: HttpRequest) -> HttpResponse:
        if not req.auth_token:
            return self._inner.execute(req)

        new_headers = deepcopy(req.headers)
        new_headers["Authorization"] = f"Bearer {req.auth_token}"

        new_req = HttpRequest(
            url=req.url,
            method=req.method,
            headers=new_headers,
            body=req.body,
            timeout=req.timeout,
            retries=req.retries,
            auth_token=req.auth_token,
            proxy=req.proxy,
            ssl_verify=req.ssl_verify,
            follow_redirects=req.follow_redirects,
            cache_ttl=req.cache_ttl,
            compression=req.compression,
        )
        return self._inner.execute(new_req)


class CompressMiddleware(MiddlewareDecorator):
    def execute(self, req: HttpRequest) -> HttpResponse:
        if req.compression and req.body is not None:
            new_headers = deepcopy(req.headers)
            new_headers["Content-Encoding"] = req.compression

            new_req = HttpRequest(
                url=req.url,
                method=req.method,
                headers=new_headers,
                body=req.body,  
                timeout=req.timeout,
                retries=req.retries,
                auth_token=req.auth_token,
                proxy=req.proxy,
                ssl_verify=req.ssl_verify,
                follow_redirects=req.follow_redirects,
                cache_ttl=req.cache_ttl,
                compression=req.compression,
            )
            return self._inner.execute(new_req)

        return self._inner.execute(req)


class RetryMiddleware(MiddlewareDecorator):
    def execute(self, req: HttpRequest) -> HttpResponse:
        attempts = req.retries + 1
        last_error: Exception | None = None

        for _ in range(attempts):
            try:
                return self._inner.execute(req)
            except Exception as exc:
                last_error = exc

        raise last_error  # type: ignore[misc]


class CacheMiddleware(MiddlewareDecorator):
    _cache: dict[tuple, HttpResponse] = {}

    @staticmethod
    def _make_key(req: HttpRequest) -> tuple:
        return (
            req.url,
            req.method,
            tuple(sorted(req.headers.items())),
            req.body,
            req.timeout,
            req.retries,
            req.auth_token,
            req.proxy,
            req.ssl_verify,
            req.follow_redirects,
            req.cache_ttl,
            req.compression,
        )

    def execute(self, req: HttpRequest) -> HttpResponse:
        if req.cache_ttl <= 0:
            return self._inner.execute(req)

        key = self._make_key(req)
        if key in self._cache:
            return self._cache[key]

        result = self._inner.execute(req)
        self._cache[key] = result
        return result


# -------------------------
# Composition helper
# -------------------------

MiddlewareFactory = Callable[[RequestHandler], RequestHandler]


def build_pipeline(*middlewares: MiddlewareFactory) -> RequestHandler:
    handler: RequestHandler = HttpSender()
    for middleware in reversed(middlewares):
        handler = middleware(handler)
    return handler


# -------------------------
# Example usage
# -------------------------

request = (
    HttpRequestBuilder("https://example.com/api")
    .method("POST")
    .header("Accept", "application/json")
    .body('{"name":"test"}')
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
print(response)