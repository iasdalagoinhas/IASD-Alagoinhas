import base64
import copy
import html
import json
from calendar import monthrange
from datetime import date, datetime
from pathlib import Path

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="IASD Alagoinhas",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arquivos e Caminhos
DATA_FILE = Path("dados_iasd.json")
PRAYER_FILE = Path("pedidos_oracao.json")
STUDY_FILE = Path("estudos_biblicos.json")
INFO_FILE = Path("textos_inicio.json")
USERS_FILE = Path("usuarios_membros.json")
IASD_IMAGE = Path("iasd.jpg")
COLEGIO_IMAGE = Path("caal.jpg")

MEDITACAO_POR_DO_SOL = "https://www.youtube.com/watch?v=MIosdlW0bY4"
MEDITACAO_DATA = "4 de setembro de 2026"

CRENCAS_FUNDAMENTAIS = [
    ("1. As Escrituras Sagradas", "A Bíblia é a Palavra de Deus, revelação suficiente para fé e conduta."),
    ("2. A Trindade", "Há um só Deus: Pai, Filho e Espírito Santo, união de três Pessoas coeternas."),
    ("3. O Pai", "Deus o Pai é Criador, Sustentador e Soberano de toda a criação."),
    ("4. O Filho", "Jesus Cristo é verdadeiro Deus e verdadeiro homem, Salvador do mundo."),
    ("5. O Espírito Santo", "O Espírito Santo convence, regenera, guia e habita o crente."),
    ("6. A Criação", "Deus criou o mundo em seis dias e descansou no sétimo."),
    ("7. A Natureza do Homem", "O ser humano foi criado à imagem de Deus, livre e responsável."),
    ("8. O Grande Conflito", "Há um conflito entre Cristo e Satanás que envolve todo o universo."),
    ("9. Vida, morte e ressurreição de Cristo", "Cristo viveu, morreu e ressuscitou para nossa salvação."),
    ("10. A Experiência da Salvação", "Somos salvos pela graça, mediante a fé em Jesus."),
    ("11. O Crescimento em Cristo", "A vida cristã é crescimento contínuo em santidade e serviço."),
    ("12. A Igreja", "A igreja é a comunidade dos que confessam a Jesus como Senhor."),
    ("13. O Remanescente e sua missão", "Deus tem um povo com a missão de proclamar o evangelho eterno."),
    ("14. Unidade no corpo de Cristo", "Em Cristo, a igreja é um só corpo, chamada à comunhão."),
    ("15. O Batismo", "O batismo por imersão testemunha a morte e a nova vida em Cristo."),
    ("16. A Ceia do Senhor", "A Santa Ceia proclama a morte de Jesus até que Ele venha."),
    ("17. Dons e ministérios espirituais", "O Espírito concede dons para o serviço da igreja."),
    ("18. O Dom de Profecia", "O dom de profecia é uma marca do povo remanescente."),
    ("19. A Lei de Deus", "Os Dez Mandamentos expressam o caráter de Deus e a vontade divina."),
    ("20. O Sábado", "O sétimo dia é memorial da criação e sinal de aliança com Deus."),
    ("21. Mordomia", "Tudo pertence a Deus; administramos tempo, dons e recursos para Ele."),
    ("22. Conduta cristã", "A vida cristã honra a Deus no corpo, na mente e nos relacionamentos."),
    ("23. O Casamento e a família", "O casamento é união entre um homem e uma mulher, instituída por Deus."),
    ("24. O ministério de Cristo no Santuário", "Jesus ministra no Santuário celestial em favor de nós."),
    ("25. A Segunda Vinda de Cristo", "Jesus voltará de forma visível, pessoal e gloriosa."),
    ("26. Morte e ressurreição", "A morte é um sono; a esperança está na ressurreição em Cristo."),
    ("27. O Milênio e o fim do pecado", "Após a volta de Jesus, o pecado será eliminado para sempre."),
    ("28. A Nova Terra", "Deus fará novos céus e nova terra, lar eterno dos redimidos."),
]

MONTHS = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

WEEKDAYS = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]

COLEGIO = {
    "name": "Colégio Adventista de Alagoinhas",
    "presentation": (
        "O Colégio Adventista de Alagoinhas integra a Rede de Educação Adventista "
        "e oferece formação do Infantil ao Ensino Médio, incluindo proposta bilíngue. "
        "É um ambiente de aprendizado, valores cristãos e cuidado com cada etapa da jornada dos alunos."
    ),
    "address": "Av. Severino Vieira, 1077 — Centro, Alagoinhas/BA",
    "cep": "48005-460",
    "phone": "(75) 99126-0008",
    "whatsapp": "(75) 99126-0008",
    "whatsapp_link": "https://wa.me/5575991260008",
    "site": "https://alagoinhas.educacaoadventista.org.br/",
    "map_embed": "https://maps.google.com/maps?q=Av.+Severino+Vieira,+1077,+Alagoinhas+BA&t=&z=16&ie=UTF8&iwloc=&output=embed",
    "map_link": "https://maps.google.com/?q=Av.+Severino+Vieira,+1077,+Alagoinhas+BA",
    "levels": [
        "Educação Infantil",
        "Ensino Fundamental — anos iniciais",
        "Ensino Fundamental — anos finais",
        "Ensino Médio",
        "Ensino Bilíngue",
    ],
    "notices": [],
    "events": [],
}

DEFAULT_TEAMS = [
    {
        "name": "Equipe Distrital de Mordomia Cristã",
        "sigla": "EDMC",
        "schedule": [],
        "photos": []
    }
]

FALLBACK_DISTRICTS = {
    "Central de Alagoinhas": {
        "pastor": "Pr. Gesse Boaventura",
        "teams": copy.deepcopy(DEFAULT_TEAMS),
        "churches": [
            {"name": "Igreja Adventista Central de Alagoinhas", "type": "Igreja", "location": "Rua Benjamin Constant, S/N — Centro, Alagoinhas/BA", "responsible": "Pr. Gesse Boaventura", "central": True, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Santa Terezinha", "type": "Igreja", "location": "Alagoinhas/BA", "responsible": "Pr. Gesse Boaventura", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Tupy Caldas", "type": "Igreja", "location": "Alagoinhas/BA", "responsible": "Pr. Gesse Boaventura", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Rua do Catu", "type": "Igreja", "location": "Rua São Jerônimo, 173 — Catu, Alagoinhas/BA", "responsible": "Pr. Gesse Boaventura", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Buri", "type": "Grupo", "location": "Buri — Alagoinhas/BA", "responsible": "Pr. Gesse Boaventura", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Aramari", "type": "Grupo", "location": "Aramari/BA", "responsible": "Pr. Gesse Boaventura", "central": False, "schedule": {}, "ja": [], "special": []},
        ],
    },
    "Alagoinhas Velha": {
        "pastor": "Pr. Melquisedeque Oliveira",
        "teams": copy.deepcopy(DEFAULT_TEAMS),
        "churches": [
            {"name": "Igreja Adventista Central de Alagoinhas Velha", "type": "Igreja", "location": "Rua 8 de Dezembro — Alagoinhas Velha, Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": True, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Novo Horizonte", "type": "Igreja", "location": "Alagoinhas Velha — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Petrolar", "type": "Igreja", "location": "Alagoinhas Velha — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Igreja Adventista Airton Senna", "type": "Igreja", "location": "Alagoinhas Velha — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Km 18", "type": "Grupo", "location": "Km 18 — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Parque São Bernardo", "type": "Grupo", "location": "Parque São Bernardo — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Pedrão", "type": "Grupo", "location": "Pedrão/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Estêvão", "type": "Grupo", "location": "Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Alagoinhas IV", "type": "Grupo", "location": "Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Boa União", "type": "Grupo", "location": "Boa União — Alagoinhas/BA", "responsible": "Pr. Melquisedeque Oliveira", "central": False, "schedule": {}, "ja": [], "special": []},
        ],
    },
    "21 de Setembro": {
        "pastor": "Pr. Josimar Martins",
        "teams": copy.deepcopy(DEFAULT_TEAMS),
        "churches": [
            {"name": "Igreja Adventista 21 de Setembro", "type": "Igreja", "location": "21 de Setembro — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": True, "schedule": {}, "ja": [], "special": [], "leadership": {"anciao": "Elenildo", "secretario": "Secretário Beltrano", "tesoureiro": "Tesoureiro Sicrano", "outros": []}},
            {"name": "Mangalô 1", "type": "Grupo", "location": "Mangalô — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Mangalô 2", "type": "Grupo", "location": "Mangalô — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Manoel Vitorino", "type": "Grupo", "location": "Manoel Vitorino — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Nova Brasília", "type": "Grupo", "location": "Nova Brasília — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Teresópolis", "type": "Grupo", "location": "Teresópolis — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "2 de Julho", "type": "Grupo", "location": "2 de Julho — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "Rua Camaçari", "type": "Grupo", "location": "Rua Camaçari — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
            {"name": "15 de Novembro", "type": "Grupo", "location": "15 de Novembro — Alagoinhas/BA", "responsible": "Pr. Josimar Martins", "central": False, "schedule": {}, "ja": [], "special": []},
        ],
    },
}

DEFAULT_INFO = {
    "distritos": {"title": "O que é um distrito?", "text": "Distrito é um conjunto de igrejas e grupos próximos geograficamente. Cada distrito tem a liderança de um pastor. Em Alagoinhas existem três distritos pastorais."},
    "comunidades": {"title": "Igrejas e grupos", "text": "Igreja é a comunidade organizada, com programação regular. Grupo é a comunidade que cresce em comunhão até ser estabelecida como igreja."},
    "missao": {"title": "Missão", "text": "A missão da Igreja Adventista do Sétimo Dia é pregar o evangelho eterno a todas as pessoas, fazer discípulos e preparar um povo para o encontro com Jesus."},
    "esperanca": {"title": "Esperança", "text": "Nossa esperança é a volta de Cristo. Essa certeza dá sentido à fé, à comunhão e ao serviço."},
    "utilidade_publica": {
        "title": "Setembro Amarelo — Valorização da Vida",
        "text": "Falar é a melhor opção. Se você precisa de apoio emocional ou conhece alguém que esteja passando por momentos difíceis, busque ajuda! Ligue 188 (CVV - Centro de Valorização da Vida) ou procure nossa liderança para apoio e oração."
    }
}

DEFAULT_USERS = [
    {
        "nome": "Elenildo",
        "username": "elenildo",
        "password": "123",
        "whatsapp": "75999999999",
        "church": "Igreja Adventista 21 de Setembro",
        "approved": True
    }
]

CHURCH_ADDRESSES = {
    "Igreja Adventista Central de Alagoinhas": "Rua Benjamin Constant, S/N — Centro, Alagoinhas/BA",
    "Igreja Adventista Santa Terezinha": "Santa Terezinha, Alagoinhas/BA",
    "Igreja Adventista Tupy Caldas": "Rua Tupy Caldas — Santa Terezinha, Alagoinhas/BA",
    "Igreja Adventista Rua do Catu": "Rua São Jerônimo, 173 — Catu, Alagoinhas/BA",
    "Buri": "Buri, Alagoinhas/BA",
    "Aramari": "Aramari/BA",
    "Igreja Adventista Central de Alagoinhas Velha": "Rua 8 de Dezembro — Alagoinhas Velha, Alagoinhas/BA",
    "Igreja Adventista Novo Horizonte": "Novo Horizonte — Alagoinhas Velha, Alagoinhas/BA",
    "Igreja Adventista Petrolar": "Petrolar — Alagoinhas Velha, Alagoinhas/BA",
    "Igreja Adventista Airton Senna": "Avenida Ayrton Senna — Alagoinhas Velha, Alagoinhas/BA",
    "Km 18": "Km 18, Alagoinhas/BA",
    "Parque São Bernardo": "Parque São Bernardo, Alagoinhas/BA",
    "Pedrão": "Pedrão/BA",
    "Estêvão": "Estêvão — Alagoinhas/BA",
    "Alagoinhas IV": "Alagoinhas IV — Alagoinhas/BA",
    "Boa União": "Boa União, Alagoinhas/BA",
    "Igreja Adventista 21 de Setembro": "Bairro 21 de Setembro, Alagoinhas/BA",
    "Mangalô 1": "Mangalô, Alagoinhas/BA",
    "Mangalô 2": "Mangalô, Alagoinhas/BA",
    "Manoel Vitorino": "Manoel Vitorino, Alagoinhas/BA",
    "Nova Brasília": "Nova Brasília, Alagoinhas/BA",
    "Teresópolis": "Teresópolis, Alagoinhas/BA",
    "2 de Julho": "2 de Julho, Alagoinhas/BA",
    "Rua Camaçari": "Rua Camaçari, Alagoinhas/BA",
    "15 de Novembro": "15 de Novembro, Alagoinhas/BA",
}

# Funções Auxiliares
def safe(value):
    return html.escape(str(value or ""))

def file_data_uri(path):
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

def normalize_community(community, pastor):
    community.setdefault("type", "Igreja")
    community.setdefault("location", "Alagoinhas/BA")
    community.setdefault("responsible", pastor)
    community.setdefault("central", False)
    community.setdefault("schedule", {})
    community.setdefault("ja", [])
    community.setdefault("special", [])
    community.setdefault("notices", [])
    community.setdefault("leadership", {
        "anciao": "Elenildo" if "21 de Setembro" in community.get("name", "") else "Ancião Fulano",
        "secretario": "Secretário Beltrano",
        "tesoureiro": "Tesoureiro Sicrano",
        "outros": []
    })
    community.setdefault("comissoes", [])
    community.setdefault("tesouraria_relatorios", [])
    return community

def remove_duplicates(communities):
    clean = []
    seen = set()
    for community in communities:
        name = str(community.get("name", "")).strip().casefold()
        kind = str(community.get("type", "Igreja")).strip().casefold()
        key = (name, kind)
        if name and key not in seen:
            seen.add(key)
            clean.append(community)
    return clean

def merge_defaults_without_duplicates(saved_district, default_district):
    saved_district.setdefault("pastor", default_district["pastor"])
    saved_district.setdefault("churches", [])
    saved_district.setdefault("teams", copy.deepcopy(DEFAULT_TEAMS))
    pastor = saved_district["pastor"]
    for community in saved_district["churches"]:
        normalize_community(community, pastor)
    saved_district["churches"] = remove_duplicates(saved_district["churches"])
    existing_names = {
        str(community.get("name", "")).strip().casefold()
        for community in saved_district["churches"]
    }
    for community in default_district["churches"]:
        name = community["name"].strip().casefold()
        if name not in existing_names:
            saved_district["churches"].append(copy.deepcopy(community))
            existing_names.add(name)
    return saved_district

def normalize_saved_data(data):
    if not isinstance(data, dict):
        return copy.deepcopy(FALLBACK_DISTRICTS)
    if "Alagoinhas" in data and "Central de Alagoinhas" not in data:
        data["Central de Alagoinhas"] = data.pop("Alagoinhas")
    for district_name, default_district in FALLBACK_DISTRICTS.items():
        if district_name not in data:
            data[district_name] = copy.deepcopy(default_district)
        else:
            data[district_name] = merge_defaults_without_duplicates(
                data[district_name],
                default_district,
            )
    return data

def load_data():
    if DATA_FILE.exists():
        try:
            saved_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return normalize_saved_data(saved_data)
        except (OSError, json.JSONDecodeError):
            pass
    return copy.deepcopy(FALLBACK_DISTRICTS)

def save_data():
    DATA_FILE.write_text(
        json.dumps(st.session_state.districts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def load_users():
    if USERS_FILE.exists():
        try:
            users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
            if isinstance(users, list) and users:
                return users
        except (OSError, json.JSONDecodeError):
            pass
    return copy.deepcopy(DEFAULT_USERS)

def save_users(users):
    USERS_FILE.write_text(
        json.dumps(users, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def load_info():
    data = copy.deepcopy(DEFAULT_INFO)
    if INFO_FILE.exists():
        try:
            saved = json.loads(INFO_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                for key, value in saved.items():
                    if key in data and isinstance(value, dict):
                        data[key].update(value)
        except (OSError, json.JSONDecodeError):
            pass
    return data

def save_info():
    INFO_FILE.write_text(
        json.dumps(st.session_state.info_pages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def go(view, district=None, church_index=None, extra=None):
    st.session_state.view = view
    st.session_state.district = district
    st.session_state.church_index = church_index
    st.session_state.extra = extra
    params = {"view": view}
    if extra:
        params["extra"] = extra
    if district:
        params["district"] = district
    if church_index is not None:
        params["church"] = str(church_index)
    if view == "home":
        st.query_params.clear()
    else:
        st.query_params.from_dict(params)
    st.rerun()

def apply_query_params():
    params = st.query_params
    view = params.get("view")
    if not view:
        return
    st.session_state.view = view
    st.session_state.extra = params.get("extra")
    st.session_state.district = params.get("district")
    church = params.get("church")
    st.session_state.church_index = int(church) if church and str(church).isdigit() else st.session_state.get("church_index")

def current_church():
    district = st.session_state.districts.get(st.session_state.get("district"))
    index = st.session_state.get("church_index")
    if not district or index is None or index >= len(district["churches"]):
        return None
    return district["churches"][index]

def district_counts(district):
    communities = district.get("churches", [])
    church_total = sum(1 for item in communities if item.get("type", "Igreja") == "Igreja")
    group_total = sum(1 for item in communities if item.get("type") == "Grupo")
    return church_total, group_total

def district_description(district_name, district):
    church_total, group_total = district_counts(district)
    return (
        f"O distrito {district_name} é composto por {church_total} igreja(s) "
        f"e {group_total} grupo(s) e tem como líder principal o pastor "
        f"{district.get('pastor', 'A definir')}."
    )

def get_program(church, selected_date):
    key = selected_date.isoformat()
    custom = church.get("schedule", {}).get(key, {})
    programs = []
    if selected_date.weekday() == 6:
        programs.append(("Culto de adoração", "19h30", custom.get("preacher", "A definir"), "Pregador"))
    elif selected_date.weekday() == 2:
        programs.append(("Culto de oração", "19h30", custom.get("preacher", "A definir"), "Pregador"))
    elif selected_date.weekday() == 5:
        programs.append(("Escola Sabatina", "09h", custom.get("sabatina", "Departamento de Escola Sabatina"), "Responsável"))
        programs.append(("Culto Divino", "11h", custom.get("preacher", "A definir"), "Pregador"))
        for item in church.get("ja", []):
            if item.get("date") == key:
                programs.append(("Jovens Adventistas", item.get("time", "16h"), item.get("responsible", "Ministério Jovem"), "Responsável"))
    return programs

def append_json(path, item):
    data = []
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except (OSError, json.JSONDecodeError):
            data = []
    data.append(item)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def iter_communities():
    for district_name, district in st.session_state.districts.items():
        for church in district.get("churches", []):
            yield district_name, district, church

def today_preachers():
    rows = []
    today = date.today()
    for district_name, district, church in iter_communities():
        for label, schedule_time, person, role in get_program(church, today):
            if role == "Pregador":
                rows.append(
                    {
                        "district": district_name,
                        "church": church["name"],
                        "label": label,
                        "time": schedule_time,
                        "person": person,
                        "pastor": district.get("pastor", ""),
                    }
                )
    return rows

def today_pastors():
    rows = today_preachers()
    found = []
    seen = set()
    for district_name, district in st.session_state.districts.items():
        pastor = district.get("pastor", "")
        spot = next(
            (row for row in rows if row["person"] == pastor),
            None,
        )
        found.append(
            {
                "pastor": pastor,
                "district": district_name,
                "church": spot["church"] if spot else None,
                "time": spot["time"] if spot else None,
                "label": spot["label"] if spot else None,
            }
        )
        seen.add(pastor)
    return found

def today_ja():
    rows = []
    today = date.today()
    for district_name, district, church in iter_communities():
        for label, schedule_time, person, role in get_program(church, today):
            if label == "Jovens Adventistas":
                rows.append(
                    {
                        "district": district_name,
                        "church": church["name"],
                        "time": schedule_time,
                        "person": person,
                    }
                )
    return rows

def all_special_events():
    rows = []
    for district_name, district, church in iter_communities():
        for event in church.get("special", []):
            rows.append(
                {
                    "district": district_name,
                    "church": church["name"],
                    "title": event.get("title", "Evento especial"),
                    "date": event.get("date", ""),
                    "description": event.get("description", ""),
                }
            )
    return rows

def church_address(church):
    name = church.get("name", "")
    return CHURCH_ADDRESSES.get(name) or church.get("location") or f"{name}, Alagoinhas/BA"

def maps_url(church):
    query = church_address(church)
    return "https://www.google.com/maps/search/?api=1&query=" + html.escape(query, quote=True)

def church_display_name(name):
    raw = str(name or "").strip()
    prefix = "Igreja Adventista"
    if raw.casefold().startswith(prefix.casefold()):
        rest = raw[len(prefix):].strip(" -–")
        return prefix, rest or raw
    return raw, ""

def month_choices(today=None):
    today = today or date.today()
    end_year = today.year + 1
    options = []
    year, month = today.year, today.month
    while (year < end_year) or (year == end_year and month <= 1):
        options.append((year, month, f"{MONTHS[month - 1]}/{year}"))
        month += 1
        if month == 13:
            month = 1
            year += 1
    return options

def churches_for_preacher(name, month=None, year=None):
    name = (name or "").strip().casefold()
    if not name:
        return []
    today = date.today()
    month = month or today.month
    year = year or today.year
    rows = []
    for day_number in range(1, monthrange(year, month)[1] + 1):
        selected = date(year, month, day_number)
        for district_name, district, church in iter_communities():
            for label, schedule_time, person, role in get_program(church, selected):
                if role != "Pregador":
                    continue
                person_name = str(person or "").strip()
                if person_name.casefold() in {"a definir", ""}:
                    continue
                if name in person_name.casefold() or person_name.casefold() in name:
                    rows.append(
                        {
                            "date": selected,
                            "church": church["name"],
                            "district": district_name,
                            "label": label,
                            "time": schedule_time,
                            "person": person_name,
                        }
                    )
    return rows

IASD_URI = file_data_uri(IASD_IMAGE)
COLEGIO_URI = file_data_uri(COLEGIO_IMAGE)

# ESTILIZAÇÃO CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

    :root {
        --primary-dark: #0D1F2D;
        --accent-blue: #1A5F7A;
        --accent-gold: #C4923A;
        --bg-main: #F8FAFC;
        --card-bg: #FFFFFF;
        --border-color: #E2E8F0;
        --text-dark: #1A202C;
        --radius-lg: 20px;
        --radius-md: 14px;
    }

    .stApp {
        background-color: var(--bg-main);
        color: var(--text-dark);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 1140px;
        padding-top: 1rem;
        padding-bottom: 2.5rem;
    }

    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { display: none; }

    /* REMOVE ESPAÇOS VAZIOS */
    div[data-testid="stVerticalBlock"] > div:empty,
    div[data-testid="element-container"]:empty {
        display: none !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* PADRONIZAÇÃO DOS BOTÕES SUPERIORES */
    div[data-testid="stButton"] {
        margin-bottom: 8px !important;
    }

    div[data-testid="stButton"] > button, div[data-testid="stFormSubmitButton"] > button {
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        width: 100% !important;
        padding: 6px 12px !important;
        border: 2px solid var(--accent-blue) !important;
        border-radius: 999px !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #1A5F7A 0%, #0D1F2D 100%) !important;
        box-shadow: 0 4px 12px rgba(26, 95, 122, 0.25) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stButton"] > button p, div[data-testid="stFormSubmitButton"] > button p {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
        text-align: center !important;
        white-space: normal !important;
        word-break: break-word !important;
    }

    /* LOGO E BANNER SUPERIOR */
    .hero-banner-container {
        width: 100%;
        max-width: 760px;
        margin: 0 auto 14px;
        border-radius: var(--radius-lg);
        overflow: hidden;
        background-color: #000000;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    }

    .hero-banner-bg {
        width: 100%;
        height: auto;
        display: block;
        object-fit: contain;
    }

    .banner-standalone-button {
        width: 100%;
        max-width: 760px;
        margin: 12px auto 20px;
        padding: 14px 24px;
        background: linear-gradient(135deg, #1A5F7A 0%, #0D1F2D 100%);
        border: 2px solid var(--accent-blue);
        border-radius: 999px;
        box-shadow: 0 6px 16px rgba(26, 95, 122, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-sizing: border-box;
    }

    .banner-standalone-button .line-1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(1.35rem, 2.5vw, 1.65rem);
        font-weight: 800;
        color: #FFD166 !important;
        line-height: 1.2;
    }

    .banner-standalone-button .line-2 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(1.05rem, 2vw, 1.25rem);
        font-weight: 600;
        color: #FFFFFF !important;
        line-height: 1.3;
        white-space: nowrap;
    }

    /* BOTÃO ESPECIAL PISCANTE */
    @keyframes pulse-special {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 209, 102, 0.8);
            transform: scale(1);
        }
        50% {
            box-shadow: 0 0 0 15px rgba(255, 209, 102, 0);
            transform: scale(1.02);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 209, 102, 0);
            transform: scale(1);
        }
    }

    .special-pulsing-btn {
        width: 100%;
        max-width: 760px;
        margin: 12px auto 16px;
        padding: 14px 24px;
        background: linear-gradient(135deg, #C4923A 0%, #D4A34A 100%);
        border: 2px solid #FFD166;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        text-decoration: none;
        animation: pulse-special 2s infinite;
        box-sizing: border-box;
    }

    .special-pulsing-btn h3 {
        font-family: 'Playfair Display', Georgia, serif;
        margin: 0;
        font-size: clamp(1.15rem, 2.2vw, 1.45rem);
        color: #0D1F2D !important;
        font-weight: 800;
    }

    /* BOTÃO 28 CRENÇAS */
    .crencas-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 12px 0 8px;
    }

    .crencas-standalone-button {
        width: 100%;
        max-width: 760px;
        min-height: 52px;
        padding: 12px 24px;
        background: linear-gradient(135deg, #1A5F7A 0%, #0D1F2D 100%);
        border: 2px solid var(--accent-blue);
        border-radius: 999px;
        box-shadow: 0 6px 16px rgba(26, 95, 122, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        text-decoration: none;
        box-sizing: border-box;
    }

    .crencas-standalone-button h3 {
        font-family: 'Playfair Display', Georgia, serif;
        margin: 0;
        font-size: clamp(1.15rem, 2.2vw, 1.4rem);
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: center;
    }

    /* ESTRUTURA DOS CARDS DE DISTRITOS */
    .district-card-box {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        background: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        padding: 1.6rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 380px;
        height: 100%;
        box-sizing: border-box;
        margin-bottom: 1.2rem;
    }

    .district-title-area {
        min-height: 64px;
        display: flex;
        align-items: flex-start;
    }

    .district-card-box h3 {
        color: var(--primary-dark) !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.4rem !important;
        font-weight: 800;
        margin-top: 0.2rem;
        margin-bottom: 0.4rem;
        line-height: 1.25;
    }

    /* ESTRUTURA DOS CARDS DE IGREJAS */
    .church-card-box {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        background: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        padding: 1.6rem;
        border-top: 5px solid var(--accent-blue);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 290px;
        height: 100%;
        box-sizing: border-box;
        margin-bottom: 1.2rem;
    }

    .tag-container {
        min-height: 28px;
        margin-bottom: 6px;
    }

    .church-title-area {
        min-height: 96px;
        display: flex;
        align-items: flex-start;
    }

    .church-card-box h3 {
        color: var(--primary-dark) !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.35rem !important;
        font-weight: 800;
        margin-top: 0.2rem;
        margin-bottom: 0.4rem;
        line-height: 1.25;
    }

    .action-btn-link {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 48px !important;
        margin-top: 14px !important;
        border-radius: 999px !important;
        background: linear-gradient(135deg, #1A5F7A 0%, #0D1F2D 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(26, 95, 122, 0.25) !important;
        box-sizing: border-box !important;
    }

    /* QUADROS DE CONTEÚDO E FORMULÁRIOS */
    .card, .info, .agenda {
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        background: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        padding: 1.6rem;
        margin-bottom: 1rem;
    }

    .info h3 {
        color: var(--primary-dark) !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.5rem !important;
        font-weight: 800;
        margin-top: 0.2rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stForm"] label p {
        color: var(--primary-dark) !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }

    .tag {
        display: inline-block;
        border-radius: 999px;
        padding: 0.35rem 0.9rem;
        color: #0D1F2D;
        background: #FFD166;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .detail {
        border-radius: var(--radius-lg);
        padding: 2.2rem;
        color: white;
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--accent-blue) 100%);
        margin-bottom: 1.5rem;
    }

    .detail h1 {
        color: white !important;
        font-family: 'Playfair Display', Georgia, serif;
    }

    .detail p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.15rem !important;
    }

    .footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2.5rem;
        border-top: 1px solid var(--border-color);
        padding: 1.8rem 0;
        color: var(--text-dark);
        font-size: 1rem;
        font-weight: 600;
    }

    .hero {
        position: relative;
        min-height: 220px;
        overflow: hidden;
        border-radius: var(--radius-lg);
        padding: 2rem 2rem;
        color: white;
        background: var(--primary-dark);
        box-shadow: 0 10px 25px rgba(13, 31, 45, 0.2);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .hero-image {
        position: absolute;
        z-index: 0;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.35;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        color: #FFFFFF !important;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.2;
        margin: 0.5rem 0;
        font-weight: 800;
    }

    .hero-description {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.15rem;
        font-weight: 500;
    }

    .eyebrow {
        color: #FFD166;
        font-size: 0.9rem;
        font-weight: 800;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    .team-header-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--primary-dark);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .team-subtitle-label {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin: 1rem 0 0.6rem 0;
    }

    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Componentes de Layout
def render_header():
    logo_img = f'<img class="hero-banner-bg" src="{IASD_URI}" alt="Logotipo IASD">' if IASD_URI else ''
    
    st.markdown(
        f"""
        <div class="hero-banner-container">
            {logo_img}
        </div>
        """,
        unsafe_allow_html=True,
    )

    specials = all_special_events()
    if specials:
        primeiro_evento = specials[0]
        titulo_evento = primeiro_evento.get("title", "Atividade Especial")
        igreja_evento = primeiro_evento.get("church", "")
        
        st.markdown(
            f"""
            <a class="special-pulsing-btn" href="?view=hoje&extra=especial" target="_self">
                <h3>🔔 EVENTO ESPECIAL: {safe(titulo_evento)} — {safe(igreja_evento)}</h3>
            </a>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown(
        """
        <div class="crencas-button-container">
            <a class="crencas-standalone-button" href="?view=crencas" target="_self">
                <h3>Conheça as 28 Crenças Fundamentais</h3>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="banner-standalone-button">
            <div class="line-1">IASD Alagoinhas.</div>
            <div class="line-2">Sempre tem uma igreja perto de você!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # LINHA 1 (BOTÕES 1 A 4: NAVEGAÇÃO)
    nav_1, nav_2, nav_3, nav_4 = st.columns(4)
    with nav_1:
        if st.button("Início", key="nav_home", use_container_width=True):
            go("home")
    with nav_2:
        if st.button("Distritos", key="nav_districts", use_container_width=True):
            go("districts")
    with nav_3:
        if st.button("Educação", key="nav_education", use_container_width=True):
            go("education")
    with nav_4:
        label_membros = "Área para membros"
        if st.session_state.get("user_logged"):
            label_membros = f"👤 {st.session_state['user_logged']['nome'].split()[0]}"
        if st.button(label_membros, key="nav_members", use_container_width=True):
            go("membros")

def render_footer(second_text="“Servi ao Senhor com alegria.” — Salmo 100:2"):
    st.markdown(
        f"""
        <footer class="footer">
            <span>IASD Alagoinhas · Uma igreja conectada pela esperança.</span>
            <i>{safe(second_text)}</i>
        </footer>
        """,
        unsafe_allow_html=True,
    )

# Visualização: Home
def render_home():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Três Distritos", key="btn_stat_1", use_container_width=True):
            go("info", extra="distritos")
    with c2:
        if st.button("Vinte e seis igrejas", key="btn_stat_2", use_container_width=True):
            go("info", extra="comunidades")
    with c3:
        if st.button("Nossa Missão", key="btn_stat_3", use_container_width=True):
            go("info", extra="missao")
    with c4:
        if st.button("Nossa Esperança", key="btn_stat_4", use_container_width=True):
            go("info", extra="esperanca")

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("Veja quem prega hoje", key="btn_hoje_prega", use_container_width=True):
            go("hoje", extra="prega")
    with q2:
        if st.button("Onde o pastor está?", key="btn_hoje_pastor", use_container_width=True):
            go("hoje", extra="pastor")
    with q3:
        if st.button("Onde tem J.A.?", key="btn_hoje_ja", use_container_width=True):
            go("hoje", extra="ja")
    with q4:
        if st.button("Qual igreja prego este mês?", key="btn_hoje_mes", use_container_width=True):
            go("hoje", extra="mes")

    form_1, form_2 = st.columns(2)
    with form_1:
        with st.form("pedido_oracao"):
            st.markdown("### Pedido de Oração")
            nome_oracao = st.text_input("Seu nome")
            texto_oracao = st.text_input("Seu pedido")
            if st.form_submit_button("Enviar Pedido", use_container_width=True):
                if texto_oracao.strip():
                    append_json(PRAYER_FILE, {"quando": datetime.now().isoformat(timespec="minutes"), "nome": nome_oracao.strip() or "Anônimo", "pedido": texto_oracao.strip()})
                    st.success("Pedido de oração enviado com sucesso.")
                else:
                    st.error("Por favor, digite seu pedido.")

    with form_2:
        with st.form("estudo_biblico"):
            st.markdown("### Estudo Bíblico")
            nome_estudo = st.text_input("Seu nome", key="estudo_nome")
            contato_estudo = st.text_input("WhatsApp com DDD", key="estudo_contato")
            if st.form_submit_button("Solicitar Estudo", use_container_width=True):
                if nome_estudo.strip() and contato_estudo.strip():
                    append_json(STUDY_FILE, {"quando": datetime.now().isoformat(timespec="minutes"), "nome": nome_estudo.strip(), "contato": contato_estudo.strip()})
                    st.success("Solicitação recebida com sucesso!")
                else:
                    st.error("Preencha o nome e o WhatsApp.")

    st.markdown(
        f"""
        <a href="{MEDITACAO_POR_DO_SOL}" target="_blank" style="text-decoration:none">
            <section class="hero" style="min-height: 180px; background: linear-gradient(120deg, #0D1F2D 0%, #1A5F7A 50%, #C4923A 100%); margin-top:20px;">
                <div class="hero-content">
                    <div class="eyebrow">Sexta-feira · {MEDITACAO_DATA}</div>
                    <h1>Meditação do Pôr do Sol</h1>
                    <p class="hero-description">Assista no canal oficial do YouTube ↗</p>
                </div>
            </section>
        </a>
        """,
        unsafe_allow_html=True,
    )

    utilidade = st.session_state.info_pages.get("utilidade_publica", DEFAULT_INFO["utilidade_publica"])
    st.markdown(
        f"""
        <div class="info" style="border-left: 6px solid #FFD166; background: #FFFDF9; margin-top: 16px;">
            <span class="tag">Utilidade Pública & Saúde</span>
            <h3 style="margin-top:10px;">{safe(utilidade.get('title', ''))}</h3>
            <p style="font-size:1.15rem; line-height:1.6;">{safe(utilidade.get('text', ''))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("⚙️ Editar mensagem de Utilidade Pública", key="edit_utilidade_toggle"):
        st.session_state.show_edit_utilidade = not st.session_state.get("show_edit_utilidade", False)

    if st.session_state.get("show_edit_utilidade", False):
        with st.form("form_edit_utilidade"):
            u_title = st.text_input("Título do Aviso", utilidade.get("title", ""))
            u_text = st.text_area("Mensagem de Utilidade Pública", utilidade.get("text", ""), height=150)
            if st.form_submit_button("Salvar Mensagem"):
                st.session_state.info_pages["utilidade_publica"] = {
                    "title": u_title.strip(),
                    "text": u_text.strip()
                }
                save_info()
                st.session_state.show_edit_utilidade = False
                st.success("Mensagem de utilidade pública atualizada!")
                st.rerun()

    render_footer()

# Visualização: ÁREA EXCLUSIVA PARA MEMBROS
def render_membros_page():
    users = load_users()
    logged_user = st.session_state.get("user_logged")

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao início", key="back_membros_home", use_container_width=True):
            go("home")

    # SE NÃO ESTIVER LOGADO -> LOGIN
    if not logged_user:
        st.markdown(
            """
            <section class="detail" style="text-align:center;">
                <div class="eyebrow">ÁREA RESTRITA</div>
                <h1>Acesso Exclusivo para Membros</h1>
                <p>Faça login com seu usuário e senha aprovados pela liderança.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        col_login_box, _ = st.columns([2, 1])
        with col_login_box:
            with st.form("form_login_membro"):
                st.markdown("### Entrar na Área do Membro")
                user_input = st.text_input("Usuário", value="elenildo")
                pass_input = st.text_input("Senha", type="password", value="123")
                
                if st.form_submit_button("Acessar Painel", use_container_width=True):
                    found = next((u for u in users if u["username"].strip().casefold() == user_input.strip().casefold() and u["password"] == pass_input), None)
                    if not found:
                        st.error("Usuário ou senha incorretos.")
                    elif not found.get("approved", False):
                        st.warning("Seu cadastro ainda está pendente de aprovação pela liderança da igreja (Pastor, Ancião, Secretário ou Tesoureiro).")
                    else:
                        st.session_state["user_logged"] = found
                        st.success(f"Bem-vindo(a), {found['nome']}!")
                        st.rerun()

        st.info("💡 Ainda não possui cadastro? Acesse a página da sua igreja no menu 'Distritos' e clique no botão 'Cadastro de Membros'.")
        render_footer()
        return

    # PAINEL DO MEMBRO
    user_church_name = logged_user.get("church")
    
    church_obj = None
    district_obj_name = None
    for d_name, d_data, c_data in iter_communities():
        if c_data["name"].strip().casefold() == user_church_name.strip().casefold():
            church_obj = c_data
            district_obj_name = d_name
            break

    if not church_obj:
        st.error("Igreja do membro não encontrada nos registros.")
        if st.button("Sair"):
            st.session_state["user_logged"] = None
            st.rerun()
        return

    church_obj.setdefault("leadership", {
        "anciao": "Elenildo",
        "secretario": "Secretário Beltrano",
        "tesoureiro": "Tesoureiro Sicrano",
        "outros": []
    })
    church_obj.setdefault("comissoes", [])
    church_obj.setdefault("tesouraria_relatorios", [])

    st.markdown(
        f"""
        <section class="detail">
            <div class="eyebrow">PAINEL DO MEMBRO · {safe(church_obj['name'])}</div>
            <h1>Olá, {safe(logged_user['nome'])}!</h1>
            <p>Seja bem-vindo à Área Restrita de Membros e Liderança.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔴 Sair da Conta", key="btn_logout"):
        st.session_state["user_logged"] = None
        st.rerun()

    tab_lider, tab_comissao, tab_tesouraria, tab_aprovacao = st.tabs([
        "👥 Liderança da Igreja",
        "📅 Reunião de Comissão",
        "📊 Relatório da Tesouraria",
        "✅ Aprovação de Membros"
    ])

    # 1. LIDERANÇA DA IGREJA
    with tab_lider:
        st.markdown("### Liderança Oficial da Igreja")
        st.write("Cargos principais e equipe de apoio administrativa da igreja local:")

        ld = church_obj["leadership"]
        pastor_nome = church_obj.get("responsible", "Pr. Josimar Martins")

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.text_input("Pastor Distrital", value=pastor_nome, disabled=True, key="pastor_read")
            anciao_val = st.text_input("Ancião", value=ld.get("anciao", "Elenildo"), key="in_anciao")
            secretario_val = st.text_input("Secretário", value=ld.get("secretario", "Secretário Beltrano"), key="in_sec")
            tesoureiro_val = st.text_input("Tesoureiro", value=ld.get("tesoureiro", "Tesoureiro Sicrano"), key="in_tes")

            if st.button("Salvar Nomes da Liderança", key="save_lead_names"):
                ld["anciao"] = anciao_val.strip()
                ld["secretario"] = secretario_val.strip()
                ld["tesoureiro"] = tesoureiro_val.strip()
                save_data()
                st.success("Liderança atualizada!")
                st.rerun()

        with col_l2:
            st.markdown("#### Outros Líderes e Departamentos")
            if ld.get("outros"):
                for o_idx, item_o in enumerate(ld["outros"]):
                    st.markdown(f"• **{safe(item_o['cargo'])}:** {safe(item_o['nome'])}")
            else:
                st.info("Nenhum outro líder adicionado.")

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("＋ Adicionar Mais Líderes"):
                with st.form("form_add_other_leader"):
                    novo_cargo = st.text_input("Cargo / Departamento (ex: Diretor de Jovens, Escola Sabatina)")
                    novo_nome_lider = st.text_input("Nome do Líder")
                    if st.form_submit_button("Adicionar à Liderança"):
                        if novo_cargo.strip() and novo_nome_lider.strip():
                            ld.setdefault("outros", []).append({
                                "cargo": novo_cargo.strip(),
                                "nome": novo_nome_lider.strip()
                            })
                            save_data()
                            st.success("Novo líder adicionado!")
                            st.rerun()

    # 2. REUNIÃO DE COMISSÃO
    with tab_comissao:
        st.markdown("### Agendamento e Relatórios de Comissão")
        
        st.markdown("#### Próximas Reuniões Marcadas")
        if church_obj["comissoes"]:
            for com in church_obj["comissoes"]:
                st.markdown(
                    f"""
                    <div class="agenda">
                        <span class="tag">Comissão em {safe(com.get('data', ''))}</span>
                        <h4 style="margin:6px 0;">Pauta / Assunto: {safe(com.get('pauta', ''))}</h4>
                        <p style="margin:0;"><b>Relatório / Ata da Última Comissão:</b> {safe(com.get('relatorio', 'Aguardando ata.'))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma reunião de comissão agendada no momento.")

        with st.expander("＋ Agendar Nova Comissão / Publicar Ata"):
            with st.form("form_nova_comissao"):
                dt_com = st.text_input("Data da Reunião (ex: 25/09/2026 - 19h30)")
                pauta_com = st.text_input("Pauta Principal")
                relatorio_com = st.text_area("Relatório / Votos da Comissão (Ata)")
                if st.form_submit_button("Salvar Registro de Comissão"):
                    if dt_com.strip():
                        church_obj.setdefault("comissoes", []).append({
                            "data": dt_com.strip(),
                            "pauta": pauta_com.strip(),
                            "relatorio": relatorio_com.strip()
                        })
                        save_data()
                        st.success("Reunião de comissão salva com sucesso!")
                        st.rerun()

    # 3. RELATÓRIO DA TESOURARIA
    with tab_tesouraria:
        st.markdown("### Resumo Mensal da Tesouraria")
        
        if church_obj["tesouraria_relatorios"]:
            for rel in church_obj["tesouraria_relatorios"]:
                st.markdown(
                    f"""
                    <div class="agenda" style="border-left:5px solid #1A5F7A;">
                        <span class="tag">{safe(rel.get('mes', 'Mês'))}</span>
                        <h4 style="margin:6px 0;">{safe(rel.get('titulo', 'Relatório Financeiro'))}</h4>
                        <p style="font-size:1.1rem; line-height:1.6;">{safe(rel.get('detalhes', ''))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhum relatório de tesouraria publicado até o momento.")

        with st.expander("＋ Publicar Resumo da Tesouraria (Exclusivo Tesoureiro/Pastor)"):
            with st.form("form_novo_rel_tesouraria"):
                mes_tes = st.text_input("Mês / Referência (ex: Agosto/2026)")
                tit_tes = st.text_input("Título do Relatório", "Balanço Mensal da Tesouraria")
                det_tes = st.text_area("Resumo das Atividades Financeiras / Entradas e Saídas")
                if st.form_submit_button("Publicar Relatório"):
                    if mes_tes.strip() and det_tes.strip():
                        church_obj.setdefault("tesouraria_relatorios", []).append({
                            "mes": mes_tes.strip(),
                            "titulo": tit_tes.strip(),
                            "detalhes": det_tes.strip()
                        })
                        save_data()
                        st.success("Relatório da tesouraria publicado!")
                        st.rerun()

    # 4. APROVAÇÃO DE MEMBROS
    with tab_aprovacao:
        st.markdown("### Gerenciamento e Aprovação de Cadastros")
        st.write("Aprovações pendentes para novos membros desta igreja:")

        pendentes = [u for u in users if u.get("church", "").strip().casefold() == church_obj["name"].strip().casefold() and not u.get("approved", False)]
        aprovados = [u for u in users if u.get("church", "").strip().casefold() == church_obj["name"].strip().casefold() and u.get("approved", False)]

        if pendentes:
            for p_idx, p_user in enumerate(pendentes):
                c_p1, c_p2 = st.columns([3, 1])
                with c_p1:
                    st.markdown(f"👤 **{safe(p_user['nome'])}** (@{safe(p_user['username'])}) · Whats: {safe(p_user.get('whatsapp',''))}")
                with c_p2:
                    if st.button("Aprovar Membro", key=f"btn_aprov_{p_idx}"):
                        p_user["approved"] = True
                        save_users(users)
                        st.success(f"{p_user['nome']} foi aprovado(a)!")
                        st.rerun()
        else:
            st.info("Não há solicitações de membros pendentes para aprovação.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Membros Aprovados")
        if aprovados:
            for a_user in aprovados:
                st.write(f"✓ **{safe(a_user['nome'])}** (@{safe(a_user['username'])})")
        else:
            st.write("Nenhum membro cadastrado e aprovado ainda.")

    render_footer()

# Visualização: Distritos
def render_districts_page():
    st.markdown(
        """
        <section class="detail">
            <div class="eyebrow">DISTRITOS PASTORAIS</div>
            <h1>Uma cidade conectada pela fé.</h1>
            <p>Conheça a estrutura dos distritos da IASD em Alagoinhas e região.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin: 2rem 0 1rem;">
            <h2>Distritos de Alagoinhas</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Cada distrito reúne comunidades de fé, serviço, esperança e missão.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    district_columns = st.columns(3)
    for index, (district_name, district) in enumerate(st.session_state.districts.items()):
        description = district_description(district_name, district)
        churches, groups = district_counts(district)
        link_url = f"?view=district&district={html.escape(district_name, quote=True)}"

        with district_columns[index % 3]:
            card_html = (
                f'<div class="district-card-box">'
                f'<div>'
                f'<div class="tag-container"><span class="tag">Distrito {index + 1:02d}</span></div>'
                f'<div class="district-title-area"><h3>{safe(district_name)}</h3></div>'
                f'<p style="font-size:1.05rem; line-height:1.6; color:var(--text-dark);">{safe(description)}</p>'
                f'</div>'
                f'<div>'
                f'<hr style="border:0; border-top:1px solid var(--border-color); margin: 12px 0;">'
                f'<small style="color:var(--text-dark); font-weight:700; font-size:1.05rem;">{churches} igreja(s) · {groups} grupo(s)</small>'
                f'<a class="action-btn-link" href="{link_url}" target="_self">Abrir Distrito ↗</a>'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

    render_footer("Distritos da IASD Alagoinhas.")

# Visualização: Distrito Individual
def render_district():
    district_name = st.session_state.get("district")
    district = st.session_state.districts.get(district_name)
    if not district:
        go("districts")
        return

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar aos distritos", key="back_district_top", use_container_width=True):
            go("districts")

    church_total, group_total = district_counts(district)
    st.markdown(
        f"""
        <section class="detail">
            <div class="eyebrow">DISTRITO PASTORAL</div>
            <h1>{safe(district_name)}</h1>
            <p>{safe(district_description(district_name, district))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="margin: 1.5rem 0;">
            <h2>Visão Geral</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Pastor responsável: <b>{safe(district['pastor'])}</b><br>{church_total} igreja(s) e {group_total} grupo(s) cadastrados.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin: 1.5rem 0;">
            <h2>Igrejas e Grupos</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Comunidades cadastradas sob a liderança deste distrito.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋ Adicionar igreja ou grupo", key="add_church"):
        st.session_state.show_add = True

    if st.session_state.get("show_add", False):
        with st.expander("Cadastrar nova comunidade", expanded=True):
            with st.form("new_church", clear_on_submit=True):
                column_1, column_2 = st.columns(2)
                with column_1:
                    new_name = st.text_input("Nome")
                    new_type = st.selectbox("Tipo", ["Igreja", "Grupo"])
                with column_2:
                    new_location = st.text_input("Localização/Endereço", "Alagoinhas/BA")
                    new_responsible = st.text_input("Responsável", district["pastor"])
                save = st.form_submit_button("Salvar Registro")
                if save:
                    if not new_name.strip():
                        st.error("O nome é obrigatório.")
                    else:
                        district["churches"].append(
                            {
                                "name": new_name.strip(),
                                "type": new_type,
                                "location": new_location.strip() or "Alagoinhas/BA",
                                "responsible": new_responsible.strip() or "A definir",
                                "central": False,
                                "schedule": {},
                                "ja": [],
                                "special": [],
                            }
                        )
                        save_data()
                        st.session_state.show_add = False
                        st.rerun()

    churches = district["churches"]
    for i in range(0, len(churches), 2):
        pair = churches[i:i + 2]
        cols = st.columns(2)
        for idx, church in enumerate(pair):
            actual_index = i + idx
            with cols[idx]:
                if church.get("central"):
                    tag_label = "Igreja Central"
                else:
                    tag_label = church.get("type") or "Igreja"
                
                link_url = f"?view=church&district={html.escape(district_name, quote=True)}&church={actual_index}"
                
                card_html = (
                    f'<div class="church-card-box">'
                    f'<div>'
                    f'<div class="tag-container"><span class="tag">{safe(tag_label)}</span></div>'
                    f'<div class="church-title-area"><h3>{safe(church["name"])}</h3></div>'
                    f'<p style="font-size:1.05rem; color:var(--text-dark); margin-bottom:12px;">{safe(church.get("location", "Alagoinhas/BA"))}</p>'
                    f'</div>'
                    f'<div>'
                    f'<hr style="border:0; border-top:1px solid var(--border-color); margin: 8px 0 12px 0;">'
                    f'<small style="color:var(--text-dark); font-weight:700; font-size:1.05rem;">Líder: {safe(church.get("responsible", "A definir"))}</small>'
                    f'<a class="action-btn-link" href="{link_url}" target="_self">Ver Detalhes →</a>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

    # SEÇÃO: EQUIPES DISTRITAIS
    st.markdown("<hr style='border:0; border-top:2px solid var(--border-color); margin:2.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2>Equipes Distritais</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Ministérios e equipes de apoio ao distrito.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    district.setdefault("teams", copy.deepcopy(DEFAULT_TEAMS))

    for team_idx, team in enumerate(district["teams"]):
        sigla = team.get("sigla", "")
        sigla_badge = f" ({safe(sigla)})" if sigla else ""
        team_title = f"{safe(team['name'])}{sigla_badge}"

        st.markdown(
            f"""
            <div class="team-header-title">
                📌 {team_title}
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_agenda, tab_fotos = st.tabs(["📅 Agenda de Atuação", "📸 Fotos da Atuação"])
        
        with tab_agenda:
            st.markdown("<div class='team-subtitle-label'>Agenda de Atuação nas Igrejas</div>", unsafe_allow_html=True)
            if team.get("schedule"):
                for item in team["schedule"]:
                    st.markdown(
                        f"""
                        <div class="agenda" style="margin-bottom:10px; padding:1rem;">
                            <span class="tag">{safe(item.get('date', 'Data a definir'))}</span>
                            <h4 style="margin:8px 0 4px 0; color:var(--primary-dark); font-family:'Playfair Display', Georgia, serif;">{safe(item.get('church', 'Igreja'))}</h4>
                            <p style="margin:0; font-size:1.05rem;">{safe(item.get('activity', 'Atividade programada'))}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("Aguardando agenda")

            with st.form(f"form_agenda_team_{team_idx}"):
                st.markdown("#### Adicionar nova atuação na agenda")
                col_dt, col_ig = st.columns(2)
                with col_dt:
                    nova_data = st.date_input("Data da Atuação", key=f"dt_team_{team_idx}")
                with col_ig:
                    ch_names = [c["name"] for c in district["churches"]]
                    nova_igreja = st.selectbox("Igreja", ch_names if ch_names else ["Igreja Central"], key=f"ig_team_{team_idx}")
                nova_ativ = st.text_input("Atividade / Programação", key=f"ativ_team_{team_idx}")
                
                if st.form_submit_button("Agendar Atuação"):
                    if nova_ativ.strip():
                        team.setdefault("schedule", []).append({
                            "date": nova_data.strftime("%d/%m/%Y"),
                            "church": nova_igreja,
                            "activity": nova_ativ.strip()
                        })
                        save_data()
                        st.success("Atuação agendada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Informe a atividade.")

        with tab_fotos:
            st.markdown("<div class='team-subtitle-label'>Registros Visuais da Atuação</div>", unsafe_allow_html=True)
            team.setdefault("photos", [])
            
            if team["photos"]:
                grid_cols = st.columns(3)
                for photo_i, photo_data in enumerate(team["photos"]):
                    with grid_cols[photo_i % 3]:
                        st.image(photo_data["uri"], caption=f"{photo_data.get('church', '')} ({photo_data.get('date', '')})", use_container_width=True)
            else:
                st.info("Nenhuma foto cadastrada para esta equipe até o momento.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Inserir Foto de Atuação")
            uploaded_photo = st.file_uploader(
                f"Selecione uma imagem para a equipe {team.get('sigla', '')}",
                type=["jpg", "jpeg", "png"],
                key=f"uploader_team_{team_idx}"
            )
            if uploaded_photo is not None:
                col_p_ig, col_p_desc = st.columns(2)
                with col_p_ig:
                    foto_igreja = st.selectbox("Igreja da Foto", [c["name"] for c in district["churches"]], key=f"foto_ig_{team_idx}")
                with col_p_desc:
                    foto_data_str = st.text_input("Data / Legenda", date.today().strftime("%d/%m/%Y"), key=f"foto_leg_{team_idx}")

                if st.button("Salvar Foto na Galeria", key=f"btn_save_photo_{team_idx}"):
                    bytes_data = uploaded_photo.getvalue()
                    mime = uploaded_photo.type
                    encoded = base64.b64encode(bytes_data).decode("ascii")
                    data_uri = f"data:{mime};base64,{encoded}"
                    
                    team["photos"].append({
                        "uri": data_uri,
                        "church": foto_igreja,
                        "date": foto_data_str
                    })
                    save_data()
                    st.success("Foto adicionada com sucesso!")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("＋ Adicionar outra equipe distrital", key="btn_add_team", use_container_width=True):
        st.session_state.show_add_team = True

    if st.session_state.get("show_add_team", False):
        with st.expander("Cadastrar Nova Equipe Distrital", expanded=True):
            with st.form("form_nova_equipe", clear_on_submit=True):
                col_t1, col_t2 = st.columns([3, 1])
                with col_t1:
                    nom_equipe = st.text_input("Nome da Equipe (ex: Equipe Distrital de Jovens)")
                with col_t2:
                    sig_equipe = st.text_input("Sigla (ex: EDJ)")
                
                if st.form_submit_button("Salvar Equipe"):
                    if nom_equipe.strip():
                        district["teams"].append({
                            "name": nom_equipe.strip(),
                            "sigla": sig_equipe.strip().upper(),
                            "schedule": [],
                            "photos": []
                        })
                        save_data()
                        st.session_state.show_add_team = False
                        st.success("Equipe cadastrada com sucesso!")
                        st.rerun()
                    else:
                        st.error("O nome da equipe é obrigatório.")

    render_footer()

# Visualização: Perfil da Igreja
def render_church():
    church = current_church()
    if not church:
        go("districts")
        return

    church.setdefault("notices", [])
    church.setdefault("special", [])
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao distrito", key="back_church", use_container_width=True):
            go("district", st.session_state.district)

    line1, line2 = church_display_name(church["name"])
    second = f'<br><small style="font-size:1.3rem; color:var(--accent-gold);">{safe(line2)}</small>' if line2 else ""
    address = church_address(church)
    maps = maps_url(church)

    st.markdown(
        f"""
        <section class="detail" style="text-align:center;">
            <h1>{safe(line1)}{second}</h1>
            <p>Perfil da Comunidade</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="info">
                <span class="tag">Distrito Pastoral</span>
                <h3>{safe(st.session_state.district)}</h3>
                <p style="font-size:1.15rem;"><b>Responsável:</b> {safe(church.get("responsible", "A definir"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="info">
                <span class="tag">Localização</span>
                <h3>{safe(address)}</h3>
                <p style="font-size:1.15rem;"><a href="{maps}" target="_blank" style="color:var(--accent-blue); font-weight:700;">Abrir no Google Maps ↗</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # BOTÃO DE CADASTRO DE MEMBROS DA IGREJA
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 Cadastro de Membros", key="btn_cad_membro", use_container_width=True):
        st.session_state.show_cad_membro = not st.session_state.get("show_cad_membro", False)

    if st.session_state.get("show_cad_membro", False):
        with st.expander(f"Solicitar Cadastro de Membro — {church['name']}", expanded=True):
            with st.form("form_novo_membro", clear_on_submit=True):
                m_nome = st.text_input("Nome Completo")
                m_user = st.text_input("Escolha um Nome de Usuário")
                m_pass = st.text_input("Escolha uma Senha", type="password")
                m_whats = st.text_input("WhatsApp com DDD")
                
                st.caption("Nota: Seu cadastro passará pela aprovação do Pastor, Ancião, Secretário ou Tesoureiro antes de liberar seu acesso.")
                
                if st.form_submit_button("Enviar Solicitação de Cadastro"):
                    if m_nome.strip() and m_user.strip() and m_pass.strip():
                        users = load_users()
                        if any(u["username"].strip().casefold() == m_user.strip().casefold() for u in users):
                            st.error("Este nome de usuário já está em uso. Escolha outro.")
                        else:
                            users.append({
                                "nome": m_nome.strip(),
                                "username": m_user.strip(),
                                "password": m_pass,
                                "whatsapp": m_whats.strip(),
                                "church": church["name"],
                                "approved": False
                            })
                            save_users(users)
                            st.success("Cadastro enviado com sucesso! Aguarde a aprovação da liderança.")
                            st.session_state.show_cad_membro = False
                            st.rerun()
                    else:
                        st.error("Preencha nome, usuário e senha.")

    st.markdown("<h2 style='text-align:center; margin-top:2rem;'>Programação Mensal</h2>", unsafe_allow_html=True)

    choices = month_choices()
    labels = [item[2] for item in choices]
    selected_label = st.selectbox("Selecione o mês para visualizar a agenda:", labels, index=0)
    year, month = next((item[0], item[1]) for item in choices if item[2] == selected_label)

    found = False
    for day_number in range(1, monthrange(year, month)[1] + 1):
        selected = date(year, month, day_number)
        programs = get_program(church, selected)
        if programs:
            found = True
            content = f"<div class='agenda'><span class='tag'>{day_number} de {MONTHS[month - 1]} · {WEEKDAYS[selected.weekday()]}</span>"
            for label, schedule_time, person, role in programs:
                content += f"<p style='margin-top:8px; font-size:1.15rem;'><b>{safe(label)} ({safe(schedule_time)}):</b> {safe(role)}: {safe(person)}</p>"
            st.markdown(content + "</div>", unsafe_allow_html=True)

    if not found:
        st.info("Nenhuma programação cadastrada para este mês.")

    st.markdown("<h2 style='margin-top:2rem;'>Eventos & Programações Especiais</h2>", unsafe_allow_html=True)
    if church.get("special"):
        for sp in church["special"]:
            st.markdown(
                f"""
                <div class="agenda" style="border-left: 5px solid var(--accent-gold);">
                    <span class="tag">Especial</span>
                    <h3 style="font-size:1.3rem; margin:6px 0;">{safe(sp.get('title', ''))}</h3>
                    <p style="margin:0; font-size:1.1rem;"><b>Data:</b> {safe(sp.get('date', ''))}</p>
                    <p style="margin:0; font-size:1.05rem; color:#555;">{safe(sp.get('description', ''))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Nenhum evento especial agendado nesta igreja.")

    with st.expander("＋ Cadastrar Evento Especial (Ativa Botão na Inicial)"):
        with st.form("form_special_event", clear_on_submit=True):
            sp_title = st.text_input("Título do Evento (ex: Santa Ceia, Semana de Oração)")
            sp_date = st.text_input("Data do Evento (ex: 20 de Setembro)")
            sp_desc = st.text_area("Descrição / Detalhes")
            if st.form_submit_button("Publicar Evento Especial"):
                if sp_title.strip() and sp_date.strip():
                    church.setdefault("special", []).append({
                        "title": sp_title.strip(),
                        "date": sp_date.strip(),
                        "description": sp_desc.strip()
                    })
                    save_data()
                    st.success("Evento especial cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Informe pelo menos o título e a data.")

    st.markdown("<h2 style='margin-top:2rem;'>Avisos & Departamentos</h2>", unsafe_allow_html=True)
    if church.get("notices"):
        for item in church["notices"]:
            st.markdown(
                f"""
                <div class="agenda">
                    <span class="tag">{safe(item.get("department", "Departamento"))}</span>
                    <p style="margin-top:8px; font-size:1.15rem;">{safe(item.get("text", ""))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Sem avisos de departamentos registrados no momento.")

    with st.expander("＋ Publicar aviso de departamento"):
        with st.form("aviso_departamento"):
            dep_name = st.text_input("Departamento")
            dep_text = st.text_area("Aviso")
            if st.form_submit_button("Publicar Aviso"):
                if dep_name.strip() and dep_text.strip():
                    church.setdefault("notices", []).append(
                        {"department": dep_name.strip(), "text": dep_text.strip()}
                    )
                    save_data()
                    st.rerun()
                else:
                    st.error("Preencha todos os campos do formulário.")

    with st.expander("⚙️ Editar dados desta comunidade"):
        with st.form("edit_church"):
            new_name = st.text_input("Nome", church["name"])
            new_type = st.selectbox("Tipo", ["Igreja", "Grupo"], index=0 if church.get("type") == "Igreja" else 1)
            new_location = st.text_input("Endereço", church.get("location", ""))
            new_responsible = st.text_input("Responsável", church.get("responsible", ""))
            if st.form_submit_button("Salvar Alterações"):
                if not new_name.strip():
                    st.error("O nome é obrigatório.")
                else:
                    church.update(
                        {
                            "name": new_name.strip(),
                            "type": new_type,
                            "location": new_location.strip() or "Alagoinhas/BA",
                            "responsible": new_responsible.strip() or "A definir",
                        }
                    )
                    save_data()
                    st.rerun()

    render_footer()

# Visualização: Hoje em Alagoinhas
def render_hoje():
    kind = st.session_state.get("extra") or "prega"
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao início", key="back_hoje", use_container_width=True):
            go("home")

    titles = {
        "prega": ("Veja quem prega hoje", "Escala de pregações nas igrejas e grupos neste dia."),
        "pastor": ("Onde o pastor está?", "Acompanhe o itinerário dos pastores distritais hoje."),
        "ja": ("Onde tem J.A.?", "Igrejas com programação do Ministério Jovem hoje."),
        "mes": ("Escala Mensal por Pregador", "Pesquise por pregador para encontrar a agenda mensal nas igrejas."),
        "especial": ("Eventos e Programações Especiais", "Programações importantes agendadas pelas igrejas de Alagoinhas."),
    }
    title, subtitle = titles.get(kind, titles["prega"])

    st.markdown(
        f"""
        <section class="detail">
            <div class="eyebrow">Programação em Alagoinhas</div>
            <h1>{safe(title)}</h1>
            <p>{safe(subtitle)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if kind == "especial":
        specials = all_special_events()
        if specials:
            for item in specials:
                st.markdown(
                    f"""
                    <div class="agenda" style="border-left: 6px solid var(--accent-gold);">
                        <span class="tag">Evento Especial</span>
                        <h3 style="font-size:1.4rem; margin-top:6px;">{safe(item['title'])}</h3>
                        <p style="font-size:1.15rem; margin-bottom:4px;"><b>Igreja:</b> {safe(item['church'])} ({safe(item['district'])})</p>
                        <p style="font-size:1.15rem; margin-bottom:4px;"><b>Data:</b> {safe(item['date'])}</p>
                        <p style="font-size:1.05rem; color:#555;">{safe(item['description'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhum evento especial agendado no momento.")

    elif kind == "prega":
        rows = today_preachers()
        if rows:
            for row in rows:
                st.markdown(
                    f"""
                    <div class="agenda">
                        <span class="tag">{safe(row["label"])}</span>
                        <h3 style="font-size:1.4rem;">{safe(row["person"])}</h3>
                        <p style="font-size:1.15rem;"><b>Igreja:</b> {safe(row["church"])} · {safe(row["district"])}</p>
                        <p style="font-size:1.15rem;"><b>Horário:</b> {safe(row["time"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhum pregador cadastrado na escala de hoje.")

    elif kind == "pastor":
        for row in today_pastors():
            if row["church"]:
                st.markdown(
                    f"""
                    <div class="agenda">
                        <span class="tag">Itinerário Pastoral</span>
                        <h3 style="font-size:1.4rem;">{safe(row["pastor"])}</h3>
                        <p style="font-size:1.15rem;">Estará presente na <b>{safe(row["church"])}</b> ({safe(row["district"])})</p>
                        <p style="font-size:1.15rem;"><b>Programação:</b> {safe(row["label"])} às {safe(row["time"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="agenda">
                        <span class="tag">Itinerário Pastoral</span>
                        <h3 style="font-size:1.4rem;">{safe(row["pastor"])}</h3>
                        <p style="font-size:1.15rem;">Sem escala registrada para hoje no distrito <b>{safe(row["district"])}</b>.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    elif kind == "ja":
        rows = today_ja()
        if rows:
            for row in rows:
                st.markdown(
                    f"""
                    <div class="agenda">
                        <span class="tag">Jovens Adventistas</span>
                        <h3 style="font-size:1.4rem;">{safe(row["church"])}</h3>
                        <p style="font-size:1.15rem;"><b>Distrito:</b> {safe(row["district"])} · <b>Responsável:</b> {safe(row["person"])}</p>
                        <p style="font-size:1.15rem;"><b>Horário:</b> {safe(row["time"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhum programa J.A. cadastrado para hoje.")

    elif kind == "mes":
        hoje = date.today()
        col_m, col_y = st.columns(2)
        with col_m:
            month = st.selectbox("Mês", range(1, 13), index=hoje.month - 1, format_func=lambda item: MONTHS[item - 1])
        with col_y:
            year = st.number_input("Ano", min_value=2025, max_value=2100, value=hoje.year)
        nome = st.text_input("Digite o nome do pregador")

        if st.button("Buscar Escala", key="busca_pregador", use_container_width=True):
            resultados = churches_for_preacher(nome, month, year)
            if not nome.strip():
                st.error("Digite o nome para pesquisar.")
            elif not resultados:
                st.info("Nenhuma pregação encontrada para este nome no mês selecionado.")
            else:
                st.success(f"{len(resultados)} data(s) encontrada(s) para '{nome.strip()}'.")
                for row in resultados:
                    dia = f"{row['date'].day} de {MONTHS[row['date'].month - 1]} · {WEEKDAYS[row['date'].weekday()]}"
                    st.markdown(
                        f"""
                        <div class="agenda">
                            <span class="tag">{safe(row["label"])}</span>
                            <h3 style="font-size:1.4rem;">{safe(row["church"])}</h3>
                            <p style="font-size:1.15rem;"><b>Data:</b> {safe(dia)} ({safe(row["district"])})</p>
                            <p style="font-size:1.15rem;"><b>Pregador:</b> {safe(row["person"])} · <b>Horário:</b> {safe(row["time"])}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    render_footer()

# Visualização: Informações Institucionais
def render_info():
    key = st.session_state.get("extra") or "distritos"
    pages = st.session_state.info_pages
    page = pages.get(key, DEFAULT_INFO["distritos"])

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao início", key="back_info", use_container_width=True):
            go("home")

    st.markdown(
        f"""
        <section class="detail">
            <div class="eyebrow">Informação</div>
            <h1>{safe(page.get("title", ""))}</h1>
            <p style="font-size:1.2rem; line-height:1.7;">{safe(page.get("text", ""))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Editar Conteúdo", key="edit_info_toggle"):
        st.session_state.show_edit_info = not st.session_state.get("show_edit_info", False)

    if st.session_state.get("show_edit_info", False):
        with st.form("edit_info"):
            new_title = st.text_input("Título", page.get("title", ""))
            new_text = st.text_area("Texto", page.get("text", ""), height=200)
            if st.form_submit_button("Salvar Alterações"):
                pages[key] = {"title": new_title.strip() or page.get("title", ""), "text": new_text.strip()}
                save_info()
                st.session_state.show_edit_info = False
                st.success("Texto atualizado com sucesso.")
                st.rerun()

    render_footer()

# Visualização: 28 Crenças
def render_crencas():
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao início", key="back_crencas", use_container_width=True):
            go("home")

    st.markdown(
        """
        <section class="detail">
            <div class="eyebrow">Fé & Doutrina</div>
            <h1>As 28 Crenças Fundamentais</h1>
            <p>Principais pilares da fé professada pela Igreja Adventista do Sétimo Dia.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    html_block = '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-top:16px;">'
    for titulo, texto in CRENCAS_FUNDAMENTAIS:
        html_block += f'<div class="info"><h3 style="font-size:1.35rem;">{safe(titulo)}</h3><p style="font-size:1.1rem; line-height:1.6;">{safe(texto)}</p></div>'
    html_block += "</div>"
    st.markdown(html_block, unsafe_allow_html=True)

    render_footer()

# Visualização: Colégio Adventista
def render_education():
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar ao início", key="back_education", use_container_width=True):
            go("home")

    st.markdown(
        f"""
        <section class="detail">
            <div class="eyebrow">REDE DE EDUCAÇÃO ADVENTISTA</div>
            <h1>{safe(COLEGIO["name"])}</h1>
            <p>Uma educação que vai muito além do ensino.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin: 2rem 0 1rem;">
            <h2>Apresentação Institucional</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Ambiente focado em excelência acadêmica e valores cristãos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    levels = " · ".join(COLEGIO["levels"])
    st.markdown(
        f"""
        <div class="info">
            <p style="font-size:1.15rem; line-height:1.7;">{safe(COLEGIO["presentation"])}</p>
            <p style="margin-top:10px; font-size:1.15rem;"><b>Níveis de Ensino:</b> {safe(levels)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin: 2rem 0 1rem;">
            <h2>Canais de Atendimento</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Contatos oficiais da instituição.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f"""
            <div class="info" style="height:100%;">
                <b>Endereço Oficial</b><br>{safe(COLEGIO["address"])}<br>CEP {safe(COLEGIO["cep"])}<br><br>
                <b>Telefone de Contato</b><br>{safe(COLEGIO["phone"])}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="info" style="height:100%;">
                <b>Portal Oficial</b><br>
                <a href="{safe(COLEGIO["site"])}" target="_blank" style="color:var(--accent-blue); font-weight:700;">{safe(COLEGIO["site"])}</a><br><br>
                <b>Atendimento via WhatsApp</b><br>
                <a href="{safe(COLEGIO["whatsapp_link"])}" target="_blank" style="color:var(--accent-blue); font-weight:700;">{safe(COLEGIO["whatsapp"])}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin: 2rem 0 1rem;">
            <h2>Localização</h2>
            <p style="font-size:1.15rem; color:var(--text-dark); font-weight:600;">Avenida Severino Vieira, 1077 — Centro, Alagoinhas/BA.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="border:1px solid var(--border-color); border-radius:var(--radius-md); overflow:hidden; height:340px; margin-bottom:12px;">
            <iframe src="{COLEGIO["map_embed"]}" width="100%" height="100%" style="border:0;" loading="lazy"></iframe>
        </div>
        <p><a href="{safe(COLEGIO["map_link"])}" target="_blank" style="color:var(--accent-blue); font-weight:700;">Abrir no Google Maps ↗</a></p>
        """,
        unsafe_allow_html=True,
    )

    if COLEGIO_IMAGE.exists():
        st.image(str(COLEGIO_IMAGE), use_container_width=True)

    st.link_button("Acessar Site Oficial do Colégio", COLEGIO["site"], use_container_width=True)
    render_footer("Colégio Adventista de Alagoinhas.")

# Inicialização de Estados
if "districts" not in st.session_state:
    st.session_state.districts = load_data()
if "view" not in st.session_state:
    st.session_state.view = "home"
if "district" not in st.session_state:
    st.session_state.district = None
if "church_index" not in st.session_state:
    st.session_state.church_index = None
if "show_add" not in st.session_state:
    st.session_state.show_add = False
if "show_add_team" not in st.session_state:
    st.session_state.show_add_team = False
if "extra" not in st.session_state:
    st.session_state.extra = None
if "info_pages" not in st.session_state:
    st.session_state.info_pages = load_info()
if "show_edit_info" not in st.session_state:
    st.session_state.show_edit_info = False

# Aplicação de Parâmetros e Roteamento
apply_query_params()
render_header()

if st.session_state.view == "home":
    render_home()
elif st.session_state.view == "districts":
    render_districts_page()
elif st.session_state.view == "district":
    render_district()
elif st.session_state.view == "church":
    render_church()
elif st.session_state.view == "education":
    render_education()
elif st.session_state.view == "hoje":
    render_hoje()
elif st.session_state.view == "info":
    render_info()
elif st.session_state.view == "crencas":
    render_crencas()
elif st.session_state.view == "membros":
    render_membros_page()
else:
    go("home")