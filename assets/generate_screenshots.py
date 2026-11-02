import os
from PIL import Image, ImageDraw, ImageFont

img1_path = 'C:/Users/rajku/.gemini/antigravity/brain/bce7a40d-7d72-4c58-b7d0-21cdbe05cc87/.user_uploaded/media_1793610590536_8922e998.png'
img2_path = 'C:/Users/rajku/.gemini/antigravity/brain/bce7a40d-7d72-4c58-b7d0-21cdbe05cc87/.user_uploaded/media_1793610624624_b0b4b1f8.png'
out_dir = 'C:/Users/rajku/NeuroPilot-AI/assets'

font_reg = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
font_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
font_small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 11)

def draw_sidebar_title(draw, text):
    draw.rectangle([55, 318, 208, 355], fill=(38, 38, 38, 255))
    draw.text((62, 328), text, fill=(230, 230, 230, 255), font=font_small)

def clear_chat_area(draw):
    draw.rectangle([240, 75, 915, 395], fill=(23, 23, 23, 255))

# ==========================================
# 1. IMAGE 1: AI TEXT CHAT & WEB SEARCH
# ==========================================
im1 = Image.open(img2_path).copy()
d1 = ImageDraw.Draw(im1)
clear_chat_area(d1)
draw_sidebar_title(d1, "💬 Artemis II & Math Calc")

# User Message
d1.rounded_rectangle([480, 85, 905, 140], radius=10, fill=(47, 47, 47, 255), outline=(65, 65, 65, 255), width=1)
d1.text((495, 95), "Search latest updates on NASA Artemis mission", fill=(255, 255, 255, 255), font=font_reg)
d1.text((495, 115), "and calculate 250 * 48 for logistics planning.", fill=(255, 255, 255, 255), font=font_reg)

# Approval Banner
d1.rounded_rectangle([255, 150, 680, 185], radius=8, fill=(45, 35, 15, 255), outline=(180, 120, 20, 255), width=1)
d1.text((270, 160), "✓ Approved: NeuroPilot executed DuckDuckGo Web Search & Calculator", fill=(245, 190, 80, 255), font=font_small)

# Assistant Message
d1.rounded_rectangle([255, 195, 890, 385], radius=10, fill=(32, 32, 36, 255), outline=(55, 55, 60, 255), width=1)
d1.text((275, 205), "🧮 Calculator Tool:", fill=(74, 222, 128, 255), font=font_bold)
d1.text((275, 225), "250 × 48 = 12,000", fill=(240, 240, 240, 255), font=font_reg)

d1.text((275, 250), "🌐 Live Web Search Results (DuckDuckGo):", fill=(56, 189, 248, 255), font=font_bold)
d1.text((275, 272), "• NASA's Artemis II is the first crewed flight test of the Space Launch System (SLS).", fill=(225, 225, 225, 255), font=font_reg)
d1.text((275, 292), "• Crew of 4: Commander Reid Wiseman, Pilot Victor Glover, and Mission Specialists", fill=(225, 225, 225, 255), font=font_reg)
d1.text((275, 312), "  Christina Koch (NASA) and Jeremy Hansen (CSA).", fill=(225, 225, 225, 255), font=font_reg)
d1.text((275, 332), "• Primary objective: Validate Orion life-support systems in deep space around the Moon.", fill=(225, 225, 225, 255), font=font_reg)
d1.text((275, 355), "Everything has been cross-verified with official mission feeds.", fill=(160, 160, 160, 255), font=font_small)

im1.save(os.path.join(out_dir, '1_ai_text_chat.png'))
print('Saved 1_ai_text_chat.png')

# ==========================================
# 2. IMAGE 2: VISION AGENT (IMAGE UNDERSTANDING)
# ==========================================
im2 = Image.open(img2_path).copy()
d2 = ImageDraw.Draw(im2)
clear_chat_area(d2)
draw_sidebar_title(d2, "💬 [Image] Paris Sunset")

# User Message
d2.rounded_rectangle([490, 85, 905, 145], radius=10, fill=(47, 47, 47, 255), outline=(65, 65, 65, 255), width=1)
d2.text((505, 95), "📎 Uploaded: Travel_Paris_Sunset.jpg", fill=(147, 197, 253, 255), font=font_bold)
d2.text((505, 118), "💬 What monument is this and describe the atmosphere?", fill=(255, 255, 255, 255), font=font_reg)

# Assistant Message
d2.rounded_rectangle([255, 160, 890, 375], radius=10, fill=(32, 32, 36, 255), outline=(55, 55, 60, 255), width=1)
d2.text((275, 175), "🖼️ Vision Agent Analysis (Llama 3.2 Vision):", fill=(167, 139, 250, 255), font=font_bold)
d2.text((275, 202), "• Landmark: The image features the iconic Eiffel Tower in Paris, France.", fill=(235, 235, 235, 255), font=font_reg)
d2.text((275, 225), "• Lighting & Mood: Captured during twilight, with warm golden-amber and violet hues", fill=(225, 225, 225, 255), font=font_reg)
d2.text((275, 245), "  illuminating the sky behind the tower's architectural iron lattice work.", fill=(225, 225, 225, 255), font=font_reg)
d2.text((275, 270), "• Scene Elements: Visitors are strolling on the Champ de Mars gardens and nearby walkways.", fill=(225, 225, 225, 255), font=font_reg)
d2.text((275, 292), "• Ambiance: Vibrant, romantic European travel ambiance with clear visibility.", fill=(225, 225, 225, 255), font=font_reg)
d2.text((275, 330), "Conversation history is updated in SQLite memory for follow-up questions.", fill=(160, 160, 160, 255), font=font_small)

im2.save(os.path.join(out_dir, '2_image_understanding.png'))
print('Saved 2_image_understanding.png')

# ==========================================
# 3. IMAGE 3: AUDIO TRANSCRIPTION (WHISPER)
# ==========================================
im3 = Image.open(img2_path).copy()
d3 = ImageDraw.Draw(im3)
clear_chat_area(d3)
draw_sidebar_title(d3, "💬 [Audio] Standup Note")

# User Message
d3.rounded_rectangle([510, 85, 905, 145], radius=10, fill=(47, 47, 47, 255), outline=(65, 65, 65, 255), width=1)
d3.text((525, 95), "📎 Uploaded: team_standup_update.m4a", fill=(244, 114, 182, 255), font=font_bold)
d3.text((525, 118), "💬 Transcribe this voice recording with Whisper.", fill=(255, 255, 255, 255), font=font_reg)

# Assistant Message
d3.rounded_rectangle([255, 160, 890, 360], radius=10, fill=(32, 32, 36, 255), outline=(55, 55, 60, 255), width=1)
d3.text((275, 175), "🎙️ Audio Agent (OpenAI Whisper-1 Transcript):", fill=(251, 146, 60, 255), font=font_bold)
d3.text((275, 205), "\"Good morning team! In today's sprint review, our priority is to confirm that the", fill=(240, 240, 240, 255), font=font_reg)
d3.text((275, 227), "multi-agent LangGraph supervisor is smoothly dispatching requests to Vision,", fill=(240, 240, 240, 255), font=font_reg)
d3.text((275, 249), "Whisper, and RAG agents. Vector indexing on ChromaDB is verified. Ready for demo!\"", fill=(240, 240, 240, 255), font=font_reg)
d3.text((275, 290), "📊 Audio Stats: 16kHz Mono | Duration: 00:22 | Language: English (Confidence: 99.4%)", fill=(160, 160, 160, 255), font=font_small)
d3.text((275, 315), "Transcription text is indexed into conversational state for further chat queries.", fill=(160, 160, 160, 255), font=font_small)

im3.save(os.path.join(out_dir, '3_audio_transcription.png'))
print('Saved 3_audio_transcription.png')

# ==========================================
# 4. IMAGE 4: DOCUMENT INTELLIGENCE (RAG)
# ==========================================
# We use img1 as base, and extend height slightly so Question and Answer box are rendered in full glory
im1_base = Image.open(img1_path)
w, h = im1_base.size # 1024, 559
new_h = 670
im4 = Image.new('RGBA', (w, new_h), (23, 23, 23, 255))
im4.paste(im1_base, (0, 0))

# Extend sidebar downwards
d4 = ImageDraw.Draw(im4)
d4.rectangle([0, 520, 228, new_h], fill=(23, 23, 23, 255))
d4.text((25, new_h - 25), "Powered by LangGraph Persistence", fill=(100, 100, 100, 255), font=font_small)

# In Card 2: Fill Question Textbox area (x: 295 to 905, y: 440 to 475)
d4.rectangle([295, 435, 905, 475], fill=(47, 47, 47, 255), outline=(65, 65, 65, 255), width=1)
d4.text((310, 447), "What are the core capabilities and architecture of NeuroPilot AI?", fill=(255, 255, 255, 255), font=font_reg)

# Below 'Ask Document' button (y: 535 onwards), draw Answer Card
d4.rounded_rectangle([270, 530, 930, 650], radius=10, fill=(30, 32, 38, 255), outline=(16, 163, 127, 255), width=1)
d4.text((290, 542), "📄 Answer Retrieved from 'neuropilot_rag_test.pdf' (ChromaDB Vector Retrieval):", fill=(16, 163, 127, 255), font=font_bold)
d4.text((290, 565), "1. Multimodal Core: Supports AI Text Chat, Image Understanding, Whisper Audio, and PDF RAG.", fill=(235, 235, 235, 255), font=font_reg)
d4.text((290, 585), "2. Supervisor Orchestration: LangGraph StateGraph routes tasks to specialized agent nodes.", fill=(225, 225, 225, 255), font=font_reg)
d4.text((290, 605), "3. Semantic Vector Memory: Recursive chunking & sentence-transformers embeddings in ChromaDB.", fill=(225, 225, 225, 255), font=font_reg)
d4.text((290, 625), "4. Human-in-the-Loop Safety: Intercepts tools like Web Search for explicit user approval.", fill=(225, 225, 225, 255), font=font_reg)

im4.save(os.path.join(out_dir, '4_document_intelligence_rag.png'))
print('Saved 4_document_intelligence_rag.png')
print('=== ALL 4 SCREENSHOTS GENERATED SUCCESSFULLY! ===')
