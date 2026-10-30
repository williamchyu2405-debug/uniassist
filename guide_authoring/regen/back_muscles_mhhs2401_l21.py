#!/usr/bin/env python3
"""MHHS2401 L21 · Muscles of the back — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "back_muscles_mhhs2401_l21.html"
META = {
    "title": "Muscles of the Back",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("Muscles of the back (MHHS2401 Lecture 21, Dr Mirjana Strkalj): extrinsic vs intrinsic classification and "
                "nerve supply by anterior vs posterior rami; superficial extrinsic muscles (trapezius, latissimus dorsi, "
                "levator scapulae, rhomboids); intermediate serratus posterior; intrinsic erector spinae, transversospinales, "
                "splenius and suboccipital muscles; and the flexors of the vertebral column."),
}

Q = [
 # easy
 q("Classification", "easy", "True (intrinsic) back muscles are supplied by:",
   ["posterior rami of spinal nerves", "anterior rami of spinal nerves", "the accessory nerve", "the thoracodorsal nerve"], "A",
   "Intrinsic muscles develop in place from the epaxial myotome and keep posterior (dorsal) ramus supply."),
 q("Trapezius nerve", "easy", "Motor supply to trapezius comes from the:",
   ["spinal accessory nerve", "dorsal scapular nerve", "thoracodorsal nerve", "long thoracic nerve"], "A",
   "Trapezius is the exception among extrinsic back muscles, with motor supply from CN XI."),
 q("Latissimus nerve", "easy", "Latissimus dorsi is supplied by the:",
   ["thoracodorsal nerve", "dorsal scapular nerve", "accessory nerve", "suprascapular nerve"], "A",
   "The thoracodorsal nerve (C6–C8) supplies latissimus dorsi."),
 q("Erector spinae order", "easy", "From lateral to medial, the columns of erector spinae are:",
   ["iliocostalis, longissimus, spinalis", "spinalis, longissimus, iliocostalis", "longissimus, iliocostalis, spinalis", "iliocostalis, spinalis, longissimus"], "A",
   "'I Love Spaghetti': iliocostalis (lateral), longissimus, spinalis (medial)."),
 q("Chief extensor", "easy", "The chief extensor of the vertebral column is:",
   ["erector spinae", "rectus abdominis", "latissimus dorsi", "serratus posterior"], "A",
   "Erector spinae extends the column bilaterally and flexes it laterally when acting on one side."),
 # medium
 q("Extrinsic rule", "medium", "A 'back' muscle supplied by an anterior ramus is best classified as:",
   ["an extrinsic muscle acting on limb or ribs", "an intrinsic muscle acting on the vertebral column", "a suboccipital muscle acting on the head and neck", "a transversospinal muscle stabilising the lumbar spine"], "A",
   "Anterior ramus supply means the muscle migrated onto the back from the hypaxial myotome and acts on the limb or ribs."),
 q("Trapezius actions", "medium", "Which part of trapezius retracts the scapula?",
   ["middle fibres", "superior fibres", "inferior fibres", "clavicular fibres"], "A",
   "Superior fibres elevate, middle fibres retract, inferior fibres depress the scapula."),
 q("Rhomboids", "medium", "The rhomboids and levator scapulae share which nerve supply?",
   ["dorsal scapular nerve", "accessory nerve", "thoracodorsal nerve", "long thoracic nerve"], "A",
   "The dorsal scapular nerve (C5) supplies the rhomboids and levator scapulae."),
 q("Latissimus actions", "medium", "Latissimus dorsi acting on the humerus produces:",
   ["extension, adduction and medial rotation", "flexion, abduction and lateral rotation", "extension, abduction and lateral rotation", "flexion, adduction and medial rotation"], "A",
   "Latissimus dorsi extends, adducts and medially rotates the arm (the 'swimmer's muscle')."),
 q("Serratus posterior", "medium", "The serratus posterior muscles act mainly as:",
   ["accessory muscles of respiration", "primary extensors of the spine", "retractors of the scapula", "rotators of the head"], "A",
   "Serratus posterior superior elevates upper ribs and the inferior part steadies the lower ribs."),
 q("Serratus posterior nerve", "medium", "Serratus posterior superior and inferior are supplied by:",
   ["intercostal nerves", "posterior rami", "the accessory nerve", "the dorsal scapular nerve"], "A",
   "As intermediate extrinsic muscles they are supplied by anterior rami (intercostal nerves)."),
 q("Thoracolumbar fascia", "medium", "The intrinsic back muscles are wrapped by the:",
   ["thoracolumbar fascia", "transversalis fascia", "endothoracic fascia", "investing cervical fascia"], "A",
   "The thoracolumbar fascia encloses the deep back muscles in the thoracic and lumbar regions."),
 q("Transversospinales", "medium", "The transversospinales group consists of:",
   ["semispinalis, multifidus, rotatores", "iliocostalis, longissimus, spinalis", "splenius capitis and cervicis", "rectus capitis and obliquus"], "A",
   "Semispinalis, multifidus and rotatores run from transverse processes to spinous processes above."),
 q("Multifidus", "medium", "Multifidus is particularly important as a:",
   ["segmental lumbar stabiliser", "primary flexor of the trunk", "retractor of the scapula", "lateral rotator of the arm"], "A",
   "Multifidus stabilises individual lumbar segments and contributes to proprioception."),
 q("Splenius", "medium", "Acting on one side, splenius capitis turns the face:",
   ["to the same side", "to the opposite side", "upward only", "downward only"], "A",
   "Unilateral splenius rotates the face to the same side; bilateral contraction extends the head and neck."),
 q("SCM rotation", "medium", "Acting on one side, sternocleidomastoid turns the face:",
   ["to the opposite side", "to the same side", "upward only", "downward only"], "A",
   "One SCM rotates the face to the opposite side; both together flex the neck."),
 q("Trunk flexion", "medium", "Flexion of the thoracic and lumbar spine is produced mainly by:",
   ["psoas major and rectus abdominis", "erector spinae and the multifidus", "latissimus dorsi and the trapezius", "the rotatores and semispinalis"], "A",
   "Flexion comes from muscles anterior to the column, assisted by gravity."),
 # hard
 q("Eccentric control", "hard", "When a standing person bends forward slowly, the movement is controlled mainly by:",
   ["erector spinae contracting eccentrically", "rectus abdominis contracting concentrically", "psoas major contracting isometrically", "latissimus dorsi contracting concentrically"], "A",
   "Gravity flexes the trunk; the extensors lengthen under tension (eccentric) to brake the movement."),
 q("Accessory nerve injury", "hard", "Damage to the accessory nerve in the posterior triangle most likely causes:",
   ["a drooping shoulder", "a winged scapula", "loss of arm adduction", "inability to extend the spine"], "A",
   "Trapezius paralysis lets the shoulder droop and weakens abduction above 90°; winging follows long thoracic nerve injury."),
 q("Suboccipital triangle", "hard", "The suboccipital triangle contains the vertebral artery and the:",
   ["posterior ramus of C1", "anterior ramus of C2", "greater occipital nerve root", "accessory nerve"], "A",
   "The suboccipital nerve (posterior ramus of C1) lies in the triangle with the vertebral artery."),
 q("Suboccipital action", "hard", "The suboccipital muscles mainly:",
   ["extend and laterally flex the head", "flex the head on the neck", "elevate the first and second ribs", "retract and rotate the scapula"], "A",
   "They act on the atlanto-occipital and atlantoaxial joints to extend, laterally flex and rotate the head."),
 q("Scalenes", "hard", "The brachial plexus and subclavian artery pass between which two muscles?",
   ["anterior and middle scalenes", "middle and posterior scalenes", "SCM and anterior scalene", "longus colli and anterior scalene"], "A",
   "The interscalene gap between anterior and middle scalenes is a site of thoracic outlet compression."),
 q("Torticollis", "hard", "Congenital torticollis from a shortened left SCM tilts the head:",
   ["left, with the face turned right", "right, with the face turned left", "left, with the face turned left", "right, with the face turned right"], "A",
   "SCM tilts the head to its own side and turns the face to the opposite side."),
 q("Prevertebral muscles", "hard", "Longus capitis and longus colli are supplied by:",
   ["anterior rami of C1–C6", "posterior rami of C1–C6", "the accessory nerve", "the dorsal scapular nerve"], "A",
   "These prevertebral neck flexors lie anterior to the column and take anterior ramus supply."),
 q("Embryology", "hard", "Intrinsic back muscles develop from the:",
   ["epaxial part of the myotome", "hypaxial part of the myotome", "lateral plate mesoderm", "neural crest"], "A",
   "Epaxial myotome forms the true back muscles (posterior rami); hypaxial forms body wall and limb muscles (anterior rami)."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
