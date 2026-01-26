# Troubleshooting Gemini Image Generation

## Authentication Issues

### "Could not find default credentials"

**Cause:** Application Default Credentials (ADC) not configured.

**Solution:**
```bash
gcloud auth application-default login
```

This opens a browser for Google authentication and saves credentials locally.

### "API key not valid"

**Cause:** Invalid or expired API key.

**Solutions:**
1. Get a new key at https://aistudio.google.com/apikey
2. Verify the key is set correctly:
   ```bash
   echo $GEMINI_API_KEY
   ```
3. Ensure no extra whitespace in the key

### "Permission denied" or quota errors

**Cause:** API key lacks permissions or quota exceeded.

**Solutions:**
1. Check your quota at Google Cloud Console
2. Request quota increase if needed
3. Use ADC instead of API key for higher limits

## Model and API Issues

### "Model not found" or "Unknown model"

**Cause:** Using a deprecated or invalid model name.

**Solutions:**
1. Check for deprecated models:
   - `gemini-2.5-flash-image-preview` is shut down - use `gemini-2.5-flash-image`
   - Imagen 3 models are deprecated - use Imagen 4
2. Verify correct model spelling
3. Check the models.md reference for current model names

### "responseModalities required" or similar config error

**Cause:** Missing required configuration for image generation.

**Solution:** Always include `response_modalities` in your config:

```python
from google.genai import types

config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE']  # Required!
)

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Your prompt",
    config=config
)
```

### Imagen 3 models not working

**Cause:** Imagen 3 has been shut down and replaced by Imagen 4.

**Solution:** Update your code to use Imagen 4 models:
- `imagen-3.0-generate-001` -> `imagen-4.0-generate-001`
- `imagen-3.0-fast-generate-001` -> `imagen-4.0-fast-generate-001`

### Resolution parameter not working

**Cause:** Resolution values are case-sensitive.

**Solution:** Use uppercase: `"1K"`, `"2K"`, `"4K"` (not `"1k"`, `"2k"`, `"4k"`)

```python
config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],
    image_config=types.ImageConfig(
        image_size="2K"  # Correct - uppercase
    )
)
```

## No Image in Response

### Model returns text instead of image

**Cause:** Safety filters triggered or prompt unclear.

**Solutions:**
1. **Rephrase the prompt** - Avoid potentially sensitive content
2. **Be more specific** - Vague prompts may get clarifying questions
3. **Check the text response** - It may explain why no image was generated

```python
for part in response.parts:
    if part.inline_data is not None:
        # Got an image
        image = part.as_image()
        image.save("output.png")
    elif part.text:
        # Model returned text - read it!
        print(f"Model says: {part.text}")
```

### Empty response

**Cause:** Request failed silently.

**Solutions:**
1. Check network connectivity
2. Verify model name is correct
3. Try a simpler prompt to test
4. Ensure `response_modalities` is set

## Performance Issues

### Slow generation

**Causes and solutions:**

| Cause | Solution |
|-------|----------|
| Using Pro model | Switch to Flash or Imagen Fast for faster results |
| High resolution | Use 1K instead of 2K/4K |
| Complex prompt | Simplify the prompt |
| Network latency | Check connection speed |
| API load | Retry after a few seconds |

### Timeout errors

**Solution:** Increase timeout or use async:

```python
# The SDK handles timeouts internally
# For very long operations, consider async patterns
import asyncio

async def generate_async():
    # Use async client if available
    pass
```

## Image Quality Issues

### Low resolution output

**Solutions:**
1. Use `gemini-3-pro-image-preview` for higher resolution
2. Explicitly set resolution in config:
   ```python
   image_config=types.ImageConfig(image_size="2K")
   ```
3. Be specific about quality in prompt: "high detail", "4K quality"
4. Avoid conflicting style instructions

### Text not rendering clearly

**Solutions:**
1. Use `gemini-3-pro-image-preview` - much better at text
2. Keep text short and simple
3. Specify text placement: "text centered at the top"
4. Use high-contrast colors for text

### Style not matching expectations

**Solutions:**
1. Be explicit about style: "photorealistic", "oil painting", "3D render"
2. Reference specific art styles or artists (where appropriate)
3. Include multiple style descriptors: "watercolor, soft colors, dreamy"

## Input Image Issues

### "Cannot open image" errors

**Causes and solutions:**

| Cause | Solution |
|-------|----------|
| File not found | Check file path exists |
| Unsupported format | Convert to PNG or JPEG |
| Corrupted file | Re-save the image |
| File too large | Resize before uploading |

### Edit not applied correctly

**Solutions:**
1. Be very specific about what to change
2. Describe what to preserve: "Keep the person, change only the background"
3. Use clear directional language: "Add a hat ON the person's head"

### Imagen doesn't support editing

**Cause:** Imagen 4 models only support generation, not editing.

**Solution:** Use Gemini models for image editing:
```python
# This won't work with Imagen
# generate_image("Edit this", input_image="photo.jpg", use_imagen=True)

# Use Gemini instead
generate_image("Edit this", input_image="photo.jpg", model="gemini-3-pro-image-preview")
```

## Multi-Image Issues

### Style transfer not working

**Solutions:**
1. Clearly identify which image is subject vs style
2. Use explicit language: "Apply the style FROM the second image TO the first"
3. Ensure style reference has distinctive characteristics

### Images getting confused

**Solutions:**
1. Reference images by order: "first image", "second image"
2. Describe each image's role in the prompt
3. Process one operation at a time for complex tasks

### Too many reference images

**Limits:**
- Character consistency: up to 5 reference images
- Object consistency: up to 6 reference images

**Solution:** Select the most representative reference images within the limit.

## Chat/Multi-turn Issues

### Context lost between turns

**Note:** Each turn in a chat maintains context, but be explicit:

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

# Be explicit about referencing previous generations
response = chat.send_message("Create a house")
# ... save image ...

response = chat.send_message("Add a garden to the house you just created")
# ... save refined image ...
```

### Iterative edits not accumulating

**Solutions:**
1. Reference previous state: "Keep all changes so far and also add..."
2. Be specific about what to preserve
3. Consider regenerating from scratch if edits conflict

## Dependency Issues

### ModuleNotFoundError: google.genai

**Solution:**
```bash
pip install google-genai
```

### ModuleNotFoundError: PIL

**Solution:**
```bash
pip install pillow
```

### Version conflicts

**Solution:** Create a clean virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install google-genai pillow
```

Or use uv for isolated execution:
```bash
uv run --with google-genai --with Pillow script.py
```

## Getting Help

If issues persist:
1. Check Google AI documentation: https://ai.google.dev/docs
2. Review API status: https://status.cloud.google.com/
3. Verify your Google Cloud project settings
4. Check the models.md reference for current model information
