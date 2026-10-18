#!/usr/bin/env python3
"""Week 11 — Filtration and reabsorption. MHHS2402. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/w11_filtration"

SPEC = {
    "slug": "renal_filtration_reabsorption_mhhs2402_wk11",
    "workdir": WD,
    "unit": "MHHS2402",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "week": 11,
    "title": "Renal Filtration &amp; Reabsorption",
    "source": "MHHS2402 Week 11 — Filtration and reabsorption, A/Prof. Mark Butlin (Macquarie University)",
    "brand": "MHHS2402 · Wk11 · Renal",
    "brandsub": "Filtration &amp;<br>Reabsorption",
    "eyebrow": "MHHS2402 · Cardiovascular, Renal &amp; Respiratory · Week 11",
    "h1": "Renal Filtration &amp; Reabsorption",
    "h1thin": "how 180 L becomes 1.5 L — and how the kidney controls it",
    "lede": "The physiology companion to the Week 10 anatomy guide: every lecture slide shown in full, then explained the way a tutor would. The through-line is one equation — GFR = K<sub>f</sub> × (P<sub>G</sub> + π<sub>B</sub> − P<sub>B</sub> − π<sub>G</sub>) — and one astonishing fact: the kidney filters ~180 L of plasma a day and reabsorbs more than 99% of it.",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The note underneath is <b>not a re-caption</b> — it adds the mechanism, the number you need, and the clinical angle the slide assumes. Keep the Starling/GFR equation on screen in your head: every \"factor affecting GFR\" is just one term of it moving.",
    "n_slides": 41,
    "sections": [
        {
            "id": "s0", "code": "§0", "lo": "Role of the kidney",
            "title": "The kidney's job — filter, reabsorb, secrete", "tag": "Three processes, one purpose: curate the plasma.",
            "lead": "A one-slide recap sets the frame: the kidney does not primarily \"make urine\" — it <em>processes plasma</em>. It filters a huge volume, then decides what to keep. Urine is simply what is left over.",
            "blocks": [
                ("plate", 4, "Roles of the kidney — recap", "Recap of the six homeostatic roles of the kidney"),
                ("box", "active", "Orientation · the six jobs in one breath", "Carry Week 10's list forward: the kidney regulates <strong>blood volume/pressure</strong>, <strong>osmolarity</strong> and <strong>ion balance</strong> (Na⁺, K⁺, Ca²⁺, Cl⁻, phosphate), guards <strong>pH</strong> (excreting H⁺, conserving HCO₃⁻), <strong>excretes wastes</strong>, and makes <strong>hormones</strong> (erythropoietin, renin). This week is about the <em>mechanics</em> of the first five."),
                ("grid", [
                    (5, "Functional overview — three processes", "Filtration, reabsorption and secretion defined"),
                    (6, "Where each process happens", "Filtration at the corpuscle, reabsorption/secretion along the tubule"),
                ]),
                ("box", "why", "Why · match each verb to a place", "Lock the vocabulary to anatomy. <strong>Filtration</strong> = fluid from blood into the tubule lumen, happening <em>only</em> at the <strong>renal corpuscle</strong> (glomerulus + Bowman's capsule). <strong>Reabsorption</strong> = material from the filtrate back into blood, along the <strong>proximal tubule, loop of Henle and distal nephron</strong>. <strong>Secretion</strong> = material from blood added into the lumen. Filtered plasma is <strong>filtrate</strong>; whatever is not reabsorbed is <strong>excreted</strong>. Everything that follows is a quantitative version of these three verbs."),
            ],
            "recall": {"head": "Recall — the three processes", "items": [
                "<li><b>Filtration —</b> blood → <b>lumen</b>, at the <b>renal corpuscle</b> only</li>",
                "<li><b>Reabsorption —</b> filtrate → <b>blood</b>, along the <b>tubule</b></li>",
                "<li><b>Secretion —</b> <b>blood</b> → lumen, along the tubule</li>",
                "<li><b>Excreted —</b> whatever is filtered/secreted and <b>not reabsorbed</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The kidney processes plasma via three steps: filtration (blood→lumen at the renal corpuscle), reabsorption (lumen→blood along the tubule), secretion (blood→lumen along the tubule).",
                    "Filtered plasma is 'filtrate'; whatever is not reabsorbed is excreted as urine.",
                ],
                "self_tests": [
                    {"q": "Where in the nephron does filtration occur, and where do reabsorption and secretion occur?", "a": "Filtration occurs only at the renal corpuscle (glomerulus + Bowman's capsule); reabsorption and secretion occur along the tubule (proximal tubule, loop of Henle, distal nephron)."},
                ],
            },
        },
        {
            "id": "s1", "code": "§1", "lo": "The glomerular filtration barrier",
            "title": "The glomerular filtration barrier", "tag": "Three layers, two gates — size and charge — and what they let through.",
            "lead": "The barrier decides what the filtrate contains. It is a three-layer sieve that sorts by <em>size</em> and by <em>charge</em>; understanding both explains why urine is normally protein-free and why disease makes it leak.",
            "blocks": [
                ("grid", [
                    (10, "Three layers of the barrier", "Endothelium, basement membrane and podocytes"),
                    (11, "Why filtration is so fast", "Large fenestrae, loose basement membrane and wide filtration slits"),
                ]),
                ("box", "why", "Why · leaky by design, 180 L/day", "The barrier has <strong>three layers</strong>: the <strong>fenestrated capillary endothelium</strong>, the <strong>basement membrane</strong>, and the <strong>podocyte epithelium</strong> whose interdigitating foot processes leave <strong>filtration slits</strong>. Unlike a normal capillary, all three are unusually <em>leaky</em> — large fenestrae, loose basement membrane, wide slits — which is why the glomerulus generates a colossal <strong>~180 L of filtrate per day</strong>. Reabsorption then reclaims almost all of it, leaving only <strong>~1.5 L</strong> as urine."),
                ("plate", 12, "Size selectivity", "Filtration rate falls with molecular weight: water to albumin"),
                ("box", "mnem", "Exam hook · the size table", "Filtration is <strong>inversely related to molecular size</strong>. Small species — <strong>water, Na⁺, glucose</strong> — filter as freely as water (normalised rate ≈ 1), and even <strong>inulin (5,500 Da)</strong> still passes freely (that is why it measures GFR, §6). The curve falls off with size: <strong>myoglobin (17,000 Da) ≈ 0.75</strong>, and <strong>albumin (69,000 Da) ≈ 0.005</strong> — effectively excluded. Learn albumin as the <em>practical cut-off</em>."),
                ("plate", 13, "The charge barrier", "Negatively charged basement membrane repels anionic albumin"),
                ("box", "clin", "Clinical · why proteinuria means disease", "Size is only half the story. The <strong>basement membrane is negatively charged</strong>, and because <strong>albumin is also negatively charged</strong>, electrostatic repulsion holds it back even beyond its size — <em>like charges repel</em>. In glomerular disease the membrane <strong>loses its negative charge</strong>, repulsion fails, and albumin slips through → <strong>albuminuria / proteinuria</strong> on urinalysis. So protein in the urine is an early fingerprint of a damaged filter (e.g. diabetic nephropathy, minimal-change disease)."),
                ("grid", [
                    (14, "Composition — what's excluded", "Filtrate is protein-free and cell-free"),
                    (15, "Composition — what's included", "Filtrate mirrors plasma: ions, glucose, urea, creatinine"),
                ]),
                ("box", "why", "Why · filtrate is 'deproteinised plasma'", "Put the two gates together and you can predict the filtrate: it is <strong>almost identical to plasma but free of protein and cells</strong>. It contains the salts/ions (<strong>Na⁺, K⁺, Cl⁻, Ca²⁺, phosphate</strong>) and small organics (<strong>glucose, urea, creatinine, uric acid</strong>) — but essentially <strong>no albumin and no red cells</strong>. That is why finding either in urine is abnormal and points straight back to the barrier."),
            ],
            "recall": {"head": "Recall — the filtration barrier", "items": [
                "<li><b>Three layers —</b> <b>fenestrated endothelium</b> → <b>basement membrane</b> → <b>podocyte slits</b></li>",
                "<li><b>Daily filtrate —</b> <b>~180 L/day</b> filtered, <b>~1.5 L</b> excreted</li>",
                "<li><b>Two gates —</b> <b>size</b> (albumin excluded) and <b>charge</b> (negative BM repels albumin)</li>",
                "<li><b>Lost negative charge —</b> <b>albuminuria / proteinuria</b> = glomerular disease</li>",
                "<li><b>Normal filtrate —</b> plasma minus <b>protein</b> and <b>cells</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The glomerular filtration barrier has three layers: fenestrated endothelium, basement membrane, podocyte foot processes with filtration slits — all unusually leaky, generating ~180 L filtrate/day (~1.5 L excreted).",
                    "Filtration is inversely related to molecular size: water/Na+/glucose and even inulin (5,500 Da) filter freely; myoglobin (17 kDa) partly; albumin (69 kDa) is essentially excluded.",
                    "A charge barrier adds to size selectivity: the negatively charged basement membrane repels negatively charged albumin; loss of this charge in disease causes albuminuria/proteinuria.",
                    "Normal filtrate is almost identical to plasma but protein-free and cell-free.",
                ],
                "self_tests": [
                    {"q": "Name the three layers of the glomerular filtration barrier.", "a": "Fenestrated capillary endothelium, basement membrane, and podocyte epithelium with filtration slits."},
                    {"q": "Besides size, what property restricts albumin filtration, and what happens when it is lost?", "a": "Charge — the basement membrane is negatively charged and repels anionic albumin; losing that charge (glomerular disease) allows albumin through, causing proteinuria/albuminuria."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "Factors affecting GFR",
            "title": "Factors affecting GFR — the Starling forces", "tag": "One equation; every 'factor' is just one of its terms moving.",
            "lead": "GFR is set by the balance of Starling pressures across the glomerular capillary. Write the equation once and every factor that follows — pressure, osmotic pull, arteriolar tone — is simply one term changing. This is the examinable core of the lecture.",
            "blocks": [
                ("grid", [
                    (18, "Starling forces in a systemic capillary", "Net filtration pressure in an ordinary capillary ≈ 0.3 mmHg"),
                    (19, "Starling forces in the glomerulus", "Glomerular net filtration pressure ≈ 10 mmHg outward"),
                ]),
                ("box", "why", "Why · the glomerulus is built to filter, hard", "A normal capillary balances to a tiny net outward pressure (~0.3 mmHg). The glomerulus is different: <strong>GFR = K<sub>f</sub> × (P<sub>G</sub> + π<sub>B</sub> − P<sub>B</sub> − π<sub>G</sub>)</strong>. Plug in the numbers — <strong>glomerular hydrostatic P<sub>G</sub> ≈ 60</strong> (the big outward push, kept high because the efferent arteriole is a downstream resistor), Bowman's hydrostatic <strong>P<sub>B</sub> ≈ 18</strong>, glomerular osmotic <strong>π<sub>G</sub> ≈ 32</strong>, Bowman's osmotic <strong>π<sub>B</sub> ≈ 0</strong> (protein-free filtrate) — giving a <strong>net ≈ 10 mmHg outward</strong>. That sustained high pressure is why the glomerulus filters so much more than any other capillary bed."),
                ("plate", 20, "The filtration coefficient (Kf)", "Kf = hydraulic conductivity × surface area"),
                ("box", "clin", "Clinical · Kf is a disease lever, not a daily dial", "<strong>K<sub>f</sub></strong> = <strong>hydraulic conductivity × capillary surface area</strong>. It is <em>not</em> used for minute-to-minute regulation, but <strong>disease changes it</strong>: losing functional glomerular capillaries <strong>reduces surface area</strong>, and thickening the capillary wall <strong>reduces conductivity</strong> — both <strong>lower K<sub>f</sub> and therefore GFR</strong>. This is the structural route by which <strong>diabetes, hypertension and ageing</strong> erode GFR."),
                ("plate", 21, "↑ Bowman's hydrostatic pressure → ↓ GFR", "Urinary obstruction raises PB and reduces GFR"),
                ("box", "clin", "Clinical · obstruction backs up the pressure", "Bowman's pressure <strong>P<sub>B</sub></strong> is normally steady (~18 mmHg), but anything that <strong>obstructs outflow downstream — a kidney stone, tumour or enlarged prostate</strong> — raises it. A bigger <strong>opposing (inward) pressure shrinks the net filtration pressure → GFR falls</strong>. This is <em>post-renal</em> acute kidney injury in one line."),
                ("grid", [
                    (22, "↑ glomerular osmotic pressure → ↓ GFR", "Filtration concentrates plasma proteins, raising πG"),
                    (23, "Filtration fraction and πG", "Higher filtration fraction raises πG and lowers GFR"),
                ]),
                ("box", "why", "Why · the filter concentrates its own brake", "As blood runs along the glomerular capillary and filtrate leaves, the <strong>plasma proteins left behind become concentrated</strong>, so the glomerular osmotic pressure <strong>π<sub>G</sub> rises</strong> and pulls fluid back — opposing filtration. Hence the rule: a <strong>higher filtration fraction → higher π<sub>G</sub> → lower GFR</strong> (and vice versa). π<sub>G</sub> is a built-in negative feedback that stops the glomerulus filtering itself dry."),
                ("plate", 24, "Afferent vs efferent arteriolar resistance", "Afferent and efferent tone move PG in opposite directions"),
                ("box", "mnem", "Exam hook · the arteriole rule — this is always tested", "Two taps control <strong>P<sub>G</sub></strong>. Constrict the <strong>afferent</strong> (inflow) arteriole → less blood reaches the glomerulus → <strong>P<sub>G</sub> falls → GFR falls</strong>. Constrict the <strong>efferent</strong> (outflow) arteriole → blood dams up behind it → <strong>P<sub>G</sub> rises → GFR rises</strong>. This is exactly how <strong>angiotensin II</strong> (efferent constrictor) <em>protects</em> GFR when renal perfusion drops — and why <strong>ACE inhibitors/ARBs can drop GFR</strong> in a kidney that depends on that efferent tone (e.g. bilateral renal artery stenosis)."),
                ("plate", 25, "Efferent resistance — the biphasic twist", "Large efferent constriction eventually lowers GFR"),
                ("box", "why", "Why · too much efferent tone backfires", "The efferent story has a <strong>biphasic</strong> ending. A modest rise in efferent resistance raises <strong>P<sub>G</sub></strong> and <strong>GFR</strong>. But a <strong>large (&gt;3-fold) or sustained</strong> rise chokes <strong>renal blood flow</strong> so much that filtrate removal concentrates the plasma proteins → <strong>π<sub>G</sub> climbs</strong> → and GFR then <strong>falls</strong> again. So severe efferent constriction ultimately <em>reduces</em> GFR despite the high pressure."),
                ("plate", 26, "Summary — what moves GFR", "Summary table of physiological and pathological causes of GFR change"),
                ("box", "mnem", "Exam hook · the summary you can be examined straight from", "Memorise the one-liners: <strong>↓K<sub>f</sub> → ↓GFR</strong> (renal disease, diabetes, hypertension, ageing); <strong>↑P<sub>B</sub> → ↓GFR</strong> (urinary obstruction); <strong>↑π<sub>G</sub> → ↓GFR</strong> (↓ renal blood flow); <strong>↓ arterial pressure → ↓P<sub>G</sub> → ↓GFR</strong> (blunted by autoregulation, §3); <strong>↓ efferent tone (↓angiotensin II, or an ACE inhibitor) → ↓P<sub>G</sub> → ↓GFR</strong>; <strong>↑ afferent tone (sympathetic, noradrenaline, endothelin) → ↓P<sub>G</sub> → ↓GFR</strong>. Every row is one term of the equation moving."),
            ],
            "recall": {"head": "Recall — Starling forces &amp; GFR", "items": [
                "<li><b>The equation —</b> GFR = <b>K<sub>f</sub></b> × (<b>P<sub>G</sub></b> + π<sub>B</sub> − <b>P<sub>B</sub></b> − <b>π<sub>G</sub></b>)</li>",
                "<li><b>Net filtration pressure —</b> ≈ <b>10</b> mmHg outward (P<sub>G</sub>~60, P<sub>B</sub>~18, π<sub>G</sub>~32)</li>",
                "<li><b>Afferent constriction —</b> ↓P<sub>G</sub> → <b>↓GFR</b>; <b>efferent</b> constriction → ↑P<sub>G</sub> → <b>↑GFR</b></li>",
                "<li><b>↑P<sub>B</sub> (obstruction) —</b> <b>↓GFR</b>; <b>↑π<sub>G</sub></b> → ↓GFR</li>",
                "<li><b>↓K<sub>f</sub> —</b> from <b>diabetes/hypertension/ageing</b> → ↓GFR</li>",
                "<li><b>Angiotensin II —</b> constricts <b>efferent</b> → <b>protects</b> GFR (ACE-i can drop it)</li>",
            ]},
            "digest": {
                "key_points": [
                    "GFR = Kf × (PG + πB − PB − πG); glomerular net filtration pressure ≈ 10 mmHg outward (PG≈60, PB≈18, πG≈32, πB≈0).",
                    "Kf = hydraulic conductivity × surface area; not a normal regulator but lowered by disease (fewer capillaries, thicker wall) in diabetes, hypertension, ageing.",
                    "Afferent arteriolar constriction lowers PG and GFR; efferent constriction raises PG and GFR (basis of angiotensin II protecting GFR and ACE inhibitors reducing it).",
                    "Raised Bowman's pressure (urinary obstruction) lowers GFR; rising glomerular osmotic pressure (higher filtration fraction / lower renal blood flow) lowers GFR.",
                    "Large/sustained efferent constriction is biphasic: it first raises then lowers GFR as renal blood flow falls and πG climbs.",
                ],
                "self_tests": [
                    {"q": "Write the glomerular filtration equation and give approximate values for each pressure.", "a": "GFR = Kf × (PG + πB − PB − πG); PG ≈ 60, PB ≈ 18, πG ≈ 32, πB ≈ 0 mmHg, net ≈ 10 mmHg outward."},
                    {"q": "How do afferent and efferent arteriolar constriction differ in their effect on GFR?", "a": "Afferent constriction lowers glomerular pressure and GFR; efferent constriction raises glomerular pressure and GFR."},
                    {"q": "Why can an ACE inhibitor reduce GFR?", "a": "Angiotensin II maintains GFR by constricting the efferent arteriole; blocking it dilates the efferent, dropping glomerular pressure and GFR — dangerous when the kidney depends on that tone (e.g. bilateral renal artery stenosis)."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "GFR regulation",
            "title": "Autoregulation of GFR", "tag": "Keeping GFR steady despite swinging blood pressure.",
            "lead": "GFR must stay constant from a quiet morning to a sprint. Two intrinsic mechanisms (myogenic, tubuloglomerular feedback) hold it steady across a wide pressure range; hormones and nerves override it when the whole body needs the blood elsewhere.",
            "blocks": [
                ("plate", 30, "The regulators — overview", "Myogenic response, tubuloglomerular feedback, hormones and nerves"),
                ("box", "why", "Why · intrinsic first, extrinsic to override", "Two <strong>intrinsic</strong> mechanisms autoregulate GFR across a mean arterial pressure of roughly <strong>80–180 mmHg</strong>: the <strong>myogenic response</strong> and <strong>tubuloglomerular feedback</strong>, both acting on arteriolar tone. On top sit <strong>extrinsic</strong> controls — <strong>hormones and sympathetic nerves</strong> — that deliberately <em>override</em> autoregulation when the body must divert blood (haemorrhage, exercise, stress)."),
                ("plate", 31, "The myogenic response", "Vascular smooth muscle constricts when stretched by higher pressure"),
                ("box", "why", "Why · the vessel defends itself", "The <strong>myogenic response</strong> is the intrinsic reflex of vascular smooth muscle: <strong>higher pressure stretches the afferent arteriole → it constricts</strong> → glomerular pressure and GFR are held down; lower pressure → it dilates → GFR is propped up. It is the same autoregulation seen in other arterioles. Its limit: below ~80 mmHg the renal bed is already near-maximally dilated, so it <strong>cannot compensate further</strong> and GFR falls."),
                ("grid", [
                    (32, "Tubuloglomerular feedback — the apparatus", "Juxtaglomerular apparatus: macula densa and granular cells"),
                    (33, "Macula densa senses NaCl", "High tubular flow triggers afferent vasoconstriction"),
                ]),
                ("box", "mnem", "Exam hook · the macula densa flow sensor", "<strong>Tubuloglomerular feedback</strong> is the nephron talking back to its own glomerulus through the <strong>juxtaglomerular apparatus</strong>. The <strong>macula densa</strong> cells sample <strong>NaCl in the distal tubule</strong> as a proxy for flow: <strong>high flow (high GFR) → more NaCl sensed → paracrine signal → afferent arteriolar constriction → GFR brought back down</strong>. The <strong>granular (juxtaglomerular) cells</strong> secrete <strong>renin</strong>, tying this local loop to the systemic RAAS. One sentence: <em>too much flow past the macula densa throttles the afferent.</em>"),
                ("plate", 34, "Sympathetic (autonomic) control", "Sympathetic stimulation constricts arterioles and reduces GFR"),
                ("box", "clin", "Clinical · when the body sacrifices the kidney", "<strong>Sympathetic neurons innervate both afferent and efferent arterioles</strong>; strong sympathetic drive causes <strong>vasoconstriction that reduces GFR</strong>. There must be a <em>reason</em> for that drive — <strong>haemorrhage/low BP, severe stress or pain, sustained hypoxia or acidosis</strong>. This is the body choosing to <strong>divert blood from the kidney to the heart and brain</strong> — adaptive in shock, but a route to <strong>pre-renal acute kidney injury</strong> if prolonged."),
                ("plate", 35, "Hormones affecting GFR", "Vasoconstrictors lower GFR; nitric oxide and prostaglandins raise it"),
                ("box", "mnem", "Exam hook · constrictors down, dilators up (and why NSAIDs bite)", "Group the messengers by vascular action. <strong>Vasoconstrictors lower GFR</strong>: <strong>noradrenaline/adrenaline, endothelin</strong>, and <strong>angiotensin II</strong> (which, by favouring the <em>efferent</em> arteriole, actually <strong>prevents GFR from falling</strong>). <strong>Vasodilators raise/protect GFR</strong>: <strong>nitric oxide</strong> and <strong>prostaglandins</strong>. That last pair is why <strong>NSAIDs (which block prostaglandins) can drop GFR</strong> in a kidney relying on dilator prostaglandins — the NSAID + ACE-inhibitor + dehydration \"triple whammy\" of acute kidney injury."),
            ],
            "recall": {"head": "Recall — autoregulation", "items": [
                "<li><b>Intrinsic pair —</b> <b>myogenic</b> response + <b>tubuloglomerular</b> feedback (MAP <b>~80–180</b>)</li>",
                "<li><b>Myogenic —</b> ↑pressure <b>stretches</b> afferent → it <b>constricts</b> → GFR steady</li>",
                "<li><b>Macula densa —</b> senses <b>NaCl</b>; high flow → <b>afferent constriction</b>; granular cells make <b>renin</b></li>",
                "<li><b>Sympathetic —</b> constricts arterioles → <b>↓GFR</b> (shock, stress, pain)</li>",
                "<li><b>Hormones —</b> AngII/NA/endothelin <b>↓</b>; <b>NO</b> &amp; <b>prostaglandins</b> ↑ (NSAIDs ↓GFR)</li>",
            ]},
            "digest": {
                "key_points": [
                    "GFR is autoregulated across MAP ~80–180 mmHg by two intrinsic mechanisms: the myogenic response and tubuloglomerular feedback.",
                    "Myogenic response: raised pressure stretches the afferent arteriole, which constricts to keep glomerular pressure/GFR steady (fails below ~80 mmHg).",
                    "Tubuloglomerular feedback: macula densa cells sense distal NaCl (a flow proxy); high flow triggers afferent constriction to lower GFR; granular cells secrete renin.",
                    "Sympathetic stimulation constricts afferent and efferent arterioles to reduce GFR (shock, stress, pain) — adaptive but can cause pre-renal AKI.",
                    "Vasoconstrictors (noradrenaline, endothelin, angiotensin II) lower GFR; vasodilators (nitric oxide, prostaglandins) raise/protect it — the basis of NSAID-induced GFR fall.",
                ],
                "self_tests": [
                    {"q": "What does the macula densa sense, and how does it respond to a high GFR?", "a": "It senses NaCl concentration in the distal tubule (a proxy for flow); high flow/high GFR triggers paracrine signals causing afferent arteriolar constriction to bring GFR back down."},
                    {"q": "Why can NSAIDs reduce GFR?", "a": "Prostaglandins are vasodilators that help maintain renal blood flow and GFR; NSAIDs block prostaglandin synthesis, so in a kidney dependent on them GFR falls."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "Tubular reabsorption",
            "title": "Tubular reabsorption", "tag": "Reclaiming &gt;99% — and why sodium drives all of it.",
            "lead": "Filtration is indiscriminate; reabsorption is where the kidney shows judgement. Over 99% of the filtered volume is recovered, powered by one pump. The section ends with transport maximum — the concept behind glycosuria in diabetes.",
            "blocks": [
                ("grid", [
                    (39, "180 L in, 1.5 L out", "More than 99% of filtered fluid is reabsorbed"),
                    (40, "Why filter so much?", "Filtering a large volume lets the kidney clear and regulate fast"),
                ]),
                ("box", "why", "Why · the 'filter everything then reclaim' strategy", "The arithmetic is stark: <strong>~180 L filtered, ~1.5 L excreted → &gt;99% reabsorbed</strong>. Why run such a wasteful-looking system? Two reasons: (1) foreign/unwanted substances are <strong>not readily reabsorbed</strong>, so filtering a huge volume <strong>clears them efficiently</strong> while <strong>wanted substances (glucose, amino acids) are reclaimed</strong>; and (2) processing a large volume lets the kidney make <strong>large, rapid adjustments</strong> to water and ion balance. High throughput buys both thorough cleaning and fast control."),
                ("plate", 41, "Mechanisms of reabsorption", "Active, electrochemical, osmotic and passive transport routes"),
                ("box", "mnem", "Exam hook · four routes", "Sort reabsorption by mechanism: <strong>Na⁺ — active</strong> (pumped); <strong>anions — follow the electrochemical gradient</strong> Na⁺ creates; <strong>water — osmosis</strong> (follows solute); <strong>permeable solutes (K⁺, Ca²⁺, urea) — passive</strong>, transcellular through transporters or paracellular between cells. The theme: <strong>move Na⁺ actively and almost everything else follows passively.</strong>"),
                ("plate", 42, "Low peritubular pressure favours reabsorption", "Peritubular Starling forces favour net reabsorption"),
                ("box", "why", "Why · the second capillary bed is a low-pressure sponge", "Recall from Week 10 that the <strong>efferent arteriole</strong> feeds the <strong>peritubular capillaries</strong> — a <em>second</em> bed, downstream of a resistor, so its <strong>hydrostatic pressure is low</strong> while its <strong>osmotic (protein) pressure is high</strong> (the proteins never left the blood). Starling forces are therefore <strong>reversed relative to the glomerulus: net reabsorption</strong>. The vessel that filtered the fluid is perfectly set up to soak it back up."),
                ("grid", [
                    (43, "Active Na⁺ transport — lumen to cell", "Na+ enters the tubule cell down its gradient via symport/antiport"),
                    (44, "Active Na⁺ transport — cell to interstitium", "Basolateral Na+/K+-ATPase pumps Na+ out into interstitium"),
                ]),
                ("box", "why", "Why · the Na⁺/K⁺-ATPase is the engine of the kidney", "<strong>Active Na⁺ transport is the primary driving force for renal reabsorption.</strong> Two steps: (1) at the <strong>apical (luminal) membrane</strong>, Na⁺ flows <em>down</em> its gradient into the cell — dragging other molecules with it (<strong>symport</strong> of glucose/amino acids <em>against</em> their gradients; <strong>antiport</strong> of H⁺ out). (2) At the <strong>basolateral membrane</strong>, the <strong>Na⁺/K⁺-ATPase</strong> pumps Na⁺ <em>up</em> its gradient into the interstitium (3 Na⁺ out for 2 K⁺ in; K⁺ leaks back through basolateral channels). That pump keeps intracellular Na⁺ low, which is what makes the luminal Na⁺ gradient — and therefore <strong>all the secondary active transport</strong> — possible. Block it and reabsorption collapses."),
                ("plate", 45, "Saturation / transport maximum", "Carrier-mediated transport saturates at a transport maximum"),
                ("box", "mnem", "Exam hook · the bus analogy for Tm", "Carrier-mediated transport uses a finite number of transporters, so it has a ceiling — the <strong>transport maximum (T<sub>m</sub>)</strong>. Beyond it, transport <strong>saturates</strong>. The lecture's analogy: a queue for a bus — if there are enough seats (carriers) everyone is reabsorbed; once the seats fill, the rest <strong>walk (are excreted)</strong>. This is the single idea behind the glucose example next."),
                ("grid", [
                    (47, "Glucose handling — the curves", "Filtration, reabsorption and excretion of glucose vs plasma level"),
                    (48, "Glucose spills in diabetes", "Above the renal threshold glucose appears in urine"),
                ]),
                ("box", "clin", "Clinical · glycosuria and the renal threshold", "Apply <strong>excretion = filtration − reabsorption</strong> to glucose. At normal plasma glucose, filtered glucose is <strong>100% reabsorbed</strong> → <strong>none in urine</strong>. But reabsorption is carrier-limited (T<sub>m</sub>): once plasma glucose exceeds the <strong>renal threshold (~300 mg/100 mL)</strong>, as in uncontrolled <strong>diabetes mellitus</strong>, the carriers saturate and the excess <strong>spills into the urine → glycosuria</strong>. The osmotic drag of that glucose explains the <strong>polyuria</strong> of untreated diabetes — and is the mechanism deliberately exploited by <strong>SGLT2-inhibitor</strong> drugs."),
            ],
            "recall": {"head": "Recall — tubular reabsorption", "items": [
                "<li><b>The numbers —</b> <b>180 L</b> filtered, <b>1.5 L</b> out → <b>&gt;99%</b> reabsorbed</li>",
                "<li><b>Primary driver —</b> <b>active Na⁺</b> transport via basolateral <b>Na⁺/K⁺-ATPase</b></li>",
                "<li><b>Luminal entry —</b> Na⁺ down gradient, <b>symport</b> (glucose) / <b>antiport</b> (H⁺)</li>",
                "<li><b>Peritubular capillaries —</b> <b>low</b> hydrostatic, <b>high</b> oncotic → net <b>reabsorption</b></li>",
                "<li><b>Transport maximum —</b> carriers <b>saturate</b> → excess <b>excreted</b></li>",
                "<li><b>Glycosuria —</b> plasma glucose &gt; <b>renal threshold</b> (~300) → glucose in urine (<b>diabetes</b>)</li>",
            ]},
            "digest": {
                "key_points": [
                    "About 180 L is filtered and 1.5 L excreted daily, so >99% of filtered fluid is reabsorbed; filtering a large volume clears non-reabsorbed wastes efficiently and allows rapid regulation.",
                    "Reabsorption mechanisms: Na+ active; anions follow the electrochemical gradient; water by osmosis; permeable solutes (K+, Ca2+, urea) passively (transcellular or paracellular).",
                    "Peritubular capillaries have low hydrostatic and high oncotic pressure (second capillary bed after the efferent arteriole), so Starling forces favour net reabsorption.",
                    "Active Na+ transport is the primary driving force: apical Na+ entry (symport of glucose/amino acids, antiport of H+) and basolateral Na+/K+-ATPase pumping Na+ into the interstitium.",
                    "Carrier transport has a transport maximum (Tm); above the renal threshold (~300 mg/100 mL) glucose saturates its carriers and spills into urine (glycosuria in diabetes mellitus).",
                ],
                "self_tests": [
                    {"q": "Why is active Na+ transport called the primary driving force for reabsorption?", "a": "The basolateral Na+/K+-ATPase keeps intracellular Na+ low, creating the luminal Na+ gradient that powers apical Na+ entry and all the secondary active transport (glucose/amino acid symport, H+ antiport)."},
                    {"q": "Explain glycosuria in diabetes using transport maximum.", "a": "Glucose reabsorption is carrier-limited (Tm); when plasma glucose exceeds the renal threshold (~300 mg/100 mL) the carriers saturate, so excess glucose cannot be reabsorbed and is excreted in urine."},
                ],
            },
        },
        {
            "id": "s5", "code": "§5", "lo": "Tubular secretion",
            "title": "Tubular secretion", "tag": "The active 'top-up' that fine-tunes excretion.",
            "lead": "Secretion is reabsorption run backwards: moving substances from blood into the tubule. It lets the nephron get rid of things faster than filtration alone — crucial for potassium, acid, and a long list of drugs.",
            "blocks": [
                ("plate", 52, "What secretion does", "Active transfer of solutes from blood into the tubule lumen"),
                ("box", "why", "Why · a second chance to dump", "<strong>Secretion</strong> is the <strong>active movement of molecules from the peritubular blood, through the cell, into the tubule lumen</strong> — the opposite direction to reabsorption. It lets the nephron <strong>increase excretion beyond what filtration delivers</strong>, which matters for anything that is protein-bound or needs tight control: <strong>K⁺ and H⁺ ions</strong> (electrolyte and acid-base balance) and <strong>organic compounds — drugs, vitamins, adrenaline/noradrenaline</strong>."),
                ("plate", 53, "Organic anion transporters — broad specificity", "The organic anion transporter secretes many drugs and toxins"),
                ("box", "clin", "Clinical · one transporter, many drugs — and interactions", "Secretory carriers like the <strong>organic anion transporter (OAT)</strong> have deliberately <strong>broad specificity</strong> — the OAT shifts <strong>bile salts, benzoate (a soft-drink preservative), salicylate (aspirin), saccharin</strong>, and many drugs. Two consequences: the kidney can <strong>clear drugs faster than filtration alone</strong>, and drugs sharing a transporter <strong>compete</strong> — the classic trick of giving <strong>probenecid to block penicillin secretion</strong> and make a dose last longer. Shared transporters are a common source of <strong>drug interactions</strong>."),
            ],
            "recall": {"head": "Recall — tubular secretion", "items": [
                "<li><b>Direction —</b> <b>blood → lumen</b> (opposite of reabsorption), <b>active</b></li>",
                "<li><b>Key secreted species —</b> <b>K⁺</b>, <b>H⁺</b>, organic compounds (<b>drugs</b>, vitamins, catecholamines)</li>",
                "<li><b>OAT —</b> <b>broad specificity</b> → secretes many drugs (aspirin, penicillin)</li>",
                "<li><b>Shared transporters —</b> drugs <b>compete</b> → <b>interactions</b> (e.g. probenecid)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Secretion is the active movement of solutes from peritubular blood into the tubule lumen (opposite of reabsorption), increasing excretion beyond filtration.",
                    "Important secreted species: K+ and H+ ions (electrolyte/acid-base balance) and organic compounds — drugs, vitamins, catecholamines.",
                    "Transporters such as the organic anion transporter (OAT) have broad specificity (bile salts, salicylate, saccharin, many drugs), so drugs compete for secretion — a source of drug interactions (e.g. probenecid blocking penicillin secretion).",
                ],
                "self_tests": [
                    {"q": "How does secretion differ from reabsorption in direction and purpose?", "a": "Secretion actively moves substances from blood into the tubule lumen (reabsorption is lumen→blood); it lets the nephron excrete substances faster than filtration alone, e.g. K+, H+, and many drugs."},
                    {"q": "Why can one drug slow the excretion of another?", "a": "They may share a broadly specific secretory transporter (e.g. OAT) and compete for it — the basis of probenecid prolonging penicillin levels."},
                ],
            },
        },
        {
            "id": "s6", "code": "§6", "lo": "Renal clearance",
            "title": "Renal clearance", "tag": "Turning filtration/reabsorption/secretion into a number for kidney function.",
            "lead": "Clearance is the quantitative pay-off: a single number that captures how the kidney handles a substance, and the standard way to measure GFR. Three worked examples — inulin, glucose, urea — pin the concept down.",
            "blocks": [
                ("grid", [
                    (57, "Excretion vs clearance", "Clearance = excretion rate normalised to plasma concentration"),
                    (58, "The equations", "Clearance of X = excretion rate of X ÷ plasma [X]"),
                ]),
                ("box", "why", "Why · clearance is excretion made comparable", "<strong>Excretion</strong> is simply the rate a substance leaves the body (urine flow × urine concentration). <strong>Clearance</strong> normalises that to the plasma level: <strong>clearance of X = excretion rate of X ÷ [X]<sub>plasma</sub></strong> — the <em>virtual volume of plasma cleared of X per minute</em>. And recall the master balance: <strong>excretion = filtration − reabsorption + secretion</strong>. Put together, clearance lets you compare how the kidney treats any substance on one scale: millilitres of plasma per minute."),
                ("grid", [
                    (59, "Inulin — clearance = GFR", "Inulin is filtered only, so its clearance equals GFR (~100 mL/min)"),
                    (60, "Glucose — clearance = 0", "Glucose is fully reabsorbed, so its clearance is zero"),
                ]),
                ("box", "mnem", "Exam hook · why inulin is the gold standard", "<strong>Inulin</strong> is <strong>freely filtered but neither reabsorbed nor secreted</strong>, so everything filtered is excreted → its <strong>clearance equals GFR</strong> (worked example: 4 mg/min ÷ 0.04 mg/mL = <strong>100 mL/min</strong>). That makes it the <strong>gold standard for measuring GFR</strong> (creatinine is the practical clinical surrogate). <strong>Glucose</strong> is the opposite — <strong>filtered then fully reabsorbed</strong> → excretion 0 → <strong>clearance 0</strong>. A clearance <em>below</em> GFR therefore signals <strong>net reabsorption</strong>."),
                ("plate", 61, "Urea — clearance between 0 and GFR", "Urea is partly reabsorbed, so its clearance is below GFR"),
                ("box", "why", "Why · urea sits in the middle", "<strong>Urea</strong> is filtered and then <strong>partly reabsorbed</strong> (4 filtered − 2 reabsorbed = 2 excreted → <strong>clearance 50 mL/min</strong>), so its clearance lands <em>between</em> 0 and GFR — the signature of a substance undergoing <strong>net reabsorption</strong> but not complete reabsorption. It is the intermediate case between inulin and glucose."),
                ("plate", 62, "Clearance vs GFR — the decision rule", "Clearance = GFR, < GFR, or > GFR reveals how a substance is handled"),
                ("box", "mnem", "Exam hook · read handling straight off clearance", "The decision rule you can be examined on: compare a substance's <strong>clearance to GFR</strong>. <strong>Clearance = GFR → filtered only</strong> (<strong>inulin</strong>, the GFR marker). <strong>Clearance &lt; GFR → net reabsorption</strong> (<strong>glucose</strong> = 0; urea = partial). <strong>Clearance &gt; GFR → net secretion</strong> (<strong>PAH</strong>, used to estimate renal plasma flow; many drugs, e.g. penicillin). One number tells you what the tubule did."),
            ],
            "recall": {"head": "Recall — renal clearance", "items": [
                "<li><b>Clearance of X —</b> excretion rate of X <b>÷ [X]<sub>plasma</sub></b> (mL plasma cleared/min)</li>",
                "<li><b>Excretion balance —</b> <b>filtration − reabsorption + secretion</b></li>",
                "<li><b>Inulin —</b> filtered only → clearance <b>= GFR</b> (gold standard, ~100 mL/min)</li>",
                "<li><b>Clearance &lt; GFR —</b> net <b>reabsorption</b> (glucose = <b>0</b>; urea ~50)</li>",
                "<li><b>Clearance &gt; GFR —</b> net <b>secretion</b> (<b>PAH</b>, penicillin)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Excretion rate = urine flow × urine [X]; clearance of X = excretion rate ÷ plasma [X] — the virtual volume of plasma cleared of X per minute.",
                    "Master balance: amount excreted = filtered − reabsorbed + secreted.",
                    "Inulin is filtered only (not reabsorbed or secreted), so its clearance equals GFR (~100 mL/min) — the gold standard for measuring GFR (creatinine is the clinical surrogate).",
                    "Clearance < GFR indicates net reabsorption (glucose clearance = 0; urea ~50 mL/min); clearance > GFR indicates net secretion (PAH, many drugs like penicillin).",
                ],
                "self_tests": [
                    {"q": "Why does inulin clearance equal GFR?", "a": "Inulin is freely filtered but neither reabsorbed nor secreted, so the amount excreted equals the amount filtered; dividing its excretion rate by plasma concentration gives GFR."},
                    {"q": "A substance has a clearance greater than GFR. What is happening to it in the tubule?", "a": "It is being secreted (net secretion) — e.g. PAH or penicillin."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
