# Gemini Image Model Comparison

## Available Models

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

### gemini-3-pro-image-preview (Nano Banana Pro)

**Best for:** Final output, text-heavy images, high-quality production work

| Attribute | Value |
|-----------|-------|
| Quality | Best |
| Speed | Slower |
| Resolution | 2K-4K |
| Text rendering | Excellent |
| Cost | Higher |

**When to use:**
- Final production images
- Images containing readable text
- Complex detailed scenes
- Professional/commercial output

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
4. **High resolution needed** - Print or large display
5. **Quality is priority** - Worth the extra time

## Workflow Recommendation

For best results, use a two-stage workflow:

1. **Explore with Flash**: Generate multiple variations quickly
2. **Refine with Pro**: Once you have a direction, use Pro for final quality

```python
# Stage 1: Quick exploration
for variation in range(5):
    generate_image(
        f"A cozy cafe scene, variation {variation}",
        output_path=f"draft_{variation}.png",
        model="gemini-2.5-flash-image"
    )

# Stage 2: Final quality
generate_image(
    "A cozy cafe scene with warm lighting and vintage decor",
    output_path="final.png",
    model="gemini-3-pro-image-preview"
)
```

## Resolution Notes

- **Flash (1K)**: ~1024x1024 pixels, good for web/screen use
- **Pro (2K-4K)**: Higher resolution, suitable for print

The actual output resolution may vary based on the prompt and content.

## API Naming

The models use codenames internally:
- "Nano Banana" = `gemini-2.5-flash-image`
- "Nano Banana Pro" = `gemini-3-pro-image-preview`

Always use the full model ID in code, not the codenames.
