import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import time
import openai
import base64
import re
from dotenv import load_dotenv

def clean_title(title):
    cleaned = re.sub(r'[^\w\u4e00-\u9fff\- ]+', '', title)
    cleaned = cleaned.strip().replace(' ', '_')
    return cleaned[:40] if cleaned else 'Untitled'

def encode_image_to_data_url(image_path):
    with open(image_path, "rb") as img_file:
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/{ext};base64,{base64_img}"

def extract_titles_from_images(img_dir, api_key_var="OPENAI_API_KEY", sleep_sec=1.2, output_file='slide_titles.txt'):
    """
    Extracts slide titles from images in the given directory using GPT-4o Vision API.
    Reads API key from .env or environment.
    """
    load_dotenv()
    api_key = os.getenv(api_key_var)
    openai.api_key = api_key
    IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    image_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(IMG_EXTENSIONS)])
    titles = []

    for idx, filename in enumerate(image_files, 1):
        img_path = os.path.join(img_dir, filename)
        data_url = encode_image_to_data_url(img_path)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract ONLY the slide title from this presentation image. Respond with the title only, no extra words."},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ]
        )
        title = response.choices[0].message.content.strip()
        print(title)
        title = clean_title(title)
        titles.append(title)
        time.sleep(sleep_sec)

    with open(os.path.join(img_dir, output_file), 'w', encoding='utf-8') as f:
        for i, t in enumerate(titles, 1):
            f.write(f"{i}. {t}\n")

    print(f"All titles extracted and saved to {output_file}.")
    return titles

def extract_outline_from_image(image_path, api_key_var="OPENAI_API_KEY"):
    """
    Given an image file path, returns a structured outline/agenda/ToC text extracted by GPT-4o Vision.
    Returns None if failed.
    """
    # Load env if not loaded
    load_dotenv()
    api_key = os.getenv(api_key_var)
    openai.api_key = api_key
    # Prepare base64 image
    ext = os.path.splitext(image_path)[1].lower().replace('.', '')
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode('utf-8')
        data_url = f"data:image/{ext};base64,{b64}"
    # LLM prompt for outline/agenda extraction
    prompt = (
        "Please extract the full agenda or table of contents or outline from this slide as a bulleted list in English. "
        "If there is no clear outline, return the main text as a list. Do NOT include page number or extra comments. "
        "Respond ONLY with the bullet list."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ]
        )
        text = response.choices[0].message.content.strip()
        # Optionally postprocess bullets (convert to Python list)
        bullets = re.findall(r"[-*•]\s+(.+)", text)
        return bullets if bullets else text.splitlines()
    except Exception as e:
        print(f"[Error] {e}")
        return None

def add_outline_items(writer, chapters, parent=None):
    for ch in chapters:
        node = writer.add_outline_item(ch["title"], ch["page"] - 1, parent=parent)
        if "children" in ch:
            add_outline_items(writer, ch["children"], parent=node)

def images_to_pdf_with_nested_bookmarks(img_dir, chapters, output_pdf="output.pdf"):
    """
    Combines all images into a PDF (原解析度), chapters為巢狀list，支援多層outline。
    """
    IMG_EXT = ('.jpg', '.jpeg', '.png')
    files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(IMG_EXT)])
    imgs = [Image.open(os.path.join(img_dir, f)).convert("RGB") for f in files]
    if not imgs:
        raise ValueError("No images found in folder!")
    temp_pdf = os.path.join(img_dir, "__tmp_no_bookmark.pdf")
    imgs[0].save(temp_pdf, save_all=True, append_images=imgs[1:])

    reader = PdfReader(temp_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    # Add nested bookmarks
    add_outline_items(writer, chapters)
    with open(os.path.join(img_dir, output_pdf), "wb") as f:
        writer.write(f)
    os.remove(temp_pdf)
    print(f"PDF with nested bookmarks saved as {output_pdf}")

# Example usage:
# chapters = [
#     {"title": "前言", "page": 1},
#     {"title": "方法", "page": 4, "children": [
#         {"title": "數據收集", "page": 5},
#         {"title": "建模流程", "page": 7}
#     ]},
#     {"title": "結果", "page": 10}
# ]
# images_to_pdf_with_nested_bookmarks("your_image_folder", chapters)

def merge_pdfs(chapter_list, input_path='', output_path="combined.pdf"):
    """
    Merge PDFs in the order given by chapter_list,
    adding a bookmark for each chapter.
    """
    merger = PdfMerger()
    for title, filename in chapter_list:
        filepath = os.path.abspath(f'{input_path}\\{filename}')
        # Append the PDF and add a bookmark at the start of this file
        merger.append(filepath, outline_item=title)
    # Write out the merged PDF
    with open(output_path, "wb") as fout:
        merger.write(fout)
    merger.close()
    print(f"Merged PDF saved as: {output_path}")
