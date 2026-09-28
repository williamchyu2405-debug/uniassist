#!/usr/bin/env python3
"""MEDI2004 W8 · Drug Regulation in Australia — the TGA — NEW exam-calibrated bank.

Net-new regen script; KEY matches the bank key so this fragment overwrites it on
assemble. Applied/scenario style (TGA/ARTG, AUST R vs AUST L risk tiers, scheduling
S2–S8, Product Information, Special Access Scheme, TGA approval vs PBS subsidy).
Correct option written first as A.; backend shuffles positions on seed.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from qbank_lib import emit  # noqa

KEY = "drug_regulation_tga_medi2004_wk8.html"
META = {
    "title": "MEDI2004 W8 · Drug Regulation in Australia — the TGA",
    "subject": "Pharmacology Fundamentals",
    "unit": "MEDI2004",
    "content": (
        "How medicines are regulated in Australia. The Therapeutic Goods Administration "
        "(TGA) regulates therapeutic goods under the Therapeutic Goods Act; a product "
        "must be entered on the Australian Register of Therapeutic Goods (ARTG) before it "
        "can be supplied. Regulation sits at the end of the development funnel — after "
        "Phase III, before and during Phase IV. Two risk tiers: Registered medicines "
        "(AUST R) are higher-risk and evaluated for quality, safety AND efficacy "
        "(prescription drugs and many over-the-counter medicines); Listed medicines "
        "(AUST L) are lower-risk, built only from pre-approved low-risk ingredients and "
        "assessed for quality and safety but NOT efficacy (e.g. vitamins, sunscreens, "
        "many complementary medicines). New-medicine approval is evidence-based, with "
        "ongoing risk management and an approved Product Information (PI) document. "
        "Scheduling under the Poisons Standard sets how a substance is supplied: S2 "
        "Pharmacy Medicine, S3 Pharmacist Only Medicine, S4 Prescription Only Medicine, "
        "S8 Controlled Drug. The Special Access Scheme allows use of unapproved goods in "
        "defined cases; prescription medicines cannot be advertised to the public. "
        "Generics and biosimilars follow their own pathways. Importantly, TGA approval "
        "(allowed on the market) is separate from PBS listing (government subsidy of cost). "
        "Phase IV exists because rare harms (thalidomide, rofecoxib) surface only after "
        "wide use."
    ),
}

Q = [
    # ── easy (5) ──
    {"topic": "TGA", "difficulty": "easy",
     "question": "In Australia, the body that regulates medicines and other therapeutic goods is the:",
     "options": ["A. TGA", "B. PBS", "C. NHMRC", "D. WHO"],
     "correct_answer": "A",
     "explanation": "The Therapeutic Goods Administration (TGA) is the national regulator of medicines and therapeutic goods in Australia.",
     "related": ["TGA", "ARTG"]},

    {"topic": "ARTG", "difficulty": "easy",
     "question": "Before a medicine can be legally supplied in Australia it must be entered on the:",
     "options": ["A. ARTG", "B. PBS list", "C. phone book", "D. share market"],
     "correct_answer": "A",
     "explanation": "A product must be listed on the Australian Register of Therapeutic Goods (ARTG) before it can be supplied.",
     "related": ["ARTG", "TGA"]},

    {"topic": "Registered Medicines", "difficulty": "easy",
     "question": "A higher-risk medicine fully evaluated for quality, safety and efficacy carries which marking?",
     "options": ["A. AUST R", "B. AUST L", "C. AUST X", "D. AUST Z"],
     "correct_answer": "A",
     "explanation": "Registered medicines carry an AUST R number, reflecting full evaluation of quality, safety and efficacy.",
     "related": ["Registered Medicines", "Listed Medicines"]},

    {"topic": "Scheduling", "difficulty": "easy",
     "question": "A medicine that can only be obtained on a doctor's prescription is scheduled as:",
     "options": ["A. S4 Prescription Only", "B. S2 Pharmacy Medicine", "C. unscheduled", "D. a foodstuff"],
     "correct_answer": "A",
     "explanation": "Schedule 4 (Prescription Only Medicine) can be supplied only on a valid prescription.",
     "related": ["Scheduling", "Poisons Standard"]},

    {"topic": "TGA vs PBS", "difficulty": "easy",
     "question": "TGA approval of a medicine means it is allowed on the market; the PBS instead decides whether it is:",
     "options": ["A. subsidised", "B. banned", "C. imported", "D. invented"],
     "correct_answer": "A",
     "explanation": "TGA approval permits marketing; PBS listing separately determines whether the government subsidises the medicine's cost.",
     "related": ["TGA vs PBS", "TGA"]},

    # ── medium (11) ──
    {"topic": "Listed Medicines", "difficulty": "medium",
     "question": "Listed (AUST L) medicines such as many vitamins are assessed for quality and safety but NOT for:",
     "options": ["A. efficacy", "B. sterility", "C. labelling", "D. packaging"],
     "correct_answer": "A",
     "explanation": "Listed medicines use pre-approved low-risk ingredients and are not evaluated by the TGA for whether they actually work.",
     "related": ["Listed Medicines", "Registered Medicines"]},

    {"topic": "Risk Tiers", "difficulty": "medium",
     "question": "The split between Registered and Listed medicines is fundamentally a classification by:",
     "options": ["A. risk", "B. colour", "C. price", "D. taste"],
     "correct_answer": "A",
     "explanation": "The two tiers sort products by risk: higher-risk medicines are Registered and fully evaluated, lower-risk ones are Listed.",
     "related": ["Risk Tiers", "Listed Medicines"]},

    {"topic": "Product Information", "difficulty": "medium",
     "question": "The approved Product Information (PI) document for a prescription medicine is mainly intended for:",
     "options": ["A. health professionals", "B. advertising agencies", "C. schoolchildren", "D. share traders"],
     "correct_answer": "A",
     "explanation": "The PI is the TGA-approved reference for prescribers and pharmacists, summarising indications, dosing, warnings and safety.",
     "related": ["Product Information", "Risk Management"]},

    {"topic": "Scheduling", "difficulty": "medium",
     "question": "A drug with high potential for abuse and dependence, tightly controlled, is scheduled as:",
     "options": ["A. S8 Controlled Drug", "B. S2 Pharmacy Medicine", "C. S3 Pharmacist Only", "D. unscheduled"],
     "correct_answer": "A",
     "explanation": "Schedule 8 (Controlled Drug) covers substances like strong opioids that need strict recording and control.",
     "related": ["Scheduling", "Poisons Standard"]},

    {"topic": "Poisons Standard", "difficulty": "medium",
     "question": "The document that assigns each substance to a schedule is the:",
     "options": ["A. Poisons Standard", "B. tax code", "C. phone directory", "D. patent register"],
     "correct_answer": "A",
     "explanation": "The Poisons Standard (SUSMP) sets the schedule for each substance, determining how it may be supplied.",
     "related": ["Poisons Standard", "Scheduling"]},

    {"topic": "Pharmacist Only", "difficulty": "medium",
     "question": "A medicine that a pharmacist must personally hand over after assessing the customer is scheduled:",
     "options": ["A. S3 Pharmacist Only", "B. S4 Prescription Only", "C. S8 Controlled Drug", "D. unscheduled"],
     "correct_answer": "A",
     "explanation": "Schedule 3 (Pharmacist Only Medicine) requires the pharmacist's involvement but not a prescription.",
     "related": ["Pharmacist Only", "Scheduling"]},

    {"topic": "Advertising Rules", "difficulty": "medium",
     "question": "Under Australian rules, prescription (S4) medicines may NOT be advertised directly to:",
     "options": ["A. the general public", "B. the treating doctors", "C. the local pharmacists", "D. the medical specialists"],
     "correct_answer": "A",
     "explanation": "Direct-to-consumer advertising of prescription medicines is prohibited; promotion is restricted to health professionals.",
     "related": ["Advertising Rules", "Scheduling"]},

    {"topic": "Special Access Scheme", "difficulty": "medium",
     "question": "The Special Access Scheme allows a patient to receive a medicine that is:",
     "options": ["A. not yet ARTG-approved", "B. already on the PBS", "C. a common vitamin", "D. an ordinary food"],
     "correct_answer": "A",
     "explanation": "The Special Access Scheme permits supply of unapproved therapeutic goods for individual patients in defined circumstances.",
     "related": ["Special Access Scheme", "ARTG"]},

    {"topic": "Regulation in Lifecycle", "difficulty": "medium",
     "question": "In the drug-development funnel, the TGA's approval decision falls after Phase III and just before:",
     "options": ["A. Phase IV surveillance", "B. drug discovery", "C. lead optimisation", "D. preclinical testing"],
     "correct_answer": "A",
     "explanation": "Regulatory approval is the last narrow point of the funnel, after the pivotal Phase III trials and before Phase IV monitoring.",
     "related": ["Regulation in Lifecycle", "TGA"]},

    {"topic": "Generics", "difficulty": "medium",
     "question": "A generic medicine entering the market must still be entered on the ARTG and shown to be:",
     "options": ["A. bioequivalent to the original", "B. cheaper than every rival", "C. a completely new molecule", "D. sold without a brand"],
     "correct_answer": "A",
     "explanation": "A generic must demonstrate bioequivalence to the reference product and be registered before it can be supplied.",
     "related": ["Generics", "Registered Medicines"]},

    {"topic": "Evidence-Based Approval", "difficulty": "medium",
     "question": "The TGA's decision to approve a new medicine is based primarily on:",
     "options": ["A. submitted evidence", "B. company reputation", "C. public popularity", "D. share price"],
     "correct_answer": "A",
     "explanation": "Approval rests on the evidence dossier — quality, safety and efficacy data — not on reputation or popularity.",
     "related": ["Evidence-Based Approval", "Product Information"]},

    # ── hard (10) ──
    {"topic": "AUST R vs AUST L", "difficulty": "hard",
     "question": "A sunscreen marked AUST L and an antibiotic marked AUST R differ most importantly in whether the TGA assessed their:",
     "options": ["A. efficacy", "B. existence", "C. colour", "D. country"],
     "correct_answer": "A",
     "explanation": "Registered (AUST R) products are evaluated for efficacy; Listed (AUST L) products are not, being lower-risk pre-approved ingredients.",
     "related": ["AUST R vs AUST L", "Risk Tiers"]},

    {"topic": "TGA vs PBS", "difficulty": "hard",
     "question": "A new cancer drug is TGA-approved but not PBS-listed. For patients this most likely means the drug is:",
     "options": ["A. available but expensive", "B. banned from sale", "C. free to everyone", "D. still unapproved"],
     "correct_answer": "A",
     "explanation": "TGA approval lets it be sold, but without PBS subsidy the patient bears the high cost until (or unless) it is listed.",
     "related": ["TGA vs PBS", "Regulation in Lifecycle"]},

    {"topic": "Independent Gate", "difficulty": "hard",
     "question": "A separate regulatory-approval step exists mainly because the company that developed the drug is:",
     "options": ["A. not an impartial judge", "B. always fully unbiased", "C. legally the regulator", "D. unaware of the data"],
     "correct_answer": "A",
     "explanation": "After years and a fortune invested, the developer cannot rule impartially on its own product, so an independent TGA gate is required.",
     "related": ["Independent Gate", "Evidence-Based Approval"]},

    {"topic": "Phase IV Rationale", "difficulty": "hard",
     "question": "Drugs like thalidomide and rofecoxib show why post-marketing surveillance matters: some harms appear only once the drug reaches:",
     "options": ["A. very large populations", "B. the discovery lab", "C. animal testing", "D. a single volunteer"],
     "correct_answer": "A",
     "explanation": "Rare or delayed harms surface only when millions are exposed after approval, which is exactly what Phase IV surveillance is designed to catch.",
     "related": ["Phase IV Rationale", "Regulation in Lifecycle"]},

    {"topic": "Scheduling Logic", "difficulty": "hard",
     "question": "Moving a substance from S4 to S3 would generally make it:",
     "options": ["A. easier to obtain", "B. harder to obtain", "C. completely banned", "D. a controlled drug"],
     "correct_answer": "A",
     "explanation": "S3 (Pharmacist Only) needs no prescription, so down-scheduling from S4 to S3 increases access under pharmacist supervision.",
     "related": ["Scheduling Logic", "Scheduling"]},

    {"topic": "Approval Not Zero-Risk", "difficulty": "hard",
     "question": "For a prescriber, 'TGA-approved' should be read as meaning the benefit–risk balance looked acceptable, not that the drug is:",
     "options": ["A. free of all risk", "B. entirely without benefit", "C. never once evaluated", "D. illegal to ever sell"],
     "correct_answer": "A",
     "explanation": "Approval reflects an acceptable benefit–risk judgement on current evidence; it never guarantees zero risk, hence continued vigilance.",
     "related": ["Approval Not Zero-Risk", "Phase IV Rationale"]},

    {"topic": "Biosimilar Pathway", "difficulty": "hard",
     "question": "A biosimilar is regulated differently from a small-molecule generic because its active substance:",
     "options": ["A. cannot be copied exactly", "B. is a simple chemical", "C. needs no evaluation", "D. is always cheaper"],
     "correct_answer": "A",
     "explanation": "A biologic cannot be reproduced identically, so a biosimilar follows a distinct pathway proving high similarity rather than identity.",
     "related": ["Biosimilar Pathway", "Generics"]},

    {"topic": "Therapeutic Goods Act", "difficulty": "hard",
     "question": "The legal authority making ARTG entry and TGA oversight compulsory comes from the:",
     "options": ["A. Therapeutic Goods Act", "B. road traffic code", "C. income tax law", "D. building regulations"],
     "correct_answer": "A",
     "explanation": "The Therapeutic Goods Act is the legislation underpinning the TGA, the ARTG and the compulsory regulation of therapeutic goods.",
     "related": ["Therapeutic Goods Act", "TGA"]},

    {"topic": "Risk Management", "difficulty": "hard",
     "question": "Ongoing risk-management requirements after approval reflect that regulation does not stop at the:",
     "options": ["A. approval stamp", "B. discovery bench", "C. first synthesis", "D. patent filing"],
     "correct_answer": "A",
     "explanation": "Risk-management plans and Phase IV monitoring continue after approval, showing that oversight extends well beyond the approval decision.",
     "related": ["Risk Management", "Phase IV Rationale"]},

    {"topic": "Listed Medicine Limits", "difficulty": "hard",
     "question": "A company wanting to make a strong efficacy claim for a herbal product could not simply List it, because Listed medicines may only use:",
     "options": ["A. pre-approved low-risk ingredients", "B. any untested new chemical", "C. prescription-only substances", "D. controlled S8 drugs"],
     "correct_answer": "A",
     "explanation": "Listing is confined to pre-approved low-risk ingredients and permits only limited claims; a strong efficacy claim would require Registration.",
     "related": ["Listed Medicine Limits", "AUST R vs AUST L"]},
]

if __name__ == "__main__":
    sys.exit(emit(KEY, META, Q))
