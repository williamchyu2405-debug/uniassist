#!/usr/bin/env python3
"""MEDI2200 W7 · Proteins — NEW gallery bank (length-matched, no bracket tells, no daredevil).
New guide: META is defined inline and the entry is written straight into guide_quizzes.json
(assemble_bank.py only rewrites keys already present in the bank)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "proteins_medi2200_wk7.html"
META = {
    "title": "Proteins — Structure, Folding, Enzymes & Regulation",
    "subject": "Human Cell & Molecular Biology",
    "unit": "MEDI2200",
    "content": ("Proteins (MEDI2200 Wk7, Dr Russell Diefenbach, Parts 1-4): the four levels of "
                "protein structure and how sequence sets 3D shape and function; protein folding "
                "(hydrophobic effect, chaperones/chaperonins, ubiquitin-proteasome degradation, "
                "amyloid misfolding disease); enzyme binding and catalysis (active site, activation "
                "energy, acid-base catalysis, catalytic triad, lysozyme, pH dependence, multienzyme "
                "complexes); and regulation (allosteric, ubiquitinylation, GTPase GEF/GAP switch, "
                "phosphorylation by kinases and phosphatases)."),
}

Q = [
 # ── easy ──────────────────────────────────────────────────────────────
 {"topic": "Structure-function", "difficulty": "easy",
  "question": "A protein's three-dimensional structure is ultimately determined by its:",
  "options": ["A. primary amino acid sequence", "B. surrounding lipid membrane",
              "C. bound metal ions", "D. rate of transcription"],
  "correct_answer": "A",
  "explanation": "Function derives from 3D structure, which is set by the primary amino acid sequence plus intramolecular noncovalent interactions.",
  "related": ["Structure-function", "Primary structure"]},

 {"topic": "Primary structure", "difficulty": "easy",
  "question": "Amino acids in a protein's primary structure are joined by which bond?",
  "options": ["A. the peptide bond", "B. the hydrogen bond",
              "C. the disulfide bond", "D. the glycosidic bond"],
  "correct_answer": "A",
  "explanation": "The primary structure is a linear sequence of amino acids linked head-to-tail by covalent peptide bonds, from N- to C-terminus.",
  "related": ["Primary structure", "Structure-function"]},

 {"topic": "Enzyme action", "difficulty": "easy",
  "question": "Enzymes speed up reactions by lowering the:",
  "options": ["A. activation energy", "B. equilibrium constant",
              "C. substrate concentration", "D. product concentration"],
  "correct_answer": "A",
  "explanation": "Enzymes accelerate reactions by lowering the activation energy, stabilising the transition state; they do not change the equilibrium.",
  "related": ["Enzyme action", "Activation energy"]},

 {"topic": "Secondary structure", "difficulty": "easy",
  "question": "Which secondary structure is a coil stabilised by backbone hydrogen bonds?",
  "options": ["A. the alpha helix", "B. the beta sheet",
              "C. the beta turn", "D. the random coil"],
  "correct_answer": "A",
  "explanation": "The alpha helix is a coiled secondary structure held by hydrogen bonds between backbone amide and carbonyl groups, with R groups projecting outward.",
  "related": ["Secondary structure", "Alpha helix"]},

 {"topic": "GTPase switch", "difficulty": "easy",
  "question": "A GTPase bound to GTP is in which state?",
  "options": ["A. the active on state", "B. the inactive off state",
              "C. a degraded state", "D. an unfolded state"],
  "correct_answer": "A",
  "explanation": "GTP-bound is the active 'on' conformation; GDP-bound is the inactive 'off' conformation.",
  "related": ["GTPase switch", "Regulation"]},

 # ── medium ────────────────────────────────────────────────────────────
 {"topic": "Secondary structure", "difficulty": "medium",
  "question": "Secondary structures are stabilised by hydrogen bonds between which groups?",
  "options": ["A. backbone amide and carbonyl", "B. two nonpolar side chains",
              "C. charged side chains only", "D. metal ions and water"],
  "correct_answer": "A",
  "explanation": "Secondary structure is held by hydrogen bonds between backbone amide (N-H) and carbonyl (C=O) groups, not the side chains.",
  "related": ["Secondary structure", "Alpha helix"]},

 {"topic": "Helix breaker", "difficulty": "medium",
  "question": "Which amino acid cannot hydrogen bond in the backbone and is excluded from an alpha helix?",
  "options": ["A. proline", "B. alanine",
              "C. leucine", "D. serine"],
  "correct_answer": "A",
  "explanation": "Proline's ring locks the backbone and leaves no amide hydrogen to donate, so it is a helix breaker excluded from alpha helices.",
  "related": ["Helix breaker", "Secondary structure"]},

 {"topic": "Beta sheet", "difficulty": "medium",
  "question": "In a beta sheet, alternate R groups project which way relative to the sheet plane?",
  "options": ["A. above and below", "B. into the sheet interior",
              "C. along a single edge", "D. toward the N-terminus"],
  "correct_answer": "A",
  "explanation": "In a beta sheet, alternate R groups project above and below the plane, while backbone hydrogen bonds link adjacent strands.",
  "related": ["Beta sheet", "Secondary structure"]},

 {"topic": "Tertiary structure", "difficulty": "medium",
  "question": "Tertiary structure is stabilised primarily by which type of interaction?",
  "options": ["A. hydrophobic interactions", "B. covalent peptide bonds",
              "C. backbone amide bonds", "D. ionic bonds only"],
  "correct_answer": "A",
  "explanation": "Tertiary structure is stabilised chiefly by hydrophobic interactions that cluster nonpolar side chains in the core, plus hydrogen bonds.",
  "related": ["Tertiary structure", "Folding"]},

 {"topic": "Native state", "difficulty": "medium",
  "question": "The native state of a protein is usually the conformation with the:",
  "options": ["A. lowest free energy", "B. highest free energy",
              "C. most hydrogen bonds", "D. fewest amino acids"],
  "correct_answer": "A",
  "explanation": "The native, correctly folded state is normally the conformation of lowest free energy.",
  "related": ["Native state", "Folding"]},

 {"topic": "Chaperones", "difficulty": "medium",
  "question": "Which of these is a molecular chaperone that helps proteins fold?",
  "options": ["A. Hsp70", "B. ubiquitin",
              "C. collagen", "D. lysozyme"],
  "correct_answer": "A",
  "explanation": "Hsp70 is an ATP-dependent molecular chaperone that binds exposed segments of unfolded proteins to prevent aggregation.",
  "related": ["Chaperones", "Folding"]},

 {"topic": "Ubiquitin", "difficulty": "medium",
  "question": "In the ubiquitin-proteasome system, ubiquitin chains are attached to which residue?",
  "options": ["A. lysine", "B. serine",
              "C. glycine", "D. cysteine"],
  "correct_answer": "A",
  "explanation": "Ubiquitin ligases (E1, E2, E3) attach ubiquitin chains to lysine residues on the target protein, marking it for the proteasome.",
  "related": ["Ubiquitin", "Degradation"]},

 {"topic": "Amyloid", "difficulty": "medium",
  "question": "Amyloid fibril aggregates are built on which shared structural feature?",
  "options": ["A. a cross-beta-sheet structure", "B. a triple alpha helix",
              "C. a random coil core", "D. a single beta turn"],
  "correct_answer": "A",
  "explanation": "Misfolded proteins aggregate into amyloid fibrils built on a cross-beta-sheet structure that assembles into protofilaments and fibrils.",
  "related": ["Amyloid", "Misfolding disease"]},

 {"topic": "Enzyme mechanism", "difficulty": "medium",
  "question": "When an enzyme binds its substrate, they form the:",
  "options": ["A. enzyme-substrate complex", "B. transition-state analogue",
              "C. covalent product bond", "D. allosteric effector site"],
  "correct_answer": "A",
  "explanation": "The enzyme binds substrate at the active site to form the enzyme-substrate (ES) complex, an intermediate on the way to product.",
  "related": ["Enzyme mechanism", "Active site"]},

 {"topic": "Enzyme equilibrium", "difficulty": "medium",
  "question": "What does an enzyme do to the equilibrium constant of the reaction it catalyses?",
  "options": ["A. leaves it unchanged", "B. increases it greatly",
              "C. decreases it greatly", "D. reverses its sign"],
  "correct_answer": "A",
  "explanation": "An enzyme speeds the approach to equilibrium by lowering activation energy but leaves the equilibrium constant unchanged.",
  "related": ["Enzyme equilibrium", "Activation energy"]},

 {"topic": "Serine protease", "difficulty": "medium",
  "question": "The catalytic triad of a serine protease such as trypsin is made of serine, aspartate and:",
  "options": ["A. histidine", "B. lysine",
              "C. tyrosine", "D. cysteine"],
  "correct_answer": "A",
  "explanation": "Serine proteases use a catalytic triad of serine, histidine and aspartate (Ser-195, His-57, Asp-102 in trypsin) to break peptide bonds.",
  "related": ["Serine protease", "Catalysis"]},

 {"topic": "Lysozyme", "difficulty": "medium",
  "question": "Lysozyme is antimicrobial because it cleaves which bacterial polymer?",
  "options": ["A. peptidoglycan", "B. phospholipid",
              "C. double-stranded DNA", "D. glycogen"],
  "correct_answer": "A",
  "explanation": "Lysozyme is a glycoside hydrolase that cleaves the beta-1,4 bond between NAM and NAG in peptidoglycan, the gram-positive cell wall polymer.",
  "related": ["Lysozyme", "Catalysis"]},

 {"topic": "Allosteric regulation", "difficulty": "medium",
  "question": "An allosteric effector regulates an enzyme by binding:",
  "options": ["A. a separate regulatory site", "B. the active site directly",
              "C. the substrate molecule", "D. the enzyme backbone"],
  "correct_answer": "A",
  "explanation": "An allosteric effector binds a site other than the active site and alters the enzyme's affinity for substrate; feedback inhibition is the classic case.",
  "related": ["Allosteric regulation", "Regulation"]},

 {"topic": "Phosphorylation", "difficulty": "medium",
  "question": "A protein kinase transfers a phosphate group onto its target from which molecule?",
  "options": ["A. ATP", "B. NADH",
              "C. GDP", "D. ubiquitin"],
  "correct_answer": "A",
  "explanation": "Kinases transfer the terminal phosphate of ATP onto Ser, Thr or Tyr residues, usually activating the target protein.",
  "related": ["Phosphorylation", "Regulation"]},

 {"topic": "Quaternary structure", "difficulty": "medium",
  "question": "A protein has quaternary structure when it is made of:",
  "options": ["A. more than one polypeptide", "B. a single long helix",
              "C. only beta sheets", "D. one folded domain"],
  "correct_answer": "A",
  "explanation": "Quaternary structure exists when a functional protein comprises more than one polypeptide chain, such as the hemagglutinin trimer.",
  "related": ["Quaternary structure", "Structure hierarchy"]},

 # ── hard ──────────────────────────────────────────────────────────────
 {"topic": "Coiled-coil", "difficulty": "hard",
  "question": "A coiled-coil motif has a heptad repeat with hydrophobic residues at which positions?",
  "options": ["A. positions 1 and 4", "B. positions 2 and 6",
              "C. positions 3 and 7", "D. positions 5 and 6"],
  "correct_answer": "A",
  "explanation": "Coiled-coils use a heptad repeat with a hydrophobic residue at positions 1 and 4, letting two helices wind around each other.",
  "related": ["Coiled-coil", "Motifs"]},

 {"topic": "Domains", "difficulty": "hard",
  "question": "Roughly what proportion of eukaryotic proteins contain multiple structural domains?",
  "options": ["A. about 75 percent", "B. about 25 percent",
              "C. about 10 percent", "D. about 50 percent"],
  "correct_answer": "A",
  "explanation": "About 75 percent of eukaryotic proteins are multidomain, reflecting how modular domains are reused across the proteome.",
  "related": ["Domains", "Tertiary structure"]},

 {"topic": "Collagen", "difficulty": "hard",
  "question": "Collagen's stabilising crosslinks are formed by hydroxylation of which residue?",
  "options": ["A. lysine", "B. arginine",
              "C. methionine", "D. tryptophan"],
  "correct_answer": "A",
  "explanation": "Collagen crosslinks form by hydroxylation of lysine (and proline), a vitamin-C-dependent step; its failure causes scurvy.",
  "related": ["Collagen", "Fibrous proteins"]},

 {"topic": "Proteasome", "difficulty": "hard",
  "question": "Inside the proteasome, target proteins are degraded by which class of protease?",
  "options": ["A. threonine proteases", "B. serine proteases",
              "C. aspartic proteases", "D. metalloproteases"],
  "correct_answer": "A",
  "explanation": "Once unfolded and translocated inside, the target is cut into peptide fragments by three threonine proteases of the proteasome.",
  "related": ["Proteasome", "Degradation"]},

 {"topic": "pH dependence", "difficulty": "hard",
  "question": "Lysosomal hydrolases have a pH optimum near which value?",
  "options": ["A. 4.5", "B. 7.4",
              "C. 8.0", "D. 2.0"],
  "correct_answer": "A",
  "explanation": "Lysosomal hydrolases peak near pH 4.5, matching the acidic interior of the lysosome where they work.",
  "related": ["pH dependence", "Catalysis"]},

 {"topic": "pH dependence", "difficulty": "hard",
  "question": "Chymotrypsin peaks near pH 8 because its active-site His-57 has a pKa near:",
  "options": ["A. 6.8", "B. 4.5",
              "C. 9.5", "D. 2.0"],
  "correct_answer": "A",
  "explanation": "The active-site His-57 has a pKa around 6.8 and must be deprotonated to act as a base, so activity peaks near pH 8.",
  "related": ["pH dependence", "Serine protease"]},

 {"topic": "Ubiquitin linkage", "difficulty": "hard",
  "question": "Which ubiquitin lysine linkage classically tags a protein for proteasomal degradation?",
  "options": ["A. Lys-48", "B. Lys-63",
              "C. Lys-6", "D. Lys-11"],
  "correct_answer": "A",
  "explanation": "Lys-48-linked polyubiquitin chains classically mark proteins for proteasomal degradation, while other linkages (e.g. Lys-63) act in signalling.",
  "related": ["Ubiquitin linkage", "Degradation"]},

 {"topic": "GTPase regulators", "difficulty": "hard",
  "question": "A GTPase-activating protein (GAP) switches a GTPase off by:",
  "options": ["A. stimulating GTP hydrolysis", "B. exchanging GDP for GTP",
              "C. adding a phosphate group", "D. attaching ubiquitin"],
  "correct_answer": "A",
  "explanation": "A GAP stimulates hydrolysis of bound GTP to GDP, switching the GTPase off; a GEF exchanges GDP for GTP to switch it on.",
  "related": ["GTPase regulators", "GTPase switch"]},

 {"topic": "Quaternary example", "difficulty": "hard",
  "question": "The influenza protein hemagglutinin assembles into which quaternary form?",
  "options": ["A. a trimer", "B. a monomer",
              "C. a dimer", "D. a tetramer"],
  "correct_answer": "A",
  "explanation": "Hemagglutinin is a trimer whose three subunits form a coiled-coil stalk, with each globular head binding sialic acid on target cells.",
  "related": ["Quaternary example", "Quaternary structure"]},

 {"topic": "Activation energy", "difficulty": "hard",
  "question": "The rate of a chemical reaction is related to its activation energy in what way?",
  "options": ["A. inversely", "B. directly",
              "C. not at all", "D. exponentially upward"],
  "correct_answer": "A",
  "explanation": "Reaction rate is inversely related to activation energy, so lowering the barrier (as enzymes do) speeds the reaction.",
  "related": ["Activation energy", "Enzyme action"]},

 {"topic": "Multienzyme complexes", "difficulty": "hard",
  "question": "Assembling pathway enzymes onto a scaffold speeds the pathway by reducing:",
  "options": ["A. substrate diffusion time", "B. the activation energy",
              "C. the equilibrium constant", "D. the number of steps"],
  "correct_answer": "A",
  "explanation": "A scaffold (or fusing enzymes into one polypeptide) hands intermediates directly to the next active site, cutting substrate diffusion time.",
  "related": ["Multienzyme complexes", "Catalysis"]},
]

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
