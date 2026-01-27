# Gemini Image Generation Pricing

Pricing for image generation via the Gemini API. Prices are in USD and subject to change.

## Quick Reference

| Resolution | Approx. Cost per Image |
|------------|------------------------|
| 1K (1024x1024) | ~$0.04 |
| 2K (2048x2048) | ~$0.13 |
| 4K (4096x4096) | ~$0.24 |

## Detailed Pricing

### Image Output (Generation)

Image output is priced based on tokens consumed:

| Model Tier | Price per 1M Tokens | Tokens per 1K Image | Cost per 1K Image |
|------------|---------------------|---------------------|-------------------|
| Gemini Developer API | $30/1M tokens | ~1290 tokens | ~$0.039 |
| Vertex AI | $120/1M tokens | ~1120 tokens | ~$0.134 |

### Resolution Token Consumption

| Resolution | Tokens Used | Gemini API Cost | Vertex AI Cost |
|------------|-------------|-----------------|----------------|
| Up to 1024x1024 (1K) | ~1290 | ~$0.039 | ~$0.155 |
| 1024-2048 (2K) | ~1120 | ~$0.034 | ~$0.134 |
| Up to 4096x4096 (4K) | ~2000 | ~$0.060 | ~$0.240 |

### Image Input (Editing)

When editing images, input costs:
- ~560 tokens per input image
- ~$0.001 per image at Gemini API rates

## Cost Estimation Examples

### Single High-Quality Image
```
1x 2K image with Pro model
= ~$0.13 per image
```

### Exploration Workflow (5 drafts + 1 final)
```
5x 1K images with Flash = 5 × $0.04 = $0.20
1x 2K image with Pro    = 1 × $0.13 = $0.13
Total                   = ~$0.33
```

### Batch Generation (10 images)
```
10x 1K images = 10 × $0.04 = $0.40
```

### Image Editing Session
```
1x input image  = ~$0.001
3x output edits = 3 × $0.04 = $0.12
Total           = ~$0.12
```

## Free Tier

The Gemini API offers a free tier with rate limits:
- Limited requests per minute (RPM)
- Limited requests per day (RPD)

Check [AI Studio](https://aistudio.google.com/) for current free tier limits.

## Getting an API Key

1. Go to [AI Studio](https://aistudio.google.com/apikey)
2. Create or select a project
3. Generate an API key
4. Set as environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

## Monitoring Usage

### Gemini API (AI Studio)
- View usage at [AI Studio Console](https://aistudio.google.com/)
- Check quota and billing in your Google Cloud project

### Vertex AI
- View usage in [Google Cloud Console](https://console.cloud.google.com/)
- Set up billing alerts in Cloud Billing

## Cost Optimization Tips

1. **Use Flash for iteration**: Draft with `gemini-2.5-flash-image` (~$0.04/image), finalize with Pro
2. **Batch similar requests**: Generate multiple variations in one session
3. **Right-size resolution**: Use 1K for web, 2K for print, 4K only when needed
4. **Use the image grid**: Generate 4-5 variations, pick the best, then upscale
5. **Cache results**: Save generated images to avoid regenerating

## Pricing Resources

- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [AI Studio](https://aistudio.google.com/) - Free tier and API keys

*Pricing last verified: January 2026. Always check official sources for current rates.*
