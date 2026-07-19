import streamlit as st
import requests
import re
import json
from datetime import datetime
import time
import random

# ============================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ============================================

st.set_page_config(
    page_title="🧠 Adaptador Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# СУПЕР-ПИЗДАТЫЙ ДИЗАЙН
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
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .card:hover {
        border-color: rgba(155, 89, 182, 0.6);
        box-shadow: 0 8px 40px rgba(155, 89, 182, 0.15);
        transform: translateY(-2px);
    }
    
    .card-title {
        color: #c9d1d9;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
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
        transition: all 0.3s ease;
    }
    
    .result-box:hover {
        box-shadow: 0 0 50px rgba(155, 89, 182, 0.1);
        border-color: rgba(155, 89, 182, 0.6);
    }
    
    .parallel-line {
        padding: 0.7rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        background: rgba(22, 27, 34, 0.5);
        border-left: 3px solid #4facfe;
        transition: all 0.3s ease;
    }
    
    .parallel-line:hover {
        background: rgba(22, 27, 34, 0.8);
        transform: translateX(5px);
        border-left-color: #f5576c;
    }
    
    .original-text {
        color: #c9d1d9;
        font-size: 0.95rem;
        opacity: 0.9;
    }
    
    .translated-text {
        color: #4facfe;
        margin-top: 0.2rem;
        font-size: 0.95rem;
        font-weight: 500;
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
    
    .stButton button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
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
        transition: all 0.3s ease !important;
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
    
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border-color: rgba(155, 89, 182, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stRadio div {
        gap: 0.5rem;
    }
    
    .stRadio label {
        background: rgba(22, 27, 34, 0.5) !important;
        padding: 0.3rem 1.2rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(155, 89, 182, 0.1) !important;
        color: #c9d1d9 !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio label:hover {
        border-color: #f5576c !important;
    }
    
    .stRadio label[data-baseweb="radio"] {
        background: transparent !important;
        border: none !important;
    }
    
    .metric-card {
        background: rgba(22, 27, 34, 0.5);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(155, 89, 182, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #4facfe;
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f093fb, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #8b949e;
        font-size: 0.8rem;
        margin-top: 0.3rem;
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
    
    .dict-word {
        display: inline-block;
        background: rgba(22, 27, 34, 0.5);
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 6px;
        border: 1px solid rgba(155, 89, 182, 0.1);
        font-size: 0.9rem;
        color: #c9d1d9;
        transition: all 0.2s ease;
    }
    
    .dict-word:hover {
        border-color: #f5576c;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ИНИЦИАЛИЗАЦИЯ СЕССИИ
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
        "color": "#9b59b6",
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
        "color": "#3498db",
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
        "A1": "A1 - Presente, лексика 1000 слов. Предложения могут быть разной длины, но с простой грамматикой. Используй союзы 'y', 'pero', 'porque'.",
        "A2": "A2 - Presente, Futuro Próximo, Pretérito Perfecto",
        "B1": "B1 - основные времена",
        "B2": "B2 - все времена, литературный язык"
    },
    "en": {
        "A1": "A1 - Present Simple, лексика 1000 слов. Предложения могут быть разной длины, но с простой грамматикой. Используй союзы 'and', 'but', 'because'.",
        "A2": "A2 - Present, Past, Future Simple",
        "B1": "B1 - all basic tenses, modals",
        "B2": "B2 - all tenses, passive, conditionals"
    }
}

STYLE_EXAMPLES = {
    "📖 Литературный": "Сохрани атмосферу и стиль оригинала. Сделай перевод красивым и литературным.",
    "🗣️ Разговорный": "Переведи в разговорном стиле, как в обычной беседе. Используй естественные для носителя выражения.",
    "📰 Новостной": "Переведи в стиле новостной статьи. Чётко, информативно, нейтрально.",
    "🎬 Художественный": "Переведи как отрывок из книги. Сохрани образность и эмоциональность.",
    "🧠 Свой вариант": "Напиши свой стиль в поле ниже."
}

# ============================================
# ФУНКЦИИ
# ============================================

def traducir_texto(texto, nivel, api_key, estilo, target_lang, dialect, callback=None):
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
    
    if callback:
        callback("⏳ Отправка запроса...")
    
    r = requests.post(url, headers=headers, json=data, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def get_stats(texto):
    palabras = re.findall(r'\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b', texto)
    return {"words": len(palabras), "unique": len(set(palabras)), "chars": len(texto)}

def update_dictionary(texto):
    palabras = re.findall(r'\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b', texto.lower())
    for p in palabras:
        if len(p) > 2:
            if p not in st.session_state.dictionary:
                st.session_state.dictionary[p] = 0
            st.session_state.dictionary[p] += 1

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.markdown('<p class="main-header">🚀 Adaptador Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ Перевод и адаптация текстов с AI-магией</p>', unsafe_allow_html=True)

# ============================================
# САЙДБАР
# ============================================

with st.sidebar:
    st.markdown("### ⚡ Быстрые настройки")
    
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
        help="Получи на platform.deepseek.com",
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
    
    # Выбор стиля
    style_preset = st.selectbox(
        "🎨 Стиль перевода",
        list(STYLE_EXAMPLES.keys()),
        index=0
    )
    
    if style_preset == "🧠 Свой вариант":
        estilo = st.text_area(
            "Напиши свой стиль",
            value="Переведи естественно и красиво, сохрани атмосферу",
            height=60
        )
    else:
        estilo = STYLE_EXAMPLES[style_preset]
        st.caption(f"📝 {estilo[:100]}...")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 Переводов", st.session_state.stats["translations"])
    with col2:
        st.metric("📚 Слов", st.session_state.stats["words"])
    
    if st.session_state.history:
        st.divider()
        st.markdown("### 📜 Последние")
        for entry in st.session_state.history[:3]:
            st.caption(f"{entry['lang']} • {entry['time']}")
            st.caption(f"_{entry['preview'][:50]}..._")
            st.divider()
    
    if st.session_state.dictionary:
        st.divider()
        st.markdown("### 📚 Словарь")
        most_common = sorted(st.session_state.dictionary.items(), key=lambda x: x[1], reverse=True)[:10]
        for word, count in most_common:
            st.markdown(f"`{word}` — {count} раз(а)")

# ============================================
# ОСНОВНАЯ ОБЛАСТЬ
# ============================================

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("""
    <div class="card">
        <div class="card-title">📝 Исходный текст</div>
    </div>
    """, unsafe_allow_html=True)
    
    texto = st.text_area(
        "",
        height=350,
        placeholder="Введите текст на русском...\n\nНапример: Вчера я посетил удивительный музей современного искусства, который находится в центре города.",
        key="input_text",
        label_visibility="collapsed"
    )
    
    if texto:
        stats = get_stats(texto)
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("📝 Слов", stats["words"])
        col_s2.metric("🔄 Уникальных", stats["unique"])
        col_s3.metric("📏 Символов", stats["chars"])
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    with col_btn1:
        btn_translate = st.button(
            f"🚀 Перевести на {lang_info['flag']}",
            type="primary",
            use_container_width=True
        )
    with col_btn2:
        btn_clear = st.button("🗑️ Очистить", use_container_width=True)
    with col_btn3:
        btn_random = st.button("🎲 Пример", use_container_width=True)
    
    if btn_clear:
        st.session_state.result = ""
        st.session_state.original = ""
        st.rerun()
    
    if btn_random:
        ejemplos = [
            "Вчера я посетил удивительный музей современного искусства, который находится в центре города. Экспозиция включала множество интерактивных инсталляций, которые поражали воображение посетителей.",
            "Мой друг из Барселоны рассказал мне историю о старом маяке на побережье. Говорят, что ночью там можно увидеть призрака старого смотрителя.",
            "Завтра мы планируем отправиться в путешествие по Андалусии и посетить Гранаду, Севилью и Кордову. Это будет незабываемая поездка.",
            "Изучение иностранных языков открывает новые возможности для общения и путешествий. Каждый новый язык — это новый мир.",
            "Замечательная английская народная сказка про трёх поросят в изложении Анны Деус рассказывает поучительную, весёлую историю, одну из самых популярных среди детей всего мира."
        ]
        st.session_state.input_text = random.choice(ejemplos)
        st.rerun()

with col_right:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{lang_info['flag']} Перевод на {lang_info['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        show_parallel = st.toggle("📖 Параллельный", value=False)
    with col_t2:
        show_stats = st.toggle("📊 Статистика", value=False)
    with col_t3:
        show_dict = st.toggle("📚 Словарь", value=False)
    with col_t4:
        show_fav = st.toggle("⭐ Избранное", value=False)
    
    if btn_translate:
        if not texto:
            st.error("⚠️ Введите текст для перевода")
        elif not api_key:
            st.error("⚠️ Введите API ключ DeepSeek")
        else:
            with st.status("🧠 Нейросеть работает...", expanded=True) as status:
                status.write("⏳ Подготовка запроса...")
                try:
                    result = traducir_texto(
                        texto, nivel, api_key, estilo, target_lang, dialect,
                        callback=lambda msg: status.write(msg)
                    )
                    
                    st.session_state.result = result
                    st.session_state.original = texto
                    st.session_state.stats["translations"] += 1
                    
                    stats = get_stats(result)
                    st.session_state.stats["words"] += stats["words"]
                    
                    # Обновляем словарь
                    update_dictionary(result)
                    
                    # Сохраняем в историю
                    st.session_state.history.insert(0, {
                        "lang": lang_info["flag"],
                        "time": datetime.now().strftime("%H:%M"),
                        "preview": result[:100]
                    })
                    
                    status.update(label="✅ Перевод готов!", state="complete")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка: {str(e)}")
    
    if st.session_state.result:
        st.markdown(f'<div class="result-box">{st.session_state.result}</div>', unsafe_allow_html=True)
        
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            st.download_button(
                "💾 Скачать",
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
                st.write("✅ Скопировано!")
                st.balloons()
        
        if show_parallel:
            st.markdown("### 📖 Параллельный текст")
            ru_sentences = [s.strip() for s in st.session_state.original.split(". ") if s.strip()]
            es_sentences = [s.strip() for s in st.session_state.result.split(". ") if s.strip()]
            
            for r, e in zip(ru_sentences, es_sentences):
                st.markdown(f"""
                <div class="parallel-line">
                    <div class="original-text">🇷🇺 {r}</div>
                    <div class="translated-text">{lang_info['flag']} {e}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if show_stats:
            st.markdown("### 📊 Статистика перевода")
            stats = get_stats(st.session_state.result)
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            col_s1.metric("📝 Всего слов", stats["words"])
            col_s2.metric("🔄 Уникальных", stats["unique"])
            col_s3.metric("📏 Символов", stats["chars"])
            col_s4.metric("📖 Предложений", len(st.session_state.result.split(". ")))
        
        if show_dict:
            st.markdown("### 📚 Словарь из текста")
            palabras = sorted(set(re.findall(r'\b[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]+\b', st.session_state.result.lower())))
            
            cols = st.columns(4)
            for i, p in enumerate(palabras[:40]):
                cols[i % 4].markdown(f'<span class="dict-word">{p}</span>', unsafe_allow_html=True)
            if len(palabras) > 40:
                st.caption(f"... и ещё {len(palabras) - 40} слов")
        
        if show_fav and st.session_state.favorites:
            st.markdown("### ⭐ Избранное")
            for fav in st.session_state.favorites[-5:]:
                with st.expander(f"{fav['lang']} • {fav['time']}"):
                    st.caption(f"🇷🇺 {fav['original']}...")
                    st.caption(f"{fav['lang']} {fav['translation']}...")
        
    else:
        st.info("👈 Введите текст и нажмите 'Перевести'")

# ============================================
# ФУТЕР
# ============================================

st.markdown(f"""
<div class="footer">
    🚀 Adaptador Pro • {datetime.now().strftime('%Y')} • Сделано с ❤️ • 
    <span class="badge badge-es">🇪🇸 Испанский</span>
    <span class="badge badge-en">🇬🇧 Английский</span>
    <span class="badge badge-level">⚡ AI-Powered</span>
</div>
""", unsafe_allow_html=True)
