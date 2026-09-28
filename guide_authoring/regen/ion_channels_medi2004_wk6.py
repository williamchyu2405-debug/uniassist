#!/usr/bin/env python3
"""MEDI2004 W6 · Ion Channels & Channelopathies — REDO (exam-calibrated).

Round 2 regeneration: fresh applied/named-drug stems (lidocaine, phenytoin, TTX,
sulfonylureas/diazoxide, nifedipine/verapamil, ethosuximide, dantrolene,
suxamethonium, ivacaftor/CFTR, hERG/long-QT). Same syllabus as Round 1; new stems
→ the app re-seeds and wipes old progress. Correct option written first as A.;
backend shuffles positions on seed. META preserved via the _meta sidecar.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "ion_channels_medi2004_wk6.html"
META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "_meta", KEY + ".meta.json"), encoding="utf-8"))

Q = [
    # ── easy (5) ──
    {"topic": "Ion Channels", "difficulty": "easy",
     "question": "An ion channel moves ions across the membrane by providing a:",
     "options": ["A. water-filled pore", "B. lipid raft", "C. covalent carrier", "D. metabolic pump"],
     "correct_answer": "A",
     "explanation": "Channels are pore-forming proteins that let ions flow down their gradient through an aqueous path, rather than binding and carrying them.",
     "related": ["Ion Channels", "Channel Structure"]},

    {"topic": "Selectivity Filter", "difficulty": "easy",
     "question": "The part of a potassium channel that lets K⁺ through but excludes Na⁺ is the:",
     "options": ["A. selectivity filter", "B. voltage sensor", "C. inactivation gate", "D. lipid anchor"],
     "correct_answer": "A",
     "explanation": "The selectivity filter's precisely spaced carbonyl oxygens fit dehydrated K⁺, so it distinguishes K⁺ from the smaller Na⁺.",
     "related": ["Selectivity Filter", "Ion Selectivity"]},

    {"topic": "Local Anaesthetics", "difficulty": "easy",
     "question": "Lidocaine produces local anaesthesia by blocking which channel type?",
     "options": ["A. voltage-gated sodium", "B. voltage-gated potassium", "C. ligand-gated chloride", "D. store-operated calcium"],
     "correct_answer": "A",
     "explanation": "Lidocaine blocks voltage-gated Na⁺ channels, stopping action-potential firing in sensory nerves so pain signals cannot propagate.",
     "related": ["Local Anaesthetics", "Action Potential"]},

    {"topic": "Action Potential", "difficulty": "easy",
     "question": "The rapid upstroke (depolarisation) of a neuronal action potential is caused by influx of:",
     "options": ["A. sodium ions", "B. chloride ions", "C. potassium ions", "D. calcium ions"],
     "correct_answer": "A",
     "explanation": "Voltage-gated Na⁺ channels open first and Na⁺ rushes in, driving the sharp depolarising upstroke before K⁺ efflux repolarises the cell.",
     "related": ["Action Potential", "Conduction"]},

    {"topic": "Calcium Channel Blockers", "difficulty": "easy",
     "question": "Amlodipine lowers blood pressure by blocking which channel in vascular smooth muscle?",
     "options": ["A. L-type calcium", "B. delayed-rectifier potassium", "C. epithelial sodium", "D. chloride"],
     "correct_answer": "A",
     "explanation": "Dihydropyridines like amlodipine block L-type Ca²⁺ channels, reducing Ca²⁺ entry and relaxing arterial smooth muscle.",
     "related": ["Calcium Channel Blockers", "Channel Drugs"]},

    # ── medium (14) ──
    {"topic": "Ion Selectivity", "difficulty": "medium",
     "question": "A potassium channel selects K⁺ over the smaller Na⁺ because the filter's carbonyl oxygens best replace the water shell of:",
     "options": ["A. potassium", "B. sodium", "C. calcium", "D. chloride"],
     "correct_answer": "A",
     "explanation": "The filter is sized so its oxygens substitute for K⁺'s hydration shell; Na⁺ is too small to fit them snugly, so it is excluded — the paradox of size.",
     "related": ["Ion Selectivity", "Selectivity Filter"]},

    {"topic": "Channel Toxins", "difficulty": "medium",
     "question": "Tetrodotoxin from pufferfish causes paralysis because it plugs the pore of the:",
     "options": ["A. voltage-gated sodium channel", "B. voltage-gated potassium channel", "C. nicotinic acetylcholine receptor", "D. ryanodine receptor"],
     "correct_answer": "A",
     "explanation": "TTX blocks voltage-gated Na⁺ channels, preventing action potentials in nerve and muscle, which stops signalling and causes paralysis.",
     "related": ["Channel Toxins", "Action Potential"]},

    {"topic": "Driving Forces", "difficulty": "medium",
     "question": "Whether an ion enters or leaves a cell through an open channel is set by its electrochemical gradient, which combines the concentration gradient with the:",
     "options": ["A. membrane voltage", "B. channel colour", "C. lipid thickness", "D. cell volume"],
     "correct_answer": "A",
     "explanation": "The net driving force is the concentration gradient plus the electrical gradient (membrane potential); together they decide the direction of flow.",
     "related": ["Driving Forces", "Nernst Potential"]},

    {"topic": "Nernst Potential", "difficulty": "medium",
     "question": "The Nernst equation gives, for a single ion, the membrane voltage at which:",
     "options": ["A. net flow is zero", "B. the channel opens", "C. the pump stops", "D. the cell divides"],
     "correct_answer": "A",
     "explanation": "The Nernst (equilibrium) potential is the voltage where the electrical force exactly balances the concentration gradient, so there is no net movement of that ion.",
     "related": ["Nernst Potential", "Driving Forces"]},

    {"topic": "Sodium-Potassium Pump", "difficulty": "medium",
     "question": "The Na⁺/K⁺-ATPase maintains the gradients that channels use by pumping, per cycle:",
     "options": ["A. 3 Na⁺ out, 2 K⁺ in", "B. 2 Na⁺ out, 3 K⁺ in", "C. 3 K⁺ out, 2 Na⁺ in", "D. 1 Na⁺ out, 1 K⁺ in"],
     "correct_answer": "A",
     "explanation": "Each cycle exports 3 Na⁺ and imports 2 K⁺ using ATP, sustaining the low-internal-Na⁺, high-internal-K⁺ gradients channels depend on.",
     "related": ["Sodium-Potassium Pump", "Transport"]},

    {"topic": "Nav Inactivation", "difficulty": "medium",
     "question": "After opening during an action potential, the voltage-gated Na⁺ channel briefly enters a state where it cannot reopen. This state is:",
     "options": ["A. inactivated", "B. resting", "C. activated", "D. leaky"],
     "correct_answer": "A",
     "explanation": "The channel passes from open to an inactivated state; it must return to resting before it can open again, which sets the refractory period.",
     "related": ["Nav Inactivation", "Gating States"]},

    {"topic": "nAChR", "difficulty": "medium",
     "question": "At the neuromuscular junction, acetylcholine opens the nicotinic receptor, a channel that admits mainly:",
     "options": ["A. sodium", "B. chloride", "C. calcium only", "D. bicarbonate"],
     "correct_answer": "A",
     "explanation": "The nicotinic ACh receptor is a cation channel; Na⁺ influx depolarises the muscle end-plate to trigger contraction.",
     "related": ["nAChR", "Neuromuscular Blockers"]},

    {"topic": "Neuromuscular Blockers", "difficulty": "medium",
     "question": "Suxamethonium first causes muscle twitching (fasciculations) before paralysis because it initially:",
     "options": ["A. activates the nicotinic receptor", "B. blocks the sodium pump", "C. closes calcium channels", "D. inhibits acetylcholinesterase"],
     "correct_answer": "A",
     "explanation": "Suxamethonium is a depolarising blocker: it first activates nicotinic receptors (fasciculations), then keeps the end-plate depolarised so it can no longer respond.",
     "related": ["Neuromuscular Blockers", "nAChR"]},

    {"topic": "K-ATP Channel", "difficulty": "medium",
     "question": "In a pancreatic beta cell, a rise in glucose closes the K-ATP channel. Closing it makes the cell:",
     "options": ["A. depolarise", "B. hyperpolarise", "C. shrink", "D. divide"],
     "correct_answer": "A",
     "explanation": "Closing the K-ATP channel stops K⁺ leaving, so the cell depolarises, opening Ca²⁺ channels and triggering insulin release.",
     "related": ["K-ATP Channel", "Insulin Secretion"]},

    {"topic": "Insulin Secretion", "difficulty": "medium",
     "question": "Sulfonylureas such as gliclazide stimulate insulin release by directly:",
     "options": ["A. closing the K-ATP channel", "B. opening the K-ATP channel", "C. blocking calcium channels", "D. inhibiting the sodium pump"],
     "correct_answer": "A",
     "explanation": "Sulfonylureas bind and close the beta-cell K-ATP channel, mimicking glucose's effect to depolarise the cell and drive insulin secretion.",
     "related": ["Insulin Secretion", "K-ATP Channel"]},

    {"topic": "Cystic Fibrosis", "difficulty": "medium",
     "question": "Cystic fibrosis results from a faulty channel that normally transports:",
     "options": ["A. chloride ions", "B. sodium ions", "C. potassium ions", "D. calcium ions"],
     "correct_answer": "A",
     "explanation": "CFTR is a chloride channel; loss of function leaves secretions thick and salty, damaging lung and pancreas — the hallmark of cystic fibrosis.",
     "related": ["Cystic Fibrosis", "Channelopathies"]},

    {"topic": "Absence Epilepsy", "difficulty": "medium",
     "question": "Ethosuximide controls childhood absence seizures by blocking which channel in thalamic neurons?",
     "options": ["A. T-type calcium", "B. L-type calcium", "C. delayed-rectifier potassium", "D. epithelial sodium"],
     "correct_answer": "A",
     "explanation": "T-type Ca²⁺ channels drive the thalamic rhythms behind absence seizures; ethosuximide blocks them, which is why it is first-line for that seizure type.",
     "related": ["Absence Epilepsy", "T-Type Channels"]},

    {"topic": "Channel Structure", "difficulty": "medium",
     "question": "Voltage-gated channels sense changes in membrane potential through a domain rich in positively charged residues called the:",
     "options": ["A. voltage sensor", "B. selectivity filter", "C. pore loop", "D. lipid anchor"],
     "correct_answer": "A",
     "explanation": "A charged transmembrane segment (the voltage sensor, S4) moves with voltage changes and pulls the gate open — how these channels read membrane potential.",
     "related": ["Channel Structure", "Gating States"]},

    # ── hard (15) ──
    {"topic": "State-Dependent Block", "difficulty": "hard",
     "question": "Lidocaine blocks firing (damaged) nerves more than resting ones because it binds best to the channel's:",
     "options": ["A. open and inactivated states", "B. the resting closed state", "C. fully degraded subunits", "D. the lipid surround"],
     "correct_answer": "A",
     "explanation": "Lidocaine shows use-dependence: it preferentially binds open/inactivated Na⁺ channels, so rapidly firing or damaged fibres are blocked more strongly.",
     "related": ["State-Dependent Block", "Local Anaesthetics"]},

    {"topic": "Channel Pharmacology", "difficulty": "hard",
     "question": "Phenytoin dampens seizures by binding inactivated Na⁺ channels and slowing their recovery. High-frequency neurons are hit hardest because they:",
     "options": ["A. spend longer inactivated", "B. have fewer channels", "C. lack a voltage sensor", "D. pump less sodium"],
     "correct_answer": "A",
     "explanation": "Rapidly firing neurons keep channels inactivated more of the time, so a drug favouring that state selectively suppresses the abnormal high-frequency firing.",
     "related": ["Channel Pharmacology", "State-Dependent Block"]},

    {"topic": "Drug-Induced LQT", "difficulty": "hard",
     "question": "Several drugs lengthen the QT interval and risk arrhythmia by blocking a cardiac potassium channel encoded by:",
     "options": ["A. hERG", "B. CFTR", "C. SCN5A", "D. GLUT4"],
     "correct_answer": "A",
     "explanation": "The hERG K⁺ channel repolarises the cardiac action potential; blocking it prolongs the QT interval, a common mechanism of drug-induced long-QT.",
     "related": ["Drug-Induced LQT", "Channelopathies"]},

    {"topic": "Channelopathies", "difficulty": "hard",
     "question": "A congenital long-QT syndrome caused by a loss-of-function potassium-channel mutation prolongs the action potential because repolarisation is:",
     "options": ["A. slowed", "B. accelerated", "C. reversed", "D. unchanged"],
     "correct_answer": "A",
     "explanation": "Less K⁺ efflux slows repolarisation, lengthening the action potential and QT interval and predisposing to dangerous arrhythmias.",
     "related": ["Channelopathies", "Drug-Induced LQT"]},

    {"topic": "Malignant Hyperthermia", "difficulty": "hard",
     "question": "In malignant hyperthermia, volatile anaesthetics trigger uncontrolled Ca²⁺ release from the sarcoplasmic reticulum. Dantrolene helps by blocking the:",
     "options": ["A. ryanodine receptor", "B. L-type calcium channel", "C. sodium pump", "D. nicotinic receptor"],
     "correct_answer": "A",
     "explanation": "Dantrolene inhibits the ryanodine receptor Ca²⁺-release channel, cutting the flood of calcium that drives the rigidity and heat of malignant hyperthermia.",
     "related": ["Malignant Hyperthermia", "Channelopathies"]},

    {"topic": "Cystic Fibrosis", "difficulty": "hard",
     "question": "Ivacaftor benefits certain cystic fibrosis patients because it acts as a CFTR:",
     "options": ["A. potentiator", "B. blocker", "C. degrader", "D. antagonist"],
     "correct_answer": "A",
     "explanation": "Ivacaftor is a potentiator that increases the open probability of CFTR channels reaching the surface, restoring some chloride transport.",
     "related": ["Cystic Fibrosis", "Channel Drugs"]},

    {"topic": "K-ATP Channel", "difficulty": "hard",
     "question": "Diazoxide opens the K-ATP channel in beta cells. The expected effect on insulin secretion is that it:",
     "options": ["A. falls", "B. rises", "C. is unchanged", "D. doubles"],
     "correct_answer": "A",
     "explanation": "Opening K-ATP hyperpolarises the beta cell, closing Ca²⁺ channels, so insulin release falls — the opposite of a sulfonylurea.",
     "related": ["K-ATP Channel", "Insulin Secretion"]},

    {"topic": "Calcium Channel Blockers", "difficulty": "hard",
     "question": "Verapamil slows the heart more than nifedipine because it blocks L-type Ca²⁺ channels preferentially in:",
     "options": ["A. cardiac tissue", "B. skeletal muscle", "C. red blood cells", "D. nerve axons"],
     "correct_answer": "A",
     "explanation": "Verapamil (a non-dihydropyridine) acts strongly on cardiac Ca²⁺ channels, slowing rate and conduction, whereas nifedipine acts mainly on vessels.",
     "related": ["Calcium Channel Blockers", "Channel Drugs"]},

    {"topic": "Nav Inactivation", "difficulty": "hard",
     "question": "The absolute refractory period exists because voltage-gated Na⁺ channels must first leave which state before firing again?",
     "options": ["A. inactivated", "B. open", "C. depolarised", "D. phosphorylated"],
     "correct_answer": "A",
     "explanation": "During the absolute refractory period enough channels are inactivated that no stimulus can fire a new action potential until they reset to resting.",
     "related": ["Nav Inactivation", "Action Potential"]},

    {"topic": "Conduction", "difficulty": "hard",
     "question": "Saltatory conduction speeds nerve signals because voltage-gated Na⁺ channels are concentrated at the:",
     "options": ["A. nodes of Ranvier", "B. myelin sheath", "C. synaptic cleft", "D. cell nucleus"],
     "correct_answer": "A",
     "explanation": "Na⁺ channels cluster at the nodes of Ranvier, so the impulse jumps node to node between insulating myelin, greatly speeding conduction.",
     "related": ["Conduction", "Action Potential"]},

    {"topic": "Gating States", "difficulty": "hard",
     "question": "A drug that binds only when a channel is open shows use-dependence, meaning its block increases when the channel is:",
     "options": ["A. frequently opening", "B. rarely opening", "C. fully degraded", "D. newly synthesised"],
     "correct_answer": "A",
     "explanation": "Use- or state-dependent block builds up with channel activity, so more frequent opening exposes more binding opportunities and deepens the block.",
     "related": ["Gating States", "State-Dependent Block"]},

    {"topic": "T-Type Channels", "difficulty": "hard",
     "question": "T-type calcium channels differ from L-type in that they activate at more negative voltages and are described as:",
     "options": ["A. low-voltage-activated", "B. high-voltage-activated", "C. ligand-gated", "D. mechanically gated"],
     "correct_answer": "A",
     "explanation": "T-type channels are low-voltage-activated and transient, suiting them to pacemaking and thalamic rhythms, unlike the high-voltage-activated L-type.",
     "related": ["T-Type Channels", "Absence Epilepsy"]},

    {"topic": "Channel Toxins", "difficulty": "hard",
     "question": "Compared with a local anaesthetic, tetrodotoxin blocks the sodium channel with far greater:",
     "options": ["A. potency and selectivity", "B. reversibility and speed", "C. lipid solubility only", "D. use-dependence only"],
     "correct_answer": "A",
     "explanation": "TTX binds the outer pore with extreme potency and Na-channel selectivity, unlike lidocaine, which is a weaker, use-dependent blocker acting from inside.",
     "related": ["Channel Toxins", "Local Anaesthetics"]},

    {"topic": "Channel States", "difficulty": "hard",
     "question": "At the normal resting membrane potential, most voltage-gated Na⁺ channels sit in which state?",
     "options": ["A. resting closed", "B. open conducting", "C. inactivated", "D. degraded"],
     "correct_answer": "A",
     "explanation": "At rest the channels are closed but available (resting state), poised to open on depolarisation — distinct from the non-conducting inactivated state.",
     "related": ["Channel States", "Gating States"]},

    {"topic": "Channel Drugs", "difficulty": "hard",
     "question": "Local anaesthetics are weak bases that cross the membrane uncharged, then block the channel from inside once they become:",
     "options": ["A. charged", "B. oxidised", "C. glucuronidated", "D. dimerised"],
     "correct_answer": "A",
     "explanation": "The neutral form crosses the membrane, then re-protonates to the charged form that binds the Na⁺ channel's inner pore — why inflamed acidic tissue resists block.",
     "related": ["Channel Drugs", "Local Anaesthetics"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
