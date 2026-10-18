#!/usr/bin/env python3
"""Week 10 — Renal & Urinary System (anatomy). MHHS2402. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/w10_renal"

SPEC = {
    "slug": "renal_urinary_anatomy_mhhs2402_wk10",
    "workdir": WD,
    "unit": "MHHS2402",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "week": 10,
    "title": "Renal & Urinary System — Anatomy",
    "source": "MHHS2402 Week 10 — Renal (Urinary) System anatomy (Macquarie University)",
    "brand": "MHHS2402 · Wk10 · Renal",
    "brandsub": "Renal &amp; Urinary<br>Anatomy",
    "eyebrow": "MHHS2402 · Cardiovascular, Renal &amp; Respiratory · Week 10",
    "h1": "Renal &amp; Urinary System — Anatomy",
    "h1thin": "from the whole kidney down to a single nephron",
    "lede": "Every lecture slide, shown in full and then explained the way a tutor would — the gross anatomy of the kidney and urinary tract, how it is wired and supplied, how it develops, and the nephron that does the actual work. Where the lecture left a blank to fill, the answer is written into the note beneath the slide.",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The text underneath is <b>not a re-caption</b> — it adds the mechanism, the reasoning and the clinical angle the slide leaves unsaid, and it <b>fills in every blank the lecture left open</b>. Work top-to-bottom: gross anatomy first, then supply and control, then the microscopic nephron where filtration begins.",
    "n_slides": 40,
    "sections": [
        {
            "id": "s0", "code": "§0", "lo": "Scope of the lecture",
            "title": "Learning objectives", "tag": "One organ, nine objectives — from surface landmarks to the nephron.",
            "lead": "The lecture walks the urinary tract top-down: what the kidney <em>does</em>, the gross anatomy of each organ, how it sits and is supplied, its nerves and development, and finally the nephron and the three steps of urine formation. Hold that arc and each slide slots into place.",
            "blocks": [
                ("plate", 1, "Learning objectives", "Learning objectives for the renal system lecture"),
                ("box", "active", "Orientation", "The kidney is fundamentally a <strong>homeostatic organ</strong> — it tunes the <em>plasma</em>, not just makes urine. Keep returning to one idea: it filters ~180 L of plasma a day and then selectively claws almost all of it back, so that what leaves the body is precisely what the body no longer wants. Every structure below exists to serve that filter-then-reclaim logic."),
            ],
        },
        {
            "id": "s1", "code": "§1", "lo": "Functions &amp; gross structure",
            "title": "Functions &amp; gross anatomy of the kidney", "tag": "What it does, where it sits, and how it is built inside.",
            "lead": "Before the plumbing, fix the kidney's <em>jobs</em> and its layered internal architecture — cortex, pyramids, calyces — because every later slide (supply, nephron, urine) maps onto this scaffold.",
            "blocks": [
                ("plate", 2, "Functions of the renal system", "The homeostatic functions of the kidney"),
                ("box", "why", "Why · it is an endocrine organ too", "Learn the functions as <strong>homeostasis, not just excretion</strong>. Beyond clearing nitrogenous waste (<strong>urea, uric acid, creatinine</strong>), the kidney sets <strong>blood volume/pressure</strong> (renin → the RAAS), guards <strong>electrolytes</strong> and <strong>acid-base</strong> (secreting H⁺, reclaiming HCO₃⁻), and acts as an <strong>endocrine gland</strong>: it secretes <strong>erythropoietin</strong> (EPO drives red-cell production when O₂ is low) and performs the final hydroxylation that turns vitamin D into active <strong>calcitriol</strong> for calcium absorption. That is why chronic kidney disease causes anaemia and bone disease, not just a rising creatinine."),
                ("grid", [
                    (3, "The kidney — overview", "Bean-shaped kidney that filters blood and makes urine"),
                    (4, "Position, levels &amp; the hilum", "Kidney position T12–L3 and the hilum contents"),
                ]),
                ("box", "mnem", "Exam hook · levels and the hilar order", "Kidneys sit <strong>retroperitoneally</strong>, spanning roughly <strong>T12–L3</strong> (about three vertebrae). The <strong>right kidney is lower</strong> — pushed down by the liver. At the <strong>hilum</strong>, learn the anterior-to-posterior order: <strong>Vein → Artery → Ureter (VAU)</strong>. The renal vein (most anterior) drains to the IVC; the renal artery branches off the aorta; the ureter leaves most posteriorly. The adrenal gland caps the superior pole but is a separate endocrine organ."),
                ("plate", 5, "Fascial &amp; fat layers", "Renal capsule, perirenal fat, renal fascia and pararenal fat"),
                ("box", "clin", "Clinical · why the layers matter", "From deep to superficial: <strong>renal capsule</strong> (tough fibrous coat) → <strong>perirenal fat</strong> → <strong>renal (Gerota's) fascia</strong>, which also encloses the adrenal → <strong>pararenal fat</strong> (mostly posterolateral). These layers <strong>suspend and cushion</strong> the kidney; lose the fat (rapid weight loss) and the kidney can drop — <em>nephroptosis</em>. The fascial planes also <strong>contain perinephric collections</strong> (blood, pus) and guide where infection tracks."),
                ("plate", 6, "Internal anatomy — cortex to calyces", "Cortex, medulla, pyramids, papillae, calyces and renal pelvis"),
                ("box", "why", "Why · follow a drop of urine out", "Trace the drainage and the internal map writes itself: <strong>cortex</strong> (outer) and <strong>medulla</strong> (inner) → medulla is packed into cone-shaped <strong>renal pyramids</strong> → each pyramid points to a <strong>renal papilla</strong> → papilla drips urine into a <strong>minor calyx</strong> → minor calyces merge into <strong>major calyces</strong> → major calyces funnel into the <strong>renal pelvis</strong> → <strong>ureter</strong>. <strong>Renal columns</strong> are cortex dipping between pyramids (they carry the interlobar vessels). This cortex-outside / pyramids-inside split is exactly where cortical vs juxtamedullary nephrons will live (§8)."),
            ],
            "recall": {"head": "Recall — functions &amp; gross anatomy", "items": [
                "<li><b>Kidney jobs —</b> clear <b>nitrogenous waste</b>, set <b>BP/volume</b> (renin), guard <b>electrolytes/pH</b>, make <b>EPO</b> and active <b>vitamin&nbsp;D</b></li>",
                "<li><b>Position —</b> retroperitoneal, <b>T12–L3</b>; the <b>right</b> kidney is lower (liver)</li>",
                "<li><b>Hilum order (ant→post) —</b> <b>vein</b>, <b>artery</b>, <b>ureter</b> (VAU)</li>",
                "<li><b>Coverings (deep→superficial) —</b> capsule, <b>perirenal fat</b>, renal fascia, <b>pararenal fat</b></li>",
                "<li><b>Urine path out —</b> papilla → <b>minor calyx</b> → major calyx → <b>renal pelvis</b> → ureter</li>",
            ]},
            "digest": {
                "key_points": [
                    "The kidney is a homeostatic + endocrine organ: clears urea/uric acid/creatinine, regulates volume/BP (renin, RAAS), electrolytes and acid-base, and secretes erythropoietin and activates vitamin D to calcitriol.",
                    "Kidneys are retroperitoneal, span ~T12–L3; the right kidney sits lower because of the liver.",
                    "Hilum structures anterior to posterior: renal vein, renal artery, ureter (VAU).",
                    "Coverings deep to superficial: renal capsule, perirenal fat, renal (Gerota's) fascia, pararenal fat.",
                    "Internal drainage: renal pyramid → papilla → minor calyx → major calyx → renal pelvis → ureter; renal columns are cortex between pyramids.",
                ],
                "self_tests": [
                    {"q": "Name two endocrine products of the kidney and their roles.", "a": "Erythropoietin (stimulates red-cell production) and calcitriol (active vitamin D, for calcium absorption); renin is also released as an enzyme controlling the RAAS."},
                    {"q": "Give the anterior-to-posterior order of structures at the renal hilum.", "a": "Renal vein (anterior), renal artery, ureter (posterior) — 'VAU'."},
                    {"q": "Why does the right kidney lie lower than the left?", "a": "It is displaced inferiorly by the liver."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "The conducting tract",
            "title": "Ureters, bladder &amp; urethra", "tag": "The plumbing that stores and delivers urine — and its sex differences.",
            "lead": "Urine is made in the kidney but <em>handled</em> by muscular tubes and a reservoir. The clinically important points are the ureteric constriction sites, the bladder's trigone and sphincters, and why the male and female urethra behave so differently.",
            "blocks": [
                ("plate", 7, "Ureters", "Ureters: muscular tubes running on psoas major to the bladder"),
                ("box", "clin", "Clinical · peristalsis and stone sites", "Ureters are <strong>25–30 cm</strong> smooth-muscle tubes that <strong>actively peristalse</strong> urine — they don't rely on gravity, which is why you can urinate lying down. They run <strong>on psoas major</strong>, anterior to its surface, cross the <strong>sacroiliac joint / pelvic brim</strong>, and turn <strong>inferomedially</strong> into the bladder. Three natural <strong>constrictions</strong> trap kidney stones: the <strong>ureteropelvic junction</strong>, the <strong>pelvic brim</strong> (crossing the iliac vessels), and the <strong>ureterovesical junction</strong> — the narrowest. A stone impacting here gives classic colicky <em>loin-to-groin</em> pain (§6)."),
                ("grid", [
                    (8, "Urinary bladder — position", "Bladder posterior to pubic symphysis, anterior to uterus in females"),
                    (9, "Bladder — male vs female relations", "Bladder relations differ by sex: uterus vs rectum/prostate"),
                ]),
                ("box", "mnem", "Exam hook · the bladder's neighbours", "A hollow muscular reservoir holding <strong>~400–600 mL</strong>. It sits <strong>behind the pubic symphysis</strong> (separated by the retropubic fat space). <strong>Females:</strong> anterior to the <strong>uterus/vagina</strong>. <strong>Males:</strong> anterior to the <strong>rectum</strong> and <strong>superior to the prostate</strong> — the reason prostate enlargement (BPH) throttles bladder outflow."),
                ("plate", 10, "Bladder wall &amp; sphincters", "Detrusor muscle, rugae, internal and external urethral sphincters"),
                ("box", "why", "Why · two sphincters, two kinds of control", "The wall is the <strong>detrusor</strong> (interlacing smooth muscle) lined by <strong>rugae</strong> that flatten as it fills, and <strong>mechanoreceptors</strong> that sense stretch. Guarding the outlet are <em>two</em> sphincters with opposite wiring: the <strong>internal urethral sphincter</strong> (smooth muscle, <strong>involuntary</strong>, autonomic) and the <strong>external urethral sphincter</strong> (skeletal muscle, <strong>voluntary</strong>, pudendal nerve). That split is the whole basis of the micturition reflex in §6."),
                ("plate", 11, "The trigone", "Trigone: triangle between two ureteric orifices and the internal urethral orifice"),
                ("box", "clin", "Clinical · why cystitis hurts here", "The <strong>trigone</strong> is the smooth triangle on the <strong>posterior-inferior</strong> wall, bounded by the <strong>two ureteric orifices</strong> and the <strong>internal urethral orifice</strong>. It is <strong>developmentally distinct</strong> (mesodermal) and rich in <strong>sensory afferents</strong>, so it is exquisitely sensitive to <strong>stretch and irritation</strong> — the focus of the urge to void and the trigger zone for the burning discomfort of a UTI."),
                ("grid", [
                    (12, "Female urethra", "Short (~4 cm) straight female urethra, prone to UTI"),
                    (13, "Male urethra", "Long (18–20 cm) male urethra carrying urine and semen"),
                ]),
                ("box", "mnem", "Exam hook · why women get more UTIs — and the 4 male parts", "The <strong>female urethra</strong> is <strong>~4 cm, straight</strong>, opening in the vestibule — short and close to the anus, so bacteria ascend easily (<strong>more UTIs</strong>), but it is easy to catheterise. The <strong>male urethra</strong> is <strong>18–20 cm</strong> with bends and carries <em>urine and semen</em> (never together). Learn its four parts in order: <strong>Pre-prostatic → Prostatic → Membranous → Spongy (penile)</strong> — mnemonic <em>\"Please Pee Many Seconds.\"</em> The <strong>membranous</strong> part is where the <strong>voluntary external sphincter</strong> sits, and the narrow membranous/bulbar region is the classic site of traumatic rupture and difficult catheterisation."),
                ("plate", 17, "Male urethra — the four parts", "Pre-prostatic, prostatic, membranous and spongy urethra"),
                ("box", "why", "Why · the prostatic part is a crossroads", "The <strong>prostatic urethra</strong> is the plumbing junction of the male pelvis: it receives the <strong>ejaculatory ducts</strong> (sperm + seminal vesicle fluid) and the <strong>prostatic ducts</strong> (alkaline prostatic secretion). This is why <strong>prostate pathology</strong> — BPH or cancer — presents with <em>both</em> urinary obstruction and effects on ejaculation, and why the gland is palpated per rectum just behind it."),
            ],
            "recall": {"head": "Recall — the conducting tract", "items": [
                "<li><b>Ureter stone sites —</b> <b>ureteropelvic</b> junction, <b>pelvic brim</b> (iliac vessels), <b>ureterovesical</b> junction</li>",
                "<li><b>Ureters move urine by —</b> <b>peristalsis</b> (smooth muscle), not gravity</li>",
                "<li><b>Internal sphincter —</b> <b>smooth</b> muscle, <b>involuntary</b>; external = <b>skeletal</b>, <b>voluntary</b> (pudendal)</li>",
                "<li><b>Trigone —</b> between <b>2 ureteric orifices</b> + <b>1 internal urethral orifice</b>; <b>sensory</b>-rich</li>",
                "<li><b>Female urethra —</b> <b>~4 cm</b>, straight → <b>more UTIs</b>; easy to catheterise</li>",
                "<li><b>Male urethra parts —</b> <b>pre-prostatic</b> → <b>prostatic</b> → <b>membranous</b> → <b>spongy</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Ureters are 25–30 cm smooth-muscle tubes moving urine by peristalsis; three constriction sites (ureteropelvic junction, pelvic brim/iliac vessels, ureterovesical junction) are where stones impact.",
                    "Bladder holds ~400–600 mL; wall = detrusor smooth muscle with rugae and stretch mechanoreceptors.",
                    "Two sphincters: internal urethral (smooth, involuntary, autonomic) and external urethral (skeletal, voluntary, pudendal nerve).",
                    "Trigone is the sensory-rich triangle between the two ureteric orifices and the internal urethral orifice.",
                    "Female urethra ~4 cm and straight (prone to UTI, easy to catheterise); male urethra 18–20 cm with four parts: pre-prostatic, prostatic, membranous, spongy.",
                ],
                "self_tests": [
                    {"q": "Name the three ureteric constriction sites where stones lodge.", "a": "Ureteropelvic junction, the pelvic brim where it crosses the iliac vessels, and the ureterovesical junction."},
                    {"q": "Contrast the internal and external urethral sphincters.", "a": "Internal = smooth muscle, involuntary (autonomic); external = skeletal muscle, voluntary (pudendal nerve, S2–S4)."},
                    {"q": "List the four parts of the male urethra in order.", "a": "Pre-prostatic, prostatic, membranous, spongy (penile)."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "Surface anatomy &amp; relations",
            "title": "Surface anatomy &amp; anatomical relations", "tag": "What each organ touches — the key to referred signs and surgical hazard.",
            "lead": "Relations are tested because they explain clinical signs: where kidney pain projects, which organs a tumour invades, and which structures a surgeon must respect. This is also where the lecture's ureter blanks get filled.",
            "blocks": [
                ("grid", [
                    (18, "Anterior relations", "Anterior peritoneal relations of the right and left kidney"),
                    (19, "Posterior relations", "Posterior muscular relations and the costodiaphragmatic recess"),
                ]),
                ("box", "mnem", "Exam hook · anterior differs, posterior is shared", "<strong>Anterior</strong> relations differ by side — <strong>Right:</strong> liver, duodenum (2nd part), right colic flexure; <strong>Left:</strong> stomach, spleen, pancreas, jejunum, left colic flexure. <strong>Posterior</strong> relations are the <em>same bed</em> on both sides: <strong>diaphragm, psoas major, quadratus lumborum, transversus abdominis</strong>, crossed by the <strong>subcostal, iliohypogastric and ilioinguinal nerves</strong>. Because the upper poles sit under the diaphragm against the <strong>pleura</strong>, a posterior (loin) approach to the kidney risks a <strong>pneumothorax</strong>."),
                ("plate", 20, "Ureter relations — “water under the bridge”", "Ureter course and its relation to gonadal vessels and uterine artery"),
                ("box", "clin", "Clinical · the blanks filled — and the surgical trap", "Here are the lecture's answers: the ureter forms at the narrowing of the <strong>renal pelvis</strong> (ureteropelvic junction); it runs <strong>anterior to psoas major</strong>, <strong>posterior to the gonadal vessels</strong>, and <strong>anterior to the iliac vessels</strong> at the pelvic brim. The money point is <strong>“water under the bridge”</strong>: the <strong>ureter (water) passes inferior/posterior to the uterine artery (bridge)</strong> in females — and under the <strong>ductus deferens</strong> in males. In hysterectomy, clamping the uterine artery can accidentally <strong>ligate the ureter</strong> — a classic exam and operating-theatre hazard."),
                ("plate", 21, "Bladder relations", "Bladder relations on its superior, posterior, inferior and anterior surfaces"),
                ("box", "why", "Why · a pelvic organ reporting to its neighbours", "Read the bladder by surface: <strong>superior</strong> is peritoneal (bowel/sigmoid above, uterus in females); the <strong>posterior base</strong> faces the <strong>seminal vesicles/vas and rectum</strong> (males) or <strong>cervix and vagina</strong> (females); the <strong>neck</strong> rests on the pelvic floor and, in males, on the <strong>prostate</strong>; <strong>anterior</strong> is the pubic symphysis with the retropubic fat space. These relations are exactly the planes a bladder tumour spreads along and a surgeon dissects."),
            ],
            "recall": {"head": "Recall — relations", "items": [
                "<li><b>Posterior bed (both kidneys) —</b> <b>diaphragm</b>, <b>psoas major</b>, <b>quadratus lumborum</b>, transversus abdominis</li>",
                "<li><b>Upper pole risk —</b> lies against <b>pleura</b> → loin approach can cause <b>pneumothorax</b></li>",
                "<li><b>Ureter vs psoas / gonadal / iliac —</b> <b>anterior</b> to psoas, <b>posterior</b> to gonadal vessels, <b>anterior</b> to iliac vessels</li>",
                "<li><b>“Water under the bridge” —</b> ureter runs <b>under</b> the <b>uterine artery</b> (or ductus deferens)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Anterior kidney relations differ by side (right: liver, duodenum, right colic flexure; left: stomach, spleen, pancreas, jejunum, left colic flexure); posterior bed is shared: diaphragm, psoas major, quadratus lumborum, transversus abdominis.",
                    "Upper poles abut the pleura, so a posterior renal approach risks pneumothorax.",
                    "Ureter runs anterior to psoas, posterior to gonadal vessels, anterior to the iliac vessels at the pelvic brim, and forms at the renal pelvis (ureteropelvic junction).",
                    "'Water under the bridge': the ureter passes inferior to the uterine artery (females) / ductus deferens (males) — a key hazard in pelvic surgery.",
                ],
                "self_tests": [
                    {"q": "What does 'water under the bridge' describe, and why does it matter clinically?", "a": "The ureter (water) passes beneath the uterine artery (bridge); during hysterectomy, clamping the uterine artery can accidentally ligate the ureter."},
                    {"q": "Name the muscles of the posterior renal bed.", "a": "Diaphragm, psoas major, quadratus lumborum, and transversus abdominis."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "The adrenal glands",
            "title": "Adrenal (suprarenal) glands", "tag": "Two endocrine organs stacked in one gland on top of the kidney.",
            "lead": "The adrenal shares the kidney's fascia but is functionally separate. The exam points are the cortex-vs-medulla division and the “salt, sugar, sex” zonation of the cortex.",
            "blocks": [
                ("plate", 22, "Adrenal glands — overview", "Triangular suprarenal glands with outer cortex and inner medulla"),
                ("box", "why", "Why · one gland, two embryological origins", "The adrenal is really <em>two glands</em>: an outer <strong>cortex</strong> (mesodermal, makes steroid hormones) wrapped around an inner <strong>medulla</strong> (neural-crest derived, essentially a modified sympathetic ganglion). That dual origin explains the two totally different hormone classes below — <strong>steroids</strong> from the cortex, <strong>catecholamines</strong> from the medulla."),
                ("plate", 23, "Adrenal cortex — salt, sugar, sex", "Zona glomerulosa, fasciculata and reticularis of the adrenal cortex"),
                ("box", "mnem", "Exam hook · “GFR — salt, sugar, sex”", "Three cortical zones, outer to inner: <strong>Glomerulosa → Fasciculata → Reticularis</strong> (“GFR”), making <strong>Salt, Sugar, Sex</strong>. <strong>Mineralocorticoids (aldosterone)</strong> — the salt hormone, retaining Na⁺/water to raise BP (the end-point of the RAAS the kidney starts). <strong>Glucocorticoids (cortisol)</strong> — metabolic and immunosuppressive. <strong>Weak androgens</strong> — precursors to sex steroids. “The deeper you go, the sweeter it gets”."),
                ("plate", 24, "Adrenal medulla — catecholamines", "Adrenal medulla secreting adrenaline and noradrenaline in fight-or-flight"),
                ("box", "clin", "Clinical · the medulla and phaeochromocytoma", "The <strong>medulla</strong> dumps <strong>adrenaline</strong> (↑heart rate, bronchodilation, ↑blood glucose) and <strong>noradrenaline</strong> (vasoconstriction, ↑BP) straight into the blood during the <strong>sympathetic fight-or-flight</strong> response — a hormonal amplifier of the sympathetic nervous system. A catecholamine-secreting medullary tumour, <strong>phaeochromocytoma</strong>, causes episodic <strong>hypertension, palpitations, sweating and headache</strong> — the classic exam vignette."),
            ],
            "recall": {"head": "Recall — adrenal glands", "items": [
                "<li><b>Two parts —</b> <b>cortex</b> (steroids, mesoderm) around <b>medulla</b> (catecholamines, neural crest)</li>",
                "<li><b>Cortex zones (GFR) —</b> <b>glomerulosa</b> → fasciculata → <b>reticularis</b> = <b>salt, sugar, sex</b></li>",
                "<li><b>Aldosterone —</b> retains <b>Na⁺/water</b> → raises <b>BP</b> (RAAS end-point)</li>",
                "<li><b>Medulla hormones —</b> <b>adrenaline</b> &amp; <b>noradrenaline</b>; tumour = <b>phaeochromocytoma</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The adrenal has an outer cortex (steroid hormones, mesodermal) and inner medulla (catecholamines, neural-crest / modified sympathetic ganglion).",
                    "Cortex zones outer-to-inner: glomerulosa, fasciculata, reticularis ('GFR') making salt (mineralocorticoids/aldosterone), sugar (glucocorticoids/cortisol), sex (weak androgens).",
                    "Aldosterone retains sodium and water to raise blood pressure — the effector arm of the RAAS the kidney initiates.",
                    "Medulla releases adrenaline and noradrenaline in fight-or-flight; a secreting tumour is a phaeochromocytoma.",
                ],
                "self_tests": [
                    {"q": "Give the three cortical zones and the hormone class each produces.", "a": "Zona glomerulosa → mineralocorticoids (aldosterone); zona fasciculata → glucocorticoids (cortisol); zona reticularis → weak androgens ('salt, sugar, sex')."},
                    {"q": "Why is the adrenal medulla considered part of the sympathetic nervous system?", "a": "It is a modified sympathetic ganglion (neural-crest derived) that releases catecholamines into the blood on sympathetic (nicotinic) stimulation."},
                ],
            },
        },
        {
            "id": "s5", "code": "§5", "lo": "Blood supply",
            "title": "Blood supply &amp; the vascular pathway", "tag": "From aorta to glomerulus and back — and the asymmetries that cause disease.",
            "lead": "The kidney receives ~20–25% of cardiac output. The lecture tests two things: the <em>named sequence</em> of vessels from aorta to nephron, and the left/right asymmetries (why the left renal vein is long and vulnerable). Several lecture blanks are answered here.",
            "blocks": [
                ("plate", 25, "Arterial supply, venous return &amp; the asymmetries", "Renal arteries from the aorta and veins to the IVC with length differences"),
                ("box", "clin", "Clinical · the blanks filled — length asymmetry and nutcracker", "The aorta lies <em>left</em> of midline and the IVC <em>right</em>, which sets up the asymmetry the lecture asks about. The <strong>right renal artery is longer</strong> (it must cross behind the IVC to reach the right kidney). The <strong>left renal vein is longer</strong> (it crosses the midline, <strong>anterior to the aorta and under the SMA</strong>) — where it can be squeezed in <strong>“nutcracker” syndrome</strong>. “What else drains via the renal veins?” On the left, the <strong>left gonadal and left suprarenal veins</strong> drain into the left renal vein; on the right they drain directly into the IVC. This is why a <strong>left-sided varicocele</strong> is the one that flags renal-vein obstruction."),
                ("plate", 26, "Anatomical variation", "Accessory and early-branching renal arteries as normal variants"),
                ("box", "why", "Why · variation is the rule, not the exception", "Accessory renal arteries and early branching are <strong>common normal variants</strong> because the kidney “picks up” successive arteries as it ascends in development (§7). It matters practically: renal arteries are <strong>end-arteries</strong> with little collateral, so an unrecognised accessory artery divided in surgery (or a donor kidney) means an <strong>infarcted segment</strong>."),
                ("grid", [
                    (27, "Anterior &amp; posterior divisions", "Renal artery splits into anterior (75%) and posterior (25%) divisions"),
                    (28, "Segmental arteries", "Five segmental arteries define surgical segments of the kidney"),
                ]),
                ("box", "mnem", "Exam hook · segments are surgical territories", "At the hilum the renal artery splits into an <strong>anterior division (~75% of flow)</strong> and a <strong>posterior division (~25%)</strong>, giving <strong>five segmental arteries</strong> (superior, anterior-superior, anterior-inferior, inferior from the anterior division; posterior from the posterior division). Each supplies an independent <strong>segment with no collateral</strong>, so segments are the units of partial nephrectomy. <strong>Brödel's bloodless line</strong> — the relatively avascular plane between anterior and posterior supply — is where the kidney is incised."),
                ("plate", 29, "The full vascular pathway", "Sequence of renal vessels from segmental arteries to the glomerulus and vasa recta"),
                ("box", "why", "Why · learn the chain to the glomerulus", "Memorise the sequence top-down: <strong>renal → segmental → interlobar (in the columns) → arcuate (arching over the pyramid bases) → interlobular/cortical radiate → afferent arteriole → glomerulus → efferent arteriole</strong>. The <strong>efferent</strong> vessel is the twist that makes the kidney unique: it leaves the glomerulus and <em>re-branches</em> into a <strong>second capillary bed</strong> — <strong>peritubular capillaries</strong> (around cortical tubules) or the long <strong>vasa recta</strong> (diving beside juxtamedullary loops). Two capillary beds in series = <strong>filter first, then reclaim</strong>, the structural basis of all of §9."),
                ("plate", 30, "Venous return, the SMA &amp; nutcracker", "Left renal vein crossing between the SMA and aorta"),
                ("box", "clin", "Clinical · why the left side is vulnerable", "Venous flow retraces the arterial names (interlobular → arcuate → interlobar → segmental → renal → IVC). The vulnerability is the <strong>left renal vein's long course between the SMA and aorta</strong>: compression there (<strong>nutcracker syndrome</strong>) raises left renal and gonadal venous pressure → <strong>flank pain, haematuria, left varicocele</strong>. Keep this paired with the length asymmetry from the first slide of this section."),
            ],
            "recall": {"head": "Recall — blood supply", "items": [
                "<li><b>Vascular chain —</b> renal → <b>segmental</b> → interlobar → <b>arcuate</b> → interlobular → <b>afferent</b> → glomerulus → <b>efferent</b></li>",
                "<li><b>Unique feature —</b> <b>efferent arteriole</b> feeds a <b>second</b> capillary bed (peritubular / <b>vasa recta</b>)</li>",
                "<li><b>Longer vessels —</b> <b>right renal artery</b> (behind IVC); <b>left renal vein</b> (crosses aorta)</li>",
                "<li><b>Nutcracker —</b> left renal vein squeezed between <b>SMA</b> and <b>aorta</b></li>",
                "<li><b>Divisions —</b> anterior <b>75%</b>, posterior <b>25%</b> → <b>five</b> segmental arteries (end-arteries)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Vascular sequence: renal → segmental → interlobar → arcuate → interlobular (cortical radiate) → afferent arteriole → glomerulus → efferent arteriole → peritubular capillaries or vasa recta.",
                    "The efferent arteriole feeds a second capillary bed (two capillary beds in series) — the basis of filtration then reabsorption.",
                    "Right renal artery is longer (crosses behind IVC); left renal vein is longer (crosses anterior to aorta, under SMA) and receives the left gonadal and left suprarenal veins.",
                    "Left renal vein compression between SMA and aorta = nutcracker syndrome (flank pain, haematuria, left varicocele).",
                    "Renal artery divides into anterior (~75%) and posterior (~25%) divisions giving five segmental end-arteries; Brödel's line is the avascular surgical plane.",
                ],
                "self_tests": [
                    {"q": "Trace a red cell from the renal artery to the glomerulus, naming each vessel.", "a": "Renal → segmental → interlobar → arcuate → interlobular (cortical radiate) → afferent arteriole → glomerulus."},
                    {"q": "Why is the left renal vein clinically vulnerable, and what drains into it?", "a": "It runs a long course between the SMA and aorta (nutcracker compression); it receives the left gonadal and left suprarenal veins (which on the right drain directly to the IVC)."},
                    {"q": "What is unusual about the efferent arteriole compared with most capillary drainage?", "a": "It drains the glomerulus into a second capillary bed (peritubular capillaries or vasa recta) rather than into a vein — two capillary beds in series."},
                ],
            },
        },
        {
            "id": "s6", "code": "§6", "lo": "Innervation &amp; micturition",
            "title": "Innervation, referred pain &amp; the micturition reflex", "tag": "Autonomic storage, parasympathetic voiding, and why stones hurt loin-to-groin.",
            "lead": "Bladder control is a tug-of-war: sympathetic stores, parasympathetic voids, somatic nerve holds the voluntary gate. Get the storage-vs-voiding wiring and referred-pain levels and this section is done. Two lecture blanks are answered.",
            "blocks": [
                ("plate", 31, "Kidney &amp; ureter innervation — referred pain", "Renal plexus sympathetic supply and loin-to-groin referred pain"),
                ("box", "clin", "Clinical · loin-to-groin, and the CN X blank", "Sympathetic fibres reach the kidney/ureter via the <strong>renal plexus (T10–L2)</strong>, controlling renal blood flow and renin release; the parasympathetic contribution is from the <strong>vagus nerve (CN X)</strong> — the lecture's blank. Because <strong>visceral afferents run back with the sympathetics (T10–L2)</strong>, ureteric colic is <em>referred</em> to those dermatomes — the classic <strong>“loin to groin”</strong> pain radiating to the flank, lower abdomen and scrotum/labia as a stone moves down the ureter."),
                ("plate", 32, "Bladder innervation", "Sympathetic storage, parasympathetic voiding and somatic sphincter control"),
                ("box", "why", "Why · the storage blanks filled", "Fill the lecture's blanks with the storage logic: <strong>sympathetic (hypogastric, T11–L2) → RELAX the detrusor and CONTRACT the internal sphincter</strong> = <em>store</em> urine. The opposite system, <strong>parasympathetic (pelvic splanchnics, S2–S4) → CONTRACT the detrusor and RELAX the internal sphincter</strong> = <em>void</em>. The <strong>pudendal nerve (S2–S4, somatic)</strong> holds the <strong>external sphincter</strong> shut for voluntary control. Mnemonic: <em>sympathetic = Storage, paraSympathetic = Squeeze-out</em> (“point &amp; shoot: Parasympathetic Points, Sympathetic Shoots” for the reproductive analogue)."),
                ("plate", 33, "The micturition reflex", "Spinal filling reflex and the pontine micturition centre"),
                ("box", "mnem", "Exam hook · the reflex and its brake", "<strong>Filling:</strong> low-level stretch signals (S2–S4) keep sympathetic storage and the pudendal brake active. <strong>Voiding:</strong> once volume is high, strong afferents drive the <strong>pontine micturition centre (PMC)</strong>, which switches on <strong>parasympathetic (S2–S4)</strong> → detrusor contracts, internal sphincter relaxes, and the PMC <strong>inhibits the pudendal nerve</strong> so the external sphincter opens. The <strong>cerebral cortex</strong> sits on top, postponing voiding until it is socially appropriate — which is why a spinal cord lesion <em>above</em> the sacral centre gives an uninhibited <strong>reflex (spastic) bladder</strong>."),
            ],
            "recall": {"head": "Recall — innervation &amp; micturition", "items": [
                "<li><b>Kidney parasympathetic —</b> <b>vagus</b> (CN <b>X</b>); afferents ride <b>sympathetics</b> (T10–L2)</li>",
                "<li><b>Ureteric colic refers —</b> <b>loin to groin</b> (T10–L2 dermatomes)</li>",
                "<li><b>Sympathetic bladder —</b> <b>relax</b> detrusor, <b>contract</b> internal sphincter = <b>store</b></li>",
                "<li><b>Parasympathetic bladder (S2–S4) —</b> <b>contract</b> detrusor, <b>relax</b> internal sphincter = <b>void</b></li>",
                "<li><b>External sphincter —</b> <b>pudendal</b> nerve; voiding switch = <b>pontine micturition centre</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Kidney/ureter sympathetic supply is the renal plexus (T10–L2); parasympathetic is the vagus (CN X); visceral afferents travel with the sympathetics.",
                    "Ureteric colic refers 'loin to groin' because afferents enter at T10–L2 dermatomes.",
                    "Storage = sympathetic (hypogastric T11–L2): relax detrusor, contract internal sphincter. Voiding = parasympathetic (pelvic splanchnic S2–S4): contract detrusor, relax internal sphincter.",
                    "External urethral sphincter = pudendal nerve (S2–S4, voluntary).",
                    "Voiding is coordinated by the pontine micturition centre; the cortex provides voluntary postponement.",
                ],
                "self_tests": [
                    {"q": "Which autonomic division stores urine and what does it do to the detrusor and internal sphincter?", "a": "Sympathetic (hypogastric, T11–L2): relaxes the detrusor and contracts the internal urethral sphincter."},
                    {"q": "Why does a ureteric stone cause loin-to-groin pain?", "a": "Ureteric visceral afferents travel with sympathetic fibres entering the cord at T10–L2, so pain is referred to those dermatomes (flank to groin/scrotum/labia)."},
                ],
            },
        },
        {
            "id": "s7", "code": "§7", "lo": "Development",
            "title": "Development &amp; common anomalies", "tag": "Three kidneys in succession — and what goes wrong when ascent or fusion fails.",
            "lead": "Renal embryology is tested through its anomalies. The one framework: three successive systems from intermediate mesoderm, with the metanephros becoming the definitive kidney as it ascends and rotates.",
            "blocks": [
                ("plate", 34, "Three successive renal systems", "Pronephros, mesonephros and metanephros from intermediate mesoderm"),
                ("box", "why", "Why · the ureteric bud is the key inducer", "The urinary system arises from <strong>intermediate mesoderm</strong> (the nephrogenic cord) as <strong>three systems in sequence</strong>: the <strong>pronephros</strong> (transient, non-functional), the <strong>mesonephros</strong> (temporary; its duct is reused by the male genital system), and the <strong>metanephros</strong> — the definitive kidney. The <strong>ureteric bud</strong> induces the metanephric blastema to form nephrons and itself becomes the collecting system (ureter, pelvis, calyces, collecting ducts). <strong>No bud, no kidney</strong> — bud problems explain most anomalies below. The kidney forms in the pelvis and <strong>ascends</strong>, picking up new arteries as it rises (why accessory arteries are common, §5)."),
                ("plate", 35, "Developmental anomalies", "Agenesis, ectopic, horseshoe and supernumerary kidney anomalies"),
                ("box", "clin", "Clinical · horseshoe kidney and friends", "<strong>Unilateral agenesis</strong> (absent ureteric bud) is survivable; <strong>bilateral</strong> is incompatible with life (Potter sequence). <strong>Ectopic</strong> kidney = failed ascent; <strong>malrotation</strong> = failed rotation; a <strong>duplicated/bifid ureter</strong> follows a split bud. The exam favourite is the <strong>horseshoe kidney</strong> — the most common fusion anomaly (~0.2%), where the lower poles fuse and the ascending kidney is <strong>trapped under the inferior mesenteric artery</strong>, so it stays low. Horseshoe kidneys predispose to <strong>obstruction, stones and infection</strong>."),
            ],
            "recall": {"head": "Recall — development", "items": [
                "<li><b>Origin —</b> <b>intermediate mesoderm</b> (nephrogenic cord)</li>",
                "<li><b>Three systems —</b> <b>pronephros</b> → <b>mesonephros</b> → <b>metanephros</b> (definitive kidney)</li>",
                "<li><b>Inducer —</b> the <b>ureteric bud</b> forms the <b>collecting system</b>; no bud = <b>agenesis</b></li>",
                "<li><b>Horseshoe kidney —</b> fused lower poles trapped under the <b>inferior mesenteric artery</b></li>",
                "<li><b>Bilateral agenesis —</b> <b>incompatible with life</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Urinary system develops from intermediate mesoderm (nephrogenic cord) as three successive systems: pronephros (transient), mesonephros (temporary), metanephros (definitive kidney).",
                    "The ureteric bud induces nephron formation and becomes the collecting system (ureter, pelvis, calyces, collecting ducts); absent bud causes renal agenesis.",
                    "The kidney ascends from the pelvis and picks up successive arteries (accessory renal arteries are common).",
                    "Horseshoe kidney (fused lower poles) is the commonest fusion anomaly and is trapped beneath the inferior mesenteric artery; bilateral agenesis is incompatible with life.",
                ],
                "self_tests": [
                    {"q": "What does the ureteric bud give rise to, and what happens if it fails to form?", "a": "The collecting system (ureter, renal pelvis, calyces, collecting ducts); failure causes renal agenesis on that side."},
                    {"q": "Why does a horseshoe kidney remain abnormally low?", "a": "Its fused lower poles catch on the inferior mesenteric artery during ascent."},
                ],
            },
        },
        {
            "id": "s8", "code": "§8", "lo": "The nephron",
            "title": "The nephron", "tag": "The functional unit — and why two nephron types exist.",
            "lead": "Everything so far was plumbing; the nephron is the machine. Fix its parts and the cortical-vs-juxtamedullary split, because the latter is the whole reason the kidney can concentrate urine.",
            "blocks": [
                ("grid", [
                    (36, "The nephron — where it sits", "Nephron spanning cortex and medulla, ~1–1.5 million per kidney"),
                    (37, "Parts of the nephron", "Renal corpuscle, PCT, loop of Henle, DCT and collecting duct"),
                ]),
                ("box", "why", "Why · learn the parts as a journey of filtrate", "Each kidney holds <strong>~1–1.5 million nephrons</strong>, spanning cortex and medulla. Follow the filtrate: <strong>renal corpuscle</strong> (glomerulus + Bowman's capsule — where filtration happens) → <strong>proximal convoluted tubule</strong> (bulk reabsorption) → <strong>loop of Henle</strong> (sets up the medullary gradient) → <strong>distal convoluted tubule</strong> (hormone-tuned fine control) → <strong>collecting duct</strong> (final water handling under ADH). Corpuscle and convoluted tubules sit in the <strong>cortex</strong>; the loop and collecting duct dive into the <strong>medullary pyramids</strong> — exactly matching the gross anatomy of §1."),
                ("plate", 38, "Cortical vs juxtamedullary nephrons", "Short-looped cortical and long-looped juxtamedullary nephrons"),
                ("box", "mnem", "Exam hook · the two nephron types", "<strong>Cortical nephrons (~80–85%)</strong> sit in the outer cortex with <strong>short loops</strong> and peritubular capillaries — they do routine <strong>filtration and reabsorption</strong>. <strong>Juxtamedullary nephrons (~15–20%)</strong> sit at the corticomedullary junction with <strong>long loops reaching deep into the medulla</strong>, paralleled by the <strong>vasa recta</strong>. These are the ones that <strong>build and maintain the medullary osmotic gradient</strong>, giving the kidney its power to <strong>concentrate urine</strong>. Short loop = routine; long loop = concentrating."),
            ],
            "recall": {"head": "Recall — the nephron", "items": [
                "<li><b>Count —</b> <b>~1–1.5 million</b> nephrons per kidney</li>",
                "<li><b>Filtrate journey —</b> <b>corpuscle</b> → <b>PCT</b> → <b>loop of Henle</b> → <b>DCT</b> → <b>collecting duct</b></li>",
                "<li><b>Cortical (80–85%) —</b> <b>short</b> loops; routine filtration/reabsorption</li>",
                "<li><b>Juxtamedullary (15–20%) —</b> <b>long</b> loops + <b>vasa recta</b> → build the <b>medullary gradient</b></li>",
                "<li><b>Concentrating urine needs —</b> the <b>long-looped</b> juxtamedullary nephrons</li>",
            ]},
            "digest": {
                "key_points": [
                    "Each kidney has ~1–1.5 million nephrons spanning cortex and medulla.",
                    "Filtrate path: renal corpuscle (glomerulus + Bowman's capsule) → proximal convoluted tubule → loop of Henle → distal convoluted tubule → collecting duct.",
                    "Cortical nephrons (~80–85%) have short loops and do routine filtration/reabsorption.",
                    "Juxtamedullary nephrons (~15–20%) have long loops with vasa recta and build the medullary osmotic gradient that lets the kidney concentrate urine.",
                ],
                "self_tests": [
                    {"q": "Which nephron type concentrates urine and why?", "a": "Juxtamedullary nephrons — their long loops of Henle and parallel vasa recta establish and maintain the medullary osmotic gradient."},
                    {"q": "List the parts of the nephron in the order filtrate passes through them.", "a": "Renal corpuscle → proximal convoluted tubule → loop of Henle → distal convoluted tubule → collecting duct."},
                ],
            },
        },
        {
            "id": "s9", "code": "§9", "lo": "Urine formation",
            "title": "Formation of urine", "tag": "Filter, reabsorb, secrete — and where each is fixed vs tunable.",
            "lead": "The capstone: three processes turn plasma into urine. The structural detail of filtration and the hormone tuning here are expanded in the Week 11 guide, but this is where the logic starts.",
            "blocks": [
                ("plate", 39, "Three processes", "Filtration, reabsorption and secretion in the nephron"),
                ("box", "why", "Why · three verbs define urine", "Urine is the net of three processes. <strong>Filtration</strong> pushes fluid from glomerular blood into the tubule, sorted only by <em>size</em>. <strong>Reabsorption</strong> returns the valuable material (water, glucose, ions) to the blood via transporters. <strong>Secretion</strong> actively adds extra waste/toxins from blood into the filtrate. The arithmetic the nephron runs: <strong>Excreted = Filtered − Reabsorbed + Secreted</strong> — the single equation that underpins all of renal physiology."),
                ("plate", 40, "Filtration", "Filtration through capillary pores, basement membrane and podocyte slits"),
                ("box", "mnem", "Exam hook · what passes and what stays", "About <strong>20% of plasma</strong> is filtered on each pass. The filter is a size sieve of three layers — <strong>fenestrated capillary → basement membrane → podocyte foot-process slits</strong>. Small solutes (<strong>glucose, amino acids, ions, urea</strong>) pass freely; <strong>large plasma proteins (albumin) and blood cells stay in the blood</strong>. So <strong>protein or blood in the urine signals a damaged filter</strong> (glomerular disease) — the clinical pay-off of this slide, detailed in Week 11."),
                ("plate", 41, "Reabsorption &amp; secretion — PCT and loop", "Obligatory reabsorption in the proximal tubule and loop of Henle"),
                ("box", "why", "Why · the proximal tubule is the workhorse", "Most <strong>obligatory (automatic) reabsorption</strong> happens early — in the <strong>proximal convoluted tubule and loop of Henle</strong>. Here <strong>glucose and amino acids are ~100% reabsorbed</strong> (they should never reach urine), along with the bulk of Na⁺, water and bicarbonate. It is “obligatory” because it runs regardless of the body's moment-to-moment needs — the fine, demand-driven adjustment is left to the distal nephron."),
                ("grid", [
                    (42, "Regulated reabsorption — DCT &amp; collecting duct", "Hormone-controlled reabsorption via ADH and aldosterone"),
                    (43, "Summary — what is handled where", "Summary map of reabsorption and secretion along the nephron"),
                ]),
                ("box", "clin", "Clinical · the two hormones to know", "The <strong>distal convoluted tubule and collecting duct</strong> do the <strong>regulated</strong> fine-tuning under hormonal command. <strong>ADH (vasopressin)</strong> from the posterior pituitary inserts <strong>aquaporins</strong> to reclaim <strong>water</strong> when you are dehydrated (concentrating the urine). <strong>Aldosterone</strong> from the adrenal cortex (end-point of the RAAS this lecture opened with) reclaims <strong>Na⁺ and water</strong> when blood pressure is low. These are the levers that let one organ hold plasma volume, osmolarity and pressure steady — and the targets of diuretic drugs. Week 11 takes filtration, reabsorption and clearance quantitatively from here."),
            ],
            "recall": {"head": "Recall — urine formation", "items": [
                "<li><b>The master equation —</b> excreted = <b>filtered − reabsorbed + secreted</b></li>",
                "<li><b>Filter layers —</b> <b>fenestrated capillary</b> → <b>basement membrane</b> → <b>podocyte slits</b></li>",
                "<li><b>Stay in blood —</b> <b>albumin</b> and <b>blood cells</b> → their presence in urine = <b>filter damage</b></li>",
                "<li><b>Obligatory reabsorption —</b> <b>PCT</b> &amp; <b>loop</b>; glucose/amino acids <b>~100%</b> reclaimed</li>",
                "<li><b>Regulated (DCT/CD) —</b> <b>ADH</b> → water (aquaporins); <b>aldosterone</b> → Na⁺/water</li>",
            ]},
            "digest": {
                "key_points": [
                    "Three processes form urine: filtration (size-based, blood→tubule), reabsorption (tubule→blood of valuable solutes/water), secretion (blood→tubule of extra wastes).",
                    "Master equation: amount excreted = amount filtered − amount reabsorbed + amount secreted.",
                    "Filtration barrier is a three-layer size sieve (fenestrated endothelium, basement membrane, podocyte slits); ~20% of plasma is filtered per pass; albumin and cells stay in blood, so proteinuria/haematuria signal glomerular damage.",
                    "Obligatory reabsorption (PCT and loop of Henle) reclaims glucose and amino acids ~100% plus bulk Na+/water; regulated reabsorption (DCT and collecting duct) is hormone-controlled.",
                    "ADH inserts aquaporins to reabsorb water (dehydration); aldosterone reabsorbs Na+/water (low blood pressure) — the RAAS end-point.",
                ],
                "self_tests": [
                    {"q": "State the equation relating excretion to filtration, reabsorption and secretion.", "a": "Amount excreted = amount filtered − amount reabsorbed + amount secreted."},
                    {"q": "Why does albumin in the urine indicate disease?", "a": "Albumin is normally too large (and too negatively charged) to cross the intact glomerular filter, so albuminuria indicates a damaged filtration barrier."},
                    {"q": "Which hormones control regulated reabsorption in the distal nephron, and what does each reclaim?", "a": "ADH (vasopressin) inserts aquaporins to reabsorb water; aldosterone drives Na+ (and water) reabsorption."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
