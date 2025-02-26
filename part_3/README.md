# CVE-2021-23434 Object-Path

## Description

Type confusion vulnerability where `currentPath === '__proto__'` returns false if `currentPath` is `['__proto__']`, leading to prototype pollution bypassing CVE-2020-15256.

## Backporting to 0.11.5

The commit that fixes this is [`7bdf4abefd102d16c163d633e8994ef154cab9eb`](https://github.com/mariocasciaro/object-path/commit/7bdf4abefd102d16c163d633e8994ef154cab9eb).

1. The tag 0.11.5 was missing, so I checked out the commit that bumped the version in the package.json, namely [`ebc5e2c7d435ce0535bc155e73952c38d30c6e20`](https://github.com/mariocasciaro/object-path/commit/ebc5e2c7d435ce0535bc155e73952c38d30c6e20).
```bash
git checkout v0.21.0
```

2. Applied the fix:

**Before:**
```javascript
var currentPath = path[0];
var currentValue = getShallowProperty(obj, currentPath);
```

**After:**
```javascript
var currentPath = path[0];
if (typeof currentPath !== 'string' && typeof currentPath !== 'number') {
    currentPath = String(currentPath)
}
var currentValue = getShallowProperty(obj, currentPath);
```

3. Created the patch file:
```bash
git diff > object-path_0.11.5_patch.diff
```
