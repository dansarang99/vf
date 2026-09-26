# -*- coding: utf-8 -*-
"""
[Templates] Master Slide Archetypes Library
Contains reusable layout renderers for:
1. Cover Slide
2. Executive Summary Slide
3. Table of Contents Slide
4. Chapter Divider Slide
5. 3-Column Strategy Slide
6. 2-Column Deep Dive / Flow Slide
7. Empirical EDA Chart Slide
"""
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

C_BG            = RGBColor(228, 248, 236)
C_CARD          = RGBColor(255, 255, 255)
C_CARD_SUB      = RGBColor(241, 249, 244)
C_CARD_BORDER   = RGBColor(209, 231, 221)
C_BLUE_ACCENT   = RGBColor(7, 133, 192)
C_GREEN_ACCENT  = RGBColor(13, 124, 91)
C_AMBER_ACCENT  = RGBColor(217, 119, 6)
C_TEXT_TITLE    = RGBColor(15, 23, 42)
C_TEXT_BOLD     = RGBColor(30, 41, 59)
C_TEXT_BODY     = RGBColor(51, 65, 85)
C_TEXT_MUTED    = RGBColor(100, 116, 139)
C_PILL_BG       = RGBColor(224, 242, 254)

FONT_HEADING = "Malgun Gothic"
FONT_BODY    = "Malgun Gothic"

def add_full_bleed_bg(slide, prs):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg

def add_header(slide, chapter_tag, title_text):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(4.3), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_PILL_BG
    pill.line.color.rgb = C_BLUE_ACCENT
    tf_p = pill.text_frame
    tf_p.paragraphs[0].text = chapter_tag
    tf_p.paragraphs[0].font.name = FONT_HEADING
    tf_p.paragraphs[0].font.size = Pt(10)
    tf_p.paragraphs[0].font.bold = True
    tf_p.paragraphs[0].font.color.rgb = C_BLUE_ACCENT

    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.733), Inches(0.65))
    tf_title = tb_title.text_frame
    p_t = tf_title.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_TITLE

def add_footer_and_insight(slide, num, script_text):
    summary = script_text.replace('\n', ' ').strip()
    if len(summary) > 130:
        summary = summary[:128] + "..."
    banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.58))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_CARD
    banner.line.color.rgb = C_CARD_BORDER
    tf_bn = banner.text_frame
    tf_bn.margin_left = Inches(0.25)
    p_bn = tf_bn.paragraphs[0]
    p_bn.text = f"【EXECUTIVE INSIGHT】 {summary}"
    p_bn.font.name = FONT_BODY
    p_bn.font.size = Pt(10.5)
    p_bn.font.color.rgb = C_TEXT_BOLD

    tb_page = slide.shapes.add_textbox(Inches(9.5), Inches(7.0), Inches(3.033), Inches(0.35))
    tf_page = tb_page.text_frame
    p_pr = tf_page.paragraphs[0]
    p_pr.alignment = PP_ALIGN.RIGHT
    p_pr.text = f"SLIDE {num:02d} / 40"
    p_pr.font.name = FONT_HEADING
    p_pr.font.size = Pt(10)
    p_pr.font.bold = True
    p_pr.font.color.rgb = C_BLUE_ACCENT
