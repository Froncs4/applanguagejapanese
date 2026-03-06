"""
API для синхронизации Web App с ботом.
Использует Telegram WebApp initData для авторизации.
"""

import hashlib
import hmac
import json
import urllib.parse
from datetime import datetime
from aiohttp import web
from config import BOT_TOKEN
from database import (
    get_or_create_user, get_user_stats, add_xp, 
    update_streak, get_card_progress, upsert_card_progress,
    get_top_players, add_daily_progress
)


def verify_telegram_auth(init_data: str) -> dict | None:
    """
    Проверяет подпись initData от Telegram WebApp.
    Возвращает данные пользователя или None если невалидно.
    """
    try:
        parsed = dict(urllib.parse.parse_qsl(init_data))
        
        check_hash = parsed.pop('hash', None)
        if not check_hash:
            return None
        
        # Сортируем и формируем строку
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        
        # Создаём секретный ключ
        secret_key = hmac.new(
            b"WebAppData", 
            BOT_TOKEN.encode(), 
            hashlib.sha256
        ).digest()
        
        # Проверяем хэш
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if calculated_hash != check_hash:
            return None
        
        # Парсим user
        user_data = json.loads(parsed.get('user', '{}'))
        return user_data
        
    except Exception as e:
        print(f"Auth error: {e}")
        return None


async def handle_get_user(request: web.Request) -> web.Response:
    """GET /api/user - получить данные пользователя"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    
    if not user_data:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    user_id = user_data.get('id')
    username = user_data.get('first_name', 'User')
    
    # Получаем или создаём пользователя
    user = await get_or_create_user(user_id, username)
    stats = await get_user_stats(user_id)
    
    return web.json_response({
        'success': True,
        'user': {
            'id': user_id,
            'name': username,
            'xp': user.get('xp', 0),
            'streak': user.get('current_streak', 0),
            'best_streak': user.get('best_streak', 0),
            'cards_learned': stats.get('total_learned', 0),
            'daily_progress': user.get('daily_progress', 0),
            'daily_goal': user.get('daily_goal', 10),
        }
    })


async def handle_save_progress(request: web.Request) -> web.Response:
    """POST /api/progress - сохранить прогресс"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    
    if not user_data:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    user_id = user_data.get('id')
    
    try:
        body = await request.json()
    except:
        return web.json_response({'error': 'Invalid JSON'}, status=400)
    
    action = body.get('action')
    
    if action == 'quiz_complete':
        correct = body.get('correct', 0)
        total = body.get('total', 0)
        quiz_type = body.get('type', 'mixed')
        
        # Начисляем XP
        xp_gained = correct * 10
        if xp_gained > 0:
            new_xp = await add_xp(user_id, xp_gained)
            await add_daily_progress(user_id, correct)
        
        # Обновляем streak если всё правильно
        if correct == total and total > 0:
            await update_streak(user_id, True)
        
        return web.json_response({
            'success': True,
            'xp_gained': xp_gained,
            'new_xp': new_xp if xp_gained > 0 else 0
        })
    
    elif action == 'card_review':
        card_type = body.get('card_type')
        card_key = body.get('card_key')
        correct = body.get('correct', False)
        
        # Получаем текущий прогресс
        progress = await get_card_progress(user_id, card_type, card_key)
        
        if progress:
            reps = progress['repetitions']
            ease = progress['ease_factor']
            interval = progress['interval_days']
        else:
            reps, ease, interval = 0, 2.5, 0
        
        # SM-2 алгоритм
        from srs import calculate_next_review
        new_reps, new_ease, new_interval, next_review = calculate_next_review(
            reps, ease, interval, correct
        )
        
        await upsert_card_progress(
            user_id, card_type, card_key,
            new_ease, new_interval, new_reps, next_review
        )
        
        # XP за правильный ответ
        if correct:
            await add_xp(user_id, 10)
        
        return web.json_response({
            'success': True,
            'next_review': next_review
        })
    
    return web.json_response({'error': 'Unknown action'}, status=400)


async def handle_get_leaderboard(request: web.Request) -> web.Response:
    """GET /api/leaderboard - получить рейтинг"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    
    if not user_data:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    players = await get_top_players(20)
    
    return web.json_response({
        'success': True,
        'players': [
            {
                'id': p['user_id'],
                'name': p['username'] or 'User',
                'xp': p['xp'],
                'streak': p['current_streak']
            }
            for p in players
        ]
    })


async def handle_claim_daily(request: web.Request) -> web.Response:
    """POST /api/daily - получить ежедневный бонус"""
    init_data = request.headers.get('X-Telegram-Init-Data', '')
    user_data = verify_telegram_auth(init_data)
    
    if not user_data:
        return web.json_response({'error': 'Unauthorized'}, status=401)
    
    user_id = user_data.get('id')
    
    from database import claim_wheel_reward
    import random
    
    rewards = [10, 15, 20, 25, 30, 50, 75, 100]
    reward = random.choice(rewards)
    
    success = await claim_wheel_reward(user_id, reward)
    
    if success:
        return web.json_response({
            'success': True,
            'reward': reward
        })
    else:
        return web.json_response({
            'success': False,
            'error': 'Already claimed today'
        })


def create_api_app() -> web.Application:
    """Создаёт aiohttp приложение для API"""
    app = web.Application()
    
    # CORS middleware
    async def cors_middleware(app, handler):
        async def middleware_handler(request):
            if request.method == 'OPTIONS':
                response = web.Response()
            else:
                response = await handler(request)
            
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Telegram-Init-Data'
            return response
        return middleware_handler
    
    app.middlewares.append(cors_middleware)
    
    # Routes
    app.router.add_get('/api/user', handle_get_user)
    app.router.add_post('/api/progress', handle_save_progress)
    app.router.add_get('/api/leaderboard', handle_get_leaderboard)
    app.router.add_post('/api/daily', handle_claim_daily)
    
    return app