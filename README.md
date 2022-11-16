Kanboard's Official Website Repository
======================================

This website is a simple HTML static webpage to serve [Kanboard](https://kanboard.org/ "Visit website").

### How to add a new plugin to the list?

1. Update the [`plugins.json`](https://github.com/kanboard/website/blob/main/plugins.json) file
    - **This file is now sorted alphabetically**
      - Your plugin submission should be positioned in the file in alphabetical order **by plugin name**
    - This file is used in the Kanboard interface Plugins Directory
    - Template:
    ```
    "MyPlugin": {
        "author": "Plugin Developer Name",
        "compatible_version": ">=1.2.20",
        "description": "My plugin description",
        "download": "https://github.com/PluginDeveloperName/MyPlugin/releases/download/v1.0/MyPlugin-1.0.zip",
        "has_hooks": false,
        "has_overrides": false,
        "has_schema": false,
        "homepage": "https://github.com/PluginDeveloperName/MyPlugin",
        "is_type": "no",
        "last_updated": "2022-11-10",
        "license": "MIT",
        "readme": "https://github.com/PluginDeveloperName/MyPlugin/blob/master/README.md",
        "remote_install": true,
        "title": "MyPlugin",
        "version": "1.0.0"
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
- `is_type`
  - `plugin` or `action` or `theme` or `multi` or `connector`
  - Specify whether your plugin is:
    | Value | Type | Description |
    | ----- | ---- | ----------- |
    | `plugin` | Normal | _A plugin with no automatic actions_ |
    | `action` | Action | _A plugin for actions only_ |
    | `theme` | Normal | _A plugin for theming and styling of the interface_ |
    | `connector` | Normal | _A plugin connecting to third party services - may contain actions_ |
    | `multi` | Normal | _A plugin containing all or any combination of the above functions_ |
  - _String type_
- `last_updated`
  - `2022-11-15`
  - Specify which date your plugin was last updated for general release
  - _ISO-8601 date type_

------
### Folder Structure

Your plugin archive **must contains a folder with the plugin name** (namespace), example:

```
MyPlugin-1.0.0.zip      <= Zip archive filename stating release version
└── MyPlugin            <= Plugin name
    ├── Assets          <= Javascript/CSS files
    │   └── cs
    │   └── js
    ├── Controller
    ├── LICENSE         <= Plugin license
    ├── Helper
    ├── Locale
    │   └── fr_FR
    │   └── en_US
    |   ├── ...
    ├── Model
    ├── Plugin.php      <= Plugin registration file
    ├── README.md
    ├── Schema          <= Database migrations
    ├── Template        <= Template files
    │   ├── ...
    ├── Test            <= Unit tests
    │   └── ...
```

The archive will be extracted by Kanboard into the `plugins` folder as `plugins/MyPlugin`.

#### Important Notes

- **Do not use the GitHub archive URL** for the download link.
  - Once unzipped, the directory structure is not the same as the one mentioned above. GitHub usually appends the branch name to the folder. **As a result, Kanboard won't be able to load the plugin**.
  - Make your own archive or set the `remote_install` field to `false`.
- If you release a new version of your plugin, always cross-check the version numbers of your archive filename and the url
