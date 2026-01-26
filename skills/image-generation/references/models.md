# Gemini Image Model Comparison

## Available Models

### Gemini Models (Conversational)

These models support text-to-image, image editing, and multi-turn conversations.

#### gemini-2.5-flash-image (Nano Banana)

**Best for:** Rapid prototyping, iteration, speed-critical applications

| Attribute | Value |
|-----------|-------|
| Quality | Good |
| Speed | Fast |
| Resolution | 1K |
| Text rendering | Basic |
| Cost | Lower |

**When to use:**
- Quick iterations during creative exploration
- Generating many variations to choose from
- Speed is more important than maximum quality
- Simple compositions without text

#### gemini-3-pro-image-preview (Nano Banana Pro)

**Best for:** Final output, text-heavy images, high-quality production work

| Attribute | Value |
|-----------|-------|
| Quality | Best |
| Speed | Slower |
| Resolution | 1K-4K |
| Text rendering | Excellent |
| Cost | Higher |

**When to use:**
- Final production images
- Images containing readable text
- Complex detailed scenes
- Professional/commercial output
- Character/object consistency workflows

### Imagen 4 Models (Standalone Generation)

These models use the `generate_images` API and are optimized for standalone generation without conversation.

#### imagen-4.0-generate-001

**Best for:** Standard quality standalone generation

| Attribute | Value |
|-----------|-------|
| Quality | High |
| Speed | Medium |
| Resolution | 1K-2K |
| Text rendering | Good |
| Editing | Not supported |

#### imagen-4.0-ultra-generate-001

**Best for:** Highest quality output

| Attribute | Value |
|-----------|-------|
| Quality | Highest |
| Speed | Slower |
| Resolution | 1K-2K |
| Text rendering | Excellent |
| Editing | Not supported |

#### imagen-4.0-fast-generate-001

**Best for:** Fast iteration, batch generation

| Attribute | Value |
|-----------|-------|
| Quality | Good |
| Speed | Fastest |
| Resolution | 1K-2K |
| Text rendering | Good |
| Editing | Not supported |

## Deprecated Models (Do Not Use)

| Model | Status | Replacement |
|-------|--------|-------------|
| `gemini-2.5-flash-image-preview` | Shut down | `gemini-2.5-flash-image` |
| `imagen-3.0-generate-001` | Deprecated | `imagen-4.0-generate-001` |
| `imagen-3.0-fast-generate-001` | Deprecated | `imagen-4.0-fast-generate-001` |

## Resolution Capabilities

| Model | 1K | 2K | 4K |
|-------|----|----|-----|
| gemini-2.5-flash-image | Yes | No | No |
| gemini-3-pro-image-preview | Yes | Yes | Yes |
| imagen-4.0-generate-001 | Yes | Yes | No |
| imagen-4.0-ultra-generate-001 | Yes | Yes | No |
| imagen-4.0-fast-generate-001 | Yes | Yes | No |

**Important:** Resolution values are case-sensitive. Use `"2K"` not `"2k"`.

## Selection Guide

### Use Gemini Flash (gemini-2.5-flash-image) when:

1. **Iterating on concepts** - Generate 5-10 variations quickly
2. **Testing prompts** - See if your prompt works before using Pro
3. **Simple subjects** - Single objects, basic scenes
4. **No text needed** - Images without readable text
5. **Budget-conscious** - Lower API costs

### Use Gemini Pro (gemini-3-pro-image-preview) when:

1. **Final output** - The image will be used as-is
2. **Text in image** - Signs, logos, readable text
3. **Complex scenes** - Multiple subjects, detailed backgrounds
4. **High resolution needed** - Print or large display (2K-4K)
5. **Quality is priority** - Worth the extra time
6. **Consistency needed** - Character or object consistency with reference images
7. **Editing images** - Transform or modify existing images

### Use Imagen 4 when:

1. **No conversation needed** - Standalone single-prompt generation
2. **Batch generation** - Multiple images from same prompt
3. **API simplicity** - Dedicated image generation endpoint
4. **Person generation control** - Need fine-grained control over people in images

## Workflow Recommendations

### For best results, use a multi-stage workflow:

#### Quick Exploration (Flash)
```python
for variation in range(5):
    generate_image(
        f"A cozy cafe scene, variation {variation}",
        output_path=f"draft_{variation}.png",
        model="gemini-2.5-flash-image"
    )
```

#### Final Quality (Pro)
```python
generate_image(
    "A cozy cafe scene with warm lighting and vintage decor",
    output_path="final.png",
    model="gemini-3-pro-image-preview",
    resolution="2K"
)
```

#### Batch Standalone (Imagen 4)
```python
# When you need multiple independent images
for subject in ["cat", "dog", "bird"]:
    generate_image(
        f"A photorealistic {subject} portrait",
        output_path=f"{subject}.png",
        use_imagen=True
    )
```

## API Naming

The models use codenames internally:
- "Nano Banana" = `gemini-2.5-flash-image`
- "Nano Banana Pro" = `gemini-3-pro-image-preview`

Always use the full model ID in code, not the codenames.

## Feature Comparison

| Feature | Gemini Flash | Gemini Pro | Imagen 4 |
|---------|--------------|------------|----------|
| Text-to-image | Yes | Yes | Yes |
| Image editing | Yes | Yes | No |
| Multi-turn chat | Yes | Yes | No |
| Character consistency | Limited | Up to 5 refs | No |
| Object consistency | Limited | Up to 6 refs | No |
| Style transfer | Yes | Yes | No |
| Google Search grounding | No | Yes | No |
| Aspect ratio control | Yes | Yes | Yes |
| Resolution control | 1K only | 1K-4K | 1K-2K |
