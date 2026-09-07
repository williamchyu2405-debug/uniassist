#!/usr/bin/env python3
"""MHHS2401 W7 · L13 Anterior & Medial Thigh + Knee — NEW gallery bank (tell-free, no daredevil)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "anterior_medial_thigh_knee_mhhs2401_wk7.html"
META = {
    "title": "Anterior & Medial Thigh + the Knee Joint",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("MHHS2401 L13 (Dr Mirjana Strkalj): muscles of the anterior thigh compartment "
                "(iliopsoas, sartorius, quadriceps femoris, TFL; femoral nerve; flex hip, extend "
                "knee) and medial thigh compartment (adductors, gracilis, pectineus, obturator "
                "externus; obturator nerve; adduction); the femoral triangle and adductor canal; "
                "and the knee joint - articular surfaces, menisci, extracapsular and intracapsular "
                "ligaments, movements, stability, and injuries (unhappy triad, ACL/PCL, "
                "Osgood-Schlatter)."),
}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Compartments", "difficulty": "easy",
  "question": "The anterior compartment of the thigh is supplied by which nerve?",
  "options": ["A. the femoral nerve", "B. the obturator nerve",
              "C. the sciatic nerve", "D. the tibial nerve"],
  "correct_answer": "A",
  "explanation": "The femoral nerve supplies the anterior compartment, which flexes the thigh at the hip and extends the leg at the knee.",
  "related": ["Compartments", "Anterior compartment"]},

 {"topic": "Compartments", "difficulty": "easy",
  "question": "The main action of the medial compartment of the thigh is:",
  "options": ["A. adduction", "B. extension",
              "C. abduction", "D. dorsiflexion"],
  "correct_answer": "A",
  "explanation": "The medial compartment is the adductor group, pulling the thigh toward the midline; it is supplied by the obturator nerve.",
  "related": ["Compartments", "Medial compartment"]},

 {"topic": "Iliopsoas", "difficulty": "easy",
  "question": "Which muscle is the chief flexor of the thigh at the hip?",
  "options": ["A. iliopsoas", "B. gracilis",
              "C. sartorius", "D. pectineus"],
  "correct_answer": "A",
  "explanation": "Iliopsoas (psoas major plus iliacus) is the chief hip flexor, inserting on the lesser trochanter of the femur.",
  "related": ["Iliopsoas", "Anterior compartment"]},

 {"topic": "Knee joint", "difficulty": "easy",
  "question": "The knee is classified as which type of joint?",
  "options": ["A. a modified hinge joint", "B. a ball-and-socket joint",
              "C. a pivot joint", "D. a saddle joint"],
  "correct_answer": "A",
  "explanation": "The knee is a synovial modified hinge joint, with a tibiofemoral and a patellofemoral articulation.",
  "related": ["Knee joint", "Movements"]},

 {"topic": "Quadriceps", "difficulty": "easy",
  "question": "The quadriceps femoris acts at the knee to produce:",
  "options": ["A. extension", "B. flexion",
              "C. medial rotation", "D. lateral rotation"],
  "correct_answer": "A",
  "explanation": "The quadriceps femoris is the great extensor of the leg at the knee; the hamstrings flex it.",
  "related": ["Quadriceps", "Movements"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Iliopsoas", "difficulty": "medium",
  "question": "Iliopsoas inserts onto which bony landmark?",
  "options": ["A. the lesser trochanter", "B. the greater trochanter",
              "C. the tibial tuberosity", "D. the linea aspera"],
  "correct_answer": "A",
  "explanation": "Psoas major and iliacus fuse and pass under the inguinal ligament to insert together on the lesser trochanter.",
  "related": ["Iliopsoas", "Anterior compartment"]},

 {"topic": "Sartorius", "difficulty": "medium",
  "question": "Sartorius runs from the ASIS to which insertion?",
  "options": ["A. the pes anserinus", "B. the tibial tuberosity",
              "C. the lesser trochanter", "D. the iliotibial tract"],
  "correct_answer": "A",
  "explanation": "Sartorius, the most superficial anterior thigh muscle, descends from the ASIS to the pes anserinus on the medial proximal tibia.",
  "related": ["Sartorius", "Pes anserinus"]},

 {"topic": "Sartorius", "difficulty": "medium",
  "question": "Besides flexing the hip and knee, sartorius also:",
  "options": ["A. abducts and laterally rotates the thigh", "B. adducts and medially rotates the thigh",
              "C. extends the thigh at the hip", "D. everts the foot at the ankle"],
  "correct_answer": "A",
  "explanation": "Sartorius abducts and laterally rotates the thigh, giving the cross-legged 'tailor's position' that names it.",
  "related": ["Sartorius", "Anterior compartment"]},

 {"topic": "Quadriceps", "difficulty": "medium",
  "question": "The quadriceps inserts on the tibial tuberosity by way of the:",
  "options": ["A. patellar ligament", "B. iliotibial tract",
              "C. pes anserinus", "D. adductor tubercle"],
  "correct_answer": "A",
  "explanation": "All four heads converge on the quadriceps tendon, then the patella, then the patellar ligament onto the tibial tuberosity.",
  "related": ["Quadriceps", "Knee joint"]},

 {"topic": "Rectus femoris", "difficulty": "medium",
  "question": "Which quadriceps head also flexes the thigh at the hip?",
  "options": ["A. rectus femoris", "B. vastus lateralis",
              "C. vastus medialis", "D. vastus intermedius"],
  "correct_answer": "A",
  "explanation": "Rectus femoris arises from the AIIS and crosses the hip, so it flexes the thigh as well as extending the knee.",
  "related": ["Rectus femoris", "Quadriceps"]},

 {"topic": "Tensor fasciae latae", "difficulty": "medium",
  "question": "Tensor fasciae latae inserts into which structure?",
  "options": ["A. the iliotibial tract", "B. the patellar ligament",
              "C. the pes anserinus", "D. the linea aspera"],
  "correct_answer": "A",
  "explanation": "TFL runs from the iliac crest into the iliotibial tract, which it tenses to help stabilise the hip and knee.",
  "related": ["Tensor fasciae latae", "Anterior compartment"]},

 {"topic": "Medial compartment", "difficulty": "medium",
  "question": "The medial thigh muscles share a common origin around the:",
  "options": ["A. ischiopubic ramus", "B. greater trochanter",
              "C. anterior iliac spine", "D. tibial plateau"],
  "correct_answer": "A",
  "explanation": "The adductor group arises around the ischiopubic ramus and is supplied by the obturator nerve.",
  "related": ["Medial compartment", "Adductors"]},

 {"topic": "Pectineus", "difficulty": "medium",
  "question": "Which medial-compartment muscle forms the floor of the femoral triangle?",
  "options": ["A. pectineus", "B. gracilis",
              "C. adductor longus", "D. obturator externus"],
  "correct_answer": "A",
  "explanation": "Pectineus (with iliopsoas) forms the floor of the femoral triangle; it runs from the pecten pubis to the pectineal line.",
  "related": ["Pectineus", "Femoral triangle"]},

 {"topic": "Gracilis", "difficulty": "medium",
  "question": "Gracilis, the most superficial medial muscle, inserts on the:",
  "options": ["A. pes anserinus", "B. linea aspera",
              "C. adductor tubercle", "D. lesser trochanter"],
  "correct_answer": "A",
  "explanation": "Gracilis crosses two joints, adducting the hip and flexing the knee, and inserts on the pes anserinus.",
  "related": ["Gracilis", "Pes anserinus"]},

 {"topic": "Femoral triangle", "difficulty": "medium",
  "question": "The femoral triangle transmits the femoral nerve, the femoral vein and the:",
  "options": ["A. femoral artery", "B. great saphenous vein",
              "C. saphenous nerve", "D. obturator nerve"],
  "correct_answer": "A",
  "explanation": "The femoral triangle transmits, from lateral to medial, the femoral nerve, femoral artery and femoral vein.",
  "related": ["Femoral triangle", "Anterior compartment"]},

 {"topic": "Knee movements", "difficulty": "medium",
  "question": "Flexion of the leg at the knee is produced mainly by the:",
  "options": ["A. hamstrings", "B. quadriceps",
              "C. adductors", "D. gluteals"],
  "correct_answer": "A",
  "explanation": "The hamstrings flex the leg at the knee; the quadriceps extends it.",
  "related": ["Knee movements", "Knee joint"]},

 {"topic": "Knee stability", "difficulty": "medium",
  "question": "The single most important muscular stabiliser of the knee is the:",
  "options": ["A. quadriceps femoris", "B. biceps femoris",
              "C. gastrocnemius", "D. sartorius"],
  "correct_answer": "A",
  "explanation": "The quadriceps, especially the inferior fibres of vastus medialis and lateralis, is the most important muscular stabiliser of the knee.",
  "related": ["Knee stability", "Knee joint"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Adductor magnus", "difficulty": "hard",
  "question": "The hamstring part of adductor magnus is supplied by which nerve?",
  "options": ["A. the sciatic nerve", "B. the obturator nerve",
              "C. the femoral nerve", "D. the superior gluteal nerve"],
  "correct_answer": "A",
  "explanation": "The hamstring part of adductor magnus is supplied by the sciatic (tibial) nerve; the adductor part takes the obturator nerve.",
  "related": ["Adductor magnus", "Medial compartment"]},

 {"topic": "Pes anserinus", "difficulty": "hard",
  "question": "Which three muscles converge at the pes anserinus?",
  "options": ["A. sartorius, gracilis, semitendinosus", "B. sartorius, gracilis, semimembranosus",
              "C. gracilis, pectineus, semitendinosus", "D. sartorius, rectus femoris, gracilis"],
  "correct_answer": "A",
  "explanation": "The pes anserinus is formed by sartorius, gracilis and semitendinosus, muscles from three compartments on three nerves.",
  "related": ["Pes anserinus", "Medial compartment"]},

 {"topic": "Menisci", "difficulty": "hard",
  "question": "The medial meniscus is clinically important because it is attached to the:",
  "options": ["A. tibial collateral ligament", "B. fibular collateral ligament",
              "C. anterior cruciate ligament", "D. patellar ligament"],
  "correct_answer": "A",
  "explanation": "The medial meniscus is attached to the tibial (medial) collateral ligament, so the two tend to tear together.",
  "related": ["Menisci", "Unhappy triad"]},

 {"topic": "ACL", "difficulty": "hard",
  "question": "The anterior cruciate ligament resists which movement of the tibia?",
  "options": ["A. anterior translation", "B. posterior translation",
              "C. medial rotation", "D. adduction"],
  "correct_answer": "A",
  "explanation": "The ACL resists anterior translation of the tibia on the femur, so its loss gives a positive anterior drawer or Lachman test.",
  "related": ["ACL", "Knee clinical"]},

 {"topic": "PCL", "difficulty": "hard",
  "question": "The posterior cruciate ligament is classically injured in which mechanism?",
  "options": ["A. a dashboard injury", "B. a lateral blow to the knee",
              "C. a fall on the heel", "D. a twisting pivot"],
  "correct_answer": "A",
  "explanation": "A dashboard injury drives the flexed tibia backward, tearing the PCL, which resists posterior tibial translation.",
  "related": ["PCL", "Knee clinical"]},

 {"topic": "Unhappy triad", "difficulty": "hard",
  "question": "The 'unhappy triad' of the knee involves the ACL, the medial meniscus and the:",
  "options": ["A. tibial collateral ligament", "B. fibular collateral ligament",
              "C. posterior cruciate ligament", "D. patellar ligament"],
  "correct_answer": "A",
  "explanation": "The unhappy triad is a torn tibial (medial) collateral ligament, medial meniscus and ACL, from a lateral blow to a planted knee.",
  "related": ["Unhappy triad", "Knee clinical"]},

 {"topic": "Popliteus", "difficulty": "hard",
  "question": "Popliteus initiates knee flexion by acting to:",
  "options": ["A. unlock the extended knee", "B. extend the leg fully",
              "C. lock the knee straight", "D. adduct the thigh"],
  "correct_answer": "A",
  "explanation": "Popliteus rotates the femur on the fixed tibia to unlock the fully extended, locked knee so that flexion can begin.",
  "related": ["Popliteus", "Knee movements"]},

 {"topic": "Knee rotation", "difficulty": "hard",
  "question": "Medial rotation of the flexed leg at the knee is produced by the:",
  "options": ["A. semitendinosus and semimembranosus", "B. biceps femoris",
              "C. quadriceps femoris", "D. the popliteus muscle"],
  "correct_answer": "A",
  "explanation": "Semitendinosus and semimembranosus medially rotate the flexed leg; biceps femoris rotates it laterally.",
  "related": ["Knee rotation", "Knee movements"]},

 {"topic": "Osgood-Schlatter", "difficulty": "hard",
  "question": "Osgood-Schlatter disease is a traction apophysitis at the:",
  "options": ["A. tibial tuberosity", "B. medial epicondyle",
              "C. patellar apex", "D. adductor tubercle"],
  "correct_answer": "A",
  "explanation": "Repeated quadriceps traction on the immature tibial tuberosity causes Osgood-Schlatter disease in active adolescents.",
  "related": ["Osgood-Schlatter", "Knee clinical"]},

 {"topic": "Adductor canal", "difficulty": "hard",
  "question": "The adductor canal carries the femoral vessels and which nerve to the knee?",
  "options": ["A. the saphenous nerve", "B. the obturator nerve",
              "C. the sciatic nerve", "D. the common fibular nerve"],
  "correct_answer": "A",
  "explanation": "The adductor canal transmits the femoral artery, femoral vein and the saphenous nerve down toward the knee.",
  "related": ["Adductor canal", "Femoral triangle"]},
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
