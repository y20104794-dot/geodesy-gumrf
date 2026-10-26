import streamlit as st
import math
import random
from datetime import date
import pandas as pd
import requests
import urllib.parse

st.set_page_config(
    page_title="Геодезия ГУМРФ • Пастельный Навигатор + ИИ",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= МЯГКИЙ ПАСТЕЛЬНЫЙ ДИЗАЙН (APPLE / NOTION PASTEL) =================
st.markdown("""
<style>
    /* Основной тёплый пастельный фон */
    .stApp {
        background-color: #F6F4F0;
        color: #37352F;
    }
    section[data-testid="stSidebar"] {
        background-color: #EFECE6 !important;
        border-right: 1px solid #E3DFD7;
    }
    /* Мягкие пастельные карточки */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FBF9F6 !important;
        border: 1px solid #E4E0D8 !important;
        border-radius: 18px !important;
        padding: 18px !important;
        box-shadow: 0 4px 14px rgba(55, 53, 47, 0.03) !important;
    }
    /* Пастельные кнопки */
    .stButton > button {
        background-color: #D8E6DF !important;
        color: #2C4A3E !important;
        border: 1px solid #C2D6CC !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #C7DCD1 !important;
        border-color: #B1CBBF !important;
    }
    /* Вкладки */
    button[data-baseweb="tab"] {
        background-color: #EFECE6 !important;
        border-radius: 12px !important;
        margin-right: 6px !important;
        padding: 8px 16px !important;
        color: #5A574F !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #DCE7E1 !important;
        color: #284438 !important;
    }
    /* Пастельные плашки */
    .pastel-card-sage {
        background: #E8F0EC; border: 1px solid #D0E0D8; border-radius: 16px; padding: 16px; margin-bottom: 12px; color: #2B443A;
    }
    .pastel-card-lavender {
        background: #EDEBF5; border: 1px solid #DAD6EA; border-radius: 16px; padding: 16px; margin-bottom: 12px; color: #3B3654;
    }
    .pastel-card-peach {
        background: #F9EFEA; border: 1px solid #EBD9D0; border-radius: 16px; padding: 16px; margin-bottom: 12px; color: #573B2E;
    }
    .pastel-card-sky {
        background: #E8F1F8; border: 1px solid #D0E1F0; border-radius: 16px; padding: 16px; margin-bottom: 12px; color: #284257;
    }
    .formula-box {
        background: #EFECE6; border-left: 4px solid #7FA392; padding: 12px 16px; border-radius: 10px;
        font-family: monospace; font-size: 0.95rem; color: #2F3E37; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================= ВСТРОЕННАЯ НЕЙРОСЕТЬ (РАБОТАЕТ СРАЗУ БЕЗ API-КЛЮЧЕЙ!) =================
LOCAL_KNOWLEDGE = {
    "нивелир": "По методичке ГУМРФ и учебнику Федотова: **Геометрическое нивелирование** — наиболее точный вид нивелирования. Прибор для механического нивелирования — **Профилограф**. На станции IV класса порядок отсчётов: 1) Задняя чёрная, 2) Передняя чёрная, 3) Передняя красная, 4) Задняя красная. Допуск расхождения превышений по чёрной и красной сторонам реек: **IV класс ≤ 5 мм** (плечо ≤ 100 м, между рейками до 200 м), **III класс ≤ 3 мм** (плечо ≤ 75 м, неравенство плеч ≤ 2 м, по чёрной стороне 3 нити). Постраничный контроль: ∑З − ∑П = ∑h_выч; (∑З − ∑П)/2 = ∑h_ср.",
    "теодолит": "Оптический теодолит **4Т30П**: 4-я модификация, Т — теодолит, 30 — СКО измерения угла одним приёмом 30'', П — прямое изображение. Штатив — **деревянный усиленный**, радиус дуги цилиндрического уровня — **от 2,5 м**. Сходимость полуприёмов КЛ и КП: **≤ 1,0'**. Место нуля для 4Т30П: **МО = (КЛ + КП)/2**, угол наклона **ν = КЛ − МО = МО − КП**. Зенитное расстояние: **Z = 90° − ν**. В теодолите 3Т5КП горизонтальное проложение d напрямую не измеряется, а вычисляется: **d = D · cos²ν**.",
    "невязк": "**Угловая невязка** замкнутого теодолитного хода: **f_β = ∑β_пр − 180°·(n − 2)**. Допуск: **f_βдоп = ±1,5'·√n** (распределяется поровну во все углы с обратным знаком). **Линейная невязка**: f_x = ∑Δx, f_y = ∑Δy, **f_абс = √(f_x² + f_y²)**, относительная **f_отн = f_абс / P ≤ 1/2000** (поправки распределяются пропорционально длинам сторон d_i с обратным знаком).",
    "дирекцион": "**Дирекционный угол α** отсчитывается от северного направления осевого меридиана (оси X) по часовой стрелке от 0° до 360°. Связь с магнитным азимутом: **α = A_м + δ − γ** (нужны три величины, поэтому в тесте СДО ответ — «Нет правильного ответа»). Передача на следующую сторону при правых углах: **α_(n+1) = α_n + 180° − β_испр**, при левых: **α_(n+1) = α_n + β_испр − 180°**.",
    "профиль": "В **Лабораторной работе №2**: горизонтальный масштаб плана и профиля — **1:5000**, а вертикальный масштаб профиля — **1:100** (укрупнён в 50 раз для наглядного отображения рельефа). Обязательно наносится вершина холма **36,6 м** (и 38,2 м). Высота сечения рельефа h = 1 м. Масштаб заложений (гипербола) строится по формуле: **d = (h · 100) / i**.",
    "карт": "В **Лабораторной работе №1 (Карта М 1:50 000)** используются три системы: 1) Географические координаты (φ, λ — по минутной рамке), 2) Прямоугольные координаты **Гаусса — Крюгера** (X, Y — по километровой сетке, где ось Y сдвинута на 500 км на запад), 3) **Балтийская система высот (БСВ)** от нуля Кронштадтского футштока.",
    "тахеометр": "**Тахеометрическая съёмка** (Приложение 12): горизонтальное проложение **d = D · cos²ν**, табличное превышение **h' = d · tg(ν)**, полное превышение **h = d · tg(ν) + i − V**, отметка пикета **H_пк = H_ст + h**. Полевой чертёж называется **кроки**.",
    "gps": "По учебнику Федотова (Гл. 14, 21, 25): для определения 3D-координат (X, Y, H) и поправки часов приёмника нужно **минимум 4 спутника GPS/ГЛОНАСС**. Точность до 1 см достигается в **дифференциальном режиме (DGPS)** с базовой станцией на опорном пункте. Три типа сеточных ЦММ: **регулярная, адаптивная и гладкая**. Вешение линий точнее способом **«на себя»**."
}

def ask_builtin_ai(user_query: str, custom_gemini_key: str = "") -> str:
    sys_prompt = (
        "Ты — встроенный ИИ-наставник и экзаменатор по инженерной геодезии ГУМРФ им. адм. С.О. Макарова "
        "(кафедра Водных путей и водных изысканий, методичка А.В. Москаля и С.В. Конопацкого 2026 г., учебник Г.А. Федотова). "
        "Отвечай чётко, дружелюбно, с формулами и допусками ГУМРФ на русском языке."
    )
    # 1. Если пользователь ввёл свой Gemini ключ — используем его
    if custom_gemini_key.strip():
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={custom_gemini_key.strip()}"
            r = requests.post(url, json={"contents": [{"parts": [{"text": sys_prompt + "\n\nВопрос студента: " + user_query}]}]}, timeout=15)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass

    # 2. Встроенная облачная нейросеть БЕЗ КЛЮЧА (Pollinations OpenAI-compatible API)
    try:
        r = requests.post(
            "https://text.pollinations.ai/openai",
            json={
                "model": "openai",
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_query}
                ]
            },
            timeout=18
        )
        if r.status_code == 200:
            data = r.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if content:
                return content
    except Exception:
        pass

    # 3. Резервный GET-канал без ключа
    try:
        q_enc = urllib.parse.quote(f"{sys_prompt}\nВопрос: {user_query}")
        r2 = requests.get(f"https://text.pollinations.ai/{q_enc}", timeout=12)
        if r2.status_code == 200 and len(r2.text) > 10:
            return r2.text
    except Exception:
        pass

    # 4. Офлайн-эксперт по базе ГУМРФ (если вообще нет интернета)
    low = user_query.lower()
    for k, v in LOCAL_KNOWLEDGE.items():
        if k in low:
            return f"🌿 **Ответ встроенной базы ГУМРФ (Офлайн-режим):**\n\n{v}"
    return (
        "🌿 **Ответ встроенного эксперта ГУМРФ:**\n\n"
        + "\n\n".join(LOCAL_KNOWLEDGE.values())
    )

# ================= ДАННЫЕ 8 НЕДЕЛЬ И СПРАВОЧНИКА =================
STUDY_PLAN = [
    {
        "week": 1, "dates": "27.10.2026 – 02.11.2026", "start": date(2026, 10, 27), "end": date(2026, 11, 2),
        "color": "pastel-card-sage",
        "title": "Блок 1: Теория погрешностей, Карта М 1:50 000 и Профиль А–В",
        "tasks": [
            "Классификация погрешностей (грубые, систематические, случайные). Предельная погрешность Δ_пред = 3m",
            "Сравнение точности линий через относительную погрешность (1/1000 и 1/2000)",
            "Лабораторная №1: Карта М 1:50 000 (географические координаты, Гаусс — Крюгер, Балтийская система высот)",
            "Лабораторная №2: План в горизонталях (М 1:5000), профиль А–В (МВ 1:100, вершина 36,6) и масштаб заложений d = (h·100)/i"
        ],
        "summary": "Предельная погрешность Δ_пред = 3m. На карте М 1:50 000: географические координаты (по рамке), Гаусса — Крюгера (по километровой сетке, сдвиг Y на +500 км), Балтийская система высот. На профиле А–В горизонтальный масштаб 1:5000, вертикальный 1:100, масштаб заложений d = 100·h/i.",
        "yt": "https://www.youtube.com/results?search_query=определение+координат+Гаусса+Крюгера+и+построение+профиля+рельефа",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%86%D0%B8%D1%8F_%D0%93%D0%B0%D1%83%D1%81%D1%81%D0%B0_%E2%80%94_%D0%9A%D1%80%D1%8E%D0%B3%D0%B5%D1%80%D0%B0"
    },
    {
        "week": 2, "dates": "03.11.2026 – 09.11.2026", "start": date(2026, 11, 3), "end": date(2026, 11, 9),
        "color": "pastel-card-lavender",
        "title": "Блок 2: Теодолиты (4Т30П, 3Т5КП), поверки, углы и Место Нуля (МО)",
        "tasks": [
            "Классы точности теодолитов (Т1, Т2/Т5/Т10, Т15/Т30/Т60), расшифровка 4Т30П, деревянный усиленный штатив, радиус уровня от 2,5 м",
            "Геометрические условия осей теодолита (U–U ⊥ J–J, H–H ⊥ J–J, V–V ⊥ H–H), центрирование и горизонтирование",
            "Измерение горизонтальных углов способом приёмов (сходимость КЛ и КП ≤ 1,0') и круговых приёмов",
            "Расчёт Места Нуля МО = (КЛ+КП)/2, угла наклона ν = КЛ − МО и зенитного расстояния Z = 90° − ν"
        ],
        "summary": "4Т30П — технический теодолит (СКО 30'', прямое изображение). Расхождение полуприёмов ≤ 1'. МО = (КЛ+КП)/2, ν = КЛ − МО. Основное положение вертикального круга — малый положительный отсчёт угла наклона повышения.",
        "yt": "https://www.youtube.com/watch?v=2szRxKqej3M",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D0%B4%D0%BE%D0%BB%D0%B8%D1%82"
    },
    {
        "week": 3, "dates": "10.11.2026 – 16.11.2026", "start": date(2026, 11, 10), "end": date(2026, 11, 16),
        "color": "pastel-card-peach",
        "title": "Блок 3: Теодолитные ходы, ориентирование и Ведомость координат",
        "tasks": [
            "Дирекционные углы α, румбы r, переход от магнитного азимута α = A_м + δ − γ",
            "Передача дирекционного угла: для правых углов α_(n+1) = α_n + 180° − β_испр, для левых α_(n+1) = α_n + β_испр − 180°",
            "Угловая невязка f_β = ∑β_пр − 180°(n − 2), допуск f_βдоп = ±1,5'√n, распределение поровну с обратным знаком",
            "Приращения Δx = d·cos(α), Δy = d·sin(α), линейная невязка f_отн ≤ 1/2000, Ведомость координат"
        ],
        "summary": "Угловая невязка распределяется поровну с обратным знаком, а невязки в приращениях координат f_x и f_y — пропорционально длинам сторон d_i: δx_i = −(f_x/P)·d_i.",
        "yt": "https://www.youtube.com/results?search_query=ведомость+вычисления+координат+теодолитного+хода",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D0%B4%D0%BE%D0%BB%D0%B8%D1%82%D0%BD%D1%8B%D0%B9_%D1%85%D0%BE%D0%B4"
    },
    {
        "week": 4, "dates": "17.11.2026 – 23.11.2026", "start": date(2026, 11, 17), "end": date(2026, 11, 23),
        "color": "pastel-card-sky",
        "title": "Блок 4: Геометрическое нивелирование, нивелиры Н-3 и рейки РН-3000",
        "tasks": [
            "Виды нивелирования: геометрическое (наиболее точное), тригонометрическое, механическое (профилограф), барометрическое",
            "Способы «из середины» (h = a − b) и «вперёд» (h = i − b), контактный уровень и компенсатор (Н-3К)",
            "Двусторонняя шашечная рейка РН-3000 (пятки красной стороны 4687 / 4787 / 4800 мм)",
            "Главная поверка нивелира: параллельность визирной оси и оси цилиндрического уровня (V–V || U–U)"
        ],
        "summary": "Способ «из середины» исключает погрешность за непараллельность визирной оси и оси уровня, а также кривизну Земли и рефракцию.",
        "yt": "https://www.youtube.com/results?search_query=устройство+и+поверки+нивелира+Н-3+рейка+РН-3000",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9D%D0%B8%D0%B2%D0%B5%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5"
    },
    {
        "week": 5, "dates": "24.11.2026 – 30.11.2026", "start": date(2026, 11, 24), "end": date(2026, 11, 30),
        "color": "pastel-card-sage",
        "title": "Блок 5: Нивелирование III и IV классов и постраничный контроль",
        "tasks": [
            "Нивелирование IV класса: ЗЧ → ПЧ → ПК → ЗК, плечо ≤ 100 м (между рейками до 200 м), |h_ч − h_кр| ≤ 5 мм",
            "Постраничный контроль журнала: ∑З − ∑П = ∑h_выч и (∑З − ∑П)/2 = ∑h_ср",
            "Нивелирование III класса: 3 нити по чёрной стороне, плечо ≤ 75 м, неравенство плеч ≤ 2 м, |h_ч − h_кр| ≤ 3 мм"
        ],
        "summary": "Главное отличие в СДО: допуск расхождения чёрного и красного превышений на станции в IV классе ≤ 5 мм, а в III классе ≤ 3 мм!",
        "yt": "https://www.youtube.com/results?search_query=заполнение+журнала+нивелирования+4+и+3+класса+постраничный+контроль",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9D%D0%B8%D0%B2%D0%B5%D0%BB%D0%B8%D1%80%D0%BD%D0%B0%D1%8F_%D1%81%D0%B5%D1%82%D1%8C"
    },
    {
        "week": 6, "dates": "01.12.2026 – 07.12.2026", "start": date(2026, 12, 1), "end": date(2026, 12, 7),
        "color": "pastel-card-lavender",
        "title": "Блок 6: Тахеометрия, линейка Дробышева, ГИС, САПР и GPS/DGPS",
        "tasks": [
            "Тахеометрическая съёмка: d = D·cos²ν, превышение h = d·tg(ν) + i − V, отметка H_пк = H_ст + h, кроки",
            "Построение сетки квадратов 10×10 см линейкой Ф.В. Дробышева (ЛТ-1, диагональ 70,711 см)",
            "Учебник Федотова: ГИС, САПР, 3 типа сеточных ЦММ (регулярная, адаптивная, гладкая), вешение «на себя», GPS (мин. 4 спутника) и DGPS (до 1 см)"
        ],
        "summary": "Линейка Дробышева строит сетку с точностью 0,2 мм. Для GPS нужно минимум 4 спутника, а режим DGPS с базовой станцией даёт точность до 1 см.",
        "yt": "https://www.youtube.com/watch?v=rFNE93023Jc",
        "wiki": "https://ru.wikipedia.org/wiki/DGPS"
    },
    {
        "week": 7, "dates": "08.12.2026 – 14.12.2026", "start": date(2026, 12, 8), "end": date(2026, 12, 14),
        "color": "pastel-card-peach",
        "title": "Блок 7: Прогон базы СДО ГУМРФ (200 вопросов) и сдача работ",
        "tasks": [
            "Ежедневный прогон билетов по 30 вопросов в вкладке «Тренажёр СДО» (результат ≥ 85%)",
            "Проверка всех полевых журналов карандашом (исправления зачёркиванием одной чертой с причиной ошибки справа)",
            "Сдача проверенных работ 2-го семестра преподавателям кафедры"
        ],
        "summary": "Полевые журналы — только простым карандашом без ластика! Титульники, дневник, тех. отчёт и ведомости — синей ручкой или печатью.",
        "yt": "https://www.youtube.com/results?search_query=инженерная+геодезия+подготовка+к+экзамену",
        "wiki": "https://sdo.gumrf.ru/"
    },
    {
        "week": 8, "dates": "15.12.2026", "start": date(2026, 12, 15), "end": date(2026, 12, 20),
        "color": "pastel-card-sky",
        "title": "Блок 8: Генеральная репетиция комиссии ГУМРФ",
        "tasks": [
            "Контрольный билет на 30–45 вопросов без подсказок",
            "Устная репетиция комиссии со встроенной нейросетью в боковой панели или вкладке ИИ",
            "Уверенная сдача комиссии на отлично!"
        ],
        "summary": "На комиссии отвечаем по схеме: точное определение → формула → численный допуск из методички Конопацкого и Москаля.",
        "yt": "https://www.youtube.com/results?search_query=геодезия+защита+практики",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%B4%D0%B5%D0%B7%D0%B8%D1%8F"
    }
]

# ================= БОКОВАЯ ПАНЕЛЬ: ВСЕГДА ДОСТУПНАЯ ВСТРОЕННАЯ НЕЙРОСЕТЬ =================
with st.sidebar:
    st.markdown("### 🤖 Встроенный ИИ-Наставник")
    st.caption("Работает сразу **без ключей** через встроенный облачный канал + знает всю методичку ГУМРФ и учебник Федотова!")
    
    quick_q = st.selectbox(
        "Быстрый вопрос нейросети:",
        [
            "Выбери готовый вопрос или напиши свой ниже...",
            "Задай мне каверзный вопрос от Конопацкого по нивелированию III и IV класса",
            "Объясни все ловушки теста СДО ГУМРФ",
            "Как защитить Лабораторную №2 (профиль А-В и масштаб заложений)?",
            "Как правильно исправлять ошибки в полевом журнале по методичке?"
        ]
    )
    sidebar_prompt = st.text_area("Спроси что угодно по геодезии:", value="" if quick_q.startswith("Выбери") else quick_q, height=90)
    custom_key = st.text_input("Опционально: твой ключ Gemini (не обязательно)", type="password")
    
    if st.button("✨ Спросить нейросеть", use_container_width=True):
        if sidebar_prompt.strip():
            with st.spinner("Нейросеть готовит ответ по методичке ГУМРФ..."):
                ans = ask_builtin_ai(sidebar_prompt.strip(), custom_key)
                st.session_state["last_ai_reply"] = ans

    if "last_ai_reply" in st.session_state:
        st.markdown(f"<div class='pastel-card-lavender'>{st.session_state['last_ai_reply']}</div>", unsafe_allow_html=True)

# ================= ГЛАВНЫЙ ЭКРАН ПРИЛОЖЕНИЯ =================
st.title("🌿 Геодезия ГУМРФ — Пастельный Навигатор + Встроенный ИИ")
st.caption("Мягкий минималистичный дизайн • Полная база знаний • Автоматические ведомости • Встроенная нейросеть без ключей")

today = date.today()
active_w = 1
for b in STUDY_PLAN:
    if b["start"] <= today <= b["end"]:
        active_w = b["week"]
        break

tabs = st.tabs([
    "📅 1. План (8 нед.) + Ресурсы",
    "🤖 2. Чат с встроенным ИИ",
    "📚 3. Справочник + Википедия",
    "🧪 4. Тренажёр СДО (Билеты)",
    "📐 5. Авто-расчёт всех журналов",
    "📂 6. Чек-лист моих работ"
])

# --- ВКЛАДКА 1: 8-НЕДЕЛЬНЫЙ ПЛАН ---
with tabs[0]:
    st.markdown(f"<div class='pastel-card-sage'><b>Сегодня: {today.strftime('%d.%m.%Y')}</b> • По твоему календарному графику сейчас идёт <b>Неделя {active_w}</b></div>", unsafe_allow_html=True)
    for b in STUDY_PLAN:
        is_cur = (b["week"] == active_w)
        with st.expander(f"{'🌿 АКТИВНАЯ НЕДЕЛЯ: ' if is_cur else ''}Неделя {b['week']} ({b['dates']}) — {b['title']}", expanded=is_cur):
            st.markdown(f"<div class='{b['color']}'><b>Краткая суть недели:</b> {b['summary']}</div>", unsafe_allow_html=True)
            for idx, t in enumerate(b["tasks"]):
                st.checkbox(t, key=f"wk_{b['week']}_{idx}")
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("▶️ Смотреть видеоразбор на YouTube", b["yt"], use_container_width=True)
            with c2:
                st.link_button("🌐 Открыть статью в Википедии", b["wiki"], use_container_width=True)

# --- ВКЛАДКА 2: ПОЛНОЭКРАННЫЙ ЧАТ С ВСТРОЕННОЙ НЕЙРОСЕТЬЮ ---
with tabs[1]:
    st.subheader("🤖 Диалог со встроенной нейросетью (Экзаменатор ГУМРФ)")
    st.markdown("<div class='pastel-card-sky'>Ты можешь сразу писать сюда любые вопросы, просить проверить твои расчёты или устроить симуляцию устной комиссии — <b>нейросеть уже подключена и работает без всяких API-ключей!</b></div>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "Привет! Я твоя встроенная нейросеть по инженерной геодезии ГУМРФ. Спрашивай любую формулу, задачу из СДО или давай проверим твои невыполненные работы второго семестра!"}
        ]

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_chat = st.chat_input("Напиши вопрос нейросети (например: Посчитай мне МО, если КЛ = +2°15', а КП = -2°13')...")
    if user_chat:
        st.session_state["chat_history"].append({"role": "user", "content": user_chat})
        with st.chat_message("user"):
            st.markdown(user_chat)
        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                reply = ask_builtin_ai(user_chat, custom_key)
                st.markdown(reply)
                st.session_state["chat_history"].append({"role": "assistant", "content": reply})

# --- ВКЛАДКА 3: СПРАВОЧНИК + ЖИВОЙ ПОИСК В ВИКИПЕДИИ ---
with tabs[2]:
    st.subheader("📚 Полная энциклопедия по курсу + Поиск в Википедии")
    wiki_q = st.text_input("🔍 Живой поиск любого геодезического термина в русской Википедии:", placeholder="Например: Теодолит, Нивелирование, Проекция Гаусса — Крюгера...")
    if wiki_q:
        try:
            w_url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(wiki_q)}&utf8=&format=json"
            res = requests.get(w_url, timeout=8).json()
            for item in res.get("query", {}).get("search", [])[:4]:
                title = item["title"]
                link = f"https://ru.wikipedia.org/wiki/{urllib.parse.quote(title)}"
                st.markdown(f"<div class='pastel-card-sky'><b><a href='{link}' target='_blank'>{title} ↗</a></b><br>{item['snippet']}...</div>", unsafe_allow_html=True)
        except Exception:
            st.warning("Проверьте подключение к интернету.")

    for k, v in LOCAL_KNOWLEDGE.items():
        st.markdown(f"<div class='pastel-card-sage'>{v}</div>", unsafe_allow_html=True)

# --- ВКЛАДКА 4: ТРЕНАЖЕР СДО ---
with tabs[3]:
    st.subheader("🧪 Симулятор теста СДО ГУМРФ")
    if st.button("🔄 Сгенерировать новый пастельный билет"):
        st.session_state["q_seed"] = random.randint(1, 99999)
    rng = random.Random(st.session_state.get("q_seed", 101))
    zc, pc = rng.randint(1200, 1900), rng.randint(1100, 1800)
    zk, pk = zc + 4800, pc + 4800 - rng.choice([-2, 0, 2])
    hm = ((zc - pc) + (zk - pk)) / 2.0

    with st.container(border=True):
        st.markdown(f"**Расчётная задача (Нивелирование IV класса):** Задняя рейка: Ч = `{zc}`, К = `{zk}`. Передняя рейка: Ч = `{pc}`, К = `{pk}`. Вычислите среднее превышение $h_{{ср}}$ (мм):")
        u_ans = st.number_input("Ваш ответ (мм):", step=0.5)
        if st.button("Проверить ответ"):
            if abs(u_ans - hm) < 0.01:
                st.success(f"Идеально! h_ч = {zc-pc} мм, h_к = {zk-pk} мм, среднее h_ср = {hm:+.1f} мм.")
            else:
                st.error(f"Правильный ответ: {hm:+.1f} мм.")

# --- ВКЛАДКА 5: КАЛЬКУЛЯТОРЫ ЖУРНАЛОВ И ПРОФИЛЯ ---
with tabs[4]:
    st.subheader("📐 Калькуляторы полевых журналов и Лабораторной №2")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### 1. Станция нивелирования IV и III класса")
            zc_in = st.number_input("Задняя чёрная (мм):", value=1450)
            zk_in = st.number_input("Задняя красная (мм):", value=6239)
            pc_in = st.number_input("Передняя чёрная (мм):", value=1445)
            pk_in = st.number_input("Передняя красная (мм):", value=6233)
            hc, hk = zc_in - pc_in, zk_in - pk_in
            hm_in = (hc + hk) / 2.0
            diff_in = abs(hc - hk)
            st.markdown(f"<div class='pastel-card-sage'>h_ч = <b>{hc} мм</b> | h_к = <b>{hk} мм</b> | <b>h_ср = {hm_in:+.1f} мм</b><br>Расхождение: <b>{diff_in} мм</b> ({'✅ Допуск III и IV кл.' if diff_in<=3 else '⚠️ Только IV кл. (≤5 мм)' if diff_in<=5 else '❌ Брак'})</div>", unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("#### 2. Тахеометрический пикет (Приложение 12)")
            hst_in = st.number_input("Отметка станции H_ст (м):", value=39.31)
            i_in = st.number_input("Высота прибора i (м):", value=1.48)
            v_in = st.number_input("Высота визирования V (м):", value=1.88)
            d_in = st.number_input("Дальномерное расстояние D (м):", value=19.3)
            nu_in = st.number_input("Угол наклона ν (в минутах со знаком, напр. -3°45' = -225):", value=-225.0)
            rad = math.radians(nu_in / 60.0)
            d_hor = d_in * (math.cos(rad) ** 2)
            h_pr = d_hor * math.tan(rad)
            h_full = h_pr + i_in - v_in
            h_pk = hst_in + h_full
            st.markdown(f"<div class='pastel-card-lavender'>Горизонтальное проложение <b>d = {d_hor:.2f} м</b><br>Табличное превышение d·tg(ν) = <b>{h_pr:+.2f} м</b><br>Полное превышение <b>h = {h_full:+.2f} м</b><br><b>Отметка пикета H_пк = {h_pk:.2f} м</b></div>", unsafe_allow_html=True)

# --- ВКЛАДКА 6: ЧЕК-ЛИСТ РАБОТ ---
with tabs[5]:
    st.subheader("📂 Чек-лист сдачи всех работ второго семестра")
    debts = [
        "Лабораторная №1: Карта М 1:50 000 (координаты, Гаусс — Крюгер, поперечный масштаб)",
        "Лабораторная №2: План в горизонталях (М 1:5000), профиль А–В (М 1:100, вершина 36,6) и масштаб заложений",
        "Журнал измерения горизонтальных углов (карандаш, полуприёмы ≤ 1')",
        "Журнал измерения длин линий и Места Нуля (МО)",
        "Ведомость вычисления координат теодолитного хода (Прил. 6)",
        "Журнал геометрического нивелирования IV класса (карандаш, постраничный контроль)",
        "Ведомость вычисления отметок вершин опорных точек (Прил. 8)",
        "Журнал тахеометрической съёмки (расстояния D, проложения d и отметки H_пк)",
        "Журнал нивелирования III класса с ведомостью (Прил. 16)"
    ]
    for i, d_item in enumerate(debts):
        st.checkbox(f"**Работа №{i+1}:** {d_item}", key=f"debt_chk_{i}")
