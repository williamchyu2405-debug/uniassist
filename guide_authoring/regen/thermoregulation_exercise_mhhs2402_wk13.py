#!/usr/bin/env python3
"""MHHS2402 Wk13 · Thermoregulation & exercise — gallery quiz bank."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qbank_write import q, write_bank  # noqa

KEY = "thermoregulation_exercise_mhhs2402_wk13.html"
META = {
    "title": "Thermoregulation & Exercise",
    "subject": "Cardiovascular, Renal & Respiratory Systems",
    "unit": "MHHS2402",
    "content": ("Cardiorespiratory system in thermoregulation and exercise (MHHS2402 Wk13, A/Prof Mark Butlin): normal body "
                "temperature; the heat balance equation and evaporation, conduction, convection and radiation; thermoreceptors, "
                "afferent pathways and the hypothalamus; effectors (skin blood flow, sweating, shivering, piloerection, brown fat); "
                "the three muscle metabolic systems; the Fick principle; VO2max and its limits; and cardiorespiratory responses "
                "to exercise including baroreceptor resetting."),
}

Q = [
 # easy
 q("Core temperature", "easy", "Core body temperature is normally held within about:",
   ["±0.6 °C", "±2.0 °C", "±4.0 °C", "±0.1 °C"], "A",
   "Core (deep tissue) temperature is very constant, within roughly ±0.6 °C."),
 q("Heat loss route", "easy", "At rest in a normal room, the largest share of heat is lost by:",
   ["radiation", "evaporation", "conduction to air", "conduction to objects"], "A",
   "Radiation ~60%, evaporation ~22%, conduction to air ~15%, conduction to objects ~3%."),
 q("Sweat glands", "easy", "Which effector exists only to LOWER body temperature?",
   ["sweat glands", "skin blood vessels", "brown adipose tissue", "arrector pili muscles"], "A",
   "Sweat glands only cool; skin vessels work both ways; brown fat and piloerection only warm."),
 q("Fastest system", "easy", "The fastest but most limited muscle energy system is the:",
   ["phosphocreatine–creatine system", "glycogen–lactic acid system", "aerobic oxidative system", "fatty-acid oxidation system"], "A",
   "Phosphocreatine yields ~4 mol ATP/min but runs out within seconds."),
 q("Fick", "easy", "The Fick principle relates oxygen consumption to cardiac output and the:",
   ["arteriovenous O₂ difference", "alveolar CO₂ concentration", "haemoglobin dissociation curve", "respiratory exchange ratio"], "A",
   "V̇O₂ = Q̇ × ([O₂]arterial − [O₂]venous)."),
 # medium
 q("Danger thresholds", "medium", "Core temperatures below about 30 °C characteristically cause:",
   ["arrhythmia and cardiac arrest", "protein denaturation and death", "amnesia without cardiac effects", "febrile seizures in children"], "A",
   "Below 30 °C the heart becomes arrhythmic and may arrest; above 41 °C proteins denature."),
 q("Evaporation", "medium", "Evaporative cooling is least effective when the air is:",
   ["hot and humid", "hot and dry", "cool and windy", "cool and dry"], "A",
   "High humidity prevents sweat from evaporating, removing the main cooling route."),
 q("Convection", "medium", "Wind increases heat loss mainly by:",
   ["replacing the warm air layer next to skin", "increasing the radiant heat arriving from the sun", "raising the thermal conductivity of the skin itself", "reducing the amount of sweat the skin produces"], "A",
   "Convection removes the warmed boundary layer, keeping a steep temperature gradient."),
 q("Conduction", "medium", "Immersion in cold water chills faster than cold air because water has a higher:",
   ["thermal conductivity", "relative humidity", "radiant emissivity", "evaporation rate"], "A",
   "Q̇ = −kAΔT/d; water's thermal conductivity k is far higher than air's."),
 q("Central thermoreceptors", "medium", "Most central thermoreceptors in the preoptic hypothalamus are:",
   ["warm-sensitive neurons", "cold-sensitive neurons", "pain-sensitive neurons", "pressure-sensitive neurons"], "A",
   "Most central receptors increase firing 2–10-fold as core temperature rises."),
 q("Peripheral thermoreceptors", "medium", "Most peripheral (skin) thermoreceptors are:",
   ["cold-sensitive, with thin myelinated fibres", "warm-sensitive, with thin myelinated fibres", "cold-sensitive, with unmyelinated fibres", "warm-sensitive, with thick myelinated fibres"], "A",
   "Skin receptors are mostly cold-sensitive (fast thin myelinated fibres); warm receptors use unmyelinated fibres."),
 q("Pathways", "medium", "The ascending pathway that drives thermoregulatory responses is the:",
   ["spino-reticulo-hypothalamic pathway", "spino-thalamo-cortical pathway", "dorsal column–medial lemniscus", "corticospinal pathway"], "A",
   "It relays via the lateral parabrachial nucleus to the median preoptic nucleus; the spino-thalamo-cortical pathway gives conscious sensation."),
 q("Skin vasodilation", "medium", "Early cutaneous vasodilation in heat is mainly due to:",
   ["withdrawal of noradrenergic vasoconstriction", "cholinergic sympathetic active dilation", "release of adrenaline from the adrenal", "local metabolite accumulation in skin"], "A",
   "It begins passively by removing sympathetic constrictor tone; active cholinergic dilation follows as core temperature climbs."),
 q("Shivering", "medium", "Shivering can raise metabolic rate by about:",
   ["3-fold", "10-fold", "1.2-fold", "30-fold"], "A",
   "Oscillating skeletal muscle contraction can roughly triple metabolic rate."),
 q("Brown fat", "medium", "Brown adipose tissue is most abundant in:",
   ["newborns", "healthy adults", "older adults", "obese adults"], "A",
   "Newborn > healthy adult > obesity and older adults."),
 q("Aerobic system", "medium", "Which statement about the aerobic system is correct?",
   ["it is slow but has unlimited capacity", "it is fast but has limited capacity", "it uses only stored phosphagens", "it produces lactate as its end product"], "A",
   "Aerobic oxidation yields ~1 mol ATP/min but can continue as long as fuel and O₂ last."),
 q("VO₂max limit", "medium", "In a healthy person, VO₂max is usually limited mainly by:",
   ["maximum cardiac output", "maximum minute ventilation", "alveolar diffusion capacity", "haemoglobin saturation"], "A",
   "Ventilation has spare capacity (100–110 vs 150–160 L/min); maximal cardiac output sets the ceiling."),
 # hard
 q("Fick calculation", "hard", "O₂ use is 200 mL/min, arterial O₂ 200 mL/L and venous O₂ 160 mL/L. Cardiac output is:",
   ["5 L/min", "4 L/min", "8 L/min", "1.25 L/min"], "A",
   "Q̇ = 200 ÷ (200 − 160) = 200 ÷ 40 = 5 L/min."),
 q("Extraction", "hard", "A marathoner has VO₂max 5.1 L/min and maximal cardiac output 30 L/min. The a−v O₂ difference is about:",
   ["170 mL/L", "40 mL/L", "60 mL/L", "510 mL/L"], "A",
   "5100 mL/min ÷ 30 L/min = 170 mL O₂ per litre of blood, about four times the resting value."),
 q("Athlete heart", "hard", "A marathoner's higher maximal cardiac output comes mainly from a higher:",
   ["stroke volume", "maximal heart rate", "resting heart rate", "haematocrit"], "A",
   "Max HR is similar (185 vs 195) but stroke volume is far larger (162 vs 110 mL)."),
 q("Resting athlete", "hard", "At rest, an endurance athlete compared with a non-athlete has:",
   ["higher stroke volume and lower heart rate", "lower stroke volume and higher heart rate", "higher cardiac output and higher heart rate", "lower cardiac output and lower stroke volume"], "A",
   "105 mL × 50 bpm vs 75 mL × 75 bpm: similar cardiac output, achieved differently."),
 q("Evaporation energy", "hard", "Evaporating 1 L of sweat removes approximately:",
   ["580 kcal", "58 kcal", "5 800 kcal", "0.58 kcal"], "A",
   "1000 g × 0.58 kcal/g = 580 kcal."),
 q("Blood flow redistribution", "hard", "From rest to strenuous exercise, skeletal muscle's share of cardiac output rises from about:",
   ["20% to 73%", "5% to 25%", "40% to 50%", "73% to 90%"], "A",
   "Muscle flow rises from 1030 mL/min (20%) to 12 500 mL/min (73%) as cardiac output goes from 5.0 to 17.5 L/min."),
 q("Sympathetic paradox", "hard", "Exercise raises sympathetic outflow, yet muscle vessels dilate because:",
   ["local metabolites override sympathetic tone", "muscle vessels lack all innervation", "adrenaline constricts muscle arterioles", "baroreceptors suppress sympathetic drive"], "A",
   "Metabolite-driven autoregulation dominates, and muscle vessels are less sensitive to sympathetic activity."),
 q("Baroreceptor resetting", "hard", "During exercise the baroreceptor function curve shifts:",
   ["rightward and upward", "leftward and downward", "leftward only", "downward only"], "A",
   "Resetting lets pressure rise while the reflex still buffers moment-to-moment swings around a higher operating point."),
 q("Venous return", "hard", "During exercise, which mechanism returns blood to the heart by compressing deep veins?",
   ["the skeletal muscle pump", "the atrial Bainbridge reflex", "local metabolic vascular autoregulation", "arterial baroreceptor resetting"], "A",
   "Contracting muscles squeeze deep veins and valves direct blood toward the heart; the respiratory pump adds to this. Bainbridge raises heart rate in response to the extra return."),
 q("Fever", "hard", "In the simplified set-point model, a fever is best explained as:",
   ["the hypothalamic set point being raised", "failure of all the heat-loss mechanisms", "loss of the peripheral cold receptors", "excess activity of brown adipose tissue"], "A",
   "Pyrogens raise the set point, so the body conserves and makes heat until it reaches the new value."),
]

if __name__ == "__main__":
    write_bank(KEY, META, Q)
