"""
API для синхронизации Web App с ботом.
Использует Telegram WebApp initData для авторизации.
"""

import hashlib
import hmac
import json
import urllib.parse
import asyncio
import os
import aiohttp
from datetime import datetime
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import get_due_reviews
from srs import process_answer
from data.content import get_content
from config import BOT_TOKEN, DB_PATH
from database import (
    get_or_create_user, get_user_stats, add_xp,
    update_streak, get_card_progress, upsert_card_progress,
    get_top_players, add_daily_progress
)
import aiosqlite
from models import LessonGroup, LessonItem, GrammarPoint, GrammarExample

# --- DB SETUP FOR API ---
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
engine = create_async_engine(DB_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# ------------------------

def verify_telegram_auth(init_data: str) -> dict | None:
    try:
        if not init_data:
            return None
        
        parsed = dict(urllib.parse.parse_qsl(init_data))
        check_hash = parsed.pop('hash', None)
        if not check_hash: return None
        
        # Проверка времени жизни данных (24 часа)
        auth_date = parsed.get('auth_date')
        if auth_date:
            auth_ts = int(auth_date)
            now_ts = int(datetime.now().timestamp())
            if now_ts - auth_ts > 86400: # Данные устарели
                return None
        
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash != check_hash: return None
        return json.loads(parsed.get('user', '{}'))
    except Exception as e:
        return None

async def handle_health_check(request: web.Request) -> web.Response:
    """Проверка работоспособности API"""
    return web.json_response({'status': 'ok', 'timestamp': datetime.now().isoformat()})

async def handle_get_user(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    user_id = user_data.get('id')
    username = user_data.get('first_name', 'User')
    user = await get_or_create_user(user_id, username)
    stats = await get_user_stats(user_id)
    return web.json_response({
        'success': True,
        'user': {
            'id': user_id, 'name': username, 'xp': user.get('xp', 0),
            'streak': user.get('current_streak', 0), 'best_streak': user.get('best_streak', 0),
            'cards_learned': stats.get('total_learned', 0), 'daily_progress': user.get('daily_progress', 0),
            'daily_goal': user.get('daily_goal', 10),
            'coins': user.get('coins', 0),                    # <--- НОВОЕ
            'freezes': user.get('streak_freezes', 0),         # <--- НОВОЕ
            'league': user.get('league', 1),                  # <--- НОВОЕ
            'weekly_xp': user.get('weekly_xp', 0)             # <--- НОВОЕ
        }
    })

async def handle_save_progress(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    user_id = user_data.get('id')
    body = await request.json()
    
    if body.get('action') == 'quiz_complete':
        try:
            correct = int(body.get('correct', 0))
            total = int(body.get('total', 0))
        except (ValueError, TypeError):
            return web.json_response({'error': 'Invalid numbers'}, status=400)
            
        # Валидация данных
        if correct < 0 or total < 0:
            return web.json_response({'error': 'Negative values'}, status=400)
        if correct > total:
            return web.json_response({'error': 'Correct > Total'}, status=400)
        if total > 100: # Защита от накрутки
            return web.json_response({'error': 'Too many questions'}, status=400)
        
        # Обновляем умные карточки в базе
        results = body.get('results', [])
        if isinstance(results, list):
            for res in results:
                if isinstance(res, dict) and 'type' in res and 'char' in res and 'isCorrect' in res:
                    await process_answer(user_id, res['type'], res['char'], res['isCorrect'])
            
        xp_gained = int(correct * 10)
        if xp_gained > 0:
            new_xp = await add_xp(user_id, xp_gained)
            await add_daily_progress(user_id, correct)
        if correct == total and total > 0: await update_streak(user_id, True)
        return web.json_response({'success': True, 'xp_gained': xp_gained})
    return web.json_response({'error': 'Unknown action'}, status=400)


async def handle_get_leaderboard(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not verify_telegram_auth(init_data): return web.json_response({'error': 'Unauthorized'}, status=401)
    players = await get_top_players(20)
    return web.json_response({
        'success': True,
        'players': [{'id': p['user_id'], 'name': p['username'] or 'User', 'xp': p['xp'], 'streak': p['current_streak'], 'league': p.get('league', 1)} for p in players]
    })

async def handle_claim_daily(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    from database import claim_wheel_reward
    import random
    reward = random.choice([10, 15, 20, 25, 30, 50, 75, 100])
    if await claim_wheel_reward(user_data.get('id'), reward):
        return web.json_response({'success': True, 'reward': reward})
    return web.json_response({'success': False, 'error': 'Already claimed'})

async def handle_user_stats(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    stats = await get_user_stats(user_data.get('id'))
    return web.json_response({'success': True, 'stats': {'xp': stats.get('xp', 0), 'streak': stats.get('current_streak', 0), 'best_streak': stats.get('best_streak', 0), 'total_learned': stats.get('total_learned', 0), 'accuracy': stats.get('accuracy', 0), 'by_type': stats.get('cards_by_type', {}), 'best_blitz': stats.get('best_blitz_score', 0), 'voice_msgs': stats.get('voice_msgs', 0)}})

async def handle_tts(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    if not verify_telegram_auth(init_data): return web.json_response({'error': 'Unauthorized'}, status=401)
    text = request.query.get('text', '')
    if not text: return web.json_response({'error': 'No text'}, status=400)
    from audio import generate_japanese_voice
    audio_bytes = await asyncio.to_thread(generate_japanese_voice, text)
    return web.Response(body=audio_bytes, content_type='audio/ogg')

async def handle_setname(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    body = await request.json()
    new_name = body.get('name', '').strip()
    if not new_name: return web.json_response({'error': 'Empty name'}, status=400)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (new_name, user_data.get('id')))
        await db.commit()
    return web.json_response({'success': True})

# === НОВЫЙ ЭНДПОИНТ: БЕЗОПАСНАЯ ЗАГРУЗКА АВАТАРОК ===
async def handle_get_avatar(request: web.Request) -> web.Response:
    user_id = request.match_info.get('user_id')
    default_url = f"https://ui-avatars.com/api/?name=User&background=667eea&color=fff&size=100"
    if not user_id: return web.HTTPFound(default_url)
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUserProfilePhotos?user_id={user_id}&limit=1"
            async with session.get(url) as resp:
                data = await resp.json()
                if data.get("ok") and data["result"]["total_count"] > 0:
                    file_id = data["result"]["photos"][0][0]["file_id"]
                    file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
                    async with session.get(file_url) as resp2:
                        data2 = await resp2.json()
                        if data2.get("ok"):
                            file_path = data2["result"]["file_path"]
                            dl_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                            # Скачиваем картинку на сервер и отдаем пользователю (чтобы не палить токен)
                            async with session.get(dl_url) as resp3:
                                img_bytes = await resp3.read()
                                return web.Response(body=img_bytes, content_type='image/jpeg')
    except Exception:
        pass
    return web.HTTPFound(default_url)

async def handle_get_reviews(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    
    due_cards = await get_due_reviews(user_data.get('id'), 15)
    response_cards = []
    for c in due_cards:
        content_dict = get_content(c['card_type'])
        if c['card_key'] in content_dict:
            response_cards.append({
                'char': c['card_key'], 'reading': content_dict[c['card_key']], 'type': c['card_type']
            })
    return web.json_response({'success': True, 'cards': response_cards})

async def handle_buy_item(request: web.Request) -> web.Response:
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    if not user_data: return web.json_response({'error': 'Unauthorized'}, status=401)
    
    body = await request.json()
    item_id = body.get('item_id')
    price = int(body.get('price', 0))
    
    from database import buy_shop_item
    success = await buy_shop_item(user_data.get('id'), item_id, price)
    return web.json_response({'success': success})

async def handle_log_error(request: web.Request) -> web.Response:
    """Логирование ошибок с клиента"""
    try:
        body = await request.json()
        print(f"🔴 CLIENT ERROR: {body}")
        # Здесь можно добавить запись в файл или БД
        return web.json_response({'status': 'logged'})
    except:
        return web.json_response({'status': 'error'}, status=400)

# --- AUTH ADMIN ---
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "super_secret_admin_key")

async def handle_admin_add_content(request: web.Request) -> web.Response:
    """Добавление контента через админку"""
    # Проверка ключа
    key = request.headers.get("X-Admin-Key")
    if key != ADMIN_SECRET:
        return web.json_response({'error': 'Forbidden'}, status=403)
    
    try:
        data = await request.json()
        category = data.get('category')
        group_key = data.get('group_key')
        char = data.get('char')
        
        if not all([category, group_key, char]):
            return web.json_response({'error': 'Missing fields'}, status=400)
            
        async with async_session() as session:
            # 1. Проверяем/Создаем группу
            result = await session.execute(
                LessonGroup.__table__.select().where(LessonGroup.key == group_key)
            )
            if not result.first():
                group = LessonGroup(
                    key=group_key,
                    category=category,
                    name=f"Group {group_key}", # Можно передавать имя с фронта
                    order_index=99
                )
                session.add(group)
                await session.flush() # Чтобы группа записалась
            
            # 2. Добавляем элемент
            item = LessonItem(
                group_key=group_key,
                char=char,
                reading=data.get('reading', ''),
                meaning=data.get('meaning', ''),
                hint=data.get('hint', ''),
                context=data.get('context', ''),
                order_index=0
            )
            session.add(item)
            await session.commit()
            
        return web.json_response({'success': True})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def handle_admin_add_grammar(request: web.Request) -> web.Response:
    """Добавление грамматики через админку"""
    key = request.headers.get("X-Admin-Key")
    if key != ADMIN_SECRET:
        return web.json_response({'error': 'Forbidden'}, status=403)

    try:
        data = await request.json()
        if not data.get('title') or not data.get('description'):
            return web.json_response({'error': 'Missing fields'}, status=400)
            
        async with async_session() as session:
            # Create Point
            point = GrammarPoint(
                level=data.get('level', 'N5'),
                title=data['title'],
                description=data['description'],
                structure=data.get('structure', '')
            )
            session.add(point)
            await session.flush() # get ID
            
            # Create Examples
            examples = data.get('examples', [])
            for ex in examples:
                g_ex = GrammarExample(
                    grammar_id=point.id,
                    japanese=ex['japanese'],
                    reading=ex.get('reading', ''),
                    translation=ex['translation']
                )
                session.add(g_ex)
                
            await session.commit()
            
        return web.json_response({'success': True})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def handle_get_content(request: web.Request) -> web.Response:
    """Получение контента уроков из БД"""
    category = request.query.get('category')
    
    async with async_session() as session:
        # Fetch groups
        query = LessonGroup.__table__.select()
        if category:
            query = query.where(LessonGroup.category == category)
        
        result = await session.execute(query)
        groups = []
        for row in result.mappings():
            groups.append(dict(row))
        
        # Fetch items
        # Если нужна оптимизация, можно фильтровать по group_key
        item_query = LessonItem.__table__.select()
        item_result = await session.execute(item_query)
        items = []
        for row in item_result.mappings():
            items.append(dict(row))
            
    return web.json_response({
        'success': True,
        'groups': groups,
        'items': items
    })

async def handle_get_grammar(request: web.Request) -> web.Response:
    """Получение грамматики из БД"""
    level = request.query.get('level', 'N5')
    
    async with async_session() as session:
        # Fetch grammar points
        from sqlalchemy.orm import selectinload
        query = GrammarPoint.__table__.select().where(GrammarPoint.level == level)
        
        # Note: raw SQL/core doesn't support selectinload easily, better to use ORM session.execute(select(...))
        # But for consistency with previous code, let's do 2 queries
        
        # 1. Get Points
        result = await session.execute(query)
        points = []
        point_ids = []
        for row in result.mappings():
            p = dict(row)
            p['examples'] = []
            points.append(p)
            point_ids.append(p['id'])
            
        if point_ids:
            # 2. Get Examples
            ex_query = GrammarExample.__table__.select().where(GrammarExample.grammar_id.in_(point_ids))
            ex_result = await session.execute(ex_query)
            
            examples_map = {}
            for row in ex_result.mappings():
                ex = dict(row)
                gid = ex['grammar_id']
                if gid not in examples_map: examples_map[gid] = []
                examples_map[gid].append(ex)
            
            # Merge
            for p in points:
                p['examples'] = examples_map.get(p['id'], [])

    return web.json_response({
        'success': True,
        'grammar': points
    })

def create_api_app() -> web.Application:
    app = web.Application()

    async def cors_middleware(app, handler):
        async def middleware_handler(request):
            if request.method == 'OPTIONS': response = web.Response()
            else: response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Telegram-Init-Data, ngrok-skip-browser-warning'
            return response
        return middleware_handler

    app.middlewares.append(cors_middleware)
    app.router.add_get('/api/health', handle_health_check)
    app.router.add_get('/api/user', handle_get_user)
    app.router.add_post('/api/progress', handle_save_progress)
    app.router.add_get('/api/leaderboard', handle_get_leaderboard)
    app.router.add_get('/api/content', handle_get_content) # <--- NEW
    app.router.add_post('/api/admin/content', handle_admin_add_content) # <--- ADMIN
    app.router.add_get('/api/grammar', handle_get_grammar) # <--- GRAMMAR
    app.router.add_post('/api/admin/grammar', handle_admin_add_grammar) # <--- NEW
    app.router.add_post('/api/daily', handle_claim_daily)
    app.router.add_get('/api/user/stats', handle_user_stats)
    app.router.add_get('/api/tts', handle_tts)
    app.router.add_post('/api/setname', handle_setname)
    app.router.add_get('/api/avatar/{user_id}', handle_get_avatar) # Подключили аватарки!
    app.router.add_get('/api/reviews', handle_get_reviews)
    app.router.add_post('/api/buy', handle_buy_item)
    app.router.add_post('/api/log', handle_log_error)

    # === SERVE FRONTEND STATIC FILES ===
    docs_path = os.path.join(os.path.dirname(__file__), 'docs')
    if os.path.exists(docs_path):
        async def handle_index(request):
            return web.FileResponse(os.path.join(docs_path, 'index.html'))
            
        app.router.add_get('/', handle_index)
        app.router.add_static('/', docs_path, name='static')

    return app
