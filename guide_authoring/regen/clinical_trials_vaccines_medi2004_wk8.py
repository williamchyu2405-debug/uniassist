#!/usr/bin/env python3
"""MEDI2004 W8 · Clinical Trials & Vaccine Development — NEW exam-calibrated bank.

Net-new regen script; KEY matches the bank key so this fragment overwrites it on
assemble. Applied/scenario style (Phase I healthy volunteers, Phase II/III patients,
Phase IV surveillance, ICH-GCP/NHMRC ethics, placebo, attrition funnel, COVID vaccine
speed). Correct option written first as A.; backend shuffles positions on seed.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "clinical_trials_vaccines_medi2004_wk8.html"
META = {
    "title": "MEDI2004 W8 · Clinical Trials & Vaccine Development",
    "subject": "Pharmacology Fundamentals",
    "unit": "MEDI2004",
    "content": (
        "How a molecule becomes a medicine through human testing. A clinical trial is a "
        "controlled, prospective experiment in humans. Trials sit in the middle of a "
        "lossy pipeline: discovery → preclinical → clinical (Phases I–III) → regulatory "
        "approval → Phase IV, with an attrition funnel of roughly 100 → 20 → 10 → 5 → 2 "
        "→ 1.2 → 1, so only about 1% of discovery projects — and about 10% of first-in-"
        "human candidates — reach the market, over ~10–15 years. Ethics and regulation: "
        "the NHMRC guidelines and ICH Good Clinical Practice (GCP), including informed "
        "consent and ethics-committee review. The phases: Phase I is first-in-human, "
        "usually in a small number of healthy volunteers, testing safety, tolerability "
        "and pharmacokinetics; Phase II tests early efficacy and dose in a modest number "
        "of patients; Phase III is the large-scale, controlled (often randomised, blinded) "
        "pivotal test of efficacy and safety; Phase IV is post-marketing surveillance in "
        "the general population after approval. Pharmacovigilance monitors safety once "
        "marketed; Phase 0 uses tiny micro-doses. The placebo effect is a real response to "
        "an inactive treatment, which controlled trials must beat. COVID-19 vaccines were "
        "developed fast by running steps in parallel and funding upfront — without skipping "
        "any phase."
    ),
}

Q = [
    # ── easy (5) ──
    {"topic": "Clinical Trial Definition", "difficulty": "easy",
     "question": "A clinical trial is best defined as a controlled, prospective experiment carried out in:",
     "options": ["A. humans", "B. rocks", "C. software", "D. archives"],
     "correct_answer": "A",
     "explanation": "A clinical trial is a controlled, forward-looking experiment in human participants to test a medical intervention.",
     "related": ["Clinical Trial Definition", "Trial Phases"]},

    {"topic": "Phase I", "difficulty": "easy",
     "question": "Phase I trials are usually the first time a new drug is given to:",
     "options": ["A. humans", "B. patients only", "C. regulators", "D. computers"],
     "correct_answer": "A",
     "explanation": "Phase I is the first-in-human step, typically in a small group of healthy volunteers to assess basic safety.",
     "related": ["Phase I", "Trial Phases"]},

    {"topic": "Phase IV", "difficulty": "easy",
     "question": "Phase IV of drug testing takes place at which point?",
     "options": ["A. after marketing", "B. before discovery", "C. during synthesis", "D. instead of Phase I"],
     "correct_answer": "A",
     "explanation": "Phase IV is post-marketing surveillance, monitoring the drug once it is approved and in wide use.",
     "related": ["Phase IV", "Pharmacovigilance"]},

    {"topic": "Placebo", "difficulty": "easy",
     "question": "A placebo used in a trial is a treatment that is:",
     "options": ["A. pharmacologically inactive", "B. highly toxic", "C. the strongest drug", "D. a live vaccine"],
     "correct_answer": "A",
     "explanation": "A placebo is an inactive treatment used as a comparison so the drug's true effect can be separated from expectation.",
     "related": ["Placebo", "Controlled Trial"]},

    {"topic": "Ethics", "difficulty": "easy",
     "question": "Before joining a trial, participants must give their informed:",
     "options": ["A. consent", "B. payment", "C. diagnosis", "D. prescription"],
     "correct_answer": "A",
     "explanation": "Informed consent — understanding and voluntarily agreeing to the trial — is a core ethical requirement of human research.",
     "related": ["Ethics", "Good Clinical Practice"]},

    # ── medium (12) ──
    {"topic": "Phase I", "difficulty": "medium",
     "question": "The main aim of a Phase I trial is to assess a drug's safety, tolerability and:",
     "options": ["A. pharmacokinetics", "B. market price", "C. brand appeal", "D. patent length"],
     "correct_answer": "A",
     "explanation": "Phase I focuses on how the body handles the drug (pharmacokinetics) and what doses are safely tolerated.",
     "related": ["Phase I", "Trial Phases"]},

    {"topic": "Phase II", "difficulty": "medium",
     "question": "Phase II trials move into patients with the disease chiefly to test early efficacy and:",
     "options": ["A. dose selection", "B. factory scale-up", "C. advertising reach", "D. shelf life"],
     "correct_answer": "A",
     "explanation": "Phase II looks for signs the drug works and helps choose the dose to carry into larger trials.",
     "related": ["Phase II", "Phase III"]},

    {"topic": "Phase III", "difficulty": "medium",
     "question": "Phase III is called the pivotal test because it provides large-scale, controlled evidence of efficacy and:",
     "options": ["A. safety", "B. colour", "C. pricing", "D. branding"],
     "correct_answer": "A",
     "explanation": "Phase III enrols many patients in controlled trials to confirm both efficacy and safety before approval is sought.",
     "related": ["Phase III", "Regulatory Approval"]},

    {"topic": "Healthy Volunteers", "difficulty": "medium",
     "question": "Phase I typically uses healthy volunteers rather than patients so that early observations reflect the drug and not the:",
     "options": ["A. underlying disease", "B. placebo colour", "C. clinic location", "D. trial sponsor"],
     "correct_answer": "A",
     "explanation": "Using healthy volunteers lets investigators study safety and handling of the drug without confounding by the disease itself.",
     "related": ["Healthy Volunteers", "Phase I"]},

    {"topic": "Attrition Funnel", "difficulty": "medium",
     "question": "Across the whole pipeline, roughly what fraction of discovery projects become a marketed drug?",
     "options": ["A. about 1 percent", "B. about 50 percent", "C. about 90 percent", "D. exactly 100 percent"],
     "correct_answer": "A",
     "explanation": "Only about 1 in 100 discovery projects survives the funnel to become an approved, marketed medicine.",
     "related": ["Attrition Funnel", "Drug Development Pipeline"]},

    {"topic": "Good Clinical Practice", "difficulty": "medium",
     "question": "The international ethical and quality standard governing how trials are run is known as:",
     "options": ["A. Good Clinical Practice", "B. Good Marketing Practice", "C. Good Accounting Practice", "D. Good Farming Practice"],
     "correct_answer": "A",
     "explanation": "ICH Good Clinical Practice (GCP) sets the ethical and scientific quality standards for designing and conducting trials.",
     "related": ["Good Clinical Practice", "Ethics"]},

    {"topic": "Controlled Trial", "difficulty": "medium",
     "question": "A controlled trial compares the new treatment against a control group to reveal the drug's:",
     "options": ["A. true added effect", "B. manufacturing cost", "C. chemical formula", "D. storage temperature"],
     "correct_answer": "A",
     "explanation": "Comparing with a control (placebo or standard care) isolates the drug's genuine effect from natural change and expectation.",
     "related": ["Controlled Trial", "Placebo"]},

    {"topic": "Pharmacovigilance", "difficulty": "medium",
     "question": "Detecting a rare side effect only after a drug is widely marketed is the job of:",
     "options": ["A. pharmacovigilance", "B. Phase I testing", "C. lead optimisation", "D. preclinical work"],
     "correct_answer": "A",
     "explanation": "Pharmacovigilance monitors safety in the marketed population, catching rare harms that trials were too small to reveal.",
     "related": ["Pharmacovigilance", "Phase IV"]},

    {"topic": "Randomisation", "difficulty": "medium",
     "question": "Randomly assigning participants to treatment or control groups mainly serves to:",
     "options": ["A. balance the groups", "B. lower the cost", "C. speed the dosing", "D. pick the healthiest"],
     "correct_answer": "A",
     "explanation": "Randomisation balances known and unknown differences between groups, so any outcome difference can be attributed to the treatment.",
     "related": ["Randomisation", "Controlled Trial"]},

    {"topic": "Blinding", "difficulty": "medium",
     "question": "Keeping participants unaware of whether they receive drug or placebo (blinding) chiefly reduces:",
     "options": ["A. expectation bias", "B. drug potency", "C. trial funding", "D. dose size"],
     "correct_answer": "A",
     "explanation": "Blinding prevents participants' expectations from colouring reported outcomes, reducing bias in the comparison.",
     "related": ["Blinding", "Placebo"]},

    {"topic": "COVID Vaccine", "difficulty": "medium",
     "question": "COVID-19 vaccines were developed unusually quickly mainly because developers:",
     "options": ["A. ran steps in parallel", "B. skipped Phase III", "C. omitted all ethics", "D. avoided any testing"],
     "correct_answer": "A",
     "explanation": "Massive upfront funding let developers overlap normally sequential steps and manufacture at risk, without skipping any trial phase.",
     "related": ["COVID Vaccine", "Drug Development Pipeline"]},

    # ── hard (10) ──
    {"topic": "Phase Ordering", "difficulty": "hard",
     "question": "Placing the phases in order, first-in-human safety comes before efficacy-and-dose, which comes before the:",
     "options": ["A. pivotal controlled trial", "B. discovery screen", "C. preclinical toxicology", "D. target selection"],
     "correct_answer": "A",
     "explanation": "Phase I (safety) precedes Phase II (efficacy/dose), which precedes the large Phase III pivotal controlled trial.",
     "related": ["Phase Ordering", "Trial Phases"]},

    {"topic": "Staged Design", "difficulty": "hard",
     "question": "Trials are run in ascending phases mainly so that expensive, large studies are done only on drugs that have already shown:",
     "options": ["A. early safety and promise", "B. a catchy brand name", "C. a low retail price", "D. a bright tablet colour"],
     "correct_answer": "A",
     "explanation": "The staged design is a cost-and-risk filter: cheap questions on few people first, so big Phase III studies run only on de-risked candidates.",
     "related": ["Staged Design", "Attrition Funnel"]},

    {"topic": "Clinical Candidate Survival", "difficulty": "hard",
     "question": "If about 10 candidates enter Phase I and 1 is approved, the success rate from first-in-human to market is about:",
     "options": ["A. 10 percent", "B. 90 percent", "C. 1 percent", "D. 50 percent"],
     "correct_answer": "A",
     "explanation": "One approval from ten entering human trials is roughly a 10% success rate for first-in-human candidates.",
     "related": ["Clinical Candidate Survival", "Attrition Funnel"]},

    {"topic": "Placebo Effect", "difficulty": "hard",
     "question": "The existence of a genuine placebo effect is the main reason a new drug must be shown to be better than:",
     "options": ["A. an inactive comparator", "B. the maximum dose", "C. an older factory", "D. its own brand name"],
     "correct_answer": "A",
     "explanation": "Because inactive treatment can itself produce improvement, a drug must beat a placebo comparator to prove a real pharmacological effect.",
     "related": ["Placebo Effect", "Controlled Trial"]},

    {"topic": "Phase IV Necessity", "difficulty": "hard",
     "question": "A harm occurring once in 10,000 users may be missed before approval because Phase III typically enrols only:",
     "options": ["A. a few thousand patients", "B. several million patients", "C. no patients at all", "D. only healthy staff"],
     "correct_answer": "A",
     "explanation": "With at most a few thousand participants, Phase III cannot reliably detect a 1-in-10,000 event, which is why Phase IV surveillance is needed.",
     "related": ["Phase IV Necessity", "Pharmacovigilance"]},

    {"topic": "Phase 0", "difficulty": "hard",
     "question": "A Phase 0 study gives participants a tiny 'micro-dose' mainly to gather very early data on:",
     "options": ["A. human pharmacokinetics", "B. large-scale efficacy", "C. long-term safety", "D. marketing appeal"],
     "correct_answer": "A",
     "explanation": "Phase 0 uses sub-therapeutic micro-doses to see how the drug behaves in humans before committing to full Phase I.",
     "related": ["Phase 0", "Phase I"]},

    {"topic": "Ethics Committee", "difficulty": "hard",
     "question": "An independent ethics committee reviews a trial protocol primarily to protect the:",
     "options": ["A. participants' welfare", "B. sponsor's profit", "C. drug's patent", "D. factory's output"],
     "correct_answer": "A",
     "explanation": "Ethics committees judge whether risks to participants are justified and consent is adequate, safeguarding the people in the trial.",
     "related": ["Ethics Committee", "Good Clinical Practice"]},

    {"topic": "COVID Vaccine", "difficulty": "hard",
     "question": "Manufacturing COVID-19 vaccines 'at risk' during trials meant companies:",
     "options": ["A. produced doses before approval", "B. released untested vaccines", "C. skipped Phase III", "D. avoided ethics review"],
     "correct_answer": "A",
     "explanation": "At-risk manufacturing built stockpiles before knowing if the vaccine would be approved, saving time without bypassing any safety phase.",
     "related": ["COVID Vaccine", "Staged Design"]},

    {"topic": "Prospective Design", "difficulty": "hard",
     "question": "Describing a clinical trial as 'prospective' means outcomes are followed:",
     "options": ["A. forward from enrolment", "B. backward from records", "C. only in the lab", "D. after the drug is banned"],
     "correct_answer": "A",
     "explanation": "A prospective trial defines the intervention and then follows participants forward in time to measure predetermined outcomes.",
     "related": ["Prospective Design", "Clinical Trial Definition"]},

    {"topic": "Drug Development Pipeline", "difficulty": "hard",
     "question": "On the development map, clinical trials sit between preclinical development and:",
     "options": ["A. regulatory approval", "B. target discovery", "C. lead optimisation", "D. chemical synthesis"],
     "correct_answer": "A",
     "explanation": "Human trials follow preclinical work and precede regulatory approval, after which Phase IV surveillance continues.",
     "related": ["Drug Development Pipeline", "Phase Ordering"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
