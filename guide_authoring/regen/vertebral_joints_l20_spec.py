#!/usr/bin/env python3
"""L20 — Joints and ligaments of the vertebral column. MHHS2401. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/l20_vert_joints"

SPEC = {
    "slug": "vertebral_column_joints_ligaments_mhhs2401_l20",
    "workdir": WD,
    "unit": "MHHS2401",
    "subject": "Musculoskeletal System",
    "week": 11,
    "title": "Joints &amp; Ligaments of the Vertebral Column",
    "source": "MHHS2401 Lecture 20 — Joints and ligaments of the vertebral column, Dr Mirjana Strkalj (Macquarie University)",
    "brand": "MHHS2401 · L20 · Spine",
    "brandsub": "Joints &amp; Ligaments<br>of the Spine",
    "eyebrow": "MHHS2401 · Musculoskeletal System · Lecture 20",
    "h1": "Joints &amp; Ligaments of the Vertebral Column",
    "h1thin": "what holds the spine together — and what fails",
    "lede": "Every lecture slide, shown in full and explained like a tutor would. Two joint families run the spine: the weight-bearing <em>symphyses</em> between the bodies (the IV discs) and the gliding <em>facet</em> joints of the arches — plus the specialised craniovertebral and costovertebral joints. Read every ligament as \"which movement does it check?\" and the clinical picture follows.",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The note underneath is <b>not a re-caption</b> — it adds the mechanism (which movement a ligament restrains), the structure the slide assumes, and the clinical lesion (disc herniation, whiplash, dens fracture). Pair each ligament with the movement it prevents.",
    "n_slides": 31,
    "sections": [
        {
            "id": "s1", "code": "§1", "lo": "Bodies &amp; the IV disc",
            "title": "Joints of the vertebral bodies &amp; the intervertebral disc", "tag": "The weight-bearing symphyses — and the disc that herniates.",
            "lead": "Adjacent bodies are joined by <strong>secondary cartilaginous joints (symphyses)</strong> — the intervertebral discs. Learn the disc's two parts and their behaviour, because the whole clinical story of back pain is the disc failing.",
            "blocks": [
                ("plate", 5, "The joints of the vertebral column", "The five families of vertebral joints"),
                ("box", "active", "Orientation · five families of joint", "Hold the full list as a scaffold: joints of the <strong>vertebral bodies</strong> (symphyses/discs), joints of the <strong>vertebral arches</strong> (facet joints), the <strong>craniovertebral</strong> joints (atlanto-occipital and atlantoaxial, §5), the <strong>costovertebral</strong> joints (ribs↔vertebrae, §6) and the <strong>sacroiliac</strong> joints. The rest of the lecture fills in each one."),
                ("grid", [
                    (6, "Bodies = secondary cartilaginous joints", "Symphysis: bone–cartilage–fibrocartilage–cartilage–bone"),
                    (7, "The intervertebral disc", "Anulus fibrosus around a nucleus pulposus"),
                ]),
                ("box", "why", "Why · the disc is a shock-absorber with two parts", "Each disc is a <strong>symphysis</strong> built for weight-bearing and strength. Its outer <strong>anulus fibrosus</strong> is concentric lamellae of <strong>fibrocartilage</strong> whose fibres run obliquely and cross at &gt;60° between layers — this lattice <strong>allows limited rotation while binding the bodies strongly</strong>. Its core, the <strong>nucleus pulposus</strong>, is a gelatinous, water-rich gel that takes the compressive load. Think of it as a water balloon (nucleus) inside a woven strap (anulus)."),
                ("grid", [
                    (8, "Nucleus pulposus", "Gelatinous, avascular, water-rich central core"),
                    (9, "Intervertebral disc — structure", "Lamellar anulus enclosing the nucleus"),
                ]),
                ("box", "why", "Why · an avascular gel that dries with age", "The <strong>nucleus pulposus</strong> is a <strong>semifluid gel</strong> that broadens when compressed and redistributes load — the source of much of the spine's flexibility and resilience. Two facts drive its pathology: it is <strong>avascular</strong> (it heals poorly) and it is <strong>water-rich at birth but dehydrates with age</strong>, so discs <strong>thin and stiffen</strong> over a lifetime. It sits <strong>centrally-to-posteriorly</strong> in the disc — which is exactly why herniation tends to go backwards."),
                ("grid", [
                    (10, "The IV discs across regions", "Disc thickness greatest in cervical and lumbar regions"),
                    (11, "Uncovertebral joints (of Luschka)", "Small synovial-like joints at the cervical uncinate processes"),
                ]),
                ("box", "clin", "Clinical · disc thickness and the uncovertebral joints", "Disc <strong>relative thickness is greatest in the cervical and lumbar regions</strong>, matching their larger ranges of movement, and in both it is <strong>thicker anteriorly</strong> (helping form the spine's forward curves). Note there is <strong>no disc between C1 and C2</strong>. The <strong>uncovertebral joints of Luschka</strong> form between the <strong>uncinate processes of C3–C6</strong> and the body above; they are considered synovial and are a common site of <strong>osteophytes</strong> that narrow the intervertebral foramen and pinch a cervical nerve root."),
            ],
            "recall": {"head": "Recall — bodies &amp; the disc", "items": [
                "<li><b>Body joints —</b> <b>secondary cartilaginous</b> joints (<b>symphyses</b>) = the IV discs</li>",
                "<li><b>Anulus fibrosus —</b> <b>fibrocartilage</b> lamellae, fibres cross &gt;<b>60°</b> → limits rotation</li>",
                "<li><b>Nucleus pulposus —</b> water-rich <b>gel</b>, <b>avascular</b>, dries with <b>age</b>, sits <b>posteriorly</b></li>",
                "<li><b>Thickest discs —</b> <b>cervical</b> &amp; <b>lumbar</b>; none between <b>C1/C2</b></li>",
                "<li><b>Uncovertebral joints —</b> at <b>C3–C6</b> uncinate processes; osteophytes pinch the root</li>",
            ]},
            "digest": {
                "key_points": [
                    "Vertebral body joints are secondary cartilaginous joints (symphyses) — the intervertebral discs.",
                    "The disc = outer anulus fibrosus (fibrocartilage lamellae with fibres crossing at >60°, limiting rotation) around a gelatinous nucleus pulposus.",
                    "The nucleus pulposus is avascular, water-rich at birth but dehydrates with age, and sits centrally-to-posteriorly (predisposing to posterior herniation).",
                    "Discs are thickest in the cervical and lumbar regions (thicker anteriorly); there is no disc between C1 and C2.",
                    "Uncovertebral joints of Luschka (C3–C6 uncinate processes) are synovial and a common osteophyte site narrowing the IV foramen.",
                ],
                "self_tests": [
                    {"q": "Name the two components of an intervertebral disc and their roles.", "a": "The anulus fibrosus (fibrocartilage lamellae binding the bodies and limiting rotation) and the nucleus pulposus (water-rich gel bearing compressive load)."},
                    {"q": "Why do intervertebral discs degenerate with age?", "a": "The nucleus pulposus is avascular and loses water content over time, so discs thin, stiffen and lose their shock-absorbing turgor."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "Longitudinal ligaments &amp; facet joints",
            "title": "Longitudinal ligaments &amp; facet joints", "tag": "Two straps that check opposite movements, and the gliding arch joints.",
            "lead": "The two long ligaments on the front and back of the bodies are a tidy pair: one stops you over-arching, the other stops you over-folding. The facet (zygapophyseal) joints add the gliding that sets each region's range.",
            "blocks": [
                ("grid", [
                    (12, "Anterior longitudinal ligament", "Broad strong band on the fronts of the bodies"),
                    (13, "ALL stretching — whiplash", "Hyperextension severely stretches the ALL"),
                ]),
                ("box", "clin", "Clinical · the ALL prevents hyperextension", "The <strong>anterior longitudinal ligament</strong> is a <strong>broad, strong</strong> band running down the <strong>front</strong> of the bodies and discs, from the sacrum to C1/occiput — the <em>only</em> ligament that <strong>limits extension (and prevents hyperextension)</strong>. In a <strong>whiplash</strong> hyperextension injury it is <strong>severely stretched</strong> and can avulse a fragment from the vertebral body. It is also the one long ligament strong enough to resist the pull."),
                ("plate", 14, "Posterior longitudinal ligament", "Narrow weaker band inside the vertebral canal"),
                ("box", "why", "Why · the PLL is weaker — and that matters", "The <strong>posterior longitudinal ligament</strong> runs inside the <strong>vertebral canal</strong> on the <strong>backs of the bodies</strong> (C2→sacrum) and <strong>prevents hyperflexion</strong> — the mirror of the ALL. But it is <strong>much narrower and weaker</strong>, and it <strong>tapers laterally</strong>, leaving the <strong>posterolateral disc unguarded</strong>. That weak flank is precisely where a nucleus pulposus herniates — explaining why disc protrusions characteristically go <strong>posterolaterally</strong> onto a nerve root rather than straight back."),
                ("grid", [
                    (15, "Facet (zygapophyseal) joints", "Plane synovial joints between articular processes"),
                    (16, "Lumbar spine — assembled", "Facets, discs and ligaments together in the lumbar spine"),
                ]),
                ("box", "mnem", "Exam hook · facet joints set the regional range", "<strong>Facet (zygapophyseal) joints</strong> are <strong>plane synovial joints</strong> between the superior and inferior articular processes, enclosed in a thin capsule and permitting <strong>gliding</strong>. Their <strong>plane of orientation is what sets each region's movement</strong> (from L19): near-horizontal in the neck (free movement), coronal in the thorax (rotation), sagittal in the lumbar spine (flexion, no rotation). Being synovial, they are a site of <strong>osteoarthritis</strong> and a source of mechanical back pain."),
            ],
            "recall": {"head": "Recall — long ligaments &amp; facets", "items": [
                "<li><b>Anterior longitudinal ligament —</b> broad/strong, on the <b>front</b> → prevents <b>hyperextension</b></li>",
                "<li><b>Posterior longitudinal ligament —</b> narrow/<b>weak</b>, in the canal → prevents <b>hyperflexion</b></li>",
                "<li><b>PLL weak point —</b> <b>posterolateral</b> → the route of disc <b>herniation</b></li>",
                "<li><b>Facet joints —</b> <b>plane synovial</b>; their <b>orientation</b> sets the regional movement</li>",
            ]},
            "digest": {
                "key_points": [
                    "The anterior longitudinal ligament is a broad, strong band on the front of the bodies that prevents hyperextension (stretched/avulsed in whiplash).",
                    "The posterior longitudinal ligament runs inside the canal on the back of the bodies, prevents hyperflexion, but is narrow and weak and tapers laterally — leaving the posterolateral disc unguarded (the herniation route).",
                    "Facet (zygapophyseal) joints are plane synovial joints whose orientation sets each region's range of movement; they are sites of osteoarthritis.",
                ],
                "self_tests": [
                    {"q": "Which movement does each longitudinal ligament prevent?", "a": "The anterior longitudinal ligament prevents hyperextension; the posterior longitudinal ligament prevents hyperflexion."},
                    {"q": "Why do intervertebral disc herniations typically occur posterolaterally?", "a": "The posterior longitudinal ligament is narrow and tapers laterally, leaving the posterolateral anulus relatively unsupported, so the nucleus herniates there onto a nerve root."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "Cord level &amp; the clinical disc",
            "title": "Spinal cord level, disc herniation &amp; lumbar puncture", "tag": "Why the cord ends high — and the three clinical set-pieces.",
            "lead": "This section is pure clinic. One developmental fact (the cord ends higher than the column) explains both why herniations compress the nerves they do and why a lumbar puncture is safe low down.",
            "blocks": [
                ("plate", 17, "Vertebral column vs spinal cord", "The cord ends at L1/L2 because the column outgrows it"),
                ("box", "why", "Why · the column outgrows the cord", "After birth the <strong>vertebral column grows faster than the spinal cord</strong>, so the cord's lower end \"ascends\" relative to the bones — ending at <strong>L1/L2 in adults</strong> (vs L2/L3 in the newborn). Two consequences: the <strong>spinal nerves must travel down inside the canal</strong> to reach their exit foramina (forming the <strong>cauda equina</strong> below the cord), and the <strong>sac of CSF continues to ~S2</strong> — the anatomical basis for the two clinical scenarios below."),
                ("grid", [
                    (18, "Disc protrusion", "Herniation of nucleus pulposus through the anulus"),
                    (19, "Nerve compression by region", "Cervical vs lumbar root compression differs"),
                ]),
                ("box", "clin", "Clinical · herniation — levels and which root", "<strong>Herniation</strong> of the nucleus through the anulus is a top cause of low-back pain, commonest at <strong>L4/5 and L5/S1</strong>. Mechanism: <strong>flexion drives the nucleus posteriorly</strong> where the anulus is thin (and the PLL weak), especially once age has dried the disc (in the young, the vertebra often fractures before the disc ruptures). The <em>root</em> hit depends on region: the <strong>small cervical IV foramen</strong> means a cervical protrusion usually compresses the root <strong>exiting at that level</strong>; in the lumbar spine the <strong>large foramen spares the exiting root</strong>, but the herniation catches the root <strong>descending to the level below</strong> (e.g. an L4/5 disc typically hits the L5 root)."),
                ("plate", 20, "Lumbar puncture", "CSF is sampled safely below the cord at L3/4 or L4/5"),
                ("box", "clin", "Clinical · why the needle goes in low", "Because the cord ends at <strong>L1/L2</strong>, a needle placed at <strong>L3/4 or L4/5</strong> (found at the iliac-crest/supracristal plane, L19) enters the <strong>lumbar cistern below the cord</strong>, where the mobile <strong>cauda equina</strong> nerve roots float aside rather than being speared — so CSF can be withdrawn safely. In <strong>infants the cord ends lower (L2/L3)</strong>, so the puncture <strong>must be done below L3</strong>. This is the clinical pay-off of the cord-level slide."),
            ],
            "recall": {"head": "Recall — cord level &amp; clinical disc", "items": [
                "<li><b>Adult cord ends —</b> <b>L1/L2</b>; below is the <b>cauda equina</b></li>",
                "<li><b>Herniation driver —</b> <b>flexion</b> pushes nucleus <b>posteriorly</b>; commonest <b>L4/5, L5/S1</b></li>",
                "<li><b>Lumbar disc —</b> spares the exiting root, hits the one <b>descending</b> to the level below</li>",
                "<li><b>Lumbar puncture —</b> <b>L3/4 or L4/5</b> (below the cord); in infants, <b>below L3</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The vertebral column grows faster than the cord after birth, so the cord ends at L1/L2 in adults (L2/L3 in newborns); nerves descend as the cauda equina and the CSF sac continues to ~S2.",
                    "Disc herniation is driven by flexion pushing the nucleus posteriorly through a thin anulus; commonest at L4/5 and L5/S1.",
                    "Cervical herniation (small foramen) compresses the root exiting at that level; a lumbar herniation spares the exiting root and compresses the root descending to the level below.",
                    "Lumbar puncture is performed at L3/4 or L4/5 (below the adult cord), and below L3 in infants whose cord ends lower.",
                ],
                "self_tests": [
                    {"q": "Why can a lumbar puncture be performed safely at L3/4?", "a": "The spinal cord ends at L1/L2 in adults, so at L3/4 the needle enters the lumbar cistern below the cord where the cauda equina nerve roots float aside."},
                    {"q": "An L4/5 disc herniation most often compresses which nerve root, and why?", "a": "The L5 root — the large lumbar foramen spares the exiting L4 root, but the posterolateral herniation catches the root descending to the level below."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "Accessory ligaments",
            "title": "Accessory ligaments of the arches", "tag": "The posterior ligaments that check flexion and hold the curve.",
            "lead": "Behind the bodies, a set of ligaments ties the arches together — chiefly resisting flexion and helping restore the upright posture. The elastic ligamentum flavum is the star.",
            "blocks": [
                ("plate", 21, "Accessory ligaments — the set", "Ligamenta flava, interspinous, supraspinous, nuchae, intertransverse"),
                ("plate", 22, "Ligamentum flavum", "Elastic yellow ligament joining adjacent laminae"),
                ("box", "why", "Why · the elastic one that snaps you upright", "The <strong>ligamentum flavum</strong> (\"yellow ligament\") joins adjacent <strong>laminae</strong> and forms part of the <strong>posterior wall of the vertebral canal</strong>. It is unusually rich in <strong>elastin</strong>, so it is stretched during flexion and <strong>recoils to help straighten the spine</strong> and preserve the normal curve. It is <strong>thickest in the lumbar region</strong> — clinically, it is the last ligament a lumbar-puncture needle pierces before the dura, and its <strong>hypertrophy</strong> is a cause of spinal canal stenosis."),
                ("grid", [
                    (23, "Interspinous, supraspinous, intertransverse", "Ligaments between spines and transverse processes"),
                    (24, "Ligamentum nuchae", "Fibroelastic midline sheet in the neck"),
                ]),
                ("box", "mnem", "Exam hook · match each to the gap it spans", "Name them by what they connect: <strong>interspinous</strong> (between adjacent spinous processes — thin, weak); <strong>supraspinous</strong> (along the <em>tips</em> of the spines, C7→sacrum — strong, cord-like); <strong>intertransverse</strong> (between transverse processes). In the neck the supraspinous/interspinous ligaments merge into the <strong>ligamentum nuchae</strong>, a strong fibroelastic midline sheet from the external occipital protuberance to the cervical spines that <strong>supports the head and gives muscle attachment</strong> (compensating for the short cervical spinous processes). All of these chiefly <strong>check flexion</strong>."),
            ],
            "recall": {"head": "Recall — accessory ligaments", "items": [
                "<li><b>Ligamentum flavum —</b> <b>elastic</b>, joins <b>laminae</b>; recoils to <b>straighten</b> the spine; thickest <b>lumbar</b></li>",
                "<li><b>Supraspinous —</b> strong, along spinous <b>tips</b> (C7→sacrum)</li>",
                "<li><b>Interspinous —</b> thin/weak, <b>between</b> spines</li>",
                "<li><b>Ligamentum nuchae —</b> neck's <b>fibroelastic</b> sheet; head support + muscle attachment</li>",
                "<li><b>Common job —</b> these mostly <b>limit flexion</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The ligamentum flavum is an elastic ligament joining adjacent laminae; it forms part of the posterior canal wall, recoils to help straighten the spine, is thickest in the lumbar region, and can hypertrophy to cause stenosis.",
                    "Interspinous ligaments (thin, between spines), supraspinous ligament (strong, along the spinous tips C7–sacrum) and intertransverse ligaments connect the arches and chiefly limit flexion.",
                    "The ligamentum nuchae is a fibroelastic midline sheet in the neck that supports the head and provides muscle attachment.",
                ],
                "self_tests": [
                    {"q": "What is special about the ligamentum flavum's composition, and what does it do?", "a": "It is elastin-rich, so it recoils after flexion to help straighten the spine and maintain its curve; it also forms part of the posterior wall of the vertebral canal."},
                    {"q": "Which accessory ligament is strong and runs along the tips of the spinous processes?", "a": "The supraspinous ligament (C7 to the sacrum; it merges with the ligamentum nuchae in the neck)."},
                ],
            },
        },
        {
            "id": "s5", "code": "§5", "lo": "Craniovertebral joints",
            "title": "Craniovertebral joints &amp; their ligaments", "tag": "The two joints that nod and shake the head — and the ligaments that stop the dens killing you.",
            "lead": "The skull meets the spine at two highly specialised joints: one says \"yes\", the other says \"no\". A dedicated ligament complex holds the dens away from the cord — and its failure is catastrophic.",
            "blocks": [
                ("plate", 26, "The craniovertebral joints", "Atlanto-occipital and atlantoaxial joints"),
                ("grid", [
                    (27, "Atlanto-occipital joint — \"yes\"", "Condyloid synovial joint for nodding"),
                    (28, "Atlantoaxial joints — \"no\"", "Median pivot + two lateral plane joints for rotation"),
                ]),
                ("box", "mnem", "Exam hook · yes vs no, and the joint types", "<strong>Atlanto-occipital joint</strong> (occipital condyles on the atlas): <strong>synovial condyloid</strong> → mainly <strong>flexion/extension</strong>, the <strong>\"YES\" nod</strong>. <strong>Atlantoaxial joint</strong> has <strong>three parts</strong> — a <strong>median</strong> <strong>synovial pivot</strong> (dens of C2 in the ring of C1) and <strong>two lateral plane (zygapophyseal)</strong> joints → <strong>rotation</strong>, the <strong>\"NO\" shake</strong>. Match joint type to movement and this slide is yours."),
                ("plate", 30, "Fractures &amp; dislocations of the axis", "Dens fracture and hangman's fracture risk the cord"),
                ("box", "clin", "Clinical · why these fractures are lethal", "The dens sits <strong>millimetres from the spinal cord/brainstem</strong>, so axis injuries are dangerous. A <strong>dens (odontoid) fracture</strong> — classically a fall onto the head — can displace and injure the cord, causing <strong>quadriplegia</strong>. A fracture through the <strong>pars interarticularis of C2</strong> — the <strong>hangman's fracture</strong> — can likewise injure the cord or brainstem and be rapidly fatal. The ligaments below are what normally keep the dens off the cord."),
                ("grid", [
                    (38, "Craniovertebral ligaments — cruciate", "Transverse ligament of the atlas and longitudinal bands"),
                    (39, "Alar, apical &amp; tectorial", "Alar ligaments, apical ligament and tectorial membrane"),
                ]),
                ("box", "why", "Why · the ligaments that cage the dens", "A dedicated complex restrains the dens. The <strong>transverse ligament of the atlas</strong> straps the dens against the anterior arch of C1 — its <strong>superior and inferior longitudinal bands</strong> make the <strong>cruciate ligament</strong>, holding the dens <em>off</em> the cord. The <strong>alar ligaments</strong> (dens → occipital condyles) <strong>check rotation</strong> of the head; the <strong>apical ligament</strong> tips the dens to the foramen magnum; and the <strong>tectorial membrane</strong> (the upward continuation of the PLL) roofs the whole complex. Rupture of the transverse ligament (e.g. in rheumatoid arthritis) lets the dens compress the cord — the reason atlantoaxial instability is screened before intubating such patients."),
            ],
            "recall": {"head": "Recall — craniovertebral joints", "items": [
                "<li><b>Atlanto-occipital —</b> condyloid → <b>flexion/extension</b> (the <b>\"yes\"</b>)</li>",
                "<li><b>Atlantoaxial —</b> median <b>pivot</b> + 2 lateral plane → <b>rotation</b> (the <b>\"no\"</b>)</li>",
                "<li><b>Dens fracture —</b> fall on head → cord injury → <b>quadriplegia</b></li>",
                "<li><b>Transverse ligament —</b> holds the <b>dens</b> off the cord (cruciate with longitudinal bands)</li>",
                "<li><b>Alar ligaments —</b> dens → occipital condyles; <b>limit rotation</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The atlanto-occipital joint is a synovial condyloid joint giving flexion/extension (the 'yes' nod).",
                    "The atlantoaxial joint has three parts (a median synovial pivot of the dens plus two lateral plane joints) giving rotation (the 'no' shake).",
                    "Dens (odontoid) fracture from a fall on the head can cause quadriplegia; a hangman's fracture through the C2 pars can injure the cord/brainstem fatally.",
                    "The transverse ligament of the atlas holds the dens against the anterior arch of C1 (forming the cruciate ligament with the longitudinal bands); the alar ligaments check rotation; the tectorial membrane continues the PLL over the complex.",
                ],
                "self_tests": [
                    {"q": "Which craniovertebral joint produces the 'no' head shake and what type is it?", "a": "The atlantoaxial joint — a median synovial pivot (dens in the atlas ring) with two lateral plane joints, producing rotation."},
                    {"q": "What does the transverse ligament of the atlas do, and why does its rupture matter?", "a": "It holds the dens against the anterior arch of C1, keeping it off the spinal cord; rupture (e.g. in rheumatoid arthritis) causes atlantoaxial instability and cord compression."},
                ],
            },
        },
        {
            "id": "s6", "code": "§6", "lo": "Thoracic wall joints",
            "title": "Joints of the thoracic wall", "tag": "Ribs to vertebrae, ribs to sternum — and the two ways the chest expands.",
            "lead": "The ribs articulate behind with the vertebrae and in front with the sternum, and the joint types dictate how the thoracic cage moves in breathing. Finish with the pump-handle and bucket-handle movements.",
            "blocks": [
                ("grid", [
                    (32, "Joints of the thoracic wall — the set", "Costovertebral, costochondral, sternocostal and sternal joints"),
                    (33, "Costovertebral &amp; costotransverse joints", "Rib head to body; rib tubercle to transverse process"),
                ]),
                ("box", "why", "Why · two posterior rib joints set the axis of motion", "Each rib joins the spine at <strong>two synovial joints</strong>: the <strong>costovertebral</strong> joint (rib <em>head</em> to the bodies — usually two adjacent bodies and the disc between) and the <strong>costotransverse</strong> joint (rib <em>tubercle</em> to the transverse process). Together they define the <strong>axis</strong> around which the rib swings in breathing — the mechanical basis for the pump-/bucket-handle movements below."),
                ("grid", [
                    (34, "Sternum &amp; its joints", "Manubriosternal symphysis, sternoclavicular saddle joint"),
                    (35, "Rib–sternum joints", "Costochondral, interchondral and sternocostal joints"),
                ]),
                ("box", "mnem", "Exam hook · name the joint type for each articulation", "Classify them cleanly: <strong>costochondral</strong> (rib↔its own cartilage) = <strong>primary cartilaginous</strong>, no movement; <strong>1st sternocostal</strong> = <strong>fibrocartilaginous (primary cartilaginous)</strong> — immobile; <strong>2nd–7th sternocostal</strong> and the <strong>interchondral</strong> joints = <strong>plane synovial</strong>; the <strong>manubriosternal</strong> joint = <strong>secondary cartilaginous (symphysis)</strong> and marks the palpable <strong>sternal angle (of Louis)</strong> at the 2nd rib; the <strong>sternoclavicular</strong> joint = <strong>saddle synovial</strong>. The manubriosternal and xiphisternal joints often fuse (synostosis) with age."),
                ("plate", 36, "Movements of the thoracic wall", "Pump-handle and bucket-handle rib movements"),
                ("box", "why", "Why · pump handle vs bucket handle", "Quiet breathing is run by the <strong>diaphragm and intercostals</strong>; accessory muscles amplify two rib motions. The <strong>pump-handle</strong> movement raises the <strong>upper ribs/sternum forward and up</strong>, increasing the <strong>antero-posterior</strong> chest diameter; the <strong>bucket-handle</strong> movement raises the <strong>lateral shafts of the lower ribs</strong>, increasing the <strong>transverse</strong> diameter. Both enlarge the thorax, drop intrathoracic pressure and draw air in — the kinematics behind the respiratory anatomy you meet in MHHS2402."),
            ],
            "recall": {"head": "Recall — thoracic wall joints", "items": [
                "<li><b>Costovertebral —</b> rib <b>head</b> ↔ bodies; <b>costotransverse —</b> rib <b>tubercle</b> ↔ transverse process</li>",
                "<li><b>Costochondral —</b> <b>primary cartilaginous</b> (no movement)</li>",
                "<li><b>Sternocostal 2–7 —</b> <b>plane synovial</b>; 1st = fibrocartilaginous</li>",
                "<li><b>Manubriosternal —</b> <b>symphysis</b> = the <b>sternal angle</b> (rib 2)</li>",
                "<li><b>Breathing —</b> <b>pump handle</b> (AP ↑), <b>bucket handle</b> (transverse ↑)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Each rib joins the spine via two synovial joints: costovertebral (rib head to bodies) and costotransverse (rib tubercle to transverse process), which set the rib's axis of movement.",
                    "Joint types anteriorly: costochondral = primary cartilaginous (immobile); 1st sternocostal = fibrocartilaginous; 2nd–7th sternocostal and interchondral = plane synovial; sternoclavicular = saddle synovial.",
                    "The manubriosternal joint is a symphysis marking the sternal angle (level of rib 2); it and the xiphisternal joint often fuse with age.",
                    "Breathing uses pump-handle movement (raises sternum, increases AP diameter) and bucket-handle movement (raises lateral rib shafts, increases transverse diameter).",
                ],
                "self_tests": [
                    {"q": "Name the two joints a typical rib makes with the vertebral column.", "a": "The costovertebral joint (rib head with the vertebral bodies and intervening disc) and the costotransverse joint (rib tubercle with the transverse process)."},
                    {"q": "Distinguish pump-handle from bucket-handle rib movement.", "a": "Pump-handle raises the sternum and upper ribs forward/up to increase the antero-posterior diameter; bucket-handle elevates the lateral shafts of the lower ribs to increase the transverse diameter."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
