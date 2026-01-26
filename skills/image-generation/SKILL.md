---
name: Gemini Image Generation
description: This skill should be used when the user asks to "generate an image", "create an image", "edit an image", "transform this image", "apply style to an image", "make a picture of", "create variations", "upscale image", or mentions "Gemini image", "Nano Banana", "Imagen", or any image generation/editing tasks. Provides guidance for using Google's Gemini image models and Imagen 4.
version: 0.2.0
---

# Gemini Image Generation

Generate and edit images using Google's Gemini models and Imagen 4.

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

# Use Imagen 4 for standalone generation
uv run --with google-genai --with Pillow generate_image.py \
  "A photorealistic cat" -o cat.png --imagen
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

# Option 2: Vertex AI
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud auth application-default login
```

## Models

| Model | Best For | Resolution |
|-------|----------|------------|
| `gemini-3-pro-image-preview` | Quality, text rendering | 1K-4K |
| `gemini-2.5-flash-image` | Speed, prototyping | 1K |
| `imagen-4.0-generate-001` | Standalone generation | 1K-2K |
| `imagen-4.0-ultra-generate-001` | Highest quality | 1K-2K |
| `imagen-4.0-fast-generate-001` | Fast iteration | 1K-2K |

**Deprecated:** `gemini-2.5-flash-image-preview`, Imagen 3 models

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

## Imagen 4 API

For standalone generation without conversation:

```python
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A golden retriever in autumn leaves",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9"
    )
)

for img in response.generated_images:
    img.image.save("output.png")
```

**Note:** Imagen 4 doesn't support editing - use Gemini models for that.

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

When generating variations, use the image grid selector:

```bash
# Generate 4 variations
for i in 1 2 3 4; do
  uv run ... generate_image.py "A cafe, variation $i" -o /tmp/cafe_$i.png -m gemini-2.5-flash-image
done

# Create clickable grid
uv run $CLAUDE_PLUGIN_ROOT/skills/image-generation/scripts/image_grid.py \
  /tmp/cafe_*.png -o /tmp/grid.html --open
```

Click preferred image to copy selection text, paste back to continue.

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
