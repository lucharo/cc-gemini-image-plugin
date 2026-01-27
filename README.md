# CC Gemini Image Plugin

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/lucharo)

A Claude Code plugin that lets you generate and edit images with Google's Gemini models. Ask for what you want in plain English and Claude handles the API calls.

## Installation

```bash
claude plugin marketplace add lucharo/cc-gemini-image-plugin
claude plugin install gemini-image@cc-gemini-image-plugin
```

Or run `/plugin` in Claude Code and find `gemini-image` in the Discover tab.

### Installing from a local clone

```bash
git clone https://github.com/lucharo/cc-gemini-image-plugin.git
claude plugin marketplace add /path/to/cc-gemini-image-plugin
claude plugin install gemini-image@cc-gemini-image-plugin
```

## Setup

You need a Gemini API key. Get one free at [AI Studio](https://aistudio.google.com/apikey).

```bash
export GEMINI_API_KEY="your-key-here"
```

`GOOGLE_API_KEY` works too. If you prefer Vertex AI, run `gcloud auth application-default login` and set `GOOGLE_CLOUD_PROJECT`.

No other dependencies to install. The scripts use `uv` to grab what they need on the fly.

## What it does

Text-to-image, image editing, style transfer, iterative refinement. You can keep a character or object looking consistent across multiple images. Output at 1K, 2K, or 4K in various aspect ratios. When you generate several variations, there's a grid selector to compare them side by side.

## Usage

Talk to Claude like normal:

- "Generate an image of a robot holding a banana"
- "Edit this image to make the background blue"
- "Apply the style from style.png to photo.jpg"
- "Create a watercolor painting of a sunset"
- "Generate 4 variations and show me a grid to choose from"

Claude picks the right model and handles the rest.

### Using the scripts directly

```bash
cd skills/image-generation/scripts

# generate
uv run --with google-genai --with Pillow generate_image.py "A cat in a spacesuit" -o cat.png

# edit an existing image
uv run --with google-genai --with Pillow generate_image.py "Make it blue" -i photo.jpg -o edited.png

# 2K panorama
uv run --with google-genai --with Pillow generate_image.py "A panorama" -o wide.png -r 2K -a 16:9
```

### Comparing variations

Generate a few options, then open them in a grid:

```bash
for i in 1 2 3 4; do
  uv run --with google-genai --with Pillow generate_image.py "A cozy cafe" -o cafe_$i.png -m gemini-2.5-flash-image
done

uv run image_grid.py cafe_*.png -o grid.html --open
```

Click the one you like and it copies a selection string you can paste back to Claude.

## Models

| Model | Use case | Resolution |
|-------|----------|------------|
| `gemini-3-pro-image-preview` | Final quality, text in images (default) | 1K-4K |
| `gemini-2.5-flash-image` | Quick iterations, drafts | 1K |

## Pricing

Rough cost per image:

| Resolution | Cost |
|------------|------|
| 1K (1024px) | ~$0.04 |
| 2K (2048px) | ~$0.13 |
| 4K (4096px) | ~$0.24 |

More details in `references/pricing.md`.

## Plugin structure

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
│           ├── workflows.md
│           └── troubleshooting.md
└── README.md
```

## Changelog

**v0.5.0** - Resolution auto-detected for cost calculation, plugin structure matches official Anthropic format, fixed install syntax

**v0.4.0** - `--refs` flag for reference images (character/object consistency), documented image limits

**v0.3.0** - Dropped Imagen 4, focused on Gemini models only

**v0.2.0** - Resolution and aspect ratio controls, image grid selector, pricing docs

**v0.1.0** - Initial release

## License

MIT
