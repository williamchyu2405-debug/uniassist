#!/usr/bin/env python3
"""L21 — Muscles of the back. MHHS2401. Slide-forward public guide."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from sf_assemble import build

WD = "guide_authoring/sources/l21_back_muscles"

SPEC = {
    "slug": "back_muscles_mhhs2401_l21",
    "workdir": WD,
    "unit": "MHHS2401",
    "subject": "Musculoskeletal System",
    "week": 11,
    "title": "Muscles of the Back",
    "source": "MHHS2401 Lecture 21 — Muscles of the back, Dr Mirjana Strkalj (Macquarie University)",
    "brand": "MHHS2401 · L21 · Spine",
    "brandsub": "Muscles of<br>the Back",
    "eyebrow": "MHHS2401 · Musculoskeletal System · Lecture 21",
    "h1": "Muscles of the Back",
    "h1thin": "extrinsic vs intrinsic — and the nerve that proves which",
    "lede": "Every lecture slide, shown in full and explained like a tutor would. The single organising rule runs through the whole lecture: a back muscle's <em>embryology</em> dictates its <em>nerve</em> — extrinsic muscles are immigrants supplied by <strong>anterior</strong> rami, true (intrinsic) back muscles develop in place and are supplied by <strong>posterior</strong> rami. Get that and every muscle sorts itself.",
    "howto": "Each slide is shown in full (click to <b>enlarge</b>). The note underneath is <b>not a re-caption</b> — it adds the function, the nerve (and the anterior-vs-posterior-ramus logic behind it), and the clinical/landmark point. For each muscle, ask: extrinsic or intrinsic, and therefore which ramus supplies it?",
    "n_slides": 26,
    "sections": [
        {
            "id": "s1", "code": "§1", "lo": "Classification",
            "title": "Classifying the back muscles", "tag": "Embryology decides the nerve — the rule the whole lecture hangs on.",
            "lead": "Before any individual muscle, lock in the classification. The split into extrinsic and intrinsic is not just descriptive — it predicts the nerve supply, which is how exams test it.",
            "blocks": [
                ("plate", 5, "Movements of the vertebral column", "What limits and assists spinal movement"),
                ("box", "why", "Why · muscles are only part of the story", "Spinal movement is <strong>limited</strong> by disc thickness/compressibility, facet orientation and capsule tension, and ligament resistance (ligamenta flava, PLL) — all from L20. It is <strong>produced</strong> not only by the back muscles but <em>assisted</em> by <strong>gravity</strong> and the <strong>anterolateral abdominal wall muscles</strong>. Key insight: standing upright, flexion is mostly controlled by the back extensors <em>paying out</em> (eccentric lengthening) against gravity — they brake the fall-forward rather than haul you back."),
                ("grid", [
                    (6, "Extrinsic vs intrinsic — the rule", "Embryonic origin dictates anterior vs posterior ramus supply"),
                    (7, "The full classification", "Extrinsic and intrinsic groups and their layers"),
                ]),
                ("box", "mnem", "Exam hook · origin predicts the ramus — memorise this", "The examinable rule: <strong>Extrinsic</strong> muscles develop from the <strong>myotomes (hypaxial)</strong> and migrate onto the back, so they keep their original nerve — the <strong>anterior (ventral) rami</strong>; functionally they move the <strong>limb or ribs</strong>. <strong>Intrinsic (\"true\") back muscles</strong> develop in place from the <strong>epaxial</strong> region of the myotome, so they are supplied by the <strong>posterior (dorsal) rami</strong>; functionally they move the <strong>vertebral column</strong> itself. If a \"back\" muscle is supplied by an anterior ramus, it is an immigrant (extrinsic). One exception to flag: trapezius is motor from the accessory nerve, CN XI."),
            ],
            "recall": {"head": "Recall — classification", "items": [
                "<li><b>Extrinsic —</b> from <b>myotomes</b>, supplied by <b>anterior rami</b>, move <b>limb/ribs</b></li>",
                "<li><b>Intrinsic (true) —</b> from <b>epaxial</b> myotome, supplied by <b>posterior rami</b>, move the <b>column</b></li>",
                "<li><b>The rule —</b> a back muscle on an <b>anterior ramus</b> is <b>extrinsic</b></li>",
                "<li><b>Standing flexion —</b> extensors work by <b>eccentric</b> (paying-out) contraction against gravity</li>",
            ]},
            "digest": {
                "key_points": [
                    "Back muscles are extrinsic (develop from myotomes, supplied by anterior/ventral rami, act on the limb or ribs) or intrinsic/true (develop from the epaxial myotome, supplied by posterior/dorsal rami, act on the vertebral column).",
                    "Embryonic origin predicts the nerve: anterior ramus = extrinsic, posterior ramus = intrinsic.",
                    "Spinal movement is limited by discs, facets and ligaments, produced by the back muscles, and assisted by gravity and the abdominal wall; standing flexion is controlled by the extensors contracting eccentrically.",
                ],
                "self_tests": [
                    {"q": "How does the embryonic origin of a back muscle predict its nerve supply?", "a": "Extrinsic muscles form from myotomes and keep anterior (ventral) ramus supply; intrinsic/true back muscles form from the epaxial myotome and are supplied by posterior (dorsal) rami."},
                    {"q": "If a back muscle is supplied by an anterior ramus, what does that tell you?", "a": "It is an extrinsic (migrated) muscle acting on the limb or ribs, not a true back muscle."},
                ],
            },
        },
        {
            "id": "s2", "code": "§2", "lo": "Extrinsic — superficial",
            "title": "Superficial extrinsic muscles", "tag": "The limb-movers draped over the back — each with its own named nerve.",
            "lead": "The superficial extrinsic group connects the upper limb to the trunk. They look like \"back\" muscles but they move the scapula and arm — and each has a distinct, examinable nerve.",
            "blocks": [
                ("grid", [
                    (8, "The extrinsic muscles", "Superficial and intermediate extrinsic layers"),
                    (9, "Trapezius", "Trapezius moves the scapula; supplied by CN XI"),
                ]),
                ("box", "clin", "Clinical · trapezius and the accessory nerve", "<strong>Trapezius</strong> anchors the pectoral girdle to the trunk, and its three parts move the scapula in different directions: <strong>superior fibres elevate</strong>, <strong>middle retract</strong>, <strong>inferior depress</strong>. Its motor supply is the <strong>accessory nerve (CN XI)</strong> (with C3/C4 for proprioception/pain) — the one superficial back muscle not run by a spinal nerve. This is why <strong>CN XI injury</strong> (e.g. in posterior-triangle neck surgery) causes a <strong>drooping shoulder</strong> and weak shrug."),
                ("grid", [
                    (10, "Levator scapulae &amp; rhomboids", "Scapular retractors supplied by the dorsal scapular nerve"),
                    (11, "Latissimus dorsi", "The 'widest of the back' — extends and adducts the arm"),
                ]),
                ("box", "mnem", "Exam hook · one muscle, one nerve", "Keep each muscle paired with its nerve. <strong>Levator scapulae</strong> (C1–C4 transverse processes → superior angle of scapula) and the <strong>rhomboids</strong> (nuchal ligament/C7–T5 spines → medial border) <strong>retract the scapula</strong> and are supplied by the <strong>dorsal scapular nerve</strong>. <strong>Latissimus dorsi</strong> (\"widest of the back\" — lower thoracic spines, thoracolumbar fascia, iliac crest, lower ribs → floor of the intertubercular groove of the humerus) <strong>extends, adducts and medially rotates the arm</strong> (the \"handcuff/climbing\" muscle) and is supplied by the <strong>thoracodorsal nerve</strong>."),
            ],
            "recall": {"head": "Recall — superficial extrinsic", "items": [
                "<li><b>Trapezius —</b> moves <b>scapula</b> (elevate/retract/depress); nerve = <b>CN XI</b> (accessory)</li>",
                "<li><b>Levator scapulae &amp; rhomboids —</b> <b>retract</b> scapula; nerve = <b>dorsal scapular</b></li>",
                "<li><b>Latissimus dorsi —</b> <b>extends/adducts/medially rotates</b> arm; nerve = <b>thoracodorsal</b></li>",
                "<li><b>They move —</b> the <b>upper limb</b>, not the spine (extrinsic)</li>",
            ]},
            "digest": {
                "key_points": [
                    "Superficial extrinsic muscles connect the upper limb to the trunk and move the scapula/arm.",
                    "Trapezius elevates (superior), retracts (middle) and depresses (inferior) the scapula; motor supply is the accessory nerve (CN XI), so injury causes a drooping shoulder.",
                    "Levator scapulae and rhomboids retract the scapula (dorsal scapular nerve); latissimus dorsi extends, adducts and medially rotates the humerus (thoracodorsal nerve).",
                ],
                "self_tests": [
                    {"q": "What is the motor nerve of trapezius and the sign of its injury?", "a": "The accessory nerve (CN XI); injury causes a drooping shoulder and weakened shrug."},
                    {"q": "Give the actions and nerve of latissimus dorsi.", "a": "Extends, adducts and medially rotates the humerus (and raises the body in climbing); supplied by the thoracodorsal nerve."},
                ],
            },
        },
        {
            "id": "s3", "code": "§3", "lo": "Extrinsic — intermediate",
            "title": "Intermediate extrinsic muscles", "tag": "Two thin respiratory muscles hiding under the superficial layer.",
            "lead": "A brief but examinable pair — the serratus posterior muscles are extrinsic (anterior-ramus supply) and act in respiration, not on the spine.",
            "blocks": [
                ("plate", 12, "Serratus posterior superior &amp; inferior", "Thin accessory muscles of respiration"),
                ("box", "why", "Why · thin respiratory sheets, not spine movers", "The <strong>serratus posterior superior</strong> and <strong>inferior</strong> are thin sheets deep to the superficial extrinsic muscles and are <strong>accessory muscles of respiration</strong>, supplied by the <strong>intercostal nerves (anterior rami)</strong> — confirming their extrinsic status. <strong>Superior elevates the upper ribs</strong> (aiding inspiration); <strong>inferior pulls the lower ribs down and back</strong>, steadying them against the diaphragm's pull. Their anterior-ramus supply is the giveaway that, despite their position, they are not true back muscles."),
            ],
            "recall": {"head": "Recall — intermediate extrinsic", "items": [
                "<li><b>Serratus posterior —</b> accessory muscles of <b>respiration</b></li>",
                "<li><b>Superior —</b> <b>elevates</b> upper ribs (inspiration); <b>inferior —</b> <b>depresses</b> lower ribs</li>",
                "<li><b>Nerve —</b> <b>intercostal</b> (anterior rami) → confirms <b>extrinsic</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Serratus posterior superior and inferior are intermediate extrinsic muscles acting as accessory muscles of respiration, supplied by intercostal (anterior ramus) nerves.",
                    "Serratus posterior superior elevates the upper ribs (inspiration); serratus posterior inferior depresses/steadies the lower ribs against diaphragmatic pull.",
                ],
                "self_tests": [
                    {"q": "Why are the serratus posterior muscles classed as extrinsic?", "a": "They are supplied by intercostal nerves (anterior rami) and act on the ribs in respiration, not on the vertebral column."},
                ],
            },
        },
        {
            "id": "s4", "code": "§4", "lo": "Intrinsic (true) back muscles",
            "title": "Intrinsic (true) back muscles", "tag": "The real spinal muscles — three layers, all on posterior rami.",
            "lead": "The true back muscles run from pelvis to skull inside the thoracolumbar fascia, all supplied by posterior rami. Learn them as three functional layers: a splenius wrap, the erector spinae extensors, and the deep transversospinales stabilisers — plus the suboccipital group.",
            "blocks": [
                ("grid", [
                    (14, "The intrinsic muscles — the set", "Spinotransversales, erector spinae, transversospinales, segmental, suboccipital"),
                    (15, "Intrinsic muscles &amp; the thoracolumbar fascia", "True back muscles enclosed by the thoracolumbar fascia"),
                ]),
                ("box", "why", "Why · the thoracolumbar fascia is the organiser", "The intrinsic muscles run <strong>pelvis → skull</strong> and are wrapped by the <strong>thoracolumbar fascia</strong>, which is the structural backbone of the region: medially it anchors to the <strong>spinous processes</strong>, laterally to the <strong>rib angles</strong>, and it <strong>separates the deep true back muscles from the superficial extrinsic ones</strong>. In the lumbar region it thickens into <strong>three layers</strong> around erector spinae and quadratus lumborum — a strong corset that transfers load and gives core muscles something to pull against."),
                ("grid", [
                    (16, "Thoracolumbar fascia — lumbar layers", "Posterior, middle and anterior layers in the lumbar region"),
                    (17, "Splenius capitis &amp; cervicis", "The 'bandage' muscles of the spinotransversales layer"),
                ]),
                ("box", "mnem", "Exam hook · splenius — the bandage wrap", "<strong>Splenius</strong> (\"bandage\") is the superficial spinotransversales layer in the neck: it runs from midline <strong>spinous processes upward and laterally</strong> to the skull/transverse processes — the opposite diagonal to the deeper transversospinales. <strong>Splenius capitis</strong> → mastoid process/superior nuchal line; <strong>splenius cervicis</strong> → upper cervical transverse processes. Supplied (like all true back muscles) by <strong>posterior rami</strong>. Action: <strong>one side turns the face to the same side</strong>; <strong>both sides extend the head and neck</strong>."),
                ("grid", [
                    (18, "Splenius — in situ", "Splenius capitis and cervicis exposed"),
                    (19, "Erector spinae — the three columns", "Iliocostalis, longissimus, spinalis"),
                ]),
                ("box", "mnem", "Exam hook · erector spinae — 'I Love Spaghetti', lateral to medial", "<strong>Erector spinae</strong> is the <strong>chief extensor of the spine</strong>, arising from a broad common tendon on the <strong>iliac crest, sacrum and lumbar spines</strong> and splitting into three columns — lateral to medial: <strong>Iliocostalis → Longissimus → Spinalis</strong> (\"<strong>I Love Spaghetti</strong>\"). Each column is named regionally (e.g. iliocostalis <em>lumborum/thoracis/cervicis</em>)."),
                ("plate", 21, "Erector spinae — action", "Bilateral extension, unilateral lateral flexion, eccentric control"),
                ("box", "why", "Why · the brake as well as the engine", "Acting <strong>bilaterally the erector spinae extend</strong> the vertebral column and head; acting <strong>unilaterally they laterally flex</strong>. The functionally crucial point: when the trunk <strong>flexes forward</strong>, they <strong>pay out their fibres (eccentric/lengthening contraction)</strong> to <em>control</em> the descent against gravity — which is why the back is most vulnerable (and why people \"put their back out\") lifting from a stooped, flexed position."),
                ("grid", [
                    (23, "Transversospinales", "Semispinalis, multifidus, rotatores — the deep stabilisers"),
                    (24, "Transversospinalis — layers", "Semispinalis (superficial), multifidus, rotatores (deep)"),
                ]),
                ("box", "why", "Why · short deep muscles that stabilise and sense", "The <strong>transversospinales</strong> run the <em>opposite</em> diagonal to splenius — from <strong>transverse processes up to the spinous processes above</strong>. Superficial to deep: <strong>semispinalis</strong> (spans many segments; semispinalis capitis is a big neck extensor), <strong>multifidus</strong> (thickest in the lumbar spine — a key <strong>segmental stabiliser</strong> targeted in back rehab), and the deepest <strong>rotatores</strong> (best developed in the thorax). They produce small rotation/extension but their main role is <strong>postural stabilisation and proprioception</strong> — they are dense with muscle spindles."),
                ("grid", [
                    (25, "Segmental (minor deep) muscles", "Levatores costarum, interspinales, intertransversarii"),
                    (26, "Suboccipital muscles", "Four small muscles of the suboccipital triangle"),
                ]),
                ("box", "clin", "Clinical · the segmental muscles and the suboccipital triangle", "The tiny <strong>segmental muscles</strong> (<strong>levatores costarum, interspinales, intertransversarii</strong>) span single segments; packed with <strong>muscle spindles</strong>, they act more as <strong>proprioceptive sensors</strong> of spinal position than as prime movers. The four <strong>suboccipital muscles</strong> (rectus capitis posterior major/minor, obliquus capitis superior/inferior) connect C1–C2 to the skull and <strong>extend and laterally flex the head</strong>; they bound the <strong>suboccipital triangle</strong>, a clinically important space containing the <strong>vertebral artery</strong> and the <strong>posterior ramus of C1 (suboccipital nerve)</strong>."),
                ("plate", 28, "Surface anatomy of the back muscles", "Palpable contours of the back musculature"),
                ("box", "mnem", "Exam hook · read the living back", "On the surface the muscles you can see and name are the <strong>trapezius</strong> (upper back/neck outline), the <strong>latissimus dorsi</strong> (lower lateral back / posterior axillary fold), the <strong>erector spinae</strong> as the two vertical paraspinal ridges flanking the midline furrow, and the triangular <strong>lumbar region</strong> where latissimus and the thoracolumbar fascia meet. Being able to point to these is a standard OSCE ask."),
            ],
            "recall": {"head": "Recall — intrinsic back muscles", "items": [
                "<li><b>All supplied by —</b> <b>posterior rami</b>; wrapped by the <b>thoracolumbar fascia</b></li>",
                "<li><b>Erector spinae (lat→med) —</b> <b>iliocostalis</b>, <b>longissimus</b>, <b>spinalis</b> — chief <b>extensor</b></li>",
                "<li><b>Transversospinales —</b> <b>semispinalis</b>, <b>multifidus</b>, <b>rotatores</b> → <b>stabilise</b> &amp; sense</li>",
                "<li><b>Splenius —</b> turns face to <b>same</b> side; both sides <b>extend</b> head/neck</li>",
                "<li><b>Suboccipital triangle —</b> contains the <b>vertebral artery</b> and <b>C1 posterior ramus</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Intrinsic/true back muscles run pelvis to skull, are wrapped by the thoracolumbar fascia, and are all supplied by posterior (dorsal) rami.",
                    "Erector spinae (iliocostalis, longissimus, spinalis — lateral to medial) is the chief extensor: bilateral extension, unilateral lateral flexion, and eccentric control of forward flexion.",
                    "Transversospinales (semispinalis, multifidus, rotatores) run transverse process to spinous process above and provide postural stabilisation and proprioception; multifidus is a key lumbar stabiliser.",
                    "Splenius turns the face to the same side (unilateral) and extends the head/neck (bilateral).",
                    "The suboccipital muscles extend/laterally flex the head and bound the suboccipital triangle containing the vertebral artery and the posterior ramus of C1 (suboccipital nerve).",
                ],
                "self_tests": [
                    {"q": "Name the three columns of erector spinae from lateral to medial and its main action.", "a": "Iliocostalis, longissimus, spinalis ('I Love Spaghetti'); it is the chief extensor of the vertebral column."},
                    {"q": "What does the suboccipital triangle contain?", "a": "The vertebral artery and the posterior ramus of C1 (the suboccipital nerve), plus accompanying veins."},
                ],
            },
        },
        {
            "id": "s5", "code": "§5", "lo": "Flexors of the column",
            "title": "Flexor muscles of the vertebral column", "tag": "The front-of-neck and trunk muscles that bend the spine forward.",
            "lead": "The back extends the spine; flexion comes from muscles on the <em>front</em>. The lecture closes with the cervical flexors (SCM, prevertebral, scalenes) and the thoracolumbar flexors.",
            "blocks": [
                ("plate", 30, "Flexors of the cervical spine", "Sternocleidomastoid, longus coli/capitis, scalenes"),
                ("grid", [
                    (31, "Sternocleidomastoid (SCM)", "The key neck landmark; flexes and rotates the neck"),
                    (32, "Torticollis", "SCM shortening causes a twisted neck"),
                ]),
                ("box", "clin", "Clinical · SCM — landmark, action and torticollis", "<strong>Sternocleidomastoid</strong> is the <strong>key landmark of the neck</strong>, dividing it into anterior and posterior triangles (mastoid/superior nuchal line → sternal + clavicular heads). Action: <strong>both sides flex the neck</strong>; <strong>one side laterally flexes to the same side and rotates the face to the opposite side</strong>. Motor supply is the <strong>accessory nerve (CN XI)</strong>, like trapezius. Shortening/fibrosis of one SCM — e.g. a birth injury — produces <strong>torticollis</strong>, the head tilted toward the lesion and turned away."),
                ("grid", [
                    (33, "Prevertebral muscles", "Longus colli/capitis, recti capitis — deep neck flexors"),
                    (34, "Scalene muscles", "Anterior, middle, posterior scalenes elevate ribs"),
                ]),
                ("box", "mnem", "Exam hook · the deep neck flexors and the scalenes", "The <strong>prevertebral muscles</strong> (<strong>longus capitis, longus colli, rectus capitis anterior/lateralis</strong>) lie in front of the cervical spine and <strong>flex the head and neck</strong> (longus colli also rotates), supplied by <strong>anterior rami of C1–C6</strong>. The <strong>scalenes</strong> (anterior, middle, posterior) run from cervical transverse processes to the <strong>1st and 2nd ribs</strong>: acting from above they <strong>laterally flex/rotate the neck</strong>; acting from below they <strong>elevate the ribs</strong> as accessory muscles of inspiration. The <strong>anterior and middle scalenes</strong> bound the gap transmitting the <strong>brachial plexus and subclavian artery</strong> — the site of thoracic outlet syndrome."),
                ("plate", 36, "Flexors of the thoracic &amp; lumbar spine", "Psoas major, rectus abdominis and gravity flex the trunk"),
                ("box", "why", "Why · trunk flexion comes from the front and from gravity", "Flexion of the <strong>thoracic and lumbar</strong> spine is produced by muscles anterior to it: chiefly <strong>psoas major</strong> and <strong>rectus abdominis</strong> (the abdominal wall) — <strong>assisted by gravity</strong>, which does much of the work once you begin to lean forward. This closes the lecture's loop: the back muscles don't <em>produce</em> flexion so much as <strong>control it eccentrically</strong>, while the true flexors sit on the opposite side of the column."),
            ],
            "recall": {"head": "Recall — flexors of the column", "items": [
                "<li><b>SCM —</b> both sides <b>flex</b> neck; one side rotates face to <b>opposite</b> side; nerve <b>CN XI</b></li>",
                "<li><b>Torticollis —</b> <b>shortened SCM</b> (e.g. birth injury) → twisted neck</li>",
                "<li><b>Prevertebral —</b> <b>longus colli/capitis</b> → deep neck <b>flexion</b> (anterior rami C1–C6)</li>",
                "<li><b>Scalenes —</b> elevate <b>ribs 1–2</b>; bound the <b>brachial plexus</b>/subclavian artery gap</li>",
                "<li><b>Thoracolumbar flexors —</b> <b>psoas major</b>, <b>rectus abdominis</b>, <b>gravity</b></li>",
            ]},
            "digest": {
                "key_points": [
                    "Flexion of the spine comes from muscles anterior to it, not the back muscles.",
                    "Sternocleidomastoid flexes the neck (bilateral) and rotates the face to the opposite side (unilateral); supplied by the accessory nerve (CN XI); unilateral shortening causes torticollis.",
                    "Prevertebral muscles (longus capitis/colli, recti capitis) flex the head and neck (anterior rami C1–C6).",
                    "Scalenes elevate ribs 1–2 (accessory inspiration) and laterally flex the neck; the anterior and middle scalenes bound the passage of the brachial plexus and subclavian artery (thoracic outlet).",
                    "Thoracic and lumbar flexion is produced by psoas major and rectus abdominis, assisted by gravity, with the back extensors controlling the movement eccentrically.",
                ],
                "self_tests": [
                    {"q": "Describe the unilateral action of sternocleidomastoid and the deformity from its shortening.", "a": "One SCM laterally flexes the head to the same side and rotates the face to the opposite side; shortening/fibrosis causes torticollis (head tilted toward, turned away from the lesion)."},
                    {"q": "Which muscles chiefly flex the thoracic and lumbar spine?", "a": "Psoas major and rectus abdominis (the abdominal wall), assisted by gravity."},
                ],
            },
        },
    ],
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "static", "guides", SPEC["slug"] + ".html")
    build(SPEC, os.path.abspath(out))
