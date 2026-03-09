// Базовая грамматика N5 (можно расширить через API)
export const GRAMMAR_N5 = [
    {
        id: "g_wa",
        level: "N5",
        title: "〜は (wa)",
        structure: "A wa B desu",
        description: "Частица は (wa) обозначает тему предложения. Она ставится после слова, которое является темой разговора.",
        examples: [
            {japanese: "私は学生です。", reading: "watashi wa gakusei desu", translation: "Я студент."},
            {japanese: "これはペンです。", reading: "kore wa pen desu", translation: "Это ручка."}
        ]
    },
    {
        id: "g_desu",
        level: "N5",
        title: "〜です (desu)",
        structure: "N + desu",
        description: "Связка です (desu) используется в конце предложения для вежливости и утверждения (быть, являться).",
        examples: [
            {japanese: "いい天気です。", reading: "ii tenki desu", translation: "Хорошая погода."},
            {japanese: "猫です。", reading: "neko desu", translation: "Это кошка."}
        ]
    },
    {
        id: "g_ka",
        level: "N5",
        title: "〜か (ka)",
        structure: "Sentence + ka",
        description: "Частица か (ka) в конце предложения превращает его в вопрос.",
        examples: [
            {japanese: "学生ですか。", reading: "gakusei desu ka", translation: "Вы студент?"},
            {japanese: "これは何ですか。", reading: "kore wa nan desu ka", translation: "Что это?"}
        ]
    },
    {
        id: "g_mo",
        level: "N5",
        title: "〜も (mo)",
        structure: "A mo B desu",
        description: "Частица も (mo) означает 'тоже', 'также'. Заменяет は (wa).",
        examples: [
            {japanese: "私も学生です。", reading: "watashi mo gakusei desu", translation: "Я тоже студент."},
            {japanese: "これもペンです。", reading: "kore mo pen desu", translation: "Это тоже ручка."}
        ]
    },
    {
        id: "g_no",
        level: "N5",
        title: "〜の (no)",
        structure: "A no B",
        description: "Частица の (no) обозначает принадлежность (родительный падеж). A принадлежит B (или A - свойство B).",
        examples: [
            {japanese: "私の本です。", reading: "watashi no hon desu", translation: "Это моя книга."},
            {japanese: "日本語の本。", reading: "nihongo no hon", translation: "Книга на японском (японского языка)."}
        ]
    }
];
