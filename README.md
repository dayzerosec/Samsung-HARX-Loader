# Samsung H-Arx Loader
Author: **dayzerosec**

_Loader for Samsung H-Arx plug-in binaries._

## Description
Binary Ninja loader for Samsung H-Arx plug-in binaries. It will try to load plug-ins and setup the correct load address and segment/section semantics.

## Installation
To install this plugin, go to Binary Ninja's plugin directory (can be found by going to Tools -> "Open Plugin Folder"), and run the following command:

```
git clone https://github.com/dayzerosec/Samsung-HARX-Loader
```

Note you'll probably need to restart Binary Ninja for the plugin to load.

## Usage
This loader is intended to be used with binaries extracted from firmware update tarbals, particularly the `BL` partition.

Simply load a H-Arx plugin binary to use the loader. Your view name on the top left of the disassembly pane should have an "H-Arx Plugin" prefix. If you encounter a problem trying to load something, please file an issue.

## Future Work / Potential Contribution
- [ ] Support more filetypes
- [ ] Better rust decompilation support?

## Notes

- Structures are reversed and may have inaccuracies. They may also change in future.

## License

This plugin is relesaed under a [MIT](LICENSE) license.