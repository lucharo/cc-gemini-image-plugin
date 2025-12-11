# CC Gemini Image Plugin

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/lucharo)

Generate and edit images using Google's Gemini image models (Nano Banana / Nano Banana Pro) in Claude Code.

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

## Usage

Once installed, simply ask Claude Code to generate or edit images:

- "Generate an image of a robot holding a banana"
- "Edit this image to make the background blue"
- "Apply the style from style.png to photo.jpg"
- "Create a watercolor painting of a sunset"

Claude will use the Gemini image API automatically.

### CLI Script

You can also use the helper script directly:

```bash
cd skills/image-generation/scripts

# Generate an image
uv run --with google-genai --with Pillow generate_image.py "A cat in a spacesuit" -o cat.png

# Edit an existing image
uv run --with google-genai --with Pillow generate_image.py "Make it blue" -i photo.jpg -o edited.png

# Use the Pro model for better quality
uv run --with google-genai --with Pillow generate_image.py "A sunset" -m gemini-3-pro-image-preview
```

## Models

| Model | Codename | Best For |
|-------|----------|----------|
| `gemini-2.5-flash-image` | Nano Banana | Fast iteration, drafts (default) |
| `gemini-3-pro-image-preview` | Nano Banana Pro | Final quality, text in images |

## Plugin Structure

```
cc-gemini-image-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── image-generation/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── generate_image.py
│       └── references/
│           ├── models.md
│           └── troubleshooting.md
└── README.md
```

## License

MIT
