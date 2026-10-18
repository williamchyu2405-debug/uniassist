#!/usr/bin/env python3
"""L19 — Bones of the vertebral column. MHHS2401. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/l19_vert_bones"

SPEC = {
    "slug": "vertebral_column_bones_mhhs2401_l19",
    "workdir": WD,
    "unit": "MHHS2401",
    "subject": "Musculoskeletal System",
    "week": 10,
    "title": "Bones of the Vertebral Column",
    "source": "MHHS2401 Lecture 19 — Bones of the vertebral column, Dr Mirjana Strkalj (Macquarie University)",
    "brand": "MHHS2401 · L19 · Spine",
    "brandsub": "Bones of the<br>Vertebral Column",
    "eyebrow": "MHHS2401 · Musculoskeletal System · Lecture 19",
    "h1": "Bones of the Vertebral Column",
    "h1thin": "the regional vertebra — and how shape dictates movement",
    "lede": "Every lecture slide, shown in full and explained like a tutor would. The organising idea: once you know the typical vertebra (from L17), each region is just a set of modifications that trade mobility for load-bearing or for protecting what passes through — so read every feature as \"what does this let the region do, and what passes here?\"",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The note underneath is <b>not a re-caption</b> — it adds the <em>why</em> behind each bony feature, what passes through it, and the clinical/identification point the slide assumes. Compare each region back to the typical vertebra of L17.",
    "n_slides": 16,
    "sections": [
        {
            "id": "s1", "code": "§1", "lo": "Cervical region",
            "title": "Cervical vertebrae (C1–C7)", "tag": "The most mobile region — and the one with its own artery tunnel.",
            "lead": "Seven small vertebrae built for range of motion. The region's signature is the <strong>transverse foramen</strong> (unique to the cervical spine), and three of the seven are <em>atypical</em> — the atlas, the axis and the vertebra prominens. Learn the identifying features as a checklist.",
            "blocks": [
                ("plate", 4, "Cervical vertebrae — overview", "The cervical vertebrae form the neck and are the most mobile region"),
                ("box", "why", "Why · built for the widest range of movement", "Cervical vertebrae are the <strong>smallest of the 24 movable vertebrae</strong>, and three design choices make the neck the most mobile region: <strong>relatively thick IV discs</strong>, <strong>near-horizontal articular facets</strong> (which permit gliding in many directions), and little surrounding body mass. The trade-off is <strong>stability</strong> — the same mobility is why the cervical spine is so vulnerable in whiplash and high-energy trauma."),
                ("grid", [
                    (5, "Distinctive cervical features", "Transverse foramina, bifid spines, uncinate processes"),
                    (6, "Typical cervical vertebra (C3–C6)", "A typical cervical vertebra with its triangular foramen"),
                ]),
                ("box", "mnem", "Exam hook · the cervical identification checklist", "Spot a cervical vertebra by: a <strong>small, wide body</strong>; a <strong>large triangular vertebral foramen</strong> (roomy because the cervical cord enlargement sits here); a <strong>transverse foramen</strong> in each transverse process (transmits the <strong>vertebral artery</strong>, C6→C1); <strong>anterior and posterior tubercles</strong> on the transverse process (the C6 anterior tubercle is the <strong>carotid tubercle</strong>, used to compress the carotid); a <strong>bifid spinous process</strong> (C2–C6); and <strong>uncinate processes</strong> (raised lateral lips of C3–C6) that form the uncovertebral joints."),
                ("grid", [
                    (7, "Atlas (C1) — the \"yes\" bone", "The atlas has no body and no spinous process"),
                    (8, "Axis (C2) — the dens", "The axis bears the dens (odontoid process)"),
                ]),
                ("box", "why", "Why · the top two are purpose-built for head motion", "The <strong>atlas (C1)</strong> is a ring with <strong>no body and no spinous process</strong> — its lost body became the <strong>dens</strong> of C2. It cradles the skull on two large facets, giving the <strong>\"yes\" nod</strong> at the atlanto-occipital joint. The <strong>axis (C2)</strong> projects the <strong>dens (odontoid process)</strong> upward as a pivot, around which the atlas (and the skull) rotate for the <strong>\"no\" shake</strong>. These two joints are detailed in the L20 craniovertebral guide."),
                ("grid", [
                    (9, "Axis (C2) — further views", "The dens and articular surfaces of the axis"),
                    (10, "C7 — vertebra prominens", "C7 has a long non-bifid spinous process you can feel"),
                ]),
                ("box", "clin", "Clinical · C7, the landmark you can feel", "<strong>C7 is the vertebra prominens</strong> — its <strong>long, non-bifid spinous process</strong> is the bony lump you feel at the base of the neck, the classic surface landmark for counting vertebrae. Its transverse foramina are small and usually transmit only accessory veins (not the vertebral artery), and it lacks the uncinate processes of the typical cervical vertebrae — an easy identification point."),
            ],
            "recall": {"head": "Recall — cervical vertebrae", "items": [
                "<li><b>Cervical signature —</b> the <b>transverse foramen</b> (carries the <b>vertebral artery</b>)</li>",
                "<li><b>Typical cervical —</b> small wide body, <b>triangular</b> foramen, <b>bifid</b> spine, <b>uncinate</b> processes</li>",
                "<li><b>Atlas (C1) —</b> no <b>body</b>, no spinous process → the <b>\"yes\"</b> joint</li>",
                "<li><b>Axis (C2) —</b> bears the <b>dens</b> → the <b>\"no\"</b> rotation pivot</li>",
                "<li><b>C7 —</b> <b>vertebra prominens</b>, long non-bifid spinous process (landmark)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Cervical vertebrae are the smallest movable vertebrae; thick discs, horizontal facets and small body mass make the neck the most mobile region.",
                    "Identifying features: small wide body, large triangular vertebral foramen, transverse foramen (vertebral artery), anterior/posterior transverse tubercles (C6 = carotid tubercle), bifid spinous processes C2–C6, uncinate processes C3–C6.",
                    "Atlas (C1) has no body or spinous process (atlanto-occipital 'yes' nod); axis (C2) bears the dens, the pivot for the 'no' rotation.",
                    "C7 is the vertebra prominens with a long non-bifid spinous process — the palpable surface landmark.",
                ],
                "self_tests": [
                    {"q": "Which feature is unique to cervical vertebrae and what passes through it?", "a": "The transverse foramen, which transmits the vertebral artery (through C6 up to C1)."},
                    {"q": "How do the atlas and axis differ structurally, and what movement does each enable?", "a": "The atlas has no body or spinous process and gives the 'yes' nod (atlanto-occipital); the axis bears the dens, the pivot for the 'no' rotation (atlantoaxial)."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "Thoracic region",
            "title": "Thoracic vertebrae (T1–T12)", "tag": "The rib-bearing region — built to rotate, not to flex.",
            "lead": "Twelve vertebrae defined by one job: articulating with the ribs. Their <strong>costal facets</strong> and <strong>near-vertical, coronally-oriented facets</strong> make rotation the dominant movement while limiting flexion/extension — the opposite emphasis to the neck.",
            "blocks": [
                ("plate", 11, "Distinctive thoracic features", "Heart-shaped body, costal facets, long sloping spinous process"),
                ("box", "mnem", "Exam hook · the thoracic identification checklist", "Identify a thoracic vertebra by its rib connections: a <strong>heart-shaped body</strong> carrying <strong>costal facets (or demifacets)</strong> for the <strong>head of a rib</strong>; a <strong>costal facet on the transverse process</strong> for the <strong>rib tubercle</strong>; a <strong>small circular vertebral foramen</strong>; and a <strong>long, slender, downward-sloping spinous process</strong> that overlaps the vertebra below (so the tip of one spine lies at the body of the next — important when counting or doing a thoracic tap)."),
                ("plate", 12, "Facet orientation controls movement", "Vertical coronal facets plus the rib cage permit rotation"),
                ("box", "why", "Why · the ribs and facets gate the movement", "The thoracic facets sit in a near-<strong>coronal, vertical plane</strong>, and the attached <strong>rib cage</strong> plus <strong>overlapping spinous processes</strong> splint the region. Together these <strong>limit flexion, extension and lateral flexion</strong> but <strong>permit a good deal of rotation</strong>. This is the mirror image of the lumbar region (§3), where sagittal facets allow flexion/extension but block rotation — a favourite compare-and-contrast question."),
                ("plate", 13, "Atypical thoracic vertebrae", "T1 and T9–T12 borrow features from neighbouring regions"),
                ("box", "why", "Why · the ends blend into their neighbours", "The <strong>transitional</strong> thoracic vertebrae borrow features from adjacent regions: <strong>T1–T4</strong> show some <em>cervical</em> traits (T1 has a long, almost horizontal spine, a complete superior costal facet and a demifacet); <strong>T9–T12</strong> show some <em>lumbar</em> traits and the costal facets simplify (T9 one demifacet; T10–T12 a single full facet each as the lower ribs articulate with a single vertebra). The facet pattern is how you pin an atypical thoracic level."),
            ],
            "recall": {"head": "Recall — thoracic vertebrae", "items": [
                "<li><b>Thoracic signature —</b> <b>costal facets</b> (body + transverse process) for the <b>ribs</b></li>",
                "<li><b>Body shape —</b> <b>heart-shaped</b>; foramen <b>small and circular</b></li>",
                "<li><b>Spinous process —</b> long, <b>sloping down</b>, overlaps the vertebra below</li>",
                "<li><b>Movement allowed —</b> mainly <b>rotation</b> (coronal facets + rib cage limit flexion)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Thoracic vertebrae have costal facets/demifacets on the body (rib head) and on the transverse process (rib tubercle), a heart-shaped body, a small circular foramen and a long downward-sloping spinous process.",
                    "Coronal, near-vertical facets plus the rib cage and overlapping spines limit flexion/extension/lateral flexion but permit rotation (opposite emphasis to the lumbar region).",
                    "Transitional vertebrae: T1–T4 show cervical features, T9–T12 show lumbar features, with the costal facet pattern simplifying from demifacets to a single facet in the lower thoracic spine.",
                ],
                "self_tests": [
                    {"q": "What two articulations do thoracic vertebrae make with a rib?", "a": "The costal facet(s) on the body receive the rib head; the costal facet on the transverse process receives the rib tubercle."},
                    {"q": "Why is rotation the dominant thoracic movement?", "a": "The coronally oriented, near-vertical facets favour rotation, while the rib cage and overlapping spinous processes restrict flexion, extension and lateral flexion."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "Lumbar region",
            "title": "Lumbar vertebrae (L1–L5)", "tag": "The load-bearers — massive bodies, sagittal facets, no rotation.",
            "lead": "Five big vertebrae carrying the most weight. Their <strong>sagittally-oriented facets</strong> are the key: they allow generous flexion and extension but <strong>lock rotation</strong>, which protects the lumbar discs — the ones that herniate most.",
            "blocks": [
                ("plate", 14, "Typical lumbar vertebra", "Massive kidney-shaped body and sagittal articular processes"),
                ("box", "mnem", "Exam hook · the lumbar identification checklist", "Identify a lumbar vertebra by <strong>size and facet plane</strong>: a <strong>massive kidney-shaped body</strong> (built for weight-bearing), a <strong>triangular vertebral foramen</strong>, <strong>long slender transverse processes</strong>, and crucially <strong>articular processes oriented in the sagittal plane</strong>. No costal facets and no transverse foramen — their absence is itself the clue."),
                ("grid", [
                    (15, "Lumbar vertebrae — views", "Lumbar vertebrae from multiple angles"),
                    (16, "Lumbar detail", "Pedicles, laminae and the pars interarticularis"),
                ]),
                ("box", "why", "Why · sagittal facets = flexion yes, rotation no", "The <strong>sagittal facet orientation</strong> is the examinable mechanical point: facets lying in the sagittal plane interlock against twisting, so the lumbar spine <strong>flexes and extends freely but barely rotates</strong>. That protects the discs from shear — but it also means the <strong>pars interarticularis</strong> (the bony bridge between superior and inferior facets) takes repetitive stress, and its stress fracture (<strong>spondylolysis</strong>, which can progress to <strong>spondylolisthesis</strong>) is a classic lumbar lesion, as covered in L17."),
            ],
            "recall": {"head": "Recall — lumbar vertebrae", "items": [
                "<li><b>Lumbar signature —</b> <b>massive kidney-shaped</b> body; <b>sagittal</b> facets</li>",
                "<li><b>Facets allow —</b> <b>flexion/extension</b> but block <b>rotation</b></li>",
                "<li><b>Absent features —</b> no <b>costal facets</b>, no <b>transverse foramen</b></li>",
                "<li><b>Stress point —</b> the <b>pars interarticularis</b> → <b>spondylolysis</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Lumbar vertebrae have massive kidney-shaped bodies, triangular foramina, long slender transverse processes, and sagittally oriented articular facets; no costal facets or transverse foramina.",
                    "Sagittal facets permit flexion and extension but block rotation, protecting the discs from shear.",
                    "The pars interarticularis is the lumbar stress point; its fracture is spondylolysis, which can progress to spondylolisthesis.",
                ],
                "self_tests": [
                    {"q": "Why does the lumbar spine rotate so little?", "a": "Its articular facets lie in the sagittal plane and interlock against twisting, allowing flexion/extension but not rotation."},
                    {"q": "Name two features present on a thoracic vertebra that are absent on a lumbar one.", "a": "Costal facets (for ribs) — and, versus cervical, the transverse foramen; lumbar vertebrae have neither costal facets nor transverse foramina."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "Sacrum, coccyx &amp; comparison",
            "title": "Sacrum, coccyx &amp; regional comparison", "tag": "The fused base — and a side-by-side of all five regions.",
            "lead": "The column ends in two fused blocks that trade all mobility for a rigid weight-transfer platform, then the lecture lines up the regions so you can read each region's job straight off its shape.",
            "blocks": [
                ("plate", 17, "Sacrum &amp; coccyx", "Five fused sacral vertebrae and the vestigial coccyx"),
                ("box", "why", "Why · fusion buys a weight-transfer platform", "The <strong>sacrum</strong> is <strong>five fused vertebrae</strong> forming a wedge that transmits body weight from the spine to the pelvis across the <strong>sacroiliac joints</strong>, and its <strong>anterior and posterior sacral foramina</strong> transmit the sacral spinal nerve rami. The <strong>coccyx</strong> is three to four vestigial fused vertebrae — small, but a real attachment site for pelvic-floor muscles and ligaments. Fusion is the whole point: the base of the column sacrifices movement for rigid, reliable load transfer."),
                ("grid", [
                    (18, "Typical vertebrae compared", "Side-by-side of cervical, thoracic and lumbar vertebrae"),
                    (19, "Surface anatomy of the back", "Palpable spinous processes and surface landmarks"),
                ]),
                ("box", "mnem", "Exam hook · read the region off the shape, and the landmarks", "Put the regions side by side and the logic is: <strong>cervical</strong> = small + transverse foramen + bifid spine (mobility); <strong>thoracic</strong> = costal facets + heart-shaped body (ribs, rotation); <strong>lumbar</strong> = massive body + sagittal facets (load, flexion). For surface anatomy, the counting landmarks are <strong>C7 vertebra prominens</strong>, the spine of <strong>T3 ≈ the scapular spine</strong>, <strong>T7 ≈ the inferior scapular angle</strong>, and <strong>L4 ≈ the iliac crest (supracristal plane)</strong> — the level used to find the space for a lumbar puncture (L20)."),
            ],
            "recall": {"head": "Recall — sacrum, coccyx &amp; comparison", "items": [
                "<li><b>Sacrum —</b> <b>5 fused</b> vertebrae; transfers weight via the <b>sacroiliac</b> joints</li>",
                "<li><b>Coccyx —</b> <b>3–4</b> vestigial fused vertebrae; pelvic-floor attachment</li>",
                "<li><b>Read the region —</b> cervical=<b>transverse foramen</b>, thoracic=<b>costal facets</b>, lumbar=<b>sagittal facets</b></li>",
                "<li><b>Landmark —</b> <b>L4</b> ≈ the <b>iliac crest</b> (supracristal plane)</li>",
            ]},
            "digest": {
                "key_points": [
                    "The sacrum is five fused vertebrae forming a wedge that transfers weight to the pelvis via the sacroiliac joints; sacral foramina transmit the sacral nerve rami.",
                    "The coccyx is three to four vestigial fused vertebrae serving as a pelvic-floor attachment.",
                    "Regional identification: cervical (transverse foramen, bifid spine), thoracic (costal facets, heart-shaped body), lumbar (massive body, sagittal facets).",
                    "Surface landmarks: C7 vertebra prominens; T7 ≈ inferior scapular angle; L4 ≈ iliac crest (supracristal plane, used for lumbar puncture).",
                ],
                "self_tests": [
                    {"q": "What does fusion of the sacrum achieve functionally?", "a": "It creates a rigid wedge that transmits body weight from the vertebral column to the pelvis across the sacroiliac joints — trading mobility for load transfer."},
                    {"q": "At what vertebral level does the iliac crest lie, and why is it useful?", "a": "Approximately L4 (the supracristal plane) — it is used to locate the L3/4 or L4/5 space for a lumbar puncture."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
