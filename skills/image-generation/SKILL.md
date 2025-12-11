---
name: Gemini Image Generation
description: This skill should be used when the user asks to "generate an image", "create an image", "edit an image", "transform this image", "apply style to an image", "make a picture of", or mentions "Gemini image", "Nano Banana", or image generation/editing tasks. Provides comprehensive guidance for using Google's Gemini image models.
version: 0.1.0
---

# Gemini Image Generation

Generate and edit images using Google's Gemini image models (Nano Banana / Nano Banana Pro).

## Authentication

Two authentication options are available:

### Application Default Credentials (Recommended)

```bash
gcloud auth application-default login
```

Initialize without an API key:

```python
from google import genai
client = genai.Client()
```

### API Key

Set the environment variable:

```bash
export GEMINI_API_KEY="your-key-from-aistudio.google.com"
```

Initialize with the key:

```python
from google import genai
import os
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
```

## Dependencies

Use `uv` for inline dependency management (no global install needed):

```bash
uv run --with google-genai --with Pillow script.py
```

Or add inline metadata to scripts:

```python
# /// script
# dependencies = ["google-genai", "Pillow"]
# ///
```

Then run with just `uv run script.py`.

## Models

| Model | Codename | Quality | Speed |
|-------|----------|---------|-------|
| `gemini-2.5-flash-image` | Nano Banana | Good | Fast |
| `gemini-3-pro-image-preview` | Nano Banana Pro | Best | Slower |

Default to `gemini-3-pro-image-preview` for best quality. Use `gemini-2.5-flash-image` when speed matters or for rapid iteration.

For detailed model comparison, see `references/models.md`.

## Core Patterns

### Text-to-Image Generation

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A serene Japanese garden at sunset with cherry blossoms"
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
    elif part.text:
        print(part.text)
```

### Image Editing

Transform or edit an existing image with a text prompt:

```python
from google import genai
from PIL import Image

client = genai.Client()
input_image = Image.open("input.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Transform this image into a watercolor painting style",
        input_image
    ]
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("edited.png")
```

### Multi-Image Composition

Combine multiple images or transfer style:

```python
from google import genai
from PIL import Image

client = genai.Client()

subject = Image.open("person.png")
style_ref = Image.open("art_style.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Apply the artistic style from the second image to the person in the first image",
        subject,
        style_ref
    ]
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("styled.png")
```

### Iterative Editing (Multi-turn Chat)

For conversational refinement:

```python
from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-3-pro-image-preview")

# First generation
response = chat.send_message("Create a cozy coffee shop interior")
# Save first image...

# Refine
response = chat.send_message("Add rain on the windows and warm lighting")
# Save refined image...

# Continue iterating
response = chat.send_message("Now add a cat sleeping on one of the chairs")
```

## Helper Script

A reusable helper function is available at `$CLAUDE_PLUGIN_ROOT/skills/image-generation/scripts/generate_image.py`.

Usage:

```python
from generate_image import generate_image

# Text-to-image
generate_image("A robot holding a banana", output_path="robot.png")

# Edit existing image
generate_image(
    "Make the background blue",
    input_image="photo.jpg",
    output_path="edited.png"
)

# Use faster model for iteration
generate_image(
    "Quick sketch of a cat",
    model="gemini-2.5-flash-image"
)
```

Alternatively, copy the function directly into the user's code.

## Prompt Tips

- **Be specific**: Include colors, materials, lighting, mood, style
- **Specify style**: "photorealistic", "oil painting", "3D render", "anime", "watercolor"
- **For text in images**: Nano Banana Pro renders text much better than Flash
- **For edits**: Be explicit about what to change and what to preserve

## Common Issues

For detailed troubleshooting, see `references/troubleshooting.md`.

Quick fixes:
- **"Could not find default credentials"**: Run `gcloud auth application-default login`
- **"API key not valid"**: Check key at https://aistudio.google.com/apikey
- **No image in response**: Model may have refused due to safety filters—try rephrasing
- **Slow generation**: Switch to `gemini-2.5-flash-image`

## Response Handling

Always iterate through `response.parts` to handle both image and text responses:

```python
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
        print(f"Saved image to output.png")
    elif part.text:
        print(f"Model response: {part.text}")
```

The model may return text alongside or instead of images (e.g., clarifying questions or refusals).

## Additional Resources

### Reference Files

- **`references/models.md`** - Detailed model comparison and selection guidance
- **`references/troubleshooting.md`** - Common issues and solutions

### Scripts

- **`scripts/generate_image.py`** - Reusable helper function for generation and editing
