#!/usr/bin/env python3
"""MHHS2401 W8 · L17 Blood supply of the lower limb — NEW gallery bank (tell-free, no daredevil)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "lower_limb_blood_supply_mhhs2401_wk8.html"
META = {
    "title": "Blood Supply of the Lower Limb",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("MHHS2401 L17 (Dr Mirjana Strkalj): arterial supply of the lower limb (femoral "
                "artery, femoral triangle and its VAN contents, profunda femoris and its perforating "
                "and circumflex femoral branches, adductor canal, popliteal fossa, anterior/posterior "
                "tibial and dorsalis pedis arteries, pulse points); venous drainage (great and small "
                "saphenous superficial veins, deep venae comitantes, varicose veins, DVT); and "
                "lymphatic drainage to the inguinal nodes."),
}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Arterial highway", "difficulty": "easy",
  "question": "The femoral artery becomes the popliteal artery at which landmark?",
  "options": ["A. the adductor hiatus", "B. the inguinal ligament",
              "C. the popliteal fossa apex", "D. the medial malleolus"],
  "correct_answer": "A",
  "explanation": "The femoral vessels pass through the adductor hiatus in adductor magnus to enter the popliteal fossa as the popliteal vessels.",
  "related": ["Arterial highway", "Adductor canal"]},

 {"topic": "Femoral triangle", "difficulty": "easy",
  "question": "The contents of the femoral triangle from medial to lateral are the femoral:",
  "options": ["A. vein, artery, nerve", "B. nerve, artery, vein",
              "C. artery, vein, nerve", "D. nerve, vein, artery"],
  "correct_answer": "A",
  "explanation": "From medial to lateral the contents are the femoral Vein, Artery and Nerve (VAN); the vein lies nearest the pubis.",
  "related": ["Femoral triangle", "VAN"]},

 {"topic": "Profunda femoris", "difficulty": "easy",
  "question": "Which artery is the chief artery of the thigh?",
  "options": ["A. the profunda femoris", "B. the obturator artery",
              "C. the popliteal artery", "D. the dorsalis pedis"],
  "correct_answer": "A",
  "explanation": "The profunda femoris (deep femoral artery) is the largest branch of the femoral artery and the chief artery supplying the thigh.",
  "related": ["Profunda femoris", "Thigh vessels"]},

 {"topic": "Popliteal fossa", "difficulty": "easy",
  "question": "Which structure lies deepest in the popliteal fossa?",
  "options": ["A. the popliteal artery", "B. the tibial nerve",
              "C. the popliteal vein", "D. the saphenous nerve"],
  "correct_answer": "A",
  "explanation": "From superficial to deep the order is tibial nerve, popliteal vein, popliteal artery, so the artery lies deepest against the joint.",
  "related": ["Popliteal fossa", "Contents"]},

 {"topic": "Superficial veins", "difficulty": "easy",
  "question": "The two superficial veins of the lower limb are the great and:",
  "options": ["A. small saphenous veins", "B. femoral veins",
              "C. popliteal veins", "D. tibial veins"],
  "correct_answer": "A",
  "explanation": "The great (long) and small (short) saphenous veins are the superficial veins, lying in the superficial fascia.",
  "related": ["Superficial veins", "Venous drainage"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Femoral pulse", "difficulty": "medium",
  "question": "The femoral pulse is felt at the midpoint between the pubic symphysis and the:",
  "options": ["A. ASIS", "B. iliac crest",
              "C. greater trochanter", "D. pubic tubercle"],
  "correct_answer": "A",
  "explanation": "The femoral pulse is felt by pressing backward at the midpoint between the ASIS and the pubic symphysis (the mid-inguinal point).",
  "related": ["Femoral pulse", "Femoral triangle"]},

 {"topic": "Femoral hernia", "difficulty": "medium",
  "question": "A femoral hernia typically presents as a mass in which position relative to the pubic tubercle?",
  "options": ["A. inferolateral", "B. superomedial",
              "C. directly superior", "D. directly medial"],
  "correct_answer": "A",
  "explanation": "A femoral hernia appears inferolateral to the pubic tubercle, distinguishing it from an inguinal hernia, which is superomedial.",
  "related": ["Femoral hernia", "Femoral triangle"]},

 {"topic": "Femoral hernia", "difficulty": "medium",
  "question": "Femoral hernias are more common in females mainly because of the:",
  "options": ["A. broader pelvic inlet", "B. weaker abdominal muscles",
              "C. longer inguinal ligament", "D. absent femoral canal"],
  "correct_answer": "A",
  "explanation": "The broader female pelvic inlet widens the femoral ring, making femoral hernias commoner in females.",
  "related": ["Femoral hernia", "Femoral triangle"]},

 {"topic": "Profunda branches", "difficulty": "medium",
  "question": "The profunda femoris supplies all three thigh compartments through its:",
  "options": ["A. perforating arteries", "B. circumflex arteries",
              "C. recurrent arteries", "D. genicular arteries"],
  "correct_answer": "A",
  "explanation": "The profunda femoris gives 3-4 perforating arteries that wrap around the femur and supply all three thigh compartments.",
  "related": ["Profunda branches", "Profunda femoris"]},

 {"topic": "Circumflex femoral", "difficulty": "medium",
  "question": "The medial and lateral circumflex femoral arteries mainly supply the:",
  "options": ["A. the femoral head", "B. muscles of the foot",
              "C. skin of the thigh", "D. the adductor hiatus"],
  "correct_answer": "A",
  "explanation": "The circumflex femoral arteries ring the proximal femur and supply its head and neck via posterior retinacular arteries.",
  "related": ["Circumflex femoral", "Profunda femoris"]},

 {"topic": "Adductor canal", "difficulty": "medium",
  "question": "The adductor canal transmits the femoral artery, femoral vein and which nerve?",
  "options": ["A. the saphenous nerve", "B. the tibial nerve",
              "C. the obturator nerve", "D. the sciatic nerve"],
  "correct_answer": "A",
  "explanation": "The adductor canal carries the femoral artery, femoral vein and the saphenous nerve from the femoral triangle toward the knee.",
  "related": ["Adductor canal", "Thigh vessels"]},

 {"topic": "Popliteal boundaries", "difficulty": "medium",
  "question": "The superolateral boundary of the popliteal fossa is formed by which muscle?",
  "options": ["A. biceps femoris", "B. semitendinosus",
              "C. gastrocnemius", "D. sartorius"],
  "correct_answer": "A",
  "explanation": "Biceps femoris forms the superolateral boundary; semitendinosus and semimembranosus form the superomedial boundary.",
  "related": ["Popliteal boundaries", "Popliteal fossa"]},

 {"topic": "Foot arteries", "difficulty": "medium",
  "question": "The anterior tibial artery continues onto the dorsum of the foot as the:",
  "options": ["A. dorsalis pedis artery", "B. posterior tibial artery",
              "C. fibular artery", "D. plantar arch"],
  "correct_answer": "A",
  "explanation": "The anterior tibial artery becomes the dorsalis pedis on the dorsum of the foot, where its pulse is palpable.",
  "related": ["Foot arteries", "Pulses"]},

 {"topic": "Posterior tibial pulse", "difficulty": "medium",
  "question": "The posterior tibial pulse is felt at which location?",
  "options": ["A. behind the medial malleolus", "B. behind the lateral malleolus",
              "C. on the dorsum of the foot", "D. in the femoral triangle"],
  "correct_answer": "A",
  "explanation": "The posterior tibial pulse is felt behind the medial malleolus, about midway between it and the heel.",
  "related": ["Posterior tibial pulse", "Pulses"]},

 {"topic": "Great saphenous vein", "difficulty": "medium",
  "question": "The great saphenous vein drains into which deep vein?",
  "options": ["A. the femoral vein", "B. the popliteal vein",
              "C. the posterior tibial vein", "D. the external iliac vein"],
  "correct_answer": "A",
  "explanation": "The great saphenous vein ascends the medial limb and drains into the femoral vein at the saphenous opening.",
  "related": ["Great saphenous vein", "Venous drainage"]},

 {"topic": "Lymphatic drainage", "difficulty": "medium",
  "question": "Lymph from the lower limb drains mainly to which group of nodes?",
  "options": ["A. the inguinal nodes", "B. the axillary nodes",
              "C. the cervical nodes", "D. the para-aortic nodes"],
  "correct_answer": "A",
  "explanation": "Both superficial and deep lower-limb lymphatics converge on the inguinal nodes, the deep set passing via popliteal nodes.",
  "related": ["Lymphatic drainage", "Inguinal nodes"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Adductor hiatus", "difficulty": "hard",
  "question": "The adductor canal ends at the adductor hiatus, which is a gap in the tendon of which muscle?",
  "options": ["A. adductor magnus", "B. adductor longus",
              "C. gracilis", "D. sartorius"],
  "correct_answer": "A",
  "explanation": "The adductor hiatus is the gap in the tendon of adductor magnus through which the femoral vessels pass to become popliteal.",
  "related": ["Adductor hiatus", "Adductor canal"]},

 {"topic": "Popliteal artery", "difficulty": "hard",
  "question": "The popliteal artery is at particular risk of injury in which event?",
  "options": ["A. a posterior knee dislocation", "B. a lateral ankle sprain",
              "C. a femoral neck fracture", "D. a hip dislocation"],
  "correct_answer": "A",
  "explanation": "Lying deepest against the joint, the popliteal artery can be torn by a posterior knee dislocation, a limb-threatening emergency.",
  "related": ["Popliteal artery", "Popliteal fossa"]},

 {"topic": "Popliteal contents", "difficulty": "hard",
  "question": "From superficial to deep, the neurovascular contents of the popliteal fossa are the:",
  "options": ["A. nerve, vein, artery", "B. artery, vein, nerve",
              "C. vein, nerve, artery", "D. nerve, artery, vein"],
  "correct_answer": "A",
  "explanation": "The order superficial to deep is tibial nerve, popliteal vein, popliteal artery, so the artery is deepest.",
  "related": ["Popliteal contents", "Popliteal fossa"]},

 {"topic": "Obturator artery", "difficulty": "hard",
  "question": "Which artery, a branch of the internal iliac, helps supply the adductor muscles?",
  "options": ["A. the obturator artery", "B. the profunda femoris",
              "C. the popliteal artery", "D. the superior gluteal artery"],
  "correct_answer": "A",
  "explanation": "The obturator artery, from the internal iliac, helps the profunda femoris supply the adductor muscles of the medial compartment.",
  "related": ["Obturator artery", "Thigh vessels"]},

 {"topic": "Perforating veins", "difficulty": "hard",
  "question": "The valves of the perforating veins allow blood to flow in which direction?",
  "options": ["A. superficial to deep", "B. deep to superficial",
              "C. distal to proximal only", "D. in both directions freely"],
  "correct_answer": "A",
  "explanation": "Perforator valves permit flow only from the superficial to the deep veins; their failure contributes to varicose veins.",
  "related": ["Perforating veins", "Venous drainage"]},

 {"topic": "Small saphenous vein", "difficulty": "hard",
  "question": "The small saphenous vein ascends the posterior calf to drain into the:",
  "options": ["A. popliteal vein", "B. femoral vein",
              "C. great saphenous vein", "D. posterior tibial vein"],
  "correct_answer": "A",
  "explanation": "The small (short) saphenous vein runs up the posterior calf and drains into the popliteal vein.",
  "related": ["Small saphenous vein", "Venous drainage"]},

 {"topic": "Dorsalis pedis pulse", "difficulty": "hard",
  "question": "The dorsalis pedis pulse is felt on the dorsum of the foot lateral to the tendon of:",
  "options": ["A. extensor hallucis longus", "B. tibialis anterior",
              "C. extensor digitorum longus", "D. flexor hallucis longus"],
  "correct_answer": "A",
  "explanation": "The dorsalis pedis pulse is palpated lateral to the extensor hallucis longus tendon on the dorsum of the foot.",
  "related": ["Dorsalis pedis pulse", "Pulses"]},

 {"topic": "Intermittent claudication", "difficulty": "hard",
  "question": "Intermittent claudication (exertional leg pain relieved by rest) is caused by:",
  "options": ["A. peripheral arterial disease", "B. deep venous thrombosis",
              "C. lymphatic obstruction", "D. a femoral hernia"],
  "correct_answer": "A",
  "explanation": "Atherosclerotic narrowing (peripheral arterial disease) starves the leg muscles on exertion, causing intermittent claudication.",
  "related": ["Intermittent claudication", "Pulses"]},

 {"topic": "Lymphangitis", "difficulty": "hard",
  "question": "Lymphangitis of the lower limb classically appears as:",
  "options": ["A. red streaks tracking proximally", "B. a cold pale foot",
              "C. sudden calf swelling", "D. a pulsatile groin mass"],
  "correct_answer": "A",
  "explanation": "Infection tracking along the lymph vessels causes lymphangitis, seen as tender red streaks running proximally toward the groin nodes.",
  "related": ["Lymphangitis", "Lymphatic drainage"]},
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
