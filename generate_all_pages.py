#!/usr/bin/env python3
"""
Generate a single MkDocs page with ALL pages in Finder order
"""

import shutil
from pathlib import Path

# Paths
markdown_dir = Path("../1989_FJ62_Owners_Manual_pages")
images_dir = Path("../1989_FJ62_Owners_Manual_images")
docs_dir = Path("docs")

# Create docs directory
docs_dir.mkdir(parents=True, exist_ok=True)

# Create images directory
docs_images_dir = docs_dir / "images"
docs_images_dir.mkdir(parents=True, exist_ok=True)

print("Generating complete manual in Finder order...")

content_parts = ["# 1989 FJ62 Owner's Manual\n\n"]

# Cover pages (page-0-01 through page-0-06)
for i in range(1, 7):
    page_name = f"page-0-{i:02d}"
    md_file = markdown_dir / f"{page_name}.md"
    image_file = images_dir / f"{page_name}.jpg"

    content_parts.append(f"## Cover Page {i}\n\n")

    if md_file.exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            page_content = f.read().strip()
            if page_content:
                content_parts.append(f"{page_content}\n\n")

    if image_file.exists():
        dest_image = docs_images_dir / f"{page_name}.jpg"
        if not dest_image.exists():
            shutil.copy2(image_file, dest_image)
        content_parts.append(f"![{page_name}](images/{page_name}.jpg)\n\n")

    content_parts.append("---\n\n")

# Main pages (page-001 through page-195)
for page_num in range(1, 196):
    page_name = f"page-{page_num:03d}"
    md_file = markdown_dir / f"{page_name}.md"
    image_file = images_dir / f"{page_name}.jpg"

    content_parts.append(f"## Page {page_num}\n\n")

    if md_file.exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            page_content = f.read().strip()
            if page_content:
                content_parts.append(f"{page_content}\n\n")
    else:
        content_parts.append("*Page content not yet processed*\n\n")

    if image_file.exists():
        dest_image = docs_images_dir / f"{page_name}.jpg"
        if not dest_image.exists():
            shutil.copy2(image_file, dest_image)
        content_parts.append(f"![Page {page_num}](images/{page_name}.jpg)\n\n")

    content_parts.append("---\n\n")

    # After page 92, insert unnumbered pages
    if page_num == 92:
        for i in range(1, 5):
            page_name = f"page-092-{i:02d}"
            md_file = markdown_dir / f"{page_name}.md"
            image_file = images_dir / f"{page_name}.jpg"

            content_parts.append(f"## Page 92.{i} (unnumbered)\n\n")

            if md_file.exists():
                with open(md_file, 'r', encoding='utf-8') as f:
                    page_content = f.read().strip()
                    if page_content:
                        content_parts.append(f"{page_content}\n\n")
            else:
                content_parts.append("*Page content not yet processed*\n\n")

            if image_file.exists():
                dest_image = docs_images_dir / f"{page_name}.jpg"
                if not dest_image.exists():
                    shutil.copy2(image_file, dest_image)
                content_parts.append(f"![Page 92.{i}](images/{page_name}.jpg)\n\n")

            content_parts.append("---\n\n")

# Write index file
index_path = docs_dir / "index.md"
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(''.join(content_parts))

print(f"\n✅ Generated complete manual with all {6 + 195 + 4} pages!")
print(f"📁 Output: {index_path}")
print(f"🖼️  Images copied to: {docs_images_dir}")
