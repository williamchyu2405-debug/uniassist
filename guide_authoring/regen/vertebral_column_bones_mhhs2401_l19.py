#!/usr/bin/env python3
"""MHHS2401 L19 · Bones of the vertebral column — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "vertebral_column_bones_mhhs2401_l19.html"
META = {
    "title": "Bones of the Vertebral Column",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("Bones of the vertebral column (MHHS2401 Lecture 19, Dr Mirjana Strkalj): cervical vertebrae including "
                "atlas, axis and vertebra prominens; thoracic vertebrae and costal facets; lumbar vertebrae, facet "
                "orientation and the pars interarticularis; sacrum and coccyx; regional identification and surface landmarks."),
}

Q = [
 # easy
 q("Atlas", "easy", "Which vertebra has no body and no spinous process?",
   ["C1, the atlas", "C2, the axis", "C7, vertebra prominens", "L5, the lumbosacral vertebra"], "A",
   "The atlas is a ring of anterior and posterior arches with lateral masses; it lacks a body and spinous process."),
 q("Axis", "easy", "The dens (odontoid process) belongs to:",
   ["C2", "C1", "C3", "C7"], "A",
   "The dens projects up from the axis (C2) and is the pivot for rotation of the atlas."),
 q("Vertebra prominens", "easy", "The palpable vertebra prominens is:",
   ["C7", "C2", "T1", "T7"], "A",
   "C7 has a long, non-bifid spinous process that is easily felt at the base of the neck."),
 q("Transverse foramen", "easy", "A transverse foramen identifies a vertebra as:",
   ["cervical", "thoracic", "lumbar", "sacral"], "A",
   "Only cervical vertebrae have transverse foramina, which transmit the vertebral artery."),
 q("Costal facets", "easy", "Costal facets on the vertebral body identify a vertebra as:",
   ["thoracic", "cervical", "lumbar", "sacral"], "A",
   "Thoracic vertebrae articulate with ribs via costal facets on the body and transverse processes."),
 # medium
 q("Cervical features", "medium", "Which combination is typical of a mid-cervical vertebra?",
   ["bifid spinous process and transverse foramen", "heart-shaped body with paired costal facets", "kidney-shaped body with sagittal articular facets", "long downward-sloping spinous process without foramina"], "A",
   "C2–C6 have bifid spines and all cervical vertebrae have transverse foramina; the other options describe thoracic or lumbar vertebrae."),
 q("Carotid tubercle", "medium", "The carotid tubercle, against which the common carotid can be compressed, is on:",
   ["C6", "C2", "C4", "T1"], "A",
   "The anterior tubercle of the C6 transverse process is the carotid tubercle."),
 q("Uncinate processes", "medium", "Uncinate processes are found on the bodies of:",
   ["C3–C6", "C1–C2", "T1–T4", "L1–L5"], "A",
   "Raised lateral lips on C3–C6 bodies form uncovertebral joints, a common osteophyte site."),
 q("Craniovertebral movement", "medium", "The 'no' head shake occurs mainly at the:",
   ["atlantoaxial joint", "atlanto-occipital joint", "C2–C3 facet joints", "C7–T1 facet joints"], "A",
   "Rotation of the atlas around the dens of the axis produces the 'no' movement; the atlanto-occipital joint gives the 'yes' nod."),
 q("Thoracic body", "medium", "A thoracic vertebral body is typically:",
   ["heart-shaped with costal demifacets", "kidney-shaped and massive", "small and wide with uncinate lips", "fused with its neighbours"], "A",
   "Thoracic bodies are heart-shaped and carry costal facets or demifacets for the rib heads."),
 q("Thoracic motion", "medium", "The thoracic region mainly permits:",
   ["rotation", "flexion and extension", "lateral flexion", "no movement"], "A",
   "Coronal facets, the rib cage and overlapping spines limit flexion, extension and lateral flexion but allow rotation."),
 q("Lumbar features", "medium", "Which feature is characteristic of lumbar vertebrae?",
   ["sagittally oriented articular facets", "transverse foramina in each process", "costal demifacets on the body", "bifid tips on spinous processes"], "A",
   "Lumbar vertebrae have massive bodies and sagittal facets, with no transverse foramina or costal facets."),
 q("Lumbar motion", "medium", "Sagittal lumbar facets permit flexion and extension but block:",
   ["rotation", "extension", "flexion", "compression"], "A",
   "The interlocking sagittal facets resist rotation, protecting the discs from shear."),
 q("Sacrum", "medium", "The sacrum transmits body weight to the pelvis through the:",
   ["sacroiliac joints", "pubic symphysis", "hip joints directly", "sacrococcygeal joint"], "A",
   "The wedge-shaped sacrum (five fused vertebrae) articulates with the ilia at the sacroiliac joints."),
 q("Coccyx", "medium", "The coccyx consists of about:",
   ["3–4 fused vestigial vertebrae", "5 fused sacral vertebrae", "2 separate small vertebrae", "6–7 fused vertebrae"], "A",
   "The coccyx is three to four fused vestigial vertebrae and anchors pelvic floor muscles."),
 q("Surface landmarks", "medium", "The iliac crests (supracristal plane) mark approximately the level of:",
   ["L4", "L1", "T12", "S2"], "A",
   "A line between the iliac crests crosses the L4 spinous process, a landmark used for lumbar puncture."),
 q("Surface landmarks", "medium", "The inferior angle of the scapula lies at about the level of:",
   ["T7", "T3", "T12", "C7"], "A",
   "With the arm by the side, the inferior scapular angle is at about T7."),
 # hard
 q("Pars interarticularis", "hard", "A stress fracture of the lumbar pars interarticularis is called:",
   ["spondylolysis", "spondylolisthesis", "spondylosis", "scoliosis"], "A",
   "Spondylolysis is the pars defect; if the vertebra then slips forward it becomes spondylolisthesis."),
 q("Spondylolisthesis", "hard", "Bilateral pars fractures may progress to spondylolisthesis, meaning:",
   ["anterior slip of one vertebra on another", "bony fusion of two adjacent vertebral bodies", "abnormal lateral curvature of the whole spine", "wedge collapse of a single vertebral body"], "A",
   "Loss of the bony link between facets lets the vertebral body slip forward."),
 q("Vertebral artery", "hard", "The vertebral artery ascends through the transverse foramina of:",
   ["C6 to C1", "C7 to C1", "C1 to C3 only", "T1 to C1"], "A",
   "The vertebral artery usually enters at C6, not C7, and runs up through the foramina to C1."),
 q("Transitional vertebrae", "hard", "Lower thoracic vertebrae (T9–T12) are transitional because they:",
   ["show lumbar-like features", "lack any costal facets", "have transverse foramina", "have bifid spinous processes"], "A",
   "T9–T12 take on lumbar features and their costal facet pattern simplifies to single facets."),
 q("Regional comparison", "hard", "An isolated vertebra has a large triangular foramen, small wide body and no costal facets. It is most likely:",
   ["cervical", "upper thoracic", "lower thoracic", "sacral"], "A",
   "A large triangular foramen with a small wide body and no costal facets fits a cervical vertebra (check for a transverse foramen)."),
 q("Lumbar foramen", "hard", "Compared with thoracic vertebrae, lumbar vertebral foramina are:",
   ["triangular rather than circular", "circular rather than triangular", "absent in the lower lumbar spine", "doubled by the uncinate processes"], "A",
   "Lumbar foramina are triangular; thoracic foramina are small and circular."),
 q("Atlas movement", "hard", "The atlanto-occipital joint between C1 and the skull mainly allows:",
   ["flexion and extension", "rotation about the dens", "side-to-side lateral gliding", "axial compression and distraction"], "A",
   "The atlanto-occipital joint produces the 'yes' nod (flexion/extension)."),
 q("Mobility", "hard", "The neck is the most mobile region of the spine mainly because of its:",
   ["thick discs and horizontal facets", "thin discs and vertical facets", "rib articulations and long spines", "massive bodies and sagittal facets"], "A",
   "Thick discs relative to small bodies and near-horizontal facets give the cervical spine a large range of motion."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
