# Notes: curl for API work

This file contains documentation and practical examples for the curl command-line tool, intended for API debugging, testing and quick requests. Keep this separate from the main README.

## What is curl?
curl is a command-line tool to transfer data to or from a server using URL syntax. It supports many protocols (HTTP, HTTPS, FTP, etc.) and is widely used to interact with web APIs.

## Basic syntax
curl [options] <URL>

Example:
curl https://api.example.com/resource

## Commonly used options

- -X, --request <METHOD>
  Specify HTTP method (GET, POST, PUT, DELETE, PATCH...). curl chooses GET by default; use -X to override.

- -d, --data <DATA>
  Send data in a POST request. Automatically sets content-type to application/x-www-form-urlencoded unless you set headers.

  Example: curl -X POST -d "a=1&b=2" https://...

- --data-raw / --data-binary
  Send raw or binary data without curl stripping newlines or special characters.

- -H, --header <HEADER>
  Add a header (can be used multiple times).

  Example: curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" ...

- -u, --user <user:password>
  Basic authentication.

  Example: curl -u username:password https://...

- -b, --cookie
  Send cookies. -c to save cookies to a file.

- -F, --form <name=content>
  Submit multipart/form-data (useful for file uploads).

  Example: curl -F "file=@/path/to/file" https://...

- -I, --head
  Fetch HTTP headers only (send HEAD request).

- -L, --location
  Follow redirects. Useful when endpoints redirect to another URL.

- -v, --verbose
  Show request/response details (headers, TLS handshake). Good for debugging.

- -s, --silent
  Suppress progress meter and error messages (combine with -S to show errors).

- -o <file>
  Write output to a file instead of stdout.

- -O
  Save with remote filename.

- --max-time <seconds>
  Set a timeout for the whole operation.

- --insecure / -k
  Allow insecure server connections when using SSL (skip certificate verification). Use only for testing.

- --data-urlencode
  URL-encode data values automatically (useful for query-like data in POST).

- --compressed
  Request compressed response (adds Accept-Encoding: gzip).

## Working with JSON APIs

GET with query parameters:
curl "https://api.example.com/sum?a=3&b=5"

POST JSON:
curl -X POST https://api.example.com/sum \
  -H "Content-Type: application/json" \
  -d '{"a":3,"b":5}'

Note: Use single quotes in many shells to avoid interpolation; on Windows use double quotes and escape as needed.

POST with file contents as JSON:
curl -X POST https://api.example.com/ingest \
  -H "Content-Type: application/json" \
  --data-binary "@/path/to/file.json"

POST form data (application/x-www-form-urlencoded):
curl -X POST https://api.example.com/login \
  -d "username=alice&password=secret"

Multipart/form-data (file upload):
curl -X POST https://api.example.com/upload \
  -F "file=@./image.png" \
  -F "description=Sample image"

## Authentication and headers

Bearer token:
curl -H "Authorization: Bearer <TOKEN>" https://api.example.com/protected

Basic auth:
curl -u user:pass https://api.example.com/secure

Custom headers:
curl -H "X-Request-ID: 12345" -H "Accept: application/json" https://...

## Inspecting requests and responses

Verbose mode:
curl -v https://api.example.com

Show only response headers:
curl -I https://api.example.com

Show headers and response body (quiet progress):
curl -s -D - https://api.example.com

Save headers to file and body to another:
curl -s -D headers.txt -o body.bin https://...

## Handling redirects, retries and timeouts

Follow redirects:
curl -L http://short.url

Limit total time:
curl --max-time 10 https://api.example.com

Retry on transient failures:
curl --retry 3 --retry-delay 2 https://api.example.com

## Useful tips

- When troubleshooting, combine -v with -H to inspect exact headers sent.
- Use --data-binary when you need to send raw payload without modification.
- Use --data-urlencode for values that may contain special characters.
- Prefer -sS when scripting (silent but show errors).
- For reproducible API tests, script curl calls in shell scripts or use tools like httpie/Postman for richer UIs.

## Examples summary

1) Simple GET:
curl "https://api.example.com/users?limit=10"

2) POST JSON:
curl -X POST https://api.example.com/items -H "Content-Type: application/json" -d '{"name":"item"}'

3) Upload file:
curl -X POST https://api.example.com/upload -F "file=@./path/to/file.txt"

4) Authenticated request:
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me

5) Debugging:
curl -v -H "Content-Type: application/json" -d '{"a":1}' https://api.example.com/test

---

Keep this notes file for quick reference while developing and testing APIs locally or remotely.
