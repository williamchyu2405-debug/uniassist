#!/usr/bin/env python3
"""MHHS2402 Wk12 · Fluid, electrolyte & acid-base balance — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "fluid_electrolyte_acid_base_mhhs2402_wk12.html"
META = {
    "title": "Fluid, Electrolyte & Acid-Base Balance",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "unit": "MHHS2402",
    "content": ("Fluid, electrolyte and acid-base balance (MHHS2402 Wk12, A/Prof Mark Butlin): body water compartments and "
                "balance; vasopressin and the countercurrent multiplier; sodium balance, ECF volume and RAAS; thirst and "
                "salt appetite; potassium homeostasis and aldosterone; the bicarbonate buffer, respiratory and renal "
                "compensation, intercalated cells; and arterial blood gas classification with the tic-tac-toe method."),
}

Q = [
 # easy
 q("Compartments", "easy", "About what fraction of total body water is intracellular?",
   ["two-thirds", "one-quarter", "one-twelfth", "one-half"], "A",
   "Intracellular ⅔ (~25 L), interstitial ¼ (~10 L), plasma 1/12 (~3 L) in a 70 kg person."),
 q("Insensible loss", "easy", "Insensible water loss occurs through the:",
   ["skin and lungs", "kidneys and gut", "skin and kidneys", "lungs and gut"], "A",
   "Evaporation from skin and humidified expired air are losses we are not normally aware of."),
 q("Vasopressin", "easy", "Vasopressin increases water reabsorption by inserting which channels?",
   ["aquaporin-2", "ENaC sodium channels", "aquaporin-1", "ROMK potassium channels"], "A",
   "Vasopressin, via cAMP, inserts AQP2 into the apical membrane of collecting-duct cells."),
 q("Normal pH", "easy", "The normal range of arterial pH is:",
   ["7.35–7.45", "7.00–7.20", "7.45–7.55", "6.80–7.00"], "A",
   "Below 7.35 is acidosis, above 7.45 is alkalosis."),
 q("Buffer", "easy", "The predominant extracellular buffer system is the:",
   ["bicarbonate system", "phosphate system", "haemoglobin system", "ammonia system"], "A",
   "CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻ is the main ECF buffer."),
 # medium
 q("Kidney and water", "medium", "Which statement about the kidney and water balance is correct?",
   ["it can reduce water loss but not add water", "it can add water to the plasma from urine", "it stops producing any urine in dehydration", "it adds water by secreting it into the blood"], "A",
   "The kidney only conserves; restoring lost water requires drinking."),
 q("Vasopressin triggers", "medium", "Which change would NOT stimulate vasopressin release?",
   ["low plasma osmolarity", "falling blood pressure", "reduced atrial stretch", "high plasma osmolarity"], "A",
   "Low BP (baroreceptors), low atrial stretch and high osmolarity (osmoreceptors) all trigger release; low osmolarity suppresses it."),
 q("Descending limb", "medium", "The descending limb of the loop of Henle is:",
   ["water-permeable without ion transport", "water-impermeable with ion transport", "permeable to both water and ions", "impermeable to both water and ions"], "A",
   "Water leaves the descending limb into the salty medulla; the ascending limb pumps ions but holds water in."),
 q("Ascending limb", "medium", "Filtrate leaving the top of the ascending limb is typically:",
   ["hypo-osmotic, near 100 mOsm", "hyper-osmotic, near 1200 mOsm", "iso-osmotic, near 300 mOsm", "hyper-osmotic, near 600 mOsm"], "A",
   "Pumping out NaCl without water makes the ascending-limb fluid dilute."),
 q("Salt calculation", "medium", "Keeping 155 mOsm of ingested Na⁺ at 140 mOsm/L would need roughly:",
   ["1.1 L of water", "0.9 L of water", "11 L of water", "2.2 L of water"], "A",
   "155 ÷ 140 ≈ 1.1 L, which must be held in the extracellular fluid."),
 q("Renin source", "medium", "Renin is secreted mainly by:",
   ["juxtaglomerular cells of afferent arterioles", "macula densa cells of the distal tubule", "the adrenal cortex zona glomerulosa", "endothelial cells of the lung"], "A",
   "Juxtaglomerular (granular) cells in the afferent arteriole wall release renin."),
 q("Aldosterone", "medium", "Aldosterone acts on the distal nephron to:",
   ["reabsorb Na⁺ and secrete K⁺", "reabsorb K⁺ and secrete Na⁺", "insert aquaporin-2 channels", "secrete HCO₃⁻ into the lumen"], "A",
   "Aldosterone raises Na⁺-K⁺-ATPase activity, so Na⁺ is retained (water follows) and K⁺ is secreted."),
 q("Thirst", "medium", "Drinking relieves thirst before plasma osmolarity falls because:",
   ["mouth and pharynx receptors detect fluid", "hypothalamic osmoreceptors respond within seconds", "the stomach wall releases extra vasopressin", "arterial baroreceptors sense the increased volume"], "A",
   "Oropharyngeal receptors sensing cool fluid switch off thirst early; ice chips exploit this."),
 q("Potassium", "medium", "Normal renal clearance of K⁺ is approximately:",
   ["10–20%", "50–60%", "1–2%", "90–100%"], "A",
   "At normal levels more K⁺ is filtered and secreted than reabsorbed, giving clearance around 10–20%."),
 q("Hyperkalaemia", "medium", "Hyperkalaemia is corrected partly because high K⁺ directly stimulates:",
   ["aldosterone release from the adrenal cortex", "vasopressin release from the pituitary", "renin release from the kidney", "natriuretic peptide release from the heart"], "A",
   "High plasma K⁺ acts on the adrenal cortex; aldosterone then increases distal K⁺ secretion."),
 q("Respiratory compensation", "medium", "If blood tends toward acidosis, chemoreceptors drive:",
   ["hyperventilation to lower PCO₂", "hypoventilation to raise PCO₂", "hyperventilation to raise PCO₂", "hypoventilation to lower PCO₂"], "A",
   "Blowing off CO₂ pulls the bicarbonate reaction left and lowers H⁺."),
 q("Tubule buffer", "medium", "Secreted H⁺ in the tubule lumen is buffered mainly by filtered:",
   ["phosphate", "albumin", "glucose", "chloride"], "A",
   "HPO₄²⁻ + H⁺ → H₂PO₄⁻, which is excreted, carrying acid out without dropping urine pH too far."),
 # hard
 q("Lactic acid", "hard", "Adding lactic acid to blood shifts the bicarbonate reaction so that:",
   ["H⁺ rises and HCO₃⁻ falls", "H⁺ rises and HCO₃⁻ rises", "H⁺ falls and HCO₃⁻ rises", "H⁺ falls and HCO₃⁻ falls"], "A",
   "Extra H⁺ drives the reaction left, consuming HCO₃⁻ and producing CO₂."),
 q("Hypoventilation", "hard", "Primary hypoventilation changes PCO₂, pH and HCO₃⁻ as follows:",
   ["PCO₂ up, pH down, HCO₃⁻ up", "PCO₂ up, pH down, HCO₃⁻ down", "PCO₂ down, pH up, HCO₃⁻ down", "PCO₂ normal, pH down, HCO₃⁻ down"], "A",
   "Retained CO₂ pushes the reaction right, raising both H⁺ and HCO₃⁻: respiratory acidosis."),
 q("Proximal HCO₃⁻", "hard", "In the proximal tubule, filtered HCO₃⁻ is reclaimed because it:",
   ["is converted to CO₂ that enters the cell", "is carried directly across by an apical symporter", "diffuses through the tight junctions unchanged", "is secreted back into blood by type B cells"], "A",
   "Secreted H⁺ combines with filtered HCO₃⁻ to form CO₂, which enters the cell and is rebuilt into HCO₃⁻."),
 q("New bicarbonate", "hard", "New HCO₃⁻ generated by the proximal tubule comes from metabolism of:",
   ["glutamine", "glucose", "urea", "creatinine"], "A",
   "Glutamine → α-ketoglutarate → HCO₃⁻, with NH₄⁺ excreted in urine."),
 q("Intercalated cells", "hard", "Type A intercalated cells compensate for acidosis by:",
   ["secreting H⁺ and reabsorbing HCO₃⁻", "reabsorbing H⁺ and secreting HCO₃⁻", "secreting both H⁺ and HCO₃⁻", "reabsorbing both H⁺ and HCO₃⁻"], "A",
   "Type A secrete H⁺ and reabsorb HCO₃⁻; type B do the opposite for alkalosis."),
 q("ABG 1", "hard", "pH 7.50, PCO₂ 25 mmHg, HCO₃⁻ 19 mEq/L is best classified as:",
   ["respiratory alkalosis, partially compensated", "metabolic alkalosis, uncompensated", "respiratory alkalosis, uncompensated", "metabolic acidosis, fully compensated"], "A",
   "pH and low PCO₂ both sit in the alkalosis column; low HCO₃⁻ is in the opposite column with pH still abnormal."),
 q("ABG 2", "hard", "pH 7.47, PCO₂ 43 mmHg, HCO₃⁻ 32 mEq/L is best classified as:",
   ["metabolic alkalosis, uncompensated", "respiratory alkalosis, partially compensated", "metabolic alkalosis, partially compensated", "respiratory acidosis, fully compensated"], "A",
   "pH and high HCO₃⁻ are in the alkalosis column; PCO₂ is normal, so there is no compensation."),
 q("ABG 3", "hard", "pH 7.37, PCO₂ 27 mmHg, HCO₃⁻ 19 mEq/L is best classified as:",
   ["metabolic acidosis, fully compensated", "respiratory alkalosis, fully compensated", "metabolic acidosis, partially compensated", "respiratory acidosis, uncompensated"], "A",
   "pH is normal but leans acidotic (below 7.40), matching low HCO₃⁻; full respiratory compensation lowered PCO₂."),
 q("Metabolic alkalosis", "hard", "Which is a typical cause of metabolic alkalosis?",
   ["prolonged vomiting", "diabetic ketoacidosis", "severe diarrhoea", "opioid overdose"], "A",
   "Vomiting loses gastric H⁺; ketoacidosis and diarrhoea cause metabolic acidosis; opioid overdose causes respiratory acidosis."),
 q("Neurological effects", "hard", "Alkalosis tends to make neurons:",
   ["hyperexcitable, risking tetany", "less excitable, causing CNS depression", "unresponsive to neurotransmitters", "dependent on anaerobic metabolism"], "A",
   "Alkalosis increases excitability (tingling, tetany); acidosis depresses the CNS."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
