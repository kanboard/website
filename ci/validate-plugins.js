const fs = require("fs");

// Load plugins.json
const inputFile = "plugins.json";
let plugins;

try {
  const rawData = fs.readFileSync(inputFile);
  plugins = JSON.parse(rawData);
} catch (error) {
  console.error(`Error reading or parsing ${inputFile}: ${error.message}`);
  process.exit(1);
}

// Convert the plugins object to an array of [key, value] pairs (key is plugin name)
const pluginEntries = Object.entries(plugins);

// Function to check alphabetical order of plugin names
const isAlphabetical = (array) => {
  for (let i = 0; i < array.length - 1; i++) {
    if (array[i][0].localeCompare(array[i + 1][0]) > 0) {
      return false;
    }
  }
  return true;
};

// Function to validate the structure of each plugin
const isValidPluginStructure = (plugin) => {
  const fields = {
    author: { type: "string" },
    compatible_version: { type: "string", regex: /^(>=|<=|>|<)?\d+(\.\d+)*$/ },
    description: { type: "string" },
    download: { type: "string", regex: /^https?:\/\/.+$/ },
    has_hooks: { type: "boolean" },
    has_overrides: { type: "boolean" },
    has_schema: { type: "boolean" },
    homepage: { type: "string", regex: /^https?:\/\/.+$/ },
    is_type: {
      type: "string",
      values: ["plugin", "action", "theme", "connector", "multi"],
    },
    last_updated: { type: "string", regex: /^\d{4}-\d{2}-\d{2}$/ },
    license: { type: "string" },
    readme: { type: "string", regex: /^https?:\/\/.+$/ },
    remote_install: { type: "boolean" },
    title: { type: "string" },
    version: { type: "string" },
  };

  for (const [field, { type, regex, values }] of Object.entries(fields)) {
    if (!plugin.hasOwnProperty(field)) {
      return { status: false, message: `Field "${field}" is missing.` };
    }

    if (typeof plugin[field] !== type) {
      return {
        status: false,
        message: `Field "${field}" should be of type "${type}".`,
      };
    }

    if (regex && !regex.test(plugin[field])) {
      return {
        status: false,
        message: `Field "${field}" does not match the required pattern.`,
      };
    }

    if (values && !values.includes(plugin[field])) {
      return {
        status: false,
        message: `Field "${field}" has an invalid value.`,
      };
    }
  }

  return { status: true };
};

// Check alphabetical order of plugin names
if (!isAlphabetical(pluginEntries)) {
  console.error("Error: Plugins are not in alphabetical order by name.");
  process.exit(1);
}

// Check structure of each plugin
let validationPassed = true;

pluginEntries.forEach(([pluginName, pluginData]) => {
  const structureStatus = isValidPluginStructure(pluginData);
  if (!structureStatus.status) {
    console.error(`Error: Plugin "${pluginName}" has an invalid structure.
Info: ${structureStatus.message}`);
    validationPassed = false;
  }
});

if (!validationPassed) {
  process.exit(1);
}

console.log("All plugins are in alphabetical order and have valid structure.");
