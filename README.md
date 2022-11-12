Kanboard's Official Website Repository
======================================

This website is a simple HTML static webpage to serve [Kanboard](https://kanboard.org/ "Visit website").

### How to add a new plugin to the list?

1. Update the [`plugins.json`](https://github.com/kanboard/website/blob/main/plugins.json) file
    - This file is used in the Kanboard interface Plugins Directory
    - Template:
    ```
    "MyPlugin": {
        "title": "MyPlugin",
        "version": "1.0.0",
        "author": "Plugin Developer Name",
        "license": "MIT",
        "description": "My plugin description",
        "homepage": "https://github.com/PluginDeveloperName/MyPlugin",
        "readme": "https://github.com/PluginDeveloperName/MyPlugin/blob/master/README.md",
        "download": "https://github.com/PluginDeveloperName/MyPlugin/releases/download/v1.0/MyPlugin-1.0.zip",
        "remote_install": true,
        "compatible_version": ">=1.2.20",
        "has_schema": false,
        "has_overrides": false,
        "has_hooks": false,
        "last_updated": "2022-11-10"
    }
    ```
2. Update the [`plugins.html`](https://github.com/kanboard/website/blob/main/plugins.html) file
    - This file is used in the Kanboard website [Plugins Directory](https://kanboard.org/plugins.html "View Plugins Directory")
    - Template:
    ```
    <dt><a href="https://github.com/pluginURL">Plugin Name</a></dt>
    <dd>
        <p>Enter your plugin description here</p>
        <p><em>By Your Name</em></p>
    </dd>
    ```
3. Send a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork "You must fork the main respoitory before you can create a Pull Request") of your changes
    - Once merged, this will automatically update the above files with your changes

------
### JSON Properties in `plugins.json`

**Mandatory**
- `compatible_version`
  - This is the latest stable version tested with your plugin
- `remote_install`
  - Allows people to install the plugin from the Kanboard user interface
- The **last property** should **NOT** have a comma at the end of the line
- The **last plugin** in the list should **NOT** have a comma at the end of the section (after the curly bracket)

**Optional**
- `has_schema`
  - `true` or `false`
  - Specify whether your plugin has any database changes
  - _Boolean type_
- `has_overrides`
  - `true` or `false`
  - Specify whether your plugin has any template overrides
  - _Boolean type_
- `has_hooks`
  - `true` or `false`
  - Specify whether your plugin has used any hooks
  - _Boolean type_
- `last_updated`
  - `November 2022`
  - Specify which date your plugin was last updated for general release
  - _ISO-8601 date type_

------
### Folder Structure

Your plugin archive **must contains a folder with the plugin name** (namespace), example:

```
MyPlugin-1.0.0.zip
└── MyPlugin
    ├── Assets
    ├── Controller
    ├── Helper
    ├── Locale
    │   └── fr_FR
    ├── Model
    ├── Template
    │   ├── ...
    ├── Test
    │   └── ...
    └── ...
```

The archive will be extracted by Kanboard into the folder `plugins` as `plugins/MyPlugin`.

#### Important Notes

- **Do not use the GitHub archive URL** for the download link.
  - Once unzipped, the directory structure is not the same as the one mentioned above. GitHub usually appends the branch name to the folder. **As a result, Kanboard won't be able to load the plugin**.
  - Make your own archive or set the `remote_install` field to `false`.
- If you release a new version of your plugin, always cross-check the version numbers of your archive filename and the url
