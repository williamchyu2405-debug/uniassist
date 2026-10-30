#!/usr/bin/env python3
"""MHHS2401 L22 · Muscles of the trunk — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "trunk_muscles_mhhs2401_l22.html"
META = {
    "title": "Muscles of the Trunk",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("Muscles of the trunk (MHHS2401 Lecture 22, Dr Mirjana Strkalj): the thorax and thoracic wall muscles "
                "(intercostals, subcostales, transversus thoracis) and intercostal neurovascular bundle; layers of the "
                "abdominal wall; posterior abdominal wall muscles; the anterolateral muscles, aponeuroses, rectus sheath "
                "and fascial continuations; blood supply, nerves and dermatomes of the abdominal wall; and region-by-region "
                "movements of the vertebral column with the muscles producing them."),
}

Q = [
 # easy
 q("Thoracic compartments", "easy", "The thoracic cavity is divided into the two pleural cavities and the:",
   ["mediastinum", "pericardial cavity", "peritoneal cavity", "retroperitoneum"], "A",
   "Left and right pleural cavities flank the central mediastinum."),
 q("Inferior aperture", "easy", "The inferior thoracic aperture is closed by the:",
   ["diaphragm", "transversus thoracis", "internal intercostals", "quadratus lumborum"], "A",
   "The musculotendinous diaphragm seals the large inferior opening of the thorax."),
 q("Rectus action", "easy", "The main action of rectus abdominis is to:",
   ["flex the trunk", "extend the trunk", "rotate the trunk", "elevate the ribs"], "A",
   "Rectus abdominis flexes the trunk; the obliques flex and rotate."),
 q("Umbilical dermatome", "easy", "The dermatome at the level of the umbilicus is:",
   ["T10", "T4", "T12", "L1"], "A",
   "T4 nipple (males), T10 umbilicus, T12 suprapubic, L1 inguinal."),
 q("Greatest flexion", "easy", "Flexion of the vertebral column is greatest in the:",
   ["cervical region", "thoracic region", "lumbar region", "sacral region"], "A",
   "Thick discs, near-horizontal facets and a slender neck make cervical flexion the greatest."),
 # medium
 q("Neurovascular bundle", "medium", "Intercostal nerves and vessels run in the costal groove between the:",
   ["internal and innermost intercostals", "external and internal intercostals", "innermost intercostals and pleura", "external intercostals and skin"], "A",
   "They lie in the costal groove of the rib above, in the plane between internal and innermost intercostals."),
 q("Chest drain", "medium", "To avoid the intercostal bundle, a chest drain is inserted:",
   ["just above the upper border of the lower rib", "just below the lower border of the upper rib", "through the middle of the costal groove", "directly through the costal cartilage"], "A",
   "The bundle hugs the inferior border of each rib, so needles pass above the rib below."),
 q("Subcostales", "medium", "The subcostales muscles are found on the:",
   ["inner posterior thoracic wall", "outer anterior thoracic wall", "deep surface of the sternum", "lateral abdominal wall"], "A",
   "Subcostales lie posteriorly in the plane of the innermost intercostals and elevate the ribs."),
 q("Transversus thoracis", "medium", "Transversus thoracis lies deep to the internal thoracic vessels and:",
   ["depresses the ribs", "elevates the ribs", "rotates the trunk", "flexes the neck"], "A",
   "On the deep anterior wall it holds the internal thoracic vessels against the wall and depresses the ribs."),
 q("Accessory muscles", "medium", "Which back muscles act as accessory respiratory muscles?",
   ["serratus posterior and levatores costarum", "erector spinae and the multifidus", "latissimus dorsi and the trapezius", "the rotatores and the semispinalis"], "A",
   "Serratus posterior and levatores costarum move the ribs; the others act on the spine or limb."),
 q("Abdominal wall layers", "medium", "Which layer lies immediately deep to the extraperitoneal fat?",
   ["parietal peritoneum", "transversalis fascia", "superficial fascia", "transversus abdominis"], "A",
   "Skin, superficial fascia, muscles and deep fascia, extraperitoneal fat, then parietal peritoneum."),
 q("Posterior wall", "medium", "Which muscle is part of the posterior abdominal wall?",
   ["quadratus lumborum", "external oblique", "rectus abdominis", "pyramidalis"], "A",
   "Posterior wall: quadratus lumborum, psoas major and iliacus."),
 q("Flat muscles", "medium", "The three flat anterolateral abdominal muscles, superficial to deep, are:",
   ["external oblique, internal oblique, transversus", "internal oblique, external oblique, transversus", "transversus, internal oblique, external oblique", "external oblique, transversus, internal oblique"], "A",
   "Layer 1 external oblique, layer 2 internal oblique, layer 3 transversus abdominis."),
 q("Transversus action", "medium", "The main action of transversus abdominis is to:",
   ["compress and support the viscera", "flex and rotate the trunk", "extend the lumbar spine", "laterally flex the neck"], "A",
   "Its horizontal fibres act like a corset; the obliques flex and rotate."),
 q("Nerve supply", "medium", "The anterolateral abdominal muscles are supplied by:",
   ["anterior rami of T7–T12 and L1", "posterior rami of T7 to L1", "the phrenic nerve and the T12", "the femoral nerve and the L2"], "A",
   "Thoracoabdominal nerves (T7–T11), the subcostal nerve (T12) and iliohypogastric/ilioinguinal branches of L1."),
 q("Neurovascular plane", "medium", "The main neurovascular plane of the abdominal wall lies between:",
   ["internal oblique and transversus", "external and internal obliques", "transversus and transversalis fascia", "rectus abdominis and its sheath"], "A",
   "Nerves and vessels run between internal oblique and transversus abdominis."),
 q("Epigastric arteries", "medium", "Within the rectus sheath, the superior epigastric artery anastomoses with the:",
   ["inferior epigastric artery", "superficial epigastric artery", "musculophrenic artery", "deep circumflex iliac artery"], "A",
   "Superior (from internal thoracic) and inferior (from external iliac) epigastric arteries meet in the sheath."),
 # hard
 q("Arcuate line", "hard", "Below the arcuate line, the posterior surface of rectus abdominis rests on:",
   ["transversalis fascia", "the transversus aponeurosis", "the internal oblique aponeurosis", "the linea alba"], "A",
   "Below the arcuate line all three aponeuroses pass anterior to rectus, leaving only transversalis fascia behind it."),
 q("Rectus sheath", "hard", "Above the arcuate line, the internal oblique aponeurosis:",
   ["splits to enclose rectus abdominis", "passes entirely behind rectus abdominis", "passes entirely in front of rectus", "ends at the lateral border of rectus"], "A",
   "Its anterior layer joins the external oblique aponeurosis and its posterior layer joins the transversus aponeurosis."),
 q("Trunk rotation", "hard", "Rotating the trunk to the right uses the left external oblique together with the:",
   ["right internal oblique", "left internal oblique", "right external oblique", "left transversus abdominis"], "A",
   "The external oblique acts with the opposite internal oblique, continuous across the linea alba."),
 q("Fascial continuity", "hard", "Urine from a ruptured spongy urethra spreads into the abdominal wall but not the thigh because Scarpa's fascia:",
   ["attaches to the fascia lata below the inguinal ligament", "fuses with the transversalis fascia at the umbilicus", "ends at the iliac crest without any firm attachment", "continues freely down into the thigh compartments"], "A",
   "Scarpa's fascia continues as Colles' fascia and dartos, and its firm attachment to the fascia lata blocks spread into the thigh."),
 q("Lumbar rotation", "hard", "Rotation is limited in the lumbar region mainly because the articular processes:",
   ["face each other and interlock", "are nearly horizontal and large", "are fused to the rib cage", "are absent below L3"], "A",
   "Vertical, facing lumbar facets interlock, allowing flexion and extension but preventing rotation."),
 q("Thoracic movement", "hard", "Thoracic flexion and extension are limited by thin discs, vertical facets and the:",
   ["ribs and sternum", "ligamentum nuchae", "iliolumbar ligaments", "sacroiliac joints"], "A",
   "The rib cage stabilises the thoracic spine but suppresses most movement other than rotation."),
 q("Extension region", "hard", "Extension of the vertebral column is greatest in the:",
   ["lumbar region", "cervical region", "thoracic region", "sacral region"], "A",
   "Thick lumbar discs and sagittal facets permit the greatest extension."),
 q("Neck flexors", "hard", "Which group lists muscles that flex the cervical spine (bilaterally)?",
   ["longus colli, scalenes, sternocleidomastoid", "splenius, semispinalis, multifidus", "rotatores, multifidus, splenius cervicis", "iliocostalis, longissimus, splenius"], "A",
   "Longus colli, scalenes and SCM flex; splenius and semispinalis extend."),
 q("Trunk flexors", "hard", "Bilateral flexion of the thoracic and lumbar spine is produced by:",
   ["rectus abdominis, psoas major and gravity", "erector spinae, multifidus and gravity together", "quadratus lumborum and both oblique muscles", "rotatores and the semispinalis thoracis"], "A",
   "Rectus abdominis and psoas major flex the trunk, assisted by gravity; erector spinae and multifidus extend it."),
 q("Psoas", "hard", "Psoas major attaches inferiorly to the:",
   ["lesser trochanter of the femur", "greater trochanter of the femur", "anterior superior iliac spine", "pubic tubercle"], "A",
   "Psoas major runs from the T12–L5 vertebrae to the lesser trochanter, joining iliacus as iliopsoas."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
