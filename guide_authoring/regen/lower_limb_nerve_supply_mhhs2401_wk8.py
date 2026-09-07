#!/usr/bin/env python3
"""MHHS2401 W8 · L18 Nerve supply of the lower limb — NEW gallery bank (tell-free, no daredevil)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "lower_limb_nerve_supply_mhhs2401_wk8.html"
META = {
    "title": "Nerve Supply of the Lower Limb",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("MHHS2401 L18 (Dr Mirjana Strkalj): the lumbar plexus (L1-L4) and sacral plexus "
                "(L4-S4); the femoral nerve (L2-L4, anterior thigh, saphenous branch) and obturator "
                "nerve (L2-L4, adductors); the sciatic nerve (L4-S3 = tibial + common fibular); the "
                "nerves of the leg and foot (tibial, deep and superficial fibular, sural) and their "
                "palsies (foot-drop, tibial lesion); and lower-limb dermatomes and myotomes."),
}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Lumbar plexus", "difficulty": "easy",
  "question": "The lumbar plexus is formed from the anterior rami of which roots?",
  "options": ["A. L1 to L4", "B. L4 to S4",
              "C. T12 to L2", "D. S1 to S4"],
  "correct_answer": "A",
  "explanation": "The lumbar plexus arises from the anterior rami of L1 to L4 and gives the femoral and obturator nerves.",
  "related": ["Lumbar plexus", "Plexuses"]},

 {"topic": "Femoral nerve", "difficulty": "easy",
  "question": "The femoral nerve supplies the muscles of which thigh compartment?",
  "options": ["A. the anterior compartment", "B. the medial compartment",
              "C. the posterior compartment", "D. the lateral compartment"],
  "correct_answer": "A",
  "explanation": "The femoral nerve supplies the anterior compartment (quadriceps, sartorius, pectineus), which extends the knee and flexes the hip.",
  "related": ["Femoral nerve", "Lumbar plexus"]},

 {"topic": "Sciatic nerve", "difficulty": "easy",
  "question": "The sciatic nerve is composed of which two nerves?",
  "options": ["A. tibial and common fibular", "B. femoral and obturator",
              "C. tibial and saphenous", "D. sural and femoral"],
  "correct_answer": "A",
  "explanation": "The sciatic nerve is the tibial and common fibular nerves bound in one sheath; they separate at the apex of the popliteal fossa.",
  "related": ["Sciatic nerve", "Sacral plexus"]},

 {"topic": "Foot-drop", "difficulty": "easy",
  "question": "Injury to which nerve classically causes foot-drop?",
  "options": ["A. the common fibular nerve", "B. the tibial nerve",
              "C. the femoral nerve", "D. the obturator nerve"],
  "correct_answer": "A",
  "explanation": "The common fibular nerve, injured at the fibular neck, paralyses dorsiflexion and eversion, causing foot-drop.",
  "related": ["Foot-drop", "Common fibular nerve"]},

 {"topic": "Sacral plexus", "difficulty": "easy",
  "question": "The sacral plexus is formed from the anterior rami of which roots?",
  "options": ["A. L4 to S4", "B. L1 to L4",
              "C. S2 to S4", "D. T12 to L3"],
  "correct_answer": "A",
  "explanation": "The sacral plexus arises from the anterior rami of L4 to S4 and gives the sciatic nerve; its lower segments supply the perineum.",
  "related": ["Sacral plexus", "Plexuses"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Femoral root value", "difficulty": "medium",
  "question": "What is the spinal root value of the femoral nerve?",
  "options": ["A. L2 to L4", "B. L4 to S3",
              "C. L1 to L3", "D. S1 to S3"],
  "correct_answer": "A",
  "explanation": "The femoral nerve has a root value of L2 to L4, the same as the obturator nerve.",
  "related": ["Femoral root value", "Femoral nerve"]},

 {"topic": "Femoral course", "difficulty": "medium",
  "question": "The femoral nerve emerges from which border of psoas major?",
  "options": ["A. the lateral border", "B. the medial border",
              "C. the anterior surface", "D. the posterior surface"],
  "correct_answer": "A",
  "explanation": "The femoral nerve emerges from the lateral border of psoas major and passes deep to the inguinal ligament into the thigh.",
  "related": ["Femoral course", "Femoral nerve"]},

 {"topic": "Obturator course", "difficulty": "medium",
  "question": "The obturator nerve emerges from which border of psoas major?",
  "options": ["A. the medial border", "B. the lateral border",
              "C. the anterior surface", "D. the inferior tip"],
  "correct_answer": "A",
  "explanation": "The obturator nerve emerges from the medial border of psoas major and passes through the obturator foramen into the medial thigh.",
  "related": ["Obturator course", "Obturator nerve"]},

 {"topic": "Obturator foramen", "difficulty": "medium",
  "question": "The obturator nerve enters the thigh through which opening?",
  "options": ["A. the obturator foramen", "B. the greater sciatic foramen",
              "C. the adductor hiatus", "D. the femoral ring"],
  "correct_answer": "A",
  "explanation": "The obturator nerve leaves the pelvis through the obturator foramen, then splits to supply the adductor muscles.",
  "related": ["Obturator foramen", "Obturator nerve"]},

 {"topic": "Saphenous nerve", "difficulty": "medium",
  "question": "The saphenous nerve is the terminal cutaneous branch of which nerve?",
  "options": ["A. the femoral nerve", "B. the obturator nerve",
              "C. the tibial nerve", "D. the sciatic nerve"],
  "correct_answer": "A",
  "explanation": "The saphenous nerve is the terminal cutaneous branch of the femoral nerve, supplying the medial leg and foot.",
  "related": ["Saphenous nerve", "Femoral nerve"]},

 {"topic": "Obturator function", "difficulty": "medium",
  "question": "The obturator nerve supplies which muscle group?",
  "options": ["A. the adductor muscles", "B. the quadriceps femoris",
              "C. the hamstrings", "D. the gluteal muscles"],
  "correct_answer": "A",
  "explanation": "The obturator nerve supplies the adductor muscles and obturator externus of the medial compartment.",
  "related": ["Obturator function", "Obturator nerve"]},

 {"topic": "Sciatic root value", "difficulty": "medium",
  "question": "What is the spinal root value of the sciatic nerve?",
  "options": ["A. L4 to S3", "B. L2 to L4",
              "C. L1 to L4", "D. S2 to S4"],
  "correct_answer": "A",
  "explanation": "The sciatic nerve has a root value of L4 to S3, arising from the sacral plexus.",
  "related": ["Sciatic root value", "Sciatic nerve"]},

 {"topic": "Sciatic split", "difficulty": "medium",
  "question": "The tibial and common fibular divisions of the sciatic nerve separate at the:",
  "options": ["A. the popliteal fossa apex", "B. neck of the fibula",
              "C. adductor hiatus", "D. greater sciatic foramen"],
  "correct_answer": "A",
  "explanation": "The two divisions run bound together down the thigh and separate at the apex of the popliteal fossa.",
  "related": ["Sciatic split", "Sciatic nerve"]},

 {"topic": "Tibial nerve", "difficulty": "medium",
  "question": "The tibial nerve supplies which muscle group of the leg?",
  "options": ["A. the posterior flexors", "B. the anterior dorsiflexors",
              "C. the lateral evertors", "D. the medial adductors"],
  "correct_answer": "A",
  "explanation": "The tibial nerve supplies the posterior compartment flexors (plantarflexors) and the intrinsic flexors of the foot.",
  "related": ["Tibial nerve", "Sciatic nerve"]},

 {"topic": "Common fibular", "difficulty": "medium",
  "question": "The common fibular nerve supplies the muscles of which compartments?",
  "options": ["A. anterior and lateral", "B. posterior and medial",
              "C. posterior only", "D. medial only"],
  "correct_answer": "A",
  "explanation": "The common fibular nerve supplies the anterior and lateral compartments of the leg via its deep and superficial branches.",
  "related": ["Common fibular", "Sciatic nerve"]},

 {"topic": "IM injection", "difficulty": "medium",
  "question": "To avoid the sciatic nerve, a gluteal intramuscular injection is placed in the:",
  "options": ["A. upper outer quadrant", "B. lower inner quadrant",
              "C. lower outer quadrant", "D. upper inner quadrant"],
  "correct_answer": "A",
  "explanation": "The upper outer (superolateral) quadrant is the safe site, lying over gluteus medius and away from the sciatic nerve.",
  "related": ["IM injection", "Sciatic nerve"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Tibial lesion", "difficulty": "hard",
  "question": "A patient with a tibial nerve lesion is characteristically unable to:",
  "options": ["A. stand on tiptoe", "B. extend the knee",
              "C. dorsiflex the ankle", "D. adduct the thigh"],
  "correct_answer": "A",
  "explanation": "The tibial nerve drives the plantarflexors, so its lesion means the patient cannot stand on tiptoe, with sensory loss over the sole.",
  "related": ["Tibial lesion", "Tibial nerve"]},

 {"topic": "Common fibular site", "difficulty": "hard",
  "question": "The common fibular nerve is most vulnerable to injury as it winds around the:",
  "options": ["A. neck of the fibula", "B. medial malleolus",
              "C. head of the femur", "D. adductor hiatus"],
  "correct_answer": "A",
  "explanation": "The common fibular nerve winds superficially around the neck of the fibula against bone, making it the most commonly injured lower-limb nerve.",
  "related": ["Common fibular site", "Foot-drop"]},

 {"topic": "Deep fibular nerve", "difficulty": "hard",
  "question": "The deep fibular nerve supplies which compartment of the leg?",
  "options": ["A. the anterior compartment", "B. the lateral compartment",
              "C. the posterior compartment", "D. the medial compartment"],
  "correct_answer": "A",
  "explanation": "The deep fibular nerve supplies the anterior compartment (the dorsiflexors), so its loss is the main cause of foot-drop.",
  "related": ["Deep fibular nerve", "Common fibular"]},

 {"topic": "Superficial fibular nerve", "difficulty": "hard",
  "question": "The superficial fibular nerve supplies the lateral compartment evertors and the skin of the:",
  "options": ["A. dorsum of the foot", "B. sole of the foot",
              "C. first web space", "D. medial malleolus"],
  "correct_answer": "A",
  "explanation": "The superficial fibular nerve supplies the evertors and most of the skin of the dorsum of the foot; the deep fibular covers the first web space.",
  "related": ["Superficial fibular nerve", "Common fibular"]},

 {"topic": "Sural nerve", "difficulty": "hard",
  "question": "The sural nerve is a cutaneous nerve supplying the:",
  "options": ["A. posterolateral leg and lateral foot", "B. anterior thigh and medial leg",
              "C. sole of the foot", "D. first web space"],
  "correct_answer": "A",
  "explanation": "The sural nerve supplies the posterolateral leg and lateral foot and is commonly harvested for nerve grafts.",
  "related": ["Sural nerve", "Leg nerves"]},

 {"topic": "Dermatomes", "difficulty": "hard",
  "question": "Which dermatome covers the dorsum of the foot and the great toe?",
  "options": ["A. L5", "B. L4",
              "C. S1", "D. L2"],
  "correct_answer": "A",
  "explanation": "L5 covers the dorsum of the foot and great toe; L4 covers the medial malleolus and S1 the lateral foot.",
  "related": ["Dermatomes", "Skin maps"]},

 {"topic": "Dermatomes", "difficulty": "hard",
  "question": "The S1 dermatome is tested over which area?",
  "options": ["A. the lateral foot", "B. the medial malleolus",
              "C. the anterior thigh", "D. the great toe"],
  "correct_answer": "A",
  "explanation": "S1 covers the lateral foot, little toe and heel; L4 is the medial malleolus and L5 the great toe.",
  "related": ["Dermatomes", "Skin maps"]},

 {"topic": "Myotomes", "difficulty": "hard",
  "question": "Ankle plantarflexion is controlled predominantly by which segments?",
  "options": ["A. S1 to S2", "B. L1 to L2",
              "C. L3 to L4", "D. L5 to S1"],
  "correct_answer": "A",
  "explanation": "Ankle plantarflexion is an S1-S2 myotome; hip flexion is L1-L2 and knee extension L3-L4.",
  "related": ["Myotomes", "Movement maps"]},

 {"topic": "Myotomes", "difficulty": "hard",
  "question": "Knee extension is controlled mainly by which segments?",
  "options": ["A. L3 to L4", "B. S1 to S2",
              "C. L1 to L2", "D. S2 to S3"],
  "correct_answer": "A",
  "explanation": "Knee extension is an L3-L4 myotome (via the femoral nerve to quadriceps); knee flexion is L5-S2.",
  "related": ["Myotomes", "Movement maps"]},
]

if __name__ == "__main__":
    bad = check_bank(Q)
    print(f"{KEY}: {summarize(Q)}")
    if bad:
        print("VIOLATIONS:")
        for i, vs in bad.items():
            print(f"  [{i}] {Q[i].get('question','')[:60]}")
            for v in vs: print(f"        - {v}")
        sys.exit(1)
    print("All questions clean ✅")
    bank_path = os.path.join(HERE, "..", "..", "guide_quizzes.json")
    bank = json.load(open(bank_path, encoding="utf-8"))
    bank[KEY] = dict(META, questions=Q)
    json.dump(bank, open(bank_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {KEY} into guide_quizzes.json ({len(bank)} galleries)")
