#!/usr/bin/env python3
"""MEDI2200 W10 · Cellular transport & trafficking — NEW gallery bank (length-matched, no bracket tells, no daredevil).
New guide: META is defined inline and the entry is written straight into guide_quizzes.json
(assemble_bank.py only rewrites keys already present in the bank)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "cell_transport_trafficking_medi2200_wk10.html"
META = {
    "title": "Cellular Transport & Trafficking",
    "subject": "Human Cell & Molecular Biology",
    "unit": "MEDI2200",
    "content": ("Cellular transport and trafficking (MEDI2200 Wk10): membranes as barriers; simple vs "
                "facilitated diffusion; passive vs active transport; transporter states; coupled "
                "transporters (uniport, symport, antiport) and the Na+-glucose symporter; P-type, ABC, "
                "V-type and F-type ATPases and the Na+/K+ pump; ion channel selectivity and gating, "
                "membrane potential, action potentials, synapses and aquaporins; vesicular transport, "
                "coats (clathrin, COPI, COPII), Sar1/ARF GTPases, Rabs and SNAREs; the secretory pathway "
                "(ER quality control, ER-Golgi traffic, Golgi processing, lysosomal sorting, constitutive vs "
                "regulated exocytosis); endocytosis, endosome maturation, lysosomes and LDL uptake."),
}

def q(topic, diff, stem, opts, ans, expl):
    return {"topic": topic, "difficulty": diff, "question": stem,
            "options": [f"{'ABCD'[i]}. {o}" for i, o in enumerate(opts)],
            "correct_answer": ans, "explanation": expl, "related": [topic]}

Q = [
 # easy
 q("Simple diffusion", "easy", "Which molecule crosses a protein-free lipid bilayer most readily?",
   ["glucose", "O2", "Na+", "water"], "B",
   "Small hydrophobic molecules such as O2 dissolve in the lipid core and cross freely; water leaks slowly, glucose barely crosses and ions are blocked."),
 q("Passive vs active", "easy", "Active transport against a gradient can be carried out by:",
   ["transporters only", "channels only", "both channels and transporters", "neither, only by vesicles"], "A",
   "Channels only allow passive flow down the electrochemical gradient; only transporters can be coupled to energy to pump uphill."),
 q("Coupled transport", "easy", "A transporter that moves two solutes in opposite directions is a:",
   ["uniporter", "symporter", "antiporter", "channel"], "C",
   "Antiporters move solutes in opposite directions; symporters move both the same way; uniporters move a single solute and are not coupled."),
 q("Coats", "easy", "Anterograde transport from the ER to the Golgi uses vesicles coated with:",
   ["COPI", "clathrin", "COPII", "AP3"], "C",
   "COPII mediates ER to Golgi (anterograde); COPI mediates Golgi to ER (retrograde); clathrin acts at the trans-Golgi and plasma membrane."),
 q("Aquaporins", "easy", "Aquaporins are channels that:",
   ["pass ions and block water", "pass water and block ions", "pump water using ATP", "pass both water and ions"], "B",
   "Aquaporins allow passive water flow while blocking ions — the opposite of ion channels."),
 q("Lysosome inputs", "easy", "Self-digestion of a cell's own worn-out organelles is called:",
   ["phagocytosis", "macropinocytosis", "autophagy", "endocytosis"], "C",
   "Autophagy delivers cytosol and worn-out organelles (via autophagosomes) to lysosomes; the other three bring material in from outside."),
 # medium
 q("Transporter states", "medium", "In a passive transporter, what determines the net direction of solute flux?",
   ["the concentration gradient of the solute", "the order of the conformational states", "ATP binding to the occluded state", "the charge of the lipid head groups"], "A",
   "Switching between outward-open and inward-open is spontaneous and random; more solute binds on the high-concentration side, so net flux follows the gradient."),
 q("Transporter states", "medium", "The occluded state of a transporter is essential because it:",
   ["keeps the site from opening to both sides", "raises the transporter's binding affinity for ATP", "lets ions shed their hydration shell first", "converts the transporter into an open channel"], "A",
   "The site is accessible from neither side, so the protein never acts as an open pore — which is what allows coupling to energy without leak."),
 q("Na+-glucose symporter", "medium", "In intestinal epithelium, the Na+-glucose symporter moves glucose:",
   ["down its gradient using ATP directly", "against its gradient using the Na+ gradient", "down its gradient with no Na+ needed", "against its gradient using the K+ gradient"], "B",
   "Na+ moving down its electrochemical gradient provides the energy to drag glucose into the cell, where glucose is already more concentrated."),
 q("Na+-glucose symporter", "medium", "The symporter reaches its occluded-occupied state only when:",
   ["only glucose has become bound", "only Na+ has become bound", "both Na+ and glucose are bound", "ATP has been hydrolysed first"], "C",
   "Binding is cooperative and the occluded intermediate forms only with both substrates bound, enforcing strict coupling."),
 q("Na+/K+ pump", "medium", "Per ATP hydrolysed, the Na+/K+ ATPase moves:",
   ["3 Na+ in and 2 K+ out", "2 Na+ out and 3 K+ in", "3 Na+ out and 2 K+ in", "2 Na+ in and 2 K+ out"], "C",
   "It exports 3 Na+ and imports 2 K+, both against their gradients, exporting one net positive charge per cycle."),
 q("ATPase types", "medium", "Acidification of lysosome and endosome lumens is achieved by:",
   ["P-type pumps", "V-type proton pumps", "F-type ATP synthases", "ABC transporters"], "B",
   "V-type pumps use ATP to pump H+ into organelles; F-type synthases run the reverse direction to make ATP from H+ flow."),
 q("ATPase types", "medium", "Which ATPase pumps small molecules rather than ions across the membrane?",
   ["the P-type pump", "the V-type pump", "the ABC transporter", "the F-type synthase"], "C",
   "ABC (ATP-binding cassette) transporters pump small molecules; P-type pumps move ions; V- and F-types move protons."),
 q("Channel selectivity", "medium", "To pass a channel's selectivity filter, an ion must:",
   ["bind ATP at the pore entrance", "be phosphorylated by the channel", "shed its surrounding water molecules", "be co-transported with Na+"], "C",
   "In solution ions carry a hydration shell that must be shed to pass single file through the narrowest part of the channel."),
 q("Gating", "medium", "A channel that opens in response to vibration or pressure is:",
   ["voltage-gated", "mechanically gated", "ligand-gated extracellularly", "ligand-gated intracellularly"], "B",
   "Mechanically gated channels respond to membrane stretch, vibration or pressure."),
 q("Resting potential", "medium", "The negative resting membrane potential depends mainly on:",
   ["Na+ entry through voltage-gated Na+ channels", "K+ efflux through K+ leak channels", "Cl- entry through aquaporin water channels", "Ca2+ efflux through ABC transporter pumps"], "B",
   "The K+ gradient built by the Na+/K+ pump plus K+ leaving through leak channels sets the inside-negative potential."),
 q("Action potential", "medium", "Repolarisation after the action-potential peak is caused by:",
   ["more Na+ channels opening at the peak", "K+ channels closing and Na+ channels reopening", "Na+ channels closing and K+ channels opening", "the Na+/K+ pump reversing its direction"], "C",
   "At the peak, voltage-gated Na+ channels close (inactivate) and voltage-gated K+ channels open, letting K+ out to restore the negative potential."),
 q("GTPases", "medium", "A GEF switches a monomeric GTPase on by:",
   ["promoting hydrolysis of its bound GTP", "promoting exchange of GDP for GTP", "phosphorylating the GTPase on serine", "removing it from the target membrane"], "B",
   "GEFs promote release of GDP and binding of GTP (on); GAPs promote hydrolysis of GTP to GDP (off)."),
 q("Coat GTPases", "medium", "COPII coat assembly at the ER membrane is controlled by:",
   ["ARF", "Sar1", "Rab", "dynamin"], "B",
   "Sar1 assembles COPII at the ER; ARF assembles COPI and clathrin coats at Golgi membranes."),
 q("Secretory pathway", "medium", "Soluble ER-resident proteins that escape to the Golgi are returned by:",
   ["COPII anterograde vesicles", "COPI retrograde vesicles", "clathrin/AP2 vesicles", "regulated secretory vesicles"], "B",
   "Escaped ER proteins (recognised by the KDEL receptor) return to the ER in COPI-coated retrograde vesicles."),
 q("Exocytosis", "medium", "Which statement about the regulated secretory pathway is correct?",
   ["it operates continuously in all cells", "it stores products until a signal arrives", "it carries escaped ER proteins back", "it supplies most new plasma membrane lipid"], "B",
   "Regulated secretion occurs in specialised cells that store hormones, neurotransmitters or enzymes in vesicles until an extracellular signal triggers fusion."),
 q("Endosomes", "medium", "As an early endosome matures into a late endosome, it:",
   ["moves to the periphery and increases recycling", "moves toward the nucleus and stops recycling", "acquires a COPII coat and fuses with the ER", "becomes a secretory vesicle for exocytosis"], "B",
   "The early endosome travels inward on microtubules, changes membrane composition, stops recycling to the surface and commits contents to degradation."),
 # hard
 q("Rabs and SNAREs", "hard", "Which event directly catalyses fusion of the vesicle and target bilayers?",
   ["Rab-GTP binding a Rab effector", "formation of a trans-SNARE complex", "Rab-GAP stimulating GTP hydrolysis", "Sar1 inserting its amphiphilic helix"], "B",
   "Rab–effector binding tethers and docks; the zipped trans-SNARE complex pulls the bilayers within <1.5 nm so lipids merge. Rab-GAP acts afterwards to reset Rab."),
 q("Vesicle formation", "hard", "Why are outer coat proteins lost soon after a vesicle buds?",
   ["fusion requires close membrane contact", "coats would be degraded in the lumen", "uncoating releases the cargo inside", "coats would block dynamin from binding"], "A",
   "Fusion with the target's cytosolic face requires the two membranes to interact very closely, which a coat lattice would prevent."),
 q("Action potential", "hard", "An action potential always travels away from its initiation site because:",
   ["K+ channels ahead of it are closed", "Na+ channels behind it are inactivated", "the Na+/K+ pump only works forwards", "myelin blocks current spreading backwards"], "B",
   "Depolarising current spreads both ways, but Na+ channels just behind the active region are inactivated and cannot reopen, so only forward membrane fires."),
 q("Golgi processing", "hard", "Phosphorylation of oligosaccharides on lysosomal proteins occurs in the:",
   ["trans Golgi network", "medial cisterna", "cis Golgi network", "trans cisterna"], "C",
   "The cis Golgi network phosphorylates lysosomal oligosaccharides (the mannose-6-phosphate tag); galactose/NANA addition is trans, sulfation is in the trans Golgi network."),
 q("Coat table", "hard", "Clathrin with AP2 adaptor complexes mediates transport from:",
   ["trans-Golgi to endosome", "plasma membrane to endosome", "cis-Golgi to ER", "Golgi to lysosome and melanosome"], "B",
   "AP2 + clathrin act at the plasma membrane (endocytosis, e.g. LDL); AP1 and GGA act at the trans-Golgi; AP3 serves lysosomes/melanosomes/platelet vesicles."),
 q("LDL endocytosis", "hard", "In LDL uptake, what causes the receptor to release its LDL particle?",
   ["the neutral pH of the cell surface", "the acidic pH of the late endosome", "GTP hydrolysis by dynamin", "binding of the AP2 adaptor"], "B",
   "Acidification (~pH 5) in the late endosome dissociates LDL from its receptor; at neutral pH after recycling the binding arm is free to bind another LDL."),
 q("Membrane potential", "hard", "At the resting potential, the net driving force on K+ is near zero because:",
   ["K+ concentrations are equal on both sides", "the electrical pull inward balances chemical efflux", "K+ leak channels are all closed at rest", "the Na+/K+ pump exactly cancels K+ influx"], "B",
   "K+ is 140 mM inside vs 5 mM outside, so it tends to leave, but the inside-negative potential pulls it back; the two forces nearly cancel."),
 q("Membrane turnover", "hard", "A cell internalises membrane by pinocytosis at a high rate yet its surface area is unchanged. This is best explained by:",
   ["endocytosed membrane being degraded in lysosomes", "equal membrane being added back by exocytosis", "new lipid being synthesised at the plasma membrane", "pinocytic vesicles never fully pinching off"], "B",
   "Endocytosis and exocytosis are coupled: the same amount of membrane removed is returned, particularly tightly in high-turnover cells such as nerve terminals."),
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
