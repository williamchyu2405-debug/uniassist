#!/usr/bin/env python3
"""MEDI2200 W12 · Glucose metabolism — NEW gallery bank (length-matched, no bracket tells, no daredevil).
New guide: META is defined inline and the entry is written straight into guide_quizzes.json
(assemble_bank.py only rewrites keys already present in the bank)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "glucose_metabolism_medi2200_wk12.html"
META = {
    "title": "Glucose Metabolism",
    "subject": "Human Cell & Molecular Biology",
    "unit": "MEDI2200",
    "content": ("Glucose metabolism (MEDI2200 Wk12, Dr Christine Chiu): redox and energy carriers (ATP, NAD+, FAD), "
                "food energy; carbohydrates and GLUT transport; glycolysis; pyruvate dehydrogenase; the TCA cycle and "
                "its regulation; the electron transport chain, ATP synthase and ADP/phosphate supply; glycogenesis, "
                "glycogenolysis and gluconeogenesis; anaerobic lactate formation and the Cori cycle."),
}

def q(topic, diff, stem, opts, ans, expl):
    return {"topic": topic, "difficulty": diff, "question": stem,
            "options": [f"{'ABCD'[i]}. {o}" for i, o in enumerate(opts)],
            "correct_answer": ans, "explanation": expl, "related": [topic]}

Q = [
 # easy
 q("Redox", "easy", "When electrons pass from a carbohydrate to NAD+, the carbohydrate is:",
   ["oxidised", "reduced", "phosphorylated", "hydrolysed"], "A",
   "Losing electrons is oxidation; NAD+ gains them and is reduced to NADH."),
 q("Glycolysis location", "easy", "Glycolysis takes place in the:",
   ["mitochondrial matrix", "cytosol", "inner mitochondrial membrane", "endoplasmic reticulum"], "B",
   "Glycolysis is a cytosolic, anaerobic 10-step pathway found in all cells."),
 q("Glycolysis yield", "easy", "The net yield of glycolysis from one glucose is:",
   ["2 pyruvate, 2 ATP, 2 NADH", "2 pyruvate, 4 ATP, 2 NADH", "2 acetyl-CoA, 2 ATP, 2 NADH", "2 lactate, 2 ATP, 2 NAD+"], "A",
   "Four ATP are made but two are spent in the investment phase, so the net is 2 ATP, plus 2 NADH and 2 pyruvate."),
 q("Food energy", "easy", "Which food class has the highest energy content per gram?",
   ["carbohydrate", "protein", "alcohol", "fat"], "D",
   "Fat provides 38 kJ/g (9 kcal/g), versus 29 kJ/g for alcohol and 17 kJ/g for carbohydrate and protein."),
 q("Storage", "easy", "The storage form of glucose in animals is:",
   ["starch", "glycogen", "cellulose", "amylopectin"], "B",
   "Glycogen, stored mainly in liver and muscle; starch (amylose and amylopectin) is the plant storage form."),
 q("Anaerobic", "easy", "Without oxygen, pyruvate in muscle is converted to:",
   ["acetyl-CoA", "oxaloacetate", "lactate", "citrate"], "C",
   "Lactate dehydrogenase converts pyruvate to lactate, regenerating NAD+ for glycolysis."),
 # medium
 q("Energy conservation", "medium", "Roughly what share of energy from oxidising glucose is conserved as ATP and NADH?",
   ["about 10%", "about 25%", "about 50%", "about 90%"], "C",
   "Approximately 50% of the energy is conserved in ATP and reduced carriers; the remainder is released as heat."),
 q("GLUT4", "medium", "The insulin-dependent glucose transporter found in skeletal muscle and adipose is:",
   ["GLUT1", "GLUT2", "GLUT3", "GLUT4"], "D",
   "GLUT4 requires insulin to reach the membrane; other GLUTs move glucose down its gradient without insulin."),
 q("Hexokinase", "medium", "Phosphorylation of glucose to glucose-6-phosphate on entering the cell mainly serves to:",
   ["trap glucose and maintain the gradient", "make ATP by substrate-level phosphorylation directly", "split glucose into two triose sugars", "carry glucose into the mitochondrial matrix"], "A",
   "The phosphate traps glucose inside and keeps free glucose low, so glucose keeps flowing in from the blood."),
 q("Glycolysis phases", "medium", "Glucose-6-phosphate is rearranged, phosphorylated and cleaved to form two molecules of:",
   ["pyruvate", "glyceraldehyde-3-phosphate", "phosphoenolpyruvate", "fructose-6-phosphate"], "B",
   "Steps 1-5 (energy-consuming phase) end with two glyceraldehyde-3-phosphate; steps 6-10 convert these to pyruvate."),
 q("Glycolysis energy", "medium", "What proportion of the available energy in glucose is extracted by glycolysis?",
   ["about 5%", "about 30%", "about 50%", "about 80%"], "A",
   "Glycolysis nets 2 ATP out of roughly 30-38 ATP available from full oxidation, about 5%."),
 q("PDH", "medium", "Pyruvate dehydrogenase converts pyruvate to acetyl-CoA by:",
   ["reversible carboxylation", "oxidative decarboxylation", "substrate-level phosphorylation", "reductive condensation"], "B",
   "PDH removes CO2 and transfers electrons to NAD+ (forming NADH) in an irreversible oxidative decarboxylation."),
 q("PDH regulation", "medium", "Pyruvate dehydrogenase is inhibited by high concentrations of:",
   ["NAD+ and CoA", "acetyl-CoA and NADH", "pyruvate and ADP", "oxaloacetate and citrate"], "B",
   "PDH is product-inhibited by acetyl-CoA and NADH and activated by NAD+ and CoA."),
 q("TCA entry", "medium", "The TCA cycle begins when acetyl-CoA condenses with:",
   ["malate", "succinate", "oxaloacetate", "alpha-ketoglutarate"], "C",
   "Acetyl-CoA + oxaloacetate form citrate (citrate synthase); the cycle ends by regenerating oxaloacetate."),
 q("TCA yield", "medium", "Per acetyl-CoA entering the TCA cycle, the products include:",
   ["3 NADH, 1 FADH2, 1 GTP", "2 NADH, 2 FADH2, 1 GTP", "3 NADH, 2 FADH2, 2 ATP", "4 NADH, 1 FADH2, 1 GTP"], "A",
   "Each turn yields 3 NADH, 1 FADH2 and 1 GTP, plus 2 CO2."),
 q("TCA regulation", "medium", "Which pair increases TCA cycle activity?",
   ["citrate and NADH", "oxaloacetate and NAD+", "acetyl-CoA and ATP", "succinate and FADH2"], "B",
   "Oxaloacetate and NAD+ increase activity; citrate and NADH inhibit it."),
 q("ETC", "medium", "The electron carriers that shuttle electrons between ETC complexes are:",
   ["NADH and FADH2", "ubiquinone and cytochrome c", "ATP and ADP", "coenzyme A and NAD+"], "B",
   "Ubiquinone (Q) and cytochrome c carry electrons between complexes I-IV."),
 q("ETC", "medium", "The ETC complexes pump protons from the:",
   ["intermembrane space to the matrix", "matrix to the intermembrane space", "cytosol to the matrix", "matrix to the cytosol"], "B",
   "Complexes act as proton pumps from the matrix into the intermembrane space, creating the gradient that ATP synthase uses."),
 q("Glycogen", "medium", "Glycogen synthase adds glucose units to glycogen in the activated form of:",
   ["glucose-6-phosphate", "glucose-1-phosphate", "UDP-glucose", "fructose-6-phosphate"], "C",
   "Glucose-6-phosphate is isomerised and activated to the sugar nucleotide UDP-glucose before glycogen synthase adds it."),
 q("Liver glycogen", "medium", "Liver glycogen can maintain blood glucose between meals for approximately:",
   ["2-4 hours", "12-16 hours", "2-3 days", "1 week"], "B",
   "The liver breaks down glycogen to maintain blood glucose for approximately 12-16 hours."),
 # hard
 q("Muscle glycogen", "hard", "Muscle glycogen cannot be used to maintain blood glucose because muscle lacks:",
   ["glycogen phosphorylase", "glucose-6-phosphatase", "debranching enzyme", "hexokinase"], "B",
   "Without glucose-6-phosphatase, muscle cannot remove the phosphate to release free glucose; it uses G6P for its own glycolysis."),
 q("ADP control", "hard", "When mitochondrial ADP is depleted, the most direct effect is that:",
   ["ATP synthase stops and O2 uptake falls", "the ETC speeds up to rebuild the gradient", "the proton gradient collapses completely", "PDH activity rises to supply NADH"], "A",
   "ADP is the key regulator: without it ATP synthase halts, the gradient stays high, the ETC slows and oxygen uptake decreases."),
 q("ADP control", "hard", "Adding ADP to respiring mitochondria increases O2 consumption because ATP synthase:",
   ["lowers the proton gradient", "directly reduces molecular oxygen", "pumps protons back outward", "regenerates NADH from NAD+"], "A",
   "ATP synthesis consumes the H+ gradient, so the ETC must work harder (using more O2) to rebuild it."),
 q("ATP synthase", "hard", "ATP synthase is driven by protons moving:",
   ["from the matrix into the intermembrane space", "from the intermembrane space into the matrix", "from the cytosol into the intermembrane space", "from the matrix into the cytosol"], "B",
   "Protons flow down their electrochemical gradient back into the matrix, turning the F0 rotor and driving ADP phosphorylation in F1."),
 q("Transport", "hard", "ADP enters the mitochondrion in exchange for ATP via the:",
   ["HPO4/OH- antiporter", "ATP/ADP antiporter", "Na+/K+ ATPase", "ATP synthase F0 pore"], "B",
   "The ATP/ADP antiporter exports newly made ATP and imports cytosolic ADP; phosphate enters via the HPO4 2-/OH- antiporter."),
 q("Gluconeogenesis", "hard", "The energy needed to run hepatic gluconeogenesis during fasting is mainly supplied by:",
   ["anaerobic glycolysis in the liver", "oxidation of fatty acids", "breakdown of liver glycogen", "lactate oxidation in muscle"], "B",
   "Fatty acids released from triglycerides are oxidised to power gluconeogenesis; glycerol from the same triglycerides is a substrate."),
 q("Gluconeogenesis", "hard", "Which molecule CANNOT serve as a net substrate for gluconeogenesis?",
   ["lactate", "glycerol", "alanine", "acetyl-CoA"], "D",
   "The PDH step is irreversible, so acetyl-CoA cannot be converted back to pyruvate or glucose; lactate, glycerol and amino acids such as alanine can."),
 q("Gluconeogenesis", "hard", "Gluconeogenesis occurs mainly in the liver because the liver:",
   ["has enzymes that bypass irreversible glycolytic steps", "is the only organ containing any mitochondria", "stores more glycogen than skeletal muscle", "lacks all of the enzymes of glycolysis"], "A",
   "The liver has the specific enzymes (e.g. pyruvate carboxylase, PEPCK, fructose-1,6-bisphosphatase, glucose-6-phosphatase) to overcome irreversible steps."),
 q("Lactate", "hard", "The main purpose of converting pyruvate to lactate under anaerobic conditions is to:",
   ["produce additional ATP directly", "regenerate NAD+ for glycolysis", "export carbon to the liver for storage", "lower the cell's pH for enzyme activity"], "B",
   "The LDH reaction makes no ATP; it oxidises NADH back to NAD+, which glycolysis requires to continue."),
 q("Cori cycle", "hard", "In the Cori cycle, lactate from exercising muscle is:",
   ["oxidised to CO2 in muscle mitochondria", "converted to glucose by the liver", "stored as glycogen within the muscle", "excreted unchanged by the kidneys"], "B",
   "Lactate travels to the liver, is converted to pyruvate and then glucose by gluconeogenesis, and glucose returns to the tissues."),
]

def _rebalance(qs):
    import re as _re
    for i, x in enumerate(qs):
        bodies = [_re.sub(r"^[A-D]\. ", "", o) for o in x["options"]]
        ci = "ABCD".index(x["correct_answer"]); ti = (i * 3 + 1) % 4
        bodies[ci], bodies[ti] = bodies[ti], bodies[ci]
        x["options"] = [f"{'ABCD'[k]}. {b}" for k, b in enumerate(bodies)]
        x["correct_answer"] = "ABCD"[ti]
_rebalance(Q)

if __name__ == "__main__":
    bad = check_bank(Q)
    print(f"{KEY}: {summarize(Q)}")
    if bad:
        print("VIOLATIONS:")
        for i, vs in bad.items():
            print(f"  [{i}] {Q[i].get('question','')[:60]}")
            for v in vs:
                print(f"        - {v}")
        sys.exit(1)
    print("All questions clean ✅")
    bank_path = os.path.join(HERE, "..", "..", "guide_quizzes.json")
    bank = json.load(open(bank_path, encoding="utf-8"))
    bank[KEY] = dict(META, questions=Q)
    json.dump(bank, open(bank_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {KEY} into guide_quizzes.json ({len(bank)} galleries, {len(Q)} questions in this bank)")
