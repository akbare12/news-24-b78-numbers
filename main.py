#!/usr/bin/env python3
"""News-image entry: Tuesday 24 November 2026 — THE DAY IN NUMBERS. 38 verified stories, 6 regions, 13 illustrated panels (3 heroes + 10 cards), world map from real lat/lon, numbered ALSO list, DATE CHECK. Deterministic PIL-only front page, 1024x1024."""
import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1024, 1024
CREAM, INK, RED, NAVY, GREY, LGREEN, GOLD = (247, 242, 231), (20, 20, 20), (166, 25, 46), (27, 42, 77), (90, 90, 90), (200, 214, 176), (201, 162, 39)
CHIP = {"CONFIRMED": (27, 120, 60), "OFFICIAL": (30, 80, 160), "REPORTED": (90, 90, 90), "CLAIM": (200, 90, 20)}
def F(sz, bold=False, serif=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if serif else ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    try: return ImageFont.truetype(p, sz)
    except Exception: return ImageFont.load_default()
def wrap(d, s, font, mw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= mw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines
def txt(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
def para(d, x, y, s, font, mw, lh, fill=INK):
    for i, ln in enumerate(wrap(d, s, font, mw)): d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(wrap(d, s, font, mw)) * lh
def chip(d, x, y, label):
    c = CHIP.get(label, (90, 90, 90)); f = F(7, True); w = d.textlength(label, font=f) + 8
    d.rounded_rectangle([x, y, x + w, y + 11], radius=3, fill=c); d.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255)); return x + w + 4
def scene(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=NAVY if kind in ("tower", "court", "party") else (70, 90, 120) if kind == "war" else (30, 90, 70) if kind == "sport" else (120, 60, 40) if kind == "ship" else (40, 40, 60) if kind == "market" else (90, 20, 20) if kind == "tech" else (60, 60, 90) if kind in ("crash", "hostage") else (110, 80, 30) if kind == "yemen" else (20, 30, 70))
    if kind == "tower":
        d.rectangle([x + w * .42, y + 12, x + w * .58, y + h - 8], fill=(220, 220, 230)); d.polygon([(x + w * .42, y + 12), (x + w * .5, y + 2), (x + w * .58, y + 12)], fill=GOLD); d.ellipse([x + w * .62, y + 18, x + w * .78, y + 34], fill=(255, 180, 60)); d.rectangle([x + w * .05, y + h - 22, x + w * .38, y + h - 8], fill=(40, 40, 60)); d.rectangle([x + w * .62, y + h - 26, x + w * .95, y + h - 8], fill=(40, 40, 60))
    elif kind == "party":
        d.rectangle([x + w * .30, y + 14, x + w * .70, y + h - 8], fill=(150, 30, 30)); d.polygon([(x + w * .30, y + 14), (x + w * .5, y + 2), (x + w * .70, y + 14)], fill=(120, 20, 20)); d.rectangle([x + w * .46, y + 30, x + w * .54, y + h - 8], fill=(220, 200, 140)); d.rectangle([x + w * .08, y + h - 30, x + w * .26, y + h - 8], fill=(200, 200, 210))
    elif kind == "court":
        d.rectangle([x + w * .28, y + 16, x + w * .72, y + h - 10], fill=(210, 205, 190)); d.polygon([(x + w * .24, y + 16), (x + w * .5, y + 2), (x + w * .76, y + 16)], fill=(150, 40, 40)); d.rectangle([x + w * .44, y + 34, x + w * .56, y + h - 10], fill=(90, 60, 30)); d.ellipse([x + w * .78, y + 14, x + w * .92, y + 28], fill=(255, 200, 60))
    elif kind == "market":
        pts = [(x + 6, y + h - 14), (x + w * .3, y + h * .55), (x + w * .55, y + h * .62), (x + w * .8, y + 12), (x + w - 6, y + 18)]; d.line(pts, fill=(255, 220, 80), width=3); d.line([x + 6, y + h - 14, x + w - 6, y + h - 14], fill=(255, 255, 255), width=1); d.ellipse([x + w * .8 - 4, y + 8, x + w * .8 + 4, y + 16], fill=(255, 220, 80))
    elif kind == "war":
        d.ellipse([x + w * .70, y + 10, x + w * .86, y + 26], fill=(255, 170, 50)); d.polygon([(x + w * .10, y + h - 8), (x + w * .22, y + h * .45), (x + w * .34, y + h - 8)], fill=(50, 50, 55)); d.polygon([(x + w * .40, y + h - 8), (x + w * .55, y + h * .55), (x + w * .70, y + h - 8)], fill=(60, 60, 65))
    elif kind == "sport":
        d.ellipse([x + w * .40, y + 12, x + w * .60, y + h - 12], fill=GOLD); d.rectangle([x + w * .40, y + 12, x + w * .60, y + h - 12], outline=(255, 255, 255), width=2); d.line([x + w * .40, y + h * .5, x + w * .60, y + h * .5], fill=(255, 255, 255), width=2)
    elif kind == "ship":
        d.rectangle([x + w * .15, y + h * .55, x + w * .85, y + h * .75], fill=(180, 60, 40)); d.rectangle([x + w * .30, y + h * .35, x + w * .55, y + h * .55], fill=(220, 220, 220)); d.line([x + w * .05, y + h * .78, x + w * .95, y + h * .78], fill=(120, 180, 220), width=4)
    elif kind == "tech":
        d.rectangle([x + w * .20, y + 14, x + w * .80, y + h - 12], fill=(200, 40, 40)); d.text((x + w * .5, y + h * .32), "!", font=F(26, True), fill=(255, 255, 255), anchor="ma"); d.rectangle([x + w * .10, y + h - 24, x + w * .90, y + h - 12], fill=(30, 30, 40))
    else:
        d.ellipse([x + w * .35, y + 10, x + w * .65, y + h - 10], fill=(255, 220, 120)); d.rectangle([x + w * .10, y + h - 20, x + w * .90, y + h - 8], fill=(40, 40, 50))
NA = [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 29), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-168, 66)]
SA = [(-80, 9), (-70, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -40), (-70, -52), (-73, -37), (-70, -20), (-80, -5), (-80, 9)]
EU = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (30, 60), (30, 70), (20, 70), (15, 68), (5, 60), (5, 58), (-5, 50), (-10, 36)]
AF = [(-17, 15), (-10, 5), (9, 4), (13, -1), (12, -17), (19, -28), (26, -34), (32, -26), (40, -15), (51, -10), (51, 11), (43, 12), (38, 18), (32, 31), (22, 33), (11, 34), (0, 36), (-10, 36), (-17, 15)]
AS = [(30, 70), (60, 70), (70, 72), (90, 75), (110, 77), (130, 72), (160, 70), (178, 66), (162, 60), (158, 52), (142, 50), (140, 40), (130, 38), (127, 35), (122, 30), (120, 22), (110, 20), (105, 10), (100, 8), (97, 16), (92, 21), (88, 22), (80, 13), (77, 8), (73, 20), (66, 25), (60, 25), (57, 26), (52, 28), (48, 30), (43, 30), (40, 36), (36, 36), (30, 36), (30, 46), (30, 70)]
AU = [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (137, -35), (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (113, -22)]

HEROES = [("1 RIYADH \u00b7 MIDDLE EAST", "CONFIRMED", "Houthi drone hits Riyadh's tallest tower again, 11 hurt", "A Houthi drone hits the PIF tower, Riyadh's tallest, for the 2nd time in a week. At least 11 hurt: 2 Saudi, 2 Indian, 3 Nepali, 4 Egyptian.", "tower", "Saudi officials \u00b7 14:27 UTC"), ("2 SHANGHAI \u00b7 ASIA", "OFFICIAL", "China probes Shanghai party chief Chen Jining", "Chen Jining, 62, Shanghai party chief, is probed for \u201cserious violations\u201d. He is the 4th Politburo member to fall in a probe this year.", "party", "CCDI \u00b7 official"), ("3 NEW YORK \u00b7 US / TECH", "CONFIRMED", "Huawei guilty on 10 of 12 counts", "A US federal jury finds Huawei guilty on 10 of 12 counts: trade-secret theft and bank fraud. It is cleared of racketeering. Sentencing is set for Sep 2027.", "court", "US court \u00b7 20:41 UTC")]
CARDS = [("4 ZAPORIZHZHIA \u00b7 EUROPE", "REPORTED", "Russian attacks kill 9 across Ukraine in a day", "Russia kills 9 and wounds 81 in Ukraine in a day. Kyiv says 96 drones were launched and 73 were shot down or jammed.", "war", "Ukraine officials \u00b7 11:37 UTC"), ("5 CAS \u00b7 AFRICA / SPORT", "OFFICIAL", "CAS hands Senegal back the AFCON title", "CAS returns the Africa Cup title to Senegal after Morocco forfeit 3\u20130, so Senegal win 1\u20130 in the final.", "sport", "CAS \u00b7 official"), ("6 HORMUZ \u00b7 MIDDLE EAST", "REPORTED", "IRGC attacks container ship in Hormuz", "An IRGC attack hits a container ship in Hormuz at 18:58 UTC, shutting its navigation near Khasab, Oman.", "ship", "UKMTO / wires \u00b7 18:58 UTC"), ("7 NEW YORK \u00b7 MARKETS", "CONFIRMED", "Dow closes above 50,000 for the first time", "The Dow closes at 50,018, its first finish above 50,000. Nasdaq falls 1.5% as chips slide, while Taiex jumps a record 8.99%.", "market", "Market close \u00b7 confirmed"), ("8 REDMOND \u00b7 TECH", "REPORTED", "Microsoft declares \u2018Code Red\u2019 after historic outage", "After a 24-hour outage on 12\u201313 Nov, the worst in Exchange Online history, Microsoft declares \u2018Code Red\u2019 with a 1-hour global recovery target.", "tech", "Reuters \u00b7 reported"), ("9 ESKISEHIR \u00b7 EUROPE", "REPORTED", "Turkish military helicopter crash kills 5", "A Turkish military AS-532 helicopter crashes in Eskisehir, killing all 5 people on board.", "crash", "Turkish officials \u00b7 19:52 UTC"), ("10 CARTAGENA \u00b7 AMERICAS", "REPORTED", "Supermarket hostages: 25 held in Cartagena", "Gunmen hold 25 hostages in a Cartagena supermarket. Five elderly women are freed and airport landings are paused for about 45 minutes.", "hostage", "Colombia officials \u00b7 17:35 UTC"), ("11 ADEN \u00b7 MIDDLE EAST", "REPORTED", "Houthis advance within 60 km of Aden", "Houthi forces advance to within 60 km of Aden, Yemen, in the latest push south toward the port city.", "yemen", "Wires \u00b7 16:51 UTC"), ("12 LAHJ \u00b7 MIDDLE EAST", "REPORTED", "Saudi strikes kill 25, wound 6 in Yemen", "Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, kill or leave missing 25 people and wound 6 more.", "yemen", "Yemen officials \u00b7 10:42 UTC"), ("13 JIUQUAN \u00b7 SPACE", "OFFICIAL", "China names first foreign astronaut for Tiangong", "China names the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner bound for Tiangong.", "space", "CMSA \u00b7 official")]
UTC = [("00:52", "Megaspeed blacklisted"), ("02:15", "NATO space defence"), ("08:16", "Hanoi hot-pot blast"), ("10:42", "Saudi strikes Yemen"), ("14:27", "Riyadh tower hit"), ("16:51", "Houthis 60 km from Aden"), ("18:58", "Hormuz ship attack"), ("20:41", "Huawei guilty")]
NUMS = [("11", "hurt in Riyadh"), ("9", "killed in Ukraine"), ("50,018", "Dow close"), ("+8.99%", "Taiex record"), ("25", "killed in Lahj"), ("26", "Cikande toll"), ("10/12", "Huawei counts"), ("96", "drones at Ukraine")]
ALSO = [(14, "Ankara", "Haftar visits Turkey for the first time", "REPORTED"), (15, "London", "UK sanctions Houthis + 4 officials", "OFFICIAL"), (16, "Villavicencio", "Car bomb injures 23", "REPORTED"), (17, "Gaza", "Israel kills Hamas internal security chief", "REPORTED"), (18, "Baghdad", "Iraq orders federal control of Kurdish oilfields", "OFFICIAL"), (19, "Gaza", "Meningitis alert: 272 cases in Oct, 15 dead in 2026", "OFFICIAL"), (20, "DR Congo", "Missing Cessna 208, rebels claim shootdown", "CLAIM"), (21, "Hanoi", "Hot-pot explosion kills at least 6", "REPORTED"), (22, "Gulf of Finland", "Ukraine hits Russian ship Sparta II", "REPORTED"), (23, "Kuala Lumpur", "Malaysia to return thousands of migrants to Myanmar", "OFFICIAL"), (24, "Ulleungdo", "S. Korea shelter order as Russian jets enter ADIZ", "OFFICIAL"), (25, "Dhaka", "Hasina plans return on 16 Dec", "REPORTED"), (26, "The Hague", "14 nations endorse ICJ Myanmar ruling", "REPORTED"), (27, "Jakarta", "Indonesia nominates 2 VP candidates", "OFFICIAL"), (28, "Beijing", "China sentences official Ma to death for spying", "OFFICIAL"), (29, "Brussels", "NATO vows defence against space threat", "OFFICIAL"), (30, "Mexico City", "US drone aided El Chapo capture; Mexico to try him", "REPORTED"), (31, "San Salvador", "Bukele names 3 Salvadoran soldiers killed in Haiti", "OFFICIAL"), (32, "Ottawa", "Pentagon rebukes Canada: only 41.9% of air fleet ready", "REPORTED"), (33, "Washington", "US adds Megaspeed to trade blacklist", "OFFICIAL"), (34, "Kyiv", "Zelensky urges Ukraine / Russia / US / Europe talks soon", "REPORTED"), (35, "Ras Al Khaimah", "UAE bus-truck crash kills 13", "REPORTED"), (36, "London", "England record 5,258 heat deaths, summer 2026", "OFFICIAL"), (37, "Kourou", "Ariane 6 lofts 36 Amazon satellites", "OFFICIAL"), (38, "Cikande", "Factory-fire toll rises to 26", "REPORTED")]
PINS = [(1, 24.7, 46.7, 0, -14), (2, 31.2, 121.5, 0, -14), (3, 40.7, -74.0, 10, -16), (4, 47.8, 35.2, 0, -14), (5, 14.7, -17.4, 0, -14), (6, 26.5, 56.3, 12, -10), (7, 40.7, -74.0, -24, 10), (8, 47.7, -122.1, 0, -14), (9, 39.8, 30.5, 0, -14), (10, 10.4, -75.5, 0, -14), (11, 12.8, 45.0, 14, -12), (12, 13.0, 44.9, -22, 12), (13, 39.7, 98.5, 0, -14)]
LEGEND = ["1 Riyadh \u2014 PIF tower hit, 11 hurt", "2 Shanghai \u2014 Chen Jining probed", "3 New York \u2014 Huawei 10/12 guilty", "4 Zaporizhzhia \u2014 9 killed, 96 drones", "5 Senegal \u2014 AFCON title back", "6 Hormuz \u2014 container ship attacked", "7 New York \u2014 Dow 50,018", "8 Redmond \u2014 Microsoft \u2018Code Red\u2019", "9 Eskisehir \u2014 helicopter crash, 5 dead", "10 Cartagena \u2014 25 hostages", "11 Aden \u2014 Houthis 60 km away", "12 Lahj \u2014 Saudi strikes kill 25", "13 Jiuquan \u2014 first foreign astronaut"]

def main():
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 20], fill=RED); txt(d, 10, 4, "THE WORLD ON ONE PAGE", F(10, True), (255, 255, 255)); txt(d, W - 10, 4, "38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS", F(10, True), (255, 255, 255), anchor="ra")
    txt(d, 10, 24, "Tuesday 24 November 2026", F(30, True, True)); txt(d, W - 10, 34, "ONE DAY \u00b7 ONE PICTURE", F(10, True), RED, anchor="ra")
    txt(d, 10, 58, "Riyadh tower hit again \u00b7 Shanghai party chief probed \u00b7 Huawei guilty on 10 of 12 counts", F(11, False, True), RED)
    # Region bar: 6 coloured segments, counts sum to 38.
    regs = [("Europe 9", (30, 80, 160)), ("Middle East 8", (166, 25, 46)), ("Asia 8", (200, 120, 20)), ("Africa 2", (27, 120, 60)), ("Americas 7", (90, 60, 140)), ("World/Space 4", (90, 90, 90))]
    x = 10
    for label, col in regs:
        wseg = 168 if label != "World/Space 4" else 172
        d.rectangle([x, 76, x + wseg - 4, 96], fill=col); txt(d, x + wseg // 2, 81, label, F(9, True), (255, 255, 255), anchor="ma"); x += wseg
    # UTC strip.
    txt(d, 10, 102, "THE DAY IN UTC", F(9, True), RED)
    ux = 132
    for hh, ev in UTC:
        txt(d, ux, 102, hh, F(9, True)); txt(d, ux, 113, ev, F(7), GREY); ux += 110
    d.line([10, 128, W - 10, 128], fill=(200, 190, 170), width=1)
    # Numbers strip: 8 big numbers.
    txt(d, 10, 134, "THE DAY IN NUMBERS", F(9, True), RED); nx = 10
    for num, lab in NUMS:
        txt(d, nx, 148, num, F(17, True, True), RED); txt(d, nx, 168, lab, F(7), GREY); nx += 127
    # Heroes.
    for i, (kick, ch, head, deck, kind, src) in enumerate(HEROES):
        hx = 10 + i * 338; hw = 328
        d.rectangle([hx, 186, hx + hw, 372], outline=(180, 170, 150), width=1, fill=(255, 255, 255))
        scene(d, hx + 1, 187, hw - 2, 78, kind); txt(d, hx + 8, 272, kick, F(9, True), RED); chip(d, hx + 8, 286, ch); txt(d, hx + 8, 286, src, F(7), GREY) if False else None
        txt(d, hx + 96, 288, src, F(7), GREY)
        para(d, hx + 8, 302, head, F(12, True, True), hw - 16, 14); para(d, hx + 8, 332, deck, F(8), hw - 16, 11)
    # Cards grid 5+5.
    for i, (kick, ch, head, deck, kind, src) in enumerate(CARDS):
        cx = 10 + (i % 5) * 202; cy = 380 + (i // 5) * 112; cw = 194
        d.rectangle([cx, cy, cx + cw, cy + 106], outline=(180, 170, 150), width=1, fill=(255, 255, 255))
        scene(d, cx + 1, cy + 1, cw - 2, 30, kind); txt(d, cx + 6, cy + 34, kick, F(7, True), RED); _sx = chip(d, cx + 6, cy + 46, ch); txt(d, _sx, cy + 47, src, F(6), GREY)
        para(d, cx + 6, cy + 60, head, F(8, True, True), cw - 12, 10); para(d, cx + 6, cy + 80, deck, F(7), cw - 12, 9)
    return im, d

def draw_map(d):
    mx, my, mw, mh = 10, 606, 400, 200
    d.rectangle([mx, my, mx + mw, my + mh], outline=(180, 170, 150), width=1, fill=(235, 240, 245))
    def P(lon, lat): return (mx + (lon + 180) / 360 * mw, my + (90 - lat) / 180 * mh)
    for poly in (NA, SA, EU, AF, AS, AU):
        d.polygon([P(lon, lat) for lon, lat in poly], fill=LGREEN, outline=(90, 110, 70))
    d.text((mx + 6, my + 4), "WORLD MAP \u2014 PINS 1\u201313", font=F(8, True), fill=NAVY)
    for n, lat, lon, dx, dy in PINS:
        px, py = P(lon, lat); lx, ly = px + dx, py + dy
        if dx or dy: d.line([px, py, lx, ly], fill=RED, width=1)
        d.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=RED, outline=(255, 255, 255), width=1); d.text((lx, ly), str(n), font=F(8, True), fill=(255, 255, 255), anchor="mm")
    # Numbered legend beside the map.
    txt(d, 424, 606, "WHERE IT HAPPENED \u2014 1\u201313", F(9, True), RED)
    for i, leg in enumerate(LEGEND):
        lx = 424 + (i % 2) * 300; ly = 624 + (i // 2) * 25
        d.ellipse([lx, ly, lx + 14, ly + 14], fill=RED); d.text((lx + 7, ly + 7), str(i + 1), font=F(8, True), fill=(255, 255, 255), anchor="mm"); d.text((lx + 19, ly + 2), leg, font=F(8), fill=INK)
    txt(d, 424, 800, "Pins from real latitude / longitude. Redmond is on the US west coast, below Canada.", F(7), GREY)
def draw_also_date(d):
    txt(d, 10, 814, "ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES", F(9, True), RED)
    for j, (n, city, head, ch) in enumerate(ALSO):
        col = j // 9; row = j % 9; ax = 10 + col * 338; ay = 832 + row * 15
        c = CHIP.get(ch, (90, 90, 90)); d.rectangle([ax, ay + 1, ax + 34, ay + 11], fill=c); d.text((ax + 17, ay + 6), ch[:4], font=F(6, True), fill=(255, 255, 255), anchor="mm")
        d.text((ax + 38, ay), f"{n}. {city}: {head}", font=F(7), fill=INK)
    d.rectangle([10, 968, W - 10, 1008], outline=RED, width=2, fill=(255, 240, 240))
    txt(d, 14, 971, "DATE CHECK", F(9, True), RED)
    para(d, 14, 983, "Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claim (23 Nov); Nvidia Huang returns as CEO (23 Nov); EU 22nd sanctions package (23 Nov); COP31 ends with no deal (22 Nov); corvette Merkury sinks (22 Nov); El Chapo Isidro arrested (Fri 20 Nov); Cikande fire starts (Sat 21 Nov); F1 Las Vegas GP (Sat 21 Nov). NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC); MPR session picks VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns (16 Dec).", F(6), W - 28, 8)
    txt(d, 10, 1012, "Sources: dailysummaryof.com/world/2026-11-24 \u00b7 Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CMSA \u00b7 CCDI. CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side. Scenes are drawn illustrations, not photographs.", F(6), GREY)
if __name__ == "__main__":
    im, d = main(); draw_map(d); draw_also_date(d)
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png"); os.makedirs(os.path.dirname(out) or ".", exist_ok=True); im.save(out, optimize=True); print(out)
