// ==================== HIRAGANA ====================
const HIRAGANA_ROWS = [
    { name: 'Гласные', id: 'vowels', chars: [
        {char: 'あ', reading: 'a', hint: 'Буква А с завитком'},
        {char: 'い', reading: 'i', hint: 'Две палочки'},
        {char: 'う', reading: 'u', hint: 'Похоже на У'},
        {char: 'え', reading: 'e', hint: 'Треугольник'},
        {char: 'お', reading: 'o', hint: 'Человечек'}
    ]},
    { name: 'Строка K', id: 'k', chars: [
        {char: 'か', reading: 'ka', hint: 'Лезвие катаны'},
        {char: 'き', reading: 'ki', hint: 'Ключ'},
        {char: 'く', reading: 'ku', hint: 'Клюв птицы'},
        {char: 'け', reading: 'ke', hint: 'Кегля'},
        {char: 'こ', reading: 'ko', hint: 'Два коромысла'}
    ]},
    { name: 'Строка S', id: 's', chars: [
        {char: 'さ', reading: 'sa', hint: 'Самурай'},
        {char: 'し', reading: 'shi', hint: 'Рыболовный крючок'},
        {char: 'す', reading: 'su', hint: 'Сушки на верёвке'},
        {char: 'せ', reading: 'se', hint: 'Сено'},
        {char: 'そ', reading: 'so', hint: 'Соломинка'}
    ]},
    { name: 'Строка T', id: 't', chars: [
        {char: 'た', reading: 'ta', hint: 'Танец'},
        {char: 'ち', reading: 'chi', hint: 'Цифра 5'},
        {char: 'つ', reading: 'tsu', hint: 'Улыбка цунами'},
        {char: 'て', reading: 'te', hint: 'Телевизор'},
        {char: 'と', reading: 'to', hint: 'Торнадо'}
    ]},
    { name: 'Строка N', id: 'n', chars: [
        {char: 'な', reading: 'na', hint: 'Узел на верёвке'},
        {char: 'に', reading: 'ni', hint: 'Нитка'},
        {char: 'ぬ', reading: 'nu', hint: 'Лапша нудл'},
        {char: 'ね', reading: 'ne', hint: 'Кошка нэко'},
        {char: 'の', reading: 'no', hint: 'Знак номера'}
    ]},
    { name: 'Строка H', id: 'h', chars: [
        {char: 'は', reading: 'ha', hint: 'Смеётся ХА'},
        {char: 'ひ', reading: 'hi', hint: 'Хихикает'},
        {char: 'ふ', reading: 'fu', hint: 'Гора Фудзи'},
        {char: 'へ', reading: 'he', hint: 'Волна'},
        {char: 'ほ', reading: 'ho', hint: 'Холодильник'}
    ]},
    { name: 'Строка M', id: 'm', chars: [
        {char: 'ま', reading: 'ma', hint: 'Мама'},
        {char: 'み', reading: 'mi', hint: 'Цифра 21'},
        {char: 'む', reading: 'mu', hint: 'Корова МУ'},
        {char: 'め', reading: 'me', hint: 'Глаз мэ'},
        {char: 'も', reading: 'mo', hint: 'Рыба в море'}
    ]},
    { name: 'Строка Y', id: 'y', chars: [
        {char: 'や', reading: 'ya', hint: 'Яхта'},
        {char: 'ゆ', reading: 'yu', hint: 'Юла'},
        {char: 'よ', reading: 'yo', hint: 'Йо-йо'}
    ]},
    { name: 'Строка R', id: 'r', chars: [
        {char: 'ら', reading: 'ra', hint: 'Рамен'},
        {char: 'り', reading: 'ri', hint: 'Лента ribbon'},
        {char: 'る', reading: 'ru', hint: 'Рулон'},
        {char: 'れ', reading: 're', hint: 'Река'},
        {char: 'ろ', reading: 'ro', hint: 'Рот открыт'}
    ]},
    { name: 'Строка W+N', id: 'w', chars: [
        {char: 'わ', reading: 'wa', hint: 'Ваза'},
        {char: 'を', reading: 'wo', hint: 'Ворота'},
        {char: 'ん', reading: 'n', hint: 'Звук Н'}
    ]}
];

// ==================== KATAKANA ====================
const KATAKANA_ROWS = [
    { name: 'Гласные', id: 'vowels', chars: [
        {char: 'ア', reading: 'a', hint: 'Похоже на А'},
        {char: 'イ', reading: 'i', hint: 'Две палочки'},
        {char: 'ウ', reading: 'u', hint: 'У с короной'},
        {char: 'エ', reading: 'e', hint: 'Этажерка'},
        {char: 'オ', reading: 'o', hint: 'О бежит'}
    ]},
    { name: 'Строка K', id: 'k', chars: [
        {char: 'カ', reading: 'ka', hint: 'Острый угол'},
        {char: 'キ', reading: 'ki', hint: 'Ключ'},
        {char: 'ク', reading: 'ku', hint: 'Куб'},
        {char: 'ケ', reading: 'ke', hint: 'Кетчуп'},
        {char: 'コ', reading: 'ko', hint: 'Коробка'}
    ]},
    { name: 'Строка S', id: 's', chars: [
        {char: 'サ', reading: 'sa', hint: 'Сабля'},
        {char: 'シ', reading: 'shi', hint: 'Улыбка'},
        {char: 'ス', reading: 'su', hint: 'Сундук'},
        {char: 'セ', reading: 'se', hint: 'Сэндвич'},
        {char: 'ソ', reading: 'so', hint: 'Сок'}
    ]},
    { name: 'Строка T', id: 't', chars: [
        {char: 'タ', reading: 'ta', hint: 'Таблица'},
        {char: 'チ', reading: 'chi', hint: 'Число'},
        {char: 'ツ', reading: 'tsu', hint: 'Цунами'},
        {char: 'テ', reading: 'te', hint: 'Телевизор'},
        {char: 'ト', reading: 'to', hint: 'Торт'}
    ]},
    { name: 'Строка N', id: 'n', chars: [
        {char: 'ナ', reading: 'na', hint: 'Нож'},
        {char: 'ニ', reading: 'ni', hint: 'Два'},
        {char: 'ヌ', reading: 'nu', hint: 'Нудл'},
        {char: 'ネ', reading: 'ne', hint: 'Нэт'},
        {char: 'ノ', reading: 'no', hint: 'Нос'}
    ]},
    { name: 'Строка H', id: 'h', chars: [
        {char: 'ハ', reading: 'ha', hint: 'Хата'},
        {char: 'ヒ', reading: 'hi', hint: 'Хихи'},
        {char: 'フ', reading: 'fu', hint: 'Фудзи'},
        {char: 'ヘ', reading: 'he', hint: 'Хэй'},
        {char: 'ホ', reading: 'ho', hint: 'Хор'}
    ]},
    { name: 'Строка M', id: 'm', chars: [
        {char: 'マ', reading: 'ma', hint: 'Мама'},
        {char: 'ミ', reading: 'mi', hint: 'Три'},
        {char: 'ム', reading: 'mu', hint: 'Му'},
        {char: 'メ', reading: 'me', hint: 'Мэч'},
        {char: 'モ', reading: 'mo', hint: 'Море'}
    ]},
    { name: 'Строка Y', id: 'y', chars: [
        {char: 'ヤ', reading: 'ya', hint: 'Яхта'},
        {char: 'ユ', reading: 'yu', hint: 'Юла'},
        {char: 'ヨ', reading: 'yo', hint: 'Йо-йо'}
    ]},
    { name: 'Строка R', id: 'r', chars: [
        {char: 'ラ', reading: 'ra', hint: 'Радио'},
        {char: 'リ', reading: 'ri', hint: 'Рис'},
        {char: 'ル', reading: 'ru', hint: 'Рука'},
        {char: 'レ', reading: 're', hint: 'Река'},
        {char: 'ロ', reading: 'ro', hint: 'Рот'}
    ]},
    { name: 'Строка W+N', id: 'w', chars: [
        {char: 'ワ', reading: 'wa', hint: 'Ваза'},
        {char: 'ヲ', reading: 'wo', hint: 'Вок'},
        {char: 'ン', reading: 'n', hint: 'Смайлик'}
    ]}
];

// ==================== KANJI N5 (103 символа) ====================
const KANJI_N5 = [
    // Числа
    {char: '一', reading: 'いち', meaning: 'один', hint: 'Одна черта = 1'},
    {char: '二', reading: 'に', meaning: 'два', hint: 'Две черты = 2'},
    {char: '三', reading: 'さん', meaning: 'три', hint: 'Три черты = 3'},
    {char: '四', reading: 'よん', meaning: 'четыре', hint: 'Окно с занавеской'},
    {char: '五', reading: 'ご', meaning: 'пять', hint: 'Скрещенные линии'},
    {char: '六', reading: 'ろく', meaning: 'шесть', hint: 'Человечек с шляпой'},
    {char: '七', reading: 'なな', meaning: 'семь', hint: 'Перевёрнутая 7'},
    {char: '八', reading: 'はち', meaning: 'восемь', hint: 'Крыша домика'},
    {char: '九', reading: 'きゅう', meaning: 'девять', hint: 'Крюк'},
    {char: '十', reading: 'じゅう', meaning: 'десять', hint: 'Крест = 10'},
    {char: '百', reading: 'ひゃく', meaning: 'сто', hint: 'Один + белый'},
    {char: '千', reading: 'せん', meaning: 'тысяча', hint: 'Человек с палкой'},
    {char: '万', reading: 'まん', meaning: '10 000', hint: 'Много-много'},
    
    // Время
    {char: '日', reading: 'にち/ひ', meaning: 'день/солнце', hint: 'Солнце в рамке'},
    {char: '月', reading: 'げつ/つき', meaning: 'месяц/луна', hint: 'Месяц с ножками'},
    {char: '火', reading: 'か/ひ', meaning: 'огонь', hint: 'Человек у костра'},
    {char: '水', reading: 'すい/みず', meaning: 'вода', hint: 'Капли воды'},
    {char: '木', reading: 'もく/き', meaning: 'дерево', hint: 'Дерево с ветками'},
    {char: '金', reading: 'きん/かね', meaning: 'золото/деньги', hint: 'Крыша над золотом'},
    {char: '土', reading: 'ど/つち', meaning: 'земля', hint: 'Росток из земли'},
    {char: '年', reading: 'ねん/とし', meaning: 'год', hint: 'Урожай за год'},
    {char: '時', reading: 'じ/とき', meaning: 'время/час', hint: 'Храм + солнце'},
    {char: '分', reading: 'ふん/ぶん', meaning: 'минута/часть', hint: 'Разделить на части'},
    {char: '半', reading: 'はん', meaning: 'половина', hint: 'Корова разрезана пополам'},
    {char: '今', reading: 'いま/こん', meaning: 'сейчас', hint: 'Крыша над моментом'},
    {char: '先', reading: 'さき/せん', meaning: 'раньше/впереди', hint: 'Ноги идут вперёд'},
    {char: '後', reading: 'あと/ご', meaning: 'после/позади', hint: 'Идти позади'},
    {char: '午', reading: 'ご', meaning: 'полдень', hint: 'Столб в центре дня'},
    {char: '前', reading: 'まえ/ぜん', meaning: 'перед/до', hint: 'Нож перед луной'},
    {char: '週', reading: 'しゅう', meaning: 'неделя', hint: 'Цикл движения'},
    {char: '毎', reading: 'まい', meaning: 'каждый', hint: 'Мать каждый день'},
    
    // Люди
    {char: '人', reading: 'ひと/じん', meaning: 'человек', hint: 'Идущий человек'},
    {char: '子', reading: 'こ/し', meaning: 'ребёнок', hint: 'Ребёнок в пелёнках'},
    {char: '女', reading: 'おんな/じょ', meaning: 'женщина', hint: 'Изящная поза'},
    {char: '男', reading: 'おとこ/だん', meaning: 'мужчина', hint: 'Сила на поле'},
    {char: '父', reading: 'ちち/ふ', meaning: 'отец', hint: 'Рука держит топор'},
    {char: '母', reading: 'はは/ぼ', meaning: 'мать', hint: 'Женщина кормит'},
    {char: '友', reading: 'とも/ゆう', meaning: 'друг', hint: 'Две руки вместе'},
    {char: '私', reading: 'わたし/し', meaning: 'я', hint: 'Колос пшеницы = моё'},
    
    // Природа
    {char: '山', reading: 'やま/さん', meaning: 'гора', hint: 'Три вершины'},
    {char: '川', reading: 'かわ/せん', meaning: 'река', hint: 'Три потока'},
    {char: '田', reading: 'た/でん', meaning: 'рисовое поле', hint: 'Поле разделено'},
    {char: '天', reading: 'てん/あま', meaning: 'небо', hint: 'Над человеком'},
    {char: '気', reading: 'き/け', meaning: 'дух/воздух', hint: 'Пар от риса'},
    {char: '雨', reading: 'あめ/う', meaning: 'дождь', hint: 'Капли под облаком'},
    {char: '電', reading: 'でん', meaning: 'электричество', hint: 'Молния под дождём'},
    {char: '花', reading: 'はな/か', meaning: 'цветок', hint: 'Трава меняется'},
    
    // Направления
    {char: '上', reading: 'うえ/じょう', meaning: 'верх', hint: 'Линия сверху'},
    {char: '下', reading: 'した/か', meaning: 'низ', hint: 'Линия снизу'},
    {char: '中', reading: 'なか/ちゅう', meaning: 'середина', hint: 'Палка в центре'},
    {char: '左', reading: 'ひだり/さ', meaning: 'лево', hint: 'Левая рука'},
    {char: '右', reading: 'みぎ/う', meaning: 'право', hint: 'Правая рука + рот'},
    {char: '外', reading: 'そと/がい', meaning: 'снаружи', hint: 'Выйти вечером'},
    {char: '北', reading: 'きた/ほく', meaning: 'север', hint: 'Два человека спиной'},
    {char: '南', reading: 'みなみ/なん', meaning: 'юг', hint: 'Тепло внутри'},
    {char: '西', reading: 'にし/せい', meaning: 'запад', hint: 'Птица в гнезде'},
    {char: '東', reading: 'ひがし/とう', meaning: 'восток', hint: 'Солнце за деревом'},
    
    // Размеры
    {char: '大', reading: 'おお/だい', meaning: 'большой', hint: 'Человек раскинул руки'},
    {char: '小', reading: 'ちい/しょう', meaning: 'маленький', hint: 'Маленькие точки'},
    {char: '高', reading: 'たか/こう', meaning: 'высокий', hint: 'Высокое здание'},
    {char: '安', reading: 'やす/あん', meaning: 'дешёвый/спокойный', hint: 'Женщина под крышей'},
    {char: '新', reading: 'あたら/しん', meaning: 'новый', hint: 'Срубить дерево'},
    {char: '古', reading: 'ふる/こ', meaning: 'старый', hint: 'Десять ртов'},
    {char: '長', reading: 'なが/ちょう', meaning: 'длинный', hint: 'Длинные волосы'},
    {char: '多', reading: 'おお/た', meaning: 'много', hint: 'Два вечера'},
    {char: '少', reading: 'すく/しょう', meaning: 'мало', hint: 'Маленький + мало'},
    
    // Места
    {char: '国', reading: 'くに/こく', meaning: 'страна', hint: 'Драгоценность в рамке'},
    {char: '店', reading: 'みせ/てん', meaning: 'магазин', hint: 'Место под крышей'},
    {char: '駅', reading: 'えき', meaning: 'станция', hint: 'Лошадь останавливается'},
    {char: '社', reading: 'しゃ', meaning: 'компания/храм', hint: 'Место для духов'},
    {char: '校', reading: 'こう', meaning: 'школа', hint: 'Дерево + здание'},
    {char: '会', reading: 'かい/あ', meaning: 'встреча', hint: 'Крыша над людьми'},
    
    // Действия
    {char: '行', reading: 'い/こう', meaning: 'идти', hint: 'Перекрёсток'},
    {char: '来', reading: 'く/らい', meaning: 'приходить', hint: 'Пшеница приходит'},
    {char: '出', reading: 'で/しゅつ', meaning: 'выходить', hint: 'Гора выходит'},
    {char: '入', reading: 'はい/にゅう', meaning: 'входить', hint: 'Входить внутрь'},
    {char: '食', reading: 'た/しょく', meaning: 'есть', hint: 'Рис + хорошо'},
    {char: '飲', reading: 'の/いん', meaning: 'пить', hint: 'Еда + недостаток'},
    {char: '見', reading: 'み/けん', meaning: 'видеть', hint: 'Глаз на ногах'},
    {char: '聞', reading: 'き/ぶん', meaning: 'слышать', hint: 'Ухо в воротах'},
    {char: '読', reading: 'よ/どく', meaning: 'читать', hint: 'Слова + продавать'},
    {char: '書', reading: 'か/しょ', meaning: 'писать', hint: 'Кисть пишет'},
    {char: '話', reading: 'はな/わ', meaning: 'говорить', hint: 'Слова + язык'},
    {char: '買', reading: 'か/ばい', meaning: 'покупать', hint: 'Сеть + глаз'},
    {char: '立', reading: 'た/りつ', meaning: 'стоять', hint: 'Человек на земле'},
    {char: '休', reading: 'やす/きゅう', meaning: 'отдыхать', hint: 'Человек у дерева'},
    {char: '学', reading: 'まな/がく', meaning: 'учиться', hint: 'Ребёнок под крышей'},
    {char: '生', reading: 'い/せい', meaning: 'жизнь/рождение', hint: 'Росток из земли'},
    
    // Другое
    {char: '何', reading: 'なに/なん', meaning: 'что', hint: 'Человек спрашивает'},
    {char: '本', reading: 'ほん/もと', meaning: 'книга/основа', hint: 'Корень дерева'},
    {char: '名', reading: 'な/めい', meaning: 'имя', hint: 'Рот вечером'},
    {char: '語', reading: 'ご/かた', meaning: 'язык/слово', hint: 'Слова + я'},
    {char: '車', reading: 'くるま/しゃ', meaning: 'машина', hint: 'Колёса'},
    {char: '道', reading: 'みち/どう', meaning: 'дорога', hint: 'Голова идёт'},
    {char: '円', reading: 'えん', meaning: 'йена/круг', hint: 'Круглая монета'},
    {char: '白', reading: 'しろ/はく', meaning: 'белый', hint: 'Солнце сверху'},
    {char: '百', reading: 'ひゃく', meaning: 'сто', hint: 'Один + белый'},
];

// ==================== KANJI N4 (181 символов - первые 50) ====================
const KANJI_N4 = [
    {char: '会', reading: 'かい/あ', meaning: 'встреча', hint: 'Люди под крышей'},
    {char: '同', reading: 'おな/どう', meaning: 'тот же', hint: 'Один рот'},
    {char: '事', reading: 'こと/じ', meaning: 'дело', hint: 'Рука с предметом'},
    {char: '自', reading: 'じ/し', meaning: 'сам', hint: 'Нос = я сам'},
    {char: '社', reading: 'しゃ', meaning: 'компания', hint: 'Место духов земли'},
    {char: '発', reading: 'はつ', meaning: 'отправление', hint: 'Ноги идут'},
    {char: '者', reading: 'しゃ/もの', meaning: 'человек (суффикс)', hint: 'Старый день'},
    {char: '地', reading: 'ち/じ', meaning: 'земля/место', hint: 'Земля + тоже'},
    {char: '業', reading: 'ぎょう/わざ', meaning: 'бизнес/работа', hint: 'Дерево труда'},
    {char: '方', reading: 'かた/ほう', meaning: 'способ/сторона', hint: 'Лодка поворачивает'},
    {char: '新', reading: 'あたら/しん', meaning: 'новый', hint: 'Топор рубит дерево'},
    {char: '場', reading: 'ば/じょう', meaning: 'место', hint: 'Земля + солнце'},
    {char: '員', reading: 'いん', meaning: 'член', hint: 'Рот + ракушка'},
    {char: '立', reading: 'た/りつ', meaning: 'стоять', hint: 'Человек на земле'},
    {char: '開', reading: 'あ/かい', meaning: 'открывать', hint: 'Ворота + руки'},
    {char: '手', reading: 'て/しゅ', meaning: 'рука', hint: 'Пять пальцев'},
    {char: '力', reading: 'ちから/りょく', meaning: 'сила', hint: 'Мускул руки'},
    {char: '問', reading: 'と/もん', meaning: 'вопрос', hint: 'Рот в воротах'},
    {char: '代', reading: 'よ/だい', meaning: 'поколение/замена', hint: 'Человек меняет'},
    {char: '明', reading: 'あか/めい', meaning: 'светлый/ясный', hint: 'Солнце + луна'},
    {char: '動', reading: 'うご/どう', meaning: 'двигаться', hint: 'Тяжёлая сила'},
    {char: '京', reading: 'きょう', meaning: 'столица', hint: 'Высокое здание'},
    {char: '目', reading: 'め/もく', meaning: 'глаз', hint: 'Глаз на боку'},
    {char: '通', reading: 'とお/つう', meaning: 'проходить', hint: 'Идти + использовать'},
    {char: '言', reading: 'い/げん', meaning: 'говорить', hint: 'Слова изо рта'},
    {char: '理', reading: 'り', meaning: 'причина/логика', hint: 'Король + деревня'},
    {char: '体', reading: 'からだ/たい', meaning: 'тело', hint: 'Человек + основа'},
    {char: '田', reading: 'た/でん', meaning: 'поле', hint: 'Рисовое поле'},
    {char: '主', reading: 'しゅ/ぬし', meaning: 'главный/хозяин', hint: 'Свеча горит'},
    {char: '題', reading: 'だい', meaning: 'тема/заголовок', hint: 'Правильно + страница'},
    {char: '意', reading: 'い', meaning: 'значение/намерение', hint: 'Звук + сердце'},
    {char: '不', reading: 'ふ/ぶ', meaning: 'не-/без-', hint: 'Отрицание'},
    {char: '作', reading: 'つく/さく', meaning: 'делать/создавать', hint: 'Человек + нож'},
    {char: '用', reading: 'よう/もち', meaning: 'использовать', hint: 'Забор'},
    {char: '度', reading: 'ど/たび', meaning: 'градус/раз', hint: 'Крыша + рука'},
    {char: '強', reading: 'つよ/きょう', meaning: 'сильный', hint: 'Лук + насекомое'},
    {char: '公', reading: 'こう/おおやけ', meaning: 'общественный', hint: 'Разделить частное'},
    {char: '持', reading: 'も/じ', meaning: 'держать', hint: 'Рука + храм'},
    {char: '野', reading: 'の/や', meaning: 'поле/дикий', hint: 'Деревня + давать'},
    {char: '以', reading: 'い', meaning: 'посредством', hint: 'Человек несёт'},
    {char: '思', reading: 'おも/し', meaning: 'думать', hint: 'Поле + сердце'},
    {char: '家', reading: 'いえ/か', meaning: 'дом/семья', hint: 'Свинья под крышей'},
    {char: '世', reading: 'よ/せ', meaning: 'мир/поколение', hint: 'Три десятка'},
    {char: '多', reading: 'おお/た', meaning: 'много', hint: 'Два вечера'},
    {char: '正', reading: 'ただ/せい', meaning: 'правильный', hint: 'Остановиться на линии'},
    {char: '安', reading: 'やす/あん', meaning: 'дешёвый/мирный', hint: 'Женщина дома'},
    {char: '院', reading: 'いん', meaning: 'институт', hint: 'Холм + завершить'},
    {char: '心', reading: 'こころ/しん', meaning: 'сердце', hint: 'Три капли'},
    {char: '界', reading: 'かい', meaning: 'мир/граница', hint: 'Поле + между'},
    {char: '教', reading: 'おし/きょう', meaning: 'учить', hint: 'Ребёнок + удар'},
];

// ==================== KANJI N3 (первые 100) ====================
const KANJI_N3 = [
    {char: '政', reading: 'せい/まつりごと', meaning: 'политика', hint: 'Правильно + удар'},
    {char: '議', reading: 'ぎ', meaning: 'обсуждение', hint: 'Слова + справедливость'},
    {char: '民', reading: 'みん/たみ', meaning: 'народ', hint: 'Глаз со стрелой'},
    {char: '連', reading: 'れん/つら', meaning: 'связь/ряд', hint: 'Идти + машина'},
    {char: '対', reading: 'たい/つい', meaning: 'против/пара', hint: 'Текст + дюйм'},
    {char: '部', reading: 'ぶ', meaning: 'часть/отдел', hint: 'Стоять + рот + город'},
    {char: '合', reading: 'あ/ごう', meaning: 'соединять', hint: 'Крышка + рот'},
    {char: '市', reading: 'し/いち', meaning: 'город/рынок', hint: 'Точка + ткань'},
    {char: '内', reading: 'ない/うち', meaning: 'внутри', hint: 'Человек в рамке'},
    {char: '相', reading: 'そう/あい', meaning: 'взаимный', hint: 'Дерево + глаз'},
    {char: '定', reading: 'てい/さだ', meaning: 'определять', hint: 'Крыша + правильно'},
    {char: '回', reading: 'かい/まわ', meaning: 'раз/вращать', hint: 'Рот в рамке'},
    {char: '選', reading: 'せん/えら', meaning: 'выбирать', hint: 'Два + уже + идти'},
    {char: '米', reading: 'べい/こめ', meaning: 'рис/Америка', hint: 'Зёрна риса'},
    {char: '実', reading: 'じつ/み', meaning: 'реальность/плод', hint: 'Крыша + голова'},
    {char: '関', reading: 'かん/せき', meaning: 'связь/барьер', hint: 'Ворота + небеса'},
    {char: '決', reading: 'けつ/き', meaning: 'решать', hint: 'Вода + раскрыть'},
    {char: '全', reading: 'ぜん/まった', meaning: 'весь/целый', hint: 'Человек + король'},
    {char: '表', reading: 'ひょう/おもて', meaning: 'поверхность/таблица', hint: 'Одежда + волосы'},
    {char: '戦', reading: 'せん/たたか', meaning: 'война', hint: 'Один + рот + копьё'},
    {char: '経', reading: 'けい/へ', meaning: 'проходить/сутра', hint: 'Нить + проход'},
    {char: '最', reading: 'さい/もっと', meaning: 'самый', hint: 'Солнце + брать'},
    {char: '現', reading: 'げん/あらわ', meaning: 'настоящий/появляться', hint: 'Яшма + видеть'},
    {char: '調', reading: 'ちょう/しら', meaning: 'исследовать/тон', hint: 'Слова + неделя'},
    {char: '化', reading: 'か/ば', meaning: 'превращаться', hint: 'Человек + ложка'},
    {char: '当', reading: 'とう/あ', meaning: 'этот/попадать', hint: 'Маленькая рука'},
    {char: '約', reading: 'やく', meaning: 'обещание/около', hint: 'Нить + ковш'},
    {char: '首', reading: 'しゅ/くび', meaning: 'шея/глава', hint: 'Голова'},
    {char: '法', reading: 'ほう', meaning: 'закон/способ', hint: 'Вода + уходить'},
    {char: '性', reading: 'せい/しょう', meaning: 'природа/пол', hint: 'Сердце + жизнь'},
    {char: '要', reading: 'よう/い', meaning: 'необходимый', hint: 'Запад + женщина'},
    {char: '制', reading: 'せい', meaning: 'система', hint: 'Корова + нож + ткань'},
    {char: '治', reading: 'じ/ち/おさ', meaning: 'управлять/лечить', hint: 'Вода + платформа'},
    {char: '務', reading: 'む/つと', meaning: 'обязанность', hint: 'Копьё + сила'},
    {char: '成', reading: 'せい/な', meaning: 'становиться', hint: 'Копьё + точка'},
    {char: '期', reading: 'き/ご', meaning: 'период', hint: 'Луна + срок'},
    {char: '取', reading: 'しゅ/と', meaning: 'брать', hint: 'Ухо + рука'},
    {char: '都', reading: 'と/みやこ', meaning: 'столица', hint: 'Человек + город'},
    {char: '和', reading: 'わ/やわ', meaning: 'гармония/Япония', hint: 'Зерно + рот'},
    {char: '機', reading: 'き/はた', meaning: 'машина/случай', hint: 'Дерево + механизм'},
    {char: '平', reading: 'へい/たい/ひら', meaning: 'плоский/мир', hint: 'Ровная линия'},
    {char: '加', reading: 'か/くわ', meaning: 'добавлять', hint: 'Сила + рот'},
    {char: '受', reading: 'じゅ/う', meaning: 'получать', hint: 'Рука + лодка + рука'},
    {char: '続', reading: 'ぞく/つづ', meaning: 'продолжать', hint: 'Нить + продавать'},
    {char: '進', reading: 'しん/すす', meaning: 'продвигаться', hint: 'Идти + птица'},
    {char: '数', reading: 'すう/かず', meaning: 'число', hint: 'Рис + женщина + удар'},
    {char: '記', reading: 'き/しる', meaning: 'записывать', hint: 'Слова + себя'},
    {char: '初', reading: 'しょ/はじ', meaning: 'начало', hint: 'Одежда + нож'},
    {char: '指', reading: 'し/ゆび', meaning: 'палец/указывать', hint: 'Рука + цель'},
    {char: '権', reading: 'けん/ごん', meaning: 'право/власть', hint: 'Дерево + двойной'},
];

// ==================== WORDS N5 ====================
const WORDS_N5 = [
    {word: 'こんにちは', reading: 'konnichiwa', meaning: 'здравствуйте'},
    {word: 'ありがとう', reading: 'arigatou', meaning: 'спасибо'},
    {word: 'すみません', reading: 'sumimasen', meaning: 'извините'},
    {word: 'おはよう', reading: 'ohayou', meaning: 'доброе утро'},
    {word: 'こんばんは', reading: 'konbanwa', meaning: 'добрый вечер'},
    {word: 'さようなら', reading: 'sayounara', meaning: 'до свидания'},
    {word: 'はい', reading: 'hai', meaning: 'да'},
    {word: 'いいえ', reading: 'iie', meaning: 'нет'},
    {word: 'わたし', reading: 'watashi', meaning: 'я'},
    {word: 'あなた', reading: 'anata', meaning: 'вы'},
    {word: 'かれ', reading: 'kare', meaning: 'он'},
    {word: 'かのじょ', reading: 'kanojo', meaning: 'она'},
    {word: 'これ', reading: 'kore', meaning: 'это (близко)'},
    {word: 'それ', reading: 'sore', meaning: 'это (средне)'},
    {word: 'あれ', reading: 'are', meaning: 'то (далеко)'},
    {word: 'なに', reading: 'nani', meaning: 'что'},
    {word: 'だれ', reading: 'dare', meaning: 'кто'},
    {word: 'どこ', reading: 'doko', meaning: 'где'},
    {word: 'いつ', reading: 'itsu', meaning: 'когда'},
    {word: 'なぜ', reading: 'naze', meaning: 'почему'},
    {word: 'たべる', reading: 'taberu', meaning: 'есть'},
    {word: 'のむ', reading: 'nomu', meaning: 'пить'},
    {word: 'みる', reading: 'miru', meaning: 'смотреть'},
    {word: 'きく', reading: 'kiku', meaning: 'слушать'},
    {word: 'いく', reading: 'iku', meaning: 'идти'},
    {word: 'くる', reading: 'kuru', meaning: 'приходить'},
    {word: 'かえる', reading: 'kaeru', meaning: 'возвращаться'},
    {word: 'ねる', reading: 'neru', meaning: 'спать'},
    {word: 'おきる', reading: 'okiru', meaning: 'просыпаться'},
    {word: 'よむ', reading: 'yomu', meaning: 'читать'},
    {word: 'かく', reading: 'kaku', meaning: 'писать'},
    {word: 'はなす', reading: 'hanasu', meaning: 'говорить'},
    {word: 'おおきい', reading: 'ookii', meaning: 'большой'},
    {word: 'ちいさい', reading: 'chiisai', meaning: 'маленький'},
    {word: 'あたらしい', reading: 'atarashii', meaning: 'новый'},
    {word: 'ふるい', reading: 'furui', meaning: 'старый'},
    {word: 'いい', reading: 'ii', meaning: 'хороший'},
    {word: 'わるい', reading: 'warui', meaning: 'плохой'},
    {word: 'たかい', reading: 'takai', meaning: 'высокий/дорогой'},
    {word: 'やすい', reading: 'yasui', meaning: 'дешёвый'},
];

// ==================== RANKS ====================
const RANKS = [
    {min: 0, name: 'Новичок', badge: '🥚', frame: 1},
    {min: 100, name: 'Ученик', badge: '🐣', frame: 2},
    {min: 500, name: 'Искатель', badge: '🔍', frame: 3},
    {min: 1000, name: 'Странник', badge: '🚶', frame: 4},
    {min: 1500, name: 'Кохай', badge: '🎒', frame: 5},
    {min: 2500, name: 'Сэмпай', badge: '🎓', frame: 6},
    {min: 4800, name: 'Мечник', badge: '⚔️', frame: 7},
    {min: 8000, name: 'Самурай', badge: '🥷', frame: 8},
    {min: 12000, name: 'Ронин', badge: '🏯', frame: 9},
    {min: 18000, name: 'Мастер', badge: '👨‍🏫', frame: 10},
    {min: 25000, name: 'Сенсей', badge: '🧙', frame: 11},
    {min: 35000, name: 'Шихан', badge: '📜', frame: 12},
    {min: 50000, name: 'Даймё', badge: '👑', frame: 13},
    {min: 70000, name: 'Сёгун', badge: '🏰', frame: 14},
    {min: 100000, name: 'Император', badge: '👘', frame: 15},
    {min: 150000, name: 'Легенда', badge: '🐉', frame: 16},
    {min: 250000, name: 'Ками', badge: '⛩️', frame: 17}
];