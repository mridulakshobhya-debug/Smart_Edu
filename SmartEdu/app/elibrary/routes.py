# E-Library Routes
from flask import Blueprint, render_template, request
from flask_login import login_required
from markupsafe import Markup
import markdown
import re

elibrary = Blueprint('elibrary', __name__)

def add_table_styles(html):
    """Add inline styles to markdown-generated tables"""
    # Add styles to table element
    html = re.sub(
        r'<table>',
        '<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0; border: 2px solid #ddd; background: #f9f9f9;">',
        html
    )
    
    # Add styles to thead
    html = re.sub(
        r'<thead>',
        '<thead style="background: #e8e8e8;">',
        html
    )
    
    # Add styles to th elements
    html = re.sub(
        r'<th>',
        '<th style="padding: 1rem; text-align: left; font-weight: 700; border-bottom: 3px solid #333; color: #000;">',
        html
    )
    
    # Add styles to td elements
    html = re.sub(
        r'<td>',
        '<td style="padding: 0.75rem 1rem; color: #000; border-bottom: 1px solid #ddd;">',
        html
    )
    
    # Add styles to tr elements in tbody (alternating colors)
    tbody_match = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
    if tbody_match:
        tbody_content = tbody_match.group(1)
        tr_count = 0
        def replace_tr(match):
            nonlocal tr_count
            tr_count += 1
            bg_color = '#ffffff' if tr_count % 2 == 1 else '#f5f5f5'
            border = 'border-bottom: 1px solid #ddd;' if 'tbody' in html else ''
            return f'<tr style="background: {bg_color}; {border}">'
        
        new_tbody = re.sub(r'<tr>', replace_tr, tbody_content)
        html = html.replace(tbody_content, new_tbody)
    
    return html

# Mock book data with markdown chapter content
BOOKS = {
    'algorithms': {
        'title': 'Introduction to Algorithms',
        'author': 'T.H. Cormen',
        'category': 'Computer Science',
        'pages': 1328,
        'rating': 4.9,
        'isbn': '978-0262033848',
        'description': 'A comprehensive guide to algorithms and data structures.',
        'chapters': {
            1: {
                'title': 'Foundations',
                'content': '''## Chapter 1: Foundations

### Introduction to Algorithms

An algorithm is a sequence of computational steps that transforms the input into the output. Here's a comparison of common sorting algorithms:

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|-----------------|------------------|----------|
| Bubble Sort | O(n²) | O(1) | Educational purposes |
| Merge Sort | O(n log n) | O(n) | Large datasets |
| Quick Sort | O(n log n) | O(log n) | General purpose |
| Heap Sort | O(n log n) | O(1) | Memory constrained |

### Key Concepts

**Time Complexity** measures how the runtime grows with input size.

**Space Complexity** measures memory usage.

**Asymptotic Analysis** helps us understand algorithm behavior for large inputs.

> **Note:** Good algorithm design is fundamental to writing efficient software!
'''
            },
            2: {
                'title': 'Sorting',
                'content': '''## Chapter 2: Sorting Algorithms

### Overview Table

| Sort Type | Description | Stability |
|-----------|-------------|-----------|
| Insertion | Builds sorted array one item at a time | Stable |
| Merge | Divide and conquer approach | Stable |
| Quick | Partitioning strategy | Unstable |
| Heap | Uses heap data structure | Unstable |

### Insertion Sort Example

```
procedure insertionSort(A : list of sortable items)
    for i from 1 to length(A) - 1 do
        j = i
        while j > 0 and A[j-1] > A[j] do
            swap(A[j], A[j-1])
            j = j - 1
```

This algorithm is simple and efficient for small lists.
'''
            },
            3: {
                'title': 'Data Structures',
                'content': '''## Chapter 3: Data Structures

### Common Data Structures

| Structure | Access | Search | Insertion | Deletion |
|-----------|--------|--------|-----------|----------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| Binary Tree | O(log n) | O(log n) | O(log n) | O(log n) |
| Hash Table | O(1) | O(1) | O(1) | O(1) |

### Choosing the Right Structure

- **Arrays**: Fixed size, fast random access
- **Linked Lists**: Dynamic size, efficient insertion/deletion
- **Trees**: Hierarchical data, searching
- **Graphs**: Complex relationships

> Selecting the right data structure is crucial for algorithm efficiency!
'''
            }
        }
    },
    'clean-code': {
        'title': 'Clean Code',
        'author': 'Robert Martin',
        'category': 'Software Development',
        'pages': 464,
        'rating': 4.8,
        'isbn': '978-0132350884',
        'description': 'Learn best practices for writing clean code.',
        'chapters': {
            1: {
                'title': 'Introduction',
                'content': '## Chapter 1: Introduction\n\nClean code is code that is easy to read and understand.'
            },
            2: {
                'title': 'Naming',
                'content': '## Chapter 2: Naming\n\nChoose clear, descriptive names for variables and functions.'
            },
            3: {
                'title': 'Functions',
                'content': '## Chapter 3: Functions\n\nFunctions should be small and focused on a single task.'
            }
        }
    }
}

# Add default chapters for books without explicit chapter content
for book_id, book in BOOKS.items():
    if 'chapters' not in book:
        book['chapters'] = {
            i: {
                'title': f'Chapter {i}',
                'content': f'# {book["title"]}\n\nChapter {i} content goes here.'
            }
            for i in range(1, 21)
        }

@elibrary.route('/')
def index():
    return render_template('elibrary.html')

@elibrary.route('/book/<book_id>')
@login_required
def book_detail(book_id):
    book = BOOKS.get(book_id)
    
    if not book:
        return render_template('book_detail.html', 
                             book_title='Book Not Found',
                             book_author='Unknown',
                             book_category='Unknown',
                             book_pages=0,
                             book_rating=0,
                             book_isbn='N/A',
                             book_description='This book could not be found.',
                             book_id=book_id), 404
    
    return render_template('book_detail.html',
                         book_title=book['title'],
                         book_author=book['author'],
                         book_category=book['category'],
                         book_pages=book['pages'],
                         book_rating=book['rating'],
                         book_isbn=book['isbn'],
                         book_description=book['description'],
                         book_id=book_id)

@elibrary.route('/book/<book_id>/read', methods=['GET', 'POST'])
@login_required
def book_reader(book_id):
    book = BOOKS.get(book_id)
    
    if not book:
        return render_template('book_reader.html', 
                             book_title='Book Not Found',
                             book_author='Unknown',
                             book_id=book_id,
                             current_page=1,
                             chapter_title='Not Found',
                             chapter_html=Markup('<p>Chapter not found</p>')), 404
    
    # Handle chapter navigation
    current_page = 1
    if request.method == 'POST':
        chapter = request.form.get('chapter')
        if chapter:
            current_page = int(chapter)
    else:
        current_page = request.args.get('page', 1, type=int)
    
    # Clamp page to valid range
    current_page = max(1, min(20, current_page))
    
    # Get chapter content
    chapter_data = book['chapters'].get(current_page, {})
    chapter_title = chapter_data.get('title', f'Chapter {current_page}')
    chapter_markdown = chapter_data.get('content', f'# {chapter_title}\n\nContent coming soon...')
    
    # Parse markdown to HTML
    html = markdown.markdown(chapter_markdown, extensions=['tables', 'fenced_code'])
    # Add inline styles to tables
    html = add_table_styles(html)
    chapter_html = Markup(html)
    
    return render_template('book_reader.html',
                         book_title=book['title'],
                         book_author=book['author'],
                         book_id=book_id,
                         current_page=current_page,
                         chapter_title=chapter_title,
                         chapter_html=chapter_html)
