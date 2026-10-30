#!/usr/bin/env python3
"""MHHS2401 L20 · Joints & ligaments of the vertebral column — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "vertebral_column_joints_ligaments_mhhs2401_l20.html"
META = {
    "title": "Joints & Ligaments of the Vertebral Column",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("Joints and ligaments of the vertebral column (MHHS2401 Lecture 20, Dr Mirjana Strkalj): intervertebral "
                "discs, longitudinal ligaments and facet joints; spinal cord level, disc herniation and lumbar puncture; "
                "ligamentum flavum and arch ligaments; craniovertebral joints and their ligaments; joints of the thoracic wall."),
}

Q = [
 # easy
 q("Disc structure", "easy", "The gelatinous centre of an intervertebral disc is the:",
   ["nucleus pulposus", "anulus fibrosus", "ligamentum flavum", "vertebral end-plate"], "A",
   "The disc is an outer anulus fibrosus of fibrocartilage lamellae around a gelatinous nucleus pulposus."),
 q("Joint type", "easy", "Joints between adjacent vertebral bodies are classified as:",
   ["secondary cartilaginous joints", "plane synovial joints", "fibrous syndesmoses", "primary cartilaginous joints"], "A",
   "Intervertebral discs form secondary cartilaginous joints (symphyses)."),
 q("No disc", "easy", "Between which two vertebrae is there NO intervertebral disc?",
   ["C1 and C2", "C2 and C3", "L5 and S1", "T12 and L1"], "A",
   "The atlas and axis articulate by synovial joints around the dens, with no disc between them."),
 q("ALL", "easy", "The anterior longitudinal ligament mainly prevents:",
   ["hyperextension", "hyperflexion", "rotation", "lateral flexion"], "A",
   "The broad, strong ALL on the front of the bodies resists hyperextension and is injured in whiplash."),
 q("Cord level", "easy", "In adults the spinal cord usually ends at about:",
   ["L1/L2", "T10/T11", "L4/L5", "S2"], "A",
   "The column outgrows the cord, so the adult cord ends at L1/L2 and the cauda equina continues below."),
 # medium
 q("PLL", "medium", "The posterior longitudinal ligament fails to protect the posterolateral disc because it is:",
   ["narrow and tapers laterally", "broad and thickest laterally", "attached only to the laminae", "absent in the lumbar region"], "A",
   "The PLL is narrow and weak, leaving the posterolateral anulus unguarded, the usual herniation route."),
 q("Anulus fibres", "medium", "Fibres in adjacent anulus fibrosus lamellae cross at a steep angle, which mainly limits:",
   ["rotation", "extension", "axial loading", "lateral gliding"], "A",
   "The alternating oblique lamellae resist torsion, limiting rotation."),
 q("Nucleus with age", "medium", "With ageing, the nucleus pulposus typically:",
   ["dehydrates and loses height", "becomes more vascular", "calcifies into bone", "increases its water content"], "A",
   "The avascular nucleus is water-rich at birth but dehydrates with age, reducing disc height and resilience."),
 q("Herniation site", "medium", "Lumbar disc herniations are most common at:",
   ["L4/5 and L5/S1", "L1/2 and L2/3", "T11/12 and T12/L1", "L2/3 and L3/4"], "A",
   "The lowest lumbar discs bear the most load and flexion, so they herniate most often."),
 q("Lumbar root", "medium", "A posterolateral L4/5 disc herniation usually compresses which root?",
   ["L5", "L4", "L3", "S1"], "A",
   "In the lumbar spine the exiting L4 root leaves above the disc; the herniation hits the descending L5 root."),
 q("Cervical root", "medium", "A C5/6 disc herniation typically compresses the root numbered:",
   ["C6", "C5", "C7", "C4"], "A",
   "Cervical roots exit above their same-numbered vertebra, so the C6 root exits at C5/6 and is compressed there."),
 q("Lumbar puncture", "medium", "In adults a lumbar puncture is performed at L3/4 or L4/5 because:",
   ["the cord has ended above this level", "the dural sac ends at about L3", "the discs are thinnest at these levels", "the CSF sac ends at around L5"], "A",
   "The adult cord ends at L1/L2 while the CSF sac continues to ~S2, so a needle below L3 avoids the cord."),
 q("Ligamentum flavum", "medium", "The ligamentum flavum connects adjacent:",
   ["laminae", "vertebral bodies", "spinous process tips", "transverse processes"], "A",
   "The elastic yellow ligament joins laminae and forms part of the posterior wall of the canal."),
 q("Flavum function", "medium", "Because it is elastic, the ligamentum flavum helps to:",
   ["restore the spine after flexion", "resist hyperextension of the neck", "anchor the dens to the atlas", "hold the rib head to the body"], "A",
   "Its elastic recoil helps straighten the column after flexion and keeps the canal wall taut."),
 q("Supraspinous", "medium", "The strong ligament joining the tips of the spinous processes from C7 to the sacrum is the:",
   ["supraspinous ligament", "interspinous ligament", "intertransverse ligament", "ligamentum nuchae"], "A",
   "The supraspinous ligament runs along the spinous tips; in the neck it is replaced by the ligamentum nuchae."),
 q("Facet joints", "medium", "Facet (zygapophyseal) joints are:",
   ["plane synovial joints", "secondary cartilaginous joints", "fibrous syndesmoses", "pivot synovial joints"], "A",
   "Facet joints are plane synovial joints whose orientation sets each region's range of movement."),
 q("Atlantoaxial", "medium", "The dens is held against the anterior arch of the atlas by the:",
   ["transverse ligament of the atlas", "paired alar ligaments of the dens", "tectorial membrane over the dens", "anterior longitudinal ligament"], "A",
   "The transverse ligament (part of the cruciate ligament) holds the dens in place; alar ligaments check rotation."),
 # hard
 q("Alar ligaments", "hard", "The alar ligaments, running from the dens to the occipital condyles, mainly:",
   ["check excessive rotation of the head", "prevent hyperextension of the neck", "hold the dens against C1", "continue the PLL over the skull"], "A",
   "Alar ligaments limit rotation; the tectorial membrane continues the PLL upward."),
 q("Herniation direction", "hard", "Discs herniate posteriorly rather than anteriorly mainly because:",
   ["the nucleus sits posteriorly and the PLL is weak", "the anterior anulus is thinner than the posterior anulus", "the ALL is narrower and weaker than the PLL", "spinal extension forces the nucleus pulposus backward"], "A",
   "The nucleus is central-to-posterior, flexion pushes it back, and the narrow PLL gives little support."),
 q("Uncovertebral joints", "hard", "Osteophytes at the uncovertebral joints of Luschka most often cause:",
   ["narrowing of the intervertebral foramen", "compression of the vertebral body", "fusion of the facet joints", "rupture of the ALL"], "A",
   "These C3–C6 joints border the intervertebral foramen, so osteophytes there compress exiting roots."),
 q("Spinal stenosis", "hard", "Hypertrophy of which ligament can narrow the lumbar canal from behind?",
   ["ligamentum flavum", "anterior longitudinal ligament", "supraspinous ligament", "intertransverse ligament"], "A",
   "The ligamentum flavum forms part of the posterior canal wall; its thickening contributes to lumbar spinal stenosis."),
 q("Odontoid fracture", "hard", "A displaced fracture through the C2 pars ('hangman's fracture') is dangerous because it can:",
   ["injure the cord and brainstem", "rupture the vertebral discs", "tear the ligamentum nuchae", "block the sacral foramina"], "A",
   "Fractures of C2 (dens or pars) threaten the upper cervical cord and brainstem."),
 q("Rib joints", "hard", "Each typical rib articulates with the vertebral column at:",
   ["costovertebral and costotransverse joints", "costochondral and sternocostal joints", "interchondral and costovertebral joints", "costotransverse and sternocostal joints"], "A",
   "The rib head joins the vertebral bodies (costovertebral) and the tubercle joins the transverse process (costotransverse)."),
 q("Sternal angle", "hard", "The manubriosternal joint, palpable as the sternal angle, marks the level of:",
   ["the second costal cartilage", "the first costal cartilage", "the fourth costal cartilage", "the xiphoid process"], "A",
   "The sternal angle is a symphysis at the level of rib 2, a key counting landmark."),
 q("Bucket handle", "hard", "Bucket-handle movement of the lower ribs mainly increases the thorax's:",
   ["transverse diameter", "anteroposterior diameter", "vertical diameter", "posterior curvature"], "A",
   "Raising the lateral rib shafts (bucket handle) widens the chest; pump-handle movement of the sternum increases AP diameter."),
 q("Costochondral", "hard", "Costochondral joints between rib and costal cartilage are:",
   ["primary cartilaginous and immobile", "plane synovial and gliding", "secondary cartilaginous symphyses", "saddle synovial joints"], "A",
   "Costochondral joints are primary cartilaginous (synchondroses) with essentially no movement."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
