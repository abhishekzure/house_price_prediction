import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def get_styles():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'RepTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1c3464'),
        fontName='Helvetica-Bold',
        spaceAfter=4,
    )
    sub_style = ParagraphStyle(
        'RepSub',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#6c757d'),
        spaceAfter=10,
    )
    section_style = ParagraphStyle(
        'RepSection',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1c3464'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6,
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#202938'),
    )
    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#202938'),
    )
    val_box_style = ParagraphStyle(
        'ValBox',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#198754'),
        alignment=1,
        fontName='Helvetica-Bold',
    )
    return {
        'title': title_style,
        'sub': sub_style,
        'section': section_style,
        'cell_bold': cell_bold,
        'cell_normal': cell_normal,
        'val_box': val_box_style,
    }


def generate_single_prediction_pdf(prediction):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    st = get_styles()
    story = []

    # Title & Subtitle
    story.append(Paragraph("HOUSE PRICE PREDICTION VALUATION REPORT", st['title']))
    story.append(Paragraph(
        f"Report ID: #{prediction.id} &bull; Generated on: {prediction.created_at.strftime('%d %B %Y, %I:%M %p')} &bull; Account: {prediction.user.username}",
        st['sub']
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#315fe8"), spaceAfter=12))

    # Estimated Valuation Banner Box
    price_val = f"INR {prediction.predicted_price:,.2f}"
    price_html = f"<b>Estimated Market Price</b><br/><font size=18 color='#198754'><b>{price_val}</b></font>"
    banner_table = Table([[Paragraph(price_html, st['val_box'])]], colWidths=[540])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eaf2ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbdcff')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 14))

    # Specifications Table
    story.append(Paragraph("Property Specifications", st['section']))

    specs_data = [
        [Paragraph("Property Attribute", st['cell_bold']), Paragraph("Specification", st['cell_bold']),
         Paragraph("Neighborhood / Surrounding", st['cell_bold']), Paragraph("Specification", st['cell_bold'])],
        [Paragraph("City", st['cell_normal']), Paragraph(str(prediction.city), st['cell_normal']),
         Paragraph("Distance to Metro", st['cell_normal']), Paragraph(f"{prediction.distance_to_metro_km} km", st['cell_normal'])],
        [Paragraph("Locality Tier", st['cell_normal']), Paragraph(str(prediction.locality_tier), st['cell_normal']),
         Paragraph("Distance to City Center", st['cell_normal']), Paragraph(f"{prediction.distance_to_citycenter_km} km", st['cell_normal'])],
        [Paragraph("Bedrooms (BHK)", st['cell_normal']), Paragraph(str(prediction.bhk), st['cell_normal']),
         Paragraph("Nearby School", st['cell_normal']), Paragraph(f"{prediction.nearby_school_km} km", st['cell_normal'])],
        [Paragraph("Bathrooms", st['cell_normal']), Paragraph(str(prediction.bathrooms), st['cell_normal']),
         Paragraph("Nearby Hospital", st['cell_normal']), Paragraph(f"{prediction.nearby_hospital_km} km", st['cell_normal'])],
        [Paragraph("Super Area", st['cell_normal']), Paragraph(f"{prediction.super_area_sqft} sq.ft.", st['cell_normal']),
         Paragraph("Crime Rate Index", st['cell_normal']), Paragraph(str(prediction.crime_rate_index), st['cell_normal'])],
        [Paragraph("Carpet Area", st['cell_normal']), Paragraph(f"{prediction.carpet_area_sqft} sq.ft.", st['cell_normal']),
         Paragraph("Parking", st['cell_normal']), Paragraph("Available" if prediction.parking else "Not available", st['cell_normal'])],
        [Paragraph("Floor Number", st['cell_normal']), Paragraph(f"Floor {prediction.floor_no} of {prediction.total_floors}", st['cell_normal']),
         Paragraph("Elevator / Lift", st['cell_normal']), Paragraph("Available" if prediction.lift else "Not available", st['cell_normal'])],
        [Paragraph("Property Age", st['cell_normal']), Paragraph(f"{prediction.property_age_years} years", st['cell_normal']),
         Paragraph("Gated Society", st['cell_normal']), Paragraph("Yes" if prediction.gated_society else "No", st['cell_normal'])],
        [Paragraph("Furnishing Status", st['cell_normal']), Paragraph(str(prediction.furnishing), st['cell_normal']),
         Paragraph("Predicted Date", st['cell_normal']), Paragraph(prediction.created_at.strftime('%d-%b-%Y'), st['cell_normal'])],
    ]

    table = Table(specs_data, colWidths=[135, 135, 135, 135])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c3464')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d6dce5')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(table)
    story.append(Spacer(1, 14))

    # Valuation Note / Disclaimer
    disclaimer = (
        "<b>Notice & Valuation Methodology:</b> This valuation estimate is computed automatically using a trained "
        "machine learning ensemble model (Random Forest / Regression) based on historical real estate transactions. "
        "Actual market value may vary based on exact interior condition, legal verification, market volatility, "
        "and physical property inspections. HousePrice AI &copy; 2026."
    )
    story.append(Paragraph(disclaimer, st['sub']))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def generate_user_report_pdf(user, predictions):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    st = get_styles()
    story = []

    # Title & Subtitle
    story.append(Paragraph("USER PREDICTION HISTORY REPORT", st['title']))
    story.append(Paragraph(
        f"User: {user.username} ({user.email or 'No email'}) &bull; Total Records: {len(predictions)}",
        st['sub']
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#315fe8"), spaceAfter=12))

    if predictions:
        total = len(predictions)
        avg_val = sum(float(p.predicted_price) for p in predictions) / total
        max_val = max(float(p.predicted_price) for p in predictions)
        min_val = min(float(p.predicted_price) for p in predictions)

        # Summary box
        summary_data = [
            [Paragraph("Total Predictions", st['cell_bold']),
             Paragraph("Average Estimated Value", st['cell_bold']),
             Paragraph("Lowest Estimate", st['cell_bold']),
             Paragraph("Highest Estimate", st['cell_bold'])],
            [Paragraph(str(total), st['cell_normal']),
             Paragraph(f"INR {avg_val:,.2f}", st['cell_normal']),
             Paragraph(f"INR {min_val:,.2f}", st['cell_normal']),
             Paragraph(f"INR {max_val:,.2f}", st['cell_normal'])],
        ]
        sum_table = Table(summary_data, colWidths=[135, 135, 135, 135])
        sum_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eaf2ff')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbdcff')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(sum_table)
        story.append(Spacer(1, 14))

        # Prediction table
        story.append(Paragraph("Detailed Prediction History", st['section']))
        rows = [
            [
                Paragraph("#", st['cell_bold']),
                Paragraph("City", st['cell_bold']),
                Paragraph("BHK / Bath", st['cell_bold']),
                Paragraph("Super Area", st['cell_bold']),
                Paragraph("Estimated Price", st['cell_bold']),
                Paragraph("Date", st['cell_bold']),
            ]
        ]
        for p in predictions[:50]:  # up to 50 entries
            rows.append([
                Paragraph(str(p.id), st['cell_normal']),
                Paragraph(f"{p.city} ({p.locality_tier})", st['cell_normal']),
                Paragraph(f"{p.bhk} BHK / {p.bathrooms} Bath", st['cell_normal']),
                Paragraph(f"{p.super_area_sqft:.0f} sq.ft.", st['cell_normal']),
                Paragraph(f"INR {p.predicted_price:,.2f}", st['cell_normal']),
                Paragraph(p.created_at.strftime('%d-%b-%Y'), st['cell_normal']),
            ])

        table = Table(rows, colWidths=[35, 115, 110, 80, 110, 90])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c3464')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d6dce5')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(table)
    else:
        story.append(Paragraph("No prediction records found for this user account.", st['cell_normal']))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "HousePrice AI Prediction System &bull; Confidential &bull; Generated for account holder.",
        st['sub']
    ))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def generate_admin_report_pdf(predictions, total_users, total_predictions, avg_price, metrics_report=None):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    st = get_styles()
    story = []

    # Title & Subtitle
    story.append(Paragraph("SYSTEM VALUATION & ML EXECUTIVE REPORT", st['title']))
    story.append(Paragraph(
        f"HousePrice AI Platform &bull; Executive System Audit &bull; Generated by Administrator",
        st['sub']
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#315fe8"), spaceAfter=12))

    # Platform KPI Summary
    story.append(Paragraph("Platform Overview", st['section']))
    model_name = metrics_report.get('selected_model', 'Random Forest') if metrics_report else 'Trained Model'
    kpi_data = [
        [
            Paragraph("Total Accounts", st['cell_bold']),
            Paragraph("Total Predictions", st['cell_bold']),
            Paragraph("Mean Predicted Value", st['cell_bold']),
            Paragraph("Active ML Algorithm", st['cell_bold']),
        ],
        [
            Paragraph(str(total_users), st['cell_normal']),
            Paragraph(str(total_predictions), st['cell_normal']),
            Paragraph(f"INR {avg_price:,.2f}", st['cell_normal']),
            Paragraph(model_name, st['cell_normal']),
        ],
    ]
    kpi_table = Table(kpi_data, colWidths=[135, 135, 135, 135])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eaf2ff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbdcff')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # ML Model Performance
    if metrics_report and 'metrics' in metrics_report:
        story.append(Paragraph("Machine Learning Pipeline Evaluation", st['section']))
        ml_rows = [
            [
                Paragraph("Model", st['cell_bold']),
                Paragraph("MAE (INR)", st['cell_bold']),
                Paragraph("RMSE (INR)", st['cell_bold']),
                Paragraph("R² Score", st['cell_bold']),
                Paragraph("Deployment Status", st['cell_bold']),
            ]
        ]
        for name, vals in metrics_report['metrics'].items():
            status = "ACTIVE / SELECTED" if name == model_name else "ALTERNATIVE"
            ml_rows.append([
                Paragraph(name, st['cell_normal']),
                Paragraph(f"INR {vals.get('mae_inr', 0):,.2f}", st['cell_normal']),
                Paragraph(f"INR {vals.get('rmse_inr', 0):,.2f}", st['cell_normal']),
                Paragraph(f"{vals.get('r2', 0):.4f}", st['cell_normal']),
                Paragraph(status, st['cell_normal']),
            ])
        ml_table = Table(ml_rows, colWidths=[120, 105, 105, 90, 120])
        ml_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c3464')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d6dce5')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(ml_table)
        story.append(Spacer(1, 10))

    # Recent System Predictions Table
    story.append(Paragraph("Recent System Predictions", st['section']))
    pred_rows = [
        [
            Paragraph("ID", st['cell_bold']),
            Paragraph("User", st['cell_bold']),
            Paragraph("City", st['cell_bold']),
            Paragraph("Specs", st['cell_bold']),
            Paragraph("Estimated Price", st['cell_bold']),
            Paragraph("Date", st['cell_bold']),
        ]
    ]
    for p in predictions[:60]:
        pred_rows.append([
            Paragraph(str(p.id), st['cell_normal']),
            Paragraph(p.user.username, st['cell_normal']),
            Paragraph(f"{p.city} ({p.locality_tier})", st['cell_normal']),
            Paragraph(f"{p.bhk}BHK/{p.super_area_sqft:.0f}sqft", st['cell_normal']),
            Paragraph(f"INR {p.predicted_price:,.2f}", st['cell_normal']),
            Paragraph(p.created_at.strftime('%d-%b-%Y'), st['cell_normal']),
        ])
    pred_table = Table(pred_rows, colWidths=[35, 95, 110, 110, 105, 85])
    pred_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1c3464')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d6dce5')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(pred_table)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "HousePrice AI Platform System &bull; Confidential Executive Report",
        st['sub']
    ))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
