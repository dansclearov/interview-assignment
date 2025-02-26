# CVE-2023-45857 Axios

## Description

Leaks the confidential XSRF-TOKEN stored in cookies by including it in the HTTP header X-XSRF-Token when using `withCredentials: true`. Would allow attackers to perform CSRF despite the protection in place.

## Fix

The fix in commit [`96ee232bd3ee4de2e657333d4d2191cd389e14d0`](https://github.com/axios/axios/commit/96ee232bd3ee4de2e657333d4d2191cd389e14d0) removes the `config.withCredentials` condition which in turn makes it so XSRF token's are sent only for same-origin requests. There is also a test update to reflet this behavior.

## Steps to backport

1. Checked out Axios v0.21.0
```bash
git checkout v0.21.0
```

2. Applied the fix
before:
```javascript
var xsrfValue = (config.withCredentials || isURLSameOrigin(fullPath)) && config.xsrfCookieName ?
   cookies.read(config.xsrfCookieName) :
   undefined;
```
after:
```javascript
var xsrfValue = isURLSameOrigin(fullPath) && config.xsrfCookieName ?
   cookies.read(config.xsrfCookieName) :
   undefined;
```

3. Changed the test case in `test/specs/xsrf.spec.js` to expect the XSRF header to be undefined
