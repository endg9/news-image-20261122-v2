#!/usr/bin/env python3
"""Render THE WORLD IN ONE DAY - 22 November 2026 (news-image-20261122 v2).

Fresh renderer written in this session. 1024x1024 PNG, PIL only.
Layout: navy masthead, 4 lead cards in a 2x2 grid, a "still to come"
timeline strip, 26 briefs in two columns (bold run-in head + text),
DATE CHECK box, footer. Every story was first reported on Sunday
22 November 2026 (WIB day); timed events that had not happened at
render time are labelled PREVIEW.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 24, 38)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
MUTED = (90, 92, 100)
CARD = (255, 255, 255)
LINE = (200, 196, 184)
AMBER_BG = (255, 244, 214)
AMBER_LINE = (214, 164, 32)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, spacing=1, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def wrap_mixed(draw, head, text, f_head, f_text, width):
    """Wrap a bold run-in head + regular text into lines of (word, font) segs."""
    toks = [(w + " ", f_head) for w in head.split()]
    toks += [(w + " ", f_text) for w in text.split()]
    lines, cur, cur_w = [], [], 0.0
    for word, fnt in toks:
        ww = draw.textlength(word, font=fnt)
        if cur and cur_w + ww > width:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur.append((word, fnt))
        cur_w += ww
    if cur:
        lines.append(cur)
    return lines


LEADS = [
    ("COP31", "Final climate text tabled \u2014 deal vote at 13:00 WIB",
     "Third draft at 03:00 local after all-night talks. No phase-out line; $120bn "
     "target dropped. Vote later \u2014 no deal yet. [PREVIEW]"),
    ("NEPAL \u2014 INDIA", "PM Balendra Shah lands in Delhi for two-day state visit",
     "First state visit since taking office in March. Arrives 15:45 WIB; Modi talks "
     "Monday. A reported ~$2bn economic package is on the table."),
    ("CRICKET \u2014 WELLINGTON", "India declare 720/9 \u2014 New Zealand 29/1, trailing 323",
     "Pant 128 breaks Kirmani's 45-year-old record; Rahul 136. Highest Test total ever "
     "at Basin Reserve. Day four, match in progress."),
    ("LAS VEGAS GP", "Verstappen on pole for tonight's night race",
     "Antonelli fastest in qualifying but a 5-place grid penalty hands pole to "
     "Verstappen. Race starts 11:00 WIB \u2014 not yet run. [PREVIEW]"),
]

# (tag, text) - text kept short so each brief fits ~2 lines at 11px
BRIEFS = [
    ("LPGA", "A Lim Kim leads the CME finale at -18 by one after a third-round 69; Thitikul and Yoshida -17; Korda two back."),
    ("ATP FINALS", "Alcaraz beats Shelton 3-6, 6-3, 7-6(1); Zverev beats Medvedev 7-6(0), 6-4. Final tonight in Turin."),
    ("NBA", "Harden scores 51 as Cleveland beat Indiana 128-119, passing Kobe; 76ers edge Bucks 132-129; SGA 40 in a Thunder win."),
    ("PREMIER LEAGUE", "Arsenal held 2-2 at Newcastle; Man City draw 1-1 at Fulham; Leeds stun Chelsea 4-1; Bournemouth 2-0 Forest."),
    ("COLLEGE FOOTBALL", "Nebraska stuns No. 14 Ohio State 31-27; No. 10 BYU outlasts Kansas 31-29 in 3OT; Wake Forest beats Georgia Tech 50-29."),
    ("TAIWAN\u2013CANADA", "Deputy FM Chen warns PM Carney that deeper China trade ties risk economic coercion; flags surveillance risks from Chinese EVs."),
    ("COPA SUDAMERICANA", "Boca Juniors beat Atletico Mineiro 2-0 in Barranquilla to win the final \u2014 first continental crown since 2007."),
    ("INDONESIA QUAKE", "A magnitude 4.7 earthquake strikes near Jayapura, Papua, on Sunday morning (06:16 WIB), BMKG reports."),
    ("SEOUL SHORT TRACK", "Sunday finals from 12:00 WIB at Mokdong: mixed team relay, women's 500m and 1500m, men's 1000m and 5000m relay. [PREVIEW]"),
    ("INDIA", "Amit Shah reviews security in Arunachal Pradesh; Modi attends Kaushal Deekshant Samaroh in Lucknow; SCO dialogue day 2 in Delhi."),
    ("TAIWAN", "TPP candidate Lin Naili freed on bail in an anti-infiltration probe; a vote-buying probe opens in Jiaoxi, Yilan."),
    ("WBBL", "Brisbane Heat host Adelaide Strikers today (11:40 WIB); Melbourne Stars face Melbourne Renegades in the derby. [PREVIEW]"),
    ("AUSTRALIA", "Deputy PM Marles tells ABC's Insiders that spreading AI infrastructure is in America's own interest; Burke calls data centres a 'magnet' for foreign interference."),
    ("LA LIGA", "Real Madrid come from behind to beat Celta Vigo 2-1 \u2014 Bellingham levels, Espi nets an 85th-minute winner after Mbappe misses a penalty."),
    ("SERIE A / BUNDESLIGA", "Lazio stay top with a 3-0 win over Lecce; Dortmund go top with a late 1-0 win at Borussia Monchengladbach (Nmecha 80')."),
    ("UFC DOHA", "Undefeated Navajo Stirling KOs former champion Jiri Prochazka at 4:58 of round two. Vallejos beats Sterling on points; Ortega retires."),
    ("NHL", "Carolina rout Edmonton 7-4; Florida edge Buffalo 4-3 as Sam Bennett scores a hat trick; Chicago beat Calgary 4-3 in OT."),
    ("RUGBY", "England rout New Zealand 37-12 \u2014 biggest-ever win over the All Blacks; France beat Argentina 45-17; Ireland edge South Africa 20-17."),
    ("GOLF", "Rain washes out the third round of the RSM Classic at Sea Island, pushing the PGA Tour finale to a Monday finish. Leaders at -9."),
    ("SPACEX", "A Falcon 9 is set to launch the NROL-136 spy-satellite batch from Vandenberg at 19:23 WIB; booster B1097 flies a 14th time. [PREVIEW]"),
    ("INDONESIA", "From 1 Jan 2027, exports of coal, crude palm oil and ferroalloy must go through Danantara's DSI, the government says."),
    ("OBIHIRO", "Jordan Stolz chases his 49th World Cup win in Sunday's second 500m (14:49 WIB) after a track-record 34.26 on Saturday. [PREVIEW]"),
    ("HONG KONG OPEN", "Badminton finals today: Antonsen vs Kunlavut (men's singles), Wang Zhiyi vs Chochuwong (women's), Man-Tee vs Leo/Daniel. [PREVIEW]"),
    ("MYANMAR QUAKE", "A magnitude 4.1 earthquake strikes Myanmar early Sunday (02:35 IST), depth 95 km, India's National Centre for Seismology reports."),
    ("PHILIPPINES QUAKE", "A magnitude 4.6 quake strikes off Balut Island, Davao Occidental, early Sunday \u2014 an aftershock of June's M7.8 Sarangani quake, PHIVOLCS says."),
    ("SAUDI ARABIA", "The national weather centre issues moderate-rain alerts for Sunday afternoon (13:00\u201320:00) in western regions, with thunderstorms expected."),
]

TIMELINE = [
    ("11:00", "F1 GP"),
    ("11:40", "WBBL Heat\u2013Strikers"),
    ("12:00", "Seoul finals"),
    ("13:00", "COP31 plenary"),
    ("14:49", "Obihiro 500m"),
    ("19:23", "SpaceX launch"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 deliberately excluded (reported before Sunday 22 Nov): Bahrain\u2013Iran strikes (21 Nov); "
    "Peru quake M6.7 (20 Nov); Kyiv barrage (19\u201320 Nov); Gaza van strike (21 Nov); El Chapo Isidro held (20 Nov); "
    "US stocks plunge (20 Nov); ICJ Myanmar ruling (19 Nov); Trump\u2013Xi\u2013Putin summit (19 Nov); Lospalos quake M6.8 (21 Nov); "
    "Riyadh missiles (21 Nov); France protests 82,500 (21 Nov); Eisenkot coalition talks (reported Sat 21 Nov); "
    "Cyclone Xavier (statement Sat 21 Nov); Bitcoin's $55k dip and $60k rebound (Sat 21 Nov); WBBL Sat results (21 Nov); "
    "Seoul Sat finals (21 Nov); Scotland 67\u20135 Japan (21 Nov); Guns N' Roses GBK (21 Nov)."
)


def render(bs=11, hs=12):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(FB, 46)
    f_sub = font(FR, 17)
    f_kick = font(FB, 13)
    f_lead_head = font(FB, 19)
    f_deck = font(FR, 13)
    f_tl_head = font(FB, 13)
    f_tl = font(FR, 13)
    f_bhead = font(FB, hs)
    f_btext = font(FR, bs)
    f_dc = font(FR, 11)
    f_foot = font(FR, 12)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 106], fill=NAVY)
    d.rectangle([0, 106, W, 111], fill=RED)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 10), title,
           font=f_title, fill=(255, 255, 255))
    sub = "SUNDAY 22 NOVEMBER 2026  \u2022  30 STORIES, ALL FIRST REPORTED TODAY"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 68), sub,
           font=f_sub, fill=(205, 212, 228))

    # ---- Leads: 2x2 grid ----
    y = 124
    cw, chh, gap = 478, 106, 20
    for i, (kick, head, deck) in enumerate(LEADS):
        x = 24 + (i % 2) * (cw + gap)
        yy = y + (i // 2) * (chh + 12)
        d.rectangle([x, yy, x + cw, yy + chh], fill=CARD, outline=LINE, width=1)
        d.rectangle([x, yy, x + 5, yy + chh], fill=RED)
        d.text((x + 16, yy + 8), f"{i+1:02d}  {kick}", font=f_kick, fill=RED)
        ny = draw_wrapped(d, x + 16, yy + 27, head, f_lead_head, cw - 32,
                          INK, spacing=1, max_lines=2)
        draw_wrapped(d, x + 16, ny + 1, deck, f_deck, cw - 32, MUTED,
                     spacing=1, max_lines=2)
    y = y + 2 * chh + 12 + 12

    # ---- Timeline strip ----
    d.rectangle([24, y, W - 24, y + 58], fill=AMBER_BG, outline=AMBER_LINE, width=1)
    d.text((38, y + 6), "STILL TO COME TODAY  (WIB) \u2014 previews, results not yet known:",
           font=f_tl_head, fill=(90, 60, 0))
    total_w = sum(d.textlength(t, font=f_tl_head) + 5 +
                  d.textlength(lab, font=f_tl) for t, lab in TIMELINE) + 5 * 20
    tx = (W - total_w) / 2
    ty = y + 30
    for t, lab in TIMELINE:
        d.text((tx, ty), t, font=f_tl_head, fill=RED)
        tx += d.textlength(t, font=f_tl_head) + 5
        d.text((tx, ty), lab, font=f_tl, fill=INK)
        tx += d.textlength(lab, font=f_tl) + 20
    y += 58 + 12

    # ---- Briefs: two columns, bold run-in heads ----
    d.text((24, y), "THE REST OF THE DAY", font=font(FB, 15), fill=NAVY)
    d.line([24, y + 22, W - 24, y + 22], fill=RED, width=2)
    y += 30
    col_w = 478
    col_x = [24, 522]
    line_h = bs + 3
    max_bottom = y
    for col in range(2):
        cy = y
        for k in range(13):
            idx = col * 13 + k
            tag, text = BRIEFS[idx]
            head = f"{idx+1:02d} {tag} \u2014 "
            lines = wrap_mixed(d, head, text, f_bhead, f_btext, col_w - 8)
            for segs in lines:
                sx = col_x[col] + 4
                for word, fnt in segs:
                    d.text((sx, cy), word, font=fnt, fill=INK)
                    sx += d.textlength(word, font=fnt)
                cy += line_h
            cy += 4
        max_bottom = max(max_bottom, cy)
    y = max_bottom + 2

    # ---- DATE CHECK box ----
    dc_lines = wrap(d, DATE_CHECK, f_dc, W - 48 - 28)
    box_h = len(dc_lines) * 14 + 14
    d.rectangle([24, y, W - 24, y + box_h], fill=(238, 234, 222),
                outline=LINE, width=1)
    yy = y + 7
    for ln in dc_lines:
        d.text((38, yy), ln, font=f_dc, fill=(70, 70, 78))
        yy += 14
    y += box_h + 8

    # ---- Footer ----
    foot = ("All 30 stories happened or were first reported on Sunday 22 November 2026 (WIB day).  "
            "Sources: Reuters, AP, Carbon Brief, Cricinfo, PHIVOLCS, BMKG, Sportradar, NCS.")
    flines = wrap(d, foot, f_foot, W - 48)
    yy = y
    for ln in flines:
        d.text(((W - d.textlength(ln, font=f_foot)) / 2, yy), ln,
               font=f_foot, fill=MUTED)
        yy += 16
    return img, yy


def main():
    for bs in (11, 10):
        img, bottom = render(bs=bs, hs=bs + 1)
        if bottom <= H - 4:
            break
    img.save("entry.png", optimize=True)
    print(f"saved entry.png bottom={bottom} brief_size={bs}")


if __name__ == "__main__":
    main()
