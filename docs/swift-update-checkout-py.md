# Swift `update-checkout.py`

Swift uses the [update_checkout.py](https://github.com/apple/swift/blob/master/utils/update_checkout.py) file to manage repo states. The functionality is similar to certain `clowder` commands, but is baked into the Swift repository

## Initial Checkout

### `update_checkout.py`

```bash
mkdir swift-source
cd swift-source
git clone https://github.com/apple/swift.git
./swift/utils/update-checkout --clone-with-ssh
```

### `clowder`

```bash
mkdir swift-source
cd swift-source
clowder init git@github.com:JrGoodle/swift-clowder.git
clowder herd
```

## Checkout Version

### `update_checkout.py`

```bash
swift/utils/update-checkout --scheme swift-4.0-branch --reset-to-remote --clone --clean
swift/utils/update-checkout --scheme swift-4.0-branch --match-timestamp
```

### `clowder`

```bash
clowder link -v swift-4.0-branch
clowder reset --timestamp apple/swift
```

# Issues

https://bugs.swift.org/browse/SR-3800

https://github.com/apple/swift/commit/421c62ea2dd8d9b0b48cc97bfc998606686c1569#diff-ed037b68ad5e78641d57aebc2973448c
