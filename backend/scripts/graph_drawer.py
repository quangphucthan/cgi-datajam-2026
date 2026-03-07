from pathlib import Path
import pandas as pd


def build_ctas_distribution(df: pd.DataFrame) -> dict[str, int]:
    return {
        "CTAS1": int(df["CTAS1"].sum()),
        "CTAS2": int(df["CTAS2"].sum()),
        "CTAS3": int(df["CTAS3"].sum()),
        "CTAS4": int(df["CTAS4"].sum()),
        "CTAS5": int(df["CTAS5"].sum()),
    }


def draw_bar_chart_svg(data: dict[str, int], output_path: Path) -> None:
    width, height = 900, 520
    margin_left, margin_right, margin_top, margin_bottom = 90, 40, 80, 90
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    max_value = max(data.values()) if data else 1

    bar_count = len(data)
    slot_width = chart_width / bar_count
    bar_width = slot_width * 0.6
    colors = ["#0b5fff", "#2a8bf2", "#36b9cc", "#7cc36b", "#f4a261"]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')
    svg.append(
        '<text x="450" y="42" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        'font-size="24" font-weight="700" fill="#222">Graph 1 - CTAS Distribution (Total ER)</text>'
    )

    # Axes
    x0, y0 = margin_left, height - margin_bottom
    x1, y1 = width - margin_right, margin_top
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#333" stroke-width="2"/>')
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#333" stroke-width="2"/>')

    # Horizontal guide lines
    for i in range(6):
        y = y0 - (chart_height * i / 5)
        value = int(max_value * i / 5)
        svg.append(f'<line x1="{x0}" y1="{y:.2f}" x2="{x1}" y2="{y:.2f}" stroke="#e6e6e6" stroke-width="1"/>')
        svg.append(
            f'<text x="{x0 - 10}" y="{y + 5:.2f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="12" fill="#555">{value}</text>'
        )

    # Bars
    for idx, (label, value) in enumerate(data.items()):
        bar_h = 0 if max_value == 0 else (value / max_value) * chart_height
        x = margin_left + (idx * slot_width) + ((slot_width - bar_width) / 2)
        y = y0 - bar_h
        color = colors[idx % len(colors)]
        svg.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_h:.2f}" '
            f'fill="{color}" rx="3" ry="3"/>'
        )
        svg.append(
            f'<text x="{x + bar_width / 2:.2f}" y="{y - 8:.2f}" text-anchor="middle" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#222">{value}</text>'
        )
        svg.append(
            f'<text x="{x + bar_width / 2:.2f}" y="{y0 + 24:.2f}" text-anchor="middle" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#222">{label}</text>'
        )

    svg.append("</svg>")
    output_path.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    input_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "hospital_service_volume"
        / "Hospital_Service_Volumes_CTAS_Wide_20260306.csv"
    )
    df = pd.read_csv(input_path)
    ctas_totals = build_ctas_distribution(df)

    output_dir = Path(__file__).resolve().parents[1] / "data" / "processed" / "hospital_service_volume"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "Graph_1_CTAS_Distribution.svg"
    draw_bar_chart_svg(ctas_totals, output_path)

    print("CTAS totals:", ctas_totals)
    print(f"Saved graph: {output_path}")


if __name__ == "__main__":
    main()
