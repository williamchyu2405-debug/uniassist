#!/usr/bin/env python3
"""MHHS2402 Wk11 · Renal filtration & reabsorption — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "renal_filtration_reabsorption_mhhs2402_wk11.html"
META = {
    "title": "Renal Filtration & Reabsorption",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "unit": "MHHS2402",
    "content": ("Renal filtration and reabsorption (MHHS2402 Wk11, A/Prof Mark Butlin): filtration, reabsorption and "
                "secretion; the glomerular filtration barrier; Starling forces and GFR; autoregulation by the myogenic "
                "response and tubuloglomerular feedback; tubular reabsorption, transport maximum and the renal threshold; "
                "tubular secretion; and renal clearance (inulin, glucose, urea, PAH)."),
}

Q = [
 # easy
 q("Three processes", "easy", "Filtration in the nephron occurs only at the:",
   ["renal corpuscle", "proximal tubule", "loop of Henle", "collecting duct"], "A",
   "Filtration happens at the glomerulus and Bowman's capsule; reabsorption and secretion occur along the tubule."),
 q("Daily volumes", "easy", "Roughly how much plasma is filtered, and how much urine excreted, per day?",
   ["180 L filtered, 1.5 L excreted", "18 L filtered, 1.5 L excreted", "180 L filtered, 15 L excreted", "1.5 L filtered, 180 mL excreted"], "A",
   "About 180 L of filtrate forms daily and only ~1.5 L leaves as urine, so over 99% is reabsorbed."),
 q("Secretion", "easy", "Tubular secretion moves substances from:",
   ["peritubular blood into the lumen", "the lumen into peritubular blood", "Bowman's space into the glomerulus", "the interstitium into the vasa recta"], "A",
   "Secretion is blood → lumen, the opposite direction to reabsorption."),
 q("Inulin", "easy", "Inulin clearance is used as the gold standard for measuring:",
   ["glomerular filtration rate", "renal plasma flow", "tubular secretion rate", "urine concentrating ability"], "A",
   "Inulin is freely filtered and neither reabsorbed nor secreted, so its clearance equals GFR."),
 q("Barrier layers", "easy", "Which is NOT a layer of the glomerular filtration barrier?",
   ["the macula densa", "the fenestrated endothelium", "the basement membrane", "the podocyte filtration slits"], "A",
   "The barrier is endothelium, basement membrane and podocyte foot processes; the macula densa is part of the distal tubule."),
 # medium
 q("Size selectivity", "medium", "Which substance is essentially excluded from the glomerular filtrate?",
   ["albumin", "inulin", "glucose", "myoglobin"], "A",
   "Filtration falls with size: glucose and inulin pass freely, myoglobin (17 kDa) partly, albumin (69 kDa) is essentially excluded."),
 q("Charge barrier", "medium", "Albumin is held back partly because the basement membrane is:",
   ["negatively charged, repelling anionic albumin", "positively charged, binding albumin tightly", "uncharged but thicker than albumin", "negatively charged, attracting albumin"], "A",
   "The negative charge of the basement membrane repels negatively charged albumin; losing it causes proteinuria."),
 q("Starling forces", "medium", "Which force OPPOSES filtration at the glomerulus?",
   ["glomerular oncotic pressure", "glomerular capillary pressure", "Bowman's space oncotic pressure", "afferent arteriolar dilation"], "A",
   "GFR = Kf × (PG + πB − PB − πG); glomerular oncotic pressure (πG) and Bowman's hydrostatic pressure (PB) oppose filtration."),
 q("Net filtration pressure", "medium", "With PG ≈ 60, PB ≈ 18, πG ≈ 32 and πB ≈ 0 mmHg, net filtration pressure is about:",
   ["10 mmHg", "42 mmHg", "28 mmHg", "110 mmHg"], "A",
   "60 + 0 − 18 − 32 = 10 mmHg outward."),
 q("Arteriolar tone", "medium", "Constricting the efferent arteriole (moderately) will:",
   ["raise PG and raise GFR", "lower PG and lower GFR", "raise PG and lower GFR", "lower PG and raise GFR"], "A",
   "Efferent constriction backs blood up in the glomerulus, raising PG and GFR; afferent constriction lowers both."),
 q("Obstruction", "medium", "A ureteric stone causing back-pressure lowers GFR mainly by raising:",
   ["Bowman's space hydrostatic pressure", "glomerular capillary pressure", "glomerular oncotic pressure", "the filtration coefficient"], "A",
   "Obstruction raises PB, which opposes filtration."),
 q("Autoregulation range", "medium", "GFR is autoregulated over a mean arterial pressure of roughly:",
   ["80–180 mmHg", "40–80 mmHg", "120–240 mmHg", "60–100 mmHg"], "A",
   "Myogenic and tubuloglomerular mechanisms hold GFR steady across MAP ~80–180 mmHg."),
 q("Myogenic response", "medium", "In the myogenic response, raised arterial pressure causes the afferent arteriole to:",
   ["constrict, keeping glomerular pressure steady", "dilate, increasing glomerular pressure", "constrict, raising GFR further", "dilate, lowering renin release"], "A",
   "Stretch triggers afferent smooth-muscle contraction, protecting glomerular pressure and GFR."),
 q("TGF", "medium", "In tubuloglomerular feedback, the macula densa senses:",
   ["NaCl delivery to the distal tubule", "pressure in the afferent arteriole", "glucose in the proximal tubule", "oncotic pressure in Bowman's space"], "A",
   "Macula densa cells sense distal NaCl as a proxy for flow; high delivery triggers afferent constriction."),
 q("Reabsorption driver", "medium", "The primary driving force for tubular reabsorption is:",
   ["active Na+ transport by Na+/K+-ATPase", "passive water diffusion from the lumen", "active glucose pumping by SGLT", "secretion of H+ into the lumen"], "A",
   "Basolateral Na+/K+-ATPase creates the Na+ gradient that powers apical symport, antiport, and the osmotic movement of water."),
 q("Peritubular capillaries", "medium", "Peritubular capillaries favour reabsorption because they have:",
   ["low hydrostatic, high oncotic pressure", "high hydrostatic, low oncotic pressure", "high hydrostatic, high oncotic pressure", "low hydrostatic, low oncotic pressure"], "A",
   "After the efferent arteriole, pressure is low and plasma proteins are concentrated, so Starling forces pull fluid in."),
 q("Secretion", "medium", "Which substances are classically secreted by the tubule?",
   ["K+, H+ and many drugs", "glucose and most amino acids", "albumin and other plasma proteins", "intact red cells and platelets"], "A",
   "Secretion regulates K+ and H+ and clears organic compounds such as drugs; glucose and amino acids are reabsorbed."),
 # hard
 q("Biphasic efferent effect", "hard", "Why does strong, sustained efferent constriction eventually LOWER GFR?",
   ["renal blood flow falls and πG rises", "Bowman's space hydrostatic pressure falls to zero", "the filtration coefficient increases very sharply", "afferent arteriolar pressure rises above 180 mmHg"], "A",
   "Severe efferent constriction cuts renal plasma flow, so more plasma is filtered per pass, πG climbs and filtration falls."),
 q("ACE inhibitors", "hard", "ACE inhibitors can lower GFR in renal artery stenosis because they:",
   ["remove angiotensin II efferent constriction", "constrict the afferent arteriole directly", "raise Bowman's space pressure", "increase glomerular oncotic pressure"], "A",
   "Angiotensin II preferentially constricts the efferent arteriole, propping up PG when perfusion is low; blocking it drops GFR."),
 q("NSAIDs", "hard", "NSAIDs can precipitate a fall in GFR mainly by:",
   ["blocking vasodilator prostaglandins", "blocking angiotensin II production", "increasing nitric oxide release", "raising tubular Na+ reabsorption"], "A",
   "Prostaglandins dilate the afferent arteriole to protect GFR when perfusion is stressed; NSAIDs remove that protection."),
 q("Sympathetic effect", "hard", "Intense sympathetic stimulation in shock affects the kidney by:",
   ["constricting arterioles and lowering GFR", "dilating afferent arterioles and raising GFR", "constricting only the efferent arteriole", "leaving GFR unchanged by autoregulation"], "A",
   "Sympathetic drive constricts afferent and efferent arterioles, reducing GFR to preserve volume — a cause of pre-renal AKI."),
 q("Transport maximum", "hard", "Glycosuria in uncontrolled diabetes occurs because:",
   ["filtered glucose exceeds the transport maximum", "glucose is actively secreted by the tubule", "the filtration barrier admits more glucose", "SGLT transporters are destroyed by insulin"], "A",
   "Above the renal threshold (~300 mg/100 mL), carriers saturate (Tm) and excess glucose spills into urine."),
 q("Drug interaction", "hard", "Probenecid prolongs penicillin levels because it:",
   ["competes for the organic anion transporter", "increases penicillin reabsorption by SGLT", "blocks glomerular filtration of penicillin", "binds penicillin in plasma protein"], "A",
   "Both are secreted by the broadly specific OAT; probenecid competitively reduces penicillin secretion."),
 q("Clearance", "hard", "A substance with clearance greater than GFR must undergo net:",
   ["secretion", "reabsorption", "filtration only", "metabolism in the tubule"], "A",
   "Clearance above GFR means more is excreted than filtered, so the tubule is secreting it (e.g. PAH, penicillin)."),
 q("Clearance calculation", "hard", "Inulin is excreted at 4 mg/min with plasma inulin 0.04 mg/mL. GFR is:",
   ["100 mL/min", "10 mL/min", "160 mL/min", "1 000 mL/min"], "A",
   "Clearance = excretion rate ÷ plasma concentration = 4 ÷ 0.04 = 100 mL/min, which equals GFR for inulin."),
 q("Urea", "hard", "Urea clearance is about 50 mL/min while GFR is 100 mL/min. This shows urea is:",
   ["filtered then partly reabsorbed", "filtered then actively secreted", "neither filtered nor reabsorbed", "completely reabsorbed like glucose"], "A",
   "Clearance below GFR but above zero indicates partial net reabsorption."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
