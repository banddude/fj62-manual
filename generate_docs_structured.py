#!/usr/bin/env python3
"""
Generate MkDocs pages from OCR markdown and images using TOC structure
"""

import shutil
from pathlib import Path

# Paths
markdown_dir = Path("../1989_FJ62_Owners_Manual_pages")
images_dir = Path("../1989_FJ62_Owners_Manual_images")
docs_dir = Path("docs")

# PDF page offsets
# Parts 1-2: manual page 1 = PDF page 7 (offset of 6)
# Part 3+: There are unnumbered pages between parts, need offset of 10
OFFSET_PART1_2 = 6
OFFSET_PART3_PLUS = 10

# Table of Contents mapping (section name, manual start page, manual end page, offset)
toc = [
    # Part 1
    ("part1/1-1_overview.md", "1-1. Overview of Instruments and Controls", 1, 4, OFFSET_PART1_2),
    ("part1/1-2_key_and_doors.md", "1-2. Key and Doors", 5, 12, OFFSET_PART1_2),
    ("part1/1-3_seats_belts.md", "1-3. Seats, Seat Belts, Steering Wheel and Mirrors", 13, 24, OFFSET_PART1_2),
    ("part1/1-4_lights_wipers.md", "1-4. Lights, Wipers and Defogger", 25, 30, OFFSET_PART1_2),
    ("part1/1-5_gauges_meters.md", "1-5. Gauges, Meters and Warning Lights", 31, 36, OFFSET_PART1_2),
    ("part1/1-6_ignition_transmission.md", "1-6. Ignition Switch, Transmission and Parking Brake", 37, 48, OFFSET_PART1_2),
    ("part1/1-7_audio_climate.md", "1-7. Car Audio and Environmental Control System", 49, 86, OFFSET_PART1_2),
    ("part1/1-8_other_equipment.md", "1-8. Other Equipment", 87, 90, OFFSET_PART1_2),

    # Part 2 (pages 91-92, then 4 unnumbered pages, then 93-100)
    ("part2/index.md", "Part 2: Information Before Driving Your Toyota", 91, 100, OFFSET_PART1_2),

    # Part 3+ (starts at printed page 101)
    ("part3/index.md", "Part 3: Starting and Driving", 101, 112, OFFSET_PART3_PLUS),

    # Part 4
    ("part4/index.md", "Part 4: In Case of an Emergency", 113, 124, OFFSET_PART3_PLUS),

    # Part 5
    ("part5/index.md", "Part 5: Corrosion Prevention and Appearance Care", 125, 128, OFFSET_PART3_PLUS),

    # Part 6
    ("part6/index.md", "Part 6: Vehicle Maintenance and Care", 129, 142, OFFSET_PART3_PLUS),

    # Part 7
    ("part7/7-1_introduction.md", "7-1. Introduction", 143, 148, OFFSET_PART3_PLUS),
    ("part7/7-2_engine_chassis.md", "7-2. Engine and Chassis", 149, 170, OFFSET_PART3_PLUS),
    ("part7/7-3_electrical.md", "7-3. Electrical Components", 171, 182, OFFSET_PART3_PLUS),

    # Part 8
    ("part8/index.md", "Part 8: Specifications", 183, 188, OFFSET_PART3_PLUS),

    # Part 9
    ("part9/index.md", "Part 9: Index", 189, 205, OFFSET_PART3_PLUS),
]

# Create directory structure
for section_file, _, _, _, _ in toc:
    section_path = docs_dir / section_file
    section_path.parent.mkdir(parents=True, exist_ok=True)

# Create images directory
docs_images_dir = docs_dir / "images"
docs_images_dir.mkdir(parents=True, exist_ok=True)

print(f"Generating structured documentation...")

# Generate sections
for section_file, section_title, manual_start, manual_end, offset in toc:
    # Convert manual pages to PDF pages using section-specific offset
    pdf_start = manual_start + offset
    pdf_end = manual_end + offset

    print(f"Processing: {section_title}")
    print(f"  Manual pages {manual_start}-{manual_end} (PDF pages {pdf_start}-{pdf_end})")

    # Build combined content
    content_parts = [f"# {section_title}\n\n"]

    for manual_page in range(manual_start, manual_end + 1):
        # Special handling for Part 2: after page 92, insert 4 unnumbered pages
        if section_file == "part2/index.md" and manual_page == 92:
            # First show page 92
            pdf_page = manual_page + offset
            md_file = markdown_dir / f"page_{pdf_page}.md"
            image_file = images_dir / f"page_{pdf_page}.png"

            content_parts.append(f"## Page {manual_page}\n\n")

            if md_file.exists():
                with open(md_file, 'r', encoding='utf-8') as f:
                    page_content = f.read().strip()
                    if page_content:
                        content_parts.append(f"{page_content}\n\n")
            else:
                content_parts.append("*Page content not yet processed*\n\n")

            if image_file.exists():
                dest_image = docs_images_dir / f"page_{pdf_page}.png"
                if not dest_image.exists():
                    shutil.copy2(image_file, dest_image)
                content_parts.append(f"![Manual Page {manual_page}](../images/page_{pdf_page}.png)\n\n")
            else:
                content_parts.append("*Image not yet available*\n\n")

            content_parts.append("---\n\n")

            # Now add the 4 unnumbered pages (PDF 99-102)
            for i in range(1, 5):
                pdf_page = 98 + i  # PDF pages 99, 100, 101, 102
                page_label = f"92.{i}"
                md_file = markdown_dir / f"page_{pdf_page}.md"
                image_file = images_dir / f"page_{pdf_page}.png"

                content_parts.append(f"## Page {page_label} (unnumbered)\n\n")

                if md_file.exists():
                    with open(md_file, 'r', encoding='utf-8') as f:
                        page_content = f.read().strip()
                        if page_content:
                            content_parts.append(f"{page_content}\n\n")
                else:
                    content_parts.append("*Page content not yet processed*\n\n")

                if image_file.exists():
                    dest_image = docs_images_dir / f"page_{pdf_page}.png"
                    if not dest_image.exists():
                        shutil.copy2(image_file, dest_image)
                    content_parts.append(f"![Manual Page {page_label}](../images/page_{pdf_page}.png)\n\n")
                else:
                    content_parts.append("*Image not yet available*\n\n")

                content_parts.append("---\n\n")

            continue  # Skip the normal processing for page 92

        # For page 93 onwards in Part 2, use the new offset
        if section_file == "part2/index.md" and manual_page >= 93:
            pdf_page = manual_page + OFFSET_PART3_PLUS
        else:
            pdf_page = manual_page + offset

        md_file = markdown_dir / f"page_{pdf_page}.md"
        image_file = images_dir / f"page_{pdf_page}.png"

        # Add page header with manual page number
        content_parts.append(f"## Page {manual_page}\n\n")

        # Read markdown content
        if md_file.exists():
            with open(md_file, 'r', encoding='utf-8') as f:
                page_content = f.read().strip()
                if page_content:
                    content_parts.append(f"{page_content}\n\n")
        else:
            content_parts.append("*Page content not yet processed*\n\n")

        # Copy and reference image (using PDF page number for file names)
        if image_file.exists():
            dest_image = docs_images_dir / f"page_{pdf_page}.png"
            if not dest_image.exists():
                shutil.copy2(image_file, dest_image)
            # Show manual page number but reference PDF page file
            content_parts.append(f"![Manual Page {manual_page}](../images/page_{pdf_page}.png)\n\n")
        else:
            content_parts.append("*Image not yet available*\n\n")

        content_parts.append("---\n\n")

    # Write combined section file
    section_path = docs_dir / section_file
    with open(section_path, 'w', encoding='utf-8') as f:
        f.write(''.join(content_parts))

print(f"\n✅ Generated {len(toc)} sections!")
print(f"📁 Structure matches manual's table of contents")
print(f"🖼️  Images copied to: {docs_images_dir}")
