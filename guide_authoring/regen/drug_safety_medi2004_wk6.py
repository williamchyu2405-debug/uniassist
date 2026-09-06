#!/usr/bin/env python3
"""MEDI2004 W6 · Drug Safety (adverse effects, interactions, poisoning) — regenerated bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "drug_safety_medi2004_wk6.html"
META = {"title": "MEDI2004 W6 · Drug Safety",
        "subject": "Pharmacology Fundamentals", "unit": "MEDI2004",
        "content": ("Drug harm = 2nd commonest hospital adverse event; ~2-3% admissions medicine-related, "
                    "~1.4% ADRs; >half preventable. Therapeutic index TI = TD50/ED50 (higher = safer, at 50% "
                    "response); TI 60/10 = 6; digoxin ~2. Narrow-TI (DIAL: Digoxin, Iron, Aminoglycosides, "
                    "Lithium; + warfarin, phenytoin, theophylline) need monitoring. Therapeutic window = "
                    "individual plasma range (TDM) vs TI = population dose ratio. ADR = harmful unintended "
                    "response at normal doses. Type A (augmented): dose-related, common, pharmacological, "
                    "reversible by dose reduction. Type B (bizarre): idiosyncratic/immune, off-target, not "
                    "dose-related, severe. Rawlins-Thomson: C chronic (HPA suppression by glucocorticoids, "
                    "taper), D delayed (thalidomide teratogenesis), E end-of-use (beta-blocker rebound, "
                    "opiate withdrawal), F failure (OCP + enzyme inducers). Predisposition: age extremes, "
                    "sex, disease, hepatic/renal function, body composition, genetics; polypharmacy (pairs "
                    "scale combinatorially); smoking (CYP1A2), alcohol (CYP2E1). DDI mechanisms: behavioural, "
                    "pharmaceutic, pharmacokinetic, pharmacodynamic. PD synergism (alcohol + benzodiazepine "
                    "-> additive GABA-A CNS depression -> respiratory arrest) vs antagonism (non-selective "
                    "beta-blocker vs beta2-agonist). PK: absorption, distribution (warfarin albumin "
                    "displacement, self-limiting), metabolism (CYP), excretion (probenecid blocks OAT -> "
                    "penicillin high). CYP inducers (rifampicin, carbamazepine, St John's wort, phenytoin, "
                    "barbiturates, efavirenz) lower substrate -> failure; inhibitors (grapefruit CYP3A4, "
                    "fluconazole, clarithromycin) raise substrate -> toxicity. Poisoning (Paracelsus): "
                    "Assess (what/how much/how long; GCS, RR, BP, temp), prevent absorption (activated "
                    "charcoal <1h; gastric lavage rare), increase elimination (repeated-dose charcoal for "
                    "theophylline/digoxin/carbamazepine; alkaline diuresis for salicylates/phenobarbital; "
                    "haemodialysis for salicylates/lithium/methanol/ethylene glycol; charcoal haemoperfusion "
                    "for theophylline/barbiturates), antidotes. Antidotes: paracetamol->N-acetylcysteine "
                    "(glutathione, <8-10h; NAPQI via CYP2E1, chronic alcohol induces it); opioids->naloxone "
                    "(competitive antagonist, short half-life -> relapse); iron->desferrioxamine (chelator); "
                    "methanol/ethylene glycol->fomepizole/ethanol (inhibit ADH); organophosphates->atropine + "
                    "pralidoxime; CO->100% O2/hyperbaric; lead/mercury->chelators. Ion-trapping: alkaline "
                    "urine ionises weak acids (salicylate pKa~3) -> trapped -> excreted.")}

Q = [
    {"topic": "Therapeutic Index", "difficulty": "medium",
     "question": "The therapeutic index (TI) of a drug is calculated as:",
     "options": ["A. TD50 divided by ED50", "B. ED50 divided by TD50",
                 "C. TD50 multiplied by ED50", "D. TD50 minus the ED50"],
     "correct_answer": "A",
     "explanation": "TI = TD50 / ED50, the ratio of the dose toxic in half the population to the dose effective in half — a higher ratio means a safer drug.",
     "related": ["Therapeutic Index", "Drug Safety"]},

    {"topic": "Therapeutic Index", "difficulty": "hard",
     "question": "If ED50 is 10 mg and TD50 is 60 mg, the therapeutic index is:",
     "options": ["A. 6", "B. 600", "C. 0.17", "D. 50"],
     "correct_answer": "A",
     "explanation": "TI = TD50 ÷ ED50 = 60 ÷ 10 = 6, meaning the toxic dose is six times the effective dose — a moderate safety margin.",
     "related": ["Therapeutic Index", "Dosing"]},

    {"topic": "Therapeutic Index", "difficulty": "easy",
     "question": "A drug with a higher therapeutic index is:",
     "options": ["A. safer, with a wider margin",
                 "B. more dangerous to dose",
                 "C. always more potent overall",
                 "D. always more expensive to make"],
     "correct_answer": "A",
     "explanation": "A higher TI means a bigger gap between effective and toxic doses, so dosing is more forgiving. Digoxin's TI of about 2 is dangerously narrow.",
     "related": ["Therapeutic Index", "Drug Safety"]},

    {"topic": "Narrow TI Drugs", "difficulty": "medium",
     "question": "Which drug is a classic narrow-therapeutic-index agent requiring level monitoring?",
     "options": ["A. Lithium", "B. Amoxicillin", "C. Paracetamol", "D. Ibuprofen"],
     "correct_answer": "A",
     "explanation": "Lithium (with digoxin, aminoglycosides, warfarin, phenytoin) has a narrow TI needing routine monitoring. Amoxicillin has a wide margin and needs none.",
     "related": ["Narrow TI Drugs", "Therapeutic Drug Monitoring"]},

    {"topic": "Therapeutic Window", "difficulty": "hard",
     "question": "How does the therapeutic window differ from the therapeutic index?",
     "options": ["A. it is an individual plasma concentration range",
                 "B. it is a population dose ratio from trials",
                 "C. it ignores toxicity entirely in practice",
                 "D. it applies only to intravenous drugs"],
     "correct_answer": "A",
     "explanation": "The therapeutic window is the individual plasma-concentration range used to guide dosing (TDM); the TI is a population dose ratio measured in trials.",
     "related": ["Therapeutic Window", "Therapeutic Index"]},

    {"topic": "Adverse Drug Reactions", "difficulty": "easy",
     "question": "An adverse drug reaction is a harmful, unintended response occurring at:",
     "options": ["A. doses normally used in humans",
                 "B. doses far above normal use",
                 "C. doses only used in overdose",
                 "D. doses below the effective range"],
     "correct_answer": "A",
     "explanation": "An ADR is a harmful, unintended response to a drug at normal therapeutic doses — distinguishing it from deliberate overdose or poisoning.",
     "related": ["Adverse Drug Reactions", "Drug Safety"]},

    {"topic": "Type A ADR", "difficulty": "medium",
     "question": "A Type A (augmented) adverse drug reaction is:",
     "options": ["A. dose-related and largely predictable",
                 "B. unrelated to dose and bizarre",
                 "C. always immune-mediated and rare",
                 "D. only seen after the drug stops"],
     "correct_answer": "A",
     "explanation": "Type A reactions are an exaggeration of the drug's known action — dose-related, common and usually reversible by lowering the dose (e.g. warfarin bleeding).",
     "related": ["Type A ADR", "Adverse Drug Reactions"]},

    {"topic": "Type B ADR", "difficulty": "hard",
     "question": "Penicillin anaphylaxis is a Type B reaction, meaning it is:",
     "options": ["A. idiosyncratic and not dose-related",
                 "B. predictable and clearly dose-related",
                 "C. the drug's main action exaggerated",
                 "D. reversible by lowering the dose"],
     "correct_answer": "A",
     "explanation": "Type B (bizarre) reactions are off-target or immunological and not dose-related — they can occur at tiny doses and often require stopping the drug entirely.",
     "related": ["Type B ADR", "Hypersensitivity"]},

    {"topic": "Type A ADR", "difficulty": "hard",
     "question": "Type A reactions track dose closely because they arise from:",
     "options": ["A. the drug's own pharmacological action",
                 "B. a rare inherited enzyme mutation",
                 "C. an immune reaction to the drug",
                 "D. contamination of the preparation"],
     "correct_answer": "A",
     "explanation": "A Type A reaction is the drug doing too much of what it was designed to do, so it follows the same dose–response curve as the therapeutic effect.",
     "related": ["Type A ADR", "Dose-Response"]},

    {"topic": "ADR Classification", "difficulty": "medium",
     "question": "HPA-axis suppression from long-term glucocorticoids is which Rawlins & Thomson type?",
     "options": ["A. Type C, chronic use", "B. Type A, augmented",
                 "C. Type B, bizarre one", "D. Type F, failure"],
     "correct_answer": "A",
     "explanation": "Type C reactions need both cumulative dose and prolonged exposure; long-term steroids suppress the HPA axis, so they must be tapered, not stopped abruptly.",
     "related": ["ADR Classification", "Glucocorticoids"]},

    {"topic": "ADR Classification", "difficulty": "hard",
     "question": "Thalidomide causing limb defects (phocomelia) is which type of ADR?",
     "options": ["A. Type D, delayed", "B. Type A, augmented",
                 "C. Type E, end-of-use", "D. Type C, chronic"],
     "correct_answer": "A",
     "explanation": "Type D reactions appear long after exposure and aren't simply dose-related; teratogenesis such as thalidomide phocomelia is the classic example.",
     "related": ["ADR Classification", "Teratogenesis"]},

    {"topic": "ADR Classification", "difficulty": "medium",
     "question": "Rebound myocardial ischaemia when a beta-blocker is stopped abruptly is which type?",
     "options": ["A. Type E, end-of-use", "B. Type B, bizarre",
                 "C. Type F, failure", "D. Type D, delayed"],
     "correct_answer": "A",
     "explanation": "Type E reactions occur on withdrawal after physiological dependence; abrupt beta-blocker cessation causes rebound ischaemia from receptor up-regulation.",
     "related": ["ADR Classification", "Withdrawal"]},

    {"topic": "ADR Classification", "difficulty": "hard",
     "question": "Oral contraceptive failure caused by rifampicin is classified as which ADR type?",
     "options": ["A. Type F, failure of therapy",
                 "B. Type A, an augmented effect",
                 "C. Type B, a bizarre reaction",
                 "D. Type C, a chronic effect"],
     "correct_answer": "A",
     "explanation": "Type F is an unexpected failure of therapy; rifampicin induces CYP3A4, accelerating hormone metabolism so the pill drops below the contraceptive threshold.",
     "related": ["ADR Classification", "Enzyme Induction"]},

    {"topic": "ADR Risk", "difficulty": "medium",
     "question": "Why are low-therapeutic-index drugs especially prone to Type A ADRs?",
     "options": ["A. small dose changes reach toxic levels",
                 "B. they are always highly immunologically reactive",
                 "C. they never require any monitoring",
                 "D. they have no pharmacological action"],
     "correct_answer": "A",
     "explanation": "With a narrow margin, any factor that raises the level — dehydration, interacting drugs, organ impairment — can tip a stable patient into dose-related toxicity.",
     "related": ["ADR Risk", "Narrow TI Drugs"]},

    {"topic": "ADR Risk", "difficulty": "medium",
     "question": "Elderly patients are more prone to ADRs partly because they have:",
     "options": ["A. reduced renal and hepatic clearance",
                 "B. faster overall drug metabolism",
                 "C. higher plasma albumin levels",
                 "D. larger physiological reserve capacity"],
     "correct_answer": "A",
     "explanation": "Declining GFR, reduced liver mass/blood flow and lower albumin all raise effective drug levels, and polypharmacy adds further interaction risk in the elderly.",
     "related": ["ADR Risk", "Elderly"]},

    {"topic": "Polypharmacy", "difficulty": "hard",
     "question": "Why does polypharmacy raise interaction risk disproportionately?",
     "options": ["A. interaction pairs grow combinatorially",
                 "B. each new drug is always toxic",
                 "C. the drugs cancel each other out",
                 "D. metabolism stops with many drugs"],
     "correct_answer": "A",
     "explanation": "Potential interaction pairs scale combinatorially — 5 drugs give 10 pairs, 10 drugs give 45 — so each added drug multiplies the chances of a collision.",
     "related": ["Polypharmacy", "Drug Interactions"]},

    {"topic": "Paracetamol Toxicity", "difficulty": "hard",
     "question": "Chronic alcohol use raises the risk of paracetamol hepatotoxicity because it:",
     "options": ["A. induces CYP2E1, making more NAPQI",
                 "B. inhibits CYP2E1, making less NAPQI",
                 "C. depletes the plasma albumin stores",
                 "D. blocks paracetamol absorption fully"],
     "correct_answer": "A",
     "explanation": "Chronic alcohol induces CYP2E1, so more paracetamol is converted to the toxic NAPQI — liver injury can occur even at moderate paracetamol doses.",
     "related": ["Paracetamol Toxicity", "Enzyme Induction"]},

    {"topic": "Drug Interactions", "difficulty": "medium",
     "question": "A pharmacokinetic drug interaction changes a drug's:",
     "options": ["A. plasma concentration at its target",
                 "B. effect at the receptor directly",
                 "C. chemical structure in the bottle",
                 "D. cost and route of administration"],
     "correct_answer": "A",
     "explanation": "Pharmacokinetic interactions alter absorption, distribution, metabolism or excretion — changing how much drug reaches the target, not the receptor effect itself.",
     "related": ["Drug Interactions", "Pharmacokinetics"]},

    {"topic": "Pharmacodynamic Interactions", "difficulty": "hard",
     "question": "Combining alcohol with a benzodiazepine is dangerous because they:",
     "options": ["A. additively depress the central nervous system",
                 "B. compete for the same receptor site",
                 "C. cancel each other's sedative effect",
                 "D. block each other's metabolism fully"],
     "correct_answer": "A",
     "explanation": "Both enhance GABA-A chloride influx through different sites, so their CNS depression adds up — enough to suppress the brainstem respiratory drive.",
     "related": ["Pharmacodynamic Interactions", "GABA-A Receptor"]},

    {"topic": "Pharmacodynamic Interactions", "difficulty": "medium",
     "question": "A non-selective beta-blocker can worsen asthma because it:",
     "options": ["A. blocks bronchial β2 receptors",
                 "B. activates bronchial β2 receptors",
                 "C. blocks cardiac β1 receptors only",
                 "D. inhibits salbutamol's metabolism"],
     "correct_answer": "A",
     "explanation": "By blocking β2 receptors in bronchial smooth muscle it opposes β2-agonist bronchodilation — a pharmacodynamic antagonism that can precipitate bronchospasm.",
     "related": ["Pharmacodynamic Interactions", "Beta-Blockers"]},

    {"topic": "CYP450 Interactions", "difficulty": "hard",
     "question": "Adding a CYP450 inducer such as rifampicin to a substrate drug will:",
     "options": ["A. lower the substrate's plasma level",
                 "B. raise the substrate's plasma level",
                 "C. leave the substrate level unchanged",
                 "D. abolish the substrate's metabolism"],
     "correct_answer": "A",
     "explanation": "An inducer upregulates enzyme over days to weeks, speeding substrate breakdown and lowering its level — risking therapeutic failure (e.g. warfarin, the pill).",
     "related": ["CYP450 Interactions", "Enzyme Induction"]},

    {"topic": "CYP450 Interactions", "difficulty": "hard",
     "question": "Adding a CYP inhibitor such as fluconazole to warfarin tends to cause:",
     "options": ["A. higher warfarin levels and bleeding",
                 "B. lower warfarin levels and clotting",
                 "C. no change in warfarin's effect",
                 "D. faster warfarin excretion by kidney"],
     "correct_answer": "A",
     "explanation": "An inhibitor blocks the enzyme, slowing warfarin metabolism so its level rises — increasing the risk of haemorrhage. Inhibitors cause overdosing.",
     "related": ["CYP450 Interactions", "Enzyme Inhibition"]},

    {"topic": "Enzyme Inhibition", "difficulty": "medium",
     "question": "Grapefruit juice raises levels of drugs like atorvastatin by inhibiting:",
     "options": ["A. intestinal CYP3A4", "B. renal OAT transporters",
                 "C. plasma albumin binding", "D. gastric acid secretion"],
     "correct_answer": "A",
     "explanation": "Grapefruit furanocoumarins inhibit intestinal CYP3A4, reducing first-pass metabolism of 3A4 substrates so more drug reaches the circulation.",
     "related": ["Enzyme Inhibition", "CYP3A4"]},

    {"topic": "Excretion Interactions", "difficulty": "medium",
     "question": "Probenecid prolongs penicillin action by blocking its:",
     "options": ["A. renal tubular secretion", "B. hepatic metabolism",
                 "C. plasma protein binding", "D. intestinal absorption"],
     "correct_answer": "A",
     "explanation": "Probenecid blocks the organic anion transporter that secretes penicillin into the tubule, reducing its renal clearance and keeping levels high longer.",
     "related": ["Excretion Interactions", "Transporters"]},

    {"topic": "Poisoning", "difficulty": "easy",
     "question": "The structured approach to a poisoned patient begins with:",
     "options": ["A. assessing patient and drug",
                 "B. giving a specific antidote",
                 "C. starting immediate haemodialysis",
                 "D. inducing vomiting at once"],
     "correct_answer": "A",
     "explanation": "First assess: what drug, how much, how long ago, and the vital parameters. Antidotes and elimination measures follow once the situation is understood.",
     "related": ["Poisoning", "Toxicology"]},

    {"topic": "Poisoning", "difficulty": "medium",
     "question": "Activated charcoal is most effective when given:",
     "options": ["A. within about one hour of ingestion",
                 "B. more than six hours after ingestion",
                 "C. only after the drug is absorbed",
                 "D. once dialysis has already begun"],
     "correct_answer": "A",
     "explanation": "Charcoal adsorbs drug still in the gut, so it works best within about an hour; once absorption is complete it is largely futile for immediate-release drugs.",
     "related": ["Poisoning", "Decontamination"]},

    {"topic": "Antidotes", "difficulty": "hard",
     "question": "N-acetylcysteine treats paracetamol overdose by:",
     "options": ["A. replenishing hepatic glutathione stores",
                 "B. blocking CYP conversion to NAPQI",
                 "C. chelating the paracetamol directly",
                 "D. speeding renal excretion of NAPQI"],
     "correct_answer": "A",
     "explanation": "NAC is a glutathione precursor; restoring glutathione lets the liver detoxify NAPQI. It must be given early, before hepatocyte damage is established.",
     "related": ["Antidotes", "Paracetamol Toxicity"]},

    {"topic": "Antidotes", "difficulty": "medium",
     "question": "Naloxone reverses opioid overdose by acting as a:",
     "options": ["A. competitive opioid receptor antagonist",
                 "B. partial opioid receptor agonist",
                 "C. glutathione-replenishing precursor",
                 "D. heavy-metal chelating agent"],
     "correct_answer": "A",
     "explanation": "Naloxone competitively displaces opioids from μ receptors, rapidly reversing respiratory depression. Its short half-life means recurrence is common.",
     "related": ["Antidotes", "Opioids"]},

    {"topic": "Antidotes", "difficulty": "hard",
     "question": "A patient revived with naloxone after heroin overdose relapses 30 minutes later because naloxone:",
     "options": ["A. has a shorter half-life than the opioid",
                 "B. has a longer half-life than the opioid",
                 "C. permanently blocks the opioid receptors",
                 "D. converts heroin back into morphine"],
     "correct_answer": "A",
     "explanation": "Naloxone lasts only ~60–90 min, shorter than most opioids, so as it wears off receptor activity and respiratory depression return — monitoring is needed.",
     "related": ["Antidotes", "Opioids"]},

    {"topic": "Antidotes", "difficulty": "hard",
     "question": "Fomepizole treats methanol and ethylene glycol poisoning by inhibiting:",
     "options": ["A. alcohol dehydrogenase", "B. acetylcholinesterase",
                 "C. cytochrome P450 3A4", "D. the organic anion transporter"],
     "correct_answer": "A",
     "explanation": "Both poisons become toxic only after alcohol dehydrogenase converts them (to formic acid and oxalate); blocking that enzyme prevents the toxic metabolites forming.",
     "related": ["Antidotes", "Alcohol Dehydrogenase"]},

    {"topic": "Ion Trapping", "difficulty": "hard",
     "question": "Alkalinising the urine speeds elimination of aspirin (a weak acid) because it:",
     "options": ["A. ionises and traps it there",
                 "B. keeps it uncharged in the tubule",
                 "C. increases its tubular reabsorption",
                 "D. blocks its glomerular filtration"],
     "correct_answer": "A",
     "explanation": "In alkaline urine the weak acid is almost fully ionised; the charged form can't diffuse back across tubular cells, so it is trapped and excreted.",
     "related": ["Ion Trapping", "Salicylate Poisoning"]},

    {"topic": "Antidotes", "difficulty": "easy",
     "question": "Organophosphate poisoning is treated with atropine plus:",
     "options": ["A. pralidoxime", "B. naloxone",
                 "C. desferrioxamine", "D. acetylcysteine"],
     "correct_answer": "A",
     "explanation": "Atropine blocks the muscarinic overstimulation; pralidoxime reactivates acetylcholinesterase if given before the organophosphate bond 'ages'.",
     "related": ["Antidotes", "Organophosphates"]},

    {"topic": "Antidotes", "difficulty": "easy",
     "question": "The antidote for iron poisoning is a chelator called:",
     "options": ["A. desferrioxamine", "B. pralidoxime",
                 "C. fomepizole", "D. flumazenil"],
     "correct_answer": "A",
     "explanation": "Desferrioxamine chelates free ferric iron into a renally excreted complex, preventing iron-driven free-radical damage.",
     "related": ["Antidotes", "Iron Poisoning"]},

    {"topic": "Antidotes", "difficulty": "medium",
     "question": "The mainstay treatment for carbon monoxide poisoning is:",
     "options": ["A. high-flow 100 percent oxygen",
                 "B. an intravenous naloxone infusion",
                 "C. oral activated charcoal doses",
                 "D. a sodium bicarbonate infusion"],
     "correct_answer": "A",
     "explanation": "CO binds haemoglobin ~240× more avidly than O₂; high-flow 100% oxygen (or hyperbaric in severe cases) displaces it and shortens the carboxyhaemoglobin half-life.",
     "related": ["Antidotes", "Carbon Monoxide"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
