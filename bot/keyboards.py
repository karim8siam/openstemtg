from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from bot.config import URLS, LEAD_EMAIL

EXPLORE_WEB_URL = "https://openstemfield.org/#/explore"
RECRUITMENT_URL = URLS["recruitment"]
BRIDGE_URL = URLS["bridge"]
GMAIL_URL = f"https://mail.google.com/mail/?view=cm&fs=1&to={LEAD_EMAIL}"
GMAIL_RESEARCH_URL = f"https://mail.google.com/mail/?view=cm&fs=1&to={LEAD_EMAIL}&su=Research%20Supervision%20%26%20Professor%20Outreach%20Inquiry"

COUNTRY_FLAGS = {
    "USA": "🇺🇸",
    "UK": "🇬🇧",
    "Canada": "🇨🇦",
    "Australia": "🇦🇺",
    "Spain": "🇪🇸",
    "New Zealand": "🇳🇿",
    "France": "🇫🇷",
    "Italy": "🇮🇹",
    "Netherlands": "🇳🇱",
    "Hungary": "🇭🇺",
    "Switzerland": "🇨🇭",
    "Germany": "🇩🇪",
    "Sweden": "🇸🇪",
    "Japan": "🇯🇵",
    "Denmark": "🇩🇰",
}

def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Explore OpenSTEM"],
            ["Explore Your Opportunity"],
            ["Explore Your Waiting University"],
            ["Explore Professor for Perfect Research"],
            ["How OpenSTEM Will Help You"],
            ["Free Courses & Test Preparation"],
            ["Join in Partnership Programme"]
        ],
        resize_keyboard=True
    )

def get_welcome_inline_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Explore OpenSTEM", callback_data="open_explore")],
        [InlineKeyboardButton("🎓 Explore Your Opportunity", callback_data="open_opp_start")],
        [InlineKeyboardButton("🏛️ Explore Your Waiting University", callback_data="open_waiting_start")],
        [InlineKeyboardButton("🔬 Explore Professor for Perfect Research", callback_data="open_prof_start")],
        [InlineKeyboardButton("🤝 How OpenSTEM Will Help You", callback_data="open_how_help")],
        [InlineKeyboardButton("📚 Free Courses & Test Preparation", callback_data="open_courses_start")],
        [InlineKeyboardButton("🤝 Join in Partnership Programme", callback_data="open_partnership_start")]
    ])

def get_explore_openstem_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton("🌐 OpenSTEM Field", url=URLS["field"]),
            InlineKeyboardButton("🎓 OpenSTEM Recruitment", url=URLS["recruitment"]),
        ],
        [
            InlineKeyboardButton("🔬 OpenSTEM Research / Lab", url=URLS["lab"]),
            InlineKeyboardButton("📚 OpenSTEM Book / Library", url=URLS["library"]),
        ],
        [
            InlineKeyboardButton("⚙️ OpenSTEM Tool", url=URLS["tool"]),
            InlineKeyboardButton("🌉 OpenSTEM Bridge", url=URLS["bridge"]),
        ],
        [
            InlineKeyboardButton("🔄 OpenSTEM Replicate", url=URLS["replicate"]),
        ],
        [
            InlineKeyboardButton("📺 YouTube Channel", url=URLS["youtube"]),
            InlineKeyboardButton("📱 Facebook Page", url=URLS["facebook"]),
        ],
        [
            InlineKeyboardButton("💬 Discord Community ↗", url=URLS["discord"]),
        ],
        [
            InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_URL),
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def get_subjects_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⌘ Computer Science", callback_data="sel_sub_computer-science"),
            InlineKeyboardButton("⌁ Engineering", callback_data="sel_sub_engineering"),
        ],
        [
            InlineKeyboardButton("✦ Physics", callback_data="sel_sub_physics"),
            InlineKeyboardButton("∑ Mathematics", callback_data="sel_sub_mathematics"),
        ],
        [
            InlineKeyboardButton("❋ Biology & Medicine", callback_data="sel_sub_biology"),
            InlineKeyboardButton("⚗ Chemistry", callback_data="sel_sub_chemistry"),
        ],
        [
            InlineKeyboardButton("◌ Earth & Environment", callback_data="sel_sub_environment"),
            InlineKeyboardButton("◇ Social Sciences", callback_data="sel_sub_social-sciences"),
        ],
        [
            InlineKeyboardButton("◈ Arts & Design", callback_data="sel_sub_arts-design"),
            InlineKeyboardButton("🌐 All Subjects", callback_data="sel_sub_all"),
        ],
        [
            InlineKeyboardButton("🔗 Explore All Opportunities on Web ↗", url=EXPLORE_WEB_URL),
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main"),
        ]
    ])

def get_countries_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇨🇦 Canada", callback_data="sel_cnt_Canada"),
            InlineKeyboardButton("🇺🇸 USA", callback_data="sel_cnt_USA"),
        ],
        [
            InlineKeyboardButton("🇬🇧 UK", callback_data="sel_cnt_UK"),
            InlineKeyboardButton("🇩🇪 Germany", callback_data="sel_cnt_Germany"),
        ],
        [
            InlineKeyboardButton("🇦🇺 Australia", callback_data="sel_cnt_Australia"),
            InlineKeyboardButton("🇮🇹 Italy", callback_data="sel_cnt_Italy"),
        ],
        [
            InlineKeyboardButton("🇯🇵 Japan", callback_data="sel_cnt_Japan"),
            InlineKeyboardButton("🇸🇪 Sweden", callback_data="sel_cnt_Sweden"),
        ],
        [
            InlineKeyboardButton("🇳🇱 Netherlands", callback_data="sel_cnt_Netherlands"),
            InlineKeyboardButton("🇨🇭 Switzerland", callback_data="sel_cnt_Switzerland"),
        ],
        [
            InlineKeyboardButton("🌍 All Countries", callback_data="sel_cnt_all"),
        ],
        [
            InlineKeyboardButton("⬅️ Change Subject", callback_data="open_opp_start"),
            InlineKeyboardButton("« Main Menu", callback_data="back_to_main"),
        ]
    ])

def get_opportunities_view_keyboard(total_pages, current_page, current_type="all"):
    types_row1 = [
        InlineKeyboardButton("🎓 Master's", callback_data="sel_typ_Master"),
        InlineKeyboardButton("🔬 PhD", callback_data="sel_typ_PhD"),
        InlineKeyboardButton("💰 Scholarship", callback_data="sel_typ_Scholarship"),
    ]
    types_row2 = [
        InlineKeyboardButton("💼 Internship", callback_data="sel_typ_Internship"),
        InlineKeyboardButton("🧪 Research", callback_data="sel_typ_Research"),
        InlineKeyboardButton("🤝 Fellowship", callback_data="sel_typ_Fellowship"),
    ]
    types_row3 = [
        InlineKeyboardButton("🌐 All Types", callback_data="sel_typ_all"),
    ]

    nav_row = []
    if current_page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"opp_page_{current_page - 1}"))
    nav_row.append(InlineKeyboardButton(f"📄 {current_page + 1}/{total_pages}", callback_data="noop"))
    if current_page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"opp_page_{current_page + 1}"))

    change_filter_row = [
        InlineKeyboardButton("🌍 Change Country", callback_data="step_change_country"),
        InlineKeyboardButton("📚 Change Subject", callback_data="open_opp_start"),
    ]

    contact_row = [
        InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_URL)
    ]

    web_row = [
        InlineKeyboardButton("🔗 Explore on Web (openstemfield.org) ↗", url=EXPLORE_WEB_URL)
    ]

    main_menu_row = [
        InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
    ]

    keyboard = [types_row1, types_row2, types_row3]
    if nav_row:
        keyboard.append(nav_row)
    keyboard.append(change_filter_row)
    keyboard.append(contact_row)
    keyboard.append(web_row)
    keyboard.append(main_menu_row)

    return InlineKeyboardMarkup(keyboard)

def get_waiting_countries_keyboard(country_counts):
    buttons = []
    row = []
    for c, cnt in country_counts:
        flag = COUNTRY_FLAGS.get(c, "🏛️")
        btn = InlineKeyboardButton(f"{flag} {c} ({cnt})", callback_data=f"w_cnt_{c}")
        row.append(btn)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🌍 All Countries (1,134)", callback_data="w_cnt_all")])
    buttons.append([
        InlineKeyboardButton("🎓 OpenSTEM Recruitment ↗", url=RECRUITMENT_URL),
        InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_URL)
    ])
    buttons.append([InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")])
    return InlineKeyboardMarkup(buttons)

def get_waiting_universities_view_keyboard(total_pages, current_page):
    buttons = []
    nav_row = []
    if current_page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"w_page_{current_page - 1}"))
    nav_row.append(InlineKeyboardButton(f"📄 {current_page + 1}/{total_pages}", callback_data="noop"))
    if current_page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"w_page_{current_page + 1}"))

    if nav_row:
        buttons.append(nav_row)

    buttons.append([
        InlineKeyboardButton("🌍 Change Country", callback_data="open_waiting_start"),
        InlineKeyboardButton("🎓 OpenSTEM Recruitment ↗", url=RECRUITMENT_URL)
    ])
    buttons.append([
        InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_URL)
    ])
    buttons.append([
        InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(buttons)

def get_professors_subject_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💻 Computer Science & AI (661)", callback_data="p_sub_computer-science"),
            InlineKeyboardButton("⚙️ Engineering (662)", callback_data="p_sub_engineering"),
        ],
        [
            InlineKeyboardButton("⚛️ Physics (273)", callback_data="p_sub_physics"),
            InlineKeyboardButton("📐 Mathematics (72)", callback_data="p_sub_mathematics"),
        ],
        [
            InlineKeyboardButton("🧬 Biology & Medicine (886)", callback_data="p_sub_biology"),
            InlineKeyboardButton("⚗️ Chemistry (242)", callback_data="p_sub_chemistry"),
        ],
        [
            InlineKeyboardButton("🌿 Earth & Environment (299)", callback_data="p_sub_environment"),
            InlineKeyboardButton("🏛️ Social Sciences (1,688)", callback_data="p_sub_social-sciences"),
        ],
        [
            InlineKeyboardButton("🎨 Arts & Design (307)", callback_data="p_sub_arts-design"),
            InlineKeyboardButton("🌐 All Subjects (5,090)", callback_data="p_sub_all"),
        ],
        [
            InlineKeyboardButton("🌉 OpenSTEM Bridge ↗", url=BRIDGE_URL),
            InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_RESEARCH_URL)
        ],
        [
            InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
        ]
    ])

def get_professors_view_keyboard(total_pages, current_page):
    buttons = []
    nav_row = []
    if current_page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"p_page_{current_page - 1}"))
    nav_row.append(InlineKeyboardButton(f"📄 {current_page + 1}/{total_pages}", callback_data="noop"))
    if current_page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"p_page_{current_page + 1}"))

    if nav_row:
        buttons.append(nav_row)

    buttons.append([
        InlineKeyboardButton("📚 Choose Another Subject", callback_data="open_prof_start"),
        InlineKeyboardButton("🌉 OpenSTEM Bridge ↗", url=BRIDGE_URL),
    ])
    buttons.append([
        InlineKeyboardButton(f"✉️ {LEAD_EMAIL}", url=GMAIL_RESEARCH_URL)
    ])
    buttons.append([
        InlineKeyboardButton("« Back to Main Menu", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(buttons)
