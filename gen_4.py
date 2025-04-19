import os
import markdown
import shutil
import frontmatter
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def initialize_directories(markdown_dir, build_dir, template_dir):
    """Initialize directories with sample files following the standardized structure."""
    print("Initializing project directories with sample files...")
    
    # Create markdown directory and sample files
    if not os.path.exists(markdown_dir):
        print(f"Creating {markdown_dir} directory...")
        os.makedirs(markdown_dir)
    
    # Create a sample markdown file with standardized frontmatter
    with open(os.path.join(markdown_dir, "index.md"), 'w', encoding='utf-8') as f:
        f.write("""---
title: Home Page
desc: Welcome to my static site generated with gen.py
template: default
---

# Welcome to My Site

This is a sample homepage created by gen.py.

## Features

- **Markdown** content with frontmatter
- **Jinja2** templates
- Static site generation
- Custom templates

Check out the [About](/about.html) page for more information.
""")
    print(f"Created a sample index file in {markdown_dir}/index.md")
    
    # Create an about page with standardized frontmatter
    with open(os.path.join(markdown_dir, "about.md"), 'w', encoding='utf-8') as f:
        f.write("""---
title: About
desc: Learn more about this project
template: default
---

# About This Project

This is a simple static site generator created with Python.

## How It Works

1. Write content in Markdown with frontmatter
2. Create templates in the templates directory
3. Run `gen.py` to build the site
4. The HTML files are generated in the build directory

[Return to Home](/index.html)
""")
    print(f"Created an about page in {markdown_dir}/about.md")

    # Create template directory
    if not os.path.exists(template_dir):
        print(f"Creating {template_dir} directory...")
        os.makedirs(template_dir)
    
    # Create a basic default template
    with open(os.path.join(template_dir, "template_default.html"), 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ desc }}">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            color: #333;
        }
        header {
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #eee;
        }
        nav {
            display: flex;
            gap: 1rem;
        }
        nav a {
            text-decoration: none;
            color: #0066cc;
        }
        nav a:hover {
            text-decoration: underline;
        }
        main {
            margin: 2rem 0;
        }
        footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            font-size: 0.9rem;
            color: #666;
        }
        pre {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }
        code {
            background-color: #f5f5f5;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    {% include 'partial_header.html' %}
    
    <main>
        {{ content }}
        
        {% if root_files %}
        <hr>
        <h2>Main Pages</h2>
        <ul>
            {% for file in root_files %}
            <li><a href="/{{ file.link }}">{{ file.title }}</a> - {{ file.desc }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        
        {% if blog_files %}
        <hr>
        <h2>Blog Posts</h2>
        <ul>
            {% for file in blog_files %}
            <li><a href="/{{ file.link }}">{{ file.title }}</a> - {{ file.desc }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </main>
    
    {% include 'partial_footer.html' %}
</body>
</html>""")
    print(f"Created default template in {template_dir}/template_default.html")
    
    # Create a blog template variation
    with open(os.path.join(template_dir, "template_blog.html"), 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ desc }}">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            color: #333;
        }
        header {
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #eee;
        }
        .blog-header {
            margin-bottom: 2rem;
        }
        nav {
            display: flex;
            gap: 1rem;
        }
        nav a {
            text-decoration: none;
            color: #0066cc;
        }
        nav a:hover {
            text-decoration: underline;
        }
        main {
            margin: 2rem 0;
        }
        footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            font-size: 0.9rem;
            color: #666;
        }
        pre {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }
        code {
            background-color: #f5f5f5;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-size: 0.9em;
        }
        .blog-list {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    {% include 'partial_header.html' %}
    
    <div class="blog-header">
        <h1>{{ title }}</h1>
    </div>
    
    <main>
        {{ content }}
        
        <div class="blog-list">
            <h3>Other Blog Posts</h3>
            <ul>
                {% for file in blog_files %}
                {% if file.link != link %}
                <li><a href="/{{ file.link }}">{{ file.title }}</a> - {{ file.desc }}</li>
                {% endif %}
                {% endfor %}
            </ul>
        </div>
    </main>
    
    {% include 'partial_footer.html' %}
</body>
</html>""")
    print(f"Created blog template in {template_dir}/template_blog.html")
    
    # Create a sample partial header template
    with open(os.path.join(template_dir, "partial_header.html"), 'w', encoding='utf-8') as f:
        f.write("""<header>
    <nav>
        <a href="/index.html">Home</a>
        <a href="/about.html">About</a>
        <a href="/blog/first-post.html">Blog</a>
    </nav>
</header>""")
    print(f"Created header partial in {template_dir}/partial_header.html")
    
    # Create a sample partial footer template
    with open(os.path.join(template_dir, "partial_footer.html"), 'w', encoding='utf-8') as f:
        f.write("""<footer>
    <p>&copy; 2025 - Generated with gen.py</p>
</footer>""")
    print(f"Created footer partial in {template_dir}/partial_footer.html")
    
    # Create an example blog post
    os.makedirs(os.path.join(markdown_dir, "blog"), exist_ok=True)
    with open(os.path.join(markdown_dir, "blog", "first-post.md"), 'w', encoding='utf-8') as f:
        f.write("""---
title: My First Blog Post
desc: An example of a blog post with the standardized frontmatter
template: blog
---

# My First Blog Post

This is an example blog post using the blog template.

## Markdown Features

You can use all standard Markdown features:

- Lists
- **Bold text**
- *Italic text*
- [Links](https://example.com)
- And more!

```python
# Even code blocks
def hello():
    print("Hello, world!")
```

Hope you enjoy using gen.py!
""")
    print(f"Created example blog post in {markdown_dir}/blog/first-post.md")
    
    print("Initialization complete!")

def validate_frontmatter(metadata, filepath):
    """Validate that required frontmatter fields are present."""
    required_fields = ['title', 'desc', 'template']
    missing_fields = [field for field in required_fields if field not in metadata]
    
    if missing_fields:
        print(f"Warning: {filepath} is missing required frontmatter fields: {', '.join(missing_fields)}")
        return False
    return True

def categorize_files(all_files, markdown_dir):
    """Categorize files based on their location in the directory structure."""
    file_categories = {
        'root_files': [],
        'blog_files': []
    }
    
    # Create additional categories for each subdirectory dynamically
    subdirs = set()
    for file_data in all_files:
        path = file_data['link']
        if '/' in path:  # If file is in a subdirectory
            subdir = path.split('/')[0]
            subdirs.add(subdir)
    
    # Initialize categories for each subdirectory
    for subdir in subdirs:
        file_categories[f'{subdir}_files'] = []
    
    # Categorize each file
    for file_data in all_files:
        path = file_data['link']
        
        # Root files (no subdirectory)
        if '/' not in path:
            file_categories['root_files'].append(file_data)
        else:
            # Files in subdirectories
            subdir = path.split('/')[0]
            file_categories[f'{subdir}_files'].append(file_data)
    
    return file_categories

def collect_all_files(markdown_dir):
    """Collect information about all markdown files in the directory and subdirectories."""
    all_files = []
    
    for root, _, files in os.walk(markdown_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, markdown_dir)
                
                # Calculate the HTML output path
                html_path = os.path.splitext(relative_path)[0] + '.html'
                
                try:
                    # Parse frontmatter
                    post = frontmatter.load(file_path)
                    metadata = post.metadata.copy()
                    
                    # Add link to the metadata
                    metadata['link'] = html_path
                    
                    # Add content to the metadata
                    metadata['content'] = post.content
                    
                    all_files.append(metadata)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    return all_files

def convert_markdown_to_html(markdown_path, html_path, template_dir, file_data):
    """Convert a markdown file to HTML using Jinja2 templates and parse frontmatter."""
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Parse the markdown file with frontmatter
    post = frontmatter.load(markdown_path)
    
    # Extract frontmatter data
    metadata = post.metadata
    
    # Validate frontmatter structure
    validate_frontmatter(metadata, markdown_path)
    
    # Convert markdown content to HTML
    md_extensions = ['extra', 'codehilite']
    html_content = markdown.markdown(post.content, extensions=md_extensions)
    
    # Determine which template to use
    template_name = metadata.get('template', 'default')
    try:
        template = env.get_template(f"template_{template_name}.html")
    except:
        print(f"Template 'template_{template_name}.html' not found, using default template.")
        try:
            template = env.get_template("template_default.html")
        except:
            print(f"Error: Default template not found in {template_dir}.")
            return False
    
    # Create template variables dictionary
    template_vars = metadata.copy()  # Start with frontmatter metadata
    
    # Add standard variables
    template_vars.update({
        'content': html_content,
        'filename': os.path.basename(markdown_path),
        'filepath': markdown_path
    })
    
    # Add all file categories
    template_vars.update(file_data)
    
    # Render the template
    output = template.render(**template_vars)
    
    # Write the HTML to the output file
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(output)
    
    return True

def process_directory(src_dir, build_dir, template_dir, file_data):
    """Process all markdown files in a directory and its subdirectories."""
    # Create the build directory if it doesn't exist
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    # Track how many files were processed
    files_processed = 0
    
    # Get all files and directories in the source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        
        # If the item is a directory, process it recursively
        if os.path.isdir(src_path):
            subdir_build = os.path.join(build_dir, item)
            if not os.path.exists(subdir_build):
                os.makedirs(subdir_build)
            files_processed += process_directory(src_path, subdir_build, template_dir, file_data)
        
        # If the item is a markdown file, convert it to HTML
        elif item.endswith('.md'):
            html_filename = os.path.splitext(item)[0] + '.html'
            html_path = os.path.join(build_dir, html_filename)
            print(f"Converting {src_path} to {html_path}")
            if convert_markdown_to_html(src_path, html_path, template_dir, file_data):
                files_processed += 1
    
    return files_processed

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Generate HTML files from Markdown using Jinja2 templates')
    parser.add_argument('--init', action='store_true', help='Initialize project with sample files')
    parser.add_argument('--markdown-dir', default='markdown', help='Directory containing markdown files (default: markdown)')
    parser.add_argument('--build-dir', default='build', help='Output directory for HTML files (default: build)')
    parser.add_argument('--template-dir', default='templates', help='Directory containing templates (default: templates)')
    
    args = parser.parse_args()
    
    # Set directories from arguments
    markdown_dir = args.markdown_dir
    build_dir = args.build_dir
    template_dir = args.template_dir
    
    # If --init flag is set, initialize the project with sample files
    if args.init:
        initialize_directories(markdown_dir, build_dir, template_dir)
        return
    
    # Check if markdown directory exists
    if not os.path.exists(markdown_dir):
        print(f"Error: Markdown directory '{markdown_dir}' does not exist.")
        print(f"Run 'python gen.py --init' to create sample directories and files.")
        return
    
    # Check if template directory exists
    if not os.path.exists(template_dir):
        print(f"Error: Template directory '{template_dir}' does not exist.")
        print(f"Run 'python gen.py --init' to create sample directories and files.")
        return
    
    # Recreate the build directory
    if os.path.exists(build_dir):
        print(f"Removing existing {build_dir} directory...")
        shutil.rmtree(build_dir)
    
    print(f"Creating {build_dir} directory...")
    os.makedirs(build_dir)
    
    # Collect information about all markdown files
    print("Collecting information about all markdown files...")
    all_files = collect_all_files(markdown_dir)
    print(f"Found {len(all_files)} markdown files.")
    
    # Categorize files based on directory structure
    file_data = categorize_files(all_files, markdown_dir)
    file_data['all_files'] = all_files
    
    # Display information about file categories
    for category, files in file_data.items():
        if category != 'all_files':
            print(f"  - {category}: {len(files)} files")
    
    # Process the markdown files
    print(f"Processing markdown files from {markdown_dir} to {build_dir} using templates from {template_dir}...")
    files_processed = process_directory(markdown_dir, build_dir, template_dir, file_data)
    
    if files_processed > 0:
        print(f"Conversion complete! {files_processed} files processed.")
    else:
        print(f"No markdown files found in {markdown_dir}. Please add .md files and run the script again.")
        print(f"You can run 'python gen.py --init' to create sample files.")

if __name__ == "__main__":
    main()
