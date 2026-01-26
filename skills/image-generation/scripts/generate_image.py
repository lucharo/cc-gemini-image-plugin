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
    model: str = "gemini-3-pro-image-preview",
    resolution: str = "1K",
    aspect_ratio: str = "1:1",
    use_imagen: bool = False
) -> str:
    """
    Generate or edit an image using Gemini or Imagen 4.

    Args:
        prompt: Text description or editing instructions
        output_path: Where to save the result (default: output.png)
        input_image: Optional path to image to edit (not supported with Imagen)
        model: Model to use:
            - "gemini-3-pro-image-preview" (default) - Best quality, slower
            - "gemini-2.5-flash-image" - Good quality, faster
            - "imagen-4.0-generate-001" - Imagen 4 standard
            - "imagen-4.0-ultra-generate-001" - Imagen 4 ultra quality
            - "imagen-4.0-fast-generate-001" - Imagen 4 fast
        resolution: Output resolution - "1K", "2K", or "4K" (case-sensitive!)
        aspect_ratio: Output aspect ratio - "1:1", "3:4", "4:3", "9:16", "16:9"
        use_imagen: If True, use Imagen 4 API instead of Gemini

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

        >>> generate_image("A cat", use_imagen=True)
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

    # Use Imagen 4 API
    if use_imagen:
        if input_image:
            raise ValueError("Imagen 4 does not support image editing. Use Gemini models instead.")

        imagen_model = model if model.startswith("imagen-") else "imagen-4.0-generate-001"

        response = client.models.generate_images(
            model=imagen_model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            )
        )

        if response.generated_images:
            response.generated_images[0].image.save(output_path)
            return output_path

        raise ValueError("No image in response. The model may have refused due to safety filters. Try rephrasing your prompt.")

    # Use Gemini API
    contents = [prompt]
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
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Generate or edit images using Gemini")
    parser.add_argument("prompt", help="Text description or editing instructions")
    parser.add_argument("-o", "--output", default="output.png", help="Output path (default: output.png)")
    parser.add_argument("-i", "--input", help="Input image to edit (optional)")
    parser.add_argument("-m", "--model", default="gemini-3-pro-image-preview",
                        choices=["gemini-2.5-flash-image", "gemini-3-pro-image-preview",
                                 "imagen-4.0-generate-001", "imagen-4.0-ultra-generate-001",
                                 "imagen-4.0-fast-generate-001"],
                        help="Model to use (default: gemini-3-pro-image-preview)")
    parser.add_argument("-r", "--resolution", default="1K",
                        choices=["1K", "2K", "4K"],
                        help="Output resolution (default: 1K). Case-sensitive!")
    parser.add_argument("-a", "--aspect-ratio", default="1:1",
                        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
                        help="Output aspect ratio (default: 1:1)")
    parser.add_argument("--imagen", action="store_true",
                        help="Use Imagen 4 API instead of Gemini")

    args = parser.parse_args()

    result = generate_image(
        args.prompt,
        args.output,
        args.input,
        args.model,
        args.resolution,
        args.aspect_ratio,
        args.imagen
    )
    print(f"Saved to {result}")
