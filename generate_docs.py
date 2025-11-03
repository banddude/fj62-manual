#!/usr/bin/env python3
"""
Generate MkDocs pages from OCR markdown and page images
"""

import shutil
from pathlib import Path

# Paths
markdown_dir = Path("../1989_FJ62_Owners_Manual_pages")
images_dir = Path("../1989_FJ62_Owners_Manual_images")
docs_dir = Path("docs")
docs_images_dir = docs_dir / "images"

# Create directories
docs_images_dir.mkdir(parents=True, exist_ok=True)

# Get all markdown files
md_files = sorted(markdown_dir.glob("page_*.md"), key=lambda x: int(x.stem.split('_')[1]))

print(f"Found {len(md_files)} markdown files")

# Generate combined pages
for md_file in md_files:
    page_num = int(md_file.stem.split('_')[1])
    image_file = images_dir / f"page_{page_num}.png"

    # Read markdown content
    if md_file.exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "*Page content not yet processed*"

    # Copy image if exists
    if image_file.exists():
        dest_image = docs_images_dir / f"page_{page_num}.png"
        shutil.copy2(image_file, dest_image)
        image_ref = f"![Page {page_num}](images/page_{page_num}.png)"
    else:
        image_ref = "*Image not yet available*"

    # Create combined markdown page
    combined_content = f"""# Page {page_num}

{content}

---

## Original Page Image

{image_ref}
"""

    # Write to docs
    output_file = docs_dir / f"page_{page_num}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_content)

    if page_num % 10 == 0:
        print(f"Generated page {page_num}...")

print(f"\nGenerated {len(md_files)} documentation pages!")
print(f"Images copied to: {docs_images_dir}")
