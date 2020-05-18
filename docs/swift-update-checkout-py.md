# Swift `update_checkout.py`

Swift uses the [update_checkout.py](https://github.com/apple/swift/blob/master/utils/update_checkout.py) file to manage repo states. The functionality is similar to certain `clowder` commands, but is baked into the Swift repository

## Initial Checkout

### `update_checkout.py`

```bash
mkdir swift-source
cd swift-source
git clone git@github.com:apple/swift.git
./swift/utils/update-checkout --clone-with-ssh
```

### `clowder`

```bash
mkdir swift-source
cd swift-source
clowder init git@github.com:JrGoodle/swift-clowder.git
clowder herd --parallel
```

## Checkout Version

### `update_checkout.py`

```bash
swift/utils/update-checkout --scheme swift-4.0-branch --reset-to-remote --clone --clean
swift/utils/update-checkout --scheme swift-4.0-branch --match-timestamp
```

### `clowder`

```bash
# Assuming repos were previously cloned
clowder link swift-4.0-branch
clowder reset --timestamp apple/swift
```
