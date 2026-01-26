# CC Gemini Image Plugin

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/lucharo)

Generate and edit images using Google's Gemini image models and Imagen 4 in Claude Code.

## Installation

### From GitHub

```bash
# Add this repo as a marketplace
claude plugin marketplace add lucharo/cc-gemini-image-plugin

# Install the plugin
claude plugin install gemini-image
```

### From Local Path

```bash
# Clone the repo
git clone https://github.com/lucharo/cc-gemini-image-plugin.git

# Add as local marketplace
claude plugin marketplace add /path/to/cc-gemini-image-plugin

# Install
claude plugin install gemini-image
```

## Prerequisites

### Authentication (choose one)

**Option 1: API Key (Recommended)**
```bash
export GEMINI_API_KEY="your-key-from-aistudio.google.com"
```

**Option 2: Vertex AI with Application Default Credentials**
```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### Dependencies

No global install needed - uses `uv` for inline dependencies:

```bash
uv run --with google-genai --with Pillow script.py
```

## Features

- **Text-to-image generation** - Create images from text descriptions
- **Image editing** - Transform existing images with text prompts
- **Multi-image composition** - Style transfer, combining images
- **Iterative editing** - Refine images through conversation
- **Character/object consistency** - Maintain consistent subjects across generations
- **Resolution control** - 1K, 2K, or 4K output
- **Aspect ratio options** - 1:1, 3:4, 4:3, 9:16, 16:9
- **Imagen 4 support** - Standalone generation with dedicated API
- **Image grid selector** - Visual comparison for multi-image workflows

## Usage

Once installed, simply ask Claude Code to generate or edit images:

- "Generate an image of a robot holding a banana"
- "Edit this image to make the background blue"
- "Apply the style from style.png to photo.jpg"
- "Create a watercolor painting of a sunset"
- "Generate 4 variations and show me a grid to choose from"

Claude will use the Gemini image API automatically.

### CLI Script

You can also use the helper script directly:

```bash
cd skills/image-generation/scripts

# Generate an image
uv run --with google-genai --with Pillow generate_image.py "A cat in a spacesuit" -o cat.png

# Edit an existing image
uv run --with google-genai --with Pillow generate_image.py "Make it blue" -i photo.jpg -o edited.png

# High resolution with aspect ratio
uv run --with google-genai --with Pillow generate_image.py "A panorama" -o wide.png -r 2K -a 16:9

# Use Imagen 4
uv run --with google-genai --with Pillow generate_image.py "A landscape" --imagen
```

### Image Grid Selector

When generating multiple variations, use the grid selector:

```bash
# Generate variations
for i in 1 2 3 4; do
  uv run --with google-genai --with Pillow generate_image.py "A cozy cafe, variation $i" -o cafe_$i.png
done

# Create selection grid
uv run image_grid.py cafe_*.png -o grid.html --open
```

Click your preferred image to copy selection text, then paste it back to Claude.

## Models

| Model | Best For | Resolution |
|-------|----------|------------|
| `gemini-2.5-flash-image` | Fast iteration, drafts | 1K |
| `gemini-3-pro-image-preview` | Final quality, text in images | 1K-4K |
| `imagen-4.0-generate-001` | Standalone generation | 1K-2K |
| `imagen-4.0-ultra-generate-001` | Highest quality | 1K-2K |
| `imagen-4.0-fast-generate-001` | Fast batch generation | 1K-2K |

## Pricing

Approximate costs per image:

| Resolution | Cost |
|------------|------|
| 1K (1024px) | ~$0.04 |
| 2K (2048px) | ~$0.13 |
| 4K (4096px) | ~$0.24 |

See `references/pricing.md` for detailed pricing and cost optimization tips.

**Get an API key:** [AI Studio](https://aistudio.google.com/apikey)

## Plugin Structure

```
cc-gemini-image-plugin/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── image-generation/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── generate_image.py
│       │   └── image_grid.py
│       └── references/
│           ├── models.md
│           ├── pricing.md
│           └── troubleshooting.md
└── README.md
```

## Changelog

### v0.2.0
- Added Imagen 4 support (`imagen-4.0-generate-001`, `imagen-4.0-ultra-generate-001`, `imagen-4.0-fast-generate-001`)
- Added resolution control (1K, 2K, 4K)
- Added aspect ratio options (1:1, 3:4, 4:3, 9:16, 16:9)
- Added `response_modalities` config (required by API)
- Added image grid selector for multi-image workflows
- Added pricing reference documentation
- Added character/object consistency examples
- Added Google Search grounding
- Marked deprecated models (`gemini-2.5-flash-image-preview`, Imagen 3)

### v0.1.0
- Initial release with Gemini image generation and editing

## License

MIT
