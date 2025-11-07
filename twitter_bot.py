import tweepy
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

# ============================================
# TWITTER API CREDENTIALS (from GitHub Secrets)
# ============================================
API_KEY = os.environ.get('TWITTER_API_KEY')
API_SECRET = os.environ.get('TWITTER_API_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# ============================================
# GTA VI COUNTDOWN SETTINGS
# ============================================
RELEASE_DATE = datetime(2026, 11, 19)
START_DATE = datetime(2025, 11, 6)

def calculate_progress():
    """Calculate progress with correct day counting"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    release = datetime(2026, 11, 19, 0, 0, 0, 0)
    
    total_days = (release - START_DATE).days
    days_passed = (today - START_DATE).days
    days_remaining = (release - today).days
    
    percentage = max(0, min(100, (days_passed / total_days) * 100))
    
    return {
        'percentage': round(percentage),
        'days_remaining': days_remaining
    }

def create_countdown_image():
    """Generate GTA VI countdown with logos"""
    img = Image.new('RGB', (1080, 1080))
    draw = ImageDraw.Draw(img)
    
    # Gradient background (Pink to Purple - Vice City style)
    for y in range(1080):
        r = int(230 - (y * 90 / 1080))
        g = int(80 - (y * 40 / 1080))
        b = int(200 + (y * 40 / 1080))
        draw.line([(0, y), (1080, y)], fill=(r, g, b))
    
    progress = calculate_progress()
    
    # Load fonts
    fonts_loaded = False
    for font_name in ["pricedown.otf", "Pricedown.otf", "PRICEDOWN.OTF", "pricedown.ttf", "Pricedown.ttf"]:
        try:
            large_font = ImageFont.truetype(font_name, 70)
            medium_font = ImageFont.truetype(font_name, 50)
            small_font = ImageFont.truetype(font_name, 50)
            supersmall_font = ImageFont.truetype(font_name, 24)
            fonts_loaded = True
            print(f"✅ Loaded Pricedown font: {font_name}")
            break
        except:
            continue
    
    if not fonts_loaded:
        print("⚠️ Pricedown font not found, trying Arial...")
        for font_name in ["arial.ttf", "Arial.ttf", "arialbd.ttf"]:
            try:
                large_font = ImageFont.truetype(font_name, 70)
                medium_font = ImageFont.truetype(font_name, 50)
                small_font = ImageFont.truetype(font_name, 42)
                supersmall_font = ImageFont.truetype(font_name, 24)
                fonts_loaded = True
                print(f"✅ Loaded font: {font_name}")
                break
            except:
                continue
    
    if not fonts_loaded:
        print("⚠️ Using default font")
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        supersmall_font = ImageFont.load_default()
    # Try to load GTA VI logo
    gta_logo_loaded = False
    try:
        gta_logo = Image.open('gta_vi_logo.png').convert('RGBA')
        logo_width = 600
        logo_height = int(gta_logo.height * (logo_width / gta_logo.width))
        gta_logo = gta_logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        logo_x = (1080 - logo_width) // 2
        logo_y = 160
        img.paste(gta_logo, (logo_x, logo_y), gta_logo)
        gta_logo_loaded = True
        print("✅ GTA VI logo loaded")
    except FileNotFoundError:
        print("⚠️ gta_vi_logo.png not found - using text fallback")
    
    if not gta_logo_loaded:
        try:
            title_font = ImageFont.truetype("pricedown.otf", 350)
        except:
            try:
                title_font = ImageFont.truetype("arial.ttf", 350)
            except:
                title_font = large_font
        
        for offset_x in range(-8, 9, 2):
            for offset_y in range(-8, 9, 2):
                if abs(offset_x) + abs(offset_y) > 2:
                    draw.text((280 + offset_x, 380 + offset_y), "VI", 
                             font=title_font, fill='white')
    
    # Progress bar
    bar_width, bar_height = 580, 90
    bar_x = (1080 - bar_width) // 2
    bar_y = 720
    
    for i in range(6):
        draw.rectangle([bar_x - i, bar_y - i, bar_x + bar_width + i, bar_y + bar_height + i],
                      outline='#FFFFFF', width=1)
    
    fill_width = int((bar_width - 20) * (progress['percentage'] / 100))
    if fill_width > 0:
        draw.rectangle([bar_x + 10, bar_y + 10, bar_x + 10 + fill_width, bar_y + bar_height - 10],
                      fill='#FF69B4')
    
    draw.text((540, 760), f"{progress['percentage']}%", font=large_font, fill='white', anchor='mm')
    draw.text((540, 940), f"{progress['days_remaining']} DAYS REMAINING", font=small_font, fill='white', anchor='mm')
    draw.text((540, 10005), "COMING", font=medium_font, fill='white', anchor='mm')
    draw.text((540, 870), "NOVEMBER 19, 2026", font=small_font, fill='white', anchor='mm')
    
    # Twitter handle watermark (subtle - blends with gradient)
    draw.text((20, 1060), "@gta6countdown26", font=supersmall_font, fill='#B080C8', anchor='lm')
    
    rockstar_logo_loaded = False
    try:
        rockstar_logo = Image.open('rockstar_logo.png').convert('RGBA')
        logo_size = 70
        rockstar_logo = rockstar_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        img.paste(rockstar_logo, (965, 965), rockstar_logo)
        rockstar_logo_loaded = True
        print("✅ Rockstar logo loaded")
    except FileNotFoundError:
        print("⚠️ rockstar_logo.png not found - using R* fallback")
    
    if not rockstar_logo_loaded:
        draw.ellipse([965, 965, 1035, 1035], outline='white', width=4)
        draw.text((1000, 1000), "R*", font=small_font, fill='white', anchor='mm')
    
    filename = f"gta_vi_countdown_{datetime.now().strftime('%Y%m%d')}.png"
    img.save(filename, quality=95)
    print(f"✅ Image created: {filename}")
    
    return filename, progress

def post_to_twitter():
    """Generate image and post to Twitter"""
    try:
        print("🔑 Authenticating with Twitter...")
        auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        client = tweepy.Client(
            consumer_key=API_KEY, consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
        )
        
        print("✅ Connected to Twitter API")
        
        print("\n🎨 Generating countdown image...")
        image_path, progress = create_countdown_image()
        
        tweet_text = f"""🎮 GTA VI COUNTDOWN 🌴

📊 Progress: {progress['percentage']}%
⏰ Days Remaining: {progress['days_remaining']}
📅 Release: November 19, 2026

#GTAVI #GrandTheftAutoVI #RockstarGames"""
        
        print("\n📤 Uploading image to Twitter...")
        media = api_v1.media_upload(filename=image_path)
        
        print("🐦 Posting tweet...")
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
        
        print("\n✅ SUCCESSFULLY POSTED!")
        print(f"🔗 https://twitter.com/user/status/{response.data['id']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 GTA VI TWITTER BOT - GitHub Actions")
    post_to_twitter()




