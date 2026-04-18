#!/usr/bin/env python3
"""
Generate Major Project Report for Social Media Forensics: Cyberbullying & Hate Speech Analysis Using ML
Based on C11/A9 report format (matching exactly).
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# ============================================================
# CONFIGURATION
# ============================================================
PROJECT_TITLE = "Social Media Forensics: Cyberbullying & Hate Speech Analysis Using Machine Learning"
STUDENTS = [
    ("160922733XXX", "Student Name 1"),
    ("160922733XXX", "Student Name 2"),
    ("160922733XXX", "Student Name 3"),
    ("160922733XXX", "Student Name 4"),
]
GUIDE_NAME = "Name of the Guide"
GUIDE_DESIGNATION = "Designation"
GUIDE_DEPT = "Dept. of CSE"
HOD_NAME = "Dr. TK Shaik Shavali"
PRINCIPAL_NAME = "Dr. Ravi Kishore Singh"
ACADEMIC_YEAR = "2024-2025"
YEAR = "2026"
COLLEGE = "LORDS INSTITUTE OF ENGINEERING AND TECHNOLOGY"
COLLEGE_SHORT = "LORDS INSTITUTE OF ENGINEERING & TECHNOLOGY"
DEPT = "Department of Computer Science & Engineering"
DEPT_FULL = "Department of Computer Science and Engineering"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "lords_logo.png")
FIGURES_DIR = os.path.join(SCRIPT_DIR, "figures")
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "Social_Media_Forensics_Hate_Speech_Major_Project_Report.docx")

# ============================================================
# DOCUMENT SETUP
# ============================================================
doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_centered_text(text, font_size=12, bold=False, color=None, space_after=6, space_before=0, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p


def add_justified_text(text, font_size=12, bold=False, space_after=6, space_before=0, first_line_indent=None, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.5
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    if first_line_indent:
        p.paragraph_format.first_line_indent = Cm(first_line_indent)
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = bold
    return p


def add_left_text(text, font_size=12, bold=False, space_after=6, space_before=0, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.5
    if keep_with_next:
        p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = bold
    return p


def add_chapter_heading(chapter_num, title):
    p1 = add_centered_text(f"CHAPTER {chapter_num}", font_size=18, bold=True, space_before=24, space_after=3)
    p1.paragraph_format.keep_with_next = True
    p2 = add_centered_text(title.upper(), font_size=16, bold=True, space_after=10)
    p2.paragraph_format.keep_with_next = True


def add_section_heading(number, title, font_size=16):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(f"{number}  {title}")
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = True
    return p


def add_subsection_heading(number, title, font_size=14):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(f"{number}  {title}")
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = True
    return p


def add_bullet(text, font_size=12):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.5
    p.clear()
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    return p


def set_cell_text(cell, text, bold=False, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT, color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.name = 'Times New Roman'
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def shade_cell(cell, color="D9E2F3"):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def keep_table_on_one_page(table):
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        cantSplit = parse_xml(f'<w:cantSplit {nsdecls("w")} w:val="true"/>')
        trPr.append(cantSplit)
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.keep_with_next = True
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                tcMar = parse_xml(
                    f'<w:tcMar {nsdecls("w")}>'
                    '<w:top w:w="30" w:type="dxa"/>'
                    '<w:bottom w:w="30" w:type="dxa"/>'
                    '</w:tcMar>'
                )
                existing = tcPr.findall(qn('w:tcMar'))
                for e in existing:
                    tcPr.remove(e)
                tcPr.append(tcMar)


def add_page_break():
    doc.add_page_break()


def add_figure(image_path, caption=None, width=Inches(5.0)):
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(image_path, width=width)
        p_img.paragraph_format.space_after = Pt(3)
    if caption:
        add_centered_text(caption, font_size=10, bold=True, space_after=8)


def add_letterhead_header(colored=False):
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    logo_cell = t.cell(0, 0)
    logo_cell.width = Inches(1.2)
    logo_para = logo_cell.paragraphs[0]
    logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(LOGO_PATH):
        logo_para.add_run().add_picture(LOGO_PATH, width=Inches(1.0))
    text_cell = t.cell(0, 1)
    text_cell.width = Inches(5.0)
    p = text_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(COLLEGE_SHORT)
    run.font.size = Pt(13)
    run.font.name = 'Times New Roman'
    run.bold = True
    if colored:
        run.font.color.rgb = RGBColor(255, 0, 0)
    p2 = text_cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("(UGC Autonomous)")
    r2.font.size = Pt(10)
    r2.font.name = 'Times New Roman'
    p3 = text_cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run("Approved by AICTE | Affiliated to Osmania University | Estd.2003.")
    r3.font.size = Pt(9)
    r3.font.name = 'Times New Roman'
    p4 = text_cell.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p4.add_run("Accredited with \u2018A\u2019 grade by NAAC | Accredited by NBA")
    r4.font.size = Pt(9)
    r4.font.name = 'Times New Roman'
    p5 = text_cell.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r5 = p5.add_run(DEPT)
    r5.font.size = Pt(12)
    r5.font.name = 'Times New Roman'
    r5.bold = True
    if colored:
        r5.font.color.rgb = RGBColor(0, 128, 0)
    for cell in [logo_cell, text_cell]:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '</w:tcBorders>')
        tcPr.append(tcBorders)
    return t


def add_page_number(section_obj, start=1, fmt='decimal'):
    sectPr = section_obj._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="{start}" w:fmt="{fmt}"/>')
    existing = sectPr.findall(qn('w:pgNumType'))
    for e in existing:
        sectPr.remove(e)
    sectPr.append(pgNumType)


# ============================================================
# PAGE i - TITLE PAGE
# ============================================================
add_centered_text("A", font_size=14, space_before=12, space_after=0)
add_centered_text("Major Project Report", font_size=16, bold=True, space_after=4)
add_centered_text("on", font_size=12, space_after=4)
add_centered_text(PROJECT_TITLE, font_size=18, bold=True, color=(255, 0, 0), space_after=6)
add_centered_text("submitted in partial fulfillment of the requirement for the award of the degree of",
                   font_size=11, space_after=4)
add_centered_text("BACHELOR OF ENGINEERING", font_size=13, bold=True, space_after=2)
add_centered_text("In", font_size=12, space_after=2)
add_centered_text("COMPUTER SCIENCE & ENGINEERING", font_size=13, bold=True, space_after=6)
add_centered_text("By", font_size=12, space_after=4)

t = doc.add_table(rows=len(STUDENTS), cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (roll, name) in enumerate(STUDENTS):
    set_cell_text(t.cell(i, 0), name, font_size=12, bold=True)
    set_cell_text(t.cell(i, 1), roll, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    t.cell(i, 0).width = Inches(3)
    t.cell(i, 1).width = Inches(2.5)

add_centered_text("", space_after=1)
add_centered_text("Under the esteemed guidance of", font_size=12, space_after=2)
add_centered_text(GUIDE_NAME, font_size=12, bold=True, space_after=2)
add_centered_text(f"{GUIDE_DESIGNATION} & {GUIDE_DEPT}", font_size=12, space_after=6)

p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(LOGO_PATH):
    p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.3))

add_centered_text(DEPT, font_size=14, bold=True, space_before=4, space_after=3)
add_centered_text(COLLEGE, font_size=13, bold=True, color=(255, 0, 0), space_after=2)
add_centered_text("(UGC Autonomous)", font_size=11, space_after=1)
add_centered_text("Approved by AICTE | Affiliated to Osmania University | Estd.2003", font_size=10, space_after=1)
add_centered_text("Sy.No.32, Himayat Sagar, Near TGPA Junction, Hyderabad-500091, India.", font_size=10, space_after=3)
add_centered_text(f"({YEAR})", font_size=14, bold=True, space_after=3)

add_page_number(doc.sections[0], start=1, fmt='lowerRoman')

# ============================================================
# PAGE ii - CERTIFICATE
# ============================================================
add_letterhead_header()
add_centered_text("", space_after=2)
add_centered_text("CERTIFICATE", font_size=16, bold=True, space_after=8)

cert_p = doc.add_paragraph()
cert_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
cert_p.paragraph_format.space_after = Pt(6)
cert_p.paragraph_format.line_spacing = 1.5
cert_p.paragraph_format.first_line_indent = Cm(1.27)
r = cert_p.add_run(f'This is to certify that the project report entitled \u201c{PROJECT_TITLE}\u201d being Submitted by ')
r.font.size = Pt(12)
r.font.name = 'Times New Roman'
student_str = ", ".join(f"{name} ({roll})" for roll, name in STUDENTS[:-1]) + f", and {STUDENTS[-1][1]} ({STUDENTS[-1][0]})" if len(STUDENTS) > 1 else f"{STUDENTS[0][1]} ({STUDENTS[0][0]})"
r3 = cert_p.add_run(student_str)
r3.font.size = Pt(12)
r3.font.name = 'Times New Roman'
r3.bold = True
r5 = cert_p.add_run(
    f' in partial fulfillment of the requirements for the award of '
    f'the degree of Bachelor of Engineering in Computer Science and Engineering during the '
    f'academic year {ACADEMIC_YEAR}.'
)
r5.font.size = Pt(12)
r5.font.name = 'Times New Roman'
add_justified_text(
    "This is further certified that the work done under my guidance, and the results of this work "
    "have not been submitted elsewhere for the award of any of the degree",
    first_line_indent=1.27, space_after=18
)

sig = doc.add_table(rows=2, cols=2)
sig.alignment = WD_TABLE_ALIGNMENT.CENTER
set_cell_text(sig.cell(0, 0), "Internal Guide", bold=True, font_size=11)
set_cell_text(sig.cell(0, 1), "Head of the Department", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)
set_cell_text(sig.cell(1, 0), f"{GUIDE_NAME}\n{GUIDE_DESIGNATION}", font_size=11)
set_cell_text(sig.cell(1, 1), f"{HOD_NAME}\nHOD - CSE", font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)

add_centered_text("", space_after=12)

sig2 = doc.add_table(rows=2, cols=2)
sig2.alignment = WD_TABLE_ALIGNMENT.CENTER
set_cell_text(sig2.cell(0, 0), "Principal", bold=True, font_size=11)
set_cell_text(sig2.cell(0, 1), "External Examiner", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)
set_cell_text(sig2.cell(1, 0), PRINCIPAL_NAME, font_size=11)
set_cell_text(sig2.cell(1, 1), "Date:", font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)

# ============================================================
# PAGE iii - DECLARATION
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=6)
add_centered_text("DECLARATION BY THE CANDIDATE", font_size=16, bold=True, space_after=12,
                   color=(0x1F, 0x4E, 0x79))

decl_text = (
    f'We, hereby declare that the project report entitled \u201c{PROJECT_TITLE}\u201d, under '
    f'the guidance of {GUIDE_NAME}, {GUIDE_DESIGNATION}, {DEPT_FULL}, '
    f'Lords Institute of Engineering & Technology, affiliated to Osmania University, Hyderabad '
    f'is submitted in partial fulfillment of the requirements for the award of the degree of '
    f'Bachelor of Engineering in Computer Science and Engineering.'
)
add_justified_text(decl_text, first_line_indent=1.27)
add_justified_text(
    "This is a record of bonafide work carried out by us and the results of this work "
    "have not been reproduced or copied from any source. The results embodied in this project report "
    "have not been submitted to any other university or institute for the award of any other degree.",
    first_line_indent=1.27, space_after=24
)

t3 = doc.add_table(rows=len(STUDENTS), cols=2)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (roll, name) in enumerate(STUDENTS):
    set_cell_text(t3.cell(i, 0), name, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t3.cell(i, 1), roll, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# ============================================================
# PAGE iv - ACKNOWLEDGMENT
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=6)
add_centered_text("ACKNOWLEDGMENT", font_size=16, bold=True, space_after=12,
                   color=(0x1F, 0x4E, 0x79))

add_justified_text(
    "First, we wish to thank GOD Almighty who created heavens and earth, who helped us in "
    "completing this project and we also thank our Parents who encouraged us in this period.",
    space_after=6
)
add_justified_text(
    f"We would like to thank {GUIDE_NAME}, {GUIDE_DESIGNATION}, {GUIDE_DEPT}, "
    f"Lords Institute of Engineering & Technology, affiliated to Osmania University, Hyderabad, "
    f"our project internal guide, for her guidance and help. Her insight during the course of our "
    f"major project and regular guidance were invaluable to us.",
    space_after=6
)
add_justified_text(
    f"We would like to express our deep sense of gratitude to {HOD_NAME}, Professor & "
    f"Head of the Department, Computer Science & Engineering, Lords Institute of Engineering "
    f"& Technology, affiliated to Osmania University, Hyderabad, for his encouragement and "
    f"cooperation throughout the project.",
    space_after=6
)
add_justified_text(
    f"We would also like to thank {PRINCIPAL_NAME}, Principal of our college, for extending his help.",
    space_after=18
)

t4 = doc.add_table(rows=len(STUDENTS)+1, cols=2)
t4.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (roll, name) in enumerate(STUDENTS):
    set_cell_text(t4.cell(i, 0), name, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t4.cell(i, 1), roll, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(t4.cell(len(STUDENTS), 0), "(Lords Institute of Engineering and Technology)",
              font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)

# ============================================================
# PAGE v - VISION & MISSION OF THE INSTITUTE
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=4)

add_left_text("Vision of the Institute:", bold=True, space_after=4)
add_justified_text(
    "Lords Institute of Engineering and Technology strives for excellence in professional education through "
    "quality, innovation and teamwork and aims to emerge as a premier institute in the state and across the nation.",
    first_line_indent=1.27, space_after=6
)

add_left_text("Mission of the Institute:", bold=True, space_after=4)
for m in [
    "To impart quality professional education that meets the needs of present and emerging technological world.",
    "To strive for student achievement and success, preparing them for life, career and leadership.",
    "To provide a scholarly and vibrant learning environment that enables faculty, staff and students to achieve personal and professional growth.",
    "To contribute to advancement of knowledge, in both fundamental and applied areas of engineering and technology.",
    "To forge mutually beneficial relationships with government organizations, industries, society and the alumni.",
]:
    add_bullet(m)

# ============================================================
# PAGE vi - VISION & MISSION OF THE DEPARTMENT
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=4)

add_left_text("Vision of the Department:", bold=True, space_after=4)
add_justified_text(
    "To emerge as a center of excellence for quality Computer Science and Engineering education "
    "with innovation, leadership and values.",
    first_line_indent=1.27, space_after=6
)

add_left_text("Mission of the Department:", bold=True, space_after=4)
for dm in [
    "DM1: Provide fundamental and practical training through learner \u2013 centric Teaching-Learning Process and state-of-the-art infrastructure.",
    "DM2: Develop design, research, and entrepreneurial skills for successful career.",
    "DM3: Promote training and activities through Industry-Academia interactions.",
]:
    add_bullet(dm)
add_left_text("Note: DM: Department Mission", font_size=11, space_before=6, space_after=6)

# ============================================================
# PAGE vii - PEOs
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=2)
add_centered_text("B.E. Computer Science and Engineering Program Educational Objectives (PEOs):",
                   font_size=12, bold=True, space_after=6, keep_with_next=True)

peos = [
    ("PEO1", "Exhibit strong foundations in Basic Sciences, Computer Science and allied engineering"),
    ("PEO2", "Identify, formulate, analyze and create professional solutions, novel products using appropriate tools and techniques, design skills."),
    ("PEO3", "Pursue successful career with continuous learning, with emphasis on competency oriented towards industry"),
    ("PEO4", "Practice ethics, managerial and leadership skills to work cohesively within a group"),
]
peo_table = doc.add_table(rows=4, cols=2)
peo_table.style = 'Table Grid'
peo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (code, desc) in enumerate(peos):
    set_cell_text(peo_table.cell(i, 0), code, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(peo_table.cell(i, 1), desc, font_size=11)
    shade_cell(peo_table.cell(i, 0), "D9E2F3")
for row in peo_table.rows:
    row.cells[0].width = Inches(0.8)
    row.cells[1].width = Inches(5.4)
keep_table_on_one_page(peo_table)

# ============================================================
# PAGE viii - POs
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=4)
add_centered_text("B.E. Computer Science and Engineering Program Outcomes (POs):", font_size=12, bold=True, space_after=3, keep_with_next=True)
add_left_text("Engineering Graduates will be able to:", font_size=12, space_after=4, keep_with_next=True)

po_table = doc.add_table(rows=12, cols=2)
po_table.style = 'Table Grid'
po_table.alignment = WD_TABLE_ALIGNMENT.CENTER
pos_data = [
    ("S. No.", "Program Outcomes (POs)"),
    ("1.", "PO1: Engineering Knowledge: Apply knowledge of mathematics, natural science, computing, engineering fundamentals and an engineering specialization as specified in WK1 to WK4 respectively to develop to the solution of complex engineering problems."),
    ("2.", "PO2: Problem Analysis: Identify, formulate, review research literature and analyze complex engineering problems reaching substantiated conclusions with consideration for sustainable development. (WK1 to WK4)"),
    ("3.", "PO3: Design/Development of Solutions: Design creative solutions for complex engineering problems and design/develop systems/components/processes to meet identified needs with consideration for the public health and safety, whole-life cost, net zero carbon, culture, society and environment as required. (WK5)"),
    ("4.", "PO4: Conduct Investigations of Complex Problems: Conduct investigations of complex engineering problems using research-based knowledge including design of experiments, modelling, analysis & interpretation of data to provide valid conclusions. (WK8)."),
    ("5.", "PO5: Engineering Tool Usage: Create, select and apply appropriate techniques, resources and modern engineering & IT tools, including prediction and modelling recognizing their limitations to solve complex engineering problems. (WK2 and WK6)"),
    ("6.", "PO6: The Engineer and The World: Analyze and evaluate societal and environmental aspects while solving complex engineering problems for its impact on sustainability with reference to economy, health, safety, legal framework, culture and environment. (WK1, WK5, and WK7)."),
    ("7.", "PO7: Ethics: Apply ethical principles and commit to professional ethics, human values, diversity and inclusion; adhere to national & international laws. (WK9)"),
    ("8.", "PO8: Individual and Collaborative Team work: Function effectively as an individual, and as a member or leader in diverse/multi-disciplinary teams."),
    ("9.", "PO9: Communication: Communicate effectively and inclusively within the engineering community and society at large, such as being able to comprehend and write effective reports and design documentation, make effective presentations considering cultural, language, and learning differences"),
    ("10.", "PO10: Project Management and Finance: Apply knowledge and understanding of engineering management principles and economic decision-making and apply these to one\u2019s own work, as a member and leader in a team, and to manage projects and in multidisciplinary environments."),
    ("11.", "PO11: Life-Long Learning: Recognize the need for, and have the preparation and ability for i) independent and life-long learning ii) adaptability to new and emerging technologies and iii) critical thinking in the broadest context of technological change. (WK8)"),
]
for i, (num, text) in enumerate(pos_data):
    set_cell_text(po_table.cell(i, 0), num, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(po_table.cell(i, 1), text, bold=(i == 0), font_size=10)
    if i == 0:
        shade_cell(po_table.cell(i, 0), "D9E2F3")
        shade_cell(po_table.cell(i, 1), "D9E2F3")
for row in po_table.rows:
    row.cells[0].width = Inches(0.6)
    row.cells[1].width = Inches(5.6)
keep_table_on_one_page(po_table)

# ============================================================
# PAGE ix - PSOs
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=4)
add_centered_text("B.E. Computer Science and Engineering Program Specific Outcomes (PSO\u2019s):",
                   font_size=12, bold=True, space_after=6, keep_with_next=True)

pso_table = doc.add_table(rows=2, cols=2)
pso_table.style = 'Table Grid'
pso_table.alignment = WD_TABLE_ALIGNMENT.CENTER
psos = [
    ("PSO1", "Professional Skills:\u00a0Implement computer programs in the areas related to algorithms, system software, multimedia, web design, big data analytics and networking for efficient analysis and design of computer-based systems of varying complexity"),
    ("PSO2", "Problem-Solving Skills:\u00a0Apply standard practices and strategies in software service management using open-ended programming environment with agility to deliver a quality service for business success"),
]
for i, (code, desc) in enumerate(psos):
    set_cell_text(pso_table.cell(i, 0), code, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(pso_table.cell(i, 1), desc, font_size=11)
    shade_cell(pso_table.cell(i, 0), "D9E2F3")
for row in pso_table.rows:
    row.cells[0].width = Inches(0.8)
    row.cells[1].width = Inches(5.4)
keep_table_on_one_page(pso_table)

# ============================================================
# PAGE x - COURSE OUTCOMES
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=4)
add_centered_text("Course Outcomes: C424 - Major Project", font_size=12, bold=True, space_after=2, keep_with_next=True)
add_left_text("Student will be able to", font_size=12, space_after=4, keep_with_next=True)

co_table = doc.add_table(rows=6, cols=3)
co_table.style = 'Table Grid'
co_table.alignment = WD_TABLE_ALIGNMENT.CENTER
cos = [
    ("CO. No", "Description", "Blooms\nTaxonomy\nLevel"),
    ("C424.1", "Demonstrate the ability to synthesize and apply the knowledge and skills acquired in the academic program to real-world problems.", "BTL3"),
    ("C424.2", "Evaluate different solutions based on economic and technical feasibility.", "BTL5"),
    ("C424.3", "Effectively plan a a project and confidently perform all aspects of project management", "BTL4"),
    ("C424.4", "Demonstrate effective oral communication skills", "BTL2"),
    ("C424.5", "Demonstrate effective team work and written skills", "BTL1"),
]
for i, (co, desc, bloom) in enumerate(cos):
    set_cell_text(co_table.cell(i, 0), co, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(co_table.cell(i, 1), desc, bold=(i == 0), font_size=10)
    set_cell_text(co_table.cell(i, 2), bloom, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    if i == 0:
        shade_cell(co_table.cell(i, 0), "D9E2F3")
        shade_cell(co_table.cell(i, 1), "D9E2F3")
        shade_cell(co_table.cell(i, 2), "D9E2F3")
for row in co_table.rows:
    row.cells[0].width = Inches(0.8)
    row.cells[1].width = Inches(4.2)
    row.cells[2].width = Inches(1.2)
keep_table_on_one_page(co_table)

# ============================================================
# PAGE xi - COURSE ARTICULATION MATRIX
# ============================================================
add_page_break()
add_letterhead_header(colored=True)
add_centered_text("", space_after=2)
add_centered_text("Course Articulation Matrix:", font_size=12, bold=True, space_after=1, keep_with_next=True)
add_centered_text("Mapping of Course Outcomes (CO) with Program Outcomes (PO) and Program Specific Outcomes (PSO\u2019s):",
                   font_size=11, space_after=2, keep_with_next=True)

cols = ["Course\nOutcome s\n(CO)", "PO1", "PO2", "PO3", "PO4", "PO5", "PO6", "PO7", "PO 8", "PO9", "PO10", "PO11", "PSO1", "PSO2"]
cam_table = doc.add_table(rows=8, cols=14)
cam_table.style = 'Table Grid'
cam_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, col_name in enumerate(cols):
    set_cell_text(cam_table.cell(0, j), col_name, bold=True, font_size=7, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade_cell(cam_table.cell(0, j), "D9E2F3")
co_matrix = [
    ("C424.1.", [3, 3, 3, 1, 3, 2, 1, 1, 2, 2, 3, 3, 3]),
    ("C424.2.", [3, 3, 3, 2, 2, 3, 1, 1, 2, 3, 3, 3, 3]),
    ("C424.3.", [3, 3, 3, 3, 3, 2, 1, 1, 3, 2, 3, 3, 3]),
    ("C424.4.", [3, 2, 1, 1, 2, 2, 1, 2, 3, 2, 3, 3, 3]),
    ("C424.5.", [3, 1, 2, 1, 2, 2, 1, 2, 3, 2, 3, 3, 3]),
    ("Average", [3.0, 2.4, 2.4, 1.6, 2.4, 2.2, 1.0, 1.4, 2.6, 2.2, 3.0, 3.0, 3.0]),
]
for i, (label, vals) in enumerate(co_matrix):
    set_cell_text(cam_table.cell(i + 1, 0), label, font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    for j, v in enumerate(vals):
        text = str(v) if isinstance(v, int) else f"{v:.1f}"
        set_cell_text(cam_table.cell(i + 1, j + 1), text, font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
keep_table_on_one_page(cam_table)

add_left_text("Level:", font_size=10, bold=True, space_after=0, space_before=2)
add_left_text("1- Low correlation (Low), 2- Medium correlation (Medium), 3-High correlation (High)", font_size=10, space_after=3)

# ============================================================
# SDG MAPPING
# ============================================================
add_left_text("SDG Mapping:", font_size=12, bold=True, space_after=2, keep_with_next=True)
sdg_table = doc.add_table(rows=7, cols=6)
sdg_table.style = 'Table Grid'
sdg_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sdg_headers = ["SDG", "Mapped\nIndicator", "SDG", "Mapped\nIndicator", "SDG", "Mapped\nIndicator"]
for j, h in enumerate(sdg_headers):
    set_cell_text(sdg_table.cell(0, j), h, bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade_cell(sdg_table.cell(0, j), "D9E2F3")

SDG_COLORS = {
    1: "E5243B", 2: "DDA63A", 3: "4C9F38", 4: "C5192D",
    5: "FF3A21", 6: "26BDE2", 7: "FCC30B", 8: "A21942",
    9: "FD6925", 10: "DD1367", 11: "FD9D24", 12: "BF8B2E",
    13: "3F7E44", 14: "0A97D9", 15: "56C02B", 16: "00689D",
    17: "19486A",
}
sdg_data = [
    [(1, "1 NO\nPOVERTY", False),       (7, "7 AFFORDABLE AND\nCLEAN ENERGY", False),   (13, "13 CLIMATE\nACTION", False)],
    [(2, "2 ZERO\nHUNGER", False),      (8, "8 DECENT WORK AND\nECONOMIC GROWTH", False),(14, "14 LIFE\nBELOW WATER", False)],
    [(3, "3 GOOD HEALTH\nAND WELL-BEING", False), (9, "9 INDUSTRY, INNOVATION\nAND INFRASTRUCTURE", False), (15, "15 LIFE\nON LAND", False)],
    [(4, "4 QUALITY\nEDUCATION", True),  (10, "10 REDUCED\nINEQUALITIES", True),        (16, "16 PEACE, JUSTICE\nAND STRONG INSTITUTIONS", True)],
    [(5, "5 GENDER\nEQUALITY", False),   (11, "11 SUSTAINABLE CITIES\nAND COMMUNITIES", False), (17, "17 PARTNERSHIPS\nFOR THE GOALS", False)],
    [(6, "6 CLEAN WATER\nAND SANITATION", False), (12, "12 RESPONSIBLE\nCONSUMPTION AND PRODUCTION", False), (0, "", False)],
]
for i, row in enumerate(sdg_data):
    for k, (sdg_num, sdg_name, mapped) in enumerate(row):
        sdg_col = k * 2
        ind_col = k * 2 + 1
        if sdg_num > 0:
            set_cell_text(sdg_table.cell(i + 1, sdg_col), sdg_name, bold=True, font_size=8,
                          align=WD_ALIGN_PARAGRAPH.CENTER, color=(255, 255, 255))
            shade_cell(sdg_table.cell(i + 1, sdg_col), SDG_COLORS[sdg_num])
            set_cell_text(sdg_table.cell(i + 1, ind_col), "\u2713" if mapped else "", font_size=12,
                          align=WD_ALIGN_PARAGRAPH.CENTER)
        else:
            set_cell_text(sdg_table.cell(i + 1, sdg_col), "", font_size=9)
            set_cell_text(sdg_table.cell(i + 1, ind_col), "", font_size=9)
for row in sdg_table.rows:
    row.cells[0].width = Inches(1.3)
    row.cells[1].width = Inches(0.7)
    row.cells[2].width = Inches(1.3)
    row.cells[3].width = Inches(0.7)
    row.cells[4].width = Inches(1.3)
    row.cells[5].width = Inches(0.7)
keep_table_on_one_page(sdg_table)

# ============================================================
# ABSTRACT
# ============================================================
add_page_break()
add_centered_text("ABSTRACT", font_size=16, bold=True, space_before=24, space_after=12)

add_justified_text(
    "Online hate speech and cyberbullying have become pressing challenges on social media platforms, "
    "threatening the safety and well-being of users worldwide. The exponential growth of user-generated "
    "content makes manual moderation impractical, creating an urgent need for automated detection systems "
    "that can classify harmful content accurately and efficiently. Natural Language Processing (NLP) combined "
    "with Machine Learning (ML) offers a powerful approach to addressing this challenge by learning patterns "
    "in text data that distinguish between hateful, offensive, and benign content.",
    first_line_indent=1.27
)
add_justified_text(
    "This project presents a web-based machine learning platform for detecting and classifying social media "
    "text into three categories: Hate Speech, Offensive Language, and Clean Text. The system employs six "
    "classification algorithms: Logistic Regression, Naive Bayes, Support Vector Machine (SVM), K-Nearest "
    "Neighbors (KNN), Gradient Boosting, and Random Forest. The NLP pipeline processes a dataset of 15,000 "
    "social media text samples through comprehensive text preprocessing (lowercasing, URL removal, mention "
    "removal, special character removal, stopword removal) followed by TF-IDF vectorization with 5,000 "
    "features and bigram support.",
    first_line_indent=1.27
)
add_justified_text(
    "Logistic Regression achieved the highest performance with 94.83% accuracy, 94.83% precision, 94.83% "
    "recall, and 94.81% F1-score, followed by Naive Bayes and SVM (both 94.83% accuracy), KNN (94.73%), "
    "Gradient Boosting (94.50%), and Random Forest (94.17%). The application provides interactive Chart.js "
    "visualizations including class distribution charts, text length analysis, model comparison metrics, "
    "and confusion matrices for comprehensive model evaluation.",
    first_line_indent=1.27
)
add_justified_text(
    "The platform is built using Flask (Python) with a Bootstrap 5 dark-themed user interface featuring "
    "responsive design and interactive dashboards. The system includes user authentication with SQLite "
    "database (Werkzeug password hashing), prediction history tracking with text length and word count "
    "analytics, and exploratory data analysis visualization galleries. Users register, log in, input text, "
    "and receive classification results with confidence scores. The application is containerized with Docker "
    "for reproducible deployment on port 5007.",
    first_line_indent=1.27
)
add_justified_text(
    "Keywords: Hate Speech Detection, Cyberbullying, Natural Language Processing, Text Classification, "
    "TF-IDF, Machine Learning, Logistic Regression, Naive Bayes, SVM, Flask, Bootstrap 5, SQLite, Docker.",
    first_line_indent=1.27, bold=True
)

# ============================================================
# TABLE OF CONTENTS
# ============================================================
add_page_break()
add_centered_text("TABLE OF CONTENTS", font_size=16, bold=True, space_before=24, space_after=12)

toc_entries = [
    ("Title Page", "i"),
    ("Certificate", "ii"),
    ("Declaration", "iii"),
    ("Acknowledgment", "iv"),
    ("Vision & Mission of the Institute", "v"),
    ("Vision & Mission of the Department", "vi"),
    ("Program Educational Objectives (PEOs)", "vii"),
    ("Program Outcomes (POs)", "viii"),
    ("Program Specific Outcomes (PSOs)", "ix"),
    ("Course Outcomes", "x"),
    ("Course Articulation Matrix", "xi"),
    ("SDG Mapping", "xi"),
    ("Abstract", "xii"),
    ("Table of Contents", "xiii"),
    ("List of Figures", "xiv"),
    ("List of Tables", "xv"),
    ("", ""),
    ("CHAPTER 1: INTRODUCTION", "1"),
    ("1.1    Introduction", "1"),
    ("1.2    Scope of the Project", "2"),
    ("1.3    Objectives", "3"),
    ("1.4    Problem Formulation", "3"),
    ("1.5    Existing System", "4"),
    ("1.6    Proposed System", "5"),
    ("", ""),
    ("CHAPTER 2: LITERATURE SURVEY", "7"),
    ("2.1 \u2013 2.15  Literature Reviews", "7"),
    ("", ""),
    ("CHAPTER 3: REQUIREMENT ANALYSIS AND SYSTEM SPECIFICATION", "15"),
    ("3.1    Feasibility Study", "15"),
    ("3.2    Software Requirement Specification", "16"),
    ("3.2.1    Overall Description", "16"),
    ("3.2.2    System Feature Requirement", "17"),
    ("3.2.3    Non-Functional Requirement", "18"),
    ("3.3    System Requirements", "19"),
    ("3.4    SDLC Model to be Used", "19"),
    ("3.5    Software Requirements", "20"),
    ("", ""),
    ("CHAPTER 4: SYSTEM DESIGN", "21"),
    ("4.1    Design Approach", "21"),
    ("4.2    System Architecture Diagram", "22"),
    ("4.3    UML Diagrams", "23"),
    ("4.4    User Interface Design", "26"),
    ("4.5    Database Schema", "27"),
    ("", ""),
    ("CHAPTER 5: IMPLEMENTATION", "29"),
    ("5.1    Methodologies", "29"),
    ("5.2    Implementation Details", "31"),
    ("5.3    Module Description", "32"),
    ("5.4    Sample Code", "33"),
    ("", ""),
    ("CHAPTER 6: TESTING", "37"),
    ("6.1    Types of Testing", "37"),
    ("6.2    Test Cases", "39"),
    ("", ""),
    ("CHAPTER 7: RESULTS AND DISCUSSION", "42"),
    ("7.1 \u2013 7.14  Application Screenshots", "42"),
    ("7.15 \u2013 7.19  Model Performance Figures", "49"),
    ("", ""),
    ("CHAPTER 8: CONCLUSION AND FUTURE SCOPE", "52"),
    ("8.1    Conclusion", "52"),
    ("8.2    Future Scope", "53"),
    ("", ""),
    ("CHAPTER 9: SUSTAINABLE DEVELOPMENT GOALS", "55"),
    ("9.1    SDG 16: Peace, Justice and Strong Institutions", "55"),
    ("9.2    SDG 4: Quality Education", "56"),
    ("9.3    SDG 10: Reduced Inequalities", "56"),
    ("9.4    Broader Impact", "57"),
    ("9.5    Future Contribution to SDGs", "57"),
    ("", ""),
    ("REFERENCES", "58"),
]

toc_table = doc.add_table(rows=len(toc_entries), cols=2)
toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (title, page) in enumerate(toc_entries):
    is_chapter = title.startswith("CHAPTER") or title == "REFERENCES"
    set_cell_text(toc_table.cell(i, 0), title, bold=is_chapter, font_size=11)
    set_cell_text(toc_table.cell(i, 1), page, font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_chapter)
    toc_table.cell(i, 0).width = Inches(5.0)
    toc_table.cell(i, 1).width = Inches(1.0)
    for cell in [toc_table.cell(i, 0), toc_table.cell(i, 1)]:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '</w:tcBorders>')
        tcPr.append(tcBorders)

# ============================================================
# LIST OF FIGURES
# ============================================================
add_page_break()
add_centered_text("LIST OF FIGURES", font_size=16, bold=True, space_before=24, space_after=12)

figures_list = [
    ("Fig. 4.1", "System Architecture Diagram", "22"),
    ("Fig. 4.2", "Use Case Diagram", "23"),
    ("Fig. 4.3", "NLP Pipeline Diagram", "24"),
    ("Fig. 4.4", "Data Preprocessing Pipeline", "25"),
    ("Fig. 4.5", "Activity Diagram", "26"),
    ("Fig. 5.1", "Agile Development Model", "31"),
    ("Fig. 7.1", "Login Page", "42"),
    ("Fig. 7.2", "Registration Page", "42"),
    ("Fig. 7.3", "Invalid Login Attempt", "43"),
    ("Fig. 7.4", "Duplicate Registration Attempt", "43"),
    ("Fig. 7.5", "Home Page Dashboard", "44"),
    ("Fig. 7.6", "Prediction Form", "44"),
    ("Fig. 7.7", "Hate Speech Prediction Result", "45"),
    ("Fig. 7.8", "Clean Text Prediction Result", "45"),
    ("Fig. 7.9", "Offensive Text Prediction Result", "46"),
    ("Fig. 7.10", "Prediction History", "46"),
    ("Fig. 7.11", "EDA Visualization Gallery", "47"),
    ("Fig. 7.12", "Model Dashboard", "47"),
    ("Fig. 7.13", "Dashboard Charts (Detailed)", "48"),
    ("Fig. 7.14", "About Page", "48"),
    ("Fig. 7.15", "Model Accuracy Comparison", "49"),
    ("Fig. 7.16", "Confusion Matrix (Logistic Regression)", "49"),
    ("Fig. 7.17", "Class Distribution", "50"),
    ("Fig. 7.18", "System Architecture", "50"),
    ("Fig. 7.19", "NLP Pipeline", "51"),
]

lof_table = doc.add_table(rows=len(figures_list)+1, cols=3)
lof_table.style = 'Table Grid'
lof_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_cell_text(lof_table.cell(0, 0), "Fig. No.", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(lof_table.cell(0, 1), "Title", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(lof_table.cell(0, 2), "Page No.", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
shade_cell(lof_table.cell(0, 0))
shade_cell(lof_table.cell(0, 1))
shade_cell(lof_table.cell(0, 2))
for i, (fno, ftitle, fpage) in enumerate(figures_list):
    r = i + 1
    set_cell_text(lof_table.cell(r, 0), fno, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(lof_table.cell(r, 1), ftitle, font_size=10)
    set_cell_text(lof_table.cell(r, 2), fpage, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    lof_table.cell(r, 0).width = Inches(0.8)
    lof_table.cell(r, 1).width = Inches(4.5)
    lof_table.cell(r, 2).width = Inches(0.9)

# ============================================================
# LIST OF TABLES
# ============================================================
add_page_break()
add_centered_text("LIST OF TABLES", font_size=16, bold=True, space_before=24, space_after=12)

tables_list = [
    ("Table 1.1", "Comparison of Existing Systems", "5"),
    ("Table 2.1", "Literature Survey Summary", "14"),
    ("Table 3.1", "Feasibility Study", "15"),
    ("Table 3.2", "Overall Description", "16"),
    ("Table 3.3", "System Feature Requirements", "17"),
    ("Table 3.4", "Non-Functional Requirements", "18"),
    ("Table 3.5", "Hardware Requirements", "19"),
    ("Table 3.6", "Software Requirements", "20"),
    ("Table 4.1", "Database Schema \u2013 Users Table", "27"),
    ("Table 4.2", "Database Schema \u2013 Predictions Table", "28"),
    ("Table 4.3", "Dataset Description", "28"),
    ("Table 6.1", "Test Cases \u2013 Authentication", "39"),
    ("Table 6.2", "Test Cases \u2013 Prediction", "40"),
    ("Table 6.3", "Test Cases \u2013 Visualization & Dashboard", "40"),
    ("Table 6.4", "Test Cases \u2013 Data & Security", "41"),
    ("Table 7.1", "Model Performance Comparison", "50"),
]

lot_table = doc.add_table(rows=len(tables_list)+1, cols=3)
lot_table.style = 'Table Grid'
lot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_cell_text(lot_table.cell(0, 0), "Table No.", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(lot_table.cell(0, 1), "Title", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_text(lot_table.cell(0, 2), "Page No.", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
shade_cell(lot_table.cell(0, 0))
shade_cell(lot_table.cell(0, 1))
shade_cell(lot_table.cell(0, 2))
for i, (tno, ttitle, tpage) in enumerate(tables_list):
    r = i + 1
    set_cell_text(lot_table.cell(r, 0), tno, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(lot_table.cell(r, 1), ttitle, font_size=10)
    set_cell_text(lot_table.cell(r, 2), tpage, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    lot_table.cell(r, 0).width = Inches(0.9)
    lot_table.cell(r, 1).width = Inches(4.4)
    lot_table.cell(r, 2).width = Inches(0.9)

# ============================================================
# SWITCH TO ARABIC PAGE NUMBERING
# ============================================================
new_section = doc.add_section(WD_SECTION_START.NEW_PAGE)
add_page_number(new_section, start=1, fmt='decimal')

# ============================================================
# CHAPTER 1 - INTRODUCTION
# ============================================================
p_ch1 = add_centered_text("CHAPTER 1", font_size=18, bold=True, space_before=24, space_after=3)
p_ch1.paragraph_format.keep_with_next = True
p_ch1t = add_centered_text("INTRODUCTION", font_size=16, bold=True, space_after=10)
p_ch1t.paragraph_format.keep_with_next = True

add_section_heading("1.1", "Introduction")

add_justified_text(
    "Social media platforms have become integral to modern communication, enabling billions of users worldwide "
    "to share ideas, opinions, and content in real time. However, the rapid growth of social media has also "
    "facilitated the spread of hate speech, cyberbullying, and offensive language, posing significant threats "
    "to online safety, mental health, and social cohesion. The World Health Organization and UNESCO have "
    "identified online hate speech as a growing public health concern, with studies linking exposure to hateful "
    "content with increased anxiety, depression, and social isolation among vulnerable populations.",
    first_line_indent=1.27
)
add_justified_text(
    "The sheer volume of user-generated content on platforms like Twitter, Facebook, Instagram, and Reddit "
    "makes manual moderation impractical. Major platforms report processing hundreds of millions of posts "
    "daily, far exceeding the capacity of human moderators. This creates an urgent need for automated "
    "content moderation systems that can accurately classify text as hate speech, offensive language, or "
    "clean content in real time. Natural Language Processing (NLP) combined with Machine Learning (ML) "
    "provides a scalable solution to this challenge.",
    first_line_indent=1.27
)
add_justified_text(
    "Text classification for hate speech detection involves several technical challenges: the informal and "
    "evolving nature of social media language, the use of slang, abbreviations, and coded expressions, "
    "the contextual ambiguity of potentially offensive content, and the need to distinguish between different "
    "severity levels (hate speech targeting specific groups vs. generally offensive language vs. benign content). "
    "Machine learning algorithms, particularly when combined with TF-IDF feature extraction, can learn complex "
    "patterns in text data that capture these nuances.",
    first_line_indent=1.27
)
add_justified_text(
    "This project presents a comprehensive web-based platform for social media text classification using "
    "six machine learning models: Logistic Regression, Naive Bayes, Support Vector Machine (SVM), K-Nearest "
    "Neighbors (KNN), Gradient Boosting, and Random Forest. The system processes a dataset of 15,000 social "
    "media text samples through an NLP preprocessing pipeline (lowercasing, URL/mention/hashtag removal, "
    "special character removal, stopword filtering) and TF-IDF vectorization (5,000 features, bigrams), "
    "then classifies text into three categories: Hate Speech, Offensive, and Clean.",
    first_line_indent=1.27
)
add_justified_text(
    "The Flask web framework provides the application layer, integrating NLTK for text preprocessing, "
    "scikit-learn for TF-IDF vectorization and model inference, Chart.js for interactive visualization, "
    "and SQLite for persistent user authentication and prediction history storage. The Bootstrap 5 dark-themed "
    "user interface provides a modern, professional appearance with responsive design suitable for content "
    "moderation analysts, researchers, and students studying NLP applications.",
    first_line_indent=1.27
)

add_section_heading("1.2", "Scope of the Project")

add_justified_text(
    "The scope of this project encompasses the design, development, and evaluation of an end-to-end NLP "
    "pipeline for social media hate speech and cyberbullying detection. The key areas covered include:",
    first_line_indent=1.27
)
add_bullet("Implementation of six classification models (Logistic Regression, Naive Bayes, SVM, KNN, Gradient Boosting, Random Forest) for comprehensive performance comparison on the hate speech dataset.")
add_bullet("NLP text preprocessing pipeline including lowercasing, URL removal, mention removal, hashtag removal, special character removal, whitespace normalization, and NLTK stopword filtering.")
add_bullet("TF-IDF (Term Frequency-Inverse Document Frequency) vectorization with 5,000 features and bigram support for capturing word-level and phrase-level patterns in social media text.")
add_bullet("Interactive web interface with user authentication (registration, login, logout), text input for classification, and real-time prediction with confidence scores.")
add_bullet("Three-class classification output: Hate Speech, Offensive Language, and Clean Text with probability-based confidence scores from the best model.")
add_bullet("Prediction history tracking with SQLite database storage including text length and word count analytics for each prediction.")
add_bullet("Comprehensive dashboard with model analytics showing accuracy, precision, recall, and F1-score metrics for all six classification models.")
add_bullet("Docker containerization for streamlined deployment and reproducibility across different computing environments.")

add_section_heading("1.3", "Objectives")

add_justified_text("The primary objectives of this project are:", first_line_indent=1.27)
add_bullet("To design and implement an NLP pipeline capable of accurately classifying social media text into Hate Speech, Offensive Language, and Clean Text categories.")
add_bullet("To compare the performance of six classification algorithms using accuracy, precision, recall, and F1-score metrics on the hate speech dataset.")
add_bullet("To develop a user-friendly web application with authentication for inputting text and receiving automated classification with confidence scores.")
add_bullet("To implement comprehensive text preprocessing including URL/mention/hashtag removal, special character filtering, and NLTK stopword removal.")
add_bullet("To create TF-IDF feature extraction with 5,000 features and bigram support for effective text representation.")
add_bullet("To implement interactive Chart.js visualizations for exploratory data analysis and model comparison dashboards.")
add_bullet("To demonstrate the practical applicability of NLP and ML techniques for automated content moderation.")
add_bullet("To containerize the application using Docker for consistent deployment across different environments.")

add_section_heading("1.4", "Problem Formulation")

add_justified_text(
    "Detecting hate speech and cyberbullying in social media text is a complex NLP challenge due to several "
    "inherent difficulties in processing informal, user-generated content:",
    first_line_indent=1.27
)
add_justified_text(
    "First, the dataset exhibits class imbalance with approximately 55% Clean text, 25% Offensive language, "
    "and 20% Hate Speech. This imbalance means that models may achieve high overall accuracy by favoring "
    "the majority class while performing poorly on the critical Hate Speech minority class. Evaluation using "
    "weighted precision, recall, and F1-score is essential for measuring performance across all three classes.",
    first_line_indent=1.27
)
add_justified_text(
    "Second, social media text presents unique preprocessing challenges: informal spelling, abbreviations "
    "(\"u\" for \"you\", \"2\" for \"to\"), slang, emojis, hashtags, @mentions, URLs, and code-switching between "
    "languages. The text preprocessing pipeline must handle these variations while preserving the semantic "
    "content that distinguishes hate speech from clean text. NLTK stopword removal and regex-based cleaning "
    "address these challenges systematically.",
    first_line_indent=1.27
)
add_justified_text(
    "Third, the boundary between hate speech, offensive language, and clean text is often ambiguous and "
    "context-dependent. Sarcasm, irony, and cultural references can make text that appears offensive actually "
    "benign, or vice versa. The TF-IDF representation with bigram support captures some of these contextual "
    "patterns, but the fundamental limitation of bag-of-words approaches in understanding context remains.",
    first_line_indent=1.27
)
add_justified_text(
    "Fourth, existing content moderation tools are primarily limited to proprietary API services (Perspective "
    "API, Content Moderator) that require internet connectivity, involve per-request costs, and raise data "
    "privacy concerns. A self-contained, locally-deployable system with transparent ML models would address "
    "these limitations while providing interpretable classification decisions.",
    first_line_indent=1.27
)

add_section_heading("1.5", "Existing System")

add_justified_text(
    "Current approaches to hate speech and cyberbullying detection can be categorized into manual moderation, "
    "keyword-based filtering, cloud API services, and research-focused ML tools. Each approach has distinct "
    "strengths and limitations that motivate the development of an integrated, accessible platform.",
    first_line_indent=1.27
)

add_centered_text("Table 1.1: Comparison of Existing Systems", font_size=10, bold=True, space_after=4, keep_with_next=True)
exist_table = doc.add_table(rows=5, cols=4)
exist_table.style = 'Table Grid'
exist_table.alignment = WD_TABLE_ALIGNMENT.CENTER
exist_data = [
    ("System", "Method", "Strengths", "Limitations"),
    ("Manual Moderation\n(Human reviewers)", "Manual review of\nflagged content", "Contextual understanding,\nhigh accuracy", "Extremely slow, costly,\nnot scalable, reviewer burnout"),
    ("Keyword Filtering\n(Regex/Blocklists)", "Pattern matching\nagainst word lists", "Fast, easy to implement,\nno ML required", "High false positives, easily\nevaded, no context understanding"),
    ("Cloud API Services\n(Perspective, Azure)", "Pre-trained DL models\nvia REST API", "State-of-art accuracy,\nmulti-language support", "Internet required, per-request\ncost, privacy concerns"),
    ("Our Proposed System", "6 ML models, TF-IDF,\nNLP pipeline, web UI", "Local, free, transparent,\ninteractive, secure", "English only, TF-IDF limited\ncontext understanding"),
]
for i, row_data in enumerate(exist_data):
    for j, val in enumerate(row_data):
        set_cell_text(exist_table.cell(i, j), val, bold=(i == 0), font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER if j != 3 else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(exist_table.cell(i, j))
    exist_table.cell(i, 0).width = Inches(1.3)
    exist_table.cell(i, 1).width = Inches(1.5)
    exist_table.cell(i, 2).width = Inches(1.4)
    exist_table.cell(i, 3).width = Inches(2.0)
keep_table_on_one_page(exist_table)

add_justified_text("The disadvantages of existing systems include:", space_before=6)
add_bullet("Manual moderation cannot scale to handle millions of daily posts on major social media platforms.")
add_bullet("Keyword filtering produces high false positive rates and is easily circumvented by misspellings or coded language.")
add_bullet("Cloud-based API services require internet connectivity, incur per-request costs, and raise data privacy concerns.")
add_bullet("Research ML tools require programming expertise and lack user-friendly web interfaces with authentication.")
add_bullet("No integrated platform combines NLP preprocessing, multiple model comparison, interactive visualization, authentication, and prediction history.")

add_section_heading("1.6", "Proposed System")

add_justified_text(
    "The proposed system addresses the limitations of existing approaches by providing a self-contained, "
    "web-based NLP platform for hate speech and cyberbullying detection. The system includes user "
    "authentication with secure password hashing, prediction history tracking with text analytics, "
    "and comprehensive model comparison through an interactive dashboard.",
    first_line_indent=1.27
)
add_justified_text("The key advantages of the proposed system include:", space_before=4)
add_bullet("Six classification models (Logistic Regression, Naive Bayes, SVM, KNN, Gradient Boosting, Random Forest) with the best model (Logistic Regression, 94.83% accuracy) used for predictions.")
add_bullet("Comprehensive NLP preprocessing pipeline that handles URL removal, mention/hashtag stripping, special character filtering, and NLTK stopword removal automatically.")
add_bullet("TF-IDF vectorization with 5,000 features and bigram support for effective text representation capturing both individual words and two-word phrases.")
add_bullet("Three-class classification (Hate Speech, Offensive, Clean) with probability-based confidence scores for nuanced content assessment.")
add_bullet("Secure user authentication using Werkzeug password hashing with SQLite database storage for user accounts and prediction history.")
add_bullet("Prediction history with text length and word count analytics enabling users to review and analyze past classifications.")
add_bullet("Interactive Chart.js visualizations for EDA and model comparison dashboards with accuracy, precision, recall, and F1-score metrics.")
add_bullet("Bootstrap 5 dark-themed responsive user interface with modern design and intuitive navigation.")
add_bullet("Docker containerization for one-command deployment on any machine with Docker installed.")

add_justified_text(
    "The proposed system follows a Model-View-Controller (MVC) architecture with Flask handling HTTP "
    "requests, SQLite providing persistent storage for users and predictions, scikit-learn powering the "
    "NLP/ML classification pipeline, and Chart.js generating interactive visualizations. The pre-trained "
    "Logistic Regression model and TF-IDF vectorizer are loaded at application startup for fast prediction "
    "responses, while the dashboard provides comprehensive analytics comparing all six trained models.",
    first_line_indent=1.27
)

# ============================================================
# CHAPTER 2 - LITERATURE SURVEY
# ============================================================
p_ch2 = add_centered_text("CHAPTER 2", font_size=18, bold=True, space_before=24, space_after=3)
p_ch2.paragraph_format.keep_with_next = True
p_ch2.paragraph_format.page_break_before = True
p_ch2t = add_centered_text("LITERATURE SURVEY", font_size=16, bold=True, space_after=10)
p_ch2t.paragraph_format.keep_with_next = True

add_section_heading("2.1", "NLP for Hate Speech Detection")
add_justified_text(
    "Davidson et al. (2017) conducted a foundational study on automated hate speech detection, creating a "
    "labeled dataset of 25,000 tweets classified into hate speech, offensive language, and neither. Their work "
    "demonstrated that distinguishing between hate speech and general offensive language is significantly more "
    "challenging than binary classification, as many offensive tweets do not target specific protected groups. "
    "They achieved 90% accuracy using logistic regression with TF-IDF features, establishing a benchmark "
    "for subsequent research in multi-class hate speech classification.",
    first_line_indent=1.27
)
add_justified_text(
    "Their study identified key challenges in hate speech detection: the subjective nature of hate speech "
    "definitions, inter-annotator disagreement, and the tendency of models to conflate offensive language "
    "with targeted hate speech. These insights informed our three-class classification approach (Hate Speech, "
    "Offensive, Clean) and our use of multiple evaluation metrics beyond simple accuracy.",
    first_line_indent=1.27
)

add_section_heading("2.2", "Text Classification with Machine Learning")
add_justified_text(
    "Sebastiani (2002) provided a comprehensive survey of machine learning methods for text classification, "
    "covering feature extraction, dimensionality reduction, and classifier evaluation. The survey established "
    "that text classification is fundamentally a high-dimensional problem where documents are represented as "
    "vectors in a space defined by vocabulary terms. Key decisions include feature representation (bag-of-words "
    "vs. n-grams), feature weighting (binary, TF, TF-IDF), and classifier selection.",
    first_line_indent=1.27
)
add_justified_text(
    "For social media hate speech detection, text classification faces additional challenges: short document "
    "length, informal vocabulary, misspellings, and evolving slang. Our project addresses these by combining "
    "comprehensive text preprocessing with TF-IDF vectorization using bigrams to capture contextual phrases, "
    "and evaluating six diverse classifiers to identify the best approach for this specific domain.",
    first_line_indent=1.27
)

add_section_heading("2.3", "TF-IDF Feature Extraction")
add_justified_text(
    "Salton and Buckley (1988) formalized Term Frequency-Inverse Document Frequency (TF-IDF) as a numerical "
    "statistic that reflects the importance of a word to a document in a collection. TF-IDF assigns higher "
    "weights to terms that are frequent in a specific document but rare across the corpus, effectively "
    "capturing discriminative vocabulary. The mathematical formulation TF-IDF(t,d) = TF(t,d) x log(N/DF(t)) "
    "balances term frequency with document frequency to produce informative feature vectors.",
    first_line_indent=1.27
)
add_justified_text(
    "In our hate speech detection system, TF-IDF vectorization with max_features=5000 and ngram_range=(1,2) "
    "creates feature vectors that capture both individual words and bigrams (two-word phrases). This is "
    "particularly effective for hate speech detection, as hateful content often uses specific phrases and "
    "word combinations that are more discriminative than individual words alone. The 5,000-feature limit "
    "balances representation quality with computational efficiency.",
    first_line_indent=1.27
)

add_section_heading("2.4", "Logistic Regression for Text Classification")
add_justified_text(
    "Hosmer, Lemeshow, and Sturdivant (2013) provided a comprehensive treatment of logistic regression for "
    "classification tasks. For multi-class text classification, the multinomial logistic regression (softmax) "
    "extension models the probability of each class using the softmax function applied to linear combinations "
    "of TF-IDF features. Logistic regression is particularly effective for high-dimensional sparse data like "
    "TF-IDF vectors, as the L2 regularization prevents overfitting and the model provides calibrated "
    "probability estimates that serve as confidence scores.",
    first_line_indent=1.27
)
add_justified_text(
    "In our project, Logistic Regression achieved the best performance with 94.83% accuracy, demonstrating "
    "that for well-preprocessed TF-IDF features, a linear model can effectively separate the three text "
    "classes. The model's max_iter=1000 ensures convergence, and its probability outputs provide meaningful "
    "confidence scores for each prediction.",
    first_line_indent=1.27
)

add_section_heading("2.5", "Naive Bayes for NLP")
add_justified_text(
    "McCallum and Nigam (1998) compared event models for Naive Bayes text classification, demonstrating "
    "that the multinomial model outperforms the multivariate Bernoulli model for most text classification "
    "tasks. Multinomial Naive Bayes assumes that features are generated from a multinomial distribution, "
    "making it naturally suited for word count and TF-IDF features. Despite its strong independence "
    "assumption, Naive Bayes often performs competitively with more complex models due to its ability to "
    "handle high-dimensional feature spaces efficiently.",
    first_line_indent=1.27
)
add_justified_text(
    "In our hate speech detection system, MultinomialNB achieved 94.83% accuracy, matching Logistic "
    "Regression. This demonstrates that the conditional independence assumption does not significantly "
    "harm performance for TF-IDF features in this domain, as the discriminative vocabulary for each class "
    "is relatively distinct after preprocessing.",
    first_line_indent=1.27
)

add_section_heading("2.6", "Support Vector Machines for Text")
add_justified_text(
    "Joachims (1998) demonstrated that SVMs are particularly well-suited for text classification due to "
    "the high dimensionality and sparsity of text feature vectors. SVMs find the maximum-margin hyperplane "
    "separating classes in the feature space, and the kernel trick enables non-linear decision boundaries "
    "when needed. For text classification, linear SVMs often perform as well as non-linear kernels while "
    "being significantly faster to train on large feature spaces.",
    first_line_indent=1.27
)
add_justified_text(
    "Our project uses LinearSVC wrapped in CalibratedClassifierCV for probability estimates, achieving "
    "94.83% accuracy. The linear kernel is appropriate for the high-dimensional TF-IDF feature space "
    "(5,000 features), and the calibration wrapper provides the probability outputs needed for confidence "
    "scores in the web application.",
    first_line_indent=1.27
)

add_section_heading("2.7", "Random Forest for Text Classification")
add_justified_text(
    "Breiman (2001) introduced Random Forest, an ensemble of decision trees using bagging and random feature "
    "selection. For text classification, Random Forest handles high-dimensional sparse features by selecting "
    "random subsets of TF-IDF features at each split, preventing overfitting. The ensemble approach averages "
    "predictions from multiple trees, producing robust classification with built-in feature importance "
    "estimation that reveals which words and phrases are most discriminative for each class.",
    first_line_indent=1.27
)
add_justified_text(
    "In our project, Random Forest with n_estimators=100 achieved 94.17% accuracy. While slightly lower "
    "than linear models, Random Forest provides feature importance rankings that identify the most "
    "discriminative words and bigrams for hate speech detection, offering interpretable insights.",
    first_line_indent=1.27
)

add_section_heading("2.8", "Gradient Boosting for NLP")
add_justified_text(
    "Friedman (2001) developed Gradient Boosting Machines, sequential ensembles where each tree corrects "
    "errors of the previous ensemble. For text classification, Gradient Boosting iteratively focuses on "
    "misclassified samples, which is beneficial for detecting hate speech in ambiguous cases where class "
    "boundaries are unclear. The sequential optimization often achieves higher accuracy than Random Forest "
    "for structured data, though the advantage is less pronounced for sparse text features.",
    first_line_indent=1.27
)
add_justified_text(
    "Our Gradient Boosting classifier with n_estimators=100 achieved 94.50% accuracy. The moderate "
    "performance improvement over Random Forest (94.17%) confirms that sequential optimization provides "
    "marginal benefits for TF-IDF text features, while linear models (Logistic Regression, SVM) achieve "
    "the best results in this high-dimensional sparse feature space.",
    first_line_indent=1.27
)

add_section_heading("2.9", "K-Nearest Neighbors for Text")
add_justified_text(
    "Cover and Hart (1967) introduced the K-Nearest Neighbors algorithm, a non-parametric method that "
    "classifies samples based on the majority vote of their K nearest neighbors in feature space. For text "
    "classification with TF-IDF features, KNN measures similarity between documents using cosine distance "
    "or Euclidean distance. The instance-based approach requires no training phase but has high inference "
    "time complexity, making it less suitable for real-time applications with large training sets.",
    first_line_indent=1.27
)
add_justified_text(
    "In our project, KNN with K=5 achieved 94.73% accuracy. While competitive with other models, KNN's "
    "inference time scales with the training set size, making it less efficient than linear models for "
    "production deployment. However, KNN provides useful insights into the local structure of the "
    "feature space around hate speech samples.",
    first_line_indent=1.27
)

add_section_heading("2.10", "Text Preprocessing Techniques")
add_justified_text(
    "Bird, Klein, and Loper (2009) authored the definitive guide to NLP with Python using NLTK, covering "
    "tokenization, stemming, lemmatization, stopword removal, and other preprocessing techniques essential "
    "for text classification. For social media text, preprocessing must handle domain-specific artifacts "
    "including URLs, @mentions, hashtags, emojis, and non-standard capitalization. NLTK's English stopword "
    "list removes 179 common function words that carry minimal discriminative information.",
    first_line_indent=1.27
)
add_justified_text(
    "Our preprocessing pipeline implements: (1) lowercasing for case normalization, (2) regex-based URL "
    "removal, (3) @mention stripping, (4) hashtag removal, (5) special character/number removal, "
    "(6) whitespace normalization, and (7) NLTK stopword filtering. This comprehensive pipeline converts "
    "raw social media text into clean tokens suitable for TF-IDF vectorization.",
    first_line_indent=1.27
)

add_section_heading("2.11", "Flask for NLP Web Applications")
add_justified_text(
    "Grinberg (2018) authored the definitive guide on Flask web development. Flask's microframework "
    "architecture provides core HTTP handling while allowing seamless integration with Python's NLP and "
    "ML libraries. For our hate speech detection platform, Flask connects the web interface to the NLP "
    "pipeline, enabling users to submit text through a form, receive classification results with confidence "
    "scores, and review prediction history without programming knowledge.",
    first_line_indent=1.27
)

add_section_heading("2.12", "SQLite for Lightweight Storage")
add_justified_text(
    "Owens (2006) described SQLite as a self-contained, serverless relational database ideal for embedded "
    "applications. Our platform uses SQLite (hate_speech.db) with two tables: users (storing credentials "
    "and admin flags) and predictions (storing input text, classification results, confidence scores, text "
    "length, and word count). SQLite's file-based architecture simplifies deployment and Docker integration.",
    first_line_indent=1.27
)

add_section_heading("2.13", "Web Authentication and Security")
add_justified_text(
    "OWASP (2021) published comprehensive guidelines for web application security. Our platform implements "
    "secure authentication using Werkzeug's generate_password_hash() and check_password_hash() functions "
    "with PBKDF2-SHA256. The @login_required decorator protects all sensitive routes from unauthorized access. "
    "Flask session management maintains authentication state across requests.",
    first_line_indent=1.27
)

add_section_heading("2.14", "Bootstrap 5 for Responsive Web Design")
add_justified_text(
    "Bootstrap (2021) version 5 provides responsive design with dark theme support. Our hate speech "
    "detection platform uses Bootstrap 5's dark theme for all pages, with the responsive grid system "
    "ensuring that text input forms, prediction results, history tables, and dashboard analytics display "
    "correctly across all device sizes.",
    first_line_indent=1.27
)

add_section_heading("2.15", "Docker for ML Application Deployment")
add_justified_text(
    "Merkel (2014) described Docker as a platform for creating portable containers that run consistently "
    "across environments. Our Dockerfile builds a complete application image from Python 3.11-slim, installs "
    "all dependencies (Flask, NLTK, scikit-learn, werkzeug), and configures the application to run on port "
    "5007 for one-command deployment.",
    first_line_indent=1.27
)

# Literature Survey Summary Table
add_page_break()
add_centered_text("Table 2.1: Literature Survey Summary", font_size=10, bold=True, space_before=6, space_after=4, keep_with_next=True)
lit_table = doc.add_table(rows=16, cols=4)
lit_table.style = 'Table Grid'
lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER

lit_data = [
    ("S.No.", "Author(s) / Year", "Topic", "Key Contribution"),
    ("1", "Davidson et al. (2017)", "Hate Speech Detection", "Three-class hate speech dataset and classification benchmark"),
    ("2", "Sebastiani (2002)", "Text Classification", "Comprehensive survey of ML methods for text categorization"),
    ("3", "Salton & Buckley (1988)", "TF-IDF", "Term weighting scheme for document representation"),
    ("4", "Hosmer et al. (2013)", "Logistic Regression", "Multinomial logistic regression for multi-class classification"),
    ("5", "McCallum & Nigam (1998)", "Naive Bayes", "Multinomial NB for text classification"),
    ("6", "Joachims (1998)", "SVM for Text", "Linear SVM effectiveness for high-dimensional text features"),
    ("7", "Breiman (2001)", "Random Forest", "Bagging + random features; ensemble classification"),
    ("8", "Friedman (2001)", "Gradient Boosting", "Sequential tree optimization; error correction"),
    ("9", "Cover & Hart (1967)", "KNN", "Instance-based classification; non-parametric method"),
    ("10", "Bird et al. (2009)", "NLTK", "Python NLP toolkit; stopwords, tokenization, preprocessing"),
    ("11", "Grinberg (2018)", "Flask Framework", "Lightweight web development for ML integration"),
    ("12", "Owens (2006)", "SQLite", "Serverless embedded relational database engine"),
    ("13", "OWASP (2021)", "Web Security", "Authentication, password hashing, session management"),
    ("14", "Bootstrap (2021)", "Bootstrap 5", "Responsive dark-theme CSS framework"),
    ("15", "Merkel (2014)", "Docker", "Containerization; reproducible deployment"),
]

for i, row_data in enumerate(lit_data):
    for j, val in enumerate(row_data):
        set_cell_text(lit_table.cell(i, j), val, bold=(i == 0), font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(lit_table.cell(i, j))
    lit_table.cell(i, 0).width = Inches(0.4)
    lit_table.cell(i, 1).width = Inches(1.6)
    lit_table.cell(i, 2).width = Inches(1.4)
    lit_table.cell(i, 3).width = Inches(2.8)
keep_table_on_one_page(lit_table)

add_justified_text(
    "The literature survey demonstrates that NLP combined with machine learning classification methods "
    "provides effective automated hate speech detection. TF-IDF feature extraction, comprehensive text "
    "preprocessing, and multiple classifier comparison form a robust pipeline for social media content "
    "classification, while Flask, SQLite, Bootstrap 5, and Docker enable practical deployment.",
    space_before=8
)

# ============================================================
# CHAPTER 3 - REQUIREMENT ANALYSIS
# ============================================================
p_ch3 = add_centered_text("CHAPTER 3", font_size=18, bold=True, space_before=24, space_after=3)
p_ch3.paragraph_format.keep_with_next = True
p_ch3.paragraph_format.page_break_before = True
p_ch3t = add_centered_text("REQUIREMENT ANALYSIS AND SYSTEM SPECIFICATION", font_size=16, bold=True, space_after=10)
p_ch3t.paragraph_format.keep_with_next = True

add_section_heading("3.1", "Feasibility Study")

add_justified_text(
    "A feasibility study evaluates the practicality and viability of a proposed project before significant "
    "resources are committed to its development. For this social media hate speech analysis system, the feasibility "
    "analysis covers three critical dimensions: technical feasibility, economic feasibility, and operational feasibility.",
    space_after=2, keep_with_next=True
)

add_centered_text("Table 3.1: Feasibility Study Table", font_size=10, bold=True, space_after=2, keep_with_next=True)
feas_table = doc.add_table(rows=4, cols=2)
feas_table.style = 'Table Grid'
feas_table.alignment = WD_TABLE_ALIGNMENT.CENTER
feas_data = [
    ("Feasibility Type", "Description"),
    ("Technical Feasibility", "The system uses Python, Flask, scikit-learn, NLTK, TF-IDF vectorization, Bootstrap 5, and SQLite \u2014 all mature, well-documented technologies with active communities. The six classification models require moderate computational resources for training (under 120 seconds on the 15,000-row dataset). Docker provides cross-platform deployment compatibility."),
    ("Economic Feasibility", "All technologies used are free and open-source (Python, Flask, scikit-learn, NLTK, Chart.js, Bootstrap, SQLite). No licensing fees are required. The system runs on commodity hardware with 4GB+ RAM. The labeled hate speech dataset is publicly available at no cost. The estimated development time is 6-8 weeks for a team of students."),
    ("Operational Feasibility", "The system provides an intuitive web interface with user authentication, a simple text input form for analysis, and interactive dashboards. Users register once, log in, enter text content for classification, and receive immediate predictions with confidence scores. Prediction history is stored for future reference. The Flask application can be deployed via Docker for containerized deployment."),
]
for i, (ftype, desc) in enumerate(feas_data):
    set_cell_text(feas_table.cell(i, 0), ftype, bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(feas_table.cell(i, 1), desc, font_size=10)
    feas_table.cell(i, 0).width = Inches(1.4)
    feas_table.cell(i, 1).width = Inches(4.8)
    if i == 0:
        shade_cell(feas_table.cell(i, 0))
        shade_cell(feas_table.cell(i, 1))
keep_table_on_one_page(feas_table)

add_section_heading("3.2", "Software Requirement Specification")

add_subsection_heading("3.2.1", "Overall Description")
add_centered_text("Table 3.2: Overall Description", font_size=10, bold=True, space_after=4, keep_with_next=True)
od_table = doc.add_table(rows=8, cols=2)
od_table.style = 'Table Grid'
od_table.alignment = WD_TABLE_ALIGNMENT.CENTER
od_data = [
    ("Parameter", "Description"),
    ("Product Name", "Social Media Forensics: Cyberbullying & Hate Speech Analysis Platform"),
    ("Product Type", "Web-based NLP Text Classification Application"),
    ("Purpose", "Automated detection and classification of hate speech, offensive language, and clean text using 6 ML models with TF-IDF features"),
    ("Users", "Social media moderators, researchers, policy analysts, students"),
    ("Platform", "Cross-platform (accessible via web browser)"),
    ("Database", "SQLite (hate_speech.db) for user accounts and prediction history"),
    ("Authentication", "Werkzeug password hashing with Flask session management"),
]
for i, (param, desc) in enumerate(od_data):
    set_cell_text(od_table.cell(i, 0), param, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(od_table.cell(i, 1), desc, bold=(i == 0), font_size=10)
    od_table.cell(i, 0).width = Inches(1.5)
    od_table.cell(i, 1).width = Inches(4.7)
    if i == 0:
        shade_cell(od_table.cell(i, 0))
        shade_cell(od_table.cell(i, 1))
keep_table_on_one_page(od_table)

p_sfr = add_subsection_heading("3.2.2", "System Feature Requirement")
p_sfr.paragraph_format.page_break_before = True
add_centered_text("Table 3.3: System Feature Requirements", font_size=10, bold=True, space_after=4, keep_with_next=True)
sfr_table = doc.add_table(rows=8, cols=2)
sfr_table.style = 'Table Grid'
sfr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sfr_data = [
    ("Feature", "Description"),
    ("User Authentication", "Secure registration and login with Werkzeug password hashing; role-based access control (admin/user)"),
    ("Text Classification", "Single text input form for content analysis; real-time 3-class prediction (Hate Speech / Offensive / Clean) with confidence score using pre-trained Logistic Regression model"),
    ("Prediction History", "SQLite-stored history of past predictions with input text, classification outcome, confidence scores, text length, word count, and timestamps"),
    ("EDA Visualizations", "Gallery of matplotlib/seaborn charts showing dataset distributions, word clouds, class balance, and feature analysis across the hate speech dataset"),
    ("Model Dashboard", "Comprehensive analytics comparing accuracy, precision, recall, and F1-score for all 6 classification models with Chart.js visualizations"),
    ("NLP Preprocessing", "Automated pipeline: lowercasing, URL/mention/hashtag removal, special character filtering, NLTK stopword removal, TF-IDF vectorization (5000 features, bigrams)"),
    ("About Page", "Project information, technology stack description, model details, and team information"),
]
for i, (feat, desc) in enumerate(sfr_data):
    set_cell_text(sfr_table.cell(i, 0), feat, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(sfr_table.cell(i, 1), desc, bold=(i == 0), font_size=10)
    sfr_table.cell(i, 0).width = Inches(1.5)
    sfr_table.cell(i, 1).width = Inches(4.7)
    if i == 0:
        shade_cell(sfr_table.cell(i, 0))
        shade_cell(sfr_table.cell(i, 1))
keep_table_on_one_page(sfr_table)

p_nfr = add_subsection_heading("3.2.3", "Non-Functional Requirement")
add_centered_text("Table 3.4: Non-Functional Requirements", font_size=10, bold=True, space_after=4, keep_with_next=True)
nfr_table = doc.add_table(rows=7, cols=2)
nfr_table.style = 'Table Grid'
nfr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
nfr_data = [
    ("Requirement", "Description"),
    ("Performance", "Prediction response under 1 second (pre-trained model + TF-IDF vectorizer); page load under 2 seconds; chart rendering under 3 seconds"),
    ("Usability", "Intuitive single text input interface; Bootstrap 5 dark theme; responsive design; clear 3-class prediction display with color-coded confidence score"),
    ("Scalability", "Modular architecture supports additional ML models, new classification categories, and extended NLP preprocessing steps"),
    ("Reliability", "Graceful error handling for empty text, authentication failures, and malformed input; SQLite transaction safety; NLTK fallback download"),
    ("Portability", "Docker containerization; cross-platform Flask deployment; SQLite requires no database server"),
    ("Security", "Werkzeug password hashing (PBKDF2-SHA256); Flask session management; @login_required route protection; no plain-text passwords"),
]
for i, (req, desc) in enumerate(nfr_data):
    set_cell_text(nfr_table.cell(i, 0), req, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(nfr_table.cell(i, 1), desc, bold=(i == 0), font_size=10)
    nfr_table.cell(i, 0).width = Inches(1.3)
    nfr_table.cell(i, 1).width = Inches(4.9)
    if i == 0:
        shade_cell(nfr_table.cell(i, 0))
        shade_cell(nfr_table.cell(i, 1))
keep_table_on_one_page(nfr_table)

add_section_heading("3.3", "System Requirements")
add_centered_text("Table 3.5: Hardware Requirements", font_size=10, bold=True, space_after=4, keep_with_next=True)
hw_table = doc.add_table(rows=6, cols=2)
hw_table.style = 'Table Grid'
hw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hw_data = [
    ("Component", "Minimum Requirement"),
    ("Processor", "Intel Core i3 or equivalent (dual-core)"),
    ("RAM", "4 GB (recommended 8 GB for TF-IDF vectorization and model training)"),
    ("Storage", "500 MB for application, dependencies, TF-IDF model, and SQLite database"),
    ("GPU", "Not required (CPU-only computation)"),
    ("Network", "Internet connection for initial NLTK data download; offline operation supported after setup"),
]
for i, (comp, req) in enumerate(hw_data):
    set_cell_text(hw_table.cell(i, 0), comp, bold=(i == 0), font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(hw_table.cell(i, 1), req, bold=(i == 0), font_size=10)
    hw_table.cell(i, 0).width = Inches(1.3)
    hw_table.cell(i, 1).width = Inches(4.9)
    if i == 0:
        shade_cell(hw_table.cell(i, 0))
        shade_cell(hw_table.cell(i, 1))
keep_table_on_one_page(hw_table)

add_section_heading("3.4", "SDLC Model to be Used")

add_justified_text(
    "The project follows the Agile Software Development Life Cycle (SDLC) model, which emphasizes iterative "
    "development, continuous feedback, and adaptability to changing requirements. The Agile approach is "
    "particularly suitable for this project because the system integrates multiple components (NLP preprocessing, "
    "TF-IDF feature extraction, multi-model training, web application, visualization, and database) that benefit from "
    "incremental integration and testing.",
    first_line_indent=1.27
)
add_bullet("Iterative Development: The system is built in sprints, with each sprint delivering a functional increment.")
add_bullet("Continuous Integration: NLP pipeline, ML models, web UI, database, and visualizations are integrated early and often.")
add_bullet("Flexibility: Requirements can evolve as the team gains insights from initial text classification results.")
add_bullet("Rapid Prototyping: Flask's lightweight architecture enables quick prototype development and user feedback cycles.")

add_section_heading("3.5", "Software Requirements")
add_centered_text("Table 3.6: Software Requirements", font_size=10, bold=True, space_after=4, keep_with_next=True)
sw_table = doc.add_table(rows=11, cols=3)
sw_table.style = 'Table Grid'
sw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sw_data = [
    ("Category", "Software", "Version / Details"),
    ("Programming Language", "Python", "3.11"),
    ("Web Framework", "Flask", "2.x (with Jinja2 templates)"),
    ("Data Processing", "pandas, NumPy", "2.x (DataFrame manipulation, CSV I/O)"),
    ("Machine Learning", "scikit-learn", "1.x (6 classification models)"),
    ("NLP", "NLTK, TF-IDF", "NLTK stopwords + TfidfVectorizer (5000 features)"),
    ("Visualization", "Chart.js, matplotlib, seaborn", "4.x (client-side charts + server-side EDA)"),
    ("Database", "SQLite", "3.x (hate_speech.db, serverless)"),
    ("Frontend", "Bootstrap 5", "5.x (dark theme, responsive design)"),
    ("Security", "Werkzeug", "2.x (password hashing, PBKDF2-SHA256)"),
    ("Containerization", "Docker", "20.x+ (Python 3.11-slim base)"),
]
for i, row_data in enumerate(sw_data):
    for j, val in enumerate(row_data):
        set_cell_text(sw_table.cell(i, j), val, bold=(i == 0), font_size=10,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j != 2 else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(3):
            shade_cell(sw_table.cell(i, j))
    sw_table.cell(i, 0).width = Inches(1.5)
    sw_table.cell(i, 1).width = Inches(1.5)
    sw_table.cell(i, 2).width = Inches(3.2)
keep_table_on_one_page(sw_table)

# ============================================================
# CHAPTER 4 - SYSTEM DESIGN
# ============================================================
p_ch4 = add_centered_text("CHAPTER 4", font_size=18, bold=True, space_before=24, space_after=3)
p_ch4.paragraph_format.keep_with_next = True
p_ch4.paragraph_format.page_break_before = True
p_ch4t = add_centered_text("SYSTEM DESIGN", font_size=16, bold=True, space_after=10)
p_ch4t.paragraph_format.keep_with_next = True

add_section_heading("4.1", "Design Approach")

add_justified_text(
    "The hate speech analysis system follows the Model-View-Controller (MVC) architectural pattern "
    "with persistent storage. The Model layer comprises the pre-trained scikit-learn classification models "
    "(loaded from pickle files at startup) along with the TF-IDF vectorizer and the SQLite database schema "
    "(users and predictions tables). The View layer is implemented using 9 Jinja2 templates (base.html, "
    "login.html, register.html, home.html, predict.html, history.html, visualize.html, dashboard.html, "
    "about.html) all extending a common base template with Bootstrap 5 dark theme styling and consistent navigation.",
    first_line_indent=1.27
)

add_justified_text(
    "The Controller layer consists of 10 Flask route handlers managing authentication (/, /register, /login, "
    "/logout), core features (/home, /predict, /history), analytics (/visualize, /dashboard), and information "
    "(/about). Authentication routes handle user registration with password hashing and login verification. "
    "The /predict route processes the text input, applies NLP preprocessing (lowercasing, URL removal, "
    "mention/hashtag removal, special character filtering, stopword removal), transforms the cleaned text "
    "using the pre-trained TF-IDF vectorizer, passes the feature vector to the Logistic Regression model, "
    "and stores the prediction result in SQLite with a confidence score.",
    first_line_indent=1.27
)

add_justified_text(
    "The NLP and ML pipeline is executed offline during model training (train_model.py), which preprocesses "
    "all text data, builds the TF-IDF vocabulary (5000 features with unigrams and bigrams), trains all six models, "
    "evaluates them, and serializes the best model (Logistic Regression) along with the TF-IDF vectorizer to "
    "pickle files. At runtime, the Flask application loads these pre-trained artifacts, enabling sub-second "
    "prediction responses. This separation of training and inference ensures fast user experience while "
    "maintaining the flexibility to retrain models with updated data.",
    first_line_indent=1.27
)

add_section_heading("4.2", "System Architecture Diagram")

add_justified_text(
    "The system architecture illustrates the interaction between the user interface, Flask application layer, "
    "NLP preprocessing pipeline, machine learning models, SQLite database, and visualization components. "
    "The architecture follows a request-response pattern: authenticated users submit text content through the "
    "web browser, Flask processes the request through the NLP pipeline, the pre-trained model generates a "
    "3-class prediction, the result is stored in SQLite, and the classification with confidence score is "
    "rendered back to the user.",
    first_line_indent=1.27
)

add_justified_text(
    "The system has three main data flows: (1) Authentication flow \u2014 user registration stores hashed "
    "passwords in the users table, login verifies credentials and creates a session; (2) Classification flow "
    "\u2014 text input is preprocessed (lowercased, cleaned, stopwords removed), vectorized using TF-IDF, "
    "passed to the Logistic Regression model, result stored in predictions table, and rendered to the user; "
    "(3) Analytics flow \u2014 dashboard and visualization pages query the models_info.json file and dataset "
    "to generate Chart.js visualizations comparing all six models.",
    first_line_indent=1.27
)

add_figure(os.path.join(FIGURES_DIR, "fig_system_architecture.png"),
           "Figure 4.1: System Architecture Diagram", width=Inches(5.5))

add_section_heading("4.3", "UML Diagrams")

add_subsection_heading("4.3.1", "Use Case Diagram")
add_justified_text(
    "The use case diagram identifies two actor types: Guest (unauthenticated) and User (authenticated). "
    "Guest actors can register and log in. Authenticated users can perform the following operations: "
    "view the home dashboard with analysis statistics, input text content and receive hate speech "
    "classification, view prediction history, explore EDA visualizations, analyze model performance on the "
    "dashboard, view project information on the about page, and log out. Admin users additionally see "
    "global statistics (total users, total predictions, total hate speech detections) on the home page.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_use_case_diagram.png"),
           "Figure 4.2: Use Case Diagram", width=Inches(5.0))

add_subsection_heading("4.3.2", "NLP Pipeline Diagram")
add_justified_text(
    "The NLP pipeline diagram shows the text processing flow from raw social media input to model prediction. "
    "The pipeline comprises six stages: (1) Text Input (receive raw text from user), (2) Preprocessing "
    "(lowercase, remove URLs, @mentions, #hashtags, special characters, extra whitespace), (3) Stopword "
    "Removal (filter English stopwords using NLTK corpus), (4) TF-IDF Vectorization (transform cleaned text "
    "into 5000-dimensional feature vector using unigrams and bigrams with min_df=2), (5) Model Inference "
    "(pass feature vector to pre-trained Logistic Regression classifier), and (6) Output (return 3-class "
    "prediction with probability-based confidence score).",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_nlp_pipeline.png"),
           "Figure 4.3: NLP Pipeline Diagram", width=Inches(5.0))

add_subsection_heading("4.3.3", "Data Preprocessing Pipeline")
add_justified_text(
    "The data preprocessing pipeline details the transformation steps applied to the raw hate speech dataset. "
    "Step 1: Load the labeled CSV dataset (15,000 text samples with 3 class labels). Step 2: Apply text "
    "cleaning to each sample (lowercasing, URL/mention/hashtag removal, special character filtering, "
    "whitespace normalization). Step 3: Remove English stopwords using NLTK's stopwords corpus. Step 4: "
    "Build TF-IDF vocabulary from the training set (max_features=5000, ngram_range=(1,2), min_df=2). "
    "Step 5: Transform text into sparse feature matrices. Step 6: Stratified 80/20 train-test split "
    "preserving the 3-class distribution.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_data_preprocessing.png"),
           "Figure 4.4: Data Preprocessing Pipeline", width=Inches(5.0))

add_subsection_heading("4.3.4", "Activity Diagram")
add_justified_text(
    "The activity diagram shows the complete user workflow from application access to text classification. "
    "A new user accesses the login page, navigates to registration, creates an account with name, username, "
    "and password, and is redirected to login. An existing user logs in with credentials, which are verified "
    "against hashed passwords in the users table. After successful authentication, the user is directed "
    "to the home page showing analysis statistics. From there, the user can navigate to predict (enter text, "
    "submit, view classification result), history (review past predictions), visualize (explore EDA charts), "
    "dashboard (compare model metrics), or about (project info). The user can log out at any time.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_nlp_pipeline.png"),
           "Figure 4.5: Activity Diagram", width=Inches(5.0))

add_section_heading("4.4", "User Interface Design")

add_justified_text(
    "The user interface is designed using Bootstrap 5's dark theme with a consistent navigation bar across "
    "all pages. The base template (base.html) defines the common layout including the navbar with links to "
    "Home, Predict, History, Visualize, Dashboard, About, and Logout. All pages use Bootstrap's card "
    "components, form controls, and grid system for responsive layout. The dark theme reduces eye strain "
    "during extended use and provides a modern, professional appearance suitable for content moderation tools.",
    first_line_indent=1.27
)

add_justified_text(
    "The prediction page (predict.html) features a single textarea input where users paste or type social "
    "media text for analysis. Upon submission, the classification result is displayed prominently with a "
    "color-coded badge (red for Hate Speech, orange for Offensive, green for Clean) along with the confidence "
    "percentage. The result card also shows text statistics (character count, word count) and the input text "
    "for reference. This simple interface design minimizes user friction while providing comprehensive results.",
    first_line_indent=1.27
)

add_section_heading("4.5", "Database Schema")

add_justified_text(
    "The SQLite database (hate_speech.db) contains two tables: users for authentication and predictions for "
    "tracking classification history. The schema is designed for simplicity and efficiency, leveraging SQLite's "
    "serverless architecture to eliminate database server configuration requirements.",
    first_line_indent=1.27
)

add_centered_text("Table 4.1: Database Schema \u2013 Users Table", font_size=10, bold=True, space_after=4, keep_with_next=True)
users_table = doc.add_table(rows=7, cols=4)
users_table.style = 'Table Grid'
users_table.alignment = WD_TABLE_ALIGNMENT.CENTER
users_data = [
    ("Column", "Type", "Constraints", "Description"),
    ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique user identifier"),
    ("name", "TEXT", "NOT NULL", "Display name"),
    ("username", "TEXT", "UNIQUE NOT NULL", "Login username"),
    ("password", "TEXT", "NOT NULL", "Werkzeug hashed password"),
    ("is_admin", "INTEGER", "DEFAULT 0", "Admin flag (0=user, 1=admin)"),
    ("created_at", "TEXT", "DEFAULT CURRENT_TIMESTAMP", "Account creation timestamp"),
]
for i, row_data in enumerate(users_data):
    for j, val in enumerate(row_data):
        set_cell_text(users_table.cell(i, j), val, bold=(i == 0), font_size=10,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(users_table.cell(i, j))
    users_table.cell(i, 0).width = Inches(1.0)
    users_table.cell(i, 1).width = Inches(0.9)
    users_table.cell(i, 2).width = Inches(2.3)
    users_table.cell(i, 3).width = Inches(2.0)
keep_table_on_one_page(users_table)

add_centered_text("Table 4.2: Database Schema \u2013 Predictions Table", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
pred_table = doc.add_table(rows=9, cols=4)
pred_table.style = 'Table Grid'
pred_table.alignment = WD_TABLE_ALIGNMENT.CENTER
pred_data = [
    ("Column", "Type", "Constraints", "Description"),
    ("id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Unique prediction identifier"),
    ("user_id", "INTEGER", "FK \u2192 users.id", "Reference to user who made prediction"),
    ("input_text", "TEXT", "", "Original text submitted for analysis"),
    ("prediction", "TEXT", "", "Classification result (Hate Speech/Offensive/Clean)"),
    ("confidence", "REAL", "", "Model confidence score (0-100%)"),
    ("text_length", "INTEGER", "", "Character count of input text"),
    ("word_count", "INTEGER", "", "Word count of input text"),
    ("created_at", "TEXT", "DEFAULT CURRENT_TIMESTAMP", "Prediction timestamp"),
]
for i, row_data in enumerate(pred_data):
    for j, val in enumerate(row_data):
        set_cell_text(pred_table.cell(i, j), val, bold=(i == 0), font_size=10,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(pred_table.cell(i, j))
    pred_table.cell(i, 0).width = Inches(1.0)
    pred_table.cell(i, 1).width = Inches(0.9)
    pred_table.cell(i, 2).width = Inches(2.3)
    pred_table.cell(i, 3).width = Inches(2.0)
keep_table_on_one_page(pred_table)

add_centered_text("Table 4.3: Dataset Feature Descriptions", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
ds_table = doc.add_table(rows=7, cols=4)
ds_table.style = 'Table Grid'
ds_table.alignment = WD_TABLE_ALIGNMENT.CENTER
ds_data = [
    ("Feature", "Type", "Values / Range", "Description"),
    ("tweet", "Text", "Variable-length string", "Raw social media text content for analysis"),
    ("class", "Categorical", "0, 1, 2", "Label: 0=Hate Speech, 1=Offensive, 2=Clean"),
    ("TF-IDF Features", "Numeric", "0.0\u20131.0 (sparse)", "5000 TF-IDF features from unigrams and bigrams"),
    ("text_length", "Numeric", "1\u2013500+", "Character count of preprocessed text"),
    ("word_count", "Numeric", "1\u2013100+", "Word count of preprocessed text"),
    ("cleaned_text", "Text", "Variable-length string", "Text after NLP preprocessing pipeline"),
]
for i, row_data in enumerate(ds_data):
    for j, val in enumerate(row_data):
        set_cell_text(ds_table.cell(i, j), val, bold=(i == 0), font_size=8,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(ds_table.cell(i, j))
    ds_table.cell(i, 0).width = Inches(1.5)
    ds_table.cell(i, 1).width = Inches(0.9)
    ds_table.cell(i, 2).width = Inches(1.5)
    ds_table.cell(i, 3).width = Inches(2.3)
keep_table_on_one_page(ds_table)

add_justified_text(
    "Note: The target variable 'class' is a 3-class label (0=Hate Speech, 1=Offensive, 2=Clean) representing "
    "the content classification of social media text. The raw text is preprocessed through the NLP pipeline "
    "and transformed into a 5000-dimensional TF-IDF feature vector before being passed to the classification "
    "models. The dataset contains 15,000 labeled text samples.",
    font_size=11, space_before=4
)

# ============================================================
# CHAPTER 5 - IMPLEMENTATION
# ============================================================
p_ch5 = add_centered_text("CHAPTER 5", font_size=18, bold=True, space_before=24, space_after=3)
p_ch5.paragraph_format.keep_with_next = True
p_ch5.paragraph_format.page_break_before = True
p_ch5t = add_centered_text("IMPLEMENTATION", font_size=16, bold=True, space_after=10)
p_ch5t.paragraph_format.keep_with_next = True

add_section_heading("5.1", "Methodologies")

add_justified_text(
    "The project follows the Agile Software Development methodology with iterative sprints, each focused "
    "on delivering a working increment of the system. The development was organized into four sprints, "
    "each lasting approximately two weeks, with regular reviews and retrospectives to ensure alignment "
    "with project objectives.",
    first_line_indent=1.27
)

add_justified_text(
    "Sprint 1: Dataset Acquisition and NLP Preprocessing \u2014 This sprint focused on obtaining the labeled "
    "hate speech dataset (15,000 text samples, 3 classes), implementing the NLP preprocessing pipeline "
    "(lowercasing, URL/mention/hashtag removal, special character filtering, NLTK stopword removal), and "
    "building the TF-IDF feature extraction module (max_features=5000, ngram_range=(1,2), min_df=2). Initial "
    "exploratory data analysis was conducted to understand class distribution and text characteristics.",
    first_line_indent=1.27
)

add_justified_text(
    "Sprint 2: Machine Learning Models and Evaluation \u2014 This sprint implemented the six classification "
    "models (Logistic Regression, Naive Bayes, SVM, KNN, Gradient Boosting, Random Forest) using scikit-learn. "
    "The evaluation pipeline computes accuracy, precision, recall, and F1-score for each model on the test set "
    "using macro averaging for 3-class metrics. Model serialization using joblib was implemented to save the "
    "best model (Logistic Regression) and the TF-IDF vectorizer for runtime inference. The models_info.json "
    "file was created to store performance metrics for the dashboard.",
    first_line_indent=1.27
)

add_justified_text(
    "Sprint 3: Authentication and Database \u2014 This sprint created the SQLite database schema (users and "
    "predictions tables), implemented user registration with Werkzeug password hashing, login verification, "
    "session management, and the @login_required decorator for route protection. The prediction history "
    "storage and retrieval system was built, including text metadata (text_length, word_count) for analytics.",
    first_line_indent=1.27
)

add_justified_text(
    "Sprint 4: Web Application, Visualization, and Deployment \u2014 The final sprint created the Flask "
    "application with 10 routes, developed the 9 Jinja2 templates with Bootstrap 5 dark theme, implemented "
    "the Chart.js visualizations for the visualize and dashboard pages, generated 8 EDA charts using "
    "matplotlib/seaborn, and created the Dockerfile for containerized deployment on port 5007. Comprehensive "
    "testing was performed across all routes and features.",
    first_line_indent=1.27
)

add_figure(os.path.join(FIGURES_DIR, "fig_nlp_pipeline.png"),
           "Figure 5.1: Agile Development Model", width=Inches(5.0))

add_section_heading("5.2", "Implementation Details")

add_justified_text(
    "The NLP and machine learning pipeline is implemented in train_model.py, which is executed once to "
    "preprocess text data, build the TF-IDF vocabulary, train all six models, and serialize the best performer. "
    "The script loads hate_speech_data.csv into a pandas DataFrame, applies the preprocess_text() function to "
    "each text sample (lowercasing, regex-based URL/mention/hashtag/special character removal, NLTK stopword "
    "filtering), and builds the TF-IDF feature matrix using TfidfVectorizer(max_features=5000, "
    "ngram_range=(1,2), min_df=2). The preprocessed data is split with stratify=y to preserve 3-class distribution.",
    first_line_indent=1.27
)

add_justified_text(
    "Each model is trained with scikit-learn's fit() method: LogisticRegression(max_iter=1000, random_state=42), "
    "MultinomialNB(), CalibratedClassifierCV(LinearSVC(max_iter=10000, random_state=42)), "
    "RandomForestClassifier(n_estimators=100, random_state=42), GradientBoostingClassifier(n_estimators=100, "
    "random_state=42), and KNeighborsClassifier(n_neighbors=5). After training, accuracy, precision (macro), "
    "recall (macro), and F1-score (macro) are computed using sklearn.metrics functions. The best model "
    "(Logistic Regression with 94.83% accuracy) is serialized to hate_speech_model.pkl, and the TF-IDF "
    "vectorizer is saved to tfidf_vectorizer.pkl using joblib.",
    first_line_indent=1.27
)

add_justified_text(
    "At runtime, the Flask application (app.py) loads the pre-trained model and vectorizer at startup. When "
    "a user submits text for analysis, the /predict route handler applies the same preprocess_text() function "
    "used during training, transforms the cleaned text using vectorizer.transform(), passes the TF-IDF "
    "feature vector to model.predict_proba(), determines the predicted class using argmax, and stores the "
    "result in the predictions table with user_id, input_text, prediction label, confidence score, "
    "text_length, and word_count.",
    first_line_indent=1.27
)

add_section_heading("5.3", "Module Description")
add_bullet("Authentication Module: Handles user registration with Werkzeug generate_password_hash(), login verification with check_password_hash(), session management using Flask sessions, and route protection with @login_required decorator. Supports admin role with global statistics. Routes: /register, /login, /logout.")
add_bullet("NLP Preprocessing Module: Implements the preprocess_text() function that applies lowercasing, URL removal (regex: http\\S+|www\\.\\S+), @mention removal, #hashtag removal, special character filtering ([^a-zA-Z\\s]), whitespace normalization, and NLTK English stopword removal. The same function is used in both training and inference.")
add_bullet("Classification Module: Processes text input through the NLP pipeline, transforms cleaned text using the pre-trained TF-IDF vectorizer, invokes model.predict_proba() on the Logistic Regression model, maps the argmax class index to the label (Hate Speech/Offensive/Clean), and stores results in SQLite. Route: /predict.")
add_bullet("History Module: Queries the predictions table for the current user's past classifications, displays them in a Bootstrap table with input text, classification label, confidence, text length, word count, and date. Route: /history.")
add_bullet("Visualization Module: Displays 8 matplotlib/seaborn EDA charts generated during training, including class distribution, word clouds, text length distributions, and feature analyses. Route: /visualize.")
add_bullet("Dashboard Module: Loads model performance metrics from models_info.json and generates Chart.js bar charts comparing accuracy, precision, recall, and F1-score across all six models. Route: /dashboard.")
add_bullet("Home Module: Displays user statistics (total analyses, hate speech count, offensive count, clean count), recent predictions, and admin stats (total users, total predictions). Route: /home.")

add_section_heading("5.4", "Sample Code")

add_subsection_heading("5.4.1", "Text Preprocessing Pipeline")
add_justified_text(
    'import re\n'
    'from nltk.corpus import stopwords\n'
    'stop_words = set(stopwords.words("english"))\n'
    '\n'
    'def preprocess_text(text):\n'
    '    text = str(text).lower()\n'
    '    text = re.sub(r"http\\S+|www\\.\\S+", "", text)\n'
    '    text = re.sub(r"@\\w+", "", text)\n'
    '    text = re.sub(r"#\\w+", "", text)\n'
    '    text = re.sub(r"[^a-zA-Z\\s]", "", text)\n'
    '    text = re.sub(r"\\s+", " ", text).strip()\n'
    '    words = text.split()\n'
    '    words = [w for w in words if w not in stop_words]\n'
    '    return " ".join(words)',
    font_size=9
)

add_subsection_heading("5.4.2", "TF-IDF Vectorization & Model Training")
add_justified_text(
    'from sklearn.feature_extraction.text import TfidfVectorizer\n'
    'from sklearn.model_selection import train_test_split\n'
    'from sklearn.linear_model import LogisticRegression\n'
    '\n'
    '# Build TF-IDF features\n'
    'vectorizer = TfidfVectorizer(\n'
    '    max_features=5000,\n'
    '    ngram_range=(1, 2),\n'
    '    min_df=2\n'
    ')\n'
    'X = vectorizer.fit_transform(df["cleaned_text"])\n'
    'y = df["class"]\n'
    '\n'
    '# Stratified train-test split\n'
    'X_train, X_test, y_train, y_test = train_test_split(\n'
    '    X, y, test_size=0.2, stratify=y, random_state=42)\n'
    '\n'
    '# Train best model\n'
    'model = LogisticRegression(max_iter=1000, random_state=42)\n'
    'model.fit(X_train, y_train)',
    font_size=9
)

add_subsection_heading("5.4.3", "User Authentication Code")
add_justified_text(
    'from werkzeug.security import generate_password_hash\n'
    'from werkzeug.security import check_password_hash\n'
    '\n'
    '@app.route("/register", methods=["GET", "POST"])\n'
    'def register():\n'
    '    if request.method == "POST":\n'
    '        name = request.form["name"]\n'
    '        username = request.form["username"]\n'
    '        password = request.form["password"]\n'
    '        conn = get_db()\n'
    '        existing = conn.execute(\n'
    '            "SELECT id FROM users WHERE username = ?",\n'
    '            (username,)).fetchone()\n'
    '        if existing:\n'
    '            flash("Username already exists.", "danger")\n'
    '            return render_template("register.html")\n'
    '        conn.execute(\n'
    '            "INSERT INTO users (name, username, password)"\n'
    '            " VALUES (?, ?, ?)",\n'
    '            (name, username,\n'
    '             generate_password_hash(password)))\n'
    '        conn.commit()\n'
    '        flash("Registration successful!", "success")\n'
    '        return redirect(url_for("login"))\n'
    '    return render_template("register.html")',
    font_size=9
)

add_subsection_heading("5.4.4", "Prediction Route Handler")
add_justified_text(
    '@app.route("/predict", methods=["GET", "POST"])\n'
    '@login_required\n'
    'def predict():\n'
    '    result = None\n'
    '    if request.method == "POST":\n'
    '        input_text = request.form["text"]\n'
    '        cleaned = preprocess_text(input_text)\n'
    '        X = vectorizer.transform([cleaned])\n'
    '        proba = model.predict_proba(X)[0]\n'
    '        pred_label = int(np.argmax(proba))\n'
    '        confidence = round(float(proba[pred_label])*100, 2)\n'
    '        prediction = LABEL_MAP[pred_label]\n'
    '        text_length = len(input_text)\n'
    '        word_count = len(input_text.split())\n'
    '        conn = get_db()\n'
    '        conn.execute(\n'
    '            "INSERT INTO predictions "\n'
    '            "(user_id, input_text, prediction, confidence,"\n'
    '            " text_length, word_count) VALUES (?,?,?,?,?,?)",\n'
    '            (session["user_id"], input_text, prediction,\n'
    '             confidence, text_length, word_count))\n'
    '        conn.commit()\n'
    '    return render_template("predict.html", result=result)',
    font_size=9
)

add_subsection_heading("5.4.5", "Database Initialization")
add_justified_text(
    'import sqlite3\n'
    '\n'
    'def init_db():\n'
    '    conn = sqlite3.connect("hate_speech.db")\n'
    '    conn.execute("""\n'
    '        CREATE TABLE IF NOT EXISTS users (\n'
    '            id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
    '            name TEXT NOT NULL,\n'
    '            username TEXT UNIQUE NOT NULL,\n'
    '            password TEXT NOT NULL,\n'
    '            is_admin INTEGER DEFAULT 0,\n'
    '            created_at TEXT DEFAULT CURRENT_TIMESTAMP)\n'
    '    """)\n'
    '    conn.execute("""\n'
    '        CREATE TABLE IF NOT EXISTS predictions (\n'
    '            id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
    '            user_id INTEGER,\n'
    '            input_text TEXT,\n'
    '            prediction TEXT,\n'
    '            confidence REAL,\n'
    '            text_length INTEGER,\n'
    '            word_count INTEGER,\n'
    '            created_at TEXT DEFAULT CURRENT_TIMESTAMP,\n'
    '            FOREIGN KEY (user_id) REFERENCES users(id))\n'
    '    """)\n'
    '    conn.commit()\n'
    '    conn.close()',
    font_size=9
)

# ============================================================
# CHAPTER 6 - TESTING
# ============================================================
p_ch6 = add_centered_text("CHAPTER 6", font_size=18, bold=True, space_before=24, space_after=3)
p_ch6.paragraph_format.keep_with_next = True
p_ch6.paragraph_format.page_break_before = True
p_ch6t = add_centered_text("TESTING", font_size=16, bold=True, space_after=10)
p_ch6t.paragraph_format.keep_with_next = True

add_section_heading("6.1", "Types of Testing")

add_subsection_heading("6.1.1", "Unit Testing")
add_justified_text(
    "Unit testing verifies the correct behavior of individual components in isolation. For the hate speech "
    "analysis system, unit tests cover the NLP preprocessing functions (verifying URL removal, mention removal, "
    "hashtag removal, special character filtering, stopword removal produce expected outputs), the TF-IDF "
    "vectorization (verifying consistent feature dimensions), the model prediction pipeline (verifying that "
    "the model produces valid 3-class predictions with probabilities), the authentication functions (verifying "
    "password hashing and verification), and the database operations (verifying insert and query operations "
    "on users and predictions tables).",
    first_line_indent=1.27
)

add_subsection_heading("6.1.2", "Integration Testing")
add_justified_text(
    "Integration testing validates the interaction between connected components. Key integration tests include "
    "the end-to-end classification pipeline (text submission \u2192 NLP preprocessing \u2192 TF-IDF vectorization "
    "\u2192 model inference \u2192 database storage \u2192 result rendering), the authentication flow "
    "(registration \u2192 login \u2192 session creation \u2192 protected route access \u2192 logout), and the "
    "history retrieval pipeline (prediction storage \u2192 history query \u2192 table rendering). These tests "
    "ensure that data flows correctly between Flask routes, the NLP/ML pipeline, SQLite database, and the "
    "template layer.",
    first_line_indent=1.27
)

add_subsection_heading("6.1.3", "Functional Testing")
add_justified_text(
    "Functional testing evaluates the system against its specified requirements. This includes testing user "
    "registration with valid and invalid inputs, login with correct and incorrect credentials, text "
    "classification with various input types (hate speech, offensive, clean text), history page displaying "
    "past predictions, visualization page rendering EDA charts, dashboard page showing model comparison "
    "metrics, and error handling for duplicate usernames, empty text submissions, and unauthorized access. "
    "Each functional test verifies that the user-facing behavior matches the specification.",
    first_line_indent=1.27
)

add_section_heading("6.2", "Test Cases")

add_centered_text("Table 6.1: Test Cases \u2013 Authentication", font_size=10, bold=True, space_after=4, keep_with_next=True)
tc1 = doc.add_table(rows=6, cols=4)
tc1.style = 'Table Grid'
tc1.alignment = WD_TABLE_ALIGNMENT.CENTER
tc1_data = [
    ("Test ID", "Scenario", "Expected Result", "Status"),
    ("TC-A01", "Register with valid name, username, password", "Account created; redirect to login page", "Pass"),
    ("TC-A02", "Register with duplicate username (admin)", "Error: Username already exists", "Pass"),
    ("TC-A03", "Login with correct credentials (admin/admin123)", "Session created; redirect to home page", "Pass"),
    ("TC-A04", "Login with incorrect password", "Error: Invalid username or password", "Pass"),
    ("TC-A05", "Access protected route (/predict) without login", "Redirect to login page with warning", "Pass"),
]
for i, row_data in enumerate(tc1_data):
    for j, val in enumerate(row_data):
        set_cell_text(tc1.cell(i, j), val, bold=(i == 0), font_size=9,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(tc1.cell(i, j))
    tc1.cell(i, 0).width = Inches(0.7)
    tc1.cell(i, 1).width = Inches(2.0)
    tc1.cell(i, 2).width = Inches(2.5)
    tc1.cell(i, 3).width = Inches(0.6)
keep_table_on_one_page(tc1)

add_centered_text("Table 6.2: Test Cases \u2013 Text Classification", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
tc2 = doc.add_table(rows=6, cols=4)
tc2.style = 'Table Grid'
tc2.alignment = WD_TABLE_ALIGNMENT.CENTER
tc2_data = [
    ("Test ID", "Scenario", "Expected Result", "Status"),
    ("TC-P01", "Submit clearly hateful text with slurs", "Hate Speech prediction with high confidence (>80%)", "Pass"),
    ("TC-P02", "Submit mildly offensive/rude text", "Offensive prediction with moderate confidence", "Pass"),
    ("TC-P03", "Submit normal, clean conversational text", "Clean prediction with high confidence (>80%)", "Pass"),
    ("TC-P04", "View prediction history after multiple analyses", "All past predictions listed with correct details", "Pass"),
    ("TC-P05", "Verify prediction stored in SQLite database", "predictions table contains correct user_id, text, result", "Pass"),
]
for i, row_data in enumerate(tc2_data):
    for j, val in enumerate(row_data):
        set_cell_text(tc2.cell(i, j), val, bold=(i == 0), font_size=9,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(tc2.cell(i, j))
    tc2.cell(i, 0).width = Inches(0.7)
    tc2.cell(i, 1).width = Inches(2.0)
    tc2.cell(i, 2).width = Inches(2.5)
    tc2.cell(i, 3).width = Inches(0.6)
keep_table_on_one_page(tc2)

add_centered_text("Table 6.3: Test Cases \u2013 Visualization & Dashboard", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
tc3 = doc.add_table(rows=5, cols=4)
tc3.style = 'Table Grid'
tc3.alignment = WD_TABLE_ALIGNMENT.CENTER
tc3_data = [
    ("Test ID", "Scenario", "Expected Result", "Status"),
    ("TC-V01", "Render EDA visualization page", "8 matplotlib/seaborn charts displayed correctly", "Pass"),
    ("TC-V02", "Render model dashboard", "Bar charts showing accuracy, precision, recall, F1 for all 6 models", "Pass"),
    ("TC-V03", "Dashboard loads model metrics from JSON", "All 6 model metrics loaded and displayed correctly", "Pass"),
    ("TC-V04", "Render about page with model info", "Technology stack and model performance displayed", "Pass"),
]
for i, row_data in enumerate(tc3_data):
    for j, val in enumerate(row_data):
        set_cell_text(tc3.cell(i, j), val, bold=(i == 0), font_size=9,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(tc3.cell(i, j))
    tc3.cell(i, 0).width = Inches(0.7)
    tc3.cell(i, 1).width = Inches(2.0)
    tc3.cell(i, 2).width = Inches(2.5)
    tc3.cell(i, 3).width = Inches(0.6)
keep_table_on_one_page(tc3)

add_centered_text("Table 6.4: Test Cases \u2013 NLP & Security", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
tc4 = doc.add_table(rows=6, cols=4)
tc4.style = 'Table Grid'
tc4.alignment = WD_TABLE_ALIGNMENT.CENTER
tc4_data = [
    ("Test ID", "Scenario", "Expected Result", "Status"),
    ("TC-S01", "Verify passwords stored as hashes", "No plain-text passwords in users table", "Pass"),
    ("TC-S02", "Verify session cleared on logout", "Protected routes inaccessible after logout", "Pass"),
    ("TC-S03", "NLP removes URLs from input text", "HTTP/HTTPS URLs stripped before vectorization", "Pass"),
    ("TC-S04", "NLP removes @mentions and #hashtags", "Social media handles and tags removed", "Pass"),
    ("TC-S05", "NLTK stopwords filtered from text", "Common words (the, is, at) removed from feature input", "Pass"),
]
for i, row_data in enumerate(tc4_data):
    for j, val in enumerate(row_data):
        set_cell_text(tc4.cell(i, j), val, bold=(i == 0), font_size=9,
                      align=WD_ALIGN_PARAGRAPH.CENTER if j in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT)
    if i == 0:
        for j in range(4):
            shade_cell(tc4.cell(i, j))
    tc4.cell(i, 0).width = Inches(0.7)
    tc4.cell(i, 1).width = Inches(2.0)
    tc4.cell(i, 2).width = Inches(2.5)
    tc4.cell(i, 3).width = Inches(0.6)
keep_table_on_one_page(tc4)

# ============================================================
# CHAPTER 7 - RESULTS AND DISCUSSION
# ============================================================
p_ch7 = add_centered_text("CHAPTER 7", font_size=18, bold=True, space_before=24, space_after=3)
p_ch7.paragraph_format.keep_with_next = True
p_ch7.paragraph_format.page_break_before = True
p_ch7t = add_centered_text("RESULTS AND DISCUSSION", font_size=16, bold=True, space_after=10)
p_ch7t.paragraph_format.keep_with_next = True

add_justified_text(
    "This chapter presents the results of the social media hate speech analysis system through application "
    "screenshots demonstrating the user interface and functionality, followed by machine learning model "
    "performance figures. The system was tested with the labeled hate speech dataset (15,000 text samples, "
    "3 classes) to validate the classification accuracy, model comparison, and visualization quality.",
    first_line_indent=1.27
)

# --- Application Screenshots ---
add_section_heading("7.1", "Login Page")
add_justified_text(
    "The login page presents a Bootstrap 5 dark-themed interface with a centered card containing username "
    "and password input fields. The page includes a link to the registration page for new users. Error "
    "messages are displayed using Flask flash messages when invalid credentials are entered. The dark theme "
    "provides a professional, modern appearance consistent across all application pages.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "login.png"),
           "Figure 7.1: Login Page", width=Inches(5.5))

add_section_heading("7.2", "Registration Page")
add_justified_text(
    "The registration page allows new users to create an account by providing a display name, username, and "
    "password. The form validates input and checks for duplicate usernames before creating the account "
    "with a Werkzeug-hashed password stored in the SQLite users table. Upon successful registration, the "
    "user is redirected to the login page with a success flash message.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "register.png"),
           "Figure 7.2: Registration Page", width=Inches(5.5))

add_section_heading("7.3", "Invalid Login Attempt")
add_justified_text(
    "When a user enters incorrect credentials, the system displays an error message indicating invalid "
    "username or password. The password verification uses Werkzeug's check_password_hash() function, "
    "which compares the entered password against the stored PBKDF2-SHA256 hash. The error message is "
    "generic (not revealing whether the username or password is wrong) to prevent enumeration attacks.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "invalid_login.png"),
           "Figure 7.3: Invalid Login Attempt", width=Inches(5.5))

add_section_heading("7.4", "Duplicate Registration Attempt")
add_justified_text(
    "When a user attempts to register with a username that already exists in the database, the system "
    "checks the users table for the duplicate username and displays an appropriate error message. This "
    "prevents duplicate accounts and maintains data integrity in the users table.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "duplicate_register.png"),
           "Figure 7.4: Duplicate Registration Attempt", width=Inches(5.5))

add_section_heading("7.5", "Home Page Dashboard")
add_justified_text(
    "After successful login, the user is directed to the home page displaying analysis statistics (total "
    "analyses, hate speech detections, offensive detections, clean text count), recent prediction cards, "
    "and quick action navigation links. Admin users see additional global statistics including total "
    "registered users, total predictions across all users, and total hate speech detections system-wide.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "home.png"),
           "Figure 7.5: Home Page Dashboard", width=Inches(5.5))

add_section_heading("7.6", "Text Analysis Form")
add_justified_text(
    "The prediction page features a simple textarea input where users can paste or type social media text "
    "for hate speech analysis. The minimalist design with a single input field reduces user friction and "
    "focuses attention on the core classification task. A submit button triggers the NLP preprocessing "
    "and model inference pipeline.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "predict_form.png"),
           "Figure 7.6: Text Analysis Form (Empty)", width=Inches(5.5))

add_section_heading("7.7", "Hate Speech Detection Result")
add_justified_text(
    "When the model classifies text as hate speech, the result is displayed with a red badge indicating "
    "'Hate Speech' along with the confidence percentage. The result card shows the original input text, "
    "text statistics (character count, word count), and the prediction class. The red color coding "
    "provides immediate visual feedback for content moderators reviewing flagged content.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "predict_hate.png"),
           "Figure 7.7: Hate Speech Detection Result", width=Inches(5.5))

add_section_heading("7.8", "Clean Text Classification Result")
add_justified_text(
    "When the model classifies text as clean, the result is displayed with a green badge indicating "
    "'Clean' along with the confidence percentage. This demonstrates the model's ability to correctly "
    "identify non-harmful content, reducing false positives in content moderation scenarios. The green "
    "color provides positive visual feedback confirming the text is appropriate.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "predict_clean.png"),
           "Figure 7.8: Clean Text Classification Result", width=Inches(5.5))

add_section_heading("7.9", "Offensive Text Classification Result")
add_justified_text(
    "When the model classifies text as offensive (but not hate speech), the result is displayed with an "
    "orange badge indicating 'Offensive' along with the confidence percentage. This intermediate category "
    "distinguishes between hate speech (targeting protected groups) and general offensive language, "
    "enabling nuanced content moderation policies.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "predict_offensive.png"),
           "Figure 7.9: Offensive Text Classification Result", width=Inches(5.5))

add_section_heading("7.10", "Prediction History")
add_justified_text(
    "The history page displays a Bootstrap table listing all past text classifications made by the current "
    "user. Each row shows the input text (truncated for display), the classification label with a color-coded "
    "badge, confidence percentage, text length, word count, and the date and time of the analysis. The "
    "table is sorted by date in descending order (newest first). This feature enables users to track "
    "classification patterns and review past content moderation decisions.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "history.png"),
           "Figure 7.10: Prediction History", width=Inches(5.5))

add_section_heading("7.11", "EDA Visualization Gallery")
add_justified_text(
    "The visualization page presents a gallery of matplotlib/seaborn charts providing exploratory data "
    "analysis of the hate speech dataset. Charts include class distribution bar charts, text length "
    "distributions by class, word frequency analyses, and other statistical visualizations that reveal "
    "patterns in the dataset. These visualizations help users understand the characteristics of hate "
    "speech, offensive, and clean text.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "visualize.png"),
           "Figure 7.11: EDA Visualization Gallery", width=Inches(5.5))

add_section_heading("7.12", "Model Dashboard")
add_justified_text(
    "The dashboard page displays comprehensive model analytics comparing all six classification models. "
    "The main section shows a performance comparison table and Chart.js bar charts with accuracy, "
    "precision, recall, and F1-score for Logistic Regression, Naive Bayes, SVM, KNN, Gradient Boosting, "
    "and Random Forest. The best model (Logistic Regression with 94.83% accuracy) is highlighted.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "dashboard.png"),
           "Figure 7.12: Model Dashboard", width=Inches(5.5))

add_section_heading("7.13", "Dashboard Charts (Detailed)")
add_justified_text(
    "The detailed dashboard view shows additional Chart.js visualizations including model comparison "
    "radar charts, prediction distribution pie charts, and confidence distribution histograms. These "
    "charts provide deeper insights into model behavior beyond simple accuracy metrics, helping users "
    "understand where each model excels and where it struggles across the three classes.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "dashboard_charts.png"),
           "Figure 7.13: Dashboard Charts (Detailed)", width=Inches(5.5))

add_section_heading("7.14", "About Page")
add_justified_text(
    "The about page provides project information including the project title, description, technology stack "
    "(Python, Flask, scikit-learn, NLTK, SQLite, Bootstrap 5, Chart.js, Docker), dataset details, model "
    "performance overview, and team information. The page uses Bootstrap cards to organize information "
    "sections and provides a comprehensive project summary.",
    first_line_indent=1.27
)
add_figure(os.path.join(SCREENSHOTS_DIR, "about.png"),
           "Figure 7.14: About Page", width=Inches(5.5))

# --- Model Performance Figures ---
add_section_heading("7.15", "Model Accuracy Comparison")
add_justified_text(
    "The model accuracy comparison figure provides a detailed view of each model's classification accuracy. "
    "Logistic Regression (94.83%) leads alongside Naive Bayes (94.83%) and SVM (94.83%), followed by KNN "
    "(94.73%), Gradient Boosting (94.50%), and Random Forest (94.17%). The close accuracy scores across all "
    "six models indicate that the TF-IDF feature representation effectively captures the linguistic patterns "
    "that distinguish hate speech from offensive and clean content.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_model_comparison.png"),
           "Figure 7.15: Model Accuracy Comparison", width=Inches(5.5))

add_section_heading("7.16", "Confusion Matrix")
add_justified_text(
    "The confusion matrix for the Logistic Regression model shows the breakdown of predictions across all "
    "three classes. The matrix reveals the model's ability to distinguish between hate speech, offensive "
    "language, and clean text. The diagonal values represent correct classifications, while off-diagonal "
    "values indicate misclassifications. The model shows strong performance in identifying clean text "
    "and hate speech, with some confusion between hate speech and offensive language due to their "
    "overlapping linguistic characteristics.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_confusion_matrix.png"),
           "Figure 7.16: Confusion Matrix (Logistic Regression)", width=Inches(5.5))

add_section_heading("7.17", "Class Distribution")
add_justified_text(
    "The class distribution chart shows the proportions of the three content categories in the dataset. "
    "The distribution reveals the balance between hate speech, offensive language, and clean text samples, "
    "which directly affects model training and evaluation. Understanding this distribution is crucial for "
    "interpreting model performance metrics, as class imbalance can lead to biased predictions favoring "
    "the majority class.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_class_distribution.png"),
           "Figure 7.17: Class Distribution", width=Inches(5.5))

add_section_heading("7.18", "System Architecture")
add_justified_text(
    "The system architecture figure provides a high-level view of the component interactions. The user "
    "layer (web browser) communicates with the Flask application layer through HTTP requests. The Flask "
    "layer coordinates four major subsystems: the authentication module (Werkzeug + SQLite), the NLP "
    "preprocessing and classification pipeline (NLTK + TF-IDF + Logistic Regression), the Chart.js and "
    "matplotlib visualization engines, and the SQLite database for persistent storage. Session management "
    "connects the authentication and classification subsystems.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_system_architecture.png"),
           "Figure 7.18: System Architecture", width=Inches(5.5))

add_section_heading("7.19", "NLP Pipeline")
add_justified_text(
    "The NLP pipeline figure illustrates the text processing stages from raw social media input to "
    "classification output. Raw text enters the pipeline and passes through lowercasing, URL removal, "
    "@mention removal, #hashtag removal, special character filtering, whitespace normalization, and "
    "NLTK stopword removal. The cleaned text is then transformed into a 5000-dimensional TF-IDF feature "
    "vector using unigrams and bigrams. The feature vector is passed to the pre-trained Logistic Regression "
    "model, which outputs class probabilities for hate speech, offensive, and clean categories.",
    first_line_indent=1.27
)
add_figure(os.path.join(FIGURES_DIR, "fig_nlp_pipeline.png"),
           "Figure 7.19: NLP Pipeline", width=Inches(5.5))

# Model Performance Table
add_centered_text("Table 7.1: Model Performance Comparison", font_size=10, bold=True, space_before=8, space_after=4, keep_with_next=True)
perf_table = doc.add_table(rows=7, cols=5)
perf_table.style = 'Table Grid'
perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
perf_data = [
    ("Model", "Accuracy", "Precision", "Recall", "F1-Score"),
    ("Logistic Regression (BEST)", "94.83%", "94.90%", "94.83%", "94.83%"),
    ("Naive Bayes", "94.83%", "94.88%", "94.83%", "94.82%"),
    ("SVM (Linear)", "94.83%", "94.90%", "94.83%", "94.83%"),
    ("KNN (k=5)", "94.73%", "94.85%", "94.73%", "94.73%"),
    ("Gradient Boosting", "94.50%", "94.57%", "94.50%", "94.49%"),
    ("Random Forest (n=100)", "94.17%", "94.27%", "94.17%", "94.15%"),
]
for i, row_data in enumerate(perf_data):
    for j, val in enumerate(row_data):
        set_cell_text(perf_table.cell(i, j), val, bold=(i == 0), font_size=10,
                      align=WD_ALIGN_PARAGRAPH.CENTER)
    if i == 0:
        for j in range(5):
            shade_cell(perf_table.cell(i, j))
    perf_table.cell(i, 0).width = Inches(2.0)
    perf_table.cell(i, 1).width = Inches(0.9)
    perf_table.cell(i, 2).width = Inches(0.9)
    perf_table.cell(i, 3).width = Inches(0.9)
    perf_table.cell(i, 4).width = Inches(0.9)
keep_table_on_one_page(perf_table)

# ============================================================
# CHAPTER 8 - CONCLUSION AND FUTURE SCOPE
# ============================================================
p_ch8 = add_centered_text("CHAPTER 8", font_size=18, bold=True, space_before=24, space_after=3)
p_ch8.paragraph_format.keep_with_next = True
p_ch8.paragraph_format.page_break_before = True
p_ch8t = add_centered_text("CONCLUSION AND FUTURE SCOPE", font_size=16, bold=True, space_after=10)
p_ch8t.paragraph_format.keep_with_next = True

add_section_heading("8.1", "Conclusion")

add_justified_text(
    "This project successfully demonstrates the application of Natural Language Processing and machine "
    "learning classification techniques for automated detection and classification of hate speech and "
    "cyberbullying content on social media platforms. The web-based platform implements six classification "
    "models \u2014 Logistic Regression, Naive Bayes, SVM, KNN, Gradient Boosting, and Random Forest \u2014 "
    "providing comprehensive performance comparison and secure text analysis capabilities with user "
    "authentication and history tracking.",
    first_line_indent=1.27
)

add_justified_text(
    "The comprehensive comparison of six classification algorithms demonstrates strong and consistent "
    "performance across all models. Logistic Regression achieved the best overall performance with 94.83% "
    "accuracy, matching Naive Bayes and SVM. KNN followed closely at 94.73%, Gradient Boosting at 94.50%, "
    "and Random Forest at 94.17%. The TF-IDF feature extraction with 5000 features using unigrams and "
    "bigrams, combined with thorough NLP preprocessing (URL removal, mention/hashtag filtering, stopword "
    "removal), proves to be highly effective for text classification tasks.",
    first_line_indent=1.27
)

add_justified_text(
    "The Flask-based web application provides a practical, accessible interface that enables content "
    "moderators and researchers to perform hate speech analysis without programming knowledge. "
    "The following key achievements were realized:",
    first_line_indent=1.27
)

add_bullet("Implemented six classification models achieving accuracy scores ranging from 94.17% (Random Forest) to 94.83% (Logistic Regression) on the hate speech dataset.")
add_bullet("Developed a comprehensive NLP preprocessing pipeline handling lowercasing, URL removal, @mention removal, #hashtag removal, special character filtering, and NLTK stopword removal.")
add_bullet("Built TF-IDF feature extraction with 5000 features using unigrams and bigrams (ngram_range=(1,2), min_df=2) for effective text representation.")
add_bullet("Built secure user authentication system with Werkzeug password hashing, admin role support, and SQLite database storage.")
add_bullet("Created prediction history tracking with text metadata (character count, word count) enabling content moderation audit trails.")
add_bullet("Implemented 8 EDA visualizations and interactive Chart.js dashboards for model comparison and dataset analysis.")
add_bullet("Designed a 3-class classification system distinguishing Hate Speech, Offensive language, and Clean text for nuanced content moderation.")
add_bullet("Containerized the application with Docker for reproducible deployment on port 5007.")

add_justified_text(
    "The NLP preprocessing pipeline proved critical for achieving high classification accuracy. By removing "
    "social media noise (URLs, mentions, hashtags) and filtering stopwords, the TF-IDF vectorizer captures "
    "meaningful linguistic features that distinguish between content categories. The project demonstrates "
    "that automated hate speech detection can effectively support human content moderators, reducing the "
    "volume of content requiring manual review while maintaining high accuracy.",
    first_line_indent=1.27
)

add_section_heading("8.2", "Future Scope")

add_justified_text(
    "The hate speech analysis system can be extended in several directions to enhance its "
    "analytical capabilities and practical utility:",
    first_line_indent=1.27
)
add_bullet("Deep Learning Models: Integrate transformer-based models (BERT, RoBERTa, DistilBERT) that capture contextual word relationships and achieve state-of-the-art performance on NLP classification tasks.")
add_bullet("Multi-language Support: Extend the system to detect hate speech in multiple languages (Hindi, Arabic, Spanish, French) using multilingual NLP models and language-specific preprocessing.")
add_bullet("Real-time Social Media Monitoring: Connect to Twitter/X, Reddit, and Facebook APIs for real-time content streaming and automated flagging of hateful content as it is posted.")
add_bullet("Context-Aware Classification: Incorporate conversation context (thread history, user profile, post metadata) to improve classification accuracy for ambiguous or sarcastic content.")
add_bullet("Severity Scoring: Develop a continuous severity score (1-10) instead of discrete categories, enabling prioritized content moderation queues based on harm potential.")
add_bullet("Explainability: Integrate LIME or SHAP for model-agnostic feature importance, highlighting which words or phrases triggered the classification for regulatory transparency.")
add_bullet("Cloud Deployment: Deploy on cloud platforms (AWS, Azure, GCP) with auto-scaling and managed databases for enterprise-level concurrent user support and global content moderation.")
add_bullet("REST API: Develop RESTful API endpoints for integration with existing social media platforms, content management systems, and third-party moderation tools.")
add_bullet("User Feedback Loop: Implement a feedback mechanism where moderators can correct misclassifications, enabling continuous model improvement through active learning.")
add_bullet("Multimedia Analysis: Extend detection to images (memes), videos, and audio content using multimodal deep learning approaches for comprehensive content moderation.")

# ============================================================
# CHAPTER 9 - SUSTAINABLE DEVELOPMENT GOALS
# ============================================================
p_ch9 = add_centered_text("CHAPTER 9", font_size=18, bold=True, space_before=24, space_after=3)
p_ch9.paragraph_format.keep_with_next = True
p_ch9.paragraph_format.page_break_before = True
p_ch9t = add_centered_text("SUSTAINABLE DEVELOPMENT GOALS", font_size=16, bold=True, space_after=10)
p_ch9t.paragraph_format.keep_with_next = True

add_section_heading("9.1", "SDG 16: Peace, Justice and Strong Institutions")

add_justified_text(
    "The hate speech analysis system directly contributes to SDG 16 (Peace, Justice and Strong Institutions) "
    "by providing automated tools for detecting and classifying harmful online content. Hate speech and "
    "cyberbullying undermine peaceful coexistence, erode social cohesion, and can escalate to real-world "
    "violence. By enabling rapid, accurate identification of hate speech on social media platforms, the "
    "system supports content moderation efforts that promote peaceful online discourse and protect "
    "vulnerable communities from targeted harassment.",
    first_line_indent=1.27
)
add_justified_text(
    "The system's 3-class classification (Hate Speech, Offensive, Clean) enables nuanced enforcement of "
    "community guidelines, distinguishing between content that targets protected groups (hate speech) and "
    "general rudeness (offensive language). This granularity supports proportionate moderation responses, "
    "balancing free expression with protection from harm. The prediction history and audit trail features "
    "promote accountability and transparency in content moderation decisions, contributing to building "
    "trust in digital institutions.",
    first_line_indent=1.27
)

add_section_heading("9.2", "SDG 4: Quality Education")

add_justified_text(
    "The project contributes to SDG 4 (Quality Education) by demonstrating practical applications of "
    "Natural Language Processing and machine learning in addressing real-world social challenges. The "
    "system serves as an educational tool for students learning NLP techniques (text preprocessing, "
    "TF-IDF vectorization, stopword removal), machine learning classification (6 different algorithms), "
    "and full-stack web development (Flask, SQLite, Bootstrap 5, Docker).",
    first_line_indent=1.27
)
add_justified_text(
    "The open-source technology stack and comprehensive documentation enable students and educators to "
    "study, reproduce, and extend the system for academic purposes. The project bridges the gap between "
    "theoretical NLP concepts taught in classrooms and practical implementation skills required in "
    "industry, promoting quality technical education that addresses societal needs.",
    first_line_indent=1.27
)

add_section_heading("9.3", "SDG 10: Reduced Inequalities")

add_justified_text(
    "The hate speech analysis system contributes to SDG 10 (Reduced Inequalities) by providing tools to "
    "identify and address online content that targets individuals based on race, ethnicity, religion, "
    "gender, sexual orientation, or other protected characteristics. Hate speech disproportionately "
    "affects marginalized communities, creating hostile online environments that limit digital participation "
    "and reinforce existing inequalities.",
    first_line_indent=1.27
)
add_justified_text(
    "By automating the detection of hate speech, the system helps social media platforms enforce "
    "anti-discrimination policies at scale, creating more inclusive online spaces for all users. The "
    "NLP preprocessing pipeline's ability to identify harmful language patterns, combined with the "
    "classification model's high accuracy, enables proactive identification of discriminatory content "
    "before it reaches a wide audience, reducing the psychological impact on targeted communities.",
    first_line_indent=1.27
)

add_section_heading("9.4", "Broader Impact")

add_bullet("Mental Health Impact: Automated hate speech detection can reduce exposure to harmful content, protecting users' mental health and well-being, particularly for young people and vulnerable populations who are most affected by cyberbullying.")
add_bullet("Platform Safety: By providing accurate content classification tools, the system enables social media platforms to create safer online environments, increasing user trust and engagement while reducing harmful interactions.")
add_bullet("Research Impact: The labeled dataset, trained models, and evaluation metrics contribute to the growing body of NLP research on hate speech detection, enabling other researchers to benchmark and improve upon the approaches used.")
add_bullet("Policy Impact: The system's classification capabilities can support policymakers and regulators in understanding the prevalence and nature of online hate speech, informing evidence-based digital safety legislation.")

add_section_heading("9.5", "Future Contribution to SDGs")

add_bullet("SDG 3 (Good Health and Well-Being): Extending the system to detect cyberbullying patterns and provide early intervention recommendations could support mental health initiatives and suicide prevention programs.")
add_bullet("SDG 5 (Gender Equality): Training specialized models to detect gender-based hate speech and online harassment could support gender equality initiatives and protect women and girls in digital spaces.")
add_bullet("SDG 17 (Partnerships): Collaborating with social media companies, civil society organizations, and academic institutions for model validation and deployment would create cross-sector partnerships for safer online environments.")

# ============================================================
# REFERENCES
# ============================================================
p_ref = add_centered_text("REFERENCES", font_size=18, bold=True, space_before=24, space_after=12)
p_ref.paragraph_format.page_break_before = True

references = [
    '[1] Davidson, T., Warmsley, D., Macy, M., & Weber, I. (2017). "Automated Hate Speech Detection and the Problem of Offensive Language." ICWSM 2017.',
    '[2] Waseem, Z., & Hovy, D. (2016). "Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter." NAACL Student Research Workshop.',
    '[3] Nobata, C., Tetreault, J., Thomas, A., Mehdad, Y., & Chang, Y. (2016). "Abusive Language Detection in Online User Content." WWW 2016.',
    '[4] Badjatiya, P., Gupta, S., Gupta, M., & Varma, V. (2017). "Deep Learning for Hate Speech Detection in Tweets." WWW 2017.',
    '[5] Zhang, Z., Robinson, D., & Tepper, J. (2018). "Detecting Hate Speech on Twitter Using a Convolution-GRU Based Deep Neural Network." ESWC 2018.',
    '[6] Pedregosa, F., et al. (2011). "Scikit-learn: Machine Learning in Python." Journal of Machine Learning Research, 12, 2825-2830.',
    '[7] Bird, S., Klein, E., & Loper, E. (2009). "Natural Language Processing with Python." O\'Reilly Media.',
    '[8] Manning, C. D., Raghavan, P., & Sch\u00fctze, H. (2008). "Introduction to Information Retrieval." Cambridge University Press.',
    '[9] Joachims, T. (1998). "Text Categorization with Support Vector Machines: Learning with Many Relevant Features." ECML 1998.',
    '[10] Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). "Applied Logistic Regression." Wiley, 3rd Edition.',
    '[11] Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.',
    '[12] Friedman, J. H. (2001). "Greedy Function Approximation: A Gradient Boosting Machine." Annals of Statistics, 29(5), 1189-1232.',
    '[13] Cover, T. M., & Hart, P. E. (1967). "Nearest Neighbor Pattern Classification." IEEE Transactions on Information Theory, 13(1), 21-27.',
    '[14] McCallum, A., & Nigam, K. (1998). "A Comparison of Event Models for Naive Bayes Text Classification." AAAI Workshop on Learning for Text Categorization.',
    '[15] Salton, G., & Buckley, C. (1988). "Term-Weighting Approaches in Automatic Text Retrieval." Information Processing & Management, 24(5), 513-523.',
    '[16] Powers, D. M. W. (2011). "Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness and Correlation." Journal of Machine Learning Technologies, 2(1), 37-63.',
    '[17] Fortuna, P., & Nunes, S. (2018). "A Survey on Automatic Detection of Hate Speech in Text." ACM Computing Surveys, 51(4), 1-30.',
    '[18] Schmidt, A., & Wiegand, M. (2017). "A Survey on Hate Speech Detection Using Natural Language Processing." SocialNLP Workshop.',
    '[19] Grinberg, M. (2018). "Flask Web Development: Developing Web Applications with Python." O\'Reilly Media.',
    '[20] OWASP Foundation (2021). "OWASP Application Security Verification Standard 4.0." owasp.org.',
    '[21] Bootstrap Contributors (2021). "Bootstrap 5 Documentation." getbootstrap.com.',
    '[22] Chart.js Contributors (2023). "Chart.js \u2014 Simple yet Flexible JavaScript Charting." chartjs.org.',
    '[23] Owens, M. (2006). "The Definitive Guide to SQLite." Apress.',
    '[24] Merkel, D. (2014). "Docker: Lightweight Linux Containers for Consistent Development and Deployment." Linux Journal, 239.',
    '[25] Werkzeug Contributors (2024). "Werkzeug \u2014 The Comprehensive WSGI Web Application Library." werkzeug.palletsprojects.com.',
    '[26] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." NAACL 2019.',
    '[27] McKinney, W. (2010). "Data Structures for Statistical Computing in Python." Proceedings of the 9th Python in Science Conference, 51-56.',
    '[28] Raschka, S., & Mirjalili, V. (2019). "Python Machine Learning." Packt Publishing.',
    '[29] Kaggle (2024). "Hate Speech and Offensive Language Dataset." kaggle.com/datasets.',
    '[30] Flask Documentation (2024). "Flask \u2014 Web Development, One Drop at a Time." flask.palletsprojects.com.',
]

for ref in references:
    add_justified_text(ref, font_size=11, space_after=4)

# ============================================================
# SAVE DOCUMENT
# ============================================================
doc.save(OUTPUT_PATH)
file_size = os.path.getsize(OUTPUT_PATH) // 1024
print(f"Report saved to: {OUTPUT_PATH}")
print(f"File size: {file_size} KB")
