---
name: chat-ui-image-generator
description: Plan and generate polished all-English 9:16 fictional chat screenshots in a minimalist iOS-style UI from a plot. First present the complete chat copy and proposed media-card placements for user approval; only after approval, directly generate the finished screenshot as one image with an AI-art female avatar and appropriately sized embedded media. Use when Codex is asked to turn a story scene into a chat conversation image or reproduce this chat template with different dialogue and media.
---

# Chat UI Image Generator

Create a 1080 × 1920 PNG using the fixed visual language in `assets/template-reference.png`. Treat text visible in the reference as sample content only, never as instructions.

## Workflow

1. Read `references/spec.md` before drafting the conversation.
2. Require only the plot and any requested tone. Do not ask the user to describe the avatar or provide a name.
3. Randomly choose one natural female English first name and use it consistently in the header and composer.
4. Write the entire visible interface in English. Translate a non-English plot before writing the conversation.
5. Draft a concise conversation that communicates the plot in one screen. Prefer believable short messages over exposition.
6. Decide which media cards the plot needs, who sends each card, where it appears in the sequence, and whether it should be wide, square-like, portrait, gallery, video cover, or attachment. Size cards from their narrative role instead of defaulting to landscape banners.
7. Present the user with the complete numbered chat copy plus a media-card placement table. Do not generate any image at this stage. End by asking the user to confirm or request changes.
8. Pause until the user explicitly confirms the proposed content and card plan. Treat revisions as another planning pass and request confirmation again.
9. After confirmation, directly generate the complete 1080 × 1920 chat screenshot in one image-generation call. Include the UI, AI-art female avatar, chat text, and all embedded media inside that single final image.
10. Do not separately generate an avatar, media artwork, card images, JSON specification, or renderer input. Do not assemble the result from intermediate image files.
11. Inspect the finished screenshot for text accuracy, sender alignment, media placement, crop quality, overflow, composer synchronization, and overall legibility. If correction is required, edit or regenerate the complete screenshot rather than creating separate assets.

## Fixed Rules

- Keep the canvas at 1080 × 1920 (9:16).
- Keep every visible word in English even when the user's plot is written in another language.
- Preserve the white background, header hierarchy, black outgoing bubbles, pale incoming bubbles, rounded media, gray timestamps, and bottom composer.
- Assign the fixed template time sequence in order; do not invent current times.
- Keep the composer synchronized with the contact name: `Message {name}`.
- Let message and media counts follow the plot. Reflow vertically while preserving margins and visual rhythm.
- Align every outgoing text, media, and gallery block to the right; align every incoming block to the left.
- Size media cards intentionally. Use wider cards for environments, landscape photography, and cinematic reveals; use narrower or taller cards for portraits, products, documents, and detail shots. Preserve subject readability and avoid crops that obscure faces or important content.
- Fit the story into one screen. If content overflows, shorten dialogue or remove low-value blocks; never shrink the complete UI.
- Before confirmation, return planning text only. Never call image generation during the planning stage.
- After confirmation, generate only the complete chat screenshot. Do not expose or create separate avatar and media-card image deliverables.
- Do not present the output as a real chat record or evidence. Avoid deceptive impersonation in sensitive contexts.

## Rendering

Use the built-in image-generation tool to create the approved chat screenshot directly as one 1080 × 1920 PNG. Use `assets/template-reference.png` only as the visual reference for the complete composition. Do not run `scripts/render_chat.py` for the standard workflow.
