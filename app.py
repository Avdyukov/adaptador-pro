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
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #0a0a0f, #1a0a2e, #0f0f23, #0a0a0f);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
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
        line-height: 1.8;
        box-shadow: 0 0 30px rgba(155, 89, 182, 0.05);
        min-height: 100px;
    }
    
    .original-box {
        border-left-color: #2ecc71 !important;
    }
    
    .translated-box {
        border-left-color: #4facfe !important;
    }
    
    .parallel-line-ru {
        padding: 0.5rem;
        margin-bottom: 0.2rem;
        border-radius: 6px;
        background: rgba(22, 27, 34, 0.3);
        border-left: 3px solid #2ecc71;
        color: #c9d1d9;
    }
    
    .parallel-line-es {
        padding: 0.5rem;
        margin-bottom: 0.2rem;
        border-radius: 6px;
        background: rgba(22, 27, 34, 0.3);
        border-left: 3px solid #4facfe;
        color: #4facfe;
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
    
    .download-section {
        background: rgba(22, 27, 34, 0.5);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(155, 89, 182, 0.1);
        margin-top: 1rem;
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
    prompt = f"""Дай перевод слова '{word}' на русский и пример использования в предложении.

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

def split_sentences(texto):
    return [s.strip() for s in re.split(r'[.!?]\s*', texto) if s.strip()]

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.markdown('<p class="main-header">🚀 Adaptador Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ Перевод и адаптация текстов • Сохранение в 3 форматах • Словарь</p>', unsafe_allow_html=True)

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
        st.metric("📚 Слов", st.session_state.stats["words"])

# ============================================
# ОСНОВНАЯ ОБЛАСТЬ
# ============================================

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="card"><b>📝 Исходный текст</b></div>', unsafe_allow_html=True)
    
    texto = st.text_area(
        "",
        height=300,
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
                    
                    st.success("✅ Перевод готов!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка: {str(e)}")
    
    if st.session_state.result:
        # === 1. ТОЛЬКО ПЕРЕВОД ===
        st.markdown("#### 📄 Текст на языке перевода")
        st.markdown(f'<div class="result-box translated-box">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        # === 2. ТОЛЬКО ОРИГИНАЛ ===
        with st.expander("📄 Текст на языке оригинала", expanded=False):
            st.markdown(f'<div class="result-box original-box">{st.session_state.original}</div>', unsafe_allow_html=True)
        
        # === 3. ПОСТРОЧНО (разными цветами) ===
        with st.expander("📖 Построчный перевод", expanded=True):
            ru_sentences = split_sentences(st.session_state.original)
            es_sentences = split_sentences(st.session_state.result)
            
            for ru, es in zip(ru_sentences, es_sentences):
                st.markdown(f'<div class="parallel-line-es">🇪🇸 {es}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="parallel-line-ru">🇷🇺 {ru}</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # === 4. СОХРАНЕНИЕ В ФАЙЛ ===
        st.markdown("#### 💾 Сохранить")
        
        col_save1, col_save2, col_save3 = st.columns(3)
        
        # Файл 1: Только перевод
        with col_save1:
            st.download_button(
                "📄 Только перевод",
                st.session_state.result,
                file_name=f"traduccion_{target_lang}.txt",
                use_container_width=True
            )
        
        # Файл 2: Оригинал + перевод
        with col_save2:
            full_text = f"===== ОРИГИНАЛ =====\n{st.session_state.original}\n\n===== ПЕРЕВОД =====\n{st.session_state.result}"
            st.download_button(
                "📄 Оригинал + перевод",
                full_text,
                file_name=f"original_traduccion_{target_lang}.txt",
                use_container_width=True
            )
        
        # Файл 3: Построчно (цветной)
        with col_save3:
            parallel_text = "===== ПОСТРОЧНЫЙ ПЕРЕВОД =====\n\n"
            ru_sentences = split_sentences(st.session_state.original)
            es_sentences = split_sentences(st.session_state.result)
            for ru, es in zip(ru_sentences, es_sentences):
                parallel_text += f"🇪🇸 {es}\n"
                parallel_text += f"🇷🇺 {ru}\n\n"
            
            st.download_button(
                "📄 Построчный",
                parallel_text,
                file_name=f"paralelo_{target_lang}.txt",
                use_container_width=True
            )
        
        # === 5. СЛОВАРЬ (добавление слова) ===
        st.markdown("#### 📚 Добавить слово в словарь")
        
        col_word1, col_word2 = st.columns([2, 1])
        with col_word1:
            word_input = st.text_input("Введите слово", placeholder="Например: casa", key="word_input")
        with col_word2:
            btn_add_word = st.button("➕ Добавить", use_container_width=True)
        
        if btn_add_word and word_input:
            if not api_key:
                st.error("⚠️ Введите API ключ")
            else:
                try:
                    translation = get_word_translation(word_input, api_key, target_lang)
                    if word_input not in st.session_state.dictionary:
                        st.session_state.dictionary[word_input] = 0
                    st.session_state.dictionary[word_input] += 1
                    st.success(f"✅ Слово '{word_input}' добавлено в словарь!")
                    st.info(f"📝 {translation}")
                except Exception as e:
                    st.error(f"❌ Ошибка: {str(e)}")
        
        # === 6. ПОКАЗ СЛОВАРЯ ===
        if st.session_state.dictionary:
            with st.expander("📚 Твой словарь", expanded=False):
                sorted_words = sorted(st.session_state.dictionary.items(), key=lambda x: x[1], reverse=True)
                for word, count in sorted_words:
                    st.markdown(f"`{word}` — {count} раз(а)")
        
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
