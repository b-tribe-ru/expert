import streamlit as st
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Graph, Line
from streamlit_echarts import st_pyecharts, st_echarts
from datetime import datetime
from github import Github
import base64

from github import InputGitTreeElement



from PIL import Image
image = Image.open('expoelectronica.png')

st.set_page_config(
    page_title="Экспертиза",
    page_icon="📺",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.yandex.ru',
        'Report a bug': "https://www.yandex.ru",
        'About': "# Экспертиза проектов на наличие технологий искусственного интеллекта!"
    }
)
st.image(image, caption=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

primaryColor = "lightgray"
s = f"""
<style>
div.stButton > button:first-child {{ border: 2px solid {primaryColor}; border-radius:3px 3px 3px 3px; background-color: white ; color:dimgray;}}
div.stButton > button:hover {{ border-inline-start: solid; writing-mode: horizontal-tb;   background-color: lightblue;    color:black;    }}
</style>
"""
st.markdown(s, unsafe_allow_html=True)




# Инициализация st.session_state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if 'button' not in st.session_state:
        st.session_state.button = False

if "answers" not in st.session_state:
    st.session_state.answers = []

def click_button():
    st.session_state.button = not st.session_state.button

# Функция для отображения страницы с вопросом и вариантами ответа
def display_question_page(question, options, slider_ranges):
    st.header(question)
    if "slider_value" not in st.session_state:
        st.session_state.slider_value = 20 # Установите начальное значение слайдера

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = options[0] # Установите первый вариант ответа по умолчанию
    

    # Создаем пользовательский интерфейс, который будет выглядеть как радиокнопки
    for option in options:
        if st.button(option, key=option, on_click=click_button):
            st.session_state.selected_option = option
        


    # Проверяем, что выбранный вариант существует в списке options
    if st.session_state.selected_option not in options:
        #st.error("Выбранный вариант не найден в списке вариантов ответа.")
        st.session_state.selected_option = options[0]
        return # Прекращаем выполнение функции

# Создаем слайдер
    slider_range = slider_ranges[options.index(st.session_state.selected_option)]
    
    #selected_option = st.radio(label="", options=options, key="selected_option")
    #slider_range = slider_ranges[options.index(selected_option)]
    inputuser = st.session_state.slider_value
    st.markdown("""<hr style="height:1px;border:none;color:white;background-color:lightgray;" /> """, unsafe_allow_html=True)
   
    if slider_range[0] != slider_range[1]:
        st.session_state.slider_value = st.slider(label="Выберите количество баллов, которым соответствует проект", min_value=slider_range[0], max_value=slider_range[1], value=slider_range[0], step=1)
        inputuser = st.session_state.slider_value
    else:
        st.write("Для этого варианта присваивается значение: " + str(slider_range[0]) + " баллов")
        inputuser = slider_range[0]
   
    if st.session_state.selected_option:
        asdf = st.session_state.selected_option[0:150] + "..."
        st.markdown(f"<div align='justify'>Вы выбрали: {asdf}</div></span>", unsafe_allow_html=True)

    if st.button("Перейти к следующему вопросу"):
        st.session_state.current_question += 1
        # Сохраняем выбранный ответ и значение слайдера
        st.session_state.answers.append({
            "question_number": st.session_state.current_question,
            "selected_option": st.session_state.selected_option,
            "slider_value": inputuser
        })
        st.markdown("""
            <script>
                window.scrollTo(0, 0);
            </script>
        """, unsafe_allow_html=True)
        st.experimental_rerun()
# Список вопросов и вариантов ответа
questions = [
    {
        "question": "Степень важности, области применения, оценка эффекта от внедрения проекта в интересах ...",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Проект не имеет ... значения (отсутствует практическая ценность, возможность применения в настоящее время отсутствует)", 
                    "Проект не решает заявленную проблему или решает в незначительной степени", 
                    "Проект отвечает текущим потребностям ..., имеется возможность внедрения (применения) в отдельных системах, комплексах, образцах и целесообразен в ходе обеспечения мероприятий ...", 
                    "Проект полностью решает заявленную проблему, отвечает перспективным потребностям ..., имеет возможность межвидового применения (развития смежных областей)"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 15), (16, 20)]
    },
    {
        "question": "Научный уровень выполненных работ и сопоставление результатов с зарубежными аналогами",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Проект не имеет научного интереса (повторение известных подходов), либо рационального использования научного потенциала", 
                    "Новизна заключается за счет распространения известных принципов на новые объекты", 
                    "Сформулированная проблема имеет научный и практический интерес. Новизна проекта заключается в использовании нескольких известных принципов в новом сочетании для придания дополнительных свойств", 
                    "Проект относится к приоритетной области исследований. Принципиально новые результаты (устранение существующей проблематики): новые теоретико- экспериментальные подходы к технологиям ИИ, новые принципы построения систем ИИ, новые оригинальные научно-технические решения"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 15), (16, 20)]
    },
    {
        "question": "Соответствие технологического и производственного потенциала заявленным требованиям к проекту при организации массового производства",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Требуется замена технических средств и технологического процесса производства (отсутствуют необходимые элементы производственных технологий, применение в технологической производственной цепочке импортируемых элементов из «недружественных» стран, критическая зависимость от поставщиков (субподрядчиков), отсутствие складских резервов, ограничения по отсутствию поддержки и др.), отсутствие опыта создания успешных проектов в сфере ИИ", 
                    "Требуется незначительная модернизация технических средств процесса производства, либо необходимость совместной разработки с организациями, отсутствие необходимых наборов данных (знаний, правил) для обучения систем ИИ", 
                    "Требуется незначительная модернизация технологического процесса производства (недостаток имеющегося в организации оборудования для работ с ИИ)", 
                    "Модернизация для массового производства не требуется (производственные технологии, станки, оснастка, инструмент, измерительные приборы, средства автоматизации производства, производственное, технологическое и испытательное оборудование позволяют создать производственно-технологический задел)"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 15), (16, 20)]
    },
    {
        "question": "Уровень технической готовности в соответствии с технологической зрелостью программных и технических средств систем и технологий ИИ и ожидаемые сроки завершения проекта",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Сформулирована фундаментальная концепция технологии и обоснована полезность технологии. Определены целевые области применения технологии и определены критические элементы технологии. Получен макетный образец с демонстрацией ключевого функционала. Проект использует лицензии GNU GPL", 
                    "Продемонстрированы ключевые характеристики макетного образца. Получен лабораторный образец и подготовлен лабораторный стенд. Проведены испытания базовых функций связи образца с другими элементами системы. Изготовлен и испытан экспериментальный образец в реальном масштабе по полупромышленной технологии", 
                    "При испытаниях образца (стенда) воспроизведены основные внешние условия. Изготовлен репрезентативный полнофункциональный образец на пилотной производственной линии. Подтверждены рабочие характеристики образца в условиях, приближенных к реальности. Проведены испытания (апробации, военно-технические эксперименты) опытно-промышленного образца в реальных условиях эксплуатации с подтверждением протоколами испытаний макетных и экспериментальных образцов (составных частей, узлов и агрегатов). Окончательно подтверждена работоспособность образца. Запущены опытно-промышленное производство и сертификация образца", 
                    "Проект удовлетворяет всем требованиям — инженерным, производственным, эксплуатационным, а также требованиям к качеству и надежности, и выпускается серийно. Наличие у заявителя документов, подтверждающих наличие научно-технического задела (проект и (или) его отдельные элементы защищены документами, подтверждающими авторство, и (или) имеют патент), результаты научно-исследовательских работ, экспертных заключений на предлагаемый к рассмотрению проект, а также предложений по готовому проекту, оформленный в виде тематических карточек, справок-обоснований и технико-экономических обоснований на аванпроекты (инициативные разработки) научно-исследовательские или опытно-конструкторские работы). Проект и (или) его отдельные элементы используется в интересах Российской Федерации (в том числе по вопросам, непосредственно связанным с обеспечением ...) и показывает высокие метрики качества"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 15), (16, 20)]
    },
    {
        "question": "Технологическая основа и возможность использования отечественной электронно- компонентной базы при реализации (модернизации), трансфера проекта",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Проект (используемое ПО) использует преимущественно иностранные комплектующие", 
                    "Используется иностранная элементная база, с возможностью быстрой разработки, адаптации, применения российских комплектующих и ПО (микросхемы 2 уровня)", 
                    "Ключевые составляющие проекта выполнены на российских комплектующих, с некритичным использованием типовых иностранных решений, либо допускает использование российских аналогов иностранных решений (микросхемы 1 уровня)", 
                    "Проект выполнен полностью на российских программных и аппаратных решениях (включая IP-блоки в микросхемах) на российских заводах"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 15), (16, 20)]
    },
    {
        "question": "Техническая (вычислительная) сложность используемых аппаратных решений",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Микроконтроллер, одноплатный компьютер: Atmel, Espressif, STMicroelectronics, RaspberryPi и аналоги (Coral, Khadas Vim3, Rock PI ЗА 3568, HaiIo8, MAIX-III), Low End-процессоры: Intel NCS2, Atom, Sempron, Pentium N-серии и др.", 
                    "CPU: Аквариус, Байкал, Комдив-64, Модуль, Мотив НТ, Элвис, Эльбрус, Iva Н, Nvidia, Syntacore, Huawei Atlas, Google TPU, Китай (ACCEL, Da Vinci, Biren, Cambricon, DeepEdgelOMax, Dragon, Enflame, HanGuang800, Horizon Robotics, Kunlun, XuanTie, Zixiao) и др.", 
                    "CPU: архитектуры x86/32/64/128, базовые процессорные комплекты общего назначения с совмещением аппаратной многопоточности и наборами инструкций SSE, AVX и др.", 
                    "Применение оптимизационных библиотек, GP GPU-видеоускорители, GPU-сервер", 
                    "Векторный (тензорный, нейро) процессор", 
                    "Мемристивные устройства и аналоги (для капсульных (импульсных, спайковых) ИНС)", 
                    "Нейрокомпьютер, нейронный квантовый компьютер, InMemory-вычисления, оптические компьютерные архитектуры, тензорные поезда, распределенные SWARM-вычисления на сети малых EDGE устройств", 
                    "Аппаратная система части нейронной сети (пример: нейронов, весов, свёрточных фильтров, аппаратная реализация полной топологии искусственной нейронной сети)", 
                    "Иное (пример: биологическое, химическое, протонные искусственные синапсы, оптическая, квантовая ИНС, физическое решение на фазовых переходах и др.)"],
        "slider_ranges": [(0, 0), (1, 2), (3, 4), (5, 6), (7, 10), (11, 12), (13, 13), (14, 16), (17, 19), (20, 20)]
    },
    {
        "question": "Программное исполнение, функциональная конфигурация",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Clojure, Go, Java, Kotlin, Lua, MathLab, .Net, Node, Octave, Python, R, Scala и др.", 
                    "Фрэймворки ML, платформы для автоматизации цикла разработки ИИ, оркестраторы утилит, настройки моделей и оптимизации гиперпараметров, версионирования, визуализации и мониторинга", 
                    "Традиционные и функциональные", 
                    "Нативные (процедурные) языки (С, С++ и др.)", 
                    "AutoML (автоматическое построение и обучение моделей), PuzzleLib, PlatLib, MLJET, LightAutoML, Fedot, Платформа-ГНС и другие Российские фреймворки", 
                    "Объектно-ориентированные: специализированные машинные коды (ассемблер), собственный язык программирования для машинного обучения с поддержкой распределенного машинного обучения"],
        "slider_ranges": [(0, 0), (1, 5), (6, 10), (11, 12), (13, 15), (16, 17), (18, 20)]
    },
    {
        "question": "Сформированные архитектурные требования к топологии искусственных нейронных сетей (классических методов)",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Классическое представление архитектуры существующей сети (топология слоев/связей)", 
                    "Преобразование топологий классических архитектур, элементов сети, функций, методов или подходов", 
                    "Сети прямого распространения, когнитрон (неокогнитрон), линейные модели, бинарные графы, когнитивные карты и правила, ER-диаграммы, UML, пробит-модели, поисковые алгоритмы", 
                    "Сети Хопфилда, Петри, Марковские (скрытые) цепи, машины Больцмана, самоорганизующиеся и радиально-базисные сети", 
                    "Сети на базе метода опорных векторов, KNN, линейный дискриминационный анализ, факторизационные машины, уменьшение размерности (обобщение)", 
                    "Автоэнкодеры, глубокие сети доверия, Highway Networks, нечеткие сети", 
                    "Свёрточные сети и комбинации их архитектур", 
                    "Рекуррентные сети, сеть Хэмминга, Сиамские сети", 
                    "Сети адаптивного резонанса, ассоциативные сети и сети с долгосрочной, краткосрочной памятью, GRU", 
                    "Генеративные (глубокие, диффузные, состязательные, вероятностные) сети, деревья эешений, бэггинг, случайный лес, стохастический градиентный спуск, наивный байесовский классификатор", 
                    "Эволюционные, генетические алгоритмы, самоорганизующиеся системы, обучение с подкреплением, жидкие, Extreme Learning Machine, эхо-сети, Deep Residual Network, Differentiable Neural Compute, Neural Tuning Machine, капсульные и другие детекторные сети", 
                    "Сети-трансформеры (реформеры), графовые нейронные сети, сети внимания и остаточные сети, гибридные, коллективные, экспертные (фундаментальные, мультимодальные) модели и др.", 
                    "Иная архитектура: ансамбли моделей, конкурирующие модели и агенты в open-ended environment, провайдеры моделей, создание собственных моделей и фрэймворков ML, отраслевых решений (программных комплексов)"],
        "slider_ranges": [(0, 0), (1, 2), (3, 4), (5, 5), (6, 6), (7, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 14), (15, 16), (17, 18), (19, 20)]
    },
    {
        "question": "Область технологий искусственного интеллекта",
        "options": ["Показатель в явном виде не представлен, либо не определен", 
                    "Реализация задач в области технического зрения, анализа и синтеза данных сенсорно—эффекторных систем", 
                    "Реализация задач в области социальных коммуникаций, кадрового потенциала и в системах обработки естественного языка (Conversational NLU, NLP)", 
                    "Реализация задач в области интеллектуальных систем управления, прогнозирования и поддержки принятия решений, информационно-аналитического взаимодействия и динамического манипулирования", 
                    "Реализация задач в области доверенных систем и обеспечении информационной безопасности технологиями искусственного интеллекта", 
                    "Реализация задач в области перспективных методов и экспериментальных технологий искусственного интеллекта"],
        "slider_ranges": [(0, 0), (1, 20), (1, 20), (1, 20), (1, 20), (1, 20)]
    },
]



# Отображение текущего вопроса
if st.session_state.current_question < len(questions):
    question_data = questions[st.session_state.current_question]
    display_question_page(question_data["question"], question_data["options"], question_data["slider_ranges"])

    #st.write("Все вопросы были отвечены.")

if st.session_state.current_question >= len(questions):
    #st.write("Все вопросы были отвечены.")
    # Создаем DataFrame для отображения в таблице
    
    df = pd.DataFrame(st.session_state.answers)
    #st.write(df)
    
    #print(df['slider_value'].values)
    llist = df.iloc[0:9, 2]
    llist0 = df.iloc[0:9, 0]
    llist1 = df.iloc[0:9, 1]
    
    st.header("Суммарные показатели проекта:")
    
    c = (
        Line()
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .add_xaxis(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        .add_yaxis("Проект", llist)
        )
    st_pyecharts(c)

    
    dddd = llist.to_numpy()

   
    st.header("Граф проекта:")
    mn = 70
    nodes = [
    {"name": "Важность", "symbolSize": int(dddd[0]/20*mn)},
    {"name": "Научный задел", "symbolSize": int(dddd[1]/20*mn)},
    {"name": "ПТЗ", "symbolSize": int(dddd[2]/20*mn)},
    {"name": "УТГ", "symbolSize": int(dddd[3]/20*mn)},
    {"name": "Импортозамещение", "symbolSize": int(dddd[4]/20*mn)},
    {"name": "Аппраратная часть", "symbolSize": int(dddd[5]/20*mn)},
    {"name": "Программное исполнение", "symbolSize": int(dddd[6]/20*mn)},
    {"name": "Архитектура", "symbolSize": int(dddd[7]/20*mn)},
    {"name": "Технология ИИ", "symbolSize": int(dddd[8]/20*mn)},
    ]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get("name"), "target": j.get("name")})
    c = (
        Graph()
        .add("", nodes, links, repulsion=9000)
    .   set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    st_pyecharts(c)


    options = {
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["1", "2", "3", "7", "5", "6", "7", "8", "9"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": [int(dddd[0]), int(dddd[1]), int(dddd[2]), int(dddd[3]), int(dddd[4]), int(dddd[5]), int(dddd[6]), int(dddd[7]), int(dddd[8])],
                "type": "line",
                "areaStyle": {},
            }
        ],
    }

    st.header("Оценка проекта:")
   

    options = {
        "title": {"text": ""},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "legend": {"data": ["Проект", "Диплом", "Сертификат"]},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": [
            {
                "type": "category",
                "boundaryGap": False,
                "data": ["1", "2", "3", "7", "5", "6", "7", "8", "9"],
            }
        ],
        "yAxis": [{"type": "value"}],
        "series": [
            {
                "name": "Сертификат",
                "type": "line",
                "stack": "Сертификат",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [10, 10, 10, 10, 10, 10, 10, 10, 10],
            },
            
            {
                "name": "Диплом",
                "type": "line",
                "stack": "Диплом",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [5, 5, 5, 5, 5, 5, 5, 5, 5],
            },
            {
                "name": "Проект",
                "type": "line",
                "stack": "Проект",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [int(dddd[0]), int(dddd[1]), int(dddd[2]), int(dddd[3]), int(dddd[4]), int(dddd[5]), int(dddd[6]), int(dddd[7]), int(dddd[8])],
            },
        ],
    }



    st_echarts(options=options, height="400px")

    
    option = {
        "title": {"text": ""},
        "legend": {"data": ["Проект", "Диплом", "Сертификат"]},
        "radar": {
            "indicator": [
                {"name": "Важность", "max": 20},
                {"name": "Научный задел", "max": 20},
                {"name": "ПТЗ", "max": 20},
                {"name": "УТГ", "max": 20},
                {"name": "Импортозамещение", "max": 20},
                {"name": "Аппраратная часть", "max": 20},
                {"name": "Программное исполнение", "max": 20},
                {"name": "Архитектура", "max": 20},
                {"name": "Технология ИИ", "max": 20},
            ]
        },
        "series": [
            {
                "name": "Сравнение проектов",
                "type": "radar",
                "data": [
                    {
                        "value": [int(dddd[0]), int(dddd[1]), int(dddd[2]), int(dddd[3]), int(dddd[4]), int(dddd[5]), int(dddd[6]), int(dddd[7]), int(dddd[8])],
                        "name": "Проект",
                    },
                    {
                        "value": [5, 5, 5, 5, 5, 5, 5, 5, 5],
                        "name": "Диплом",
                    },
                    {
                        "value": [10, 10, 10, 10, 10, 10, 10, 10, 10],
                        "name": "Сертификат",
                    },
                ],
            }
        ],
    }
    st_echarts(option, height="400px")

    st.header("Таблица ответов:")
    

    data = [
    [dddd[0], dddd[3], dddd[6]],
    [dddd[1], dddd[4], dddd[7]],
    [dddd[2], dddd[5], dddd[8]]
    ]

    
     # Вычисляем сумму всех значений в массиве
    total_sum = sum(int(cell) for row in data for cell in row)
    # Вычисляем процентное отношение суммы к числу 180
    percentage = (total_sum / 180) * 100
    # Создаем HTML-таблицу без заголовков
    html_table = "<table>"
    for row in data:
        html_table += "<tr>"
        for cell in row:
            html_table += f"<td>{cell}</td>"
        html_table += "</tr>"
    html_table += "</table>"
    
    html_table = "<table>"
    html_table += "<tr>"
    html_table += f"<td>{1}</td>"
    html_table += f"<td>{2}</td>"
    html_table += f"<td>{3}</td>"
    html_table += f"<td>{4}</td>"
    html_table += f"<td>{5}</td>"
    html_table += f"<td>{6}</td>"
    html_table += f"<td>{7}</td>"
    html_table += f"<td>{8}</td>"
    html_table += f"<td>{9}</td>"
    html_table += "</tr>"
    html_table += "<tr>"
    html_table += f"<td>{dddd[0]}</td>"
    html_table += f"<td>{dddd[1]}</td>"
    html_table += f"<td>{dddd[2]}</td>"
    html_table += f"<td>{dddd[3]}</td>"
    html_table += f"<td>{dddd[4]}</td>"
    html_table += f"<td>{dddd[5]}</td>"
    html_table += f"<td>{dddd[6]}</td>"
    html_table += f"<td>{dddd[7]}</td>"
    html_table += f"<td>{dddd[8]}</td>"
    html_table += "</tr>"
    html_table += "</table>" 
    

    
    # Добавляем сумму в таблицу
    html_table += f"<p><div align='justify'>Сумма всех значений: {total_sum} балла(ов) ({(percentage):.2f}%)</div></p>"

    # Выводим HTML-таблицу
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("""<hr style="height:2px;border:none;color:white;background-color:lightgray;" /> """, unsafe_allow_html=True)



    # Создаем DataFrame из данных
    #df = pd.DataFrame(data, columns=["1", "2", "3"])

    # Добавляем кнопку для загрузки CSV-файла
    username = st.text_input('Эксперт (фамилия, инициалы):')
    project = st.text_input('Название проекта: ')
    verdikt = st.text_input('Заключение эксперта: ')
   
    data_save = username + ',' + project+ ',' + str(dddd[0])+ ',' + str(dddd[1])+ ',' + str(dddd[2])+ ',' + str(dddd[3])+ ',' + str(dddd[4])+ ',' +str(dddd[5])+ ',' + str(dddd[6])+ ',' + str(dddd[7])+ ',' + str(dddd[8])+ ',' +str(total_sum)+ ',' +str(percentage) + ',' + str(verdikt)

    

    reference = str(datetime.now().date()) + ' ' + str(username) + ' ' + str(project) 
    
    

    # href = f'<a href="data:text/plain;charset=UTF-8,{data_save}" download="{reference}.txt">Скачать результат оценки проекта</a> ({reference}.txt)'
    # st.markdown(href, unsafe_allow_html=True)

    #st.download_button(label="Скачать результат оценки проекта", data=data_save, file_name=reference)


    if st.button('Опубликовать результат оценки проекта'):
        
        # access_token = "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" 

        # gh = Github(access_token)

        # for repo in gh.get_user().get_repos():
            

        st.write('Подключение установлено...')
        g = Github("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")

        with open(reference + ".csv", "w") as file:
            file.write(data_save)
        st.write('Файл подготовлен...')
        # for personal repo
        repo = g.get_user().get_repo('expert')

        all_files = []
        contents = repo.get_contents("")
        #print('contents')
        #print(contents)

        file_list = [
        reference+'.csv',
        ]
        file_names = [
        reference+'.csv',
        ]
        commit_message = 'expert opinion'
        master_ref = repo.get_git_ref('heads/main')
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        element_list = list()
        st.write('Производится публикация...')

        # Define the subdirectory path
        subdirectory_path = 'expert_logs/'



        for i, entry in enumerate(file_list):
            with open(entry) as input_file:
                data = input_file.read()
            if entry.endswith('.png'): # images must be encoded
                data = base64.b64encode(data)
            file_path_in_repo = subdirectory_path + file_names[i]
            element = InputGitTreeElement(file_path_in_repo, '100644', 'blob', data)
            element_list.append(element)

        tree = repo.create_git_tree(element_list, base_tree)
        
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
        st.write('Результат опубликован успешно в ' + str(datetime.now()))
