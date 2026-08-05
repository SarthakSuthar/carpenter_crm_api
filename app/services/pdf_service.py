import base64
from datetime import date
from decimal import Decimal
from io import BytesIO
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.user import User

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm

styles = getSampleStyleSheet()
normal = styles["Normal"]
right_style = ParagraphStyle("right", parent=normal, alignment=TA_RIGHT)
bold = ParagraphStyle("bold", parent=normal, fontName="Helvetica-Bold")
bold_right = ParagraphStyle("bold_right", parent=right_style, fontName="Helvetica-Bold")


def _build_pdf(order: Order, user: User, logo_image: Image | None) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
    )

    elements: list[Flowable] = []

    left_col: list[Flowable] = [
        Paragraph("To,", normal),
        Paragraph(f"<b>{order.customer_name}</b>", normal),
        Paragraph(f"Date: {date.today().strftime('%d-%m-%Y')}", normal),
    ]

    right_col: list[Flowable] = []
    if logo_image:
        right_col.append(logo_image)
    right_col += [
        Paragraph(user.contact_person_name or "", right_style),
        Paragraph(user.contact_number or "", right_style),
        Paragraph(user.address or "", right_style),
    ]

    left_table = Table([[p] for p in left_col])
    right_table = Table([[p] for p in right_col])

    header_table = Table(
        [[left_table, right_table]],
        colWidths=[(PAGE_W - 2 * MARGIN) * 0.55, (PAGE_W - 2 * MARGIN) * 0.45],
    )
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    elements.append(header_table)
    elements.append(Spacer(1, 10 * mm))

    data: list[list[str]] = [["Item", "Qty", "Size", "Rate", "Amount"]]
    for li in order.line_items or []:
        item_name: str = li.item_name
        quantity: Decimal = li.quantity
        measurement: str = li.measurement
        rate: Decimal = li.rate
        amount: Decimal = quantity * rate
        data.append(
            [
                item_name,
                str(int(quantity) if quantity == int(quantity) else quantity),
                measurement,
                f"{rate:.2f}",
                f"{amount:.2f}",
            ]
        )
    data.append(["", "", "", "Total", f"{order.total_amount:.2f}"])

    items_table = Table(data, colWidths=[80 * mm, 20 * mm, 30 * mm, 30 * mm, 30 * mm])
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
                ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(items_table)
    elements.append(Spacer(1, 10 * mm))

    elements.append(Paragraph("<b>Notes</b>", normal))
    for note in order.notes or []:
        elements.append(Paragraph(f"- {note}", normal))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def convert_pdf_to_base64(buffer: BytesIO) -> str:
    buffer.seek(0)
    pdf_bytes = buffer.read()
    return base64.b64encode(pdf_bytes).decode("ascii")


def convert_base64_to_image(image: str, width: float, height: float) -> Image:
    if "," in image:
        image = image.split(",", 1)[1]

    image_bytes = base64.b64decode(image)
    return Image(BytesIO(image_bytes), width=width, height=height)


async def create_pdf(db: AsyncSession, order_id: UUID) -> JSONResponse:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No order found."
        )

    user_result = await db.execute(select(User).where(User.id == order.user_id))
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have this record.",
        )

    if not order.line_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has no line items to invoice.",
        )

    logo_image: Image | None = None
    if user.company_logo:
        logo_image = convert_base64_to_image(
            user.company_logo,
            width=30 * mm,
            height=15 * mm,
        )

    from starlette.concurrency import run_in_threadpool

    buffer = await run_in_threadpool(_build_pdf, order, user, logo_image)
    base64_pdf = convert_pdf_to_base64(buffer)

    return JSONResponse(
        {
            "order_id": order.id,
            "filename": f"invoice_{order.id}.pdf",
            "base64": base64_pdf,
        }
    )
