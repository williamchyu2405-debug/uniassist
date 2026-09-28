#!/usr/bin/env python3
"""MEDI2004 W2 · Pharmacokinetics (Absorption & Distribution) — REDO (exam-calibrated).

Round 2 regeneration: fresh applied stems (aspirin weak-acid trapping, GTN sublingual
to dodge first-pass, propranolol high first-pass, warfarin albumin binding, digoxin
large Vd, IV vs oral bioavailability). Same syllabus as Round 1; new stems → the app
re-seeds and wipes old progress. Correct option written first as A.; backend shuffles
positions on seed. META via _meta sidecar.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "pharmacokinetics_medi2004.html"
META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "_meta", KEY + ".meta.json"), encoding="utf-8"))

Q = [
    # ── easy (5) ──
    {"topic": "ADME", "difficulty": "easy",
     "question": "The 'A' and 'D' in the ADME scheme of pharmacokinetics stand for absorption and:",
     "options": ["A. distribution", "B. degradation", "C. digestion", "D. dilution"],
     "correct_answer": "A",
     "explanation": "ADME is Absorption, Distribution, Metabolism, Excretion — the four processes the body applies to a drug.",
     "related": ["ADME", "Pharmacology Basics"]},

    {"topic": "Routes of Administration", "difficulty": "easy",
     "question": "Which route delivers a drug straight into the bloodstream, bypassing absorption?",
     "options": ["A. intravenous", "B. oral", "C. subcutaneous", "D. rectal"],
     "correct_answer": "A",
     "explanation": "Intravenous dosing places drug directly in the blood, so there is no absorption step and bioavailability is complete.",
     "related": ["Routes of Administration", "Bioavailability"]},

    {"topic": "Bioavailability", "difficulty": "easy",
     "question": "By definition, the bioavailability of a drug given intravenously is:",
     "options": ["A. 100%", "B. 50%", "C. 10%", "D. 0%"],
     "correct_answer": "A",
     "explanation": "IV drug reaches the systemic circulation completely, so bioavailability is defined as 100% and is the reference for other routes.",
     "related": ["Bioavailability", "Routes of Administration"]},

    {"topic": "Membrane Transport", "difficulty": "easy",
     "question": "Most small lipid-soluble drugs cross cell membranes mainly by:",
     "options": ["A. simple diffusion", "B. active transport", "C. endocytosis", "D. filtration"],
     "correct_answer": "A",
     "explanation": "Lipid-soluble drugs dissolve through the membrane down their gradient by simple passive diffusion, needing no carrier or energy.",
     "related": ["Membrane Transport", "Absorption"]},

    {"topic": "Distribution", "difficulty": "easy",
     "question": "After absorption, the process that carries a drug from blood into the tissues is called:",
     "options": ["A. distribution", "B. metabolism", "C. excretion", "D. ionisation"],
     "correct_answer": "A",
     "explanation": "Distribution is the reversible movement of drug from the bloodstream into and out of the body's tissues and compartments.",
     "related": ["Distribution", "Body Compartments"]},

    # ── medium (15) ──
    {"topic": "First-Pass Metabolism", "difficulty": "medium",
     "question": "Glyceryl trinitrate is given under the tongue rather than swallowed mainly to avoid:",
     "options": ["A. first-pass metabolism", "B. renal excretion", "C. protein binding", "D. slow diffusion"],
     "correct_answer": "A",
     "explanation": "Sublingual absorption drains into systemic veins, bypassing the liver's first-pass metabolism that would otherwise destroy swallowed GTN.",
     "related": ["First-Pass Metabolism", "Routes of Administration"]},

    {"topic": "First-Pass Metabolism", "difficulty": "medium",
     "question": "A drug with extensive hepatic first-pass metabolism will typically have an oral bioavailability that is:",
     "options": ["A. low", "B. complete", "C. over 100%", "D. exactly equal to IV"],
     "correct_answer": "A",
     "explanation": "First-pass metabolism removes much of an oral dose before it reaches the circulation, so oral bioavailability is low compared with IV.",
     "related": ["First-Pass Metabolism", "Bioavailability"]},

    {"topic": "Weak Acids", "difficulty": "medium",
     "question": "Aspirin is a weak acid with pKa around 3.5. In the acidic stomach (pH ~2) it will be largely:",
     "options": ["A. un-ionised", "B. ionised", "C. metabolised", "D. excreted"],
     "correct_answer": "A",
     "explanation": "A weak acid below its pKa is mostly protonated and un-ionised; the un-ionised form is lipid-soluble and can cross the gastric mucosa.",
     "related": ["Weak Acids", "Ionisation"]},

    {"topic": "Ionisation", "difficulty": "medium",
     "question": "Only the un-ionised fraction of a drug crosses membranes readily because it is:",
     "options": ["A. lipid-soluble", "B. water-soluble", "C. protein-bound", "D. electrically charged"],
     "correct_answer": "A",
     "explanation": "The un-ionised (uncharged) form is lipophilic and dissolves through the lipid membrane, whereas the charged ionised form is trapped in water.",
     "related": ["Ionisation", "Membrane Transport"]},

    {"topic": "Henderson-Hasselbalch", "difficulty": "medium",
     "question": "The Henderson–Hasselbalch equation lets you predict, for a given pH, a drug's ratio of:",
     "options": ["A. ionised to un-ionised", "B. bound to metabolised", "C. absorbed to excreted", "D. oral to IV"],
     "correct_answer": "A",
     "explanation": "Henderson–Hasselbalch relates pH and pKa to the ratio of ionised to un-ionised drug, predicting how much can cross membranes.",
     "related": ["Henderson-Hasselbalch", "Ionisation"]},

    {"topic": "Ion Trapping", "difficulty": "medium",
     "question": "A weak base entering the acidic stomach becomes ionised and cannot diffuse back out. This phenomenon is called:",
     "options": ["A. ion trapping", "B. first-pass", "C. protein binding", "D. active efflux"],
     "correct_answer": "A",
     "explanation": "Ion trapping occurs when a drug ionises on one side of a membrane and, being charged, is held there — a weak base is trapped in acid.",
     "related": ["Ion Trapping", "Weak Acids"]},

    {"topic": "Active Transport", "difficulty": "medium",
     "question": "Unlike simple diffusion, carrier-mediated active transport of a drug can:",
     "options": ["A. move against a gradient", "B. only follow the gradient", "C. never saturate", "D. avoid all proteins"],
     "correct_answer": "A",
     "explanation": "Active transport uses energy to move drug against its concentration gradient and can be saturated, unlike passive diffusion.",
     "related": ["Active Transport", "Membrane Transport"]},

    {"topic": "Protein Binding", "difficulty": "medium",
     "question": "Warfarin is about 99% bound to plasma albumin. Only the drug that is:",
     "options": ["A. unbound is active", "B. bound is active", "C. bound is excreted", "D. bound reaches tissues"],
     "correct_answer": "A",
     "explanation": "Just the free (unbound) fraction can leave the plasma to act, be metabolised and be excreted; bound drug is a temporarily inactive reservoir.",
     "related": ["Protein Binding", "Distribution"]},

    {"topic": "Volume of Distribution", "difficulty": "medium",
     "question": "A drug with a very large volume of distribution is one that mostly resides:",
     "options": ["A. in the tissues", "B. in the plasma", "C. in the urine", "D. in the gut"],
     "correct_answer": "A",
     "explanation": "A large Vd means little drug stays in plasma because most has moved into tissues, giving an apparent volume larger than body water.",
     "related": ["Volume of Distribution", "Distribution"]},

    {"topic": "Body Compartments", "difficulty": "medium",
     "question": "A large water-soluble drug that cannot leave the circulation will distribute into which compartment only?",
     "options": ["A. plasma", "B. total body water", "C. intracellular fluid", "D. body fat"],
     "correct_answer": "A",
     "explanation": "A drug confined to the vascular space distributes only into plasma, giving a small volume of distribution near plasma volume.",
     "related": ["Body Compartments", "Volume of Distribution"]},

    {"topic": "Absorption", "difficulty": "medium",
     "question": "Most oral drug absorption occurs in the small intestine mainly because it offers a very large:",
     "options": ["A. surface area", "B. acid content", "C. muscle mass", "D. blood pH"],
     "correct_answer": "A",
     "explanation": "The small intestine's villi give an enormous absorptive surface area, so even acidic drugs are absorbed there despite the pH.",
     "related": ["Absorption", "Routes of Administration"]},

    {"topic": "Routes of Administration", "difficulty": "medium",
     "question": "Which feature makes the oral route convenient but its absorption less predictable than intravenous?",
     "options": ["A. variable gut absorption", "B. direct blood entry", "C. guaranteed full dose", "D. instant onset"],
     "correct_answer": "A",
     "explanation": "Oral absorption varies with food, gut motility and first-pass metabolism, so the fraction reaching blood is less reliable than IV.",
     "related": ["Routes of Administration", "Bioavailability"]},

    {"topic": "Pharmacokinetic Parameters", "difficulty": "medium",
     "question": "Bioavailability from the oral route is measured by comparing its area under the curve to that of the:",
     "options": ["A. intravenous dose", "B. inhaled dose", "C. topical dose", "D. rectal dose"],
     "correct_answer": "A",
     "explanation": "Oral bioavailability is the ratio of oral AUC to IV AUC, since the IV route is the 100% reference standard.",
     "related": ["Pharmacokinetic Parameters", "Bioavailability"]},

    {"topic": "Drug Interactions", "difficulty": "medium",
     "question": "One highly protein-bound drug can raise another's free level by competing for binding sites on:",
     "options": ["A. albumin", "B. haemoglobin", "C. collagen", "D. keratin"],
     "correct_answer": "A",
     "explanation": "Albumin is the main plasma-binding protein; displacement from it transiently raises the free, active fraction of the other drug.",
     "related": ["Drug Interactions", "Protein Binding"]},

    {"topic": "Pharmacology Basics", "difficulty": "medium",
     "question": "Pharmacokinetics and pharmacodynamics together determine a dose's effect; pharmacokinetics specifically sets the drug's:",
     "options": ["A. concentration over time", "B. receptor mechanism", "C. maximal efficacy", "D. therapeutic class"],
     "correct_answer": "A",
     "explanation": "Pharmacokinetics governs the concentration–time profile reaching the target, which then drives the pharmacodynamic effect.",
     "related": ["Pharmacology Basics", "ADME"]},

    # ── hard (14) ──
    {"topic": "Weak Acids", "difficulty": "hard",
     "question": "Aspirin (a weak acid) is absorbed somewhat in the stomach but far more in the small intestine, chiefly because the intestine offers:",
     "options": ["A. much greater surface area", "B. a far more acidic pH", "C. no blood supply at all", "D. active aspirin pumps"],
     "correct_answer": "A",
     "explanation": "Although less aspirin is un-ionised at intestinal pH, the vast surface area more than compensates, so most absorption happens there.",
     "related": ["Weak Acids", "Absorption"]},

    {"topic": "Ion Trapping", "difficulty": "hard",
     "question": "Breast milk is slightly more acidic than plasma, so a weak-base drug can concentrate in milk by:",
     "options": ["A. ion trapping", "B. first-pass loss", "C. active efflux", "D. protein binding"],
     "correct_answer": "A",
     "explanation": "The weak base becomes ionised in the more acidic milk and is trapped there, an example of pH-dependent ion trapping across a membrane.",
     "related": ["Ion Trapping", "Weak Acids"]},

    {"topic": "Volume of Distribution", "difficulty": "hard",
     "question": "Digoxin has a very large volume of distribution, which tells you a plasma sample taken early after an IV dose may:",
     "options": ["A. underestimate total drug", "B. overestimate total drug", "C. equal the full dose", "D. contain no drug"],
     "correct_answer": "A",
     "explanation": "With a large Vd most drug is in tissues, so plasma holds only a fraction; the concentration reflects little of the total body load.",
     "related": ["Volume of Distribution", "Distribution"]},

    {"topic": "Volume of Distribution", "difficulty": "hard",
     "question": "Using Vd = dose / plasma concentration, a drug that gives a very low plasma concentration for a given dose must have a Vd that is:",
     "options": ["A. large", "B. small", "C. negative", "D. zero"],
     "correct_answer": "A",
     "explanation": "Vd is inversely related to plasma concentration; a low concentration for the dose implies most drug left the plasma, so Vd is large.",
     "related": ["Volume of Distribution", "Pharmacokinetic Parameters"]},

    {"topic": "Protein Binding", "difficulty": "hard",
     "question": "In hypoalbuminaemia, a normally highly-bound drug like phenytoin may cause toxicity at a 'normal' total level because there is more:",
     "options": ["A. free active drug", "B. bound inactive drug", "C. drug in the gut", "D. drug in the urine"],
     "correct_answer": "A",
     "explanation": "Less albumin means a larger free fraction for the same total concentration, so the active free level — and toxicity risk — rises.",
     "related": ["Protein Binding", "Drug Interactions"]},

    {"topic": "First-Pass Metabolism", "difficulty": "hard",
     "question": "Propranolol shows much higher blood levels intravenously than orally at the same dose. The best explanation is extensive:",
     "options": ["A. hepatic first-pass metabolism", "B. renal tubular secretion", "C. plasma protein binding", "D. gastric acid breakdown"],
     "correct_answer": "A",
     "explanation": "Orally absorbed propranolol passes through the liver first and is heavily metabolised, so oral levels are far lower than IV.",
     "related": ["First-Pass Metabolism", "Bioavailability"]},

    {"topic": "Membrane Transport", "difficulty": "hard",
     "question": "Carrier-mediated transport differs from simple diffusion in that, as drug concentration rises, carrier transport will eventually:",
     "options": ["A. saturate", "B. accelerate forever", "C. reverse polarity", "D. stop the heart"],
     "correct_answer": "A",
     "explanation": "A finite number of carriers means transport reaches a maximum (saturates), unlike simple diffusion which keeps rising with gradient.",
     "related": ["Membrane Transport", "Active Transport"]},

    {"topic": "Bioavailability", "difficulty": "hard",
     "question": "A tablet and a capsule of the same drug give the same AUC. They are therefore said to be:",
     "options": ["A. bioequivalent", "B. bioinequivalent", "C. chemically different", "D. therapeutically opposed"],
     "correct_answer": "A",
     "explanation": "Equal bioavailability (AUC) and rate of absorption define bioequivalence — the basis for interchanging brands and generics.",
     "related": ["Bioavailability", "Pharmacokinetic Parameters"]},

    {"topic": "Henderson-Hasselbalch", "difficulty": "hard",
     "question": "For a weak acid, when the surrounding pH equals its pKa, the fraction that is ionised is:",
     "options": ["A. 50%", "B. 0%", "C. 100%", "D. 10%"],
     "correct_answer": "A",
     "explanation": "At pH = pKa the ionised and un-ionised forms are equal, so exactly half the drug is ionised — a direct read from Henderson–Hasselbalch.",
     "related": ["Henderson-Hasselbalch", "Weak Acids"]},

    {"topic": "Body Compartments", "difficulty": "hard",
     "question": "A highly lipophilic drug such as a general anaesthetic tends to accumulate over time in:",
     "options": ["A. body fat", "B. plasma water", "C. bone matrix", "D. urine"],
     "correct_answer": "A",
     "explanation": "Lipophilic drugs partition into adipose tissue, which acts as a slow-filling, slow-emptying reservoir affecting duration of action.",
     "related": ["Body Compartments", "Distribution"]},

    {"topic": "Distribution", "difficulty": "hard",
     "question": "A drug that cannot cross the blood–brain barrier is most likely to be:",
     "options": ["A. highly ionised", "B. highly lipophilic", "C. very small", "D. uncharged"],
     "correct_answer": "A",
     "explanation": "The blood–brain barrier admits lipid-soluble un-ionised drugs; a highly ionised, polar drug is largely excluded from the CNS.",
     "related": ["Distribution", "Ionisation"]},

    {"topic": "Pharmacokinetic Parameters", "difficulty": "hard",
     "question": "If oral AUC is one quarter of the IV AUC for the same dose, the oral bioavailability (F) is about:",
     "options": ["A. 0.25", "B. 0.75", "C. 1.0", "D. 4.0"],
     "correct_answer": "A",
     "explanation": "F = oral AUC / IV AUC = 1/4 = 0.25, meaning only a quarter of the oral dose reaches the systemic circulation.",
     "related": ["Pharmacokinetic Parameters", "Bioavailability"]},

    {"topic": "Active Transport", "difficulty": "hard",
     "question": "An efflux transporter in the gut wall that pumps drug back into the lumen will tend to:",
     "options": ["A. reduce oral absorption", "B. increase oral absorption", "C. raise the Vd", "D. lower protein binding"],
     "correct_answer": "A",
     "explanation": "By actively returning drug to the gut lumen, an efflux pump like P-glycoprotein lowers the fraction absorbed and hence bioavailability.",
     "related": ["Active Transport", "Absorption"]},

    {"topic": "Absorption", "difficulty": "hard",
     "question": "Taking a drug with food that slows gastric emptying will usually change its absorption by making the onset:",
     "options": ["A. slower", "B. instantaneous", "C. impossible", "D. unchanged always"],
     "correct_answer": "A",
     "explanation": "Delayed gastric emptying holds drug in the stomach longer, so it reaches the absorptive small intestine later and onset is slower.",
     "related": ["Absorption", "Routes of Administration"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
