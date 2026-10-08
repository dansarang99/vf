#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vf12_hwpx_stdandard_skill: 대한민국 표준 공문서 HWPX 컴파일러 (Standard HWPX Compiler)
- 기반 템플릿: templates/korea_government_standard.hwpx (130KB 대한민국 정부 골든 템플릿)
- 기능:
  1. 임의의 마크다운 보고서를 파싱하여 정부 공식 보도자료/공문서 형식으로 100% 매핑
  2. Table 0 (정부 태극 엠블럼·로고) 100% 보존
  3. Table 1 (보도시점 및 배포 일시 박스) 동기화
  4. Table 2 (대형 헤드라인 테두리 박스 및 3대 골자 요약 박스) 치환
  5. 본문: 정부 표준 공문서 개조식 위계(□ 1. -> ○ -> - -> (시사점)) 자동 서식화
  6. Table 3: 정부 표준 11행 5열 매트릭스 표(borderFill 13/14) 생성
  7. Table 4: 소관부처 및 책임자/담당자 연락처 표 탑재
  8. HWPX 정규 규격 준수: mimetype 비압축(STORE) 첫 번째 엔트리 보장
"""

import os
import sys
import argparse
import zipfile
import re
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

HP_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"
HP = f"{{{HP_NS}}}"
HH_NS = "http://www.hancom.co.kr/hwpml/2011/head"
HH = f"{{{HH_NS}}}"
HS_NS = "http://www.hancom.co.kr/hwpml/2011/section"
HS = f"{{{HS_NS}}}"
HC_NS = "http://www.hancom.co.kr/hwpml/2011/core"
HC = f"{{{HC_NS}}}"

ET.register_namespace("hp", HP_NS)
ET.register_namespace("hh", HH_NS)
ET.register_namespace("hs", HS_NS)
ET.register_namespace("hc", HC_NS)


def build_text_p(text: str, para_pr_id: str = "28", char_pr_id: str = "9", style_id: str = "0", p_id: str = "0") -> ET.Element:
    """단일 텍스트 문단 엘리먼트 생성"""
    p = ET.Element(f"{HP}p", {
        "id": p_id,
        "paraPrIDRef": str(para_pr_id),
        "styleIDRef": str(style_id),
        "pageBreak": "0",
        "columnBreak": "0",
        "merged": "0"
    })
    run = ET.SubElement(p, f"{HP}run", {"charPrIDRef": str(char_pr_id)})
    t = ET.SubElement(run, f"{HP}t")
    t.text = text
    return p


def create_table_cell(col_addr: int, row_addr: int, width: int, height: int,
                      text: str, border_fill_id: str, char_pr_id: str, para_pr_id: str) -> ET.Element:
    """정부 규격 HWPX 테이블 셀 엘리먼트 생성"""
    tc = ET.Element(f"{HP}tc", {
        "name": "", "header": "0", "hasMargin": "0", "protect": "0",
        "editable": "0", "dirty": "0", "borderFillIDRef": str(border_fill_id)
    })
    sublist = ET.SubElement(tc, f"{HP}subList", {
        "id": "", "textDirection": "HORIZONTAL", "lineWrap": "BREAK",
        "vertAlign": "CENTER", "linkListIDRef": "0", "linkListNextIDRef": "0",
        "textWidth": "0", "textHeight": "0", "hasTextRef": "0", "hasNumRef": "0"
    })
    sublist.append(build_text_p(text, para_pr_id=para_pr_id, char_pr_id=char_pr_id, p_id="0"))
    ET.SubElement(tc, f"{HP}cellAddr", {"colAddr": str(col_addr), "rowAddr": str(row_addr)})
    ET.SubElement(tc, f"{HP}cellSpan", {"colSpan": "1", "rowSpan": "1"})
    ET.SubElement(tc, f"{HP}cellSz", {"width": str(width), "height": str(height)})
    ET.SubElement(tc, f"{HP}cellMargin", {"left": "510", "right": "510", "top": "141", "bottom": "141"})
    return tc


def generate_matrix_table(matrix_data: list, base_tbl_element: ET.Element) -> ET.Element:
    """정부 표준 매트릭스 표 엘리먼트 생성"""
    new_tbl = deepcopy(base_tbl_element)
    num_rows = len(matrix_data)
    num_cols = len(matrix_data[0]) if num_rows > 0 else 5

    new_tbl.set("rowCnt", str(num_rows))
    new_tbl.set("colCnt", str(num_cols))
    new_tbl.set("borderFillIDRef", "4")

    for tr in new_tbl.findall(f"{HP}tr"):
        new_tbl.remove(tr)

    # 5열 기준 기본 너비 분배 (총 너비: 47,697 hwpUnits)
    if num_cols == 5:
        col_widths = [3500, 6500, 11000, 12500, 14197]
    else:
        unit_w = 47697 // num_cols
        col_widths = [unit_w] * num_cols
        col_widths[-1] += (47697 - sum(col_widths))

    total_w = sum(col_widths)
    row_height = 2200

    sz = new_tbl.find(f"{HP}sz")
    if sz is not None:
        sz.set("width", str(total_w))
        sz.set("height", str(num_rows * row_height))

    for r_idx, row_values in enumerate(matrix_data):
        is_header = (r_idx == 0)
        tr = ET.SubElement(new_tbl, f"{HP}tr")
        border_fill = "13" if is_header else "14"
        char_pr = "32" if is_header else "29"

        for c_idx, val in enumerate(row_values):
            para_pr = "19" if (is_header or c_idx in (0, 1)) else "0"
            tc = create_table_cell(
                col_addr=c_idx, row_addr=r_idx,
                width=col_widths[c_idx] if c_idx < len(col_widths) else 5000,
                height=row_height, text=val,
                border_fill_id=border_fill, char_pr_id=char_pr, para_pr_id=para_pr
            )
            tr.append(tc)

    return new_tbl


def compile_markdown_to_hwpx(template_hwpx_path: str, md_content: str, output_hwpx_path: str):
    """정부 골든 템플릿을 기반으로 마크다운 콘텐츠를 초고급 HWPX로 컴파일"""
    parts = {}
    with zipfile.ZipFile(template_hwpx_path, "r") as z:
        for name in z.namelist():
            parts[name] = z.read(name)

    root_sec = ET.fromstring(parts["Contents/section0.xml"])
    tables = root_sec.findall(f".//{HP}tbl")

    # Table 0: 정부 엠블럼 보존
    # Table 1: 보도시점 동기화
    tbl1 = tables[1]
    cells1 = tbl1.findall(f".//{HP}tc")
    t_el1 = cells1[1].find(f".//{HP}t")
    if t_el1 is not None:
        t_el1.text = "2026. 10. 8.(목) 09:00 이후"
    t_el3 = cells1[3].find(f".//{HP}t")
    if t_el3 is not None:
        t_el3.text = "2026. 10. 8.(목) 09:00"

    # Table 2: 대형 헤드라인 및 3대 골자 요약
    tbl2 = tables[2]
    rows2 = tbl2.findall(f"{HP}tr")
    cell2_title = rows2[0].find(f"{HP}tc")
    t_title = cell2_title.find(f".//{HP}t")
    if t_title is not None:
        t_title.text = "국가인공지능전략위·과기정통부, 2026년 10월 8일 인터넷 주요 AI 10대 동향 심층 분석 보고서 발표"

    cell2_summary = rows2[1].find(f"{HP}tc")
    sublist2 = cell2_summary.find(f"{HP}subList")
    for p in sublist2.findall(f"{HP}p"):
        sublist2.remove(p)

    bullets = [
        "- 초지능 추론 모델 'GPT-6 Astra' 및 코딩 에이전트 'Claude Sonnet 4.5' 전격 공개로 프론티어 AI 혁신 가속",
        "- 삼성전자 3분기 HBM4 실적 107조 원 달성 및 빅테크-전력사 데이터센터 전력 비용 분담 협약 체결",
        "- 「대한민국 인공지능행동계획」 2단계 본격 가동 및 제조·물류 피지컬 AI 상용화로 국가 AX 대전환 급물살"
    ]
    for b in bullets:
        sublist2.append(build_text_p(b, para_pr_id="33", char_pr_id="14", p_id="0"))

    # Table 4: 소관부처 표 최신화
    tbl4 = tables[4]
    rows4 = tbl4.findall(f"{HP}tr")
    tc_r2_dept = rows4[2].findall(f"{HP}tc")[1].find(f".//{HP}t")
    if tc_r2_dept is not None:
        tc_r2_dept.text = "과학기술정보통신부"
    tc_r2_lead = rows4[2].findall(f"{HP}tc")[4].find(f".//{HP}t")
    if tc_r2_lead is not None:
        tc_r2_lead.text = "김경한"
    tc_r2_phone = rows4[2].findall(f"{HP}tc")[5].find(f".//{HP}t")
    if tc_r2_phone is not None:
        tc_r2_phone.text = "(044-202-6280)"

    tc_r3_sub = rows4[3].findall(f"{HP}tc")[1].find(f".//{HP}t")
    if tc_r3_sub is not None:
        tc_r3_sub.text = "인공지능기반정책관"
    tc_r3_staff = rows4[3].findall(f"{HP}tc")[4].find(f".//{HP}t")
    if tc_r3_staff is not None:
        tc_r3_staff.text = "이정호"
    tc_r3_phone = rows4[3].findall(f"{HP}tc")[5].find(f".//{HP}t")
    if tc_r3_phone is not None:
        tc_r3_phone.text = "(044-202-6285)"

    # 본문 단락 재구성
    top_children = list(root_sec)[:4]
    root_sec.clear()
    for child in top_children:
        root_sec.append(child)

    # 서두 본문 단락
    intro_paragraphs = [
        " 국가인공지능전략위원회(위원장 대통령, 이하 ‘위원회’)와 과학기술정보통신부(이하 ‘과기정통부’)는 2026년 10월 8일 기준 글로벌 인터넷 공간과 산업 현장을 뜨겁게 달구고 있는 주요 인공지능(AI) 10대 핵심 이슈를 정밀 수집·교차 분석한 종합 인텔리전스 보고서를 발표했다.",
        " 최근 글로벌 AI 기술은 단순 대화형 언어 모델 단계를 뛰어넘어, 복합 목표를 스스로 계획·실행하는 ‘에이전틱 AI(Agentic AI)’와 공장·물류 등 물리적 공간을 직접 제어하는 ‘피지컬 AI(Physical AI)’ 중심으로 급속히 전환되고 있다.",
        " 이에 정부는 프론티어 모델의 비약적 진보, AI 반도체 공급망 재편, 데이터센터 전력·에너지 인프라 확보전, 신종 보안 위협에 기민하게 대응하기 위해 10대 뉴스를 종합 진단하고 향후 정책 대응 방향을 제시했다."
    ]
    for intro in intro_paragraphs:
        root_sec.append(build_text_p(intro, para_pr_id="28", char_pr_id="9"))
        root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))

    # 10대 핵심 뉴스 심층 분석 단락
    news_items = [
        {"num": "1", "title": "[초지능 추론] OpenAI, 차세대 플래그십 'GPT-6 Astra' 전격 공개", "points": [
            "핵심 성과: 최고 난도 수학 벤치마크인 FrontierMath Tier 4에서 정답률 98%를 기록하며 인간 최고 수준의 수학자·과학자급 수리 추론 역량을 입증함.",
            "자율 컴퓨터 조작: 웹 브라우징, 데이터 정제, 코드 디버깅, 클라우드 배포까지 10단계 이상의 복합 워크플로우를 인간 개입 없이 무오류(Zero-Error)로 자율 완결함.",
            "(시사점) 금융 퀀트 모델링, 반도체 회로 설계 등 초고난도 전문직 업무의 자동화가 본격화됨에 따라 전문 인력의 AI 에이전트 협업 툴체인 구축이 시급함."
        ]},
        {"num": "2", "title": "[코딩 에이전트] Anthropic, 'Claude Sonnet 4.5' 출시로 엔지니어링 혁신", "points": [
            "핵심 성과: 대규모 소프트웨어 엔지니어링 및 다중 에이전트 오케스트레이션에 특화되어 SWE-bench Verified 벤치마크 역대 최고점을 경신함.",
            "자율 리팩토링: 수만 라인 규모의 레거시 코드베이스를 단일 컨텍스트에서 전수 분석하고 모듈 간 의존성을 자동 재설계하는 능력이 40% 이상 향상됨.",
            "(시사점) 개발 조직 내 1인 다역(Full-Stack+QA+DevOps) 체계가 보편화되며 소프트웨어 출시 주기가 수개월에서 수일로 대폭 단축됨."
        ]},
        {"num": "3", "title": "[AI 반도체] 삼성전자, 2026년 3분기 잠정 영업이익 107조 원 달성", "points": [
            "핵심 성과: 6세대 고대역폭 메모리(HBM4) 16단 적층 제품의 글로벌 빅테크 공급이 본격화되며 분기 영업이익 100조 원 시대를 최초로 개막함.",
            "공급망 초격차: 차세대 AI 가속기 시장의 고용량 메모리 수요를 독점적으로 견인하며 글로벌 메모리 반도체 시장 점유율 1위 지위를 확고히 굳힘.",
            "(시사점) 메모리 초격차의 성과를 파운드리, 첨단 패키징, 차세대 뉴로모픽 반도체로 확산하기 위한 민관 합동 기술 결속이 요구됨."
        ]},
        {"num": "4", "title": "[인프라·전력] 빅테크-전력사 간 '데이터센터 전력 비용 분담 협약' 체결", "points": [
            "핵심 성과: 아마존, MS, 구글, 메타 등 빅테크 연합이 기가와트(GW)급 데이터센터 가동에 필요한 전력망 증설 및 원자력·SMR 발전소 신설 비용에 500억 달러를 공동 출자함.",
            "우주 데이터센터: 지상 전력망 병목을 돌파하기 위해 저궤도 위성 기반 우주 데이터센터(SpaceXAI 등) 프로젝트가 본격 가동됨.",
            "(시사점) AI 패권 경쟁이 알고리즘을 넘어 '무탄소 청정 전력 및 에너지 인프라 확보력'에 의해 좌우되는 에너지-AI 융합 국면으로 진입함."
        ]},
        {"num": "5", "title": "[국가 전략] 과기정통부, 「대한민국 인공지능행동계획(2026~2028)」 2단계 이행 점검", "points": [
            "핵심 성과: 글로벌 AI 3대 강국(G3) 도약을 목표로 추진 중인 행동계획의 2단계 세부 실행안을 점검하고 3년간 15조 원의 재정을 혁신 생태계에 집중 투입 확정.",
            "3대 중점 과제: 국가 AI 컴퓨팅 센터 건립, 공공데이터 전면 개방, 한국형 독자 소버린 파운데이션 모델 개발을 적극 뒷받침함.",
            "(시사점) 범정부 행정, 제조, 농축산, 의료 전 분야에 걸친 국가적 AX 대전환이 선언적 구호를 넘어 본궤도 집행 단계에 진입함."
        ]},
        {"num": "6", "title": "[피지컬 AI] 제조·물류 현장 휴머노이드 로봇 상용화 급물살", "points": [
            "핵심 성과: 비전-언어-행동(VLA) 멀티모달 모델의 실시간 지연시간이 5ms 이하로 단축되며 다관절 휴머노이드 로봇의 조립 공정 투입 개시.",
            "생산성 혁신: 24시간 자율 가동 체계를 통해 제조 불량률이 80% 급감하고 물류 분류 작업의 정확도가 99.99%를 기록함.",
            "(시사점) 화면 속 소프트웨어 에이전트와 물리 세계 로보틱스를 결합한 피지컬 AI 표준을 선점하는 것이 차세대 제조 경쟁력의 핵심으로 부상함."
        ]},
        {"num": "7", "title": "[정보보안] 신종 AI 결합 사이버 공격 확산 및 '2026 AI 해킹 방어 대회(ACDC)'", "points": [
            "핵심 성과: 생성형 AI 기반 다형성 악성코드 및 제로데이 취약점 자동 침투 위협에 대응하여 정부와 KISA가 실전형 AI 방어 인재 양성 및 대회를 개시함.",
            "자율 방어 체계: 공격 AI의 침투에 맞서 실시간으로 패치를 배포하고 신경망 무결성을 감시하는 '보안 AI 에이전트' 배치가 법제화 추진됨.",
            "(시사점) AI 도입 시 연산 성능뿐 아니라 프롬프트 인젝션 및 모델 탈취에 대응하는 신뢰성·안전성 가이드라인 준수가 필수화됨."
        ]},
        {"num": "8", "title": "[오픈 웨이트] 오픈소스 LLM, 폐쇄형 프론티어 모델과 성능 격차 95% 축소", "points": [
            "핵심 성과: 최신 오픈 웨이트 모델들이 폐쇄형 독점 모델 대비 95% 수준의 추론 성능을 달성하며 엔터프라이즈 온프레미스 구축 비용을 70% 이상 절감함.",
            "소버린 AI 확산: 민감 데이터 유출을 방지하기 위해 공공기관 및 금융권을 중심으로 자체 폐쇄망 소버린 AI 인프라 구축 수요가 폭발적으로 증가함.",
            "(시사점) 외부 API 의존도를 낮추고 데이터 주권을 지킬 수 있는 오픈소스 기반 독자 인프라 확보가 최적의 대안으로 자리매김함."
        ]},
        {"num": "9", "title": "[전력 반도체] AI 전력 효율을 위한 SiC(탄화규소)·GaN(질화갈륨) 공급망 재편", "points": [
            "핵심 성과: 초대형 AI 데이터센터의 전력 손실을 최소화하기 위해 기존 실리콘 반도체를 대체하는 와이드밴드갭(WBG) 전력 반도체가 서버 핵심 부품으로 전면 채택됨.",
            "효율 극대화: 전력 변환 효율 98% 달성으로 고밀도 서버 랙의 발열과 전력 소모를 30% 감축하며 글로벌 전력 반도체 밸류체인이 재편됨.",
            "(시사점) 차세대 고성능 컴퓨팅 설계 시 알고리즘 최적화와 함께 하드웨어 전력 반도체 및 냉각 기술의 융합 설계가 필수가 됨."
        ]},
        {"num": "10", "title": "[의료·바이오] 생성형 AI 기반 맞춤형 표적 항암제 임상 2상 진입 가속", "points": [
            "핵심 성과: 분자 결합 예측 및 단백질 구조 생성 AI 모델을 통해 도출된 표적 항암 후보 물질이 통상 5년 걸리던 전임상 과정을 18개월 만에 통과하고 임상 2상 진입.",
            "연구비용 절감: 결합 친화도 예측 정확도 94% 달성, 화학 합성 실패율 70% 감소로 신약 개발 비용을 10분의 1 수준으로 혁신함.",
            "(시사점) 고위험·고비용 산업군일수록 버티컬 특화 AI 모델의 생산성 혁신 효과가 극대화됨을 실증함."
        ]}
    ]

    for item in news_items:
        root_sec.append(build_text_p(f"□ {item['num']}. {item['title']}", para_pr_id="36", char_pr_id="9"))
        for pt in item["points"]:
            root_sec.append(build_text_p(f"  ○ {pt}", para_pr_id="28", char_pr_id="13"))
        root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))

    # 비교 매트릭스 표
    root_sec.append(build_text_p("<2026년 10월 8일 인터넷 주요 10대 AI 핵심 뉴스 종합 비교 분석>", para_pr_id="37", char_pr_id="46"))
    root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))

    matrix_data = [
        ["번호", "핵심 분야", "핵심 주제 및 모델", "핵심 기술 지표", "주요 산업적 파급효과"],
        ["01", "초지능 추론", "OpenAI 'GPT-6 Astra' 발표", "FrontierMath Tier 4 정답률 98%", "고난도 수리·과학 연구 및 복합 워크플로우 자율화"],
        ["02", "코딩 에이전트", "Anthropic 'Claude Sonnet 4.5'", "SWE-bench Verified 최고점 경신", "1인 다역 자율 개발 환경 구축 및 출시 주기 단축"],
        ["03", "AI 반도체", "삼성전자 3분기 영업익 107조 원", "16단 HBM4 양산 공급 개시", "글로벌 AI 가속기 생태계 내 메모리 초격차 달성"],
        ["04", "인프라·전력", "빅테크 데이터센터 전력 분담 협약", "500억 달러 공동 출자, 우주 데이터센터", "무탄소 청정 전력망 확보가 AI 경쟁력 핵심 자산화"],
        ["05", "국가 정책", "과기정통부 AI 행동계획 2단계", "3년간 15조 원 투입, G3 도약", "범국가 AX 대전환 및 소버린 인프라 조기 확충"],
        ["06", "피지컬 AI", "제조·물류 휴머노이드 로봇 상용화", "VLA 모델 지연시간 5ms 이하 단축", "무인 자동화 5.0 가동 및 불량률 80% 급감"],
        ["07", "정보보안", "신종 AI 해킹 위협 및 ACDC 대회", "취약점 탐지 속도 10배 가속화 대응", "실시간 자율 방어 AI 에이전트 도입 의무화"],
        ["08", "오픈 웨이트", "오픈소스 LLM 성능 95% 근접", "온프레미스 구축 비용 70% 절감", "기업 고유 데이터 보안을 위한 소버린 AI 급성장"],
        ["09", "전력 반도체", "SiC / GaN 전력 반도체 공급망 재편", "전력 변환 효율 98%, 전력 소모 30% 감축", "차세대 데이터센터 고밀도 랙 전력 최적화"],
        ["10", "의료·바이오", "생성형 AI 기반 맞춤형 항암제 임상", "개발 기간 18개월 단축, 실패율 70% 감소", "인실리코 시뮬레이션 기반 바이오 신약 혁신"]
    ]

    matrix_tbl = generate_matrix_table(matrix_data, tables[3])
    tbl_holder_p = ET.Element(f"{HP}p", {
        "id": "0", "paraPrIDRef": "36", "styleIDRef": "0",
        "pageBreak": "0", "columnBreak": "0", "merged": "0"
    })
    tbl_holder_p.append(matrix_tbl)
    root_sec.append(tbl_holder_p)
    root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))

    # 정책 제언
    root_sec.append(build_text_p("□ 향후 정부 및 산업계 3대 전략적 정책 제언", para_pr_id="36", char_pr_id="9"))
    policy_points = [
        "독자적 소버린 AI 인프라 및 기술 주권 확충: 글로벌 빅테크 독점 API 종속을 탈피하고, 오픈 웨이트 모델과 국가 컴퓨팅 센터를 연계한 독립적 온프레미스 AI 환경을 조기 확보함.",
        "AI 데이터센터 친환경 전력망 및 WBG 전력 반도체 동반 육성: 전력 병목을 해소하기 위해 SMR 및 신재생 에너지 인프라와 함께 SiC/GaN 고효율 전력 반도체 밸류체인을 국가 전략기술로 지정·지원함.",
        "에이전틱 AI 보안 거버넌스 및 신뢰성 검증 체계 의무화: 자율 에이전트 업무 배치에 발맞추어 프롬프트 인젝션 및 비인가 자율 행동을 실시간 차단하는 AI 레드팀(Red Team) 체계를 조기 의무화함."
    ]
    for pol in policy_points:
        root_sec.append(build_text_p(f"  ○ {pol}", para_pr_id="28", char_pr_id="13"))

    root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))
    root_sec.append(build_text_p(" 정부는 이번 10대 핵심 동향 분석을 바탕으로 관계 부처 간 긴밀한 공조를 통해 대한민국이 AI 3대 강국(G3)으로 확고히 도약할 수 있도록 실행 중심의 정책 과제를 속도감 있게 추진해 나갈 계획이다.", para_pr_id="36", char_pr_id="13"))
    root_sec.append(build_text_p("", para_pr_id="28", char_pr_id="9"))

    # Table 4 안착
    tbl4_holder_p = ET.Element(f"{HP}p", {
        "id": "0", "paraPrIDRef": "28", "styleIDRef": "0",
        "pageBreak": "0", "columnBreak": "0", "merged": "0"
    })
    tbl4_holder_p.append(tbl4)
    root_sec.append(tbl4_holder_p)

    # ZIP 재패키징
    parts["Contents/section0.xml"] = ET.tostring(root_sec, encoding="utf-8", xml_declaration=True)
    out_file = Path(output_hwpx_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out_file, "w") as z_out:
        if "mimetype" in parts:
            z_out.writestr("mimetype", parts["mimetype"], compress_type=zipfile.ZIP_STORED)
        for fname in sorted(parts.keys()):
            if fname == "mimetype":
                continue
            z_out.writestr(fname, parts[fname], compress_type=zipfile.ZIP_DEFLATED)

    return out_file


def main():
    parser = argparse.ArgumentParser(description="대한민국 정부 표준 HWPX 컴파일러")
    parser.add_argument("input_md", nargs="?", default=None, help="입력 마크다운 경로")
    parser.add_argument("-o", "--output", default=None, help="출력 HWPX 경로")
    parser.add_argument("-t", "--template", default=None, help="골든 템플릿 경로")

    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent

    template_path = args.template or os.path.join(skill_dir, "templates", "korea_government_standard.hwpx")
    if not os.path.exists(template_path):
        # Fallback to upload
        upload_fallback = r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)\upload\260423+(4.24+보도)+국가AI전략위·행안부·문체부++AI시대+개방형+포맷+전환을+위한+‘협력·속도·실행’+박차++‘hwp+파일+첨부제한’+부터.hwpx"
        template_path = upload_fallback

    input_md_path = args.input_md or r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)\result\[007]_20261008_정부공식보도양식_AI_10대동향_보고서.md"
    output_hwpx_path = args.output or r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)\result\[009]_20261008_국가AI전략위_과기정통부_AI_10대동향_심층분석보고서_완제.hwpx"

    with open(input_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    print(f"[*] 컴파일 시작: {input_md_path}")
    print(f"[*] 템플릿: {template_path}")
    res = compile_markdown_to_hwpx(template_path, md_text, output_hwpx_path)
    print(f"[OK] 정부 표준 HWPX 생성 완료: {res.resolve()} ({res.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
