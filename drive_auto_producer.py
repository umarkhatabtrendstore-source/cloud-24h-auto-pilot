# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import random
import pickle
import requests
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(r"H:\UMAR_MULTI_BRAND_4_IN_1")
BG_MUSIC_DIR = BASE_DIR / "5_CUSTOM_SCRIPT_STUDIO" / "BG_MUSIC"
LOG_FILE = BASE_DIR / "uploaded_history.json"
OLLAMA_URL = "http://localhost:11434/api/generate"

FOLDER_MAP = {
    "1": "1_The_Umar_Show_AI",
    "2": "2_Umar_MiniCrafts",
    "3": "3_UMAR_MART",
    "4": "4_Umar_Media_777"
}

# Har brand ke liye 8 specific scenes aur script mapping
CHANNELS = {
    "1": {
        "key": "the_umar_show",
        "name": "THE UMAR SHOW AI",
        "tag": "@TheUmarShowAI",
        "page_id": "1292333420632038",
        "fb_token": "EAAe5VUXteqQBSoLEYx2Es8ott7pxaGwAipFCp8wnjoWZCa7KNlU0xc2Je4Dw3cyPHJNwXZAYrvSo89cN44kDvlhKHElwsveaq1O4dsPBJ1d0JW2XUopBbWZBtK0Kr6TriI0XvZBHmTrMeXbIOroUAuKvAYNrCkYARN8ZBPZCR6nGZAs8qaYIMr6uVf5rYffIZAoc5eO2TFQGZAbb2QYdPZCyds",
        "ig_user_id": "17841425142044849",
        "yt_token": "yt_token_The_Umar_Show_AI.pickle",
        "yt_category": "28",
        "voice": "ur-PK-AsadNeural",
        "prompt": "Write a 45-second high-impact tech script in clean native Urdu script (اردو). Explain 3 ways AI tools and Python scripts save daily work and boost productivity. Pure Urdu only.",
        "fallback": "آج کے جدید دور میں آرٹیفیشل انٹیلیجنس اور آٹومیشن نے کام کرنے کا پورا طریقہ بدل دیا ہے۔ اگر آپ اپنے روزانہ کے کاموں کو تیز بنانا چاہتے ہیں تو پائتھن اسکرپٹس اور جدید اے آئی ٹولز کا استعمال شروع کریں۔ یہ ٹولز آپ کے گھنٹوں کا کام سیکنڈوں میں خودکار طریقے سے نمٹا دیتے ہیں، چاہے وہ ڈیٹا اینالیسز ہو یا کنٹینٹ کریشن۔ اپنے وقت کو قیمتی بنائیں اور ٹیکنالوجی کی طاقت سے اپنے کاروبار کو دس گنا تیزی سے آگے بڑھائیں۔ مزید بہترین ٹیکنالوجی اپڈیٹس کے لیے ہمارے ساتھ جڑے رہیں اور فالو کریں۔",
        "giveaway_prompt": "Act as an expert Python Automation Engineer. Write a Python script to automate my repetitive daily files, organize downloads, and generate an automated daily summary report.",
        "hashtags": "#TheUmarShowAI #AIAgents #PythonAutomation #Tech2026 #Shorts #Reels",
        "scenes": [
            {"keyword": "artificial-intelligence-humanoid-robot-face", "caption": "Future of AI Agents", "backup": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "hacker-coding-screen-matrix", "caption": "Python Automation Hub", "backup": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "robotics-automation-industry", "caption": "Autonomous Systems", "backup": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "server-rack-data-center", "caption": "Cloud Computing Power", "backup": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "cyber-security-network", "caption": "Zero Bug Workflows", "backup": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "ai-neural-chip-technology", "caption": "Neural Intelligence", "backup": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "programmer-developer-workspace", "caption": "Speed Up 10x Daily", "backup": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "futuristic-digital-dashboard", "caption": "Automate Everything", "backup": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1080&h=1920&q=80"}
        ]
    },
    "2": {
        "key": "umar_minicrafts",
        "name": "UMAR MINICRAFTS",
        "tag": "@UmarMiniCrafts",
        "page_id": "1277199158813270",
        "fb_token": "EAAe5VUXteqQBSkHIz5IwFhFoKyslZA2E0ZC21aOaTrp72kqdBCLyPgbL9xBoUZAiEljCzmwkwpXi1ElZBusG6H1fb2aZBJ87ULtj8qsmDtrlIlna1ZASmhfITmyZCz2weNJCBge5N5vJpf21v6kdLMITZBOWeCV9s2NBfFoBNJfqCCy9WXJsjgtiZBb00BpCjC5f33c4ZAlXciig6LLPwzNUj9DHCP",
        "ig_user_id": "17841436265845764",
        "yt_token": "yt_token_Umar_MiniCrafts.pickle",
        "yt_category": "26",
        "voice": "ur-PK-UzmaNeural",
        "prompt": "Write a 45-second soothing ASMR craft narrative in clean Urdu script (اردو). Pure Urdu only.",
        "fallback": "ریزن آرٹ اور مائیکرو کرافٹس کی دنیا میں ہر چھوٹی تفصیل اپنا ایک الگ حسن رکھتی ہے۔ جب نیلے شفاف ریزن کو لکڑی کے ٹکڑوں پر بکھیرا جاتا ہے تو سمندر کی لہروں کا قدرتی منظر ابھر کر سامنے آتا ہے۔ باریک اوزاروں کے ساتھ گھنٹوں کی محنت اس چھوٹے سے ماڈل کو ایک جادوئی شکل دے دیتی ہے۔ ایسی ہی دلکش اور پرسکون فن پاروں کی ویڈیوز دیکھنے کے لیے ہمارے پیج کو فالو کیجیے۔",
        "giveaway_prompt": "Step-by-step DIY Blueprint: Mix 2:1 epoxy resin with blue mica pigment, pour over stabilized burl wood, cure for 24 hours, and polish up to 7000 grit for mirror glass finish.",
        "hashtags": "#UmarMiniCrafts #MiniCrafts #ResinArt #ASMR #DIY #Shorts #Reels",
        "scenes": [
            {"keyword": "epoxy-resin-ocean-art", "caption": "Crystal Ocean Diorama", "backup": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "miniature-woodwork-detail", "caption": "Precision Micro Crafting", "backup": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "tiny-sculpture-handmade", "caption": "Handmade Details", "backup": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "craftsman-hands-workbench", "caption": "Artisan Workbench", "backup": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "miniature-painting-brush", "caption": "Precision Detailing", "backup": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "glowing-resin-crystal", "caption": "Finished Masterpiece", "backup": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "wood-carving-macro", "caption": "Macro ASMR Carving", "backup": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "glass-resin-diorama", "caption": "Pure Crafting Magic", "backup": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1080&h=1920&q=80"}
        ]
    },
    "3": {
        "key": "umar_mart",
        "name": "UMAR MART & DIGITAL SOLUTIONS",
        "tag": "@UmarMartDigital",
        "page_id": "968050116400329",
        "fb_token": "EAAe5VUXteqQBSqdVb4w9xr3d71mtSlerlMlPjdcBqyVJ9qjUmyLS8reG9pTMQkF3tNjhZBZCygVsXaQNNzsz4ndl3iR585V5yinqKJeh8Hh7bU84g9EJ0x7AL4fC8hrLurCeXJrYM0TRubqa3ZAqhjJ0CpZAzbLQ180ZBabNbukQngjHdIdBshyu4bQ7zBiN6ZBkbalJXtj8fa7MIKdEld",
        "ig_user_id": "",
        "yt_token": "yt_token.pickle",
        "yt_category": "22",
        "voice": "ur-PK-AsadNeural",
        "prompt": "Write a 45-second commercial script in clean Urdu script (اردو). Pure Urdu only.",
        "fallback": "کیا آپ کا کاروبار کسٹمرز کے دیر سے جواب ملنے کی وجہ سے سیلز کھو رہا ہے؟ عمر مارٹ ڈیجیٹل سلوشنز لایا ہے آپ کے لیے واٹس ایپ کلاؤڈ اے پی آئی کا مکمل خودکار نظام۔ اب آپ کا بزنس چوبیس گھنٹے جاگے گا، کسٹمرز کو خودکار جواب دے گا اور ہر نئی لیڈ کو فوراً کنفرم کرے گا۔ دیر مت کیجیے، اپنے بزنس کو ڈیجیٹل آٹومیشن پر منتقل کریں اور سیلز میں دس گنا اضافہ دیکھیں۔ ابھی دیے گئے لنک سے رابطہ کریں۔",
        "giveaway_prompt": "WhatsApp Automation Setup Checklist: 1. Meta Cloud API permanent token, 2. Webhook payload verification, 3. Auto-reply instant catalog dispatch.",
        "hashtags": "#UmarMart #DigitalSolutions #TechDeals #OnlineStore #Shorts #Reels",
        "scenes": [
            {"keyword": "customer-messaging-smartphone", "caption": "WhatsApp Cloud API", "backup": "https://images.unsplash.com/photo-1556742049-0a67e5572293?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "modern-call-center-support", "caption": "Instant Auto Support", "backup": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "ecommerce-online-store-orders", "caption": "10x Sales Funnel", "backup": "https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "marketing-dashboard-sales", "caption": "Zero Lead Loss", "backup": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "business-team-growth-charts", "caption": "Smart CRM System", "backup": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "credit-card-online-payment", "caption": "Fast Checkout Engine", "backup": "https://images.unsplash.com/photo-1556742044-3c52d6e88c62?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "warehouse-delivery-shipping", "caption": "Automated Order Dispatch", "backup": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "successful-entrepreneur-office", "caption": "Scale Business Today", "backup": "https://images.unsplash.com/photo-1556742049-0a67e5572293?auto=format&fit=crop&w=1080&h=1920&q=80"}
        ]
    },
    "4": {
        "key": "umar_media_777",
        "name": "UMAR MEDIA 777",
        "tag": "@UmarMedia777",
        "page_id": "240389702494313",
        "fb_token": "EAAe5VUXteqQBSgS5olW1UuZCiQuCRAYj32Ylz5riLDZAxUTrm1gju0jHGWvD3rok8GseVgvWdvZC4P6Qx2NS3aGYdHrWi3lQRT4w9vaqOUZCerO56V1vsiDJgkcTsE0s0yXQbJZAuwfm93rhLk3AyrrWZCoA8y4lTOUBhB4kPdRQvWQADljrILFxHfqG2wqfjM0kVvAXY4tJTr4kaHefQEufQZD",
        "ig_user_id": "17841475118196836",
        "yt_token": "yt_token_Umar_Media_777.pickle",
        "yt_category": "27",
        "voice": "ur-PK-AsadNeural",
        "prompt": "Write a 45-second viral marketing strategy in clean Urdu script (اردو). Pure Urdu only.",
        "fallback": "سوشل میڈیا پر وائرل ہونا کوئی اتفاق نہیں بلکہ ایک سوچی سمجھی حکمت عملی ہے۔ اگر آپ اپنی ریلز اور شارٹس پر لاکھوں ویوز چاہتے ہیں تو پہلے تین سیکنڈز کے ہک کو مضبوط بنائیں۔ جب تک آڈینس ویڈیو کے شروع میں رکتی نہیں، الگورتھم آپ کا ساتھ نہیں دیتا۔ روزانہ مستقل مزاجی اور معیاری ساؤنڈ ڈیزائن آپ کو عام کریئیٹر سے الگ بنا دیتا ہے۔ الگورتھم کے خفیہ راز جاننے کے لیے عمر میڈیا سات سو ستتر کو فالو کریں۔",
        "giveaway_prompt": "Viral 3-Second Hook Formula: [Question/Pain Point] + [Unusual Visual Contrast] + [Bold Promise within 3 seconds]. Example: 'Why 99% of automation workflows fail before day 30.'",
        "hashtags": "#UmarMedia777 #ViralGrowth #MediaHacks #Shorts #Reels #Monetization",
        "scenes": [
            {"keyword": "cinematic-camera-lens-studio", "caption": "Viral Studio Engine", "backup": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "social-media-content-creator", "caption": "Beat The Algorithm", "backup": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "viral-video-views-analytics", "caption": "100K Views Strategy", "backup": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "studio-microphone-podcast", "caption": "Sound Design Mastery", "backup": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "digital-creator-cash-growth", "caption": "Content Monetization", "backup": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "video-editing-timeline-monitor", "caption": "Fast Visual Cuts", "backup": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "mobile-filmmaking-ringlight", "caption": "High Retention Flow", "backup": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1080&h=1920&q=80"},
            {"keyword": "creator-award-success", "caption": "Dominating Social Media", "backup": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1080&h=1920&q=80"}
        ]
    }
}

history = json.load(open(LOG_FILE, "r", encoding="utf-8")) if LOG_FILE.exists() else []

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

def download_scene_image(keyword, backup_url, save_path):
    """Pehle script keyword ke mutabiq fresh image download karta hai, fallback backup_url use karta hai"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    clean_kw = keyword.replace("-", "+")
    urls = [
        f"https://source.unsplash.com/1080x1920/?{clean_kw}",
        backup_url
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as response, open(save_path, 'wb') as out_f:
                out_f.write(response.read())
            with Image.open(save_path) as test_im:
                test_im.verify()
            return True
        except:
            continue
            
    im = Image.new("RGB", (1080, 1920), color=(15, 23, 42))
    im.save(save_path)
    return False

def make_burned_card(img_path, out_path, ch_name, ch_tag, caption_text):
    im = Image.open(img_path).convert("RGBA")
    im = im.resize((1080, 1920), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Top Brand Card
    draw.rectangle([60, 90, 1020, 220], fill=(12, 18, 30, 235), outline=(0, 200, 255, 230), width=3)
    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 44)
        font_tag = ImageFont.truetype("arial.ttf", 28)
        font_capt = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font_brand = font_tag = font_capt = ImageFont.load_default()

    draw.text((95, 112), ch_name, font=font_brand, fill=(255, 255, 255, 255))
    draw.text((95, 168), f"{ch_tag} | Verified Studio", font=font_tag, fill=(0, 200, 255, 255))

    # Bottom Highlight Card
    draw.rectangle([50, 1570, 1030, 1750], fill=(10, 12, 18, 240), outline=(255, 215, 0, 230), width=3)
    draw.text((80, 1600), "EXCLUSIVE HIGHLIGHT:", font=font_tag, fill=(255, 215, 0, 255))
    draw.text((80, 1655), caption_text, font=font_capt, fill=(255, 255, 255, 255))

    final_img = Image.alpha_composite(im, overlay).convert("RGB")
    final_img.save(out_path, quality=95)

def is_pure_urdu(text):
    english_keywords = ["here is", "narrator", "script", "welcome", "today", "whatsapp", "business"]
    text_lower = text.lower()
    for kw in english_keywords:
        if kw in text_lower:
            return False
    urdu_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return urdu_chars > 30

def ask_ollama_urdu_45s(prompt, fallback):
    print("    [*] Generating 45s High-Value Script with Local Ollama...")
    try:
        payload = {
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.5}
        }
        res = requests.post(OLLAMA_URL, json=payload, timeout=25).json()
        raw = res.get("response", "").strip()
        lines = [line.strip() for line in raw.splitlines() if line.strip() and not line.startswith(("#", "-", "*", "Note", "Sure", "Narrator"))]
        clean_urdu = " ".join(lines)
        if len(clean_urdu) > 150 and is_pure_urdu(clean_urdu):
            return clean_urdu
    except Exception:
        pass
    print("    [+] Using Studio Verified 45s Master Native Urdu Script.")
    return fallback

def render_original_studio_reel(info, urdu_text, review_dir):
    work_dir = review_dir / "_temp_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    voice_path = work_dir / "voice.mp3"
    print(f"    [1] 45s Voice-over generate ho raha hai ({info['voice']})...")
    
    temp_txt_file = work_dir / "script.txt"
    temp_txt_file.write_text(urdu_text, encoding="utf-8")
    
    subprocess.run([
        sys.executable, "-m", "edge_tts",
        "--voice", info["voice"],
        "--rate=-2%",
        "--pitch=+0Hz",
        "-f", str(temp_txt_file),
        "--write-media", str(voice_path)
    ], check=True)

    v_duration = get_audio_duration(voice_path)
    print(f"        Video Duration: {v_duration:.2f} seconds | Voice: {info['voice']}")

    scenes = info["scenes"]
    n_scenes = len(scenes)
    scene_dur = v_duration / n_scenes

    print(f"    [2] Script ke mutabiq 8 matching HD images download ho rahi hain...")
    img_list = []
    for i, sc in enumerate(scenes):
        raw_p = work_dir / f"scene_raw_{i}.jpg"
        burned_p = work_dir / f"scene_burned_{i}.jpg"
        
        # Fresh download based on scene
        print(f"        -> Scene {i+1}/{n_scenes}: {sc['caption']} ({sc['keyword']})")
        download_scene_image(sc["keyword"], sc["backup"], raw_p)
        make_burned_card(raw_p, burned_p, info["name"], info["tag"], sc["caption"])
        img_list.append(burned_p)

    print("    [3] ZoomPan Dynamic Video stitch ho rahi hai (8 scenes cut)...")
    clip_files = []
    for i, img_path in enumerate(img_list):
        clip_p = work_dir / f"clip_{i}.mp4"
        frames = int(scene_dur * 25)
        zoom_expr = "min(zoom+0.0015,1.20)" if i % 2 == 0 else "if(lte(zoom,1.0),1.20,max(1.001,zoom-0.0015))"
        vf = f"scale=1080:1920,zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=25"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
            "-t", str(scene_dur), "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip_p)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_files.append(clip_p)

    concat_txt = work_dir / "clips.txt"
    concat_txt.write_text("\n".join([f"file '{c.name}'" for c in clip_files]))
    raw_video = work_dir / "stitched.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(raw_video)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    bgm_list = list(BG_MUSIC_DIR.glob("*.mp3"))
    final_output = review_dir / f"{info['key']}_{timestamp}.mp4"
    fade_start = max(0, v_duration - 1.0)

    if bgm_list:
        bgm_file = random.choice(bgm_list)
        print(f"    [4] Background Music 10% Ducking mix ho raha hai: {bgm_file.name}")
        filter_complex = f"[1:a]volume=1.5,dynaudnorm=f=75:g=15,afade=t=out:st={fade_start}:d=1.0[v];[2:a]volume=0.10,afade=t=out:st={fade_start}:d=1.0[bg];[v][bg]amix=inputs=2:duration=first[aout]"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_video), "-i", str(voice_path),
            "-stream_loop", "-1", "-i", str(bgm_file),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac",
            "-t", str(v_duration), str(final_output)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_video), "-i", str(voice_path),
            "-filter:a", f"volume=1.5,dynaudnorm=f=75:g=15,afade=t=out:st={fade_start}:d=1.0",
            "-c:v", "copy", "-c:a", "aac",
            "-t", str(v_duration), str(final_output)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return final_output

def open_folder_and_select_video(file_path):
    try:
        subprocess.run(f'explorer /select,"{file_path}"', shell=True)
    except:
        pass

def post_facebook(page_id, token, vid_path, caption):
    print("    [>>>] Facebook par upload ho raha hai...")
    url = f"https://graph.facebook.com/v21.0/{page_id}/videos"
    with open(vid_path, "rb") as f:
        r = requests.post(url, data={"access_token": token, "description": caption}, files={"source": f}).json()
    if "id" in r:
        print(f"    [OK] Facebook Live! ID: {r['id']}")
        return True
    print(f"    [X] Facebook Error: {r}")
    return False

def post_instagram(ig_user_id, token, vid_path, caption):
    if not ig_user_id:
        return False
    print("    [>>>] Instagram Reel upload shuru...")
    try:
        init_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
        init_res = requests.post(init_url, data={'media_type': 'REELS', 'upload_type': 'resumable', 'caption': caption, 'access_token': token}).json()
        upload_uri = init_res.get('upload_url')
        vid_id = init_res.get('id')
        if not upload_uri:
            print(f"    [X] Instagram Init Error: {init_res}")
            return False

        file_size = os.path.getsize(vid_path)
        headers = {'Authorization': f'OAuth {token}', 'offset': '0', 'file_size': str(file_size)}
        with open(vid_path, 'rb') as f:
            requests.post(upload_uri, headers=headers, data=f)

        for _ in range(12):
            time.sleep(5)
            s_res = requests.get(f"https://graph.facebook.com/v21.0/{vid_id}?fields=status_code&access_token={token}").json()
            if s_res.get('status_code') == 'FINISHED':
                break

        pub_res = requests.post(f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish", data={'creation_id': vid_id, 'access_token': token}).json()
        if 'id' in pub_res:
            print(f"    [OK] Instagram Reel Live! ID: {pub_res['id']}")
            return True
        print(f"    [X] Instagram Error: {pub_res}")
        return False
    except Exception as e:
        print(f"    [X] Instagram Exception: {e}")
        return False

def post_youtube(token_file, vid_path, title, caption, tags, category_id):
    t_path = BASE_DIR / token_file
    if not t_path.exists():
        return False
    print("    [>>>] YouTube Shorts upload shuru...")
    try:
        with open(t_path, "rb") as f:
            credentials = pickle.load(f)
        youtube = build("youtube", "v3", credentials=credentials)
        body = {
            "snippet": {"title": f"{title[:90]} #Shorts", "description": caption, "tags": tags, "categoryId": category_id},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        }
        media = MediaFileUpload(str(vid_path), chunksize=4*1024*1024, resumable=True, mimetype="video/mp4")
        req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        res = None
        while res is None:
            status, res = req.next_chunk()
            if status:
                print(f"       -> YouTube Progress: {int(status.progress() * 100)}%")
        print(f"    [OK] YouTube Short Live: https://youtube.com/shorts/{res.get('id')}")
        return True
    except Exception as e:
        print(f"    [X] YouTube Upload Error: {e}")
        return False

def run_ollama_engine():
    print("=" * 65)
    print("   UMAR 4-PAGE HIGH RETENTION AUTO ENGINE (FB + INSTA + YT)")
    print("=" * 65)

    for ch_key in ["1", "2", "3", "4"]:
        config = CHANNELS[ch_key]
        brand_folder_name = FOLDER_MAP[ch_key]
        review_dir = BASE_DIR / brand_folder_name / "output_review"
        review_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=======================================================")
        print(f"[*] Processing Channel: {config['name']}")
        print(f"=======================================================")
        
        # 1. 45-Second Native Urdu Voice Script
        urdu_voice_text = ask_ollama_urdu_45s(config["prompt"], config["fallback"])
        
        # 2. Value-Packed Caption with Copy-Paste Prompt & Follow Hook
        title = f"{config['scenes'][0]['caption']} | {config['name']}"
        caption = (
            f"🔥 {title}\n\n"
            f"{urdu_voice_text}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 USEFUL PROMPT (Copy-Paste Below):\n"
            f"\"{config['giveaway_prompt']}\"\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"❤️ Video ko LIKE karein aur aisi mazedar tricks ke liye FOLLOW zaroor karein!\n"
            f"📢 Brand: {config['name']} ({config['tag']})\n\n"
            f"{config['hashtags']}"
        )
        tags = [t.replace("#", "") for t in config["hashtags"].split() if "#" in t]

        # 3. Render 45s Video with 8 Script Matched Scenes
        try:
            video_file = render_original_studio_reel(config, urdu_voice_text, review_dir)
        except Exception as e:
            print(f"    [!] Render Error: {e}")
            continue

        if not video_file.exists():
            print(f"    [!] Video render nahi ho saki for {config['name']}, skipping.")
            continue

        print("\n" + "-" * 60)
        print(f"[!] OUTPUT FOLDER POP-UP KHUL GAYA HAI!")
        print(f"[!] Video File: {video_file.name}")
        print("-" * 60)

        # 4. Auto Open Windows Explorer
        open_folder_and_select_video(str(video_file))

        # 5. Review Confirmation
        ans = input(f"\n[?] Umar bhai, video play karke check kar lein.\n    Kya FB + Insta + YT par LIVE post karein? (YES/NO): ").strip().upper()
        if ans in ["YES", "Y"]:
            print(f"\n[+] Live Multi-Posting: {config['name']}...")
            post_facebook(config["page_id"], config["fb_token"], str(video_file), caption)
            post_instagram(config["ig_user_id"], config["fb_token"], str(video_file), caption)
            post_youtube(config["yt_token"], str(video_file), title, caption, tags, config["yt_category"])

            history.append(video_file.name)
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
            print(f"[SUCCESS] {config['name']} Live Posted to FB, IG & YT!\n")
        else:
            print(f"[*] Post Cancel. Video '{video_file.name}' output_review folder mein hi safe hai.\n")

if __name__ == "__main__":
    run_ollama_engine()