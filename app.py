import flet as ft
import math
import random
import json
import urllib.request
import urllib.parse
from datetime import date

# ================= ПАСТЕЛЬНАЯ ПАЛИТРА 2026 (БЕЗ БЕЛОГО ЦВЕТА #FFFFFF) =================
BG_OAT = "#ECE7DF"           # Основной овсяно-кремовый фон окна
BG_PANEL = "#E3DDD3"         # Панели и поля ввода (тёплый кашемир)
BG_CARD = "#F4F0E8"          # Базовая карточка (молочный пергамент)

SAGE_BG = "#D6E5DD"          # Пастельный шалфей
SAGE_BORDER = "#B5CFC1"
SAGE_TEXT = "#233D31"

LAVENDER_BG = "#DFD9EC"      # Пастельная лаванда
LAVENDER_BORDER = "#C3B9DA"
LAVENDER_TEXT = "#332B4D"

PEACH_BG = "#F1DFD6"         # Пастельный персик
PEACH_BORDER = "#DFC2B3"
PEACH_TEXT = "#4F3020"

SKY_BG = "#D8E6F0"           # Пастельное небо
SKY_BORDER = "#B6CFE2"
SKY_TEXT = "#1F3A4D"

BUTTER_BG = "#F0E8C9"        # Пастельное сливочное масло
BUTTER_BORDER = "#D9CE9E"
BUTTER_TEXT = "#4A3F17"

TEXT_DARK = "#2E2C29"        # Мягкий графит вместо чёрного
TEXT_MUTED = "#6E6A63"       # Приглушённый серо-бежевый
BORDER_SOFT = "#D6D0C4"

# ================= БАЗА ЗНАНИЙ И 8 НЕДЕЛЬ ПЛАНА (27.10.2026 – 15.12.2026) =================
STUDY_BLOCKS = [
    {
        "week": 1,
        "dates": "27.10.2026 – 02.11.2026",
        "start": date(2026, 10, 27),
        "end": date(2026, 11, 2),
        "bg": SAGE_BG, "border": SAGE_BORDER, "tc": SAGE_TEXT,
        "title": "Блок 1: Теория погрешностей, Карта М 1:50 000 и Профиль А–В",
        "tasks": [
            "Классификация погрешностей (грубые, систематические, случайные). Предельная погрешность Δ_пред = 3m",
            "Сравнение точности линий через относительную погрешность (1/1000 и 1/2000)",
            "Лабораторная №1: Карта М 1:50 000 (географические координаты, Гаусс — Крюгер, Балтийская система высот)",
            "Лабораторная №2: План в горизонталях (М 1:5000), профиль А–В (МВ 1:100, вершина 36,6) и масштаб заложений d = (h·100)/i"
        ],
        "theory": (
            "1. ТЕОРИЯ ПОГРЕШНОСТЕЙ (Ловушки СДО ГУМРФ):\n"
            "• Измеренная величина — найдена путём сравнения с единицей меры.\n"
            "• Предельная погрешность: утроенная средняя квадратическая погрешность Δ_пред = 3m.\n"
            "• Точность линий разной длины сравнивают ТОЛЬКО по относительной погрешности: линия 1000 м с ошибкой 0,5 м (1/2000) в 2 раза точнее линии 200 м с ошибкой 0,2 м (1/1000).\n\n"
            "2. ЛАБОРАТОРНАЯ №1 (Карта М 1:50 000):\n"
            "• 3 системы: Географическая (φ, λ — по минутной рамке), прямоугольная Гаусса — Крюгера (X — осевой меридиан, Y — экватор со сдвигом +500 км на запад) и Балтийская система высот (от нуля Кронштадтского футштока).\n\n"
            "3. ЛАБОРАТОРНАЯ №2 (План в горизонталях и профиль А–В):\n"
            "• Горизонтальный масштаб 1:5000 (в 1 см 50 м), вертикальный масштаб профиля 1:100 (в 1 см 1 м — укрупнён в 50 раз для наглядности рельефа!).\n"
            "• Обязательно наносятся экстремумы (вершины холмов 36,6 м и 38,2 м) с плавным закруглением.\n"
            "• Масштаб заложений (гипербола при h = 1 м) строится по формуле: d = (h · 100) / i."
        ),
        "yt": "https://www.youtube.com/results?search_query=координаты+Гаусса+Крюгера+и+построение+профиля+рельефа",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%86%D0%B8%D1%8F_%D0%93%D0%B0%D1%83%D1%81%D1%81%D0%B0_%E2%80%94_%D0%9A%D1%80%D1%8E%D0%B3%D0%B5%D1%80%D0%B0"
    },
    {
        "week": 2,
        "dates": "03.11.2026 – 09.11.2026",
        "start": date(2026, 11, 3),
        "end": date(2026, 11, 9),
        "bg": LAVENDER_BG, "border": LAVENDER_BORDER, "tc": LAVENDER_TEXT,
        "title": "Блок 2: Теодолиты (4Т30П, 3Т5КП), поверки, углы и Место Нуля (МО)",
        "tasks": [
            "Классы точности теодолитов (Т1, Т2/Т5/Т10, Т15/Т30/Т60), расшифровка 4Т30П, деревянный усиленный штатив",
            "Геометрические условия осей теодолита (U–U ⊥ J–J, H–H ⊥ J–J, V–V ⊥ H–H) и поверки",
            "Способ приёмов (расхождение КЛ и КП ≤ 1,0') и способ круговых приёмов (замыкание горизонта)",
            "Расчёт Места Нуля МО = (КЛ+КП)/2, угла наклона ν = КЛ − МО и зенитного расстояния Z = 90° − ν"
        ],
        "theory": (
            "1. УСТРОЙСТВО И ПОВЕРКИ ТЕОДОЛИТА 4Т30П:\n"
            "• 4Т30П: 4-я модификация, Теодолит, СКО измерения угла одним приёмом 30'' (технический), Прямое изображение.\n"
            "• Штатив для точных теодолитов — деревянный усиленный; радиус дуги цилиндрического уровня — от 2,5 м.\n"
            "• Геометрические условия: 1) Ось уровня ⊥ вертикальной оси J–J; 2) Визирная ось V–V ⊥ оси вращения трубы H–H; 3) Ось вращения трубы H–H ⊥ вертикальной оси J–J.\n\n"
            "2. ФОРМУЛЫ УГЛОВ И ВЕРТИКАЛЬНОГО КРУГА (4Т30П):\n"
            "• Горизонтальный угол в полуприёме: β = Отсчёт(Правый) − Отсчёт(Левый). Допуск |β_КЛ − β_КП| ≤ 1,0'.\n"
            "• Место нуля: МО = (КЛ + КП) / 2.\n"
            "• Угол наклона: ν = КЛ − МО = МО − КП = (КЛ − КП) / 2.\n"
            "• Зенитное расстояние: Z = 90° − ν.\n"
            "• Ловушка СДО: Основное положение вертикального круга — то, при котором получают малый положительный отсчёт угла наклона повышения.\n"
            "• Ловушка СДО по 3Т5КП: горизонтальное проложение d напрямую не измеряется, а вычисляется по формуле d = D · cos²ν."
        ),
        "yt": "https://www.youtube.com/watch?v=2szRxKqej3M",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D0%B4%D0%BE%D0%BB%D0%B8%D1%82"
    },
    {
        "week": 3,
        "dates": "10.11.2026 – 16.11.2026",
        "start": date(2026, 11, 10),
        "end": date(2026, 11, 16),
        "bg": PEACH_BG, "border": PEACH_BORDER, "tc": PEACH_TEXT,
        "title": "Блок 3: Теодолитные ходы, ориентирование и Ведомость координат",
        "tasks": [
            "Дирекционные углы α, румбы r, переход от магнитного азимута α = A_м + δ − γ",
            "Передача дирекционного угла: для правых углов α_(n+1) = α_n + 180° − β_испр",
            "Угловая невязка f_β = ∑β_пр − 180°(n − 2), допуск f_βдоп = ±1,5'√n, распределение поровну с обратным знаком",
            "Приращения Δx = d·cos(α), Δy = d·sin(α), линейная невязка f_отн ≤ 1/2000, Ведомость координат"
        ],
        "theory": (
            "1. ОРИЕНТИРОВАНИЕ И ПЕРЕДАЧА ДИРЕКЦИОННОГО УГЛА:\n"
            "• Связь с магнитным азимутом: α = A_м + δ − γ (нужны три величины, поэтому в радиокнопках СДО правильный ответ — «Нет правильного ответа»).\n"
            "• Для правых по ходу углов: α_(n+1) = α_n + 180° − β_испр.\n"
            "• Для левых по ходу углов: α_(n+1) = α_n + β_испр − 180°.\n"
            "• Перевод в румбы: I ч. (0–90°) СВ: r = α; II ч. (90–180°) ЮВ: r = 180° − α; III ч. (180–270°) ЮЗ: r = α − 180°; IV ч. (270–360°) СЗ: r = 360° − α.\n\n"
            "2. УВЯЗКА ВЕДОМОСТИ КООРДИНАТ (Приложение 6):\n"
            "• Угловая невязка замкнутого полигона: f_β = ∑β_пр − 180°·(n − 2); допуск f_βдоп = ±1,5'·√n.\n"
            "• Линейные невязки: f_x = ∑Δx, f_y = ∑Δy, f_абс = √(f_x² + f_y²), относительная f_отн = f_абс / P ≤ 1/2000.\n"
            "• Поправки в приращения координат: δx_i = −(f_x / P) · d_i; δy_i = −(f_y / P) · d_i."
        ),
        "yt": "https://www.youtube.com/results?search_query=ведомость+вычисления+координат+теодолитного+хода",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BE%D0%B4%D0%BE%D0%BB%D0%B8%D1%82%D0%BD%D1%8B%D0%B9_%D1%85%D0%BE%D0%B4"
    },
    {
        "week": 4,
        "dates": "17.11.2026 – 23.11.2026",
        "start": date(2026, 11, 17),
        "end": date(2026, 11, 23),
        "bg": SKY_BG, "border": SKY_BORDER, "tc": SKY_TEXT,
        "title": "Блок 4: Геометрическое нивелирование, нивелиры Н-3 и рейки РН-3000",
        "tasks": [
            "Виды нивелирования: геометрическое (наиболее точное), тригонометрическое, механическое (профилограф), барометрическое",
            "Способы «из середины» (h = a − b) и «вперёд» (h = i − b), контактный уровень и компенсатор (Н-3К)",
            "Шашечная двусторонняя рейка РН-3000 (пятки красной стороны 4687 / 4787 / 4800 мм)",
            "Главная поверка нивелира: параллельность визирной оси и оси цилиндрического уровня (V–V || U–U)"
        ],
        "theory": (
            "1. ВИДЫ И СПОСОБЫ НИВЕЛИРОВАНИЯ:\n"
            "• Самый точный вид нивелирования — Геометрическое (Геометрический). Прибор для механического нивелирования — Профилограф.\n"
            "• Способ «из середины»: h = a − b (при равенстве плеч автоматически исключаются погрешность за главное условие нивелира V–V || U–U, кривизна Земли и рефракция).\n"
            "• Способ «вперёд»: h = i − b. Через Горизонт Инструмента: ГИ = H_A + a; H_пром = ГИ − c.\n\n"
            "2. НИВЕЛИР Н-3 И РЕЙКА РН-3000:\n"
            "• Классы нивелиров: высокоточные (Н-05), точные (Н-3, Н-3К с компенсатором), технические (Н-10).\n"
            "• Рейка РН-3000: длина 3000 мм, шашки по 1 см (10 мм), отсчёт в мм (4 цифры). Разность нулей черной и красной сторон — 4687, 4787 или 4800 мм."
        ),
        "yt": "https://www.youtube.com/results?search_query=устройство+нивелира+Н-3+отсчеты+по+рейке+РН-3000",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9D%D0%B8%D0%B2%D0%B5%D0%BB%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5"
    },
    {
        "week": 5,
        "dates": "24.11.2026 – 30.11.2026",
        "start": date(2026, 11, 24),
        "end": date(2026, 11, 30),
        "bg": BUTTER_BG, "border": BUTTER_BORDER, "tc": BUTTER_TEXT,
        "title": "Блок 5: Нивелирование III и IV классов и постраничный контроль",
        "tasks": [
            "Нивелирование IV класса: ЗЧ → ПЧ → ПК → ЗК, плечо ≤ 100 м (между рейками до 200 м), |h_ч − h_кр| ≤ 5 мм",
            "Постраничный контроль журнала: ∑З − ∑П = ∑h_выч и (∑З − ∑П)/2 = ∑h_ср",
            "Нивелирование III класса: 3 нити на чёрной стороне, плечо ≤ 75 м, неравенство плеч ≤ 2 м, |h_ч − h_кр| ≤ 3 мм"
        ],
        "theory": (
            "ДОПУСКИ НИВЕЛИРОВАНИЯ IV И III КЛАССОВ (Приложения 7, 8, 16):\n"
            "• IV класс: 4 отсчёта по средней нити (ЗЧ → ПЧ → ПК → ЗК). Максимальное плечо ≤ 100 м (между рейками до 200 м — в СДО выбирается «Нет правильного ответа»). Неравенство плеч ≤ 5 м. Расхождение |h_ч − h_кр| ≤ 5 мм. Допустимая невязка хода f_hдоп = ±50 мм·√L(км).\n"
            "• III класс: по чёрным сторонам берут отсчёты по 3 нитям (верхней, нижней дальномерным и средней), по красным — по средней нити. Плечо ≤ 75 м, неравенство плеч на станции ≤ 2 м (в секции ≤ 5 м). Расхождение |h_ч − h_кр| ≤ 3 мм! Допустимая невязка f_hдоп = ±10 мм·√L(км).\n"
            "• Постраничный контроль: ∑З − ∑П = ∑h_выч; (∑З − ∑П)/2 = ∑h_ср."
        ),
        "yt": "https://www.youtube.com/results?search_query=заполнение+журнала+нивелирования+4+класса+постраничный+контроль",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%9D%D0%B8%D0%B2%D0%B5%D0%BB%D0%B8%D1%80%D0%BD%D0%B0%D1%8F_%D1%81%D0%B5%D1%82%D1%8C"
    },
    {
        "week": 6,
        "dates": "01.12.2026 – 07.12.2026",
        "start": date(2026, 12, 1),
        "end": date(2026, 12, 7),
        "bg": SAGE_BG, "border": SAGE_BORDER, "tc": SAGE_TEXT,
        "title": "Блок 6: Тахеометрия, линейка Дробышева, ГИС, САПР и GPS/DGPS",
        "tasks": [
            "Тахеометрическая съёмка: d = D·cos²ν, превышение h = d·tg(ν) + i − V, отметка H_пк = H_ст + h, кроки",
            "Построение координатной сетки 10×10 см линейкой Ф.В. Дробышева (ЛТ-1, диагональ 70,711 см)",
            "Учебник Федотова: ГИС, САПР, 3 типа сеточных ЦММ (регулярная, адаптивная, гладкая), вешение «на себя», GPS (мин. 4 спутника) и DGPS (до 1 см)"
        ],
        "theory": (
            "1. ТАХЕОМЕТРИЧЕСКАЯ СЪЁМКА (Приложение 12):\n"
            "• Горизонтальное проложение: d = D · cos²(ν).\n"
            "• Табличное превышение: h' = d · tg(ν).\n"
            "• Полное превышение: h = d · tg(ν) + i − V; Отметка пикета: H_пк = H_ст + h.\n"
            "• Полевой схематический чертёж называется кроки.\n\n"
            "2. ЛИНЕЙКА ДРОБЫШЕВА, ЦММ И GPS/DGPS:\n"
            "• Линейка Ф.В. Дробышева (ЛТ-1) строит сетку квадратов 10×10 см по прямоугольному треугольнику (катеты 50 см, диагональ 70,711 см, точность 0,2 мм).\n"
            "• Три типа сеточных ЦММ: регулярная, адаптивная и гладкая.\n"
            "• Вешение линий: способ «на себя» точнее способа «от себя».\n"
            "• Спутниковые системы GPS/ГЛОНАСС: нужно минимум 4 спутника; дифференциальный режим DGPS с базовой станцией повышает точность до 1 см."
        ),
        "yt": "https://www.youtube.com/watch?v=rFNE93023Jc",
        "wiki": "https://ru.wikipedia.org/wiki/DGPS"
    },
    {
        "week": 7,
        "dates": "08.12.2026 – 14.12.2026",
        "start": date(2026, 12, 8),
        "end": date(2026, 12, 14),
        "bg": LAVENDER_BG, "border": LAVENDER_BORDER, "tc": LAVENDER_TEXT,
        "title": "Блок 7: Полный прогон базы СДО ГУМРФ (200 вопросов) и сдача работ",
        "tasks": [
            "Решать по 2–3 билета во вкладке «Тест СДО» с результатом ≥ 85%",
            "Проверить все полевые журналы карандашом (исправления одной чертой с причиной ошибки справа)",
            "Сдать проверенные ведомости и журналы 2-го семестра преподавателям кафедры"
        ],
        "theory": (
            "ПРАВИЛА ОФОРМЛЕНИЯ ОТЧЁТА ПО МЕТОДИЧКЕ ГУМРФ (2026):\n"
            "• Все полевые журналы заполняются строго простым карандашом. Ластик запрещён: ошибка зачёркивается одной тонкой чертой, сверху пишется верный отсчёт, справа — причина ошибки (причина зачёркивания).\n"
            "• Титульный лист (без слова «Приложение»), Дневник практики, Технический отчёт (с фото бригады 10×15 см на глянцевой бумаге) и Ведомости — синей ручкой или печатью."
        ),
        "yt": "https://www.youtube.com/results?search_query=инженерная+геодезия+подготовка+к+экзамену",
        "wiki": "https://sdo.gumrf.ru/"
    },
    {
        "week": 8,
        "dates": "15.12.2026",
        "start": date(2026, 12, 15),
        "end": date(2026, 12, 20),
        "bg": PEACH_BG, "border": PEACH_BORDER, "tc": PEACH_TEXT,
        "title": "Блок 8: Генеральная репетиция комиссии ГУМРФ",
        "tasks": [
            "Пройти контрольный билет в тренажёре без подсказок (≥ 90%)",
            "Провести устную защиту своих работ со встроенной нейросетью во вкладке «ИИ-Наставник»",
            "Уверенно сдать комиссию на отлично!"
        ],
        "theory": (
            "ЗОЛОТОЕ ПРАВИЛО ОТВЕТА НА КОМИССИИ:\n"
            "1) Чёткое определение → 2) Точная математическая формула → 3) Численный допуск из методички Конопацкого и Москаля."
        ),
        "yt": "https://www.youtube.com/results?search_query=геодезия+защита+практики",
        "wiki": "https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%B4%D0%B5%D0%B7%D0%B8%D1%8F"
    }
]

DEBTS_LIST = [
    "1. Лабораторная №1: Карта М 1:50 000 (координаты, Гаусс — Крюгер, поперечный масштаб)",
    "2. Лабораторная №2: План в горизонталях (М 1:5000), профиль А–В (М 1:100, вершина 36,6) и график заложений",
    "3. Журнал измерения горизонтальных углов (карандаш, замыкание горизонта, допуск полуприёмов ≤ 1')",
    "4. Журнал измерения длин линий и определения Места Нуля (МО)",
    "5. Ведомость вычисления координат теодолитного хода (6. Ведомость вычисления координат.xlsx)",
    "6. Журнал геометрического нивелирования IV класса (карандаш, постраничный контроль ∑З − ∑П = ∑h)",
    "7. Ведомость вычисления отметок вершин опорных точек (8. Ведомость вычисления отметок.xlsx)",
    "8. Журнал тахеометрической съёмки (все расстояния D, проложения d, превышения h и отметки H_пк)",
    "9. Журнал нивелирования III класса с ведомостью вычисления отметок реперов"
]

# ================= ВСТРОЕННАЯ НЕЙРОСЕТЬ НА PYTHON (БЕЗ КЛЮЧЕЙ!) =================
def query_builtin_ai_python(prompt_text: str) -> str:
    sys_msg = (
        "Ты — встроенный ИИ-экзаменатор и наставник по инженерной геодезии ГУМРФ им. адм. С.О. Макарова "
        "(кафедра Водных путей и водных изысканий, методичка А.В. Москаля и С.В. Конопацкого 2026 г., учебник Г.А. Федотова). "
        "Отвечай дружелюбно, чётко, с формулами и допусками ГУМРФ на русском языке."
    )
    try:
        req_data = json.dumps({
            "model": "openai",
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt_text}
            ]
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://text.pollinations.ai/openai",
            data=req_data,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=16) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            ans = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
            if ans:
                return ans
    except Exception:
        pass

    low = prompt_text.lower()
    for b in STUDY_BLOCKS:
        if any(w in low for w in b["title"].lower().split()):
            return f"🌿 Из встроенной базы ГУМРФ ({b['title']}):\n\n{b['theory']}"
    return "🌿 Сводка ключевых правил и формул ГУМРФ:\n\n" + "\n\n".join(b["theory"] for b in STUDY_BLOCKS[:4])

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ РАСЧЁТОВ =================
def fmt_dm(total_min: float) -> str:
    sign = "-" if total_min < 0 else ""
    am = abs(total_min)
    deg = int(am // 60)
    m = am % 60
    m_str = f"{int(m):02d}" if float(m).is_integer() else f"{m:04.1f}"
    return f"{sign}{deg}°{m_str}'"

# ================= ГЛАВНАЯ ФУНКЦИЯ ПРИЛОЖЕНИЯ FLET =================
def main(page: ft.Page):
    page.title = "Геодезия ГУМРФ • Нативное Пастельное Приложение"
    page.bgcolor = BG_OAT
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1020
    page.window_height = 820

    # --- СОСТОЯНИЕ ГАЛОЧЕК ---
    checked_state = {}

    def load_saved_state():
        nonlocal checked_state
        raw = page.client_storage.get("gumrf_checks")
        if raw:
            try:
                checked_state = json.loads(raw)
            except Exception:
                checked_state = {}

    def save_check(key: str, val: bool):
        checked_state[key] = val
        try:
            page.client_storage.set("gumrf_checks", json.dumps(checked_state))
        except Exception:
            pass
        update_progress_banner()

    load_saved_state()

    # --- МОДАЛЬНОЕ ОКНО ПОЛНОГО КОНСПЕКТА ---
    dlg_title = ft.Text("", weight=ft.FontWeight.BOLD, size=18, color=SAGE_TEXT)
    dlg_body = ft.Text("", size=14, color=TEXT_DARK, selectable=True)
    info_dialog = ft.AlertDialog(
        bgcolor=BG_CARD,
        title=dlg_title,
        content=ft.Container(
            content=ft.Column([dlg_body], scroll=ft.ScrollMode.AUTO),
            width=680,
            height=420,
            padding=10,
            bgcolor=BUTTER_BG,
            border_radius=16,
            border=ft.border.all(1, BUTTER_BORDER)
        ),
        actions=[
            ft.TextButton("Закрыть конспект", on_click=lambda e: page.close(info_dialog))
        ]
    )

    def open_theory_modal(block_item):
        dlg_title.value = block_item["title"]
        dlg_body.value = block_item["theory"]
        page.open(info_dialog)

    # ================= ЭКРАН 0: ПЛАН НА 8 НЕДЕЛЬ =================
    progress_text = ft.Text("Прогресс подготовки: 0%", weight=ft.FontWeight.BOLD, size=15, color=SAGE_TEXT)
    progress_bar = ft.ProgressBar(value=0, color="#5C8A73", bgcolor=BG_PANEL, height=10, border_radius=8)

    def update_progress_banner():
        total_t = sum(len(b["tasks"]) for b in STUDY_BLOCKS)
        done_t = sum(1 for k, v in checked_state.items() if k.startswith("w_") and v)
        pct = done_t / total_t if total_t else 0
        progress_bar.value = pct
        progress_text.value = f"Изучено тем по 8-недельному плану: {int(pct * 100)}% ({done_t} из {total_t})"
        page.update()

    weeks_column = ft.Column(spacing=14)
    today_d = date.today()
    cur_week_num = 1
    for b in STUDY_BLOCKS:
        if b["start"] <= today_d <= b["end"]:
            cur_week_num = b["week"]
            break

    weeks_column.controls.append(
        ft.Container(
            bgcolor=SAGE_BG,
            border=ft.border.all(1.5, SAGE_BORDER),
            border_radius=22,
            padding=20,
            content=ft.Column([
                ft.Text(f"📅 Календарный маршрут к комиссии (Сегодня: {today_d.strftime('%d.%m.%Y')} • Активна Неделя {cur_week_num})",
                        size=18, weight=ft.FontWeight.BOLD, color=SAGE_TEXT),
                progress_text,
                progress_bar
            ], spacing=8)
        )
    )

    for b in STUDY_BLOCKS:
        t_controls = []
        for idx, t_str in enumerate(b["tasks"]):
            k = f"w_{b['week']}_{idx}"
            cb = ft.Checkbox(
                label=t_str,
                value=checked_state.get(k, False),
                fill_color="#5C8A73",
                check_color=BG_CARD,
                on_change=lambda e, key=k: save_check(key, e.control.value)
            )
            t_controls.append(cb)

        links_row = ft.Row([
            ft.ElevatedButton(
                "📖 Открыть полный конспект",
                bgcolor=BUTTER_BG,
                color=BUTTER_TEXT,
                on_click=lambda e, blk=b: open_theory_modal(blk)
            ),
            ft.ElevatedButton(
                "▶️ Видео YouTube",
                bgcolor=PEACH_BG,
                color=PEACH_TEXT,
                on_click=lambda e, url=b["yt"]: page.launch_url(url)
            ),
            ft.ElevatedButton(
                "🌐 Статья Википедии",
                bgcolor=SKY_BG,
                color=SKY_TEXT,
                on_click=lambda e, url=b["wiki"]: page.launch_url(url)
            )
        ], wrap=True, spacing=8)

        weeks_column.controls.append(
            ft.Container(
                bgcolor=b["bg"],
                border=ft.border.all(1.5, b["border"]),
                border_radius=22,
                padding=20,
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Неделя {b['week']} ({b['dates']})", weight=ft.FontWeight.BOLD, size=13, color=b["tc"]),
                        ft.Container(
                            content=ft.Text("🌿 Текущий этап" if b["week"] == cur_week_num else "По плану", size=12, weight=ft.FontWeight.BOLD, color=b["tc"]),
                            bgcolor=BUTTER_BG, padding=ft.padding.symmetric(horizontal=10, vertical=4), border_radius=12
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(b["title"], size=17, weight=ft.FontWeight.BOLD, color=b["tc"]),
                    ft.Column(t_controls, spacing=2),
                    links_row
                ], spacing=10)
            )
        )

    # ================= ЭКРАН 1: ВСТРОЕННАЯ НЕЙРОСЕТЬ (ЧАТ БЕЗ КЛЮЧЕЙ) =================
    chat_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=370)
    chat_list.controls.append(
        ft.Container(
            bgcolor=LAVENDER_BG, border=ft.border.all(1, LAVENDER_BORDER), border_radius=18, padding=14,
            content=ft.Text(
                "🌿 Привет! Я твоя встроенная нейросеть по инженерной геодезии ГУМРФ.\n"
                "Я работаю прямо внутри приложения без всяких ключей! Напиши любой вопрос, попроси проверить твои отсчёты или нажми кнопку симуляции комиссии.",
                color=LAVENDER_TEXT, size=14
            )
        )
    )

    ai_input = ft.TextField(
        hint_text="Напиши вопрос нейросети (например: Разбери допуски нивелирования III и IV класса)...",
        bgcolor=BG_CARD,
        border_color=LAVENDER_BORDER,
        border_radius=14,
        color=TEXT_DARK,
        expand=True
    )

    def send_ai_msg(custom_text=None):
        q_text = custom_text if custom_text else ai_input.value.strip()
        if not q_text:
            return
        ai_input.value = ""
        chat_list.controls.append(
            ft.Container(
                bgcolor=SAGE_BG, border=ft.border.all(1, SAGE_BORDER), border_radius=18, padding=14,
                content=ft.Text(f"Вы: {q_text}", color=SAGE_TEXT, weight=ft.FontWeight.W_600)
            )
        )
        wait_box = ft.Container(
            bgcolor=BUTTER_BG, border=ft.border.all(1, BUTTER_BORDER), border_radius=18, padding=14,
            content=ft.Text("⏳ Встроенная нейросеть готовит ответ по методичке ГУМРФ...", color=BUTTER_TEXT)
        )
        chat_list.controls.append(wait_box)
        page.update()

        ans = query_builtin_ai_python(q_text)
        wait_box.bgcolor = LAVENDER_BG
        wait_box.border = ft.border.all(1, LAVENDER_BORDER)
        wait_box.content = ft.Text(ans, color=LAVENDER_TEXT, selectable=True)
        page.update()

    ai_view = ft.Column([
        ft.Container(
            bgcolor=LAVENDER_BG, border=ft.border.all(1.5, LAVENDER_BORDER), border_radius=22, padding=20,
            content=ft.Column([
                ft.Text("🤖 Встроенная нейросеть-экзаменатор ГУМРФ", size=19, weight=ft.FontWeight.BOLD, color=LAVENDER_TEXT),
                ft.Text("Подключена напрямую из коробки (без API-ключей). Знает методичку Конопацкого и Москаля (2026), учебник Федотова и все ловушки СДО.", color=LAVENDER_TEXT),
                ft.Row([
                    ft.ElevatedButton("🎯 Вопрос от комиссии", bgcolor=PEACH_BG, color=PEACH_TEXT,
                                      on_click=lambda e: send_ai_msg("Задай мне каверзный вопрос от Конопацкого и Москаля по геодезии и проверь мой ответ")),
                    ft.ElevatedButton("⚡ Ловушки СДО ГУМРФ", bgcolor=SAGE_BG, color=SAGE_TEXT,
                                      on_click=lambda e: send_ai_msg("Перечисли все главные ловушки теста СДО ГУМРФ с правильными ответами")),
                    ft.ElevatedButton("📈 Защита Профиля А–В", bgcolor=SKY_BG, color=SKY_TEXT,
                                      on_click=lambda e: send_ai_msg("Какие вопросы задают на защите Лабораторной №2 по профилю А-В и масштабу заложений?"))
                ], wrap=True, spacing=8)
            ], spacing=10)
        ),
        ft.Container(
            bgcolor=BG_PANEL, border=ft.border.all(1, BORDER_SOFT), border_radius=22, padding=16,
            content=chat_list
        ),
        ft.Row([
            ai_input,
            ft.ElevatedButton("✨ Спросить ИИ", bgcolor=LAVENDER_BG, color=LAVENDER_TEXT, height=48, on_click=lambda e: send_ai_msg())
        ])
    ], spacing=14)

    # ================= ЭКРАН 2: БАЗА ЗНАНИЙ + ЖИВОЙ ПОИСК В ВИКИПЕДИИ =================
    wiki_input = ft.TextField(
        hint_text="Введи термин для поиска в русской Википедии (например: Теодолит, Нивелир, Проекция Гаусса — Крюгера)...",
        bgcolor=BG_CARD, border_color=SKY_BORDER, border_radius=14, color=TEXT_DARK, expand=True
    )
    wiki_results_col = ft.Column(spacing=8)

    def run_wiki_search(e):
        q = wiki_input.value.strip()
        if not q:
            return
        wiki_results_col.controls.clear()
        try:
            url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&utf8=&format=json"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("query", {}).get("search", [])[:4]:
                    title = item["title"]
                    clean_snip = item["snippet"].replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                    link = f"https://ru.wikipedia.org/wiki/{urllib.parse.quote(title)}"
                    wiki_results_col.controls.append(
                        ft.Container(
                            bgcolor=BG_CARD, border=ft.border.all(1, SKY_BORDER), border_radius=16, padding=14,
                            content=ft.Column([
                                ft.Text(title, weight=ft.FontWeight.BOLD, size=15, color=SKY_TEXT),
                                ft.Text(clean_snip + "...", size=13, color=TEXT_DARK),
                                ft.ElevatedButton("🌐 Читать статью в браузере", bgcolor=SKY_BG, color=SKY_TEXT,
                                                  on_click=lambda ev, u=link: page.launch_url(u))
                            ], spacing=6)
                        )
                    )
        except Exception:
            wiki_results_col.controls.append(ft.Text("Проверьте подключение к интернету.", color=PEACH_TEXT))
        page.update()

    kb_view = ft.Column([
        ft.Container(
            bgcolor=SKY_BG, border=ft.border.all(1.5, SKY_BORDER), border_radius=22, padding=20,
            content=ft.Column([
                ft.Text("📚 Полный справочник «От корки до корки» + Живой поиск в Википедии", size=18, weight=ft.FontWeight.BOLD, color=SKY_TEXT),
                ft.Row([wiki_input, ft.ElevatedButton("🔍 Найти", bgcolor=BUTTER_BG, color=BUTTER_TEXT, height=48, on_click=run_wiki_search)]),
                wiki_results_col
            ], spacing=10)
        )
    ], spacing=14)

    for b in STUDY_BLOCKS:
        kb_view.controls.append(
            ft.Container(
                bgcolor=b["bg"], border=ft.border.all(1.5, b["border"]), border_radius=20, padding=18,
                content=ft.Column([
                    ft.Text(b["title"], size=16, weight=ft.FontWeight.BOLD, color=b["tc"]),
                    ft.Text(b["theory"], size=13.5, color=b["tc"], selectable=True),
                    ft.Row([
                        ft.ElevatedButton("▶️ Видеоразбор YouTube", bgcolor=PEACH_BG, color=PEACH_TEXT,
                                          on_click=lambda e, u=b["yt"]: page.launch_url(u)),
                        ft.ElevatedButton("🌐 Статья Википедии", bgcolor=SKY_BG, color=SKY_TEXT,
                                          on_click=lambda e, u=b["wiki"]: page.launch_url(u))
                    ], spacing=8)
                ], spacing=8)
            )
        )

    # ================= ЭКРАН 3: СИМУЛЯТОР СДО ГУМРФ =================
    quiz_col = ft.Column(spacing=14)
    score_state = {"ok": 0, "err": 0}
    score_banner_txt = ft.Text("Верно: 0 • Ошибок: 0", weight=ft.FontWeight.BOLD, size=15, color=BUTTER_TEXT)

    def build_quiz_ticket(e=None):
        score_state["ok"] = 0
        score_state["err"] = 0
        score_banner_txt.value = "Верно: 0 • Ошибок: 0"
        quiz_col.controls.clear()

        zc, pc = random.randint(1200, 1950), random.randint(1100, 1850)
        dk = random.choice([-2, 0, 2])
        zk, pk = zc + 4800, pc + 4800 - dk
        hm = ((zc - pc) + (zk - pk)) / 2.0
        ans_niv = f"{hm:+.1f} мм"

        kl_m = random.randint(80, 240)
        mo_m = random.choice([-4, -2, 2, 4])
        nu_m = kl_m - mo_m
        ans_nu = "+" + fmt_dm(nu_m)

        questions = [
            {
                "q": f"1. [Расчёт нивелирования IV класса] Задняя рейка: Ч = {zc}, К = {zk}. Передняя рейка: Ч = {pc}, К = {pk}. Найдите среднее превышение h_ср:",
                "hint": "h_ч = ЗЧ − ПЧ; h_к = ЗК − ПК; h_ср = (h_ч + h_к) / 2.",
                "opts": [ans_niv, f"{-hm:+.1f} мм", f"{hm + 12:+.1f} мм", f"{zc - pc + 4800} мм"],
                "ans": ans_niv
            },
            {
                "q": f"2. [Расчёт угла наклона 4Т30П] Отсчёт по вертикальному кругу КЛ = +{fmt_dm(kl_m)}, место нуля МО = {mo_m:+}'. Чему равен угол наклона ν?",
                "hint": "Формула для 4Т30П: ν = КЛ − МО (внимание на знак МО!).",
                "opts": [ans_nu, "+" + fmt_dm(kl_m + mo_m), "-" + fmt_dm(nu_m), "+" + fmt_dm(nu_m + 15)],
                "ans": ans_nu
            },
            {
                "q": "3. [Ловушка СДО] Наиболее точный вид нивелирования имеет название:",
                "hint": "Спрашивают вид нивелирования, а не класс точности!",
                "opts": ["Геометрическое (Геометрический)", "Тригонометрическое", "Барометрическое", "Механическое"],
                "ans": "Геометрическое (Геометрический)"
            },
            {
                "q": "4. [Ловушка СДО] Разница превышений по чёрным и красным сторонам реек на станции при нивелировании III класса может составлять:",
                "hint": "В IV классе ≤ 5 мм, а в III классе — строже!",
                "opts": ["Не более 3 мм", "Не более 4 мм", "Не более 5 мм", "Не более 10 мм"],
                "ans": "Не более 3 мм"
            },
            {
                "q": "5. [Ловушка СДО] Максимальное расстояние между рейками при нивелировании IV класса в тесте СДО (при вариантах 50, 75, 100 м и «Нет правильного ответа»):",
                "hint": "Плечо от прибора до рейки — 100 м, а между двумя рейками — 200 м!",
                "opts": ["Нет правильного ответа (между рейками до 200 м)", "Не более 50 м", "Не более 75 м", "Не более 100 м"],
                "ans": "Нет правильного ответа (между рейками до 200 м)"
            },
            {
                "q": "6. [Лабораторная №2] По какой формуле строится гипербола масштаба заложений и почему на профиле А–В вертикальный масштаб (1:100) крупнее горизонтального (1:5000)?",
                "hint": "Связь заложения d, высоты сечения h и уклона i.",
                "opts": [
                    "d = (h·100)/i; вертикальный масштаб укрупняют в 50 раз для наглядного отображения рельефа",
                    "d = D·cos²ν; масштабы выбираются произвольно",
                    "h = a − b; для экономии миллиметровки",
                    "Δ_пред = 3m"
                ],
                "ans": "d = (h·100)/i; вертикальный масштаб укрупняют в 50 раз для наглядного отображения рельефа"
            }
        ]

        for idx, item in enumerate(questions):
            opts = list(item["opts"])
            random.shuffle(opts)
            feedback_txt = ft.Text("", weight=ft.FontWeight.BOLD, size=13.5)
            hint_txt = ft.Text(f"💡 Подсказка: {item['hint']}", size=13, color=BUTTER_TEXT, visible=False)

            def make_handler(chosen_opt, correct_opt, fb_ctrl):
                def on_click_opt(ev):
                    if chosen_opt == correct_opt:
                        score_state["ok"] += 1
                        fb_ctrl.value = f"✅ Верно! Ответ: {correct_opt}"
                        fb_ctrl.color = SAGE_TEXT
                    else:
                        score_state["err"] += 1
                        fb_ctrl.value = f"❌ Ошибка. Правильный ответ: {correct_opt}"
                        fb_ctrl.color = PEACH_TEXT
                    score_banner_txt.value = f"Верно: {score_state['ok']} • Ошибок: {score_state['err']}"
                    page.update()
                return on_click_opt

            btn_col = ft.Column(spacing=6)
            for o in opts:
                btn_col.controls.append(
                    ft.ElevatedButton(
                        o,
                        bgcolor=BG_PANEL,
                        color=TEXT_DARK,
                        on_click=make_handler(o, item["ans"], feedback_txt)
                    )
                )

            quiz_col.controls.append(
                ft.Container(
                    bgcolor=BG_CARD, border=ft.border.all(1.5, BORDER_SOFT), border_radius=20, padding=18,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(item["q"], weight=ft.FontWeight.BOLD, size=15, color=TEXT_DARK, expand=True),
                            ft.ElevatedButton("💡 Подсказка", bgcolor=BUTTER_BG, color=BUTTER_TEXT,
                                              on_click=lambda ev, h=hint_txt: (setattr(h, 'visible', not h.visible), page.update()))
                        ]),
                        hint_txt,
                        btn_col,
                        feedback_txt
                    ], spacing=8)
                )
            )
        page.update()

    build_quiz_ticket()

    sdo_view = ft.Column([
        ft.Container(
            bgcolor=BUTTER_BG, border=ft.border.all(1.5, BUTTER_BORDER), border_radius=22, padding=20,
            content=ft.Row([
                ft.Column([
                    ft.Text("🧪 Экзаменационный симулятор СДО ГУМРФ", size=18, weight=ft.FontWeight.BOLD, color=BUTTER_TEXT),
                    score_banner_txt
                ]),
                ft.ElevatedButton("🔄 Новый билет (Случайные числа)", bgcolor=SAGE_BG, color=SAGE_TEXT, on_click=build_quiz_ticket)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True)
        ),
        quiz_col
    ], spacing=14)

    # ================= ЭКРАН 4: ПОЛЕВЫЕ КАЛЬКУЛЯТОРЫ =================
    zc_f = ft.TextField(label="Задняя чёрная (мм)", value="1450", bgcolor=BG_CARD, width=180)
    zk_f = ft.TextField(label="Задняя красная (мм)", value="6239", bgcolor=BG_CARD, width=180)
    pc_f = ft.TextField(label="Передняя чёрная (мм)", value="1445", bgcolor=BG_CARD, width=180)
    pk_f = ft.TextField(label="Передняя красная (мм)", value="6233", bgcolor=BG_CARD, width=180)
    niv_res = ft.Text("", weight=ft.FontWeight.BOLD, color=SAGE_TEXT)

    def calc_niv(e):
        try:
            zc, zk = float(zc_f.value), float(zk_f.value)
            pc, pk = float(pc_f.value), float(pk_f.value)
            hc, hk = zc - pc, zk - pk
            hm = (hc + hk) / 2.0
            diff = abs(hc - hk)
            status = "✅ Допуск III и IV кл. выполнен" if diff <= 3 else ("⚠️ Только IV кл. (≤ 5 мм)" if diff <= 5 else "❌ БРАК (> 5 мм)")
            niv_res.value = f"Пятки: З = {zk-zc:.0f} мм, П = {pk-pc:.0f} мм | h_ч = {hc:+.0f} мм, h_к = {hk:+.0f} мм | Среднее h_ср = {hm:+.1f} мм | Расхождение: {diff:.0f} мм ({status})"
        except Exception:
            niv_res.value = "Проверьте введённые числа."
        page.update()

    hst_f = ft.TextField(label="Отметка ст. H_ст (м)", value="39.31", bgcolor=BG_CARD, width=160)
    i_f = ft.TextField(label="Высота прибора i (м)", value="1.48", bgcolor=BG_CARD, width=160)
    v_f = ft.TextField(label="Наводка V (м)", value="1.88", bgcolor=BG_CARD, width=160)
    d_f = ft.TextField(label="Расстояние D (м)", value="19.3", bgcolor=BG_CARD, width=160)
    nu_f = ft.TextField(label="Угол ν в минутах (напр. -3°45' = -225)", value="-225", bgcolor=BG_CARD, width=240)
    tach_res = ft.Text("", weight=ft.FontWeight.BOLD, color=LAVENDER_TEXT)

    def calc_tach(e):
        try:
            hst, i_v, v_v, d_v, nu_m = float(hst_f.value), float(i_f.value), float(v_f.value), float(d_f.value), float(nu_f.value)
            rad = math.radians(nu_m / 60.0)
            d_hor = d_v * (math.cos(rad) ** 2)
            h_pr = d_hor * math.tan(rad)
            h_tot = h_pr + i_v - v_v
            h_pk = hst + h_tot
            tach_res.value = f"Горизонт. проложение d = {d_hor:.2f} м | d·tg(ν) = {h_pr:+.2f} м | Превышение h = {h_tot:+.2f} м | Отметка пикета H_пк = {h_pk:.2f} м"
        except Exception:
            tach_res.value = "Проверьте введённые числа."
        page.update()

    calc_view = ft.Column([
        ft.Container(
            bgcolor=SAGE_BG, border=ft.border.all(1.5, SAGE_BORDER), border_radius=22, padding=20,
            content=ft.Column([
                ft.Text("1. Калькулятор станции нивелирования IV и III классов", size=17, weight=ft.FontWeight.BOLD, color=SAGE_TEXT),
                ft.Row([zc_f, zk_f, pc_f, pk_f], wrap=True),
                ft.ElevatedButton("📏 Проверить станцию", bgcolor=BUTTER_BG, color=BUTTER_TEXT, on_click=calc_niv),
                niv_res
            ], spacing=10)
        ),
        ft.Container(
            bgcolor=LAVENDER_BG, border=ft.border.all(1.5, LAVENDER_BORDER), border_radius=22, padding=20,
            content=ft.Column([
                ft.Text("2. Калькулятор тахеометрического пикета (Приложение 12)", size=17, weight=ft.FontWeight.BOLD, color=LAVENDER_TEXT),
                ft.Row([hst_f, i_f, v_f, d_f, nu_f], wrap=True),
                ft.ElevatedButton("🗺️ Посчитать пикет", bgcolor=BUTTER_BG, color=BUTTER_TEXT, on_click=calc_tach),
                tach_res
            ], spacing=10)
        )
    ], spacing=14)

    # ================= ЭКРАН 5: ЧЕК-ЛИСТ 9 РАБОТ ВТОРОГО СЕМЕСТРА =================
    debts_col = ft.Column(spacing=8)
    for idx, d_str in enumerate(DEBTS_LIST):
        k = f"debt_{idx}"
        debts_col.controls.append(
            ft.Checkbox(
                label=d_str,
                value=checked_state.get(k, False),
                fill_color="#5C8A73",
                check_color=BG_CARD,
                on_change=lambda e, key=k: save_check(key, e.control.value)
            )
        )

    debts_view = ft.Column([
        ft.Container(
            bgcolor=PEACH_BG, border=ft.border.all(1.5, PEACH_BORDER), border_radius=22, padding=20,
            content=ft.Column([
                ft.Text("📂 Чек-лист работ ко 2-му семестру и правила оформления", size=18, weight=ft.FontWeight.BOLD, color=PEACH_TEXT),
                ft.Text(
                    "• Все полевые журналы ведутся СТРОГО простым карандашом без ластика.\n"
                    "• Ошибочный отсчёт зачёркивается одной тонкой чертой, сверху пишется верный, а справа — причина ошибки.\n"
                    "• Титульники, дневник практики, тех. отчёт и ведомости оформляются синей ручкой или печатаются.",
                    color=PEACH_TEXT
                )
            ], spacing=8)
        ),
        ft.Container(
            bgcolor=BG_CARD, border=ft.border.all(1.5, BORDER_SOFT), border_radius=22, padding=20,
            content=debts_col
        )
    ], spacing=14)

    # ================= ПЕРЕКЛЮЧЕНИЕ ВКЛАДОК =================
    views = [weeks_column, ai_view, kb_view, sdo_view, calc_view, debts_view]
    body_container = ft.Container(
        content=views[0],
        padding=ft.padding.symmetric(horizontal=22, vertical=18),
        expand=True
    )

    def on_nav_change(e):
        idx = e.control.selected_index
        body_container.content = views[idx]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        bgcolor=BG_PANEL,
        indicator_color=SAGE_BG,
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="План 8 нед."),
            ft.NavigationBarDestination(icon=ft.Icons.SMART_TOY, label="ИИ-Наставник"),
            ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK, label="Справочник"),
            ft.NavigationBarDestination(icon=ft.Icons.QUIZ, label="Тест СДО"),
            ft.NavigationBarDestination(icon=ft.Icons.CALCULATE, label="Расчёты"),
            ft.NavigationBarDestination(icon=ft.Icons.TASK_ALT, label="Мои работы")
        ]
    )

    page.add(
        ft.Column([body_container], scroll=ft.ScrollMode.AUTO, expand=True)
    )
    update_progress_banner()

if __name__ == "__main__":
    ft.app(target=main)
