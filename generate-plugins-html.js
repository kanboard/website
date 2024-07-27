const fs = require("fs");
const Mustache = require("mustache");
const marked = require("marked");

// Read plugins.json
const pluginsData = JSON.parse(fs.readFileSync("plugins.json", "utf-8"));

// HTML template
const template = `
<div class="plugin-info">
  <dt>
    <a href="{{homepage}}">{{title}}</a>
  </dt>
  <dd>
      {{{description}}}
    <p>
      <em>
        <svg class="icon">
          <use xlink:href="#people-fill"></use>
        </svg>
        <b>By {{author}}</b>
      </em>
      <em>Version: {{version}}</em>
        • 
      <em>{{last_updated}}</em>
    </p>
    <p>
      <img
        alt="License: {{license}}"
        data-tippy-content="License: {{license}}"
        src="https://badgen.net/static/license/{{license}}/blue"
      />
      <img
        alt="Compatible Version: {{compatible_version}}"
        data-tippy-content="Compatible Version: {{compatible_version}}"
        src="https://badgen.net/static/KB/{{compatible_version}}/orange"
      />
    </p>
    <p>
      <a
        href="{{readme}}"
        >Readme</a
      >
    </p>
    <div class="structure-list">
      {{#has_schema}}
      <svg class="icon orange" data-tippy-content="This plugin using schema">
        <use xlink:href="#database-add-icon"></use>
      </svg>
      {{/has_schema}}
      {{^has_schema}}
      <svg
        class="icon green"
        data-tippy-content="This plugin not using any schema"
      >
        <use xlink:href="#database-check-icon"></use>
      </svg>
      {{/has_schema}}
      {{#has_hooks}}
      <svg class="icon orange" data-tippy-content="This plugin uses Kanboard Hooks">
        <use xlink:href="#hooks-add-icon"></use>
      </svg>
      {{/has_hooks}}
      {{^has_hooks}}
      <svg
        class="icon green"
        data-tippy-content="This plugin not using any Kanboard Hooks"
      >
        <use xlink:href="#hooks-check-icon"></use>
      </svg>
      {{/has_hooks}}
      {{#has_overrides}}
      <svg class="icon orange" data-tippy-content="This plugin override Kanboard data">
        <use xlink:href="#overrides-add-icon"></use>
      </svg>
      {{/has_overrides}}
      {{^has_overrides}}
      <svg
        class="icon green"
        data-tippy-content="This plugin not override any Kanboard data"
      >
        <use xlink:href="#overrides-check-icon"></use>
      </svg>
      {{/has_overrides}}
    </div>
  </dd>
</div>
`;

// Generate HTML for each plugin
let generatedContent = "";
for (const pluginKey in pluginsData) {
  const plugin = pluginsData[pluginKey];
  plugin.description = marked.parse(plugin.description); // Convert markdown to HTML
  generatedContent += Mustache.render(template, plugin);
}

// Read the existing plugins.html file
let pluginsHtml = fs.readFileSync("plugins.html", "utf-8");

// Replace the content between <!-- PLUGINS_LIST:START --> and <!-- PLUGINS_LIST:END -->
const startTag = "<!-- PLUGINS_LIST:START -->";
const endTag = "<!-- PLUGINS_LIST:END -->";
const startIndex = pluginsHtml.indexOf(startTag) + startTag.length;
const endIndex = pluginsHtml.indexOf(endTag);

if (startIndex !== -1 && endIndex !== -1) {
  const before = pluginsHtml.substring(0, startIndex);
  const after = pluginsHtml.substring(endIndex);
  pluginsHtml = before + "\n" + generatedContent + "\n" + after;
}

// Write the updated content back to plugins.html
fs.writeFileSync("plugins.html", pluginsHtml);

console.log("plugins.html has been updated successfully.");
