#!/usr/bin/env -S uv run --with google-genai --with Pillow
"""
Gemini Image Generation Helper

A reusable function for generating and editing images using Google's Gemini models.

Run directly:
    uv run --with google-genai --with Pillow generate_image.py "A robot holding a banana"

Or import in a script:
    # /// script
    # dependencies = ["google-genai", "Pillow"]
    # ///
    from generate_image import generate_image
    generate_image("A robot holding a banana")
"""

from google import genai
from google.genai import types
from PIL import Image
from pathlib import Path
import os


def generate_image(
    prompt: str,
    output_path: str = "output.png",
    input_image: str | None = None,
    reference_images: list[str] | None = None,
    model: str = "gemini-3-pro-image-preview",
    resolution: str = "1K",
    aspect_ratio: str = "1:1",
) -> str:
    """
    Generate or edit an image using Gemini.

    Args:
        prompt: Text description or editing instructions
        output_path: Where to save the result (default: output.png)
        input_image: Optional path to image to edit (single image)
        reference_images: Optional list of reference image paths for consistency
            - Character consistency: up to 5 images
            - Object consistency: up to 6 images
            - Style transfer: 1-2 images
        model: Model to use:
            - "gemini-3-pro-image-preview" (default) - Best quality
            - "gemini-2.5-flash-image" - Faster, good for drafts
        resolution: Output resolution - "1K", "2K", or "4K" (case-sensitive!)
        aspect_ratio: Output aspect ratio - "1:1", "3:4", "4:3", "9:16", "16:9"

    Returns:
        Path to saved image

    Raises:
        ValueError: If no image in response (may indicate safety filter)

    Examples:
        >>> generate_image("A serene mountain landscape at dawn")
        'output.png'

        >>> generate_image("Add a red hat", input_image="person.jpg", output_path="with_hat.png")
        'with_hat.png'

        >>> generate_image("A panorama", resolution="2K", aspect_ratio="16:9")
        'output.png'

        >>> generate_image(
        ...     "Generate this character riding a bike",
        ...     reference_images=["char1.png", "char2.png", "char3.png"]
        ... )
        'output.png'
    """
    # Initialize client
    # Priority: GEMINI_API_KEY > Vertex AI (ADC with project/location)
    api_key = os.environ.get("GEMINI_API_KEY")
    project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if api_key:
        client = genai.Client(api_key=api_key)
    elif project:
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        raise ValueError(
            "No authentication configured. Set either:\n"
            "  - GEMINI_API_KEY (from aistudio.google.com)\n"
            "  - GOOGLE_CLOUD_PROJECT (for Vertex AI with ADC)"
        )

    # Build contents
    contents = [prompt]

    # Add reference images first (for consistency workflows)
    if reference_images:
        for ref_path in reference_images:
            contents.append(Image.open(ref_path))

    # Add input image (for editing)
    if input_image:
        contents.append(Image.open(input_image))

    # Build config with response_modalities (required) and image_config
    config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        )
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )

    # Process response
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(output_path)
            return output_path
        elif part.text:
            # Model returned text (might be a clarification or refusal)
            print(f"Model response: {part.text}")

    raise ValueError("No image in response. The model may have refused due to safety filters. Try rephrasing your prompt.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate or edit images using Gemini")
    parser.add_argument("prompt", help="Text description or editing instructions")
    parser.add_argument("-o", "--output", default="output.png", help="Output path (default: output.png)")
    parser.add_argument("-i", "--input", help="Input image to edit (optional)")
    parser.add_argument("--refs", nargs="+", metavar="IMG",
                        help="Reference images for consistency (character: up to 5, object: up to 6)")
    parser.add_argument("-m", "--model", default="gemini-3-pro-image-preview",
                        choices=["gemini-2.5-flash-image", "gemini-3-pro-image-preview"],
                        help="Model to use (default: gemini-3-pro-image-preview)")
    parser.add_argument("-r", "--resolution", default="1K",
                        choices=["1K", "2K", "4K"],
                        help="Output resolution (default: 1K). Case-sensitive!")
    parser.add_argument("-a", "--aspect-ratio", default="1:1",
                        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
                        help="Output aspect ratio (default: 1:1)")

    args = parser.parse_args()

    result = generate_image(
        args.prompt,
        args.output,
        args.input,
        args.refs,
        args.model,
        args.resolution,
        args.aspect_ratio,
    )
    print(f"Saved to {result}")
