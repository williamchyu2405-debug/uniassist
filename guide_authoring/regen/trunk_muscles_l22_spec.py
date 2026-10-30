#!/usr/bin/env python3
"""L22 — Muscles of the trunk. MHHS2401. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/trunk1"

SPEC = {
    "slug": "trunk_muscles_mhhs2401_l22",
    "workdir": WD,
    "unit": "MHHS2401",
    "subject": "Musculoskeletal System",
    "week": 12,
    "title": "Muscles of the Trunk",
    "source": "MHHS2401 Lecture 22 — Muscles of the trunk, Dr Mirjana Strkalj (Macquarie University)",
    "brand": "MHHS2401 · L22 · Trunk",
    "brandsub": "Muscles of<br>the Trunk",
    "eyebrow": "MHHS2401 · Musculoskeletal System · Lecture 22",
    "h1": "Muscles of the Trunk",
    "h1thin": "thoracic wall, abdominal wall, and how the spine moves",
    "lede": "Every lecture slide is shown in full and explained the way a tutor would. The lecture wraps the trunk in two layers: the <strong>thoracic wall</strong>, where intercostal muscles close the gaps between ribs and move them for breathing, and the <strong>abdominal wall</strong>, where three flat muscles cross at angles like plywood and their aponeuroses wrap the rectus abdominis. It then brings back the back muscles from L21 to explain why each region of the spine moves the way it does.",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The note underneath is <b>not a re-caption</b>. It adds the action, the nerve, and the clinical or landmark point. For every muscle ask three things: what does it attach to, what does it do, and which nerve supplies it? For the spine, ask what <em>limits</em> movement in that region.",
    "n_slides": 23,
    "sections": [
        {
            "id": "s1", "code": "§1", "lo": "LO1 · Muscles of the thoracic wall",
            "title": "The thoracic wall and its muscles", "tag": "A ribbed cylinder closed by muscle, moved for breathing.",
            "lead": "The trunk is the body minus the head, neck and limbs. Its upper part, the thorax, is a cage of ribs whose gaps are filled by three layers of intercostal muscle, with the nerves and vessels running in a protected groove.",
            "blocks": [
                ("plate", 5, "The trunk — skeleton and walls", "Thoracic cage, lumbar spine and pelvis; abdominal wall muscles shown on the right"),
                ("box", "active", "Orientation · bone above, muscle below", "Slide 5 is the map for the whole lecture. Above the <strong>costal margin</strong>, the trunk wall is mostly <strong>bone</strong> (ribs) with muscle in the gaps. Between the costal margin and the <strong>pelvis</strong> (iliac crest, inguinal ligament) there is almost no bone, so the <strong>abdominal wall is entirely muscle and aponeurosis</strong>: external oblique, internal oblique, transversus abdominis, rectus abdominis, with quadratus lumborum, psoas major and iliacus behind. That difference explains why the abdomen can expand (eating, pregnancy, breathing) and the chest can't."),
                ("plate", 6, "The thorax", "An irregular cylinder; superior and inferior thoracic apertures; diaphragm; pleural cavities and mediastinum"),
                ("box", "why", "Why · a cylinder with a lid and a floor", "The thorax is an <strong>irregularly shaped cylinder</strong>. It has a <strong>narrow superior thoracic aperture</strong> (rib 1, manubrium, T1), through which trachea, oesophagus and great vessels pass to the neck, and a <strong>wide inferior thoracic aperture</strong> closed by the musculotendinous <strong>diaphragm</strong>. Its <strong>musculoskeletal wall</strong> protects heart and lungs while still moving for breathing. Inside are three compartments: the <strong>left and right pleural cavities</strong> (lungs) and the central <strong>mediastinum</strong> (heart, great vessels, oesophagus, trachea)."),
                ("plate", 7, "Muscles attached to the thoracic wall", "Pectoralis major and minor, subclavius, serratus anterior; serratus posterior and levatores costarum as accessory respiratory muscles"),
                ("box", "mnem", "Exam hook · muscles that sit on the chest but aren't \"thoracic wall\"", "Several <strong>upper-limb</strong> muscles attach to the ribs: <strong>pectoralis major, pectoralis minor, subclavius, serratus anterior</strong> (shoulder lectures, wk1). With the arm fixed (e.g. hands on knees), they can lift the ribs, which is why breathless patients brace their arms (the \"tripod position\"). <strong>Serratus posterior</strong> (superior and inferior) and <strong>levatores costarum</strong>, deep back muscles, are <strong>accessory respiratory muscles</strong>. The true thoracic wall muscles are the intercostals, subcostales and transversus thoracis."),
                ("plate", 8, "Intercostal spaces", "External, internal and innermost intercostals; the neurovascular bundle in the costal groove"),
                ("box", "why", "Why · three layers, and a protected groove", "Each <strong>intercostal space</strong> is closed by three muscle layers. <strong>External intercostals</strong> run down and forward (the \"hands in pockets\" direction) and mainly <strong>elevate ribs</strong> (inspiration). <strong>Internal intercostals</strong> run at right angles to them and mainly <strong>depress ribs</strong> (forced expiration). <strong>Innermost intercostals</strong> run in the same direction as the internal layer. The <strong>intercostal nerve, artery and vein</strong> run in the <strong>costal groove on the lower border of the rib above</strong>, between the internal and innermost layers, in the order <strong>V-A-N</strong> (vein, artery, nerve) from top to bottom. All intercostal muscles are supplied by <strong>intercostal nerves</strong> (anterior rami T1–T11)."),
                ("box", "clin", "Clinical · where to put the needle", "Because the neurovascular bundle hugs the <strong>inferior border</strong> of each rib, chest drains and pleural taps go in <strong>just above the upper border of the rib below</strong>, avoiding the vessels and nerve. The safe site for a chest drain is the \"triangle of safety\" in the 4th–5th intercostal space, mid-axillary line. An <strong>intercostal nerve block</strong> is placed at the lower border of the rib for rib-fracture pain."),
                ("plate", 9, "Subcostales and transversus thoracis", "Subcostales posteriorly elevate ribs; transversus thoracis anteriorly depresses ribs"),
                ("box", "why", "Why · the innermost layer's extensions", "Both lie in the same plane as the <strong>innermost intercostals</strong>, completing the deepest layer. <strong>Subcostales</strong> lie on the inner <strong>posterior</strong> wall, are more numerous lower down, and can span <strong>more than one intercostal space</strong>; they <strong>elevate ribs</strong>. <strong>Transversus thoracis</strong> lies on the deep surface of the <strong>anterior</strong> wall (from sternum to costal cartilages), <strong>deep to the internal thoracic vessels</strong>, which it holds against the wall; it <strong>depresses ribs</strong>. Both are supplied by intercostal nerves."),
            ],
            "recall": {"head": "Recall — thoracic wall", "items": [
                "<li><b>Thoracic cavity compartments —</b> <b>two pleural cavities</b> and the <b>mediastinum</b></li>",
                "<li><b>Inferior thoracic aperture is closed by —</b> the <b>diaphragm</b></li>",
                "<li><b>Upper-limb muscles attached to ribs —</b> <b>pectoralis major/minor</b>, <b>subclavius</b>, <b>serratus anterior</b></li>",
                "<li><b>Accessory respiratory back muscles —</b> <b>serratus posterior</b>, <b>levatores costarum</b></li>",
                "<li><b>Intercostal neurovascular bundle runs between —</b> <b>internal</b> and <b>innermost</b> intercostals, in the <b>costal groove</b></li>",
                "<li><b>Order in the costal groove (top to bottom) —</b> <b>vein, artery, nerve</b></li>",
                "<li><b>Subcostales —</b> posterior wall, <b>elevate ribs</b></li>",
                "<li><b>Transversus thoracis —</b> anterior wall, deep to internal thoracic vessels, <b>depresses ribs</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The thorax is an irregular cylinder with a narrow superior thoracic aperture and a large inferior aperture closed by the diaphragm; its cavity has left and right pleural cavities and the mediastinum.",
                    "Upper limb muscles attaching to ribs: pectoralis major, pectoralis minor, subclavius, serratus anterior; serratus posterior and levatores costarum are accessory respiratory muscles.",
                    "Intercostal muscles close the spaces between ribs; intercostal nerves, arteries and veins lie in the costal groove along the inferior margin of the superior rib, between the internal and innermost intercostals.",
                    "Subcostales: same plane as innermost intercostals, more numerous in the lower posterior wall, may span more than one space, elevate ribs. Transversus thoracis: deep surface of anterior wall, deep to internal thoracic vessels, depresses ribs.",
                    "Intercostal, subcostal and transversus thoracis muscles are supplied by intercostal nerves.",
                ],
                "self_tests": [
                    {"q": "Where does the intercostal neurovascular bundle run, and why does it matter clinically?", "a": "In the costal groove on the inferior margin of the rib above, between internal and innermost intercostals; needles are inserted just above the rib below to avoid it."},
                    {"q": "Contrast the location and action of subcostales and transversus thoracis.", "a": "Subcostales: posterior thoracic wall, elevate ribs. Transversus thoracis: deep anterior wall, deep to internal thoracic vessels, depress ribs."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "LO2 · Abdominal wall — structure",
            "title": "Layers of the abdominal wall and its posterior muscles", "tag": "From skin to peritoneum, and the muscles that line the back of the abdomen.",
            "lead": "The abdominal wall is built in layers, and those layers are the order you cut through in surgery. Its muscles fall into posterior, lateral (anterolateral) and anterior groups.",
            "blocks": [
                ("plate", 11, "Layers and skeletal frame of the abdominal wall", "Skin, superficial fascia, muscles with deep fascia, extraperitoneal fat, parietal peritoneum; lumbar vertebrae, pelvis, lower thoracic cage"),
                ("box", "mnem", "Exam hook · the layers, outside to in", "<strong>Skin → superficial fascia</strong> (fatty Camper's and membranous Scarpa's layers) <strong>→ muscles and their deep fascia → transversalis fascia → extraperitoneal fat → parietal peritoneum</strong>. Its <strong>skeletal frame</strong> is the <strong>5 lumbar vertebrae and IV discs</strong> behind, the <strong>upper pelvic bones</strong> below, and the <strong>lower thoracic cage</strong> above. A midline incision passes through only skin, fascia, the linea alba, transversalis fascia, fat and peritoneum, with no muscle fibres, which is why it bleeds little."),
                ("plate", 12, "Muscle groups of the abdominal wall", "Posterior: quadratus lumborum, psoas major, iliacus; lateral: external oblique, internal oblique, transversus abdominis; anterior: rectus abdominis"),
                ("box", "why", "Why · one continuous wall of different muscles", "<strong>Posterior</strong> (beside the vertebral column): <strong>quadratus lumborum, psoas major, iliacus</strong>. <strong>Lateral (anterolateral)</strong>: three layers, <strong>external oblique, internal oblique, transversus abdominis</strong>. <strong>Anterior</strong>: the segmented <strong>rectus abdominis</strong>. They are joined into one continuous wall by <strong>fascia</strong> posteriorly (thoracolumbar fascia) and by the flat tendinous sheets (<strong>aponeuroses</strong>) of the lateral muscles anteriorly. A <strong>fascial layer</strong> (transversalis fascia) separates the muscles from the peritoneum."),
                ("plate", 13, "Posterior abdominal wall muscles", "Psoas major and minor, quadratus lumborum, iliacus; anterior and posterior views"),
                ("box", "mnem", "Exam hook · posterior wall: attachments, action, nerve", "<strong>Psoas major</strong>: from the T12–L5 vertebral bodies, discs and transverse processes, to the <strong>lesser trochanter</strong>. It <strong>flexes the hip</strong> (with iliacus as <em>iliopsoas</em>) and flexes the trunk (bilaterally) or bends it laterally. Nerve: <strong>anterior rami L1–L3</strong>. <strong>Psoas minor</strong> (absent in ~40%) is a weak trunk flexor. <strong>Iliacus</strong>: from the iliac fossa to the lesser trochanter with psoas, hip flexor, supplied by the <strong>femoral nerve</strong>. <strong>Quadratus lumborum</strong>: from the iliac crest and iliolumbar ligament to <strong>rib 12</strong> and the lumbar transverse processes. It <strong>fixes rib 12</strong> in inspiration and <strong>laterally flexes</strong> the trunk. Nerve: <strong>anterior rami T12–L4</strong>."),
                ("box", "clin", "Clinical · the psoas sign", "Psoas lies directly behind the appendix (right) and the kidneys. When an <strong>inflamed appendix</strong> or a <strong>psoas abscess</strong> irritates it, extending the hip stretches psoas and causes pain (the <strong>psoas sign</strong>), and patients lie with the hip flexed. A psoas abscess (classically spinal TB) can track down within the psoas sheath and appear as a lump in the groin below the inguinal ligament."),
            ],
            "recall": {"head": "Recall — abdominal wall structure", "items": [
                "<li><b>Deepest layer of the abdominal wall —</b> <b>parietal peritoneum</b></li>",
                "<li><b>Abdominal wall skeletal elements —</b> <b>5 lumbar vertebrae</b>, upper <b>pelvic bones</b>, lower <b>thoracic cage</b></li>",
                "<li><b>Posterior wall muscles —</b> <b>quadratus lumborum</b>, <b>psoas major</b>, <b>iliacus</b></li>",
                "<li><b>Three lateral layers —</b> <b>external oblique</b>, <b>internal oblique</b>, <b>transversus abdominis</b></li>",
                "<li><b>Anterior segmented muscle —</b> <b>rectus abdominis</b></li>",
                "<li><b>Psoas major nerve —</b> anterior rami <b>L1–L3</b></li>",
                "<li><b>Quadratus lumborum attaches to —</b> <b>rib 12</b> and <b>iliac crest</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The abdominal wall consists of skin, superficial fascia, muscles and their deep fascia, extraperitoneal fat and parietal peritoneum; skeletal elements are the 5 lumbar vertebrae and IV discs, superior pelvic bones and inferior thoracic cage.",
                    "Posterior abdominal wall muscles lie lateral to the vertebral column: quadratus lumborum, psoas major (and minor) and iliacus.",
                    "Lateral (anterolateral) wall has 3 layers: external oblique, internal oblique, transversus abdominis; anterior wall has the segmented rectus abdominis.",
                    "Structural continuity is provided by fascia posteriorly and aponeuroses of the lateral muscles anteriorly; a fascial layer separates the wall from the peritoneum.",
                ],
                "self_tests": [
                    {"q": "List the layers of the anterior abdominal wall from superficial to deep.", "a": "Skin, superficial fascia, muscles with deep fascia (and transversalis fascia), extraperitoneal fat, parietal peritoneum."},
                    {"q": "Name the posterior abdominal wall muscles.", "a": "Psoas major (and minor), quadratus lumborum, iliacus."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "LO2 · Anterolateral muscles, aponeuroses and rectus sheath",
            "title": "The anterolateral abdominal muscles and the rectus sheath", "tag": "Three flat muscles crossing like plywood, wrapped around a central strap.",
            "lead": "Five muscles make up the anterolateral wall. Three flat sheets become aponeuroses near the midline, and those aponeuroses form the rectus sheath around the two vertical muscles.",
            "blocks": [
                ("plate", 14, "Anterior abdominal wall muscles", "Three flat muscles become aponeuroses toward the midline; rectus abdominis and pyramidalis lie in the sheath"),
                ("box", "why", "Why · fibres at three angles make a strong wall", "The <strong>three flat muscles</strong> start posterolaterally and run forward, becoming <strong>aponeuroses</strong> toward the midline. <strong>External oblique</strong> fibres run down and medially (\"hands in pockets\"). <strong>Internal oblique</strong> fibres run up and medially, at right angles to the external oblique. <strong>Transversus abdominis</strong> fibres run horizontally. Like plywood, the crossed layers resist forces from every direction, which makes a thin but strong, flexible wall. Near the midline lie <strong>two vertical muscles</strong> enclosed in a tendinous sheath: <strong>rectus abdominis</strong> and the small <strong>pyramidalis</strong> (which tenses the linea alba and is absent in some people)."),
                ("plate", 15, "Actions of the anterolateral muscles", "All compress and support viscera and assist respiration; obliques flex and rotate; transversus compresses; rectus flexes the trunk"),
                ("box", "mnem", "Exam hook · actions and nerves", "<strong>All four</strong> compress and support the abdominal viscera and assist (forced) <strong>expiration</strong>, by raising intra-abdominal pressure and pushing the diaphragm up. <strong>External and internal obliques</strong> <strong>flex and rotate</strong> the trunk. <strong>Transversus abdominis</strong> <strong>compresses</strong> (the \"corset\" muscle, key to core stability). <strong>Rectus abdominis</strong> <strong>flexes</strong> the trunk. <strong>Nerves</strong>: the <strong>thoracoabdominal nerves (anterior rami T7–T11)</strong> and the <strong>subcostal nerve (T12)</strong> supply all of them. Internal oblique and transversus also receive <strong>L1</strong> (iliohypogastric and ilioinguinal)."),
                ("plate", 16, "The three layers and rectus, lateral views", "Layer 1 external oblique; layer 2 internal oblique; layer 3 transversus abdominis; rectus with tendinous intersections"),
                ("box", "why", "Why · the six-pack", "<strong>Rectus abdominis</strong> runs from the <strong>pubic crest and symphysis</strong> to the <strong>xiphoid and costal cartilages 5–7</strong>. It is crossed by usually three <strong>tendinous intersections</strong> fused to the front of its sheath, which divide it into the visible segments. The segmented design reflects its origin from several body segments and lets parts contract separately. The lower fibres of the flat muscles also form the walls of the <strong>inguinal canal</strong>, and the lower edge of the external oblique aponeurosis forms the <strong>inguinal ligament</strong>."),
                ("plate", 17, "The rectus sheath above and below the arcuate line", "Transverse sections showing how the aponeuroses wrap rectus differently above and below the umbilical region"),
                ("box", "mnem", "Exam hook · the arcuate line switch", "<strong>Above the arcuate line</strong> (about a third of the way from umbilicus to pubis), the <strong>internal oblique aponeurosis splits</strong>: the anterior layer joins the external oblique aponeurosis <strong>in front</strong> of rectus, and the posterior layer joins the transversus aponeurosis <strong>behind</strong> it. <strong>Below the arcuate line</strong>, <strong>all three aponeuroses pass in front</strong>, so the back of rectus lies directly on <strong>transversalis fascia</strong>. The aponeuroses meet in the midline at the <strong>linea alba</strong>, where fibres cross from one side to the other."),
                ("plate", 18, "Interlacing aponeurotic fibres", "Intramuscular and intermuscular exchange of fibres across the linea alba"),
                ("box", "why", "Why · the two sides are one muscle sheet", "At the linea alba, aponeurotic fibres <strong>cross the midline</strong>: superficial fibres from one side run deep on the other (<strong>intramuscular</strong> exchange within the external obliques), and the right external oblique continues into the left internal oblique (<strong>intermuscular</strong> exchange). The left and right obliques therefore act as one continuous diagonal sling. Rotating the trunk to the right uses the <em>left</em> external oblique together with the <em>right</em> internal oblique, the \"synchronous\" action in the slide 28 table."),
                ("plate", 19, "Continuation of the fascial layers", "Scarpa's fascia continues into the perineum as Colles' fascia and dartos; attaches to the fascia lata"),
                ("box", "clin", "Clinical · where leaked urine goes", "The membranous layer of superficial fascia (<strong>Scarpa's fascia</strong>) continues into the perineum as <strong>Colles' fascia</strong>, around the penis as the superficial penile fascia, and into the scrotum as the <strong>dartos</strong>. It is firmly <strong>attached to the fascia lata</strong> just below the inguinal ligament and to the ischiopubic rami. So if the spongy urethra ruptures (e.g. a straddle injury), extravasated urine spreads into the scrotum, penis and up the anterior abdominal wall, <strong>but not into the thighs</strong>. The attachments act as barriers."),
            ],
            "recall": {"head": "Recall — anterolateral wall", "items": [
                "<li><b>Number of anterolateral muscles —</b> <b>5</b> (3 flat, 2 vertical)</li>",
                "<li><b>Two vertical midline muscles —</b> <b>rectus abdominis</b> and <b>pyramidalis</b></li>",
                "<li><b>Muscles that flex and rotate the trunk —</b> <b>external</b> and <b>internal obliques</b></li>",
                "<li><b>Muscle that mainly compresses and supports viscera —</b> <b>transversus abdominis</b></li>",
                "<li><b>Nerves of the anterolateral muscles —</b> <b>T7–T11</b> thoracoabdominal, <b>T12</b> subcostal (+ L1)</li>",
                "<li><b>Below the arcuate line —</b> all aponeuroses pass <b>anterior</b> to rectus</li>",
                "<li><b>Midline meeting of the aponeuroses —</b> <b>linea alba</b></li>",
                "<li><b>Scarpa's fascia continues as —</b> <b>Colles' fascia</b> in the perineum</li>",
            ]},
            "digest": {
                "key_points": [
                    "There are 5 anterolateral muscles: 3 flat muscles (external oblique, internal oblique, transversus abdominis) that begin posterolaterally and become aponeuroses toward the midline, and 2 vertical muscles (rectus abdominis, pyramidalis) enclosed in a sheath formed by these aponeuroses.",
                    "All anterolateral muscles compress and support abdominal viscera and assist respiration; external and internal obliques flex and rotate the trunk; transversus abdominis compresses and supports viscera; rectus abdominis flexes the trunk.",
                    "Rectus abdominis has tendinous intersections; the rectus sheath is formed by the aponeuroses, which pass both in front of and behind rectus above the arcuate line and all in front below it; they meet at the linea alba.",
                    "Aponeurotic fibres exchange across the linea alba (intramuscular and intermuscular).",
                    "Superficial fascia layers continue into the perineum (Scarpa's to Colles' fascia, dartos, superficial penile fascia) and attach to the fascia lata.",
                ],
                "self_tests": [
                    {"q": "What are the actions of the anterolateral abdominal wall muscles?", "a": "All compress and support viscera and assist respiration; the obliques flex and rotate the trunk; transversus abdominis compresses; rectus abdominis flexes the trunk."},
                    {"q": "How does the rectus sheath differ below the arcuate line?", "a": "All three aponeuroses pass anterior to rectus abdominis, leaving only transversalis fascia behind it."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "LO2 · Blood and nerve supply of the abdominal wall",
            "title": "Blood supply, nerves and dermatomes of the abdominal wall", "tag": "A vessel and nerve plane between internal oblique and transversus.",
            "lead": "The abdominal wall's vessels and nerves travel in one plane, between internal oblique and transversus abdominis, the same plane as the intercostal bundle above.",
            "blocks": [
                ("plate", 20, "Blood supply of the abdominal wall", "Superior and inferior epigastric arteries meet in the rectus sheath; neurovascular plane between internal oblique and transversus"),
                ("box", "why", "Why · two arteries meet in the sheath", "The <strong>neurovascular bundle runs between internal oblique and transversus abdominis</strong>, continuous with the intercostal plane (§1). Within the rectus sheath, the <strong>superior epigastric artery</strong> (from the internal thoracic) runs down and the <strong>inferior epigastric artery</strong> (from the external iliac) runs up, and they <strong>anastomose</strong>. That link between subclavian and iliac territories can bypass a blocked aorta (coarctation). The lateral wall is also fed by the <strong>10th–11th posterior intercostal</strong> and <strong>subcostal</strong> arteries, the <strong>musculophrenic</strong>, and the <strong>deep and superficial circumflex iliac</strong> and <strong>superficial epigastric</strong> arteries."),
                ("box", "clin", "Clinical · rectus sheath haematoma", "Coughing, injections or anticoagulants can tear an epigastric artery inside the sheath. Above the arcuate line the haematoma is contained by the posterior sheath. Below it, it can spread more widely, mimicking an acute abdomen. Surgeons placing laparoscopic ports lateral to rectus aim to avoid the inferior epigastric vessels."),
                ("plate", 21, "Nerve supply and dermatomes", "T7–T11 thoracoabdominal, T12 subcostal, iliohypogastric and ilioinguinal (L1); T4 nipple, T10 umbilicus, T12 suprapubic, L1 inguinal"),
                ("box", "mnem", "Exam hook · the dermatome landmarks", "Nerves: <strong>anterior rami T7–T11</strong> (thoracoabdominal nerves, the continuations of the intercostal nerves), <strong>T12 subcostal</strong>, and from L1 the <strong>iliohypogastric</strong> and <strong>ilioinguinal</strong> nerves. Dermatome landmarks: <strong>T4 at the nipple</strong> (in males), <strong>T10 at the umbilicus</strong>, <strong>T12 suprapubic</strong>, <strong>L1 at the inguinal region</strong>. Remember \"T10 = belly but-TEN\"."),
                ("box", "clin", "Clinical · referred pain and shingles", "Because the same spinal segments supply viscera, early <strong>appendicitis</strong> pain is felt around the <strong>umbilicus (T10)</strong> before it moves to the right iliac fossa as the parietal peritoneum becomes involved. <strong>Shingles</strong> (herpes zoster) follows a single dermatome as a band of painful rash around one side of the trunk. A low transverse (Pfannenstiel) incision can injure the iliohypogastric or ilioinguinal nerves, causing numbness or groin pain."),
            ],
            "recall": {"head": "Recall — blood and nerve supply", "items": [
                "<li><b>Neurovascular plane —</b> between <b>internal oblique</b> and <b>transversus abdominis</b></li>",
                "<li><b>Arteries anastomosing in the rectus sheath —</b> <b>superior</b> and <b>inferior epigastric</b></li>",
                "<li><b>Anterior wall nerves —</b> anterior rami <b>T7–T11</b>, <b>T12 subcostal</b>, <b>iliohypogastric</b>, <b>ilioinguinal</b></li>",
                "<li><b>T10 dermatome —</b> <b>umbilicus</b></li>",
                "<li><b>T4 dermatome —</b> <b>nipple</b> (males)</li>",
                "<li><b>L1 dermatome —</b> <b>inguinal region</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "The neurovascular bundle of the abdominal wall lies between the internal oblique and transversus abdominis muscles.",
                    "Superior epigastric (from internal thoracic) and inferior epigastric (from external iliac) arteries supply rectus abdominis and anastomose within the rectus sheath.",
                    "The anterior abdominal wall is supplied by anterior rami of T7-T11, the subcostal nerve (T12), and the iliohypogastric and ilioinguinal nerves.",
                    "Dermatomes: T4 at the nipples (males), T10 around the umbilicus, T12 suprapubic, L1 inguinal region.",
                ],
                "self_tests": [
                    {"q": "In which plane do the nerves and vessels of the anterolateral abdominal wall run?", "a": "Between the internal oblique and transversus abdominis muscles."},
                    {"q": "Which dermatome lies at the umbilicus?", "a": "T10."},
                ],
            },
        },
        {
            "id": "s5", "code": "§5", "lo": "LO3 · Movements of the back",
            "title": "Movements of the vertebral column — region by region", "tag": "Disc thickness and facet orientation decide what each region can do.",
            "lead": "This section brings back L19–L21. Each region's mobility follows from its discs and facet orientation, and each movement is produced by a predictable set of back and trunk muscles.",
            "blocks": [
                ("plate", 23, "What permits and limits spinal movement", "Mobility from disc compressibility; limited by disc thickness, facet orientation, capsule tension, ligaments and muscles; assisted by abdominal wall and gravity"),
                ("box", "why", "Why · mobility comes from the discs, direction from the facets", "Movement varies by region and between individuals. It comes mainly from the <strong>compressibility and elasticity of the IV discs</strong>. Its <strong>range</strong> is limited by: <strong>disc thickness</strong> (thicker relative to the body means more motion); the <strong>shape and orientation of the articular processes</strong> (which <em>steer</em> the movement); <strong>facet joint capsule tension</strong>; and the <strong>resistance of back muscles and ligaments</strong> (ligamenta flava, posterior longitudinal ligament). It is <strong>assisted</strong> by the <strong>anterolateral abdominal wall</strong> and <strong>gravity</strong>."),
                ("plate", 24, "Cervical region — the most mobile", "Thick discs, near-horizontal facets, loose capsules, slender neck; flexion greatest here"),
                ("plate", 25, "Muscles moving the cervical spine", "Flexion: longus colli, scalenes, SCM; extension: splenius, semispinalis; lateral bending and rotation: unilateral actions"),
                ("box", "mnem", "Exam hook · neck movers", "The cervical spine is <strong>free</strong> because its <strong>discs are thick</strong> relative to the small vertebral bodies, its <strong>facets are almost horizontal</strong> and large, its <strong>capsules are loose</strong>, and the slender neck has no surrounding bulk. <strong>Flexion is greatest in the neck.</strong> <strong>Flexion</strong> (bilateral): longus colli, scalenes, sternocleidomastoid. <strong>Extension</strong> (bilateral): splenius capitis and cervicis, semispinalis capitis and cervicis. <strong>Lateral bending</strong> (unilateral): iliocostalis cervicis, longissimus capitis and cervicis, splenius. <strong>Rotation</strong> (unilateral): rotatores, semispinalis, multifidus, splenius cervicis. Bilateral contraction gives flexion or extension; one side alone gives bending or rotation."),
                ("plate", 26, "Thoracic region — rotation, little else", "Thin discs, vertical facets, and the rib cage limit flexion and extension; rotation is permitted"),
                ("box", "why", "Why · the ribs lock the thoracic spine", "In the thoracic region <strong>rotation</strong> is the main free movement. The <strong>discs are thin</strong> relative to the vertebral bodies, the <strong>articular processes are vertical</strong> (the facets lie roughly on an arc centred on the vertebral body, which allows twisting but suppresses flexion and extension), and the <strong>ribs and sternum</strong> brace the region. The rib cage provides stability and protects the thoracic organs at the cost of mobility."),
                ("plate", 27, "Lumbar region — flexion and extension, not rotation", "Thick discs and interlocking vertical facets that face each other; extension greatest here"),
                ("box", "clin", "Clinical · why the lower back takes the strain", "Lumbar discs are <strong>thick</strong>, so <strong>flexion and extension are free</strong>. <strong>Extension is greatest in the lumbar region.</strong> But the facets face each other (sagittally) and <strong>interlock</strong>, so <strong>rotation is blocked</strong>. Twisting while bent forward and lifting combines a lot of flexion with an attempt to rotate a segment built to resist it. This is the classic mechanism for <strong>lumbar disc herniation</strong>, usually posterolateral at L4/5 or L5/S1, where the posterior longitudinal ligament is narrowest (L20)."),
                ("plate", 28, "Muscles moving the thoracic and lumbar spine", "Flexion: rectus abdominis, psoas, gravity; extension: erector spinae, multifidus; lateral bending and rotation listed"),
                ("box", "mnem", "Exam hook · trunk movers (back + abdomen together)", "<strong>Flexion</strong> (bilateral): <strong>rectus abdominis</strong>, <strong>psoas major</strong>, and <strong>gravity</strong>. Standing up, flexion is mostly the back extensors <em>lowering</em> you eccentrically (L21). <strong>Extension</strong> (bilateral): <strong>erector spinae</strong>, <strong>multifidus</strong>, semispinalis thoracis. <strong>Lateral bending</strong> (unilateral): iliocostalis, longissimus, multifidus, <strong>external and internal obliques</strong>, <strong>quadratus lumborum</strong>. <strong>Rotation</strong> (unilateral): rotatores, multifidus, and the <strong>external oblique acting together with the opposite internal oblique</strong> (the sling from slide 18), plus semispinalis thoracis."),
                ("plate", 29, "Integration with other muscle groups", "Lateral flexion and rotation involve neck, back, abdominal, hip and limb muscles"),
                ("box", "active", "Synthesis · no movement uses one muscle", "Real movements recruit whole chains. <strong>Lateral flexion</strong> uses splenius, sternocleidomastoid, iliocostalis and longissimus, the obliques, quadratus lumborum, and even rhomboids, serratus anterior and the glutei to stabilise. <strong>Rotation</strong> pairs the transversospinalis group with the external and internal obliques. Starred muscles in the figure take part in the overall movement without acting on the IV joints themselves. This is the point of LO3: back (L21) and trunk (L22) muscles work as one system around the spine (L19–L20)."),
            ],
            "recall": {"head": "Recall — movements of the back", "items": [
                "<li><b>Spinal mobility comes mainly from —</b> <b>IV disc</b> compressibility and elasticity</li>",
                "<li><b>Movement is assisted by —</b> the <b>anterolateral abdominal wall</b> and <b>gravity</b></li>",
                "<li><b>Region with greatest flexion —</b> <b>cervical</b></li>",
                "<li><b>Main free movement of the thoracic spine —</b> <b>rotation</b></li>",
                "<li><b>Region with greatest extension —</b> <b>lumbar</b></li>",
                "<li><b>Why lumbar rotation is limited —</b> <b>interlocking</b> articular processes</li>",
                "<li><b>Trunk flexors —</b> <b>rectus abdominis</b>, <b>psoas major</b>, <b>gravity</b></li>",
                "<li><b>Trunk extensors —</b> <b>erector spinae</b>, <b>multifidus</b></li>",
                "<li><b>Trunk rotation by the obliques —</b> <b>external oblique</b> with the <b>opposite internal oblique</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Vertebral column mobility results primarily from IV disc compressibility and elasticity; range is limited by disc thickness, articular process shape/orientation, facet capsule tension and resistance of back muscles and ligaments (ligamenta flava, posterior longitudinal ligament), and assisted by the anterolateral abdominal wall and gravity.",
                    "Cervical movements are free: thick discs, nearly horizontal articular processes with large facets, loose capsules, slender neck; flexion is greatest in the cervical region.",
                    "Cervical flexion: longus colli, scalenes, sternocleidomastoid; extension: splenius capitis/cervicis, semispinalis capitis/cervicis; lateral bending: iliocostalis cervicis, longissimus capitis/cervicis, splenius; rotation: rotatores, semispinalis, multifidus, splenius cervicis.",
                    "Thoracic region mainly rotates; other movements are limited by thin discs, vertical articular processes and the ribs and sternum.",
                    "Lumbar region: thick discs, vertical facing articular surfaces allow free flexion and extension but interlocking prevents rotation; extension is greatest in the lumbar region.",
                    "Thoracolumbar flexion: rectus abdominis, psoas major, gravity; extension: erector spinae, multifidus, semispinalis thoracis; lateral bending: iliocostalis, longissimus, multifidus, external and internal obliques, quadratus lumborum; rotation: rotatores, multifidus, external oblique with the opposite internal oblique, semispinalis thoracis.",
                ],
                "self_tests": [
                    {"q": "Why is rotation limited in the lumbar region but free in the thoracic region?", "a": "Lumbar articular processes interlock (facing each other), preventing rotation; thoracic articular processes are vertical and arranged to permit rotation, though flexion and extension are suppressed by thin discs and the rib cage."},
                    {"q": "Which muscles flex the thoracolumbar spine?", "a": "Rectus abdominis and psoas major (bilaterally), assisted by gravity."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
