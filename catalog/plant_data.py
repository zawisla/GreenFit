"""Demonstration catalogue for GreenFit.

The data lives here, separate from the ``seed_plants`` management command, so the
command stays focused on logic. Every plant is one :func:`P` call; the positional
order matches the signature below. Choice values must stay within the model
choices (validated by ``seed_plants`` and by ``catalog.tests``):

    light    : low | medium | bright
    humidity : low | medium | high
    care     : easy | medium | hard
    water    : rare | regular | frequent
"""

from django.utils.text import slugify


def P(name, scientific_name, category, light, humidity, t_min, t_max,
      toxic, care, water, height, description):
    return {
        "name": name,
        "scientific_name": scientific_name,
        "category": category,
        "light_needs": light,
        "humidity_needs": humidity,
        "temp_min": t_min,
        "temp_max": t_max,
        "toxicity": toxic,
        "care_difficulty": care,
        "water_frequency": water,
        "max_height": height,
        "description": description,
    }


CATEGORIES = [
    {"name": "Суккуленты", "slug": "succulents",
     "description": "Засухоустойчивые растения, запасающие влагу в листьях и стеблях."},
    {"name": "Кактусы", "slug": "cacti",
     "description": "Колючие и неприхотливые жители засушливых регионов."},
    {"name": "Папоротники", "slug": "ferns",
     "description": "Влаголюбивые растения с ажурными вайями."},
    {"name": "Пальмы", "slug": "palms",
     "description": "Комнатные пальмы, создающие атмосферу тропиков."},
    {"name": "Декоративно-лиственные", "slug": "foliage",
     "description": "Растения, ценные своей выразительной листвой."},
    {"name": "Цветущие", "slug": "flowering",
     "description": "Красивоцветущие комнатные растения."},
    {"name": "Лианы и ампельные", "slug": "vines",
     "description": "Вьющиеся и свисающие растения для кашпо и опор."},
    {"name": "Комнатные деревья", "slug": "trees",
     "description": "Крупные одревесневающие растения и бонсай."},
    {"name": "Цитрусовые", "slug": "citrus",
     "description": "Плодоносящие цитрусовые деревца."},
    {"name": "Пряные травы", "slug": "herbs",
     "description": "Съедобные ароматические травы для подоконника."},
    {"name": "Луковичные", "slug": "bulbs",
     "description": "Растения с подземными луковицами и эффектным цветением."},
    {"name": "Бромелиевые", "slug": "bromeliads",
     "description": "Яркие тропические розеточные растения."},
    {"name": "Орхидеи", "slug": "orchids",
     "description": "Изысканные эпифитные растения с долгим цветением."},
    {"name": "Хищные растения", "slug": "carnivorous",
     "description": "Растения, ловящие насекомых для дополнительного питания."},
]


PLANTS = [
    # --- Суккуленты ---
    P("Сансевиерия трёхполосная", "Sansevieria trifasciata", "succulents", "low", "low", 15, 30, True, "easy", "rare", 90, "Жёсткие вертикальные листья, прощает тень и редкий полив."),
    P("Алоэ вера", "Aloe vera", "succulents", "bright", "low", 13, 30, True, "easy", "rare", 60, "Суккулент с целебным соком, любит яркий свет."),
    P("Эхеверия изящная", "Echeveria elegans", "succulents", "bright", "low", 10, 27, False, "easy", "rare", 15, "Аккуратная розетка из голубоватых листьев."),
    P("Толстянка (денежное дерево)", "Crassula ovata", "succulents", "bright", "low", 10, 30, True, "easy", "rare", 100, "Дерево-суккулент с мясистыми округлыми листьями."),
    P("Хавортия полосатая", "Haworthia fasciata", "succulents", "medium", "low", 15, 28, False, "easy", "rare", 15, "Миниатюрная розетка с белыми полосками, теневынослива."),
    P("Очиток Моргана", "Sedum morganianum", "succulents", "bright", "low", 15, 30, False, "easy", "rare", 60, "Ампельный суккулент со свисающими «хвостами»."),
    P("Каланхоэ Блоссфельда", "Kalanchoe blossfeldiana", "succulents", "bright", "low", 15, 28, True, "easy", "rare", 30, "Цветущий суккулент с яркими зонтиками соцветий."),
    P("Литопс (живые камни)", "Lithops", "succulents", "bright", "low", 15, 32, False, "hard", "rare", 5, "Крошечный суккулент, имитирующий камешки."),
    P("Агава американская", "Agave americana", "succulents", "bright", "low", 10, 32, True, "easy", "rare", 100, "Крупная розетка жёстких листьев с шипами."),
    P("Гастерия", "Gasteria", "succulents", "medium", "low", 12, 28, False, "easy", "rare", 25, "Толстые языковидные листья, переносит полутень."),
    P("Граптопеталум", "Graptopetalum paraguayense", "succulents", "bright", "low", 10, 30, False, "easy", "rare", 20, "Пастельные розетки, легко размножается листом."),
    P("Молочай тучный", "Euphorbia obesa", "succulents", "bright", "low", 15, 30, True, "medium", "rare", 20, "Шаровидный суккулент-молочай, сок ядовит."),
    P("Алоэ пёстрое", "Aloe variegata", "succulents", "bright", "low", 13, 28, True, "easy", "rare", 30, "Компактное алоэ с белым крапом на листьях."),
    P("Седум Рубротинктум", "Sedum rubrotinctum", "succulents", "bright", "low", 15, 30, True, "easy", "rare", 20, "«Бобовый» суккулент, краснеющий на солнце."),

    # --- Кактусы ---
    P("Эхинопсис", "Echinopsis", "cacti", "bright", "low", 10, 35, False, "easy", "rare", 30, "Классический шаровидный кактус с крупными цветками."),
    P("Маммиллярия", "Mammillaria", "cacti", "bright", "low", 10, 32, False, "easy", "rare", 20, "Небольшой кактус с венчиком цветков на макушке."),
    P("Опунция мелковолосистая", "Opuntia microdasys", "cacti", "bright", "low", 10, 35, False, "easy", "rare", 40, "Кактус с плоскими «лопатками» и мягкими глохидиями."),
    P("Шлюмбергера (декабрист)", "Schlumbergera", "cacti", "medium", "medium", 15, 26, False, "easy", "regular", 30, "Лесной кактус, цветущий зимой; любит влагу."),
    P("Рипсалис", "Rhipsalis", "cacti", "medium", "medium", 15, 28, False, "easy", "regular", 60, "Ампельный лесной кактус со свисающими побегами."),
    P("Гимнокалициум", "Gymnocalycium", "cacti", "bright", "low", 12, 32, False, "easy", "rare", 15, "Компактный кактус, часто с цветной прививкой."),
    P("Цереус перуанский", "Cereus repandus", "cacti", "bright", "low", 12, 35, False, "easy", "rare", 200, "Колонновидный кактус, со временем вырастает высоким."),
    P("Эхинокактус Грузони", "Echinocactus grusonii", "cacti", "bright", "low", 12, 35, False, "medium", "rare", 60, "«Золотой шар» с плотными золотистыми колючками."),

    # --- Папоротники ---
    P("Нефролепис возвышенный", "Nephrolepis exaltata", "ferns", "medium", "high", 16, 24, False, "medium", "frequent", 70, "Пышный папоротник, очищающий воздух."),
    P("Адиантум (венерин волос)", "Adiantum", "ferns", "medium", "high", 16, 22, False, "hard", "frequent", 40, "Нежные ажурные вайи, очень требователен к влажности."),
    P("Асплениум (костенец)", "Asplenium nidus", "ferns", "medium", "high", 18, 27, False, "medium", "frequent", 60, "Папоротник с цельными волнистыми листьями-«гнездом»."),
    P("Птерис критский", "Pteris cretica", "ferns", "medium", "high", 16, 24, False, "medium", "frequent", 40, "Невысокий папоротник с пёстрыми вайями."),
    P("Даваллия (заячьи лапки)", "Davallia", "ferns", "medium", "high", 16, 24, False, "medium", "frequent", 40, "Папоротник с пушистыми наземными корневищами."),
    P("Платицериум (олений рог)", "Platycerium", "ferns", "medium", "high", 18, 26, False, "hard", "frequent", 50, "Эпифит с вайями, похожими на рога оленя."),
    P("Блехнум", "Blechnum gibbum", "ferns", "medium", "high", 18, 24, False, "hard", "frequent", 60, "Папоротник, формирующий деревовидный ствол."),

    # --- Пальмы ---
    P("Хамедорея изящная", "Chamaedorea elegans", "palms", "medium", "medium", 18, 27, False, "medium", "regular", 180, "Компактная теневыносливая пальма, безопасна для животных."),
    P("Арека (хризалидокарпус)", "Dypsis lutescens", "palms", "bright", "medium", 18, 28, False, "medium", "regular", 250, "Пышная перистая пальма для светлых комнат."),
    P("Кентия", "Howea forsteriana", "palms", "medium", "medium", 16, 27, False, "easy", "regular", 250, "Элегантная неприхотливая пальма."),
    P("Ливистона", "Livistona", "palms", "bright", "medium", 16, 28, False, "medium", "regular", 200, "Веерная пальма с крупными рассечёнными листьями."),
    P("Финик Робелена", "Phoenix roebelenii", "palms", "bright", "medium", 16, 28, False, "medium", "regular", 180, "Изящная финиковая пальма с тонкими листьями."),
    P("Рапис высокий", "Rhapis excelsa", "palms", "medium", "medium", 16, 27, False, "easy", "regular", 200, "Бамбуковидная пальма, хорошо растёт в полутени."),
    P("Вашингтония", "Washingtonia", "palms", "bright", "low", 15, 30, False, "medium", "regular", 250, "Мощная веерная пальма, любит много света."),

    # --- Декоративно-лиственные ---
    P("Замиокулькас", "Zamioculcas zamiifolia", "foliage", "low", "low", 16, 30, True, "easy", "rare", 100, "Глянцевые перья листьев, копит влагу в корнях."),
    P("Драцена окаймлённая", "Dracaena marginata", "foliage", "medium", "medium", 18, 28, True, "easy", "regular", 200, "Стройное растение с узкими листьями на тонком стволе."),
    P("Диффенбахия", "Dieffenbachia", "foliage", "medium", "high", 18, 27, True, "medium", "regular", 150, "Крупные пёстрые листья; сок раздражает кожу."),
    P("Аглаонема", "Aglaonema", "foliage", "low", "medium", 18, 27, True, "easy", "regular", 70, "Теневыносливое растение с узорчатой листвой."),
    P("Калатея украшенная", "Calathea ornata", "foliage", "medium", "high", 18, 26, False, "hard", "frequent", 60, "Тёмные листья с тонкими розовыми полосками."),
    P("Маранта беложильчатая", "Maranta leuconeura", "foliage", "medium", "high", 18, 26, False, "hard", "frequent", 30, "«Молящееся растение», складывает листья на ночь."),
    P("Строманта", "Stromanthe sanguinea", "foliage", "medium", "high", 18, 27, False, "hard", "frequent", 60, "Яркая трёхцветная листва с розовой изнанкой."),
    P("Кротон (кодиеум)", "Codiaeum variegatum", "foliage", "bright", "medium", 18, 28, True, "hard", "regular", 100, "Кожистые листья всех оттенков жёлтого и красного."),
    P("Колеус", "Plectranthus scutellarioides", "foliage", "bright", "medium", 18, 28, True, "easy", "frequent", 60, "Бархатистые разноцветные листья, быстро растёт."),
    P("Фиттония", "Fittonia albivenis", "foliage", "medium", "high", 18, 26, False, "hard", "frequent", 15, "Низкое растение с сетью контрастных прожилок."),
    P("Пеперомия туполистная", "Peperomia obtusifolia", "foliage", "medium", "medium", 18, 26, False, "easy", "regular", 25, "Компактная пеперомия с мясистыми листьями."),
    P("Аукуба японская", "Aucuba japonica", "foliage", "medium", "medium", 10, 22, True, "easy", "regular", 150, "«Золотое дерево» с жёлтыми крапинами; ягоды ядовиты."),
    P("Хлорофитум хохлатый", "Chlorophytum comosum", "foliage", "bright", "medium", 15, 27, False, "easy", "regular", 40, "Дугообразные листья и «детки» на усах, растёт везде."),
    P("Аспидистра", "Aspidistra elatior", "foliage", "low", "low", 10, 25, False, "easy", "rare", 70, "«Чугунное растение», выносит глубокую тень."),
    P("Радермахера", "Radermachera sinica", "foliage", "bright", "medium", 18, 27, False, "medium", "regular", 150, "Блестящие резные листья на изящном деревце."),
    P("Бегония Рекс", "Begonia rex", "foliage", "medium", "high", 18, 26, True, "medium", "regular", 40, "Декоративная бегония с металлическим узором листа."),
    P("Ктенанта", "Ctenanthe", "foliage", "medium", "high", 18, 26, False, "hard", "frequent", 80, "Перистые листья с тёмно-зелёными мазками."),
    P("Пилея пеперомиевидная", "Pilea peperomioides", "foliage", "medium", "medium", 16, 26, False, "easy", "regular", 30, "«Денежное растение» с круглыми листьями-монетками."),
    P("Гипоэстес", "Hypoestes phyllostachya", "foliage", "bright", "high", 18, 26, False, "medium", "frequent", 30, "Листья в розовых и белых веснушках."),

    # --- Цветущие ---
    P("Спатифиллум", "Spathiphyllum wallisii", "flowering", "low", "high", 18, 28, True, "medium", "frequent", 60, "«Женское счастье» с белыми покрывалами соцветий."),
    P("Антуриум Андре", "Anthurium andraeanum", "flowering", "medium", "high", 18, 28, True, "medium", "regular", 60, "Глянцевые красные покрывала-«сердца»."),
    P("Сенполия (узамбарская фиалка)", "Saintpaulia", "flowering", "medium", "medium", 18, 25, False, "medium", "regular", 15, "Классическая фиалка с бархатистыми листьями."),
    P("Глоксиния", "Sinningia speciosa", "flowering", "bright", "medium", 18, 25, False, "medium", "regular", 25, "Крупные бархатистые колокольчики цветков."),
    P("Бегония вечноцветущая", "Begonia semperflorens", "flowering", "bright", "medium", 16, 26, True, "easy", "regular", 30, "Обильно и долго цветёт мелкими цветками."),
    P("Пеларгония (герань)", "Pelargonium", "flowering", "bright", "low", 12, 27, True, "easy", "regular", 50, "Неприхотливая герань с шапками соцветий."),
    P("Гибискус (китайская роза)", "Hibiscus rosa-sinensis", "flowering", "bright", "medium", 16, 28, False, "medium", "regular", 150, "Крупные эффектные цветки, любит свет."),
    P("Азалия", "Rhododendron simsii", "flowering", "bright", "high", 12, 20, True, "hard", "frequent", 60, "Пышное прохладолюбивое цветение зимой."),
    P("Цикламен персидский", "Cyclamen persicum", "flowering", "medium", "medium", 12, 18, True, "medium", "regular", 25, "Изящные цветки-«бабочки», любит прохладу."),
    P("Кливия", "Clivia miniata", "flowering", "medium", "low", 16, 24, True, "easy", "regular", 50, "Зонтики оранжевых цветков, очень вынослива."),
    P("Стрептокарпус", "Streptocarpus", "flowering", "medium", "medium", 16, 25, False, "medium", "regular", 30, "Длительное цветение нежными воронками."),
    P("Бальзамин (ванька мокрый)", "Impatiens walleriana", "flowering", "medium", "medium", 16, 26, False, "easy", "frequent", 40, "Сочные стебли и почти непрерывное цветение."),
    P("Абутилон (комнатный клён)", "Abutilon", "flowering", "bright", "medium", 15, 27, False, "medium", "regular", 150, "Кленовидные листья и колокольчатые цветки."),
    P("Гардения жасминовидная", "Gardenia jasminoides", "flowering", "bright", "high", 16, 24, True, "hard", "frequent", 80, "Белоснежные ароматные цветки, капризна."),
    P("Антуриум Шерцера", "Anthurium scherzerianum", "flowering", "medium", "high", 18, 26, True, "medium", "regular", 40, "Компактный антуриум с закрученным початком."),
    P("Жасмин самбак", "Jasminum sambac", "flowering", "bright", "medium", 16, 28, False, "medium", "regular", 150, "Ароматные белые цветки на вьющихся побегах."),
    P("Эписция", "Episcia", "flowering", "medium", "high", 18, 26, False, "medium", "frequent", 20, "Ампельное растение с бархатной листвой и цветками."),
    P("Колерия", "Kohleria", "flowering", "medium", "medium", 18, 26, False, "medium", "regular", 40, "Опушённые крапчатые цветки-колокольчики."),
    P("Брунфельсия", "Brunfelsia", "flowering", "bright", "medium", 16, 24, True, "hard", "regular", 100, "Цветки меняют цвет от фиолетового к белому."),

    # --- Лианы и ампельные ---
    P("Эпипремнум золотистый", "Epipremnum aureum", "vines", "medium", "medium", 17, 30, True, "easy", "regular", 200, "Быстрорастущая лиана с пёстрой листвой."),
    P("Сциндапсус", "Scindapsus pictus", "vines", "medium", "medium", 18, 28, True, "easy", "regular", 150, "Сердцевидные листья с серебристым узором."),
    P("Филодендрон лазящий", "Philodendron hederaceum", "vines", "medium", "medium", 18, 28, True, "easy", "regular", 200, "Неприхотливая лиана с сердцевидными листьями."),
    P("Сингониум", "Syngonium podophyllum", "vines", "medium", "high", 18, 27, True, "easy", "regular", 150, "Стреловидные листья, светлеющие к центру."),
    P("Плющ обыкновенный", "Hedera helix", "vines", "medium", "medium", 10, 24, True, "easy", "regular", 200, "Классический вьющийся плющ для опор и кашпо."),
    P("Хойя мясистая", "Hoya carnosa", "vines", "bright", "medium", 16, 28, False, "easy", "rare", 300, "Восковой плющ с ароматными звёздчатыми зонтиками."),
    P("Церопегия Вуда", "Ceropegia woodii", "vines", "bright", "low", 15, 26, False, "easy", "rare", 100, "«Цепочка сердечек» со свисающими тонкими нитями."),
    P("Традесканция зебрина", "Tradescantia zebrina", "vines", "bright", "medium", 15, 26, True, "easy", "regular", 60, "Полосатые серебристо-фиолетовые побеги."),
    P("Циссус ромболистный", "Cissus rhombifolia", "vines", "medium", "medium", 16, 26, False, "easy", "regular", 200, "«Берёзка» — выносливая лиана для дома и офиса."),
    P("Дисхидия", "Dischidia", "vines", "bright", "high", 18, 28, False, "medium", "regular", 100, "Эпифитная ампель с мелкими округлыми листьями."),
    P("Сенецио Роули", "Senecio rowleyanus", "vines", "bright", "low", 15, 26, True, "medium", "rare", 80, "«Жемчужная нить» из круглых листьев-горошин."),
    P("Стефанотис", "Stephanotis floribunda", "vines", "bright", "medium", 16, 26, False, "hard", "regular", 200, "Вьющийся «мадагаскарский жасмин» с ароматом."),
    P("Монстера деликатесная", "Monstera deliciosa", "vines", "medium", "medium", 18, 29, True, "medium", "regular", 250, "Крупная лиана с резными перфорированными листьями."),
    P("Филодендрон двоякоперистый", "Philodendron bipinnatifidum", "vines", "medium", "medium", 18, 28, True, "medium", "regular", 150, "Крупные глубоко рассечённые листья на мощном стебле."),

    # --- Комнатные деревья ---
    P("Фикус Бенджамина", "Ficus benjamina", "trees", "bright", "medium", 18, 28, True, "medium", "regular", 200, "Деревце с мелкими глянцевыми листьями."),
    P("Фикус каучуконосный", "Ficus elastica", "trees", "medium", "medium", 18, 28, True, "easy", "regular", 200, "Крупные кожистые листья, очень вынослив."),
    P("Фикус лировидный", "Ficus lyrata", "trees", "bright", "medium", 18, 27, True, "medium", "regular", 200, "Огромные листья в форме скрипки."),
    P("Шеффлера", "Schefflera arboricola", "trees", "medium", "medium", 16, 27, True, "easy", "regular", 200, "Пальчатые «зонтики» листьев на тонких стволах."),
    P("Фатсия японская", "Fatsia japonica", "trees", "medium", "medium", 10, 23, False, "easy", "regular", 150, "Крупные глянцевые резные листья, любит прохладу."),
    P("Полисциас", "Polyscias", "trees", "bright", "high", 18, 27, True, "hard", "regular", 150, "Ажурная крона, популярен для формирования бонсай."),
    P("Лавр благородный", "Laurus nobilis", "trees", "bright", "medium", 10, 26, False, "medium", "regular", 150, "Ароматные листья для кухни, легко стрижётся."),
    P("Гранат карликовый", "Punica granatum 'Nana'", "trees", "bright", "medium", 12, 28, False, "medium", "regular", 100, "Миниатюрный гранат, цветёт и плодоносит дома."),
    P("Кофейное дерево", "Coffea arabica", "trees", "bright", "high", 18, 26, True, "hard", "regular", 150, "Глянцевые листья и настоящие кофейные зёрна."),
    P("Фикус Микрокарпа (бонсай)", "Ficus microcarpa", "trees", "bright", "medium", 16, 28, True, "hard", "regular", 60, "Популярный фикус для выращивания в стиле бонсай."),
    P("Брахихитон", "Brachychiton rupestris", "trees", "bright", "low", 15, 28, False, "medium", "regular", 200, "«Бутылочное дерево» с утолщённым стволом."),

    # --- Цитрусовые ---
    P("Лимон Мейера", "Citrus × meyeri", "citrus", "bright", "medium", 14, 28, True, "medium", "regular", 150, "Компактный лимон, плодоносит в комнате."),
    P("Каламондин", "Citrus × microcarpa", "citrus", "bright", "medium", 14, 28, True, "medium", "regular", 100, "Декоративный цитрус с мелкими кислыми плодами."),
    P("Мандарин уншиу", "Citrus unshiu", "citrus", "bright", "medium", 14, 28, True, "hard", "regular", 150, "Бессемянный мандарин для домашнего сада."),
    P("Кумкват", "Citrus japonica", "citrus", "bright", "medium", 14, 28, True, "hard", "regular", 120, "Миниатюрные плоды, которые едят с кожурой."),
    P("Лайм", "Citrus aurantiifolia", "citrus", "bright", "medium", 15, 28, True, "hard", "regular", 150, "Ароматные зелёные плоды, требователен к свету."),

    # --- Пряные травы ---
    P("Базилик", "Ocimum basilicum", "herbs", "bright", "medium", 18, 28, False, "easy", "frequent", 40, "Ароматная зелень для салатов и соусов."),
    P("Мята перечная", "Mentha × piperita", "herbs", "medium", "medium", 14, 26, True, "easy", "frequent", 50, "Быстрорастущая мята с освежающим ароматом."),
    P("Розмарин", "Salvia rosmarinus", "herbs", "bright", "low", 12, 27, False, "medium", "regular", 80, "Хвоистый ароматный полукустарник."),
    P("Тимьян", "Thymus vulgaris", "herbs", "bright", "low", 12, 27, False, "easy", "regular", 30, "Низкая пряная трава, любит солнце и сухость."),
    P("Петрушка", "Petroselinum crispum", "herbs", "medium", "medium", 12, 24, True, "easy", "regular", 30, "Классическая зелень, растёт на прохладном окне."),
    P("Орегано", "Origanum vulgare", "herbs", "bright", "low", 14, 27, True, "easy", "regular", 50, "Пряная средиземноморская трава (душица)."),
    P("Шалфей лекарственный", "Salvia officinalis", "herbs", "bright", "low", 12, 27, False, "easy", "regular", 60, "Бархатистые серо-зелёные ароматные листья."),

    # --- Луковичные ---
    P("Гиппеаструм", "Hippeastrum", "bulbs", "bright", "medium", 16, 24, True, "medium", "regular", 60, "Огромные цветки-граммофоны на мощном цветоносе."),
    P("Зефирантес", "Zephyranthes", "bulbs", "bright", "medium", 16, 26, True, "easy", "regular", 30, "«Выскочка» — быстро зацветает после полива."),
    P("Эухарис (амазонская лилия)", "Eucharis grandiflora", "bulbs", "medium", "high", 18, 26, True, "medium", "regular", 50, "Белые ароматные цветки, похожие на нарциссы."),
    P("Гименокаллис", "Hymenocallis", "bulbs", "bright", "medium", 16, 26, True, "medium", "regular", 60, "Необычные «паучьи» белые цветки с ароматом."),
    P("Вельтгеймия", "Veltheimia", "bulbs", "bright", "low", 10, 22, True, "medium", "regular", 40, "Зимнецветущая луковичная с трубчатыми цветками."),
    P("Кринум", "Crinum", "bulbs", "bright", "medium", 16, 26, True, "medium", "regular", 90, "Крупная луковичная с эффектными цветками."),

    # --- Бромелиевые ---
    P("Гузмания", "Guzmania", "bromeliads", "medium", "high", 18, 27, False, "medium", "regular", 40, "Яркий прицветник-«звезда» держится месяцами."),
    P("Эхмея", "Aechmea fasciata", "bromeliads", "bright", "medium", 18, 27, False, "medium", "regular", 50, "Серебристые листья и розовое соцветие."),
    P("Вриезия", "Vriesea", "bromeliads", "medium", "high", 18, 26, False, "medium", "regular", 50, "Плоский «меч»-соцветие огненной окраски."),
    P("Тилландсия", "Tillandsia", "bromeliads", "bright", "high", 16, 28, False, "medium", "frequent", 25, "Атмосферное растение, живёт без почвы."),
    P("Криптантус", "Cryptanthus", "bromeliads", "medium", "high", 18, 26, False, "medium", "regular", 15, "Низкая «земляная звезда» с полосатой листвой."),
    P("Неорегелия", "Neoregelia", "bromeliads", "bright", "high", 18, 27, False, "medium", "regular", 40, "Розетка, краснеющая в центре перед цветением."),

    # --- Орхидеи ---
    P("Фаленопсис", "Phalaenopsis", "orchids", "medium", "high", 18, 28, False, "medium", "regular", 70, "Самая выносливая орхидея с долгим цветением."),
    P("Дендробиум", "Dendrobium", "orchids", "bright", "medium", 16, 28, False, "hard", "regular", 80, "Орхидея на псевдобульбах, любит перепад температур."),
    P("Камбрия", "Cambria", "orchids", "medium", "medium", 16, 25, False, "medium", "regular", 50, "Гибридная орхидея с звездчатыми пёстрыми цветками."),
    P("Цимбидиум", "Cymbidium", "orchids", "bright", "medium", 10, 25, False, "hard", "regular", 90, "Крупная орхидея, любит прохладные ночи."),
    P("Ванда", "Vanda", "orchids", "bright", "high", 18, 30, False, "hard", "frequent", 100, "Орхидея с открытыми корнями и яркими цветками."),
    P("Онцидиум", "Oncidium", "orchids", "medium", "medium", 16, 26, False, "medium", "regular", 60, "«Танцующие куколки» — россыпь жёлтых цветков."),

    # --- Хищные растения ---
    P("Венерина мухоловка", "Dionaea muscipula", "carnivorous", "bright", "high", 16, 28, False, "hard", "frequent", 15, "Ловит насекомых захлопывающимися «капканами»."),
    P("Непентес", "Nepenthes", "carnivorous", "medium", "high", 18, 28, False, "hard", "frequent", 60, "Лиана с висячими кувшинчиками-ловушками."),
    P("Росянка", "Drosera", "carnivorous", "bright", "high", 15, 27, False, "hard", "frequent", 20, "Листья в липких «росинках», ловящих добычу."),
    P("Саррацения", "Sarracenia", "carnivorous", "bright", "high", 15, 28, False, "hard", "frequent", 60, "Трубчатые ловчие листья-кувшины."),
]


def _assign_image_slugs():
    """Give every plant a stable Latin filename slug for its photo."""
    used = set()
    for plant in PLANTS:
        base = slugify(plant["scientific_name"]) or slugify(plant["name"]) or "plant"
        slug = base
        index = 2
        while slug in used:
            slug = f"{base}-{index}"
            index += 1
        used.add(slug)
        plant["image_slug"] = slug


_assign_image_slugs()
