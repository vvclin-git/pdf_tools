# pdf_tools

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
