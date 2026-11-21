#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Saturday 21 November 2026.

A map-dominant atlas front page: masthead, two lead panels, a large
world map with 36 numbered markers, and a region-grouped story ledger.
Deterministic: fixed content, no randomness, no network. Writes
entry.png (1024x1024, <= 1 MiB) to $MAKEFUN_OUTPUT_DIR or ./out.
All 36 stories were verified against news reported on 20-21 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 221)
INK = (26, 26, 46)
RED = (176, 48, 48)
BLUE = (31, 78, 121)
OCEAN = (216, 230, 236)
LAND = (232, 217, 168)
LAND_EDGE = (138, 123, 82)
GOLD = (180, 138, 40)
GREY = (90, 90, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# (num, region, headline, detail, lon, lat) -- display lon/lat nudged
# slightly where markers would collide on the east coast of the USA.
STORIES = [
    # EUROPE
    (1, "Europe", "Russian missile hits Poland",
     "NATO ally condemns the strike as a violation; allies hold drills.", 19, 52),
    (2, "Europe", "Russia hits Kyiv bridges; 9 dead",
     "Double-tap strike on Kryvyi Rih kills a child, injures 42.", 30.5, 50.4),
    (3, "Europe", "Danes charged in Russia murder plot",
     "Two men accused of being recruited to kill a Ukrainian rapper.", 11, 56.5),
    (4, "Europe", "UK and EU agree closer ties",
     "New deal struck; Burnham says explore even closer relations.", -1, 52.5),
    (5, "Europe", "EU approves EUR 1bn arms aid",
     "Council adopts two decisions for military aid to Ukraine.", 8, 52.5),
    (6, "Europe", "Paris police sentenced",
     "Officers convicted over the beating of producer Michel Zecler.", 2.35, 48.85),
    (7, "Europe", "UK pledges 1,000 drones",
     "GBP 260m package of drones for Ukraine announced in London.", -0.1, 51.5),
    # AMERICAS
    (8, "Americas", "Magnitude 6.8 quake shakes Peru",
     "Junin in the Andes hit; tremors felt 320 km away in Lima.", -75, -11),
    (9, "Americas", "Rikers Island to close by 2032",
     "Mayor Mamdani unveils New York's plan to shut the jail complex.", -74, 40.7),
    (10, "Americas", "Trump targets AI centres abroad",
     "US firms building data centres overseas face penalties.", -77, 38.9),
    (11, "Americas", "Senate rejects Iran war powers",
     "Resolution fails 51-48 in the US Senate.", -79.5, 36.5),
    (12, "Americas", "19 years for Sikh murder plot",
     "Indian man sentenced in the US over a separatist killing plot.", -73.5, 41.8),
    (13, "Americas", "More UFO footage declassified",
     "US releases new footage filmed in the Middle East.", 47, 29),
    (14, "Americas", "Trump pardons Pete Rose",
     "Posthumous pardon for the late baseball star.", -84.5, 39),
    (15, "Americas", "Bukele eyes third term",
     "El Salvador's president set to formalise a third-term bid.", -89.2, 13.7),
    # ASIA-PACIFIC
    (16, "Asia-Pacific", "Record cash floods Indian shares",
     "Foreign investors pour in Rs 1.22 lakh crore in November.", 72.8, 19),
    (17, "Asia-Pacific", "Cyclone Akvan hits Odisha",
     "Storm crosses the coast near Gopalpur with heavy rain.", 85, 20),
    (18, "Asia-Pacific", "Rahul makes SENA history",
     "First Indian opener with Test tons in all four SENA nations.", 174.8, -41.3),
    (19, "Asia-Pacific", "Nepal PM heads to Delhi",
     "Balen Shah's first foreign visit since taking office in March.", 77.2, 28.6),
    (20, "Asia-Pacific", "India U17 qualify unbeaten",
     "Goalless draw with Malaysia tops the group for Uzbekistan 2027.", 101.7, 3.1),
    (21, "Asia-Pacific", "Pakistan win first Test series",
     "Eight-wicket win over Sri Lanka ends a two-year wait.", 67, 24.9),
    (22, "Asia-Pacific", "Hong Kong Open semi-finals",
     "Lakshya Sen and Satwik-Chirag reach the last four.", 114.2, 22.3),
    # MIDDLE EAST & AFRICA
    (23, "Middle East & Africa", "ICJ: Myanmar committed genocide",
     "Landmark ruling for the Rohingya; states hail the judgment.", 96, 21),
    (24, "Middle East & Africa", "Riyadh hit by Houthi missile",
     "Saudi Arabia intercepts the attack; debris causes damage.", 46.7, 24.6),
    (25, "Middle East & Africa", "US sanctions four Iranians",
     "Treasury targets handlers of Iranian oil revenues.", 51.4, 35.7),
    (26, "Middle East & Africa", "ANC fights for South Africa cities",
     "Party battles to hold key metros after an election setback.", 28, -26.2),
    (27, "Middle East & Africa", "Yemen displacement rises",
     "UN counts about 357,000 displaced since August.", 44, 15.3),
    (28, "Middle East & Africa", "Pyongyang and Laos draw closer",
     "North Korea and Laos vow closer cooperation in Pyongyang.", 125.8, 39),
    (29, "Middle East & Africa", "Palestinian shot in West Bank",
     "Man killed by a settler guard in the occupied territory.", 35.2, 31.9),
    # MARKETS, TECH & SPORT
    (30, "Markets, Tech & Sport", "COP31 talks run into overtime",
     "Antalya summit stalls as fossil-fuel wording drops from draft.", 30.7, 36.9),
    (31, "Markets, Tech & Sport", "Tech sell-off sinks markets",
     "S&P 500 falls 3.7%; Nasdaq turns negative for the year.", -72, 42.5),
    (32, "Markets, Tech & Sport", "Banks hit by vendor cyberattack",
     "JPMorgan, Visa and Mastercard report third-party breaches.", -75.5, 39.8),
    (33, "Markets, Tech & Sport", "Kane out for months",
     "Bayern star tears ankle ligament in 1-1 draw with Cologne.", 11.6, 48.1),
    (34, "Markets, Tech & Sport", "Lyon end Arsenal's unbeaten run",
     "OL Lyonnes win 2-0 in the Women's Champions League.", -0.5, 51.7),
    (35, "Markets, Tech & Sport", "Zverev into ATP Finals semis",
     "German beats Shelton in straight sets in Turin.", 7.7, 45.1),
    (36, "Markets, Tech & Sport", "US clears 900k AI chips for China",
     "House committee reports six months of export approvals.", 116.4, 39.9),
]

REGIONS = ["Europe", "Americas", "Asia-Pacific",
           "Middle East & Africa", "Markets, Tech & Sport"]
REGION_COLOURS = {"Europe": (31, 78, 121), "Americas": (176, 48, 48),
                  "Asia-Pacific": (42, 110, 70),
                  "Middle East & Africa": (146, 90, 20),
                  "Markets, Tech & Sport": (96, 52, 130)}

# Rough continent outlines in (lon, lat). Stylised atlas shapes.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-70, 62), (-65, 60), (-60, 55), (-55, 52), (-60, 47),
     (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
     (-84, 30), (-89, 29), (-91, 19), (-94, 17), (-97, 16), (-92, 15),
     (-87, 13), (-83, 9), (-79, 8), (-77, 7), (-80, 9), (-83, 10),
     (-86, 12), (-88, 14), (-90, 14), (-92, 15), (-95, 18), (-97, 21),
     (-97, 26), (-101, 25), (-105, 20), (-109, 23), (-112, 29),
     (-114, 31), (-117, 33), (-121, 34), (-124, 40), (-124, 48),
     (-127, 50), (-130, 54), (-135, 58), (-140, 60), (-145, 60),
     (-150, 61), (-158, 58), (-162, 55), (-165, 60)],
    [(-77, 7), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-61, 9),
     (-59, 8), (-55, 6), (-52, 5), (-50, 0), (-44, -3), (-41, -5),
     (-35, -8), (-37, -11), (-39, -15), (-40, -20), (-41, -23),
     (-48, -27), (-52, -32), (-57, -38), (-62, -41), (-66, -45),
     (-68, -50), (-69, -54), (-71, -54), (-73, -50), (-73, -44),
     (-72, -37), (-71, -30), (-70, -23), (-70, -18), (-75, -15),
     (-77, -12), (-80, -6), (-81, -3), (-80, 1), (-79, 4)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 34), (-2, 35),
     (3, 37), (10, 37), (11, 34), (15, 32), (19, 31), (25, 32),
     (30, 31), (32, 31), (35, 28), (37, 22), (39, 21), (43, 12),
     (48, 11), (51, 11), (51, 2), (46, -1), (41, -4), (40, -10),
     (39, -16), (36, -18), (35, -23), (32, -26), (28, -33), (26, -34),
     (20, -35), (17, -32), (15, -27), (13, -18), (12, -12), (13, -6),
     (9, -1), (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)],
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (1, 51),
     (3, 53), (5, 53), (7, 54), (8, 57), (10, 59), (6, 58), (5, 60),
     (6, 62), (10, 64), (14, 67), (18, 69), (25, 71), (30, 70), (35, 67),
     (40, 68), (45, 68), (50, 69), (55, 69), (60, 69), (65, 69), (70, 72),
     (75, 73), (80, 73), (85, 74), (95, 76), (105, 77), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 71), (160, 70), (170, 66),
     (178, 65), (178, 62), (170, 60), (162, 59), (158, 53), (156, 51),
     (150, 59), (142, 59), (141, 53), (140, 47), (138, 43), (135, 43),
     (132, 43), (128, 39), (127, 35), (122, 38), (121, 32), (120, 28),
     (115, 23), (110, 21), (109, 18), (109, 13), (105, 9), (103, 7),
     (100, 8), (98, 12), (98, 15), (97, 16), (94, 17), (92, 21), (89, 22),
     (86, 20), (80, 16), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25),
     (62, 25), (58, 25), (56, 27), (52, 28), (50, 29), (48, 30),
     (44, 29), (48, 28), (52, 26), (55, 25), (58, 22), (59, 20),
     (55, 17), (50, 15), (45, 13), (42, 15), (40, 20), (39, 24),
     (37, 28), (35, 29), (36, 36), (33, 35), (30, 36), (27, 37),
     (23, 36), (22, 37), (19, 40), (16, 38), (12, 38), (10, 37),
     (8, 37), (6, 37), (3, 37), (0, 36), (-2, 35), (-5, 36), (-9, 37)],
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (137, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
     (141, 40), (142, 42), (144, 44), (142, 45), (140, 42), (139, 39),
     (137, 37), (135, 35), (133, 34), (131, 33)],
    [(95, 5), (98, 3), (100, 0), (104, -3), (106, -6), (110, -7),
     (114, -8), (119, -9), (120, -10), (124, -10), (128, -8), (131, -4),
     (132, -2), (131, 0), (128, 1), (124, 1), (120, 1), (117, 0),
     (114, 2), (110, 2), (106, 1), (103, 1), (100, 0), (97, 5)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (175, -40), (173, -42), (170, -44), (167, -46)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -23), (45, -25),
     (44, -21), (43, -17)],
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 74), (-25, 78), (-35, 80), (-55, 80), (-60, 76), (-58, 70)],
    [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-20, 66), (-24, 65)],
]

MAP_X0, MAP_X1 = 24, 1000
MAP_Y0, MAP_Y1 = 236, 500


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (84.0 - lat) / 144.0 * (MAP_Y1 - MAP_Y0)
    return x, y


def draw_map(draw):
    draw.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN,
                   outline=INK, width=2)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # graticule
    for lon in range(-150, 181, 30):
        x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
        draw.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(190, 205, 210), width=1)
    for lat in (60, 30, 0, -30):
        _, y = project(0, lat)
        draw.line([(MAP_X0, y), (MAP_X1, y)], fill=(190, 205, 210), width=1)
    # equator label
    draw.text((MAP_X0 + 6, project(0, 0)[1] + 3), "EQUATOR",
              font=SANS(8), fill=GREY)
    # markers
    for num, _reg, _t, _d, lon, lat in STORIES:
        x, y = project(lon, lat)
        r = 10
        draw.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(num)
        fnt = SANS_B(9 if num < 10 else 8)
        tw = draw.textlength(label, font=fnt)
        draw.text((x - tw / 2, y - 6.5), label, font=fnt,
                  fill=(255, 255, 255))


def draw_lead(draw, x0, x1, y0, y1, kicker, title, body):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 251, 238),
                   outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 24], fill=RED)
    draw.text((x0 + 10, y0 + 5), kicker, font=SANS_B(12),
              fill=(255, 255, 255))
    draw.text((x0 + 10, y0 + 30), title, font=SERIF_B(17), fill=INK)
    for i, line in enumerate(wrap(draw, body, SANS(12), x1 - x0 - 20)):
        draw.text((x0 + 10, y0 + 56 + i * 16), line, font=SANS(12),
                  fill=(40, 40, 55))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # outer frame
    draw.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    draw.rectangle([14, 14, W - 15, H - 15], outline=GOLD, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(46)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    draw.line([(60, 88), (W - 60, 88)], fill=INK, width=2)
    sub = "SATURDAY, 21 NOVEMBER 2026  \u00b7  36 STORIES  \u00b7  5 REGIONS  \u00b7  ONE DAY OF WORLD NEWS"
    sf = SANS_B(13)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 96), sub, font=sf, fill=RED)

    # ---- lead panels ----
    draw_lead(draw, 20, 502, 122, 212, "LEAD 1  \u00b7  PERU",
              "Quake shakes the Andes",
              "A magnitude 6.8 earthquake strikes Junin in central Peru; "
              "tremors are felt 320 km away in the capital, Lima.")
    draw_lead(draw, 522, 1004, 122, 212, "LEAD 2  \u00b7  THE HAGUE",
              "Myanmar guilty of genocide",
              "The International Court of Justice rules Myanmar committed "
              "genocide against the Rohingya, a landmark judgment.")

    # ---- map ----
    draw.text((20, 220), "THE WORLD AT A GLANCE \u2014 36 STORIES, NUMBERED ON THE MAP",
              font=SANS_B(13), fill=INK)
    draw_map(draw)

    # ---- story ledger ----
    draw.text((20, 512), "THE DAY IN BRIEF \u2014 BY REGION",
              font=SANS_B(13), fill=INK)
    draw.line([(20, 532), (1004, 532)], fill=INK, width=2)
    col_w, gap = 192, 6
    x = 20
    for region in REGIONS:
        items = [s for s in STORIES if s[1] == region]
        colour = REGION_COLOURS[region]
        draw.rectangle([x, 540, x + col_w, 562], fill=colour)
        rf = SANS_B(11)
        label = region.upper()
        while draw.textlength(label, font=rf) > col_w - 8 and len(label) > 4:
            label = label[:-1]
        draw.text((x + 4, 546), label, font=rf, fill=(255, 255, 255))
        y = 570
        for num, _r, headline, detail, _lon, _lat in items:
            draw.text((x, y), str(num), font=SANS_B(11), fill=RED)
            lines = wrap(draw, headline, SANS_B(10), col_w - 24)
            for i, ln in enumerate(lines):
                draw.text((x + 22, y + i * 13), ln, font=SANS_B(10),
                          fill=INK)
            y += len(lines) * 13 + 2
            dlines = wrap(draw, detail, SANS(9), col_w - 22)
            for i, ln in enumerate(dlines):
                draw.text((x + 22, y + i * 12), ln, font=SANS(9),
                          fill=(60, 60, 70))
            y += len(dlines) * 12 + 6
        x += col_w + gap

    # ---- footer ----
    draw.line([(20, 992), (1004, 992)], fill=INK, width=1)
    foot = ("All 36 stories reported 20\u201321 November 2026  \u00b7  "
            "Drawn from the day's news wires  \u00b7  THE WORLD IN ONE DAY")
    ff = SANS(10)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 1000), foot, font=ff, fill=GREY)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
