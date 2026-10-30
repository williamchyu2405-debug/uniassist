#!/usr/bin/env python3
"""MEDI2200 W11 · Signalling pathways — NEW gallery bank (length-matched, no bracket tells, no daredevil).
New guide: META is defined inline and the entry is written straight into guide_quizzes.json
(assemble_bank.py only rewrites keys already present in the bank)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from qbank_lib import check_bank, summarize  # noqa

KEY = "signalling_pathways_medi2200_wk11.html"
META = {
    "title": "Signalling Pathways",
    "subject": "Human Cell & Molecular Biology",
    "unit": "MEDI2200",
    "content": ("Signalling pathways (MEDI2200 Wk11, Dr Esther Lim): why cells signal; contact-dependent, "
                "paracrine, synaptic and endocrine signalling; reception, transduction and response; receptor "
                "classes; second messengers; regulation by molecular switches (kinases/phosphatases, GEFs/GAPs), "
                "scaffolds, docking domains, feedback and adaptation; GPCR cAMP-PKA-CREB and PLC-IP3-DAG pathways; "
                "RTK activation, Grb2-Sos-Ras, Raf-MEK-ERK, PI3K-Akt-Bad; Wnt/beta-catenin."),
}

def q(topic, diff, stem, opts, ans, expl):
    return {"topic": topic, "difficulty": diff, "question": stem,
            "options": [f"{'ABCD'[i]}. {o}" for i, o in enumerate(opts)],
            "correct_answer": ans, "explanation": expl, "related": [topic]}

Q = [
 # easy
 q("Types of signalling", "easy", "Hormones released into the blood to act on distant cells is:",
   ["paracrine signalling", "endocrine signalling", "synaptic signalling", "contact-dependent signalling"], "B",
   "Endocrine signalling sends hormones through the circulation to distant targets; paracrine acts locally, synaptic across a synapse, contact-dependent by touch."),
 q("Steps", "easy", "The step in which intracellular proteins relay the signal to effectors is:",
   ["reception", "transduction", "response", "adaptation"], "B",
   "Reception is ligand binding; transduction relays and amplifies inside the cell; response is the effector outcome."),
 q("Second messengers", "easy", "Which of these is NOT one of the lecture's second messengers?",
   ["cAMP", "IP3", "DAG", "ERK"], "D",
   "cAMP, Ca2+, IP3 and DAG are small second messengers; ERK is a protein kinase (MAPK) in the RTK cascade."),
 q("GPCR structure", "easy", "A G protein-coupled receptor crosses the membrane:",
   ["once", "four times", "seven times", "twelve times"], "C",
   "GPCRs are 7-transmembrane receptors."),
 q("MAPK cascade", "easy", "In the MAPK cascade, MEK is the:",
   ["MAPKKK", "MAPKK", "MAPK", "Ras-GEF"], "B",
   "Raf is MAPKKK, MEK is MAPKK, ERK is MAPK; Sos is the Ras-GEF."),
 q("Wnt", "easy", "Which protein is the transcriptional effector stabilised by Wnt signalling?",
   ["beta-catenin", "Dishevelled", "Axin", "GSK3"], "A",
   "Wnt stops the destruction complex (Axin, APC, GSK3, CK1) degrading beta-catenin, which then enters the nucleus with LEF1/TCF."),
 # medium
 q("Reception", "medium", "A single receptor recognising two structurally similar ligands illustrates:",
   ["receptor redundancy", "receptor adaptation", "signal divergence", "negative feedback"], "A",
   "Redundancy means a receptor can recognise more than one ligand if the ligands are similar."),
 q("Receptor classes", "medium", "Which receptor class is typically used for rapid synaptic signalling?",
   ["G protein-coupled receptors", "receptor tyrosine kinases", "ion-channel-coupled receptors", "intracellular steroid receptors"], "C",
   "Ion-channel-coupled receptors open a pore directly on ligand binding, the fastest mechanism, used in synaptic signalling."),
 q("Switches", "medium", "A GTPase-activating protein (GAP) acts to:",
   ["promote GDP release and GTP binding", "promote hydrolysis of bound GTP", "phosphorylate the GTPase on tyrosine", "anchor the GTPase to the membrane"], "B",
   "GAPs switch GTPases off by promoting GTP hydrolysis; GEFs switch them on by promoting GDP-for-GTP exchange."),
 q("Switches", "medium", "A protein phosphatase regulates signalling by:",
   ["adding phosphate from ATP", "removing a phosphate group", "exchanging GDP for GTP", "cleaving PIP2 into two messengers"], "B",
   "Kinases add phosphate (on); phosphatases remove it (off)."),
 q("Location", "medium", "Proteins with interaction domains that hold signalling proteins together are:",
   ["scaffold proteins", "effector proteins", "second messengers", "adaptor ligands"], "A",
   "Scaffold proteins assemble signalling molecules at one location so the pathway can switch on."),
 q("Feedback", "medium", "Negative feedback in a signalling pathway mainly serves to:",
   ["prolong the duration of the response", "limit the intensity of the response", "amplify the initial signal", "create new docking sites"], "B",
   "Negative feedback limits intensity; positive feedback prolongs duration."),
 q("Adaptation", "medium", "Receptors endocytosed and destroyed in lysosomes after prolonged signal is:",
   ["receptor sequestration", "receptor down-regulation", "receptor inactivation", "positive feedback"], "B",
   "Down-regulation destroys receptors in lysosomes; sequestration holds them in endosomes for recycling; inactivation leaves them at the surface but blocked."),
 q("G protein", "medium", "When a ligand activates a GPCR, the G protein alpha subunit:",
   ["exchanges GDP for GTP and dissociates", "hydrolyses GTP and binds the receptor", "phosphorylates the beta-gamma subunits", "exchanges GTP for GDP and stays bound"], "A",
   "The activated receptor acts as a GEF: G-alpha releases GDP, binds GTP and separates from the complex to activate effectors."),
 q("cAMP pathway", "medium", "In the cAMP pathway, the enzyme directly activated by G-alpha is:",
   ["phospholipase C", "protein kinase A", "adenylyl cyclase", "PI 3-kinase"], "C",
   "Gs-alpha activates adenylyl cyclase, which converts ATP to cAMP; cAMP then activates PKA."),
 q("cAMP pathway", "medium", "Activated PKA promotes gene transcription by phosphorylating:",
   ["CREB in the nucleus", "LEF1/TCF in the nucleus", "ERK in the cytosol", "Bad in the cytosol"], "A",
   "PKA translocates to the nucleus and phosphorylates CREB, which binds the cAMP response element (CRE)."),
 q("PI pathway", "medium", "IP3 produced by phospholipase C acts by:",
   ["activating protein kinase C directly", "opening Ca2+ channels in the ER", "activating adenylyl cyclase at the membrane", "recruiting Akt via its PH domains"], "B",
   "IP3 binds IP3 receptors (Ca2+ channels) in the ER to release Ca2+; DAG is the product that activates PKC."),
 q("RTK activation", "medium", "The first event after a ligand binds receptor tyrosine kinases is:",
   ["receptor dimerisation", "Ras activation", "Grb2 recruitment", "ERK phosphorylation"], "A",
   "Ligand binding dimerises RTKs, bringing kinase domains together so they trans-phosphorylate tyrosines; docking and downstream steps follow."),
 q("Grb2", "medium", "Grb2 binds the activated receptor's phosphotyrosine through its:",
   ["SH3 domain", "PH domain", "SH2 domain", "kinase domain"], "C",
   "Grb2's SH2 domain binds phosphotyrosine; its SH3 domains bind Sos. PH domains bind PIP3 (Akt, PDK1)."),
 q("PI3K", "medium", "PI3K contributes to Akt activation by converting:",
   ["PIP3 into PIP2", "PIP2 into IP3 and DAG", "PIP2 into PIP3", "ATP into cAMP"], "C",
   "PI3K phosphorylates PIP2 to PIP3, which recruits Akt and PDK1 via PH domains; PLC (not PI3K) splits PIP2 into IP3 and DAG."),
 q("Wnt", "medium", "In the absence of Wnt, beta-catenin levels stay low because it is:",
   ["exported from the cell", "ubiquitinylated and degraded", "sequestered by Dishevelled", "bound by LEF1/TCF on DNA"], "B",
   "The active destruction complex phosphorylates beta-catenin, marking it for ubiquitinylation and proteasomal degradation."),
 # hard
 q("Docking", "hard", "One PDGF receptor activates PI3K, a Ras-GAP and PLC-gamma at once. This is best explained by:",
   ["distinct phosphotyrosine docking sites", "a single scaffold binding all three", "receptor sequestration in endosomes", "three receptor classes in one protein"], "A",
   "Different phosphorylated tyrosines (740/751, 771, 1009/1021) each recruit a different SH2-domain protein, so one receptor diverges to several pathways."),
 q("Ras", "hard", "After activation by Sos, active Ras-GTP:",
   ["stays bound to Sos at the receptor", "moves into the nucleus to bind DNA", "leaves Sos but stays at the membrane", "leaves the membrane and enters the cytosol"], "C",
   "Activated Ras dissociates from Sos but remains anchored to the cytoplasmic face of the plasma membrane."),
 q("Ras", "hard", "An oncogenic Ras mutation most likely makes Ras unable to:",
   ["bind GTP when Sos is present", "hydrolyse GTP when GAP binds", "associate with the plasma membrane", "be recognised by the Grb2 adaptor"], "B",
   "Oncogenic Ras is GAP-resistant, so it stays GTP-bound and permanently ON; a Ras unable to bind GTP would be inactive, not oncogenic."),
 q("Akt", "hard", "Akt is fully activated by phosphorylation from:",
   ["PDK1 and the mTOR complex", "PI3K and the RTK itself", "Raf and MEK in sequence", "PKA and PKC together"], "A",
   "PIP3 recruits Akt and PDK1 via PH domains; Akt is then phosphorylated by PDK1 and mTOR complex 2."),
 q("Akt", "hard", "Phosphorylation of Bad by Akt promotes cell survival because Bad then:",
   ["releases the apoptosis-inhibitory protein", "binds and activates caspases", "enters the nucleus as a transcription factor", "blocks PIP3 at the membrane"], "A",
   "Phospho-Bad (held by 14-3-3) releases the apoptosis-inhibitory protein, which then inhibits apoptosis."),
 q("PKC", "hard", "Full activation of protein kinase C in the PI pathway depends on:",
   ["IP3 alone", "DAG and Ca2+", "cAMP and Ca2+", "PIP3 and PDK1"], "B",
   "DAG (membrane) activates PKC and IP3-released Ca2+ also regulates it; both products of PIP2 cleavage contribute."),
 q("Wnt", "hard", "When Wnt binds, the destruction complex is disrupted because:",
   ["Dishevelled phosphorylates beta-catenin", "Axin binds phosphorylated LRP", "APC is degraded by the proteasome", "GSK3 enters the nucleus with TCF"], "B",
   "CK1 and GSK3 phosphorylate LRP; Axin binds phospho-LRP at the membrane, breaking up the complex so beta-catenin escapes degradation."),
 q("Response timing", "hard", "A signal causes an effect within seconds that needs no new protein synthesis. It most likely acts by:",
   ["changing gene transcription via CREB", "modifying existing protein activity", "stabilising beta-catenin in the nucleus", "inducing a negative-feedback inhibitor"], "B",
   "Altering function of existing proteins is fast (seconds to minutes); routes through gene expression take minutes to hours."),
 q("Adaptation", "hard", "Prolonged signal exposure that reduces the response mainly allows a cell to:",
   ["amplify the signal more strongly", "detect small changes in concentration", "switch the pathway permanently on", "respond to a wider range of ligands"], "B",
   "Adaptation resets sensitivity so the cell can still detect small changes in signal concentration against a high background."),
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
