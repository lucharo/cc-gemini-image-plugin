---
name: Gemini Image Generation
description: This skill should be used when the user asks to "generate an image", "create an image", "edit an image", "transform this image", "apply style to an image", "make a picture of", "create variations", or mentions "Gemini image", "Nano Banana", or any image generation/editing tasks. Provides guidance for using Google's Gemini image models.
version: 0.4.0
---

# Gemini Image Generation

Generate and edit images using Google's Gemini models.

## Quick Start

Use the helper script for most tasks:

```bash
# Generate an image
uv run --with google-genai --with Pillow \
  $CLAUDE_PLUGIN_ROOT/skills/image-generation/scripts/generate_image.py \
  "A robot holding a banana" -o robot.png

# Edit an existing image
uv run --with google-genai --with Pillow generate_image.py \
  "Make the background blue" -i photo.jpg -o edited.png

# High resolution with aspect ratio
uv run --with google-genai --with Pillow generate_image.py \
  "A panoramic landscape" -o wide.png -r 2K -a 16:9

# Fast iteration with Flash model
uv run --with google-genai --with Pillow generate_image.py \
  "Quick sketch" -o draft.png -m gemini-2.5-flash-image

# Character consistency with reference images
uv run --with google-genai --with Pillow generate_image.py \
  "Generate this character riding a bike" --refs char1.png char2.png -o biking.png
```

Or import in Python:

```python
from generate_image import generate_image

generate_image("A sunset over mountains", output_path="sunset.png")
generate_image("Add clouds", input_image="sunset.png", output_path="cloudy.png")
generate_image("Wide shot", resolution="2K", aspect_ratio="16:9")
```

## Authentication

Set one of these:

```bash
# Option 1: API Key (recommended)
export GEMINI_API_KEY="your-key-from-aistudio.google.com"
# GOOGLE_API_KEY also works

# Option 2: Vertex AI
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud auth application-default login
```

## Models

| Model | Best For | Resolution |
|-------|----------|------------|
| `gemini-3-pro-image-preview` | Quality, text rendering (default) | 1K-4K |
| `gemini-2.5-flash-image` | Speed, prototyping | 1K |

**Deprecated:** `gemini-2.5-flash-image-preview`

See `references/models.md` for detailed comparison.

## Core API Pattern

When writing custom code, always include `response_modalities`:

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A serene Japanese garden at sunset",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # 1:1, 3:4, 4:3, 9:16, 16:9
            image_size="2K"       # 1K, 2K, 4K (case-sensitive!)
        )
    )
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("output.png")
    elif part.text:
        print(part.text)
```

## Image Editing

```python
from PIL import Image

input_img = Image.open("photo.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Transform into watercolor style", input_img],
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)
```

## Reference Images

Use reference images for consistency across generations:

| Use Case | Max References |
|----------|----------------|
| Character consistency | Up to 5 images |
| Object consistency | Up to 6 images |
| Style transfer | 1-2 images |
| Image editing | 1 image |

```bash
# CLI with --refs
uv run ... generate_image.py "This character in a forest" \
  --refs char1.png char2.png char3.png -o forest_scene.png
```

```python
# Python API
generate_image(
    "Generate this character cooking dinner",
    reference_images=["char_front.png", "char_side.png"],
    output_path="cooking.png"
)
```

## Multi-turn Chat

For iterative refinement:

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)

response = chat.send_message("Create a cozy coffee shop")
# Save image...
response = chat.send_message("Add rain on the windows")
# Save refined image...
```

## Multi-Image Selection

When generating variations, use the image grid selector.

**IMPORTANT:** Always use `--open` to automatically open the grid in the user's browser.

```bash
# Generate 4 variations with Flash (fast)
for i in 1 2 3 4; do
  uv run ... generate_image.py "A cafe, variation $i" -o /tmp/cafe_$i.png -m gemini-2.5-flash-image
done

# Create clickable grid and open in browser
uv run $CLAUDE_PLUGIN_ROOT/skills/image-generation/scripts/image_grid.py \
  /tmp/cafe_*.png -o /tmp/grid.html --open
```

The grid opens automatically. User clicks preferred image to copy selection text, then pastes back to continue.

See `references/workflows.md` for complete workflow examples.

## Prompt Tips

- **Be specific**: colors, materials, lighting, mood, style
- **Specify style**: "photorealistic", "oil painting", "anime", "watercolor"
- **For text in images**: Use Pro model - much better text rendering
- **For edits**: Be explicit about what to change and preserve

## Common Issues

| Issue | Solution |
|-------|----------|
| No image returned | Safety filter triggered - rephrase prompt |
| "responseModalities required" | Add `response_modalities=['TEXT', 'IMAGE']` to config |
| Model not found | Check for deprecated models |
| Resolution not working | Use uppercase: `"2K"` not `"2k"` |

See `references/troubleshooting.md` for more.

## Pricing

| Resolution | ~Cost/Image |
|------------|-------------|
| 1K | $0.04 |
| 2K | $0.13 |
| 4K | $0.24 |

See `references/pricing.md` for details.

## References

- `references/models.md` - Model comparison
- `references/pricing.md` - Costs and optimization
- `references/troubleshooting.md` - Common issues
- `references/workflows.md` - Multi-image, consistency workflows
- `scripts/generate_image.py` - Helper function
- `scripts/image_grid.py` - Grid selector
