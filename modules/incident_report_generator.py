"""
NECROS X - Incident Report Generator Module
Generates professional PDF incident reports for compliance and SOC documentation.
Preserved from original + enhanced with executive summary, risk tables, and timeline.
"""
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd
from datetime import datetime


def generate_incident_report(attack_history, soc_summary):
    file_path = "NECROS_X_Incident_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "NecrosTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
    )
    heading_style = ParagraphStyle(
        "NecrosHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#c0392b"),
        spaceBefore=12,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "NecrosBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
    )

    elements = []

    # Title
    elements.append(Paragraph("NECROS X — Cybersecurity Incident Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC", body_style))
    elements.append(Spacer(1, 16))

    if len(attack_history) == 0:
        elements.append(Paragraph("No attack activity detected in this session.", body_style))
    else:
        attack_df = pd.DataFrame(attack_history)
        total_attacks = len(attack_df)
        critical_attacks = len(attack_df[attack_df["severity"] == "Critical"])
        high_attacks = len(attack_df[attack_df["severity"] == "High"])
        top_target = attack_df["api_target"].value_counts().idxmax()
        top_ip = attack_df["source_ip"].value_counts().idxmax()

        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        exec_text = (
            f"During this monitoring session, NECROS X detected <b>{total_attacks}</b> attack events "
            f"across the API infrastructure. <b>{critical_attacks}</b> events were classified as Critical, "
            f"and <b>{high_attacks}</b> as High severity. The most targeted API endpoint was "
            f"<b>{top_target}</b>. The most active threat actor source was IP <b>{top_ip}</b>."
        )
        elements.append(Paragraph(exec_text, body_style))
        elements.append(Spacer(1, 10))

        # Statistics Table
        elements.append(Paragraph("Attack Statistics", heading_style))
        stats_data = [
            ["Metric", "Value"],
            ["Total Events Detected", str(total_attacks)],
            ["Critical Severity", str(critical_attacks)],
            ["High Severity", str(high_attacks)],
            ["Most Targeted API", top_target],
            ["Most Active Source IP", top_ip],
            ["Unique APIs Targeted", str(attack_df["api_target"].nunique())],
            ["Unique Source IPs", str(attack_df["source_ip"].nunique())],
        ]
        stats_table = Table(stats_data, colWidths=[3*inch, 3.5*inch])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 10),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8f8f8"), colors.white]),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 14))

        # AI SOC Summary
        elements.append(Paragraph("AI SOC Analyst Summary", heading_style))
        clean_summary = soc_summary.replace("\n", "<br/>").replace("━", "─")
        elements.append(Paragraph(clean_summary, body_style))
        elements.append(Spacer(1, 14))

        # Attack Log (last 20 events)
        elements.append(Paragraph("Attack Event Log (last 20 events)", heading_style))
        log_cols = ["timestamp", "api_target", "attack_type", "source_ip", "severity"]
        available = [c for c in log_cols if c in attack_df.columns]
        log_subset = attack_df[available].tail(20)
        table_data = [list(log_subset.columns)] + log_subset.values.tolist()
        log_table = Table(table_data, repeatRows=1)
        log_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#c0392b")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#fff5f5"), colors.white]),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        elements.append(log_table)

    doc.build(elements)
    return file_path
