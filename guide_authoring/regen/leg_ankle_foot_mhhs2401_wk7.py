#!/usr/bin/env python3
"""MHHS2401 W7 · L15 Leg, Ankle & Foot — NEW gallery bank (tell-free, no daredevil)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "leg_ankle_foot_mhhs2401_wk7.html"
META = {
    "title": "The Leg, Ankle Joint & Foot",
    "subject": "Musculoskeletal System",
    "unit": "MHHS2401",
    "content": ("MHHS2401 L15 (Dr Mirjana Strkalj): tibia/fibula and the ankle mortise; the three "
                "leg compartments (anterior dorsiflexors - deep fibular nerve; lateral evertors - "
                "superficial fibular nerve; posterior plantarflexors - tibial nerve) and the tarsal "
                "tunnel; bones and joints of the foot; the ankle and subtalar joints, their "
                "movements, ligaments and injuries (inversion sprain, Pott's fracture); and the "
                "arches of the foot with the spring and plantar ligaments."),
}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Anterior compartment", "difficulty": "easy",
  "question": "The anterior compartment of the leg acts at the ankle to produce:",
  "options": ["A. dorsiflexion", "B. plantar flexion",
              "C. eversion", "D. inversion"],
  "correct_answer": "A",
  "explanation": "The anterior compartment muscles dorsiflex the ankle and extend the toes; they are supplied by the deep fibular nerve.",
  "related": ["Anterior compartment", "Leg compartments"]},

 {"topic": "Lateral compartment", "difficulty": "easy",
  "question": "The lateral compartment of the leg mainly produces which movement?",
  "options": ["A. eversion", "B. inversion",
              "C. dorsiflexion", "D. toe flexion"],
  "correct_answer": "A",
  "explanation": "Fibularis longus and brevis evert the foot; they are supplied by the superficial fibular nerve.",
  "related": ["Lateral compartment", "Leg compartments"]},

 {"topic": "Ankle mortise", "difficulty": "easy",
  "question": "The ankle mortise is formed by the distal ends of which two bones?",
  "options": ["A. tibia and fibula", "B. tibia and talus",
              "C. fibula and calcaneus", "D. talus and calcaneus"],
  "correct_answer": "A",
  "explanation": "The distal tibia and fibula form the mortise, a deep socket that grips the trochlea of the talus.",
  "related": ["Ankle mortise", "Bones"]},

 {"topic": "Posterior compartment", "difficulty": "easy",
  "question": "The posterior compartment of the leg is supplied by which nerve?",
  "options": ["A. the tibial nerve", "B. the deep fibular nerve",
              "C. the superficial fibular nerve", "D. the saphenous nerve"],
  "correct_answer": "A",
  "explanation": "The tibial nerve supplies the posterior compartment, which plantar flexes the ankle, flexes the toes and inverts the foot.",
  "related": ["Posterior compartment", "Leg compartments"]},

 {"topic": "Ankle injuries", "difficulty": "easy",
  "question": "Which is the most frequently injured major joint in the body?",
  "options": ["A. the ankle", "B. the knee",
              "C. the hip", "D. the shoulder"],
  "correct_answer": "A",
  "explanation": "The ankle is the most frequently injured major joint; sprains are the commonest injury and are usually inversion injuries.",
  "related": ["Ankle injuries", "Ligaments"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Anterior nerve", "difficulty": "medium",
  "question": "Which nerve supplies the anterior compartment of the leg?",
  "options": ["A. the deep fibular nerve", "B. the superficial fibular nerve",
              "C. the tibial nerve", "D. the sural nerve"],
  "correct_answer": "A",
  "explanation": "The deep fibular nerve supplies the anterior compartment; a lesion causes foot-drop from lost dorsiflexion.",
  "related": ["Anterior nerve", "Leg compartments"]},

 {"topic": "Triceps surae", "difficulty": "medium",
  "question": "The triceps surae of the superficial posterior compartment comprises the soleus, plantaris and:",
  "options": ["A. gastrocnemius", "B. tibialis posterior",
              "C. flexor hallucis longus", "D. popliteus"],
  "correct_answer": "A",
  "explanation": "The superficial posterior group (triceps surae) is gastrocnemius, soleus and plantaris, the powerful plantarflexors.",
  "related": ["Triceps surae", "Posterior compartment"]},

 {"topic": "Distal tibiofibular joint", "difficulty": "medium",
  "question": "The distal tibiofibular joint is which type of joint?",
  "options": ["A. a fibrous joint", "B. a synovial hinge",
              "C. a synovial plane", "D. a ball-and-socket"],
  "correct_answer": "A",
  "explanation": "The distal tibiofibular joint is a fibrous syndesmosis permitting no movement, giving strong support to the ankle mortise.",
  "related": ["Distal tibiofibular joint", "Ankle mortise"]},

 {"topic": "Ankle stability", "difficulty": "medium",
  "question": "The ankle joint is most stable in which position?",
  "options": ["A. dorsiflexion", "B. plantar flexion",
              "C. inversion", "D. eversion"],
  "correct_answer": "A",
  "explanation": "The talar trochlea is wider anteriorly, so dorsiflexion wedges it tightly into the mortise; plantar flexion is looser and less stable.",
  "related": ["Ankle stability", "Movements"]},

 {"topic": "Subtalar joint", "difficulty": "medium",
  "question": "Inversion and eversion of the foot occur mainly at which joint?",
  "options": ["A. the subtalar joint", "B. the ankle joint",
              "C. the interphalangeal joints", "D. the tarsometatarsal joint"],
  "correct_answer": "A",
  "explanation": "The subtalar (talocalcaneal) joint, between talus and calcaneus, produces inversion and eversion, not the ankle hinge.",
  "related": ["Subtalar joint", "Movements"]},

 {"topic": "Deltoid ligament", "difficulty": "medium",
  "question": "The strong ligament on the medial side of the ankle is the:",
  "options": ["A. deltoid ligament", "B. anterior talofibular ligament",
              "C. calcaneofibular ligament", "D. spring ligament"],
  "correct_answer": "A",
  "explanation": "The medial ankle is guarded by the strong deltoid ligament; the lateral side has three weaker ligaments.",
  "related": ["Deltoid ligament", "Ligaments"]},

 {"topic": "Ankle sprain", "difficulty": "medium",
  "question": "A typical ankle sprain is which mechanism of injury?",
  "options": ["A. an inversion injury", "B. an eversion injury",
              "C. a dorsiflexion injury", "D. a rotation injury"],
  "correct_answer": "A",
  "explanation": "Most sprains are inversion injuries that tear the weaker lateral ligaments; the strong deltoid resists eversion.",
  "related": ["Ankle sprain", "Ligaments"]},

 {"topic": "Transverse tarsal joint", "difficulty": "medium",
  "question": "The transverse tarsal joint is the combined calcaneocuboid and:",
  "options": ["A. talocalcaneonavicular joint", "B. subtalar joint",
              "C. tarsometatarsal joint", "D. cuneonavicular joint"],
  "correct_answer": "A",
  "explanation": "The transverse tarsal joint combines the calcaneocuboid and talocalcaneonavicular joints; it is the plane for surgical amputation of the foot.",
  "related": ["Transverse tarsal joint", "Foot joints"]},

 {"topic": "Spring ligament", "difficulty": "medium",
  "question": "The plantar calcaneonavicular (spring) ligament is key to maintaining which arch?",
  "options": ["A. the medial longitudinal arch", "B. the lateral longitudinal arch",
              "C. the transverse arch", "D. the metatarsal arch"],
  "correct_answer": "A",
  "explanation": "The spring ligament supports the head of the talus and maintains the medial longitudinal arch of the foot.",
  "related": ["Spring ligament", "Arches"]},

 {"topic": "Flexor hallucis longus", "difficulty": "medium",
  "question": "Flexor hallucis longus is especially important during which phase of walking?",
  "options": ["A. toe-off", "B. heel-strike",
              "C. mid-swing", "D. mid-stance"],
  "correct_answer": "A",
  "explanation": "At toe-off the great toe is the last part of the foot to leave the ground and propels the body forward, driven by flexor hallucis longus.",
  "related": ["Flexor hallucis longus", "Posterior compartment"]},

 {"topic": "Tibialis posterior", "difficulty": "medium",
  "question": "Tibialis posterior, a deep posterior muscle, produces which combination?",
  "options": ["A. inversion and plantar flexion", "B. eversion and dorsiflexion",
              "C. inversion and dorsiflexion", "D. eversion and plantar flexion"],
  "correct_answer": "A",
  "explanation": "Tibialis posterior inverts and plantar flexes the foot and helps support the medial arch.",
  "related": ["Tibialis posterior", "Posterior compartment"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Tarsal tunnel", "difficulty": "hard",
  "question": "Which nerve passes through the tarsal tunnel behind the medial malleolus?",
  "options": ["A. the tibial nerve", "B. the deep fibular nerve",
              "C. the sural nerve", "D. the saphenous nerve"],
  "correct_answer": "A",
  "explanation": "The tarsal tunnel transmits the tibial nerve with the posterior tibial artery and the deep posterior tendons into the sole.",
  "related": ["Tarsal tunnel", "Posterior compartment"]},

 {"topic": "Pott's fracture", "difficulty": "hard",
  "question": "Because the deltoid ligament is so strong, a forced eversion injury tends to:",
  "options": ["A. avulse the medial malleolus", "B. tear the deltoid ligament",
              "C. rupture the spring ligament", "D. dislocate the subtalar joint"],
  "correct_answer": "A",
  "explanation": "Forced eversion is resisted by the strong deltoid ligament, so the force avulses the medial malleolus, a Pott's fracture-dislocation.",
  "related": ["Pott's fracture", "Ligaments"]},

 {"topic": "Trochlea shape", "difficulty": "hard",
  "question": "The ankle is unstable in plantar flexion because the talar trochlea is:",
  "options": ["A. narrower posteriorly", "B. narrower anteriorly",
              "C. perfectly cylindrical", "D. flat on top"],
  "correct_answer": "A",
  "explanation": "The trochlea is wider anteriorly and narrower posteriorly, so plantar flexion brings the narrow part into the mortise, loosening the grip.",
  "related": ["Trochlea shape", "Ankle stability"]},

 {"topic": "Long plantar ligament", "difficulty": "hard",
  "question": "The long plantar ligament forms a tunnel for the tendon of which muscle?",
  "options": ["A. fibularis longus", "B. tibialis posterior",
              "C. flexor hallucis longus", "D. flexor digitorum longus"],
  "correct_answer": "A",
  "explanation": "The long plantar ligament forms a tunnel that carries the fibularis longus tendon across the sole to the medial foot.",
  "related": ["Long plantar ligament", "Arches"]},

 {"topic": "Popliteus", "difficulty": "hard",
  "question": "Popliteus, a deep posterior muscle, acts at the knee to:",
  "options": ["A. unlock the extended knee", "B. lock the knee straight",
              "C. extend the leg fully", "D. plantar flex the ankle"],
  "correct_answer": "A",
  "explanation": "Popliteus laterally rotates the femur on the fixed tibia to unlock the fully extended knee so flexion can begin.",
  "related": ["Popliteus", "Posterior compartment"]},

 {"topic": "Flexor digitorum longus", "difficulty": "hard",
  "question": "Flexor digitorum longus flexes which toes?",
  "options": ["A. the lateral four toes", "B. the great toe only",
              "C. all five toes", "D. the great and second toes"],
  "correct_answer": "A",
  "explanation": "Flexor digitorum longus flexes the lateral four toes; flexor hallucis longus flexes the great toe (hallux).",
  "related": ["Flexor digitorum longus", "Posterior compartment"]},

 {"topic": "Foot drop", "difficulty": "hard",
  "question": "Injury to which nerve abolishes dorsiflexion and causes foot-drop?",
  "options": ["A. the deep fibular nerve", "B. the tibial nerve",
              "C. the superficial fibular nerve", "D. the sural nerve"],
  "correct_answer": "A",
  "explanation": "The deep fibular nerve drives the anterior dorsiflexors, so its injury causes foot-drop; the common fibular nerve is often the site.",
  "related": ["Foot drop", "Anterior compartment"]},

 {"topic": "Talonavicular joint", "difficulty": "hard",
  "question": "The talonavicular part of the talocalcaneonavicular joint is which joint type?",
  "options": ["A. ball-and-socket", "B. synovial plane",
              "C. hinge", "D. condyloid"],
  "correct_answer": "A",
  "explanation": "The talonavicular articulation is a ball-and-socket joint, giving the midfoot rotational adaptability.",
  "related": ["Talonavicular joint", "Foot joints"]},

 {"topic": "Acquired flat foot", "difficulty": "hard",
  "question": "The commonest cause of acquired adult flat foot (pes planus) is dysfunction of the:",
  "options": ["A. tibialis posterior tendon", "B. fibularis longus tendon",
              "C. Achilles tendon", "D. plantaris tendon"],
  "correct_answer": "A",
  "explanation": "Tibialis posterior dysfunction overloads the spring ligament, the talar head drops, and the medial arch collapses into pes planus.",
  "related": ["Acquired flat foot", "Arches"]},

 {"topic": "Subtalar ligaments", "difficulty": "hard",
  "question": "The subtalar joint is held together mainly by which ligaments?",
  "options": ["A. interosseous talocalcaneal", "B. anterior talofibular",
              "C. plantar calcaneonavicular", "D. long plantar"],
  "correct_answer": "A",
  "explanation": "The interosseous talocalcaneal ligaments bind the talus to the calcaneus at the subtalar joint, which allows inversion and eversion.",
  "related": ["Subtalar ligaments", "Subtalar joint"]},
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
