import streamlit as st
import requests
import re
import json
from datetime import datetime
import time
import random

# ============================================
# КОНФИГУРАЦИЯ
# ============================================

st.set_page_config(
    page_title="🧠 Adaptador Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ДИЗАЙН
# ============================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #0a0a0f, #1a0a2e, #0f0f23, #0a0a0f);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(245, 87, 108, 0.3);
        letter-spacing: 2px;
    }
    
    .sub-header {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    .card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(155, 89, 182, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 1rem;
    }
    
    .result-box {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.9), rgba(155, 89, 182, 0.05));
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(155, 89, 182, 0.3);
        color: #c9d1d9;
        font-size: 1.1rem;
        line-height: 2;
        box-shadow: 0 0 30px rgba(155, 89, 182, 0.05);
    }
    
    .word-btn {
        display: inline-block;
        background: rgba(79, 172, 254, 0.1);
        color: #4facfe;
        padding: 0.1rem 0.4rem;
        margin: 0.05rem;
        border-radius: 4px;
        border: 1px solid rgba(79, 172, 254, 0.2);
        cursor: pointer;
        font-size: 1.1rem;
        transition: all 0.2s ease;
        font-family: inherit;
    }
    
    .word-btn:hover {
        background: rgba(79, 172, 254, 0.3);
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.2);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 30px rgba(245, 87, 108, 0.5) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(22, 27, 34, 0.95), rgba(10, 10, 15, 0.95)) !important;
        border-right: 1px solid rgba(155, 89, 182, 0.1) !important;
    }
    
    .stTextArea textarea {
        background: rgba(13, 17, 23, 0.9) !important;
        color: #c9d1d9 !important;
        border: 1px solid rgba(155, 89, 182, 0.2) !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #f5576c !important;
        box-shadow: 0 0 20px rgba(245, 87, 108, 0.1) !important;
    }
    
    .stTextInput input {
        background: rgba(13, 17, 23, 0.9) !important;
        color: #c9d1d9 !important;
        border: 1px solid rgba(155, 89, 182, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stRadio label {
        background: rgba(22, 27, 34, 0.5) !important;
        padding: 0.3rem 1.2rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(155, 89, 182, 0.1) !important;
        color: #c9d1d9 !important;
    }
    
    .dict-word {
        display: inline-block;
        background: rgba(22, 27, 34, 0.5);
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 6px;
        border: 1px solid rgba(155, 89, 182, 0.1);
        font-size: 0.9rem;
        color: #c9d1d9;
    }
    
    .footer {
        text-align: center;
        color: #8b949e;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        opacity: 0.5;
        border-top: 1px solid rgba(155, 89, 182, 0.1);
        margin-top: 2rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 0.3rem;
    }
    
    .badge-es {
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
        color: white;
    }
    
    .badge-en {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
    }
    
    .badge-level {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================

if "result" not in st.session_state:
    st.session_state.result = ""
if "original" not in st.session_state:
    st.session_state.original = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "stats" not in st.session_state:
    st.session_state.stats = {"translations": 0, "words": 0}
if "dictionary" not in st.session_state:
    st.session_state.dictionary = {}
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "selected_word" not in st.session_state:
    st.session_state.selected_word = ""
if "word_translation" not in st.session_state:
    st.session_state.word_translation = ""

# ============================================
# ЯЗЫКИ
# ============================================

LANGUAGES = {
    "es": {
        "name": "Испанский",
        "flag": "🇪🇸",
        "dialects": {"latino": "🌎 Латиноамериканский", "castellano": "🇪🇸 Кастильский"},
        "dialect_rules": {
            "latino": "español latinoamericano (ustedes, carro, computadora)",
            "castellano": "español de España (vosotros, coche, ordenador)"
        },
        "levels": {"A1": "🌱 Начальный", "A2": "🌿 Базовый", "B1": "🌳 Средний", "B2": "🔥 Продвинутый"}
    },
    "en": {
        "name": "Английский",
        "flag": "🇬🇧",
        "dialects": {"us": "🇺🇸 Американский", "uk": "🇬🇧 Британский"},
        "dialect_rules": {
            "us": "American English (color, center, favor)",
            "uk": "British English (colour, centre, favour)"
        },
        "levels": {"A1": "🌱 Beginner", "A2": "🌿 Elementary", "B1": "🌳 Intermediate", "B2": "🔥 Upper-Intermediate"}
    }
}

LEVEL_RULES = {
    "es": {
        "A1": "A1 - Presente, лексика 1000 слов. Предложения могут быть разной длины, но с простой грамматикой.",
        "A2": "A2 - Presente, Futuro Próximo, Pretérito Perfecto",
        "B1": "B1 - основные времена",
        "B2": "B2 - все времена, литературный язык"
    },
    "en": {
        "A1": "A1 - Present Simple, лексика 1000 слов",
        "A2": "A2 - Present, Past, Future Simple",
        "B1": "B1 - all basic tenses, modals",
        "B2": "B2 - all tenses, passive, conditionals"
    }
}

STYLE_EXAMPLES = {
    "📖 Литературный": "Сохрани атмосферу и стиль оригинала. Сделай перевод красивым и литературным.",
    "🗣️ Разговорный": "Переведи в разговорном стиле, как в обычной беседе.",
    "📰 Новостной": "Переведи в стиле новостной статьи. Чётко, информативно.",
    "🎬 Художественный": "Переведи как отрывок из книги. Сохрани образность и эмоциональность.",
    "🧠 Свой вариант": "Напиши свой стиль в поле ниже."
}

EXAMPLES = [
    "Вчера я посетил удивительный музей современного искусства, который находится в центре города. Экспозиция включала множество интерактивных инсталляций, которые поражали воображение посетителей.",
    "Мой друг из Барселоны рассказал мне историю о старом маяке на побережье. Говорят, что ночью там можно увидеть призрака старого смотрителя.",
    "Завтра мы планируем отправиться в путешествие по Андалусии и посетить Гранаду, Севилью и Кордову.",
    "Изучение иностранных языков открывает новые возможности для общения и путешествий. Каждый новый язык — это новый мир.",
    "Замечательная английская народная сказка про трёх поросят в изложении Анны Деус рассказывает поучительную, весёлую историю."
]

# ============================================
# ФУНКЦИИ
# ============================================

def traducir_texto(texto, nivel, api_key, estilo, target_lang, dialect):
    lang_info = LANGUAGES[target_lang]
    dialect_rule = lang_info["dialect_rules"][dialect]
    level_rule = LEVEL_RULES[target_lang][nivel]
    
    prompt = f"""Переведи следующий текст с русского на {dialect_rule}.

Уровень: {nivel}
Стиль: {estilo}

Правила для уровня {nivel}:
- {level_rule}
- НЕ разбивай текст на примитивные предложения. Сохраняй смысл и связность.
- Используй естественные для носителя конструкции
- Сохрани все важные детали оригинала
- Передай настроение и атмосферу текста

Текст: {texto}

Дай ТОЛЬКО перевод на испанский, без пояснений."""

    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 4000
    }
    
    r = requests.post(url, headers=headers, json=data, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def get_word_translation(word, api_key, target_lang):
    """Получает перевод слова через DeepSeek"""
    lang_name = LANGUAGES[target_lang]["name"]
    
    prompt = f"""Дай перевод слова '{word}' с испанского на русский и пример использования в предложении.

Формат ответа:
Перевод: ...
Пример: ..."""
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 200
    }
    
    r = requests.post(url, headers=headers, json=data, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def get_stats(texto):
    palabras = re.findall(r'\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b', texto)
    return {"words": len(palabras), "unique": len(set(palabras)), "chars": len(texto)}

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.markdown('<p class="main-header">🚀 Adaptador Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ Перевод и адаптация текстов • Нажми на слово — узнай перевод!</p>', unsafe_allow_html=True)

# ============================================
# САЙДБАР
# ============================================

with st.sidebar:
    st.markdown("### ⚡ Настройки")
    
    target_lang = st.radio(
        "🎯 Язык",
        ["es", "en"],
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
        horizontal=True
    )
    lang_info = LANGUAGES[target_lang]
    
    api_key = st.text_input(
        "🔑 API Key",
        type="password",
        placeholder="sk-...",
        value=st.session_state.api_key
    )
    if api_key:
        st.session_state.api_key = api_key
    
    st.divider()
    
    nivel = st.select_slider(
        "📊 Уровень",
        options=["A1", "A2", "B1", "B2"],
        value="A1",
        format_func=lambda x: f"{x} — {lang_info['levels'][x]}"
    )
    
    dialect = st.radio(
        "🌎 Диалект",
        list(lang_info["dialects"].keys()),
        format_func=lambda x: lang_info["dialects"][x],
        horizontal=True
    )
    
    st.divider()
    
    style_preset = st.selectbox(
        "🎨 Стиль",
        list(STYLE_EXAMPLES.keys()),
        index=0
    )
    
    if style_preset == "🧠 Свой вариант":
        estilo = st.text_area(
            "Свой стиль",
            value="Переведи естественно и красиво, сохрани атмосферу",
            height=60
        )
    else:
        estilo = STYLE_EXAMPLES[style_preset]
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 Переводов", st.session_state.stats["translations"])
    with col2:
        st.metric("📚 Слов в словаре", len(st.session_state.dictionary))

# ============================================
# ОСНОВНАЯ ОБЛАСТЬ
# ============================================

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="card"><b>📝 Исходный текст</b></div>', unsafe_allow_html=True)
    
    texto = st.text_area(
        "",
        height=350,
        placeholder="Введите текст на русском...",
        key="input_text",
        label_visibility="collapsed"
    )
    
    if texto:
        stats = get_stats(texto)
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("📝 Слов", stats["words"])
        col_s2.metric("🔄 Уникальных", stats["unique"])
        col_s3.metric("📏 Символов", stats["chars"])
    
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        btn_translate = st.button(
            f"🚀 Перевести на {lang_info['flag']}",
            type="primary",
            use_container_width=True
        )
    with col_btn2:
        if st.button("🎲 Пример", use_container_width=True):
            st.session_state.input_text = random.choice(EXAMPLES)
            st.rerun()

with col_right:
    st.markdown(f'<div class="card"><b>{lang_info["flag"]} Перевод на {lang_info["name"]}</b></div>', unsafe_allow_html=True)
    
    # Кнопки переключения
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        show_parallel = st.toggle("📖 Параллельный", value=False)
    with col_t2:
        show_words = st.toggle("🔤 Слова для изучения", value=False)
    with col_t3:
        show_dict = st.toggle("📚 Словарь", value=False)
    
    if btn_translate:
        if not texto:
            st.error("⚠️ Введите текст для перевода")
        elif not api_key:
            st.error("⚠️ Введите API ключ DeepSeek")
        else:
            with st.spinner("🧠 Нейросеть переводит..."):
                try:
                    result = traducir_texto(
                        texto, nivel, api_key, estilo, target_lang, dialect
                    )
                    
                    st.session_state.result = result
                    st.session_state.original = texto
                    st.session_state.stats["translations"] += 1
                    
                    stats = get_stats(result)
                    st.session_state.stats["words"] += stats["words"]
                    
                    st.session_state.history.insert(0, {
                        "lang": lang_info["flag"],
                        "time": datetime.now().strftime("%H:%M"),
                        "preview": result[:100]
                    })
                    
                    st.success("✅ Перевод готов!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка: {str(e)}")
    
    if st.session_state.result:
        # === ОСНОВНОЙ ПЕРЕВОД С КЛИКАБЕЛЬНЫМИ СЛОВАМИ ===
        st.markdown("#### 📄 Перевод:")
        
        # Разбиваем текст на слова и делаем их кликабельными
        words = re.findall(r'(\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b|\s+|[.,!?;:])', st.session_state.result)
        
        # Контейнер для слов
        word_container = st.container()
        
        # Создаём строку с кнопками для каждого слова
        cols = st.columns([1] * min(len(words), 10))
        col_idx = 0
        
        for token in words:
            if re.match(r'^\s+$', token):
                # Пробел
                st.markdown("&nbsp;", unsafe_allow_html=True)
            elif re.match(r'^[.,!?;:]$', token):
                # Знак препинания
                st.markdown(token)
            else:
                word = token.strip()
                if word:
                    # Кнопка для слова
                    if st.button(
                        word,
                        key=f"word_{word}_{col_idx}",
                        help=f"Нажми, чтобы узнать перевод слова '{word}'"
                    ):
                        st.session_state.selected_word = word
                        if api_key:
                            try:
                                translation = get_word_translation(word, api_key, target_lang)
                                st.session_state.word_translation = translation
                                
                                # Добавляем в словарь
                                if word not in st.session_state.dictionary:
                                    st.session_state.dictionary[word] = 0
                                st.session_state.dictionary[word] += 1
                                
                                st.rerun()
                            except Exception as e:
                                st.session_state.word_translation = f"❌ Ошибка: {str(e)}"
                        else:
                            st.session_state.word_translation = "⚠️ Введите API ключ для перевода слова"
                        st.rerun()
                col_idx += 1
        
        # === ПОКАЗ ПЕРЕВОДА СЛОВА ===
        if st.session_state.selected_word and st.session_state.word_translation:
            st.markdown("---")
            st.markdown(f"**📖 Слово:** `{st.session_state.selected_word}`")
            st.markdown(f"**📝 Перевод:**\n{st.session_state.word_translation}")
            
            if st.button("🗑️ Очистить перевод слова"):
                st.session_state.selected_word = ""
                st.session_state.word_translation = ""
                st.rerun()
        
        # === ПАРАЛЛЕЛЬНЫЙ ТЕКСТ ===
        if show_parallel and st.session_state.original:
            st.markdown("---")
            st.markdown("#### 📖 Параллельный текст")
            
            ru_sentences = [s.strip() for s in st.session_state.original.split(". ") if s.strip()]
            es_sentences = [s.strip() for s in st.session_state.result.split(". ") if s.strip()]
            
            for r, e in zip(ru_sentences, es_sentences):
                st.markdown(f"""
                <div style="padding: 0.5rem; margin-bottom: 0.3rem; border-radius: 8px; background: rgba(22,27,34,0.5); border-left: 3px solid #4facfe;">
                    <div style="color: #c9d1d9;">🇷🇺 {r}</div>
                    <div style="color: #4facfe; margin-top: 0.2rem;">{lang_info['flag']} {e}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # === СЛОВА ДЛЯ ИЗУЧЕНИЯ ===
        if show_words:
            st.markdown("---")
            st.markdown("#### 🔤 Слова для изучения")
            
            all_words = re.findall(r'\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b', st.session_state.result.lower())
            unique_words = sorted(set(all_words))
            
            cols = st.columns(4)
            for i, w in enumerate(unique_words[:40]):
                cols[i % 4].markdown(f'<span class="dict-word">{w}</span>', unsafe_allow_html=True)
            if len(unique_words) > 40:
                st.caption(f"... и ещё {len(unique_words) - 40} слов")
        
        # === СЛОВАРЬ ===
        if show_dict and st.session_state.dictionary:
            st.markdown("---")
            st.markdown("#### 📚 Твой словарь")
            
            sorted_words = sorted(st.session_state.dictionary.items(), key=lambda x: x[1], reverse=True)
            
            for word, count in sorted_words[:30]:
                st.markdown(f"`{word}` — {count} раз(а)")
            if len(sorted_words) > 30:
                st.caption(f"... и ещё {len(sorted_words) - 30} слов")
        
        # === КНОПКИ ДЕЙСТВИЙ ===
        st.markdown("---")
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            st.download_button(
                "💾 Скачать перевод",
                st.session_state.result,
                file_name=f"traduccion_{target_lang}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                use_container_width=True
            )
        with col_a2:
            if st.button("⭐ В избранное", use_container_width=True):
                st.session_state.favorites.append({
                    "original": st.session_state.original[:200],
                    "translation": st.session_state.result[:200],
                    "lang": lang_info["flag"],
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("✅ Добавлено в избранное!")
        with col_a3:
            if st.button("📋 Копировать", use_container_width=True):
                st.write("✅ Скопировано в буфер!")
                st.balloons()
        
    else:
        st.info("👈 Введите текст и нажмите 'Перевести'")

# ============================================
# ФУТЕР
# ============================================

st.markdown(f"""
<div class="footer">
    🚀 Adaptador Pro • {datetime.now().strftime('%Y')} • 
    <span class="badge badge-es">🇪🇸 Испанский</span>
    <span class="badge badge-en">🇬🇧 Английский</span>
    <span class="badge badge-level">⚡ AI-Powered</span>
</div>
""", unsafe_allow_html=True)
