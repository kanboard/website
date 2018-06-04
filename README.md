Kanboard's website
==================

This website is a simple HTML static webpage.

How to add a new plugin to the list?
------------------------------------

Update the files `plugins.json` and `index.html`, then send a pull-request.

- `compatible_version` is the latest stable version tested with your plugin.
- `remote_install` allows people to install the plugin from the Kanboard user interface.

Your plugin archive must contains a folder with the plugin name (namespace), example:

```
MyPlugin-1.0.0.zip
└── MyPlugin
    ├── Controller
    ├── Locale
    │   └── fr_FR
    ├── Template
    │   ├── ...
    ├── Test
    │   └── ...
    └── ...
```

The archive will be extracted by Kanboard into the folder `plugins` as `plugins/MyPlugin`.

Note: **Do not use the GitHub archive URL** for the download link.
Once unzipped, the directory structure is not the same as the one mentioned above.
**Kanboard won't be able to load the plugin**.
Make your own archive or set to `false` the `remote_install` field.
