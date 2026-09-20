# Practical Insights: Hybrid Local/Cloud Image Generation Pipeline

*Knowledge base entry #47 | Author: Fleet Ops | Last updated: 2024-05-18*

---

## 1. Model Selection: SD 1.5 Is a Workhorse, Not a Showhorse

On a 6GB GPU, SD 1.5 checkpoints are your bread and butter—but only if you treat them as *style engines*, not as universal generators. The sweet spot is **photorealistic base models** (e.g., Realistic Vision, deliberate v2) for product mockups and environments, and **stylized anime/illustration checkpoints** only when the brief explicitly demands it. Avoid mixing base models mid-pipeline; the latent space drift will cost you more in re-rolls than you save in compute.

**Key rule:** Test a new checkpoint with a fixed prompt set of 10 canonical images (portrait, landscape, object, scene, texture). If it fails on 3+, archive it.

---

## 2. LoRA Stacking: Less Is More, Order Matters

We run LoRAs at 0.6–0.8 strength, never 1.0. Stacking more than 2 LoRAs on SD 1.5 produces "LoRA soup"—mushy textures and identity bleed. The practical sequence:

1. **Base style LoRA** (e.g., "film grain" or "concept art") at 0.7.
2. **Subject/object LoRA** (e.g., "cyberpunk vehicle" or "specific character") at 0.8.

Never stack two subject LoRAs. Instead, generate the subject, then inpaint the style second. On a 6GB card, batch size 1, 30 steps, 512×512 is your comfort zone; push to 768 only for hero shots.

---

## 3. Prompt Engineering: The "Noun-Verb-Context" Sandwich

Our most reliable pattern for both SD 1.5 and FLUX:

- **Layer 1 (Subject):** 3–5 concrete nouns with descriptors (e.g., "weathered brass steampunk owl, intricate gears")
- **Layer 2 (Action/State):** one verb + state ("perched on a mossy stone, wings slightly spread")
- **Layer 3 (Environment/Lighting):** 2–3 context cues ("foggy dawn, volumetric light, shallow depth of field")

**Negative prompts matter more locally than in cloud.** For SD 1.5, always include: `blurry, deformed, extra limbs, watermark, text`. For FLUX, skip the negative prompt—it handles it natively and you'll waste tokens.

---

## 4. Cloud vs. Local: The 80/20 Rule

We use **local for iteration, cloud for finalization**. Concretely:

- **Local (SD 1.5):** rapid concept exploration, style tests, LoRA tuning, batch variations. You get 10 images in the time FLUX gives you 2.
- **Cloud (FLUX via DeepInfra):** final hero images, high-res (1024+), complex compositions with multiple subjects, or when you need photorealistic lighting that SD 1.5 just can't do.

**Pragmatic trigger:** if you've spent more than 15 minutes fighting SD 1.5 for a single image, switch to FLUX. The cost per image (~$0.01–0.03) is cheaper than your time.

---

## 5. Building a Shared Visual Vocabulary

This is the highest-leverage insight. We maintain a **"style bible"**—a shared folder of 20–30 reference images, each tagged with a 1-line prompt recipe that reproduces it. When a stakeholder says "make it more moody," we don't guess; we point to reference #14 ("low-key lighting, teal shadows, rain-streaked glass") and apply that exact prompt template.

**Practical method:** Every Friday, we pick 5 failed generations and 5 wins, document what changed (seed, prompt structure, LoRA strength), and update the bible. Within a month, the team speaks in a shared shorthand: "Give it a #3 lighting with a #7 texture overlay." This cuts re-roll requests by ~40%.

---

**Bottom line:** Treat local as your sketchpad, cloud as your canvas, and the style bible as your shared language. The models change; the workflow stays.
