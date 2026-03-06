"""
ПРЕМИУМ ДИЗАЙН: Глобальные фоны, Рамки Лиг, Достижения (Пагинация), Грамматика, GIF-АНИМАЦИИ!
"""

import io
import math
import urllib.request
import unicodedata
import random
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from pathlib import Path

BASE_DIR = Path(__file__).parent
FONTS_DIR = BASE_DIR / "fonts"
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

SCREEN_BACKGROUNDS = {
    "menu": "bg_sakura.jpg",
    "study": "bg_temple.jpg",
    "quiz": "bg_neon.jpg",
    "stats": "bg_night.jpg",
    "achievements": "bg_fuji_1.jpg",
    "leaderboard": "bg_cyber.jpg",
    "dictionary": "bg_bamboo.jpg"
}

ASSETS_URLS = {
    # 15 ВАРИАНТОВ ГОРЫ ФУДЗИ
    "bg_fuji_1.jpg": "https://images.unsplash.com/photo-1528164344705-47542687000d?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_2.jpg": "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_3.jpg": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_4.jpg": "https://images.unsplash.com/photo-1553986782-9f37ef95ae40?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_5.jpg": "https://images.unsplash.com/photo-1570942851080-60b6d21469e3?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_6.jpg": "https://images.unsplash.com/photo-1542052125323-e69ad37a47c2?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_7.jpg": "https://images.unsplash.com/photo-1583091720875-9e663a830026?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_8.jpg": "https://images.unsplash.com/photo-1558230230-671c6670868a?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_9.jpg": "https://images.unsplash.com/photo-1585860295874-8b6b02a2491a?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_10.jpg": "https://images.unsplash.com/photo-1537136009893-685b8c3de7cc?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_11.jpg": "https://images.unsplash.com/photo-1612140417865-c33b49e17bfa?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_12.jpg": "https://images.unsplash.com/photo-1562916667527-375ba381fcad?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_13.jpg": "https://images.unsplash.com/photo-1598284583921-25501fb33139?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_14.jpg": "https://images.unsplash.com/photo-1570208226065-27a1f6a62372?q=80&w=800&auto=format&fit=crop",
    "bg_fuji_15.jpg": "https://images.unsplash.com/photo-1545622879-11ba246830f1?q=80&w=800&auto=format&fit=crop",
    
    # ОСТАЛЬНЫЕ ФОНЫ
    "bg_sakura.jpg": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=800&auto=format&fit=crop",
    "bg_night.jpg": "https://images.unsplash.com/photo-1542931287-023b922fa89b?q=80&w=800&auto=format&fit=crop",
    "bg_temple.jpg": "https://images.unsplash.com/photo-1590559899731-a382839cecdf?q=80&w=800&auto=format&fit=crop",
    "bg_cyber.jpg": "https://images.unsplash.com/photo-1601042879364-f3947d3f9c16?q=80&w=800&auto=format&fit=crop",
    "bg_tokyo.jpg": "https://images.unsplash.com/photo-1503899036067-7c5f3e9b177d?q=80&w=800&auto=format&fit=crop",
    "bg_bamboo.jpg": "https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?q=80&w=800&auto=format&fit=crop",
    "bg_neon.jpg": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?q=80&w=800&auto=format&fit=crop",
    "bg_anime_sky.jpg":"https://images.unsplash.com/photo-1560930950-5cc20e980f98?q=80&w=800&auto=format&fit=crop",
    
    # ИКОНКИ
    "icon_star.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Star/3D/star_3d.png",
    "icon_rocket.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Rocket/3D/rocket_3d.png",
    "icon_fire.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Fire/3D/fire_3d.png",
    "icon_medal.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/1st%20place%20medal/3D/1st_place_medal_3d.png",
    "icon_trophy.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Trophy/3D/trophy_3d.png",
    "icon_crown.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Crown/3D/crown_3d.png",
    "icon_book.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Open%20book/3D/open_book_3d.png",
    "icon_brain.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Brain/3D/brain_3d.png",
    "icon_gem.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Gem%20stone/3D/gem_stone_3d.png",
    "icon_lightning.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/High%20voltage/3D/high_voltage_3d.png",
    "icon_target.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Direct%20hit/3D/direct_hit_3d.png",
    "icon_scroll.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Scroll/3D/scroll_3d.png",
    "icon_owl.png": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Owl/3D/owl_3d.png"
}

def get_asset(filename: str) -> Image.Image:
    filepath = ASSETS_DIR / filename
    if not filepath.exists():
        try:
            req = urllib.request.Request(ASSETS_URLS[filename], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(filepath, 'wb') as f: f.write(response.read())
        except Exception:
            img = Image.new('RGBA', (200, 200), (0,0,0,0))
            ImageDraw.Draw(img).ellipse([20,20,180,180], fill=(99,102,241,180))
            return img
    return Image.open(filepath)

_font_cache = {}

def load_font(size: int, is_japanese: bool = False) -> ImageFont.FreeTypeFont:
    """Загружает шрифт с кэшированием."""
    cache_key = f"{size}_{is_japanese}"
    if cache_key in _font_cache: 
        return _font_cache[cache_key]

    fonts_jp = [
        FONTS_DIR / "NotoSansCJKjp-Bold.otf",
        FONTS_DIR / "NotoSansJP-Bold.ttf",
        Path("C:/Windows/Fonts/meiryo.ttc"),      
        Path("C:/Windows/Fonts/msgothic.ttc"),    
        Path("C:/Windows/Fonts/YuGothB.ttc"),     
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"), 
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc") 
    ]
    fonts_ru = [
        FONTS_DIR / "NotoSans-Bold.ttf",
        Path("C:/Windows/Fonts/segoeui.ttf"),     
        Path("C:/Windows/Fonts/arialbd.ttf"),     
        Path("/System/Library/Fonts/Supplemental/Arial.ttf") 
    ]

    font_list = fonts_jp if is_japanese else fonts_ru
    
    for font_path in font_list:
        if font_path.exists():
            try:
                font = ImageFont.truetype(str(font_path), size)
                _font_cache[cache_key] = font
                return font
            except Exception:
                continue
    
    # Если ничего не нашли, используем дефолтный шрифт
    font = ImageFont.load_default()
    _font_cache[cache_key] = font
    return font


def get_cyrillic_font(size: int) -> ImageFont.FreeTypeFont:
    """Получить кириллический шрифт."""
    return load_font(size, False)


def get_japanese_font(size: int) -> ImageFont.FreeTypeFont:
    """Получить японский шрифт."""
    return load_font(size, True)

def get_cyrillic_font(size: int): return load_font(size, False)
def get_japanese_font(size: int): return load_font(size, True)

def clean_username(name: str) -> str:
    if not name: return "Ученик"
    cleaned = [c for c in name if unicodedata.category(c).startswith('L') or unicodedata.category(c).startswith('N') or c == ' ']
    res = "".join(cleaned).strip()
    return res[:15] if res else "Ученик"

def create_photographic_bg(filename: str, width: int, height: int, darken: int = 60) -> Image.Image:
    bg = get_asset(filename).convert("RGBA")
    bg_ratio = bg.width / bg.height
    target_ratio = width / height
    if bg_ratio > target_ratio:
        new_w = int(height * bg_ratio)
        bg = bg.resize((new_w, height), Image.Resampling.LANCZOS)
        offset = (new_w - width) // 2
        bg = bg.crop((offset, 0, offset + width, height))
    else:
        new_h = int(width / bg_ratio)
        bg = bg.resize((width, new_h), Image.Resampling.LANCZOS)
        offset = (new_h - height) // 2
        bg = bg.crop((0, offset, width, offset + height))
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, darken))
    return Image.alpha_composite(bg, overlay)

def draw_glass_card(target_img: Image.Image, coords: list, radius: int):
    x1, y1, x2, y2 = coords
    width, height = target_img.size
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([x1+10, y1+20, x2+10, y2+20], radius=radius, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=30))
    target_img.paste(shadow, (0, 0), shadow)
    
    box = (x1, y1, x2, y2)
    bg_crop = target_img.crop(box)
    blurred_crop = bg_crop.filter(ImageFilter.GaussianBlur(radius=15))
    target_img.paste(blurred_crop, box)
    
    glass_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glass_draw = ImageDraw.Draw(glass_layer)
    glass_draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=(255, 255, 255, 215), outline=(255, 255, 255, 255), width=2)
    target_img.paste(glass_layer, (0, 0), glass_layer)
    return ImageDraw.Draw(target_img)

def get_text_size(draw: ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_text_centered(draw: ImageDraw, text: str, y: int, width: int, font: ImageFont.FreeTypeFont, fill: tuple):
    x = (width - get_text_size(draw, text, font)[0]) // 2
    draw.text((x, y), text, font=font, fill=fill)

def make_grayscale_icon(icon: Image.Image) -> Image.Image:
    alpha = icon.split()[3]
    gray = ImageOps.grayscale(icon).convert("RGBA")
    gray.putalpha(alpha.point(lambda p: int(p * 0.4)))
    return gray

def draw_progress_bar(draw: ImageDraw, x: int, y: int, width: int, height: int, progress: float, bg_color: tuple, fill_color: tuple):
    radius = height // 2
    draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=bg_color)
    fill_w = int(width * min(max(progress, 0), 1.0))
    if fill_w > radius * 2: draw.rounded_rectangle([x, y, x + fill_w, y + height], radius=radius, fill=fill_color)
    elif fill_w > 0: draw.ellipse([x, y, x + height, y + height], fill=fill_color)

def draw_circular_progress(target_img: Image.Image, cx: int, cy: int, radius: int, thickness: int, progress: float, bg_color: tuple, fg_color: tuple):
    scale = 4
    size = (radius + thickness) * 2 * scale
    hr_img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(hr_img)
    center = size // 2
    r = radius * scale
    t = thickness * scale
    bbox = [center - r, center - r, center + r, center + r]
    draw.arc(bbox, 0, 360, fill=bg_color, width=t)
    if progress > 0:
        angle = int(360 * min(progress, 1.0))
        draw.arc(bbox, -90, -90 + angle, fill=fg_color, width=t)
        r_center = r - t / 2
        cap_r = t / 2
        draw.ellipse([center - cap_r, center - r_center - cap_r, center + cap_r, center - r_center + cap_r], fill=fg_color)
        angle_rad = math.radians(-90 + angle)
        end_cx = center + r_center * math.cos(angle_rad)
        end_cy = center + r_center * math.sin(angle_rad)
        draw.ellipse([end_cx - cap_r, end_cy - cap_r, end_cx + cap_r, end_cy + cap_r], fill=fg_color)
    hr_img = hr_img.resize((size // scale, size // scale), Image.Resampling.LANCZOS)
    target_img.paste(hr_img, (cx - size//scale//2, cy - size//scale//2), hr_img)

def draw_pill_label(draw: ImageDraw, img_w: Image.Image, text: str, x: int, y: int, font: ImageFont.FreeTypeFont, bg_color: tuple, text_color: tuple):
    tw, th = get_text_size(draw, text, font)
    pad_x, pad_y = 12, 6
    overlay = Image.new('RGBA', img_w.size, (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(overlay)
    c_draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + th + pad_y * 2], radius=(th + pad_y*2)//2, fill=bg_color)
    c_draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=text_color)
    img_w.paste(overlay, (0, 0), overlay)
    return tw + pad_x * 2

def get_league_info(xp: int) -> tuple:
    thresholds = [
        (0, "Новичок", 1, (148, 163, 184)), (100, "Ученик", 2, (100, 116, 139)), (500, "Искатель", 3, (120, 113, 108)),
        (1000, "Странник", 4, (168, 162, 158)), (1500, "Кохай", 5, (250, 204, 21)), (2500, "Сэмпай", 6, (234, 179, 8)),
        (4800, "Мечник", 7, (202, 138, 4)), (8000, "Самурай", 8, (161, 98, 7)), (12000, "Ронин", 9, (248, 113, 113)),
        (18000, "Асигару", 10, (239, 68, 68)), (25000, "Буси", 11, (220, 38, 38)), (35000, "Мастер", 12, (185, 28, 28)),
        (50000, "Сенсей", 13, (192, 132, 252)), (70000, "Шихан", 14, (168, 85, 247)), (100000, "Даймё", 15, (147, 51, 234)),
        (130000, "Сёгун", 16, (126, 34, 206)), (170000, "Тэнно", 17, (96, 165, 250)), (230000, "Герой", 18, (59, 130, 246)),
        (300000, "Полубог", 19, (37, 99, 235)), (500000, "Легенда", 20, (29, 78, 216)), (1000000, "Ками", 21, (251, 191, 36)),
    ]
    for xp_req, name, lvl, color in reversed(thresholds):
        if xp >= xp_req: return name, lvl, color
    return "Новичок", 1, (148, 163, 184)


def create_welcome_banner(username: str, level: int, xp: int, streak: int, avatar_bytes: bytes = None, width: int = 800, height: int = 440) -> bytes:
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("menu", "bg_sakura.jpg"), width, height, darken=80)
    draw = ImageDraw.Draw(img)
    safe_name = clean_username(username)
    
    league_name, frame_num, league_color = get_league_info(xp)
    FRAME_SETTINGS = {6: (60, -4, 4)}
    FRAME_SIZE = 120 
    av_size, shift_x, shift_y = FRAME_SETTINGS.get(frame_num, (68, 0, 0)) 
    
    av_img = Image.new('RGBA', (av_size, av_size), (226, 232, 240, 255))
    if avatar_bytes:
        try:
            raw_av = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
            av_img = ImageOps.fit(raw_av, (av_size, av_size), Image.Resampling.LANCZOS)
        except: pass
    else:
        av_draw = ImageDraw.Draw(av_img)
        av_draw.rectangle([0, 0, av_size, av_size], fill=league_color)
        initial = safe_name[0].upper() if safe_name and safe_name != "Ученик" else "?"
        tw, th = get_text_size(av_draw, initial, get_cyrillic_font(30))
        av_draw.text(((av_size-tw)//2, (av_size-th)//2 - 2), initial, font=get_cyrillic_font(30), fill=(255,255,255))
        
    mask = Image.new("L", (av_size, av_size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, av_size, av_size), fill=255)
    
    composite_layer = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE), (0,0,0,0))
    offset = (FRAME_SIZE - av_size) // 2
    final_av_x = offset + shift_x
    final_av_y = offset + shift_y
    composite_layer.paste(av_img, (final_av_x, final_av_y), mask)
    
    frame_path = ASSETS_DIR / f"frame_{frame_num}.png"
    if frame_path.exists():
        frame_img = Image.open(frame_path).convert("RGBA")
        frame_img = frame_img.resize((FRAME_SIZE, FRAME_SIZE), Image.Resampling.LANCZOS)
        composite_layer.paste(frame_img, (0, 0), frame_img)
    else:
        dr = ImageDraw.Draw(composite_layer)
        dr.arc([final_av_x - 2, final_av_y - 2, final_av_x + av_size + 2, final_av_y + av_size + 2], 0, 360, fill=league_color, width=3)
    
    name_font = get_cyrillic_font(36)
    name_w, _ = get_text_size(draw, f"Привет, {safe_name}!", name_font)
    total_w = FRAME_SIZE + 20 + name_w 
    start_x = (width - total_w) // 2
    
    img.paste(composite_layer, (start_x, 25), composite_layer)
    draw.text((start_x + FRAME_SIZE + 20, 60), f"Привет, {safe_name}!", font=name_font, fill=(255, 255, 255))

    c_draw = draw_glass_card(img, [30, 160, width - 30, height - 30], radius=25)
    col_width = (width - 60) // 3
    
    icons = [(get_asset("icon_crown.png" if frame_num > 10 else "icon_star.png"), "РАНГ", league_name), (get_asset("icon_rocket.png"), "ОПЫТ", str(xp)), (get_asset("icon_fire.png"), "СЕРИЯ", str(streak))]
    for i, (icon_img, label, value) in enumerate(icons):
        cx = 30 + col_width // 2 + i * col_width
        icon_size = 70
        icon_resized = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        img.paste(icon_resized, (cx - icon_size//2, 185), icon_resized)
        val_font_size = 32 if len(value) <= 6 else 24
        c_draw.text((cx, 280), value, font=get_cyrillic_font(val_font_size), fill=(30, 41, 59), anchor="mm")
        c_draw.text((cx, 315), label, font=get_cyrillic_font(14), fill=(100, 116, 139), anchor="mm")
        
    c_draw.rectangle([60, 350, width - 60, 352], fill=(226, 232, 240))
    if frame_num == 1: motto = "Твой путь к японскому начинается здесь"
    else: motto = random.choice(["Даже путь в 1000 ри начинается с первого шага", "Упади семь раз, поднимись восемь", "Каждый иероглиф — это маленькая история", "Лучшее время для изучения японского — сегодня", "Вода точит камень, а регулярность — кандзи", "Твои знания растут с каждой карточкой", "Ошибки — это ступеньки к совершенству", "Постоянство — ключ к свободной речи"])
        
    draw_text_centered(c_draw, motto, 370, width, get_cyrillic_font(20), (30, 41, 59))
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()


def create_achievements_card(user_data: dict, page: int = 0, width: int = 800, height: int = 720) -> bytes:
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("achievements", "bg_fuji_1.jpg"), width, height, darken=100)
    draw = draw_glass_card(img, [30, 80, width - 30, height - 30], radius=30)
    draw_text_centered(ImageDraw.Draw(img), "ТВОИ ДОСТИЖЕНИЯ", 25, width, get_cyrillic_font(32), (255, 255, 255))
    
    xp, best_streak, cards_learned = user_data.get('xp', 0), user_data.get('best_streak', 0), user_data.get('total_learned', 0)
    best_blitz, voice_msgs = user_data.get('best_blitz_score', 0), user_data.get('voice_msgs', 0)
    is_night_owl, grammar_perfect = user_data.get('night_owl', 0) > 0, user_data.get('grammar_perfect', 0)
    
    all_achievements = [
        ("Новичок", xp >= 100, "100 XP", get_asset("icon_medal.png")), ("Студент", xp >= 500, "500 XP", get_asset("icon_trophy.png")), ("Мастер", xp >= 1500, "1500 XP", get_asset("icon_crown.png")),
        ("Огонёк", best_streak >= 3, "3 Дня", get_asset("icon_star.png")), ("Пламя", best_streak >= 10, "10 Дней", get_asset("icon_fire.png")), ("Легенда", best_streak >= 30, "30 Дней", get_asset("icon_rocket.png")),
        ("Словарь", cards_learned >= 20, "20 Слов", get_asset("icon_book.png")), ("Полиглот", cards_learned >= 100, "100 Слов", get_asset("icon_brain.png")), ("Гуру", cards_learned >= 250, "250 Слов", get_asset("icon_scroll.png")),
        ("Рывок", best_blitz >= 10, "Блиц 10", get_asset("icon_lightning.png")), ("Спринтер", best_blitz >= 25, "Блиц 25", get_asset("icon_target.png")), ("Флэш", best_blitz >= 50, "Блиц 50", get_asset("icon_gem.png")),
        ("Болтун", voice_msgs >= 1, "1 Голосовое ИИ", get_asset("icon_star.png")), ("Оратор", voice_msgs >= 10, "10 Голосовых ИИ", get_asset("icon_medal.png")), ("Диктор", voice_msgs >= 50, "50 Голосовых ИИ", get_asset("icon_crown.png")),
        ("Сова", is_night_owl, "Играть ночью", get_asset("icon_owl.png")), ("Энтузиаст", xp >= 5000, "5000 XP", get_asset("icon_trophy.png")), ("Сенсей", xp >= 10000, "10000 XP", get_asset("icon_gem.png")),
        ("Новичок Грамматики", grammar_perfect >= 1, "1 Грамматика без ошибок", get_asset("icon_book.png")), ("Знаток Грамматики", grammar_perfect >= 5, "5 Грамматик", get_asset("icon_scroll.png")), ("Лингвист", grammar_perfect >= 15, "15 Грамматик", get_asset("icon_brain.png")),
        ("Вундеркинд", cards_learned >= 500, "500 Слов", get_asset("icon_rocket.png")), ("Вспышка", best_blitz >= 75, "Блиц 75", get_asset("icon_lightning.png")), ("Машина", best_streak >= 100, "100 Дней", get_asset("icon_fire.png")),
    ]
    page_items = all_achievements[page * 12 : (page + 1) * 12]
    cols, cell_w, cell_h = 3, (width - 100) // 3, 140
    start_x, start_y = 50, 105
    icon_size = 65
    
    for i, (title, is_unlocked, req_text, icon_source) in enumerate(page_items):
        cx, y = start_x + (i % cols) * cell_w + cell_w // 2, start_y + (i // cols) * cell_h
        icon_resized = icon_source.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        if is_unlocked:
            img.paste(icon_resized, (cx - icon_size//2, y + 15), icon_resized)
            draw.text((cx, y + 100), title, font=get_cyrillic_font(20), fill=(30, 41, 59), anchor="mm")
            draw.text((cx, y + 125), req_text, font=get_cyrillic_font(14), fill=(34, 197, 94), anchor="mm")
        else:
            gray_icon = make_grayscale_icon(icon_resized)
            img.paste(gray_icon, (cx - icon_size//2, y + 15), gray_icon)
            draw.text((cx, y + 100), "Закрыто", font=get_cyrillic_font(20), fill=(148, 163, 184), anchor="mm")
            draw.text((cx, y + 125), f"Нужно: {req_text}", font=get_cyrillic_font(14), fill=(148, 163, 184), anchor="mm")
            
    draw_text_centered(draw, f"Страница {page+1} из 2", height - 40, width, get_cyrillic_font(16), (148, 163, 184))
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_stats_card(xp, level, streak, best_streak, cards_learned, total_possible, progress, width=800, height=520) -> bytes:
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("stats", "bg_night.jpg"), width, height, darken=120)
    draw = draw_glass_card(img, [30, 80, width - 30, height - 30], radius=30)
    draw_text_centered(ImageDraw.Draw(img), "ТВОЯ СТАТИСТИКА", 25, width, get_cyrillic_font(32), (255, 255, 255))
    overall_pct = cards_learned / total_possible if total_possible > 0 else 0
    circle_x, circle_y = 170, 210
    draw_circular_progress(img, circle_x, circle_y, radius=70, thickness=16, progress=overall_pct, bg_color=(226, 232, 240, 150), fg_color=(99, 102, 241))
    draw.text((circle_x, circle_y - 10), f"{int(overall_pct * 100)}%", font=get_cyrillic_font(36), fill=(30, 41, 59), anchor="mm")
    draw.text((circle_x, circle_y + 20), "изучено", font=get_cyrillic_font(14), fill=(100, 116, 139), anchor="mm")
    metrics = [("Уровень", str(level), (99, 102, 241), 320, 140), ("Опыт (XP)", str(xp), (245, 158, 11), 540, 140), ("Серия", f"{streak} дн.", (34, 197, 94), 320, 240), ("Лучшая", f"{best_streak} дн.", (34, 197, 94), 540, 240)]
    for lbl, val, col, x, y in metrics:
        draw.text((x, y), val, font=get_cyrillic_font(32), fill=col)
        draw.text((x, y + 40), lbl, font=get_cyrillic_font(14), fill=(100, 116, 139))
    draw.rectangle([60, 330, width - 60, 332], fill=(226, 232, 240))
    sy = 350
    for name, keys, total in [("Хирагана/Катакана", ["hiragana", "katakana"], 92),("JLPT N5 (База)", ["kanji_n5", "words_n5"], 24),("JLPT N4 (Продолж.)", ["kanji_n4", "words_n4"], 12)]:
        learned = sum(progress.get(k, 0) for k in keys)
        draw.text((60, sy), name, font=get_cyrillic_font(18), fill=(30, 41, 59))
        draw.text((width - 120, sy+4), f"{learned}/{total}", font=get_cyrillic_font(14), fill=(100, 116, 139))
        pw, p_pct = width - 180, learned / total if total > 0 else 0
        draw.rounded_rectangle([60, sy + 30, 60 + pw, sy + 40], radius=5, fill=(226, 232, 240))
        if p_pct > 0: draw.rounded_rectangle([60, sy + 30, 60 + int(pw * p_pct), sy + 40], radius=5, fill=(34, 197, 94))
        sy += 50
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_leaderboard_card(players: list, current_user_id: int, title: str, score_key: str, width=800) -> bytes:
    ROW_H, FRAME_SIZE = 70, 60   
    FRAME_SETTINGS = {6: (30, -2, 2)}
    height = 140 + len(players) * ROW_H
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("leaderboard", "bg_cyber.jpg"), width, height, darken=120)
    draw = draw_glass_card(img, [30, 80, width - 30, height - 30], radius=30)
    draw_text_centered(ImageDraw.Draw(img), title, 25, width, get_cyrillic_font(32), (255, 255, 255))
    
    list_y = 100
    for i, p in enumerate(players):
        rank_str, name = f"{i+1}.", clean_username(p['username'])
        if name == "Ученик" and p['username'] == "": name = f"ID {p['user_id']}"
        name_color = (99, 102, 241) if p['user_id'] == current_user_id else (30, 41, 59)
        score_val, user_xp = p.get(score_key, 0), p.get('xp', 0)
        league_name, frame_num, league_color = get_league_info(user_xp)
        av_size, shift_x, shift_y = FRAME_SETTINGS.get(frame_num, (34, 0, 0))

        draw.text((50, list_y + 20), rank_str, font=get_cyrillic_font(22), fill=(100, 116, 139))
        base_x, base_y, offset = 100, list_y + (ROW_H - FRAME_SIZE) // 2, (FRAME_SIZE - av_size) // 2
        av_img = Image.new('RGBA', (av_size, av_size), (226, 232, 240, 255))
        if p.get('avatar_bytes'):
            try: av_img = ImageOps.fit(Image.open(io.BytesIO(p['avatar_bytes'])).convert("RGBA"), (av_size, av_size), Image.Resampling.LANCZOS)
            except: pass
        else:
            av_draw = ImageDraw.Draw(av_img)
            av_draw.rectangle([0, 0, av_size, av_size], fill=league_color)
            initial = name[0].upper() if name else "?"
            tw, th = get_text_size(av_draw, initial, get_cyrillic_font(18))
            av_draw.text(((av_size-tw)//2, (av_size-th)//2 - 2), initial, font=get_cyrillic_font(18), fill=(255,255,255))
            
        mask = Image.new("L", (av_size, av_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, av_size, av_size), fill=255)
        
        composite_layer = Image.new('RGBA', (FRAME_SIZE, FRAME_SIZE), (0,0,0,0))
        final_av_x, final_av_y = offset + shift_x, offset + shift_y
        composite_layer.paste(av_img, (final_av_x, final_av_y), mask)
        
        frame_path = ASSETS_DIR / f"frame_{frame_num}.png"
        if frame_path.exists():
            frame_img = Image.open(frame_path).convert("RGBA").resize((FRAME_SIZE, FRAME_SIZE), Image.Resampling.LANCZOS)
            composite_layer.paste(frame_img, (0, 0), frame_img)
        else: ImageDraw.Draw(composite_layer).arc([final_av_x - 2, final_av_y - 2, final_av_x + av_size + 2, final_av_y + av_size + 2], 0, 360, fill=league_color, width=2)

        img.paste(composite_layer, (base_x, base_y), composite_layer)
        draw.text((180, list_y + 20), name, font=get_cyrillic_font(22), fill=name_color)
        
        if score_key == "xp":
            draw_pill_label(draw, img, league_name, 380, list_y + 20, get_cyrillic_font(14), league_color, (255,255,255))
            draw.text((width - 150, list_y + 22), f"{score_val} XP", font=get_cyrillic_font(20), fill=(245, 158, 11))
        else:
            draw.text((width - 150, list_y + 22), f"Блиц: {score_val}", font=get_cyrillic_font(20), fill=(245, 158, 11))
        
        if i < len(players) - 1: draw.rectangle([60, list_y + ROW_H - 2, width - 60, list_y + ROW_H - 1], fill=(226, 232, 240))
        list_y += ROW_H
        
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_mode_select_card(action: str, width: int = 800, height: int = 400) -> bytes:
    """
    Создает красивую карточку выбора режима с правильными отступами.
    """
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("menu", "bg_sakura.jpg"), width, height, darken=130)
    
    # Стеклянная карточка с большими отступами
    card_margin = 50
    card_top = 60
    card_bottom = height - 50
    
    draw = draw_glass_card(img, [card_margin, card_top, width - card_margin, card_bottom], radius=25)
    
    # Определяем контент по типу действия
    if action == "learn":
        title = "ПРАКТИКА"
        desc = "Реши тесты и проверь знания"
        subtitle = "Случайные карточки для тренировки"
        icon_name = "icon_rocket.png"
        accent_color = (99, 102, 241)
    elif action == "review":
        title = "ПОВТОРЕНИЕ"
        desc = "Умный алгоритм SM-2"
        subtitle = "Интервальное повторение"
        icon_name = "icon_brain.png"
        accent_color = (168, 85, 247)
    elif action == "alphabet":
        title = "ЯПОНСКАЯ АЗБУКА"
        desc = "Хирагана и Катакана"
        subtitle = "Основа японского языка"
        icon_name = "icon_book.png"
        accent_color = (236, 72, 153)
    elif action == "jlpt":
        title = "УРОВНИ JLPT"
        desc = "Кандзи и Слова"
        subtitle = "N5, N4 и выше"
        icon_name = "icon_crown.png"
        accent_color = (245, 158, 11)
    else:
        title = "ВЫБЕРИ РАЗДЕЛ"
        desc = "Продолжай изучение"
        subtitle = "Выбери категорию"
        icon_name = "icon_star.png"
        accent_color = (34, 197, 94)

    # Загружаем иконку
    try:
        icon = get_asset(icon_name)
        icon_size = 100
        icon_resized = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icon_x = card_margin + 40
        icon_y = card_top + (card_bottom - card_top - icon_size) // 2
        img.paste(icon_resized, (icon_x, icon_y), icon_resized)
        text_x = icon_x + icon_size + 40
    except:
        text_x = card_margin + 40

    # Текстовый блок
    text_area_top = card_top + 40
    
    # Заголовок
    title_font = get_cyrillic_font(36)
    draw.text((text_x, text_area_top), title, font=title_font, fill=accent_color)

    # Разделительная линия
    line_y = text_area_top + 50
    draw.rectangle([text_x, line_y, text_x + 250, line_y + 3], fill=accent_color)

    # Описание
    desc_font = get_cyrillic_font(22)
    desc_y = line_y + 20
    draw.text((text_x, desc_y), desc, font=desc_font, fill=(30, 41, 59))

    # Подзаголовок
    subtitle_font = get_cyrillic_font(16)
    subtitle_y = desc_y + 35
    draw.text((text_x, subtitle_y), subtitle, font=subtitle_font, fill=(100, 116, 139))

    # Подсказка внизу карточки
    hint_y = card_bottom - 40
    hint_font = get_cyrillic_font(14)
    draw.text((text_x, hint_y), "⬇️ Выберите на клавиатуре ниже", font=hint_font, fill=(148, 163, 184))

    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_study_card(symbol, reading, hint, card_type, group_name, index, total, audio_hint="", width=800, height=600):
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("study", "bg_temple.jpg"), width, height, darken=130)
    draw = draw_glass_card(img, [40, 40, width - 40, height - 40], radius=30)
    draw.text((70, 70), group_name, font=get_cyrillic_font(20), fill=(100, 116, 139))
    draw.text((width - 120, 70), f"{index} / {total}", font=get_cyrillic_font(20), fill=(100, 116, 139))
    draw_progress_bar(draw, 70, 105, width - 140, 8, index/total, (226, 232, 240), (34, 197, 94))
    font_size = 180 if len(symbol) <= 2 else (120 if len(symbol) <= 4 else (60 if len(symbol) <= 15 else 40))
    draw.text((width//2, 230), symbol, font=get_japanese_font(font_size), fill=(30, 41, 59), anchor="mm")
    draw.text((width//2, 400), reading, font=get_cyrillic_font(48), fill=(99, 102, 241), anchor="mm")
    if hint: draw.text((width//2, 480), hint, font=get_cyrillic_font(20), fill=(100, 116, 139), anchor="mm")
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_groups_card(card_type, groups, width=800, height=750):
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("study", "bg_temple.jpg"), width, height, darken=130)
    draw = ImageDraw.Draw(img)
    draw_text_centered(draw, "ВЫБЕРИ УРОК", 30, width, get_cyrillic_font(36), (255, 255, 255))
    cw = (width - 90) // 2
    for i, (key, group) in enumerate(groups):
        x, y = 30 + (i % 2) * (cw + 30), 110 + (i // 2) * 110
        if y + 100 > height: break
        c_draw = draw_glass_card(img, [x, y, x + cw, y + 95], radius=20)
        c_draw.text((x + 20, y + 15), group["name"], font=get_cyrillic_font(22), fill=(30, 41, 59))
        c_draw.text((x + 20, y + 55), " ".join(group["chars"][:5]), font=get_japanese_font(18), fill=(99, 102, 241))
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_full_table(card_type, chars, readings, title="Таблица", width=800):
    cols, cell_h = 5, 90
    rows = math.ceil(len(chars) / cols)
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("study", "bg_temple.jpg"), width, 100 + rows * cell_h + 40, darken=150)
    draw = ImageDraw.Draw(img)
    draw_text_centered(draw, title.upper(), 35, width, get_cyrillic_font(36), (255, 255, 255))
    cw = (width - 60) // cols
    for i, (char, read) in enumerate(zip(chars, readings)):
        x, y = 30 + (i % cols) * cw, 100 + (i // cols) * cell_h
        draw_glass_card(img, [x+5, y+5, x+cw-5, y+cell_h-5], 15)
        c_font_size = 36 if len(char) < 4 else 18
        draw.text((x + cw//2, y + 35), char, font=get_japanese_font(c_font_size), fill=(30, 41, 59), anchor="mm")
        draw.text((x + cw//2, y + 70), read[:8], font=get_cyrillic_font(14), fill=(99, 102, 241), anchor="mm")
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_quiz_card(symbol, card_type, width=800, height=450):
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("quiz", "bg_neon.jpg"), width, height, darken=120)
    draw = draw_glass_card(img, [50, 50, width - 50, height - 40], radius=30)
    title_text = "ГРАММАТИКА" if card_type == "grammar_n5" else "ТЕСТ"
    draw_text_centered(draw, title_text, 75, width, get_cyrillic_font(18), (99, 102, 241))
    font_size = 180 if len(symbol) <= 2 else (100 if len(symbol) <= 4 else (60 if len(symbol) <= 10 else 40))
    sw, sh = get_text_size(draw, symbol, get_japanese_font(font_size))
    draw.text(((width - sw)//2, 120 + (180 - font_size)//2), symbol, font=get_japanese_font(font_size), fill=(30, 41, 59))
    hint_txt = "Вставьте пропущенную частицу" if card_type == "grammar_n5" else "Выбери правильный вариант"
    draw_text_centered(draw, hint_txt, height - 90, width, get_cyrillic_font(22), (100, 116, 139))
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()


# === СТАТИЧНАЯ КАРТОЧКА РЕЗУЛЬТАТА (Идеальный размер 800x440) ===
def create_result_card(correct, symbol, answer, xp_gained=0, streak=0, width=800, height=440):
    bg_name = SCREEN_BACKGROUNDS.get("quiz", "bg_neon.jpg") if correct else "bg_night.jpg"
    img = create_photographic_bg(bg_name, width, height, darken=120)
    
    # Рисуем стеклянную карточку
    draw = draw_glass_card(img, [40, 40, width - 40, height - 40], radius=30)
    
    # Подготавливаем шрифты
    jp_font = get_japanese_font(40 if len(symbol) > 10 else (50 if len(symbol) > 4 else 60))
    is_jap_ans = bool(re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', answer))
    ans_font = get_japanese_font(40 if len(answer) > 10 else 50) if is_jap_ans else get_cyrillic_font(40 if len(answer) > 10 else 50)
    
    # Заголовок
    title_text = "ОТЛИЧНО!" if correct else "НУЖНО ЗАПОМНИТЬ"
    title_color = (34, 197, 94) if correct else (239, 68, 68)
    draw_text_centered(draw, title_text, 75, width, get_cyrillic_font(36), title_color)
    
    # Центрируем текст уравнения: Символ = Перевод
    sym_w, _ = get_text_size(draw, symbol, jp_font)
    eq_w, _ = get_text_size(draw, " = ", get_cyrillic_font(40))
    ans_w, _ = get_text_size(draw, answer, ans_font)
    
    total_w = sym_w + eq_w + ans_w
    start_x = (width - total_w) // 2
    
    # Рисуем само уравнение
    y_pos = 170
    draw.text((start_x, y_pos), symbol, font=jp_font, fill=(30, 41, 59))
    draw.text((start_x + sym_w, y_pos), " = ", font=get_cyrillic_font(40), fill=(100, 116, 139))
    draw.text((start_x + sym_w + eq_w, y_pos), answer, font=ans_font, fill=(30, 41, 59))
    
    # Нижний блок с XP и Серией
    if correct:
        draw.text((width//2 - 80, 310), f"+{xp_gained} XP", font=get_cyrillic_font(24), fill=(99, 102, 241), anchor="mm")
        if streak > 0: 
            draw.text((width//2 + 80, 310), f"Серия {streak}", font=get_cyrillic_font(24), fill=(245, 158, 11), anchor="mm")
    else:
        draw_text_centered(draw, "Карточка скоро повторится", 310, width, get_cyrillic_font(20), (100, 116, 139))
            
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_dictionary_card(search_query: str, found_items: list, page: int = 0, width=800) -> bytes:
    page_items = found_items[page*3 : (page+1)*3]
    items_count = max(len(page_items), 1)
    height = 250 + (items_count * 150)
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("dictionary", "bg_bamboo.jpg"), width, height, darken=130)
    draw = draw_glass_card(img, [30, 80, width - 30, height - 30], radius=30)
    draw_text_centered(ImageDraw.Draw(img), f"ПОИСК: {search_query.upper()}", 30, width, get_cyrillic_font(28), (255, 255, 255))
    if not found_items: draw_text_centered(draw, "Ничего не найдено", height // 2 - 20, width, get_cyrillic_font(28), (100, 116, 139))
    else:
        start_y = 110
        for i, item in enumerate(page_items):
            sym = item['symbol']
            sym_font = 70 if len(sym) < 4 else 40
            draw_text_centered(draw, sym, start_y, width, get_japanese_font(sym_font), (30, 41, 59))
            draw_text_centered(draw, item['reading'], start_y + 80, width, get_cyrillic_font(28), (99, 102, 241))
            t_name = {"hiragana": "Хирагана", "katakana": "Катакана", "kanji": "Кандзи", "words": "Слово"}.get(item['type'], "Символ")
            draw_pill_label(draw, img, t_name, width//2 - get_text_size(draw, t_name, get_cyrillic_font(14))[0]//2 - 12, start_y + 125, get_cyrillic_font(14), (226, 232, 240), (100, 116, 139))
            start_y += 150
            if i < items_count - 1: draw.rectangle([100, start_y - 25, width - 100, start_y - 23], fill=(226, 232, 240, 150))
        total_pages = math.ceil(len(found_items) / 3)
        if total_pages > 1: draw_text_centered(draw, f"Страница {page+1} из {total_pages} (Всего: {len(found_items)})", height - 60, width, get_cyrillic_font(16), (148, 163, 184))
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

def create_alphabet_card(width: int = 800, height: int = 420) -> bytes:
    """
    Специальная карточка для раздела Азбуки с правильными отступами.
    """
    img = create_photographic_bg(SCREEN_BACKGROUNDS.get("study", "bg_temple.jpg"), width, height, darken=130)
    
    # Заголовок НАД карточкой (на тёмном фоне)
    header_draw = ImageDraw.Draw(img)
    title_font = get_cyrillic_font(36)
    title_text = "ЯПОНСКАЯ АЗБУКА"
    title_w, title_h = get_text_size(header_draw, title_text, title_font)
    title_x = (width - title_w) // 2
    title_y = 25  # Отступ сверху
    
    # Рисуем заголовок с тенью для читаемости
    header_draw.text((title_x + 2, title_y + 2), title_text, font=title_font, fill=(0, 0, 0, 128))
    header_draw.text((title_x, title_y), title_text, font=title_font, fill=(255, 255, 255))
    
    # Стеклянная карточка НИЖЕ заголовка
    card_top = title_y + title_h + 25
    card_margin = 40
    draw = draw_glass_card(img, [card_margin, card_top, width - card_margin, height - 40], radius=25)
    
    # Иконки азбук
    icon_size = 80
    spacing = 60
    total_icons_width = icon_size * 2 + spacing
    start_x = (width - total_icons_width) // 2
    icons_y = card_top + 30
    
    # Хирагана
    hira_icon = get_asset("icon_book.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(hira_icon, (start_x, icons_y), hira_icon)
    draw.text((start_x + icon_size // 2, icons_y + icon_size + 15), "あ", 
              font=get_japanese_font(36), fill=(236, 72, 153), anchor="mm")
    draw.text((start_x + icon_size // 2, icons_y + icon_size + 55), "Хирагана", 
              font=get_cyrillic_font(16), fill=(100, 116, 139), anchor="mm")
    
    # Катакана
    kata_icon = get_asset("icon_scroll.png").resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    kata_x = start_x + icon_size + spacing
    img.paste(kata_icon, (kata_x, icons_y), kata_icon)
    draw.text((kata_x + icon_size // 2, icons_y + icon_size + 15), "ア", 
              font=get_japanese_font(36), fill=(99, 102, 241), anchor="mm")
    draw.text((kata_x + icon_size // 2, icons_y + icon_size + 55), "Катакана", 
              font=get_cyrillic_font(16), fill=(100, 116, 139), anchor="mm")
    
    # Описание внизу
    desc_y = height - 100
    desc_text = "46 базовых символов в каждой азбуке"
    draw_text_centered(draw, desc_text, desc_y, width, get_cyrillic_font(18), (71, 85, 105))
    
    hint_text = "⬇️ Выберите азбуку для изучения"
    draw_text_centered(draw, hint_text, desc_y + 35, width, get_cyrillic_font(16), (148, 163, 184))

    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='PNG', quality=95)
    return buffer.getvalue()