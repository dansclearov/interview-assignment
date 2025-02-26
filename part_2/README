# CVE-2020-36604 Hoek

Question 1: Is Hoek 6.1.3 Vulnerable to CVE-2020-36604?
No.

## Findings

I investigated the prototype pollution vulnerability in Hoek affecting versions prior to 8.5.1. Despite lacking the explicit fix, version 6.1.3 is unexpectedly immune to this vulnerability.

## Root Cause

- **Version 6.1.3**: Uses `Object.defineProperty()` exclusively, which treats `__proto__` as a regular property without modifying the prototype chain
- **Later vulnerable versions**: Use direct assignment (`newObj[key] = value`), which triggers prototype modification when `key` is `__proto__`

## The Fix

Later versions added an explicit check to skip the `__proto__` key:
```javascript
if (key === '__proto__') {
    continue;
}
```

## Recommendation

While my tests show version 6.1.3 is immune using `Object.defineProperty()`, this behavior could potentially vary in different JavaScript environments or Node.js versions. For complete confidence, I'd recommend both backporting the explicit check and comprehensive testing across all target environments.
