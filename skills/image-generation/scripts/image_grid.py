#!/usr/bin/env -S uv run --with Pillow
# /// script
# dependencies = ["Pillow"]
# ///
"""
Image Grid Generator

Creates an HTML file showing multiple images in a grid. Clicking an image copies
selection text to clipboard for easy feedback to the model.

Usage:
    uv run image_grid.py image1.png image2.png image3.png -o grid.html
    uv run image_grid.py *.png -o grid.html --prefix "variation_"

Then open grid.html in browser, click preferred image to copy selection text.
"""

import argparse
import base64
from pathlib import Path
import webbrowser
from PIL import Image


# Cost lookup table based on resolution (max dimension in pixels)
COST_BY_RESOLUTION = {
    1024: 0.04,   # 1K
    2048: 0.13,   # 2K
    4096: 0.24,   # 4K
}


def get_image_cost(img_path: Path) -> float:
    """Get cost for an image based on its resolution."""
    try:
        with Image.open(img_path) as img:
            max_dim = max(img.size)
            # Find the matching resolution tier
            for res, cost in sorted(COST_BY_RESOLUTION.items()):
                if max_dim <= res:
                    return cost
            # If larger than 4K, use 4K price
            return COST_BY_RESOLUTION[4096]
    except Exception:
        # Default to 1K if we can't read the image
        return COST_BY_RESOLUTION[1024]

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image Selection Grid</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a1a;
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-weight: 400;
            color: #888;
            font-size: 14px;
        }
        .toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
            font-size: 14px;
        }
        .toast.show { opacity: 1; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .card {
            background: #2a2a2a;
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.4);
        }
        .card:active {
            transform: translateY(-2px);
        }
        .card img {
            width: 100%;
            height: auto;
            display: block;
        }
        .card .label {
            position: absolute;
            top: 12px;
            left: 12px;
            background: rgba(0,0,0,0.7);
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
        }
        .card .filename {
            padding: 12px;
            font-size: 12px;
            color: #888;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .instructions {
            text-align: center;
            margin-bottom: 20px;
            color: #666;
            font-size: 13px;
        }
        .cost-footer {
            max-width: 1400px;
            margin: 24px auto 0;
            padding: 16px 20px;
            background: #2a2a2a;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
        }
        .cost-footer .total {
            color: #4CAF50;
            font-weight: 600;
            font-size: 15px;
        }
        .cost-footer .detail {
            color: #888;
        }
    </style>
</head>
<body>
    <h1>Click an image to copy selection text</h1>
    <p class="instructions">Paste the copied text back to continue with your chosen image</p>
    <div id="toast" class="toast">Copied to clipboard!</div>
    <div class="grid">
        {cards}
    </div>
    {cost_footer}
    <script>
        function copyToClipboard(text, label) {
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById('toast');
                toast.textContent = 'Copied: ' + label;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            });
        }
    </script>
</body>
</html>'''

CARD_TEMPLATE = '''
        <div class="card" onclick="copyToClipboard('{copy_text}', '{label}')">
            <span class="label">{label}</span>
            <img src="{src}" alt="{label}">
            <div class="filename">{filename}</div>
        </div>'''


def image_to_data_uri(path: Path) -> str:
    """Convert image to base64 data URI for embedding in HTML."""
    suffix = path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime = mime_types.get(suffix, 'image/png')
    data = base64.b64encode(path.read_bytes()).decode('utf-8')
    return f"data:{mime};base64,{data}"


COST_FOOTER_TEMPLATE = '''
    <div class="cost-footer">
        <span class="detail">{detail}</span>
        <span class="total">Total: ${total:.2f}</span>
    </div>'''


def generate_grid(
    images: list[Path],
    output: Path,
    embed: bool = True,
    copy_format: str = "I choose {label} ({filename})",
    show_cost: bool = True
) -> tuple[Path, float]:
    """
    Generate an HTML grid of images.

    Args:
        images: List of image paths
        output: Output HTML path
        embed: If True, embed images as data URIs (portable, larger file)
        copy_format: Format string for clipboard text. Available vars: {label}, {filename}, {path}
        show_cost: If True, show cost footer based on auto-detected resolution

    Returns:
        Tuple of (path to generated HTML, total cost)
    """
    cards = []
    costs = []

    for i, img_path in enumerate(images):
        label = f"#{i + 1}"
        filename = img_path.name

        if embed:
            src = image_to_data_uri(img_path)
        else:
            src = str(img_path.absolute())

        copy_text = copy_format.format(
            label=label,
            filename=filename,
            path=str(img_path.absolute())
        )

        cards.append(CARD_TEMPLATE.format(
            src=src,
            label=label,
            filename=filename,
            copy_text=copy_text.replace("'", "\\'")
        ))

        if show_cost:
            costs.append(get_image_cost(img_path))

    # Generate cost footer with auto-detected costs
    cost_footer = ""
    total_cost = 0.0
    if show_cost and costs:
        total_cost = sum(costs)
        # Check if all costs are the same
        if len(set(costs)) == 1:
            detail = f"{len(images)} images × ${costs[0]:.2f} each"
        else:
            detail = f"{len(images)} images (mixed resolutions)"
        cost_footer = COST_FOOTER_TEMPLATE.format(
            detail=detail,
            total=total_cost
        )

    html = HTML_TEMPLATE.replace('{cards}', ''.join(cards)).replace('{cost_footer}', cost_footer)
    output.write_text(html)
    return output, total_cost


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML grid for image selection"
    )
    parser.add_argument(
        "images",
        nargs="+",
        help="Image files to include in grid"
    )
    parser.add_argument(
        "-o", "--output",
        default="image_grid.html",
        help="Output HTML file (default: image_grid.html)"
    )
    parser.add_argument(
        "--no-embed",
        action="store_true",
        help="Use file paths instead of embedding images (smaller HTML, not portable)"
    )
    parser.add_argument(
        "--copy-format",
        default="I choose {label} ({filename})",
        help="Format for clipboard text. Vars: {label}, {filename}, {path}"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the HTML file in default browser after creation"
    )
    parser.add_argument(
        "--no-cost",
        action="store_true",
        help="Hide cost information (cost is auto-detected from image resolution)"
    )

    args = parser.parse_args()

    images = [Path(p) for p in args.images]
    missing = [p for p in images if not p.exists()]
    if missing:
        print(f"Error: Files not found: {', '.join(str(p) for p in missing)}")
        return 1

    output = Path(args.output)
    output, total_cost = generate_grid(
        images,
        output,
        embed=not args.no_embed,
        copy_format=args.copy_format,
        show_cost=not args.no_cost
    )

    cost_msg = f" (${total_cost:.2f} total)" if not args.no_cost else ""
    print(f"Created {output} with {len(images)} images{cost_msg}")

    if args.open:
        webbrowser.open(f"file://{output.absolute()}")

    return 0


if __name__ == "__main__":
    exit(main())
