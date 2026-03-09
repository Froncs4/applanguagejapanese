export const STORIES = [
    {
        id: "story_cafe",
        title: "☕ Поход в кафе",
        level: "N5",
        difficulty: "Легко",
        duration: "5 мин",
        xp: 50,
        description: "Помоги Таро заказать кофе в токийском кафе",
        preview: "今日は、カフェに行きます...",
        image: "☕",
        isUnlocked: true,
        isCompleted: false,
        content: [
            {jp: "今日", kana: "きょう", ru: "Сегодня", interactive: true},
            {jp: "は", kana: "わ", ru: "(тема)", interactive: false},
            {jp: "カフェ", kana: "カフェ", ru: "кафе", interactive: true},
            {jp: "に", kana: "に", ru: "в (место)", interactive: false},
            {jp: "行きます", kana: "いきます", ru: "иду/еду", interactive: true},
            {jp: "。", kana: "", ru: "", interactive: false}
        ],
        quiz: { 
            question: "Куда идёт герой?", 
            options: ["В школу", "В кафе", "Домой", "В парк"], 
            correct: "В кафе",
            hint: "Посмотри на слово カフェ"
        },
        achievements: ["Первая история", "Читатель N5"],
        vocabulary: ["今日", "カフェ", "行きます"]
    },
    {
        id: "story_friend",
        title: "👥 Новый друг",
        level: "N5", 
        difficulty: "Легко",
        duration: "7 мин",
        xp: 60,
        description: "Познакомься с новым другом и узнай о его хобби",
        preview: "私の友達は猫が好きです...",
        image: "👥",
        isUnlocked: true,
        isCompleted: false,
        content: [
            {jp: "私", kana: "わたし", ru: "Я", interactive: true},
            {jp: "の", kana: "の", ru: "(принадлежность)", interactive: false},
            {jp: "友達", kana: "ともだち", ru: "друг", interactive: true},
            {jp: "は", kana: "わ", ru: "(тема)", interactive: false},
            {jp: "猫", kana: "ねこ", ru: "кошка/кот", interactive: true},
            {jp: "が", kana: "が", ru: "(объект)", interactive: false},
            {jp: "好き", kana: "すき", ru: "нравится", interactive: true},
            {jp: "です", kana: "です", ru: "есть/является", interactive: false},
            {jp: "。", kana: "", ru: "", interactive: false}
        ],
        quiz: { 
            question: "Что нравится другу героя?", 
            options: ["Собаки", "Кошки", "Рыбки", "Птицы"], 
            correct: "Кошки",
            hint: "Ищи слово 猫 (ねこ)"
        },
        achievements: ["Дружелюбный", "Любитель животных"],
        vocabulary: ["私", "友達", "猫", "好き", "です"]
    },
    {
        id: "story_shopping",
        title: "🛍️ Шоппинг в Токио",
        level: "N5",
        difficulty: "Средне",
        duration: "10 мин", 
        xp: 80,
        description: "Сходи за покупками в японский магазин",
        preview: "このリンゴはいくらですか...",
        image: "🛍️",
        isUnlocked: false,
        isCompleted: false,
        requirement: "Заверши 2 истории",
        content: [
            {jp: "この", kana: "この", ru: "этот/эта/это", interactive: true},
            {jp: "リンゴ", kana: "リンゴ", ru: "яблоко", interactive: true},
            {jp: "は", kana: "わ", ru: "(тема)", interactive: false},
            {jp: "いくら", kana: "いくら", ru: "сколько", interactive: true},
            {jp: "です", kana: "です", ru: "стоит", interactive: false},
            {jp: "か", kana: "か", ru: "? (вопрос)", interactive: false},
            {jp: "。", kana: "", ru: "", interactive: false}
        ],
        quiz: { 
            question: "Что хочет купить герой?", 
            options: ["Банан", "Яблоко", "Апельсин", "Грушу"], 
            correct: "Яблоко",
            hint: "リンゴ - это яблоко"
        },
        achievements: ["Покупатель", "Экономист"],
        vocabulary: ["この", "リンゴ", "いくら", "です"]
    },
    {
        id: "story_train",
        title: "☕ Поездка на поезде",
        level: "N5",
        difficulty: "Средне",
        duration: "20 мин",
        xp: 120,
        description: "Отправляйся в путешествие на знаменитом японском поезде синкансэн",
        preview: "新幹線で京都に行きます...",
        image: "🚅",
        isUnlocked: false,
        isCompleted: false,
        requirement: "XP 500+",
        stages: [
            {
                id: "stage_1",
                title: "На вокзале",
                content: [
                    {jp: "新幹線", kana: "しんかんせん", ru: "синкансэн (пуля)", interactive: true},
                    {jp: "で", kana: "で", ru: "на (транспорте)", interactive: false},
                    {jp: "京都", kana: "きょうと", ru: "Киото", interactive: true},
                    {jp: "に", kana: "に", ru: "в (место)", interactive: false},
                    {jp: "行きます", kana: "いきます", ru: "поеду", interactive: true},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "На чём едет герой?", 
                    options: ["Автобус", "Машина", "Синкансэн", "Велосипед"], 
                    correct: "Синкансэн",
                    hint: "新幹線 - это знаменитый японский поезд"
                }
            },
            {
                id: "stage_2",
                title: "В вагоне",
                content: [
                    {jp: "窓", kana: "まど", ru: "окно", interactive: true},
                    {jp: "から", kana: "から", ru: "из", interactive: false},
                    {jp: "富士山", kana: "ふじさん", ru: "Фудзияма", interactive: true},
                    {jp: "が", kana: "が", ru: "подлежащее", interactive: false},
                    {jp: "見えます", kana: "みえます", ru: "видно", interactive: true},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Что видно из окна?", 
                    options: ["Фудзияма", "Токио", "Море", "Горы"], 
                    correct: "Фудзияма",
                    hint: "富士山 (ふじさん) - это знаменитая гора Японии"
                }
            },
            {
                id: "stage_3", 
                title: "Прибытие",
                content: [
                    {jp: "京都", kana: "きょうと", ru: "Киото", interactive: true},
                    {jp: "に", kana: "に", ru: "в (место)", interactive: false},
                    {jp: "着きました", kana: "つきました", ru: "прибыл", interactive: true},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Куда прибыл герой?", 
                    options: ["Токио", "Киото", "Осака", "Нагоя"], 
                    correct: "Киото",
                    hint: "京都 (きょうと) - это древняя столица Японии"
                }
            }
        ],
        achievements: ["Путешественник", "Скоростник"],
        vocabulary: ["新幹線", "京都", "行きます", "窓", "富士山", "見えます", "着きました"]
    },
    {
        id: "story_festival",
        title: "🎌 Фестиваль Сакуры",
        level: "N4",
        difficulty: "Сложно",
        duration: "25 мин",
        xp: 180,
        description: "Участвуй в традиционном японском фестивале цветения сакуры",
        preview: "春の桜祭りに参加しましょう...",
        image: "🎌",
        isUnlocked: false,
        isCompleted: false,
        requirement: "XP 1000+",
        stages: [
            {
                id: "stage_1",
                title: "Подготовка к фестивалю",
                content: [
                    {jp: "春", kana: "はる", ru: "весна", interactive: true},
                    {jp: "の", kana: "の", ru: "(принадлежность)", interactive: false},
                    {jp: "桜", kana: "さくら", ru: "сакура", interactive: true},
                    {jp: "祭り", kana: "まつり", ru: "фестиваль", interactive: true},
                    {jp: "の", kana: "の", ru: "(принадлежность)", interactive: false},
                    {jp: "準備", kana: "じゅんび", ru: "подготовка", interactive: true},
                    {jp: "を", kana: "を", ru: "объект", interactive: false},
                    {jp: "します", kana: "します", ru: "делаю", interactive: false},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Что готовит герой?", 
                    options: ["Новогодний праздник", "Фестиваль сакуры", "День рождения", "Свадьбу"], 
                    correct: "Фестиваль сакуры",
                    hint: "桜 (さくら) - это сакура/вишнёвый цвет"
                }
            },
            {
                id: "stage_2",
                title: "На фестивале",
                content: [
                    {jp: "公園", kana: "こうえん", ru: "парк", interactive: true},
                    {jp: "で", kana: "で", ru: "в (месте)", interactive: false},
                    {jp: "たくさん", kana: "たくさん", ru: "много", interactive: true},
                    {jp: "の", kana: "の", ru: "частиц", interactive: false},
                    {jp: "人", kana: "ひと", ru: "людей", interactive: true},
                    {jp: "が", kana: "が", ru: "подлежащее", interactive: false},
                    {jp: "集まります", kana: "あつまります", ru: "собираются", interactive: true},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Где происходит действие?", 
                    options: ["В школе", "В ресторане", "В парке", "В магазине"], 
                    correct: "В парке",
                    hint: "公園 (こうえん) - это парк"
                }
            },
            {
                id: "stage_3",
                title: "Танцы под сакурой",
                content: [
                    {jp: "美しい", kana: "うつくしい", ru: "красивый", interactive: true},
                    {jp: "音楽", kana: "おんがく", ru: "музыка", interactive: true},
                    {jp: "を", kana: "を", ru: "Объект", interactive: false},
                    {jp: "聴きながら", kana: "ききながら", ru: "слушая", interactive: true},
                    {jp: "踊ります", kana: "おどります", ru: "танцую", interactive: true},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Что делает герой под сакурой?", 
                    options: ["Поёт", "Танцует", "Рисует", "Читает"], 
                    correct: "Танцует",
                    hint: "踊ります (おどります) - это танцевать"
                }
            },
            {
                id: "stage_4",
                title: "Завершение фестиваля",
                content: [
                    {jp: "楽しい", kana: "たのしい", ru: "весёлый", interactive: true},
                    {jp: "一日", kana: "いちにち", ru: "один день", interactive: true},
                    {jp: "でした", kana: "でした", ru: "был (прошлое время)", interactive: false},
                    {jp: "。", kana: "", ru: "", interactive: false}
                ],
                quiz: { 
                    question: "Как прошёл день фестиваля?", 
                    options: ["Скучно", "Грустно", "Весело", "Обычно"], 
                    correct: "Весело",
                    hint: "楽しい (たのしい) - это весёлый/радостный"
                }
            }
        ],
        achievements: ["Фестивальщик", "Любитель весны", "Мастер культуры", "Танцор"],
        vocabulary: ["春", "桜", "祭り", "準備", "公園", "集まります", "美しい", "音楽", "聴きながら", "踊ります", "楽しい", "一日"]
    }
];
