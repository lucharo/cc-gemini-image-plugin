# Gemini Image Model Comparison

## Available Models

### gemini-3-pro-image-preview (Nano Banana Pro)

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
- Image editing and style transfer

### gemini-2.5-flash-image (Nano Banana)

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
- Testing prompts before using Pro

## Deprecated Models

| Model | Status | Replacement |
|-------|--------|-------------|
| `gemini-2.5-flash-image-preview` | Shut down | `gemini-2.5-flash-image` |

## Resolution Capabilities

| Model | 1K | 2K | 4K |
|-------|----|----|-----|
| gemini-3-pro-image-preview | Yes | Yes | Yes |
| gemini-2.5-flash-image | Yes | No | No |

**Important:** Resolution values are case-sensitive. Use `"2K"` not `"2k"`.

## Selection Guide

### Use Flash (gemini-2.5-flash-image) when:

1. **Iterating on concepts** - Generate 5-10 variations quickly
2. **Testing prompts** - See if your prompt works before using Pro
3. **Simple subjects** - Single objects, basic scenes
4. **No text needed** - Images without readable text
5. **Budget-conscious** - Lower API costs

### Use Pro (gemini-3-pro-image-preview) when:

1. **Final output** - The image will be used as-is
2. **Text in image** - Signs, logos, readable text
3. **Complex scenes** - Multiple subjects, detailed backgrounds
4. **High resolution needed** - Print or large display (2K-4K)
5. **Quality is priority** - Worth the extra time
6. **Consistency needed** - Character or object consistency
7. **Editing images** - Transform or modify existing images

## Recommended Workflow

Use a two-stage workflow for best results:

### Stage 1: Explore with Flash
```python
for variation in range(5):
    generate_image(
        f"A cozy cafe scene, variation {variation}",
        output_path=f"draft_{variation}.png",
        model="gemini-2.5-flash-image"
    )
```

### Stage 2: Finalize with Pro
```python
generate_image(
    "A cozy cafe scene with warm lighting and vintage decor",
    output_path="final.png",
    model="gemini-3-pro-image-preview",
    resolution="2K"
)
```

## Feature Comparison

| Feature | Flash | Pro |
|---------|-------|-----|
| Text-to-image | Yes | Yes |
| Image editing | Yes | Yes |
| Multi-turn chat | Yes | Yes |
| Character consistency | Limited | Up to 5 refs |
| Object consistency | Limited | Up to 6 refs |
| Style transfer | Yes | Yes |
| Google Search grounding | No | Yes |
| Aspect ratio control | Yes | Yes |
| Resolution control | 1K only | 1K-4K |

## API Naming

The models use codenames internally:
- "Nano Banana" = `gemini-2.5-flash-image`
- "Nano Banana Pro" = `gemini-3-pro-image-preview`

Always use the full model ID in code, not the codenames.
