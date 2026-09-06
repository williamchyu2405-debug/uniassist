#!/usr/bin/env python3
"""MHHS2401 W5 · Muscle Physiology III (reflexes) — regenerated bank (length-matched, no bracket tells, no daredevil)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "muscle_physiology_3_mhhs2401.html"
BANK = json.load(open(os.path.join(HERE, "..", "..", "guide_quizzes.json"), encoding="utf-8"))
META = {k: BANK[KEY][k] for k in ("title", "subject", "unit", "content")}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Reflex definition", "difficulty": "easy",
  "question": "A reflex is best described as a response that is:",
  "options": ["A. rapid and involuntary", "B. slow and voluntary",
              "C. rapid and voluntary", "D. slow and conscious"],
  "correct_answer": "A",
  "explanation": "A reflex is a rapid, involuntary response mediated by the spinal cord, allowing adjustments without waiting for conscious thought.",
  "related": ["Reflex definition", "Reflex arc"]},

 {"topic": "Reflex arc", "difficulty": "easy",
  "question": "How many components make up the reflex arc?",
  "options": ["A. five", "B. three",
              "C. four", "D. six"],
  "correct_answer": "A",
  "explanation": "The reflex arc has five parts: receptor, sensory neuron, integration center, motor neuron and effector.",
  "related": ["Reflex arc", "Reflex definition"]},

 {"topic": "Proprioceptors", "difficulty": "easy",
  "question": "Which muscle receptor senses stretch, or change in length?",
  "options": ["A. the muscle spindle", "B. the Golgi tendon organ",
              "C. the Pacinian corpuscle", "D. the free nerve ending"],
  "correct_answer": "A",
  "explanation": "The muscle spindle in the muscle belly senses stretch (length); the Golgi tendon organ senses tension.",
  "related": ["Proprioceptors", "Muscle spindle"]},

 {"topic": "Stretch reflex", "difficulty": "easy",
  "question": "The classic knee-jerk reflex is an example of which reflex?",
  "options": ["A. the stretch reflex", "B. the withdrawal reflex",
              "C. the crossed-extensor reflex", "D. the flexor reflex"],
  "correct_answer": "A",
  "explanation": "The knee-jerk is the stretch reflex, the simplest monosynaptic reflex driven by the muscle spindle.",
  "related": ["Stretch reflex", "Monosynaptic"]},

 {"topic": "Reflex sides", "difficulty": "easy",
  "question": "In anatomy, the term ipsilateral means:",
  "options": ["A. the same side", "B. the opposite side",
              "C. the front side", "D. the back side"],
  "correct_answer": "A",
  "explanation": "Ipsilateral means the same side; contralateral means the opposite side, as in the crossed-extensor reflex.",
  "related": ["Reflex sides", "Reciprocal inhibition"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Reflex arc", "difficulty": "medium",
  "question": "What is the correct order of the reflex arc components?",
  "options": ["A. receptor, sensory, integration, motor, effector",
              "B. receptor, motor, integration, sensory, effector",
              "C. effector, sensory, integration, motor, receptor",
              "D. sensory, receptor, motor, integration, effector"],
  "correct_answer": "A",
  "explanation": "The reflex arc runs receptor, then sensory neuron in, then integration center, then motor neuron out, then effector.",
  "related": ["Reflex arc", "Reflex definition"]},

 {"topic": "Afferent and efferent", "difficulty": "medium",
  "question": "The sensory (afferent) neuron of a reflex arc carries the signal:",
  "options": ["A. into the spinal cord", "B. out of the spinal cord",
              "C. toward the effector muscle", "D. along the tendon organ"],
  "correct_answer": "A",
  "explanation": "The afferent sensory neuron carries the signal into the cord; the efferent motor neuron carries the command out.",
  "related": ["Afferent and efferent", "Reflex arc"]},

 {"topic": "Proprioceptors", "difficulty": "medium",
  "question": "The Golgi tendon organ is located at the:",
  "options": ["A. muscle-tendon junction", "B. centre of the belly",
              "C. neuromuscular junction", "D. bony attachment site"],
  "correct_answer": "A",
  "explanation": "The Golgi tendon organ sits at the muscle-tendon junction, where it senses tension; the spindle sits in the muscle belly.",
  "related": ["Proprioceptors", "Golgi tendon organ"]},

 {"topic": "Muscle spindle", "difficulty": "medium",
  "question": "When a muscle spindle is stretched, the reflex response of that muscle is to:",
  "options": ["A. contract", "B. relax",
              "C. lengthen further", "D. do nothing"],
  "correct_answer": "A",
  "explanation": "The spindle guards length, so stretch fires the stretch reflex and the muscle contracts to resist being lengthened.",
  "related": ["Muscle spindle", "Stretch reflex"]},

 {"topic": "Golgi tendon organ", "difficulty": "medium",
  "question": "When a Golgi tendon organ senses excessive tension, the muscle response is to:",
  "options": ["A. relax", "B. contract",
              "C. shorten quickly", "D. stay unchanged"],
  "correct_answer": "A",
  "explanation": "The Golgi tendon organ guards tension, so excessive force makes the muscle relax, protecting it and the tendon from tearing.",
  "related": ["Golgi tendon organ", "Proprioceptors"]},

 {"topic": "Monosynaptic", "difficulty": "medium",
  "question": "A monosynaptic reflex has how many synapses in the central nervous system?",
  "options": ["A. one", "B. two",
              "C. three", "D. none"],
  "correct_answer": "A",
  "explanation": "A monosynaptic reflex has a single CNS synapse directly from sensory to motor neuron, making it the fastest reflex.",
  "related": ["Monosynaptic", "Reflex arc"]},

 {"topic": "Polysynaptic", "difficulty": "medium",
  "question": "What feature distinguishes a polysynaptic reflex from a monosynaptic one?",
  "options": ["A. it includes interneurons", "B. it lacks a receptor",
              "C. it skips the motor neuron", "D. it bypasses the cord"],
  "correct_answer": "A",
  "explanation": "Polysynaptic reflexes include one or more interneurons and two or more synapses, allowing routing, inhibition and divergence.",
  "related": ["Polysynaptic", "Monosynaptic"]},

 {"topic": "Reciprocal inhibition", "difficulty": "medium",
  "question": "Reciprocal inhibition means that as the agonist contracts, the antagonist is:",
  "options": ["A. relaxed", "B. contracted",
              "C. stretched", "D. stimulated"],
  "correct_answer": "A",
  "explanation": "In reciprocal inhibition, an inhibitory interneuron relaxes the antagonist while the agonist contracts, giving unopposed movement.",
  "related": ["Reciprocal inhibition", "Ipsilateral reflexes"]},

 {"topic": "Crossed-extensor reflex", "difficulty": "medium",
  "question": "In the crossed-extensor reflex, while one limb withdraws, the opposite limb:",
  "options": ["A. extends to bear weight", "B. also withdraws sharply",
              "C. stays completely still", "D. flexes toward the body"],
  "correct_answer": "A",
  "explanation": "As the stimulated limb withdraws, the opposite limb extends to bear the shifted weight, maintaining postural stability.",
  "related": ["Crossed-extensor reflex", "Contralateral reflexes"]},

 {"topic": "Reflex sides", "difficulty": "medium",
  "question": "A contralateral reflex acts on which side of the body?",
  "options": ["A. the opposite side", "B. the same side",
              "C. both sides equally", "D. neither side directly"],
  "correct_answer": "A",
  "explanation": "Contralateral means opposite side; the crossed-extensor reflex acts on both limbs but in opposite directions.",
  "related": ["Reflex sides", "Crossed-extensor reflex"]},

 {"topic": "Reflex function", "difficulty": "medium",
  "question": "The general function of reflexes is to:",
  "options": ["A. maintain homeostasis rapidly", "B. store long-term memories",
              "C. generate conscious thought", "D. slow down all responses"],
  "correct_answer": "A",
  "explanation": "Reflexes maintain homeostasis by making rapid positional or functional adjustments without waiting for conscious thought.",
  "related": ["Reflex function", "Reflex definition"]},

 {"topic": "Rhythmic movement", "difficulty": "medium",
  "question": "Rhythmic movements such as walking and breathing combine reflex activity with:",
  "options": ["A. voluntary control", "B. purely random firing",
              "C. no neural input", "D. sensory input only"],
  "correct_answer": "A",
  "explanation": "Rhythmic movements combine involuntary reflex cycling with voluntary control that starts, stops and changes them.",
  "related": ["Rhythmic movement", "Central pattern generators"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Spindle afferent", "difficulty": "hard",
  "question": "The muscle spindle sends its signal along which afferent fibre?",
  "options": ["A. the 1a fibre", "B. the 1b fibre",
              "C. the C fibre", "D. the alpha fibre"],
  "correct_answer": "A",
  "explanation": "The muscle spindle uses the 1a afferent fibre; the Golgi tendon organ uses the 1b fibre.",
  "related": ["Spindle afferent", "Muscle spindle"]},

 {"topic": "Proprioceptor activity", "difficulty": "hard",
  "question": "The Golgi tendon organ is chiefly active during which type of contraction?",
  "options": ["A. isometric contraction", "B. isotonic contraction",
              "C. eccentric lengthening", "D. resting muscle tone"],
  "correct_answer": "A",
  "explanation": "The Golgi tendon organ is most active during isometric contraction, when tension is high; the spindle is active in isotonic contraction and tone.",
  "related": ["Proprioceptor activity", "Golgi tendon organ"]},

 {"topic": "Interneurons", "difficulty": "hard",
  "question": "Reciprocal inhibition requires an interneuron because it must convert the input into a signal that is:",
  "options": ["A. inhibitory", "B. excitatory",
              "C. sensory", "D. rhythmic"],
  "correct_answer": "A",
  "explanation": "Only an interneuron can turn the excitatory sensory input into an inhibitory signal that switches off the antagonist's motor neuron.",
  "related": ["Interneurons", "Reciprocal inhibition"]},

 {"topic": "Cord lesion", "difficulty": "hard",
  "question": "If a spinal cord lesion lies above a reflex arc, the reflex itself will:",
  "options": ["A. persist, often exaggerated", "B. disappear completely",
              "C. become fully voluntary", "D. reverse its direction"],
  "correct_answer": "A",
  "explanation": "The arc still exists and fires, often exaggerated, but the brain can no longer modulate it, which helps localise the lesion.",
  "related": ["Cord lesion", "Reflex definition"]},

 {"topic": "Central pattern generators", "difficulty": "hard",
  "question": "Central pattern generators contribute to rhythmic movement by:",
  "options": ["A. cycling the pattern spontaneously", "B. initiating the whole activity",
              "C. changing the rate consciously", "D. detecting muscle tension"],
  "correct_answer": "A",
  "explanation": "Once an activity is started, central pattern generators fire the reflexes spontaneously to cycle the pattern without further thought.",
  "related": ["Central pattern generators", "Rhythmic movement"]},

 {"topic": "Crossed-extensor circuit", "difficulty": "hard",
  "question": "The crossed-extensor reflex reaches the opposite limb because the sensory neuron:",
  "options": ["A. diverges to crossing interneurons", "B. synapses directly on motor neurons",
              "C. ascends only to the brain", "D. returns to the same receptor"],
  "correct_answer": "A",
  "explanation": "The sensory neuron diverges to crossing interneurons that carry the signal to the opposite side and flip the muscle pattern.",
  "related": ["Crossed-extensor circuit", "Polysynaptic"]},

 {"topic": "Voluntary modulation", "difficulty": "hard",
  "question": "In rhythmic movement, the voluntary contribution from the brain is mainly to:",
  "options": ["A. start, stop and change intensity", "B. maintain the repetitive cycle",
              "C. detect stretch in the belly", "D. relay tension from tendons"],
  "correct_answer": "A",
  "explanation": "Voluntary control initiates or terminates the activity and changes its rate or intensity, while the pattern generator maintains the cycle.",
  "related": ["Voluntary modulation", "Central pattern generators"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
