archive_html_content: str = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% for post in posts %}
        <h3>{{ post.metadata.title }}</h3>
        <br>
        <br>
    {% endfor %}
</body>
</html>
'''

index_html_content: str = '''
<!doctype html>
<html>
    <head>
        <title>{{ config.site_title }}</title>
    </head>

    <body>
        <h1>{{ config.site_title }}</h1>
        {%- for post in posts -%}
            <h1>{{ post.metadata.title }}</h1>
            {{ post.content }}
        {% endfor %}
    </body>
</html>
'''

page_html_content = '''
<!doctype html>
<html>
    <head>
        <title>{{ config.site_title }}</title>
    </head>
    <body>
        <h1>{{ this.metadata.title }}</h1>
        {{ this.content }}
    </body>
</html>
'''

post_html_content = '''
<!doctype html>
<html>
    <head>
        <title>{{ config.site_title }}</title>
    </head>
    <body>
        <h1>{{ this.metadata.title }}</h1>
        {{ this.content }}
    </body>
</html>
'''


def rb_create_default_theme(theme_dir: str) -> None:
    with open(theme_dir + 'index.html', 'w') as i_file:
        i_file.write(index_html_content)
    with open(theme_dir + 'archive.html', 'w') as i_file:
        i_file.write(archive_html_content)
    with open(theme_dir + 'page.html', 'w') as i_file:
        i_file.write(page_html_content)
    with open(theme_dir + 'post.html', 'w') as i_file:
        i_file.write(index_html_content)