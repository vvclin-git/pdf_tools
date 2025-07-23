# pdf_tools

# Presentation Tools

**A Python toolkit for:**
- Extracting slide titles and outlines from images (with OpenAI Vision)
- Converting image slides to PDF with (nested) bookmarks
- Merging PDFs with custom bookmarks

---

## Features

- 🖼️ **Extract Titles/ToC:** Use OpenAI GPT-4o Vision API to extract slide titles or outlines from image slides  
- 📄 **Image to PDF:** Combine images into a PDF (keeps original resolution, no compression)  
- 🔖 **PDF Bookmarks:** Add (multi-level) bookmarks/outlines to PDF for chapters/subsections  
- 🛠️ **Merge PDFs:** Merge multiple PDFs and add bookmarks  

---

## Installation

```bash
pip install pillow pypdf2 python-dotenv openai
```

---

## Usage

### 1. Extract Slide Titles

```python
from presentation_tools import extract_titles_from_images

# 提取所有圖片的標題並輸出成 slide_titles.txt
extract_titles_from_images("slides_folder")
```

### 2. Extract Outline / Agenda from One Slide

```python
from presentation_tools import extract_outline_from_image

outline = extract_outline_from_image("slides_folder/slide1.jpg")
print(outline)
```

### 3. Images to PDF with Nested Bookmarks

```python
from presentation_tools import images_to_pdf_with_nested_bookmarks

chapters = [
    {"title": "前言", "page": 1},
    {"title": "方法", "page": 4, "children": [
        {"title": "數據收集", "page": 5},
        {"title": "建模流程", "page": 7}
    ]},
    {"title": "結果", "page": 10}
]
images_to_pdf_with_nested_bookmarks("slides_folder", chapters)
```

### 4. Merge Multiple PDFs with Bookmarks

```python
from presentation_tools import merge_pdfs

chapter_list = [
    ("Intro", "intro.pdf"),
    ("Methods", "methods.pdf"),
    ("Results", "results.pdf"),
]
merge_pdfs(chapter_list, input_path="pdfs/", output_path="combined.pdf")
```

---

## Configuration

Make sure you have a `.env` file in your project root with your OpenAI API key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Input Format

For nested bookmarks, use the following structure:

```python
[
    {"title": "章節1", "page": 1},
    {"title": "章節2", "page": 5, "children": [
        {"title": "小節2.1", "page": 6},
        {"title": "小節2.2", "page": 8}
    ]}
]
```

- `page` is 1-based
- Any level of nesting is supported

---

## Notes

- **Image sorting**: Sorted by filename
- **PDF bookmarks**: Supported by all major PDF readers
- **Original image quality preserved**
- Supports English and Traditional Chinese
- Python 3.8+

---
## Quick Start

1. Place all your presentation images in a folder (e.g., 001.jpg, 002.jpg, …)
2. Create a `.env` file and add your OpenAI API key
3. Use `extract_titles_from_images()` to automatically extract titles
4. Use `images_to_pdf_with_nested_bookmarks()` to generate a bookmarked PDF

