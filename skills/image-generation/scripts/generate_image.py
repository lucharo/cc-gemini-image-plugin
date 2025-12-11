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
from PIL import Image
from pathlib import Path
import os


def generate_image(
    prompt: str,
    output_path: str = "output.png",
    input_image: str | None = None,
    model: str = "gemini-3-pro-image-preview"
) -> str:
    """
    Generate or edit an image using Gemini.

    Args:
        prompt: Text description or editing instructions
        output_path: Where to save the result (default: output.png)
        input_image: Optional path to image to edit
        model: Model to use:
            - "gemini-3-pro-image-preview" (default) - Best quality, slower
            - "gemini-2.5-flash-image" - Good quality, faster

    Returns:
        Path to saved image

    Raises:
        ValueError: If no image in response (may indicate safety filter)

    Examples:
        >>> generate_image("A serene mountain landscape at dawn")
        'output.png'

        >>> generate_image("Add a red hat", input_image="person.jpg", output_path="with_hat.png")
        'with_hat.png'
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

    # Build contents list
    contents = [prompt]
    if input_image:
        contents.append(Image.open(input_image))

    # Generate
    response = client.models.generate_content(
        model=model,
        contents=contents
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
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Generate or edit images using Gemini")
    parser.add_argument("prompt", help="Text description or editing instructions")
    parser.add_argument("-o", "--output", default="output.png", help="Output path (default: output.png)")
    parser.add_argument("-i", "--input", help="Input image to edit (optional)")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash-image",
                        choices=["gemini-2.5-flash-image", "gemini-3-pro-image-preview"],
                        help="Model to use (default: gemini-2.5-flash-image)")

    args = parser.parse_args()

    result = generate_image(args.prompt, args.output, args.input, args.model)
    print(f"Saved to {result}")
