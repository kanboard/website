# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "markdown",
#     "python-frontmatter",
# ]
# ///
import glob
import html
import json
import os
import shutil
import markdown
import frontmatter

OUTPUT_DIR = "output"
RELEASE_CONTENT_DIR = "releases"

STYLESHEET = """
body {
    font-family: sans-serif;
    color: #222;
    font-size: 110%;
    margin: 0 auto;
    max-width: 800px;
    padding-left: 5px;
    padding-right: 5px;
    padding-bottom: 20px;
}

body > header nav {
    margin-bottom: 20px;
    font-size: 18px;
}

body > header nav a {
    padding-right: 10px;
    display: inline-block;
}

h1 {
    font-weight: 400;
    font-size: 2em;
    line-height: 130%;
}

hr {
    height: 1px;
    border: none;
    background-color: #ddd;
}

a {
    color: #3366CC;
    border: 1px solid rgba(255, 255, 255, 0);
}

a:focus {
    outline: 0;
    color: red;
    text-decoration: none;
    border: 1px dotted #aaa;
}

a:hover {
    color: #333;
    text-decoration: none;
}

li {
    margin-bottom: 10px;
    line-height: 18px;
}

li ul {
    margin-top: 5px;
}

li a {
    overflow-wrap: break-word;
}

dt {
    margin-bottom: 8px;
    color: #555;
    font-size: 1.3em;
}

dt a {
    color: #3366CC;
    font-weight: 400;
}

dt a:hover,
dt a:focus {
    color: #555;
    text-decoration: none;
}

dd {
    margin-bottom: 15px;
    margin-left: 15px;
    border-left: 3px solid #eee;
    padding-left: 10px;
    line-height: 1.4em;
    color: #888;
    font-weight: 300;
}

dd ul {
    padding-left: 20px;
}

dd li {
    list-style-type: circle;
}

figure {
    margin: 0;
}

img {
    max-width: 100%;
    border: 1px solid #000;
}

code {
    background-color: #ebe8e8;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 0 4px;
    display: inline-block;
    line-height: 125%;
    margin: 0 2px;
}

input[type="text"] {
    border: 1px solid #ccc;
    padding: 3px;
    height: 22px;
    width: 250px;
    font-size: 99%;
    margin-bottom: 15px;
}

input[type="text"]:focus {
    color: #000;
    border-color: rgba(82, 168, 236, 0.8);
    outline: 0;
    box-shadow: 0 0 8px rgba(82, 168, 236, 0.6);
}

#plugins dt {
    font-size: 1.1em;
}

"""

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="images/png" href="/assets/img/favicon.png">
    <link rel="apple-touch-icon" href="/assets/img/touch-icon-iphone.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/assets/img/touch-icon-ipad.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/assets/img/touch-icon-iphone-retina.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/assets/img/touch-icon-ipad-retina.png">
    <link rel="alternate" type="application/atom+xml" title="Kanboard Releases" href="https://github.com/kanboard/kanboard/releases.atom">
    <title>{title}</title>
    <style>{stylesheet}</style>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/#donations">Donations</a>
            <a href="/releases.html">Releases</a>
            <a href="https://github.com/kanboard/">Repositories</a>
            <a href="/plugins.html">Plugins</a>
            <a href="https://docs.kanboard.org/">Docs</a>
            <a href="https://kanboard.discourse.group/">Forum</a>
            <a href="https://mastodon.social/@kanboard" title="@kanboard@mastodon.social">Mastodon</a>
        </nav>
    </header>
    <main>
        {body}
    </main>
</body>
</html>
"""

RELEASE_TEMPLATES = {
    "kanboard": """
<article>
    <header>
        <h1>{title}</h1>
        <nav class="breadcrumb">
            <a href="/">Home</a> &gt; <a href="/releases.html">Releases</a>
        </nav>
        <p><strong>Release date:</strong> <time datetime="{release_date}">{release_date_in_english}</time></p>
    </header>
    <h2>Changes</h2>
    {markdown_content}
    <h2>Links</h2>
    <ul>
        <li><a href="https://github.com/kanboard/kanboard/tree/{release_version}">https://github.com/kanboard/kanboard/tree/{release_version}</a></li>
        <li><a href="https://github.com/kanboard/kanboard/archive/refs/tags/{release_version}.zip">https://github.com/kanboard/kanboard/archive/refs/tags/{release_version}.zip</a></li>
        <li><a href="https://github.com/kanboard/kanboard/archive/refs/tags/{release_version}.tar.gz">https://github.com/kanboard/kanboard/archive/refs/tags/{release_version}.tar.gz</a></li>
    </ul>
    <h2>Docker Images</h2>
    <ul>
        <li><code>docker pull docker.io/kanboard/kanboard:{release_version}</code></li>
        <li><code>docker pull ghcr.io/kanboard/kanboard:{release_version}</code></li>
        <li><code>docker pull quay.io/kanboard/kanboard:{release_version}</code></li>
    </ul>
</article>
""",
    "python-api-client": """
<article>
    <header>
        <h1>{title}</h1>
        <nav class="breadcrumb">
            <a href="/">Home</a> &gt; <a href="/releases.html">Releases</a>
        </nav>
        <p><strong>Release date:</strong> <time datetime="{release_date}">{release_date_in_english}</time></p>
    </header>
    <h2>Changes</h2>
    {markdown_content}
    <h2>Links</h2>
    <ul>
        <li><a href="https://github.com/kanboard/python-api-client/tree/{release_version}">https://github.com/kanboard/python-api-client/tree/{release_version}</a></li>
        <li><a href="https://pypi.org/project/kanboard/{release_version}/">https://pypi.org/project/kanboard/{release_version}/</a></li>
    </ul>
</article>
""",
}


RELEASE_INDEX_TEMPLATE = """
<article>
    <header>
        <h1>{title}</h1>
        <nav class="breadcrumb">
            <a href="/">Home</a> &gt; <a href="/releases.html">Releases</a>
        </nav>
    </header>
    {release_list}
</article>
"""

INDEX_TEMPLATE = """
<section id="overview">
    <h1>Kanboard</h1>
    <p><em>Kanboard is a free and open source Kanban project management software.</em></p>
    <figure>
        <img src="/assets/img/board.png" alt="Kanban Board" title="Kanban Board">
    </figure>
    <ul>
        <li>Visualize your work</li>
        <li>Limit your work in progress to <strong>focus on your goal</strong></li>
        <li>Drag and drop tasks to manage your project</li>
        <li>Self-hosted</li>
        <li>Super simple installation</li>
    </ul>
</section>

<section id="features">
    <h2>Features</h2>
    <dl>
        <dt>Simple</dt>
        <dd>
            There is no fancy user interface, Kanboard focuses on simplicity and minimalism.
            The number of features is voluntarily limited.
        </dd>
        <dt>Visual and clear overview of your tasks</dt>
        <dd>
            The Kanban board is the best way to know the current status of a project because it's visual.
            It's very easy to understand, there is nothing to explain and no training is required.
        </dd>
        <dt>Drag and drop tasks between columns easily</dt>
        <dd>
            <img src="/assets/img/drag-and-drop.png" alt="Drag and Drop Tasks" title="Drag and Drop Tasks">
            <p>You can add, rename and remove columns at any time to adapt the board to your project.</p>
        </dd>
        <dt>Limit your work in progress to be more efficient</dt>
        <dd>
            <img src="/assets/img/task-limit.png" alt="Task Limit" title="Task Limit">
            <p>Avoid multitasking to stay focused on your work. When you are over the limit, the column is highlighted.</p>
        </dd>
        <dt>Search and filter tasks</dt>
        <dd>
            <img src="/assets/img/search.png" alt="Search and Filters" title="Search and Filters">
            <p>
                Kanboard has a very simple query language that offers the flexibility to find tasks in no time.
                Dynamically apply custom filters on the board to find what you need. Search by assignees, description, categories, due date, etc.
            </p>
        </dd>
        <dt>Tasks, subtasks, attachments and comments</dt>
        <dd>
            <ul>
                <li>Break down a task into sub-tasks, estimate the time or the complexity.</li>
                <li>Describe your task by using Markdown syntax.</li>
                <li>Add comments, documents, change the color, the category, the assignee, the due date.</li>
                <li>Move or duplicate your tasks across projects with one click.</li>
            </ul>
        </dd>
        <dt>Automatic actions</dt>
        <dd>
            <img src="/assets/img/automatic-actions.png" alt="Automatic Actions" title="Automatic Actions">
            <p>
                Don't repeat yourself! Automate your workflow with automated actions.
                Stop doing again and again the same thing manually.
                Change automatically the assignee, colors, categories and almost anything based on events.
            </p>
        </dd>
        <dt>Translated in 30+ languages</dt>
        <dd>
            Thanks to the different contributors, Kanboard is translated in Bahasa Indonesia, Bosnian,
            Brazilian Portuguese, Chinese, Chinese (Taiwan), Czech, Danish, Dutch, English, Finnish,
            French, German, Greek, Hungarian, Italian, Japanese, Korean, Malay, Norwegian, Polish,
            Portuguese, Romanian, Russian, Serbian, Spanish, Swedish, Thai, Turkish, Vietnamese.
        </dd>
        <dt>Multiple Authentication Backends</dt>
        <dd>
            Connect Kanboard to your LDAP/Active Directory server or use any OAuth2 provider (Google, GitHub, GitLab...).
        </dd>
        <dt>Free and Open Source software</dt>
        <dd>
            Kanboard is distributed under <strong>the permissive MIT License</strong>.
            The software is mainly developed by Frédéric Guillot, but more than 334+ people have contributed!
        </dd>
    </dl>
</section>

<section id="donations">
    <h2>Donations</h2>
    <p>If you are using Kanboard every day at your company, consider making a small donation.</p>

<h3>LiberaPay</h3>
<p><a href="https://liberapay.com/Kanboard/">Make a donation to Kanboard on LiberaPay</a>.</p>

<h3>PayPal</h3>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
        <input type="hidden" name="cmd" value="_s-xclick">
        <input type="hidden" name="hosted_button_id" value="RCQNQETNVHRJ4">
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" name="submit" alt="PayPal Donation">
    </form>
</section>
"""

PLUGINS_TEMPLATE = """
<div id="overview">
    <h1>Plugins</h1>
    <p>You can extend the features of Kanboard by installing some extensions.</p>
    <p>
        <em>
            There is no approval process and code review.
            This is up to you to validate the compatibility of these plugins with your Kanboard instance.
        </em>
    </p>
    <input
        type="text"
        id="pluginsfilter_input"
        onkeyup="pluginFilter()"
        placeholder="Search for plugin.."
        title="Search input for plugin filter"
    >
</div>
<div id="plugins"><dl id="pluginsfilter">{plugins_list}</dl></div>
<script>
    function pluginFilter() {{
        var input, filter, dl, dt, dd, a, b, i, pluginInfo;
        input = document.getElementById("pluginsfilter_input");
        filter = input.value.toUpperCase();
        dl = document.getElementById("pluginsfilter");
        dt = dl.getElementsByTagName("dt");
        dd = dl.getElementsByTagName("dd");
        pluginInfo = dl.getElementsByClassName("plugin-info");

        for (i = 0; i < dt.length; i++) {{
            a = dt[i].innerHTML;
            b = dd[i].innerHTML;
            if (
                a.toUpperCase().indexOf(filter) > -1 ||
                b.toUpperCase().indexOf(filter) > -1
            ) {{
                pluginInfo[i].style.display = "";
            }} else {{
                pluginInfo[i].style.display = "none";
            }}
        }}
    }}
    </script>
"""

PLUGIN_TEMPLATE = """
<div class="plugin-info">
    <dt>
        <a href="{homepage}">{title}</a> <small>(<a href="{download}">Download</a>)</small>
    </dt>
    <dd>
        <div class="plugin-description">{description}</div>
        <ul>
            <li><strong>Version:</strong> <code>{version}</code></li>
            <li><strong>Last updated:</strong> {last_updated}</li>
            <li><strong>Author:</strong> {author}</li>
            <li><strong>License:</strong> {license}</li>
            <li><strong>Kanboard compatibility:</strong> <code>{compatible_version}</code></li>
        </ul>
    </dd>
</div>
"""


def parse_markdown_file(filepath: str) -> frontmatter.Post:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        return frontmatter.loads(content)


def convert_markdown_to_html(content: str) -> str:
    return markdown.Markdown().convert(content)


def generate_html_document(title: str, content: str) -> str:
    return PAGE_TEMPLATE.format(
        stylesheet=STYLESHEET, title=html.escape(title), body=content
    ).strip()


def generate_index_document() -> str:
    return generate_html_document("Kanboard", INDEX_TEMPLATE)


def generate_release_document(metadata: dict, content: str) -> str:
    body = RELEASE_TEMPLATES[metadata["release_type"]].format(
        stylesheet=STYLESHEET,
        title=html.escape(metadata.get("title", "")),
        release_version=html.escape(metadata.get("release_version", "")),
        release_date=metadata.get("release_date"),
        release_date_in_english=metadata.get("release_date", "").strftime("%B %d, %Y"),
        markdown_content=convert_markdown_to_html(content),
    )
    return generate_html_document(metadata.get("title", ""), body)


def generate_release_index(release_docs: list) -> str:
    page_title = "Kanboard Releases"
    release_list = "<ul>"
    for doc in release_docs:
        release_url = f"/releases/{doc.metadata.get('release_type')}/{doc.metadata.get('release_version')}.html"
        release_list += f'<li><time datetime="{doc.metadata.get("release_date")}">{doc.metadata.get("release_date")}</time> - <a href="{release_url}">{doc.metadata.get("title")}</a></li>'
    release_list += "</ul>"
    body = RELEASE_INDEX_TEMPLATE.format(
        stylesheet=STYLESHEET,
        title=page_title,
        release_list=release_list,
    )
    return generate_html_document(page_title, body)


def generate_release_documents(content_dir: str, output_dir: str) -> None:
    release_docs = []
    for filepath in glob.glob(f"{content_dir}/*/*.md", recursive=True):
        print(f"Processing {filepath}")
        post = parse_markdown_file(filepath)
        html_content = generate_release_document(post.metadata, post.content)

        destination_folder = os.path.join(
            output_dir,
            "releases",
            str(post.metadata.get("release_type", "kanboard")),
        )
        os.makedirs(destination_folder, exist_ok=True)

        output_filepath = os.path.join(
            destination_folder,
            os.path.basename(filepath).replace(".md", ".html"),
        )
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        release_docs.append(post)

    print("Generate release index")
    release_docs.sort(key=lambda x: x.metadata.get("release_date"), reverse=True)

    with open(f"{output_dir}/releases.html", "w", encoding="utf-8") as f:
        f.write(generate_release_index(release_docs))


def generate_plugins_document(plugin_file: str) -> str:
    with open(plugin_file, "r") as f:
        plugins = json.load(f)

    plugins_html = []

    for _, plugin_info in plugins.items():
        plugin_html = PLUGIN_TEMPLATE.format(
            title=html.escape(plugin_info.get("title")),
            description=markdown.Markdown().convert(plugin_info.get("description")),
            author=html.escape(plugin_info.get("author")),
            license=html.escape(plugin_info.get("license")),
            compatible_version=html.escape(plugin_info.get("compatible_version")),
            homepage=html.escape(plugin_info.get("homepage")),
            version=html.escape(plugin_info.get("version")),
            last_updated=html.escape(plugin_info.get("last_updated")),
            download=html.escape(plugin_info.get("download")),
        )
        plugins_html.append(plugin_html)

    return generate_html_document(
        title="Kanboard Plugins",
        content=PLUGINS_TEMPLATE.format(plugins_list="\n".join(plugins_html)),
    )


def main():
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generate_release_documents(RELEASE_CONTENT_DIR, OUTPUT_DIR)

    print("Generate index page")
    with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(generate_index_document())

    print("Generate plugins page")
    with open(f"{OUTPUT_DIR}/plugins.html", "w", encoding="utf-8") as f:
        f.write(generate_plugins_document("plugins.json"))

    print("Copy assets")
    shutil.copytree("assets", f"{OUTPUT_DIR}/assets")
    shutil.copy("assets/img/favicon.ico", f"{OUTPUT_DIR}/favicon.ico")
    shutil.copy("plugins.json", f"{OUTPUT_DIR}/plugins.json")


if __name__ == "__main__":
    main()
