#!/usr/bin/env python3
"""MHHS2402 Wk10 · Renal & urinary system anatomy — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "renal_urinary_anatomy_mhhs2402_wk10.html"
META = {
    "title": "Renal & Urinary System — Anatomy",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "unit": "MHHS2402",
    "content": ("Renal and urinary anatomy (MHHS2402 Wk10): kidney functions, position, hilum and coverings; "
                "internal drainage; ureters, bladder, sphincters and urethra; relations and surface anatomy; "
                "adrenal glands; renal blood supply; innervation, referred pain and micturition; development and "
                "anomalies; the nephron; and urine formation by filtration, reabsorption and secretion."),
}

Q = [
 # easy
 q("Kidney position", "easy", "The kidneys lie approximately between which vertebral levels?",
   ["T12 and L3", "T8 and T12", "L3 and S1", "T6 and L1"], "A",
   "The retroperitoneal kidneys span about T12 to L3, the right slightly lower than the left because of the liver."),
 q("Hilum", "easy", "From anterior to posterior, the structures at the renal hilum are:",
   ["vein, artery, ureter", "artery, vein, ureter", "ureter, artery, vein", "vein, ureter, artery"], "A",
   "Renal vein, renal artery, then ureter (pelvis) from front to back, remembered as VAU."),
 q("Sphincters", "easy", "The external urethral sphincter is best described as:",
   ["skeletal and voluntary, via the pudendal nerve", "smooth and involuntary, via hypogastric nerves", "smooth and voluntary, via pelvic splanchnics", "skeletal and involuntary, via the vagus nerve"], "A",
   "The external sphincter is skeletal muscle under voluntary control from the pudendal nerve (S2–S4); the internal sphincter is smooth and autonomic."),
 q("Adrenal cortex", "easy", "From outer to inner, the zones of the adrenal cortex are:",
   ["glomerulosa, fasciculata, reticularis", "fasciculata, glomerulosa, reticularis", "reticularis, fasciculata, glomerulosa", "glomerulosa, reticularis, fasciculata"], "A",
   "GFR: glomerulosa (aldosterone, salt), fasciculata (cortisol, sugar), reticularis (weak androgens, sex)."),
 q("Nephron types", "easy", "Which nephrons build the medullary osmotic gradient used to concentrate urine?",
   ["juxtamedullary nephrons with long loops", "cortical nephrons with short loops", "cortical nephrons without vasa recta", "juxtamedullary nephrons without loops"], "A",
   "Juxtamedullary nephrons (~15–20%) have long loops of Henle with vasa recta and generate the medullary gradient."),
 # medium
 q("Coverings", "medium", "From deep to superficial, the coverings of the kidney are:",
   ["capsule, perirenal fat, renal fascia, pararenal fat", "perirenal fat, capsule, pararenal fat, renal fascia", "capsule, pararenal fat, renal fascia, perirenal fat", "renal fascia, capsule, perirenal fat, pararenal fat"], "A",
   "Renal capsule, perirenal fat, renal (Gerota's) fascia, then pararenal fat."),
 q("Internal drainage", "medium", "Urine leaving a renal papilla drains next into a:",
   ["minor calyx", "major calyx", "renal column", "renal pelvis"], "A",
   "Pyramid → papilla → minor calyx → major calyx → renal pelvis → ureter. Renal columns are cortical tissue between pyramids."),
 q("Ureter constrictions", "medium", "Which is NOT one of the three classic sites where ureteric stones lodge?",
   ["the renal papilla", "the ureteropelvic junction", "crossing the pelvic brim", "the ureterovesical junction"], "A",
   "Stones impact at the ureteropelvic junction, at the pelvic brim over the iliac vessels, and at the ureterovesical junction."),
 q("Trigone", "medium", "The bladder trigone is bounded by:",
   ["two ureteric orifices and the internal urethral orifice", "two ureteric orifices and the external urethral orifice", "the internal and external urethral orifices and the apex", "the detrusor apex and both ureteric orifices"], "A",
   "The sensory-rich trigone lies between the two ureteric orifices and the internal urethral orifice."),
 q("Urethra", "medium", "Compared with the male urethra, the female urethra is:",
   ["about 4 cm and straight", "about 18 cm with four parts", "about 4 cm with a prostatic part", "about 10 cm and S-shaped"], "A",
   "The short straight female urethra (~4 cm) explains higher UTI rates; the male urethra is 18–20 cm with four parts."),
 q("Relations", "medium", "Which structure is an anterior relation of the LEFT kidney but not the right?",
   ["spleen", "liver", "duodenum", "psoas major"], "A",
   "Left kidney: stomach, spleen, pancreas, jejunum, left colic flexure. Right: liver, duodenum, right colic flexure. Psoas is a shared posterior relation."),
 q("Ureter course", "medium", "In 'water under the bridge', the ureter in a female passes:",
   ["inferior to the uterine artery", "superior to the uterine artery", "posterior to the internal iliac vein", "anterior to the round ligament"], "A",
   "The ureter (water) passes beneath the uterine artery (bridge), a key hazard when clamping in hysterectomy."),
 q("Adrenal medulla", "medium", "The adrenal medulla is best described as:",
   ["neural-crest tissue releasing catecholamines", "mesodermal tissue releasing aldosterone", "neural-crest tissue releasing cortisol", "mesodermal tissue releasing adrenaline"], "A",
   "The medulla is a modified sympathetic ganglion (neural crest) releasing adrenaline and noradrenaline; the cortex is mesodermal."),
 q("Vascular sequence", "medium", "Immediately before the afferent arteriole, blood flows through the:",
   ["interlobular artery", "arcuate artery", "interlobar artery", "segmental artery"], "A",
   "Renal → segmental → interlobar → arcuate → interlobular → afferent arteriole → glomerulus."),
 q("Renal vessels", "medium", "Which renal vessel is longer, and why?",
   ["left vein, crossing anterior to the aorta", "right vein, crossing anterior to the aorta", "left artery, crossing behind the IVC", "right vein, crossing behind the IVC"], "A",
   "The left renal vein crosses in front of the aorta to the IVC; the right renal artery is the longer artery, crossing behind the IVC."),
 q("Micturition", "medium", "During voiding, the detrusor contracts mainly through:",
   ["pelvic splanchnic nerves, S2–S4", "hypogastric nerves, T11–L2", "the pudendal nerve, S2–S4", "the vagus nerve"], "A",
   "Parasympathetic pelvic splanchnics contract the detrusor and relax the internal sphincter; sympathetic hypogastric nerves favour storage."),
 q("Development", "medium", "The ureteric bud gives rise to the:",
   ["collecting ducts, calyces, pelvis and ureter", "glomeruli and proximal tubules", "loops of Henle and distal tubules", "bladder trigone and urethra"], "A",
   "The ureteric bud forms the collecting system and induces the metanephric mesoderm to form nephrons."),
 # hard
 q("Nutcracker", "hard", "Compression of the left renal vein between the SMA and aorta most typically produces:",
   ["haematuria and a left varicocele", "right flank pain and oliguria", "hypertension from renin release", "a right-sided varicocele"], "A",
   "Nutcracker syndrome raises left renal venous pressure; the left gonadal vein drains into it, giving a left varicocele and haematuria."),
 q("Segmental arteries", "hard", "Segmental renal arteries matter surgically because they are:",
   ["end-arteries with no anastomoses", "richly anastomosing with each other", "branches of the arcuate arteries", "paired with segmental veins only"], "A",
   "Segmental arteries are end-arteries, so occluding one infarcts its segment; Brödel's line is the avascular plane between divisions."),
 q("Referred pain", "hard", "Ureteric colic is felt 'loin to groin' because ureteric afferents enter the cord at about:",
   ["T10–L2", "S2–S4", "T1–T4", "L4–S1"], "A",
   "Visceral afferents travel with the sympathetics (T10–L2), so pain is referred to those dermatomes, from loin to groin."),
 q("Horseshoe kidney", "hard", "A horseshoe kidney sits lower than normal because its ascent is blocked by the:",
   ["inferior mesenteric artery", "superior mesenteric artery", "common iliac arteries", "coeliac trunk"], "A",
   "The fused lower poles catch on the inferior mesenteric artery during ascent."),
 q("Posterior approach", "hard", "A posterior surgical approach to the upper pole of the kidney risks:",
   ["pneumothorax from pleural injury", "injury to the ureter at the brim", "splenic rupture from the front", "compression of the left renal vein"], "A",
   "The upper poles are related to the diaphragm and pleura, so a posterior approach can breach the pleura."),
 q("Two capillary beds", "hard", "The functional significance of the efferent arteriole leading to a second capillary bed is that it:",
   ["lets filtration be followed by reabsorption", "doubles the blood supply to the medulla", "prevents protein from entering the filtrate", "allows renin release into the glomerulus"], "A",
   "Glomerular capillaries filter; the downstream peritubular capillaries and vasa recta reabsorb, two beds in series."),
 q("Urine formation", "hard", "Which equation describes the amount of a substance excreted?",
   ["filtered − reabsorbed + secreted", "filtered + reabsorbed − secreted", "secreted − filtered + reabsorbed", "filtered − secreted − reabsorbed"], "A",
   "Excretion equals filtration minus reabsorption plus secretion."),
 q("Regulated reabsorption", "hard", "Hormone-regulated reabsorption mainly takes place in the:",
   ["distal tubule and collecting duct", "proximal tubule and loop of Henle", "glomerulus and Bowman's capsule", "proximal tubule and collecting duct"], "A",
   "Obligatory bulk reabsorption occurs in the PCT and loop; ADH and aldosterone act on the distal tubule and collecting duct."),
 q("Filtration barrier", "hard", "Proteinuria with haematuria suggests damage specifically to the:",
   ["glomerular filtration barrier", "proximal tubule brush border", "collecting duct aquaporins", "ureteric smooth muscle"], "A",
   "Albumin and cells are normally excluded by the three-layer glomerular barrier; their appearance signals glomerular injury."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
