# Image Generation Workflows

Common workflows for generating and selecting images.

## Multi-Image Selection Workflow

When generating multiple variations, use the image grid selector for easy comparison.

### 1. Generate Variations

```bash
# Quick variations with Flash model
for i in 1 2 3 4; do
  uv run --with google-genai --with Pillow generate_image.py \
    "A cozy cafe, variation $i" -o /tmp/cafe_$i.png -m gemini-2.5-flash-image
done
```

Or in Python:

```python
from generate_image import generate_image

for i in range(4):
    generate_image(
        f"A mountain landscape, variation {i+1}",
        output_path=f"/tmp/mountain_{i+1}.png",
        model="gemini-2.5-flash-image"
    )
```

### 2. Create Selection Grid

```bash
uv run ~/.claude/plugins/gemini-image/skills/image-generation/scripts/image_grid.py \
    /tmp/cafe_*.png -o /tmp/grid.html --open
```

This opens a browser with clickable images. Click your preferred image to copy selection text.

### 3. Refine Selection

Paste the copied text back to Claude, then regenerate at higher quality:

```python
generate_image(
    "A cozy cafe, variation 2",  # User's choice
    output_path="final_cafe.png",
    model="gemini-3-pro-image-preview",
    resolution="2K"
)
```

### Grid Script Options

```bash
# Basic
uv run image_grid.py image1.png image2.png -o grid.html

# Open in browser automatically
uv run image_grid.py *.png -o grid.html --open

# Custom copy text
uv run image_grid.py *.png -o grid.html --copy-format "Use {filename}"

# File paths instead of embedding (smaller HTML)
uv run image_grid.py *.png -o grid.html --no-embed
```

**Copy format variables:** `{label}`, `{filename}`, `{path}`

## Character Consistency Workflow

Maintain consistent characters across multiple images.

### 1. Prepare Reference Images

Gather 3-5 images of your character from different angles.

### 2. Generate with References

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

refs = [Image.open(f"char_{i}.png") for i in range(1, 4)]

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Generate this character riding a bicycle. "
        "Maintain same appearance, clothing, and features.",
        *refs
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)
```

**Tips:**
- Use 3-5 reference images from different angles
- Describe distinctive features in prompt
- Reference specific clothing/accessories to preserve

## Object Consistency Workflow

Keep products/objects consistent across scenes.

```python
product_refs = [Image.open(f"product_{i}.png") for i in range(1, 5)]

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Show this product on a kitchen counter with morning light. "
        "Maintain exact design, colors, and branding.",
        *product_refs
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)
```

**Limits:** Up to 6 reference images for objects.

## Batch Generation Workflow

Generate many images efficiently.

### Using Imagen 4 (fastest for standalone)

```python
from generate_image import generate_image

subjects = ["cat", "dog", "bird", "rabbit"]
for subject in subjects:
    generate_image(
        f"A photorealistic {subject} portrait",
        output_path=f"{subject}.png",
        use_imagen=True
    )
```

### Two-Stage Workflow

1. **Explore** with Flash (fast, cheap)
2. **Finalize** with Pro (quality)

```python
# Stage 1: Quick drafts
for i in range(5):
    generate_image(prompt, output_path=f"draft_{i}.png", model="gemini-2.5-flash-image")

# Stage 2: Final quality
generate_image(prompt, output_path="final.png", model="gemini-3-pro-image-preview", resolution="2K")
```

## Style Transfer Workflow

Apply artistic style from one image to another.

```python
subject = Image.open("photo.png")
style = Image.open("art_style.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Apply the artistic style from the second image to the subject in the first image",
        subject,
        style
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)
```

**Tips:**
- Clearly identify subject vs style image
- Use explicit language: "Apply style FROM second TO first"
- Ensure style reference has distinctive characteristics
