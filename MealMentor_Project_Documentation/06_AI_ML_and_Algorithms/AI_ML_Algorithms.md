# MealMentor — AI, Machine Learning, and Algorithms Documentation

## Overview: What Types of AI/ML Are Used?

MealMentor uses the following categories, clearly distinguished:

| Category | Implementation | Purpose |
|----------|---------------|---------|
| Mathematical Formulas | Mifflin–St Jeor BMR, TDEE, calorie target | Nutrition target calculation |
| Rule-Based Algorithm | Gap-fill scoring with weights and penalties | Food candidate filtering and scoring |
| Trained ML Model (Supervised) | XGBoost Learning-to-Rank (XGBRanker) | Re-ranking food candidates |
| Trained ML Model (Supervised) | Random Forest Regression | 7-day weight change forecasting |
| External LLM (Cloud API) | Google Gemini (gemini-3.8-flash) | Food photo recognition, AI chatbot |
| Supporting Models | Ridge Regression (calorie), RandomForest (meal type), XGBoost (protein) | Experimental/supporting metrics |
| Database Lookup | Food dataset + barcode cache | Nutrition retrieval |

**Important**: All nutrition values used in recommendations are read from the food dataset. ML models do not generate or fabricate nutrition values — they only re-rank which foods are most suitable.

---

## Algorithm 1: BMR — Mifflin–St Jeor Equation

**Type**: Mathematical Formula

**Formula** (verified from `src/lib/nutrition.ts → calcBMR()`):
```
base = (10 × weightKg) + (6.25 × heightCm) - (5 × age)

Male:   BMR = base + 5
Female: BMR = base - 161
Other:  BMR = base   (neutral, no sex adjustment)
```

**Why Used**: The Mifflin–St Jeor equation is widely cited as one of the most accurate BMR estimation formulas for general adult populations.

**Example Dry Run**:
- Female, 22 years, 55 kg, 160 cm
- base = (10 × 55) + (6.25 × 160) - (5 × 22) = 550 + 1000 - 110 = 1440
- BMR = 1440 - 161 = **1279 kcal/day**

**Limitation**: The formula provides an estimate; actual BMR varies by body composition, metabolic rate, and genetics. It is not clinically validated for specific populations.

---

## Algorithm 2: TDEE — Activity Factor Multiplication

**Type**: Mathematical Formula

**Formula** (verified from `src/lib/nutrition.ts → calcTDEE()`):
```
TDEE = BMR × Activity Factor

Activity Factors (Harris-Benedict style):
  sedentary:   1.2
  light:       1.375
  moderate:    1.55
  active:      1.725
  very-active: 1.9
```

**Example Dry Run** (continuing from above):
- BMR = 1279, Activity Level = light (1.375)
- TDEE = 1279 × 1.375 = **1758.6 kcal/day**

---

## Algorithm 3: Calorie Target — Goal-Adjusted TDEE

**Formula** (verified from `src/lib/nutrition.ts → calcCalorieTarget()`):
```
Calorie Target = max(1200, round(TDEE + Goal Delta))

Goal Deltas:
  weight-loss:              -500 kcal
  weight-gain:              +500 kcal
  muscle-building:          +250 kcal
  maintain-weight:             0 kcal
  improve-energy:              0 kcal
  general-healthy-lifestyle:   0 kcal
```

**Example Dry Run** (continuing):
- TDEE = 1758.6, Goal = weight-loss
- Target = max(1200, round(1758.6 - 500)) = max(1200, 1259) = **1259 kcal/day**

---

## Algorithm 4: Nutrient Intake Calculation

**Type**: Mathematical Formula

**Formula** (verified from `src/lib/intake.ts → computeIntake()`):
```
Nutrient Consumed = (qtyG / 100) × nutrient_per_100g
```

This applies to all nutrients: calories, protein, carbs, fat, fiber, sugar, sodium, calcium, iron, vitamin C.

**Example Dry Run**:
- Food: Adai Aviyal (protein = 5.5g per 100g), Quantity = 200g
- Protein Consumed = (200 / 100) × 5.5 = **11.0g**

---

## Algorithm 5: Nutrient Gap Calculation

**Type**: Mathematical Formula

**Formula** (verified from `src/lib/gaps.ts → calcGaps()`):
```
Gap = max(0, Target - Consumed)
```

For upper-limit nutrients (sugar, sodium):
```
Remaining = max(0, Limit - Consumed)
```

**Example Dry Run**:
- Protein Target = 60g, Consumed = 22g
- Protein Gap = max(0, 60 - 22) = **38g**

---

## Algorithm 6: Adaptive Nutrient Weight Calculation

**Type**: Rule-Based Algorithm

**Formula** (verified from `src/lib/gaps.ts → calcNutrientWeights()`):
```
For each nutrient:
  gap_percentage = (gap / target) × 100

weight_i = gap_percentage_i / sum(all gap_percentages)
```

This means: nutrients with larger remaining gaps receive proportionally higher weights, directing recommendations toward the most deficient nutrients first.

---

## Algorithm 7: Rule-Based Food Scoring

**Type**: Rule-Based Algorithm

**Formula** (verified from `src/lib/recommend.ts → scoreFood()`):
```
For each gap nutrient (protein, fiber, calcium, iron, vitaminC):
  fill_i = clamp(0, 1, food_value_per_100g / gap_i)

nutrient_score = sum(weight_i × fill_i)  [for all 5 gap nutrients]

calorie_density = food.calories / gaps.calorieGap
calorie_penalty = (calorie_density - 0.5) × 0.4  [if calorie_density > 0.5]

sugar_ratio = food.sugarG / gaps.sugarRemaining
sugar_penalty = min(1, (sugar_ratio - 1) × 0.5)  [if sugar_ratio > 1]

sodium_ratio = food.sodiumMg / gaps.sodiumRemaining
sodium_penalty = min(1, (sodium_ratio - 1) × 0.5)  [if sodium_ratio > 1]

rejected = (sugar_ratio > 3 OR sodium_ratio > 3)

match = max(0, nutrient_score - calorie_penalty - sugar_penalty - sodium_penalty)
```

**Score Modifiers**:
- Favorite / liked food: +0.05 to final score
- Rejected food: -0.15 to final score
- Recent food (fallback): multiplicative discount up to 50%

---

## Algorithm 8: Serving Size Optimization

**Type**: Rule-Based Algorithm

**Formula** (verified from `src/lib/recommend.ts → pickServing()`):
```
For each gap nutrient, compute a candidate serving size:
  servingG = (gap / food_value_per_100g) × 100

Select the nutrient where food provides the most value (weight × fill).
Serving size = that candidate's recommended grams.

Constrain: max(50, min(250, computed_serving))
Budget constraint: min(serving, (remaining_budget / pricePer100g) × 100)
```

**Example**: If protein gap = 40g and food has 10g protein per 100g:
- Candidate serving = (40 / 10) × 100 = 400g → clamped to **250g** (max serving)

---

## Algorithm 9: XGBoost Learning-to-Rank

**Type**: Trained Supervised ML Model

**Model**: XGBRanker with `objective="rank:ndcg"`

**Purpose**: Re-rank rule-based filtered food candidates by predicted suitability score.

**Training Data**: Synthetically generated from 120 user "queries" with varied calorie/protein/carb/fat/fiber targets and gaps. Each (query, food) pair is labeled with a relevance score 0–4 using the rule-based nutrition/gap-fit logic. This avoids random labels while providing diverse training examples.

**Features Used** (per food candidate):
- Calories, Protein_g, Carbs_g, Fat_g, Fibre_g (from food dataset)
- calorie_gap_ratio, protein_gap_ratio, carbs_gap_ratio, fat_gap_ratio, fiber_gap_ratio
- calorie_fraction (food calories / calorie target)
- protein_fraction, fiber_fraction

**Hyperparameters** (verified from `ml/train_xgb_rank.py`):
```
objective = rank:ndcg
n_estimators = 100
learning_rate = 0.1
max_depth = 5
random_state = 42
```

**Training Split**: Group-aware 80/20 split (by whole query groups, not individual rows, to prevent data leakage).

**Evaluation Metrics** (from `ml/evaluation_metrics.json` — note: these are for supporting models, not XGBRanker; XGBRanker metrics are written to `ml/models/xgboost_ranker_meta.json` after training):
```json
Calorie Regression (Ridge): MAE=23.11, RMSE=29.43, R²=0.871
Meal Classification (RF): Accuracy=0.519, F1=0.524
Protein Prediction (XGBoost): MAE=1.41, RMSE=2.33, R²=0.868
```

**Inference**:
1. Build feature matrix from candidate foods
2. Load `ml/models/xgboost_ranker.pkl` via joblib
3. `model.predict()` → raw scores
4. Logistic transform: `1 / (1 + exp(-score))` → (0,1) range (monotonic, preserves ranking)
5. Sort descending → top-N selected

**Fallback**: If model file not found or prediction fails, rule-based score order is used (no crash).

**Source**: `ml/train_xgb_rank.py`, `ml/ranker/predict.py`, `ml/rank_food.py`

---

## Algorithm 10: Random Forest Weight Forecasting

**Type**: Trained Supervised ML Model (via FastAPI backend)

**Purpose**: Predict 7-day weight change in kg based on user profile and historical intake averages.

**Architecture**: FastAPI service (`backend/`) with Random Forest Regression model.

**Features** (19 total):
- User biometrics: age, gender (encoded), heightCm, weightKg
- Calculated targets: calorieTarget, protein, carbs, fat, fiber
- 7-day intake averages: avg_calories, avg_protein, avg_carbs, avg_fat, avg_fiber
- Calorie balance: avg_calories - calorieTarget
- Activity level (encoded)
- Days of data available

**Honest Gating**: The service returns `{available: false, reason: "..."}` if the model has not been trained or insufficient historical data exists. No fake predictions are produced.

**Integration**: Next.js calls `GET /api/ml/forecast` → tries FastAPI `http://127.0.0.1:8000/api/v1/predict` → subprocess fallback if unavailable.

**Source**: `backend/app/`, `src/app/api/ml/forecast/`

---

## Algorithm 11: Python Rule-Based Scoring (ML Layer)

**Type**: Rule-Based Algorithm

**Formula** (verified from `ml/recommend_service.py → score_food()`):
```python
gap_score = average fill efficiency across protein, fiber, calcium, iron, vitaminC

cal_score = norm(max(0, remaining_calories - food_calories), remaining_calories + food_calories)

meal_score = 1.0 if food's meal type matches requested, else 0.5/0.4

rep_penalty = 0.5 if food in 7-day history, else 0.0

fb_score = 1.0 if liked, -1.0 if disliked, 0.0 otherwise

score = (W_GAP×gap_score + W_CALORIE×cal_score + W_MEAL_TYPE×meal_score 
         + W_PREFERENCE×0.5 + W_FEEDBACK×(0.5 + 0.5×fb_score)) 
        × pref_bonus × (1 - W_REPETITION×rep_penalty)

Weights: W_GAP=0.40, W_CALORIE=0.20, W_MEAL_TYPE=0.10, 
         W_PREFERENCE=0.10, W_FEEDBACK=0.10, W_REPETITION=0.10
```

---

## Algorithm 12: Gemini Vision Food Recognition

**Type**: External LLM API (Cloud)

**API**: Google Generative Language API, model `gemini-3.8-flash`

**Input**: Base64-encoded image + structured prompt requesting JSON output with per-100g nutrition values

**Prompt Design**: Instructs the model to return a specific JSON schema with food names, portion grams (estimated actual weight), per-100g nutrition values, and confidence scores.

**Post-processing**:
- Strip markdown code fences if present
- Parse JSON, clamp all values to valid ranges
- Scale to actual portion: `value = per_100g_value × (portionGrams / 100)`

**Model Fallback Chain**: gemini-3.8-flash → gemini-3.8-flash-lite (on 503 overload)

**Disclaimer**: AI-estimated nutrition values are approximations and may vary from actual values. The model is not clinically validated.

---

## Algorithm 13: Water Target Calculation

**Type**: Mathematical Formula

**Formula** (verified from `src/lib/hydration.ts → calcWaterTargetMl()`):
```
Daily Water Target (ml) = weightKg × 35
Default (no weight data): 65 × 35 = 2275 ml
Custom override takes precedence if set.
```

**Example**: 70 kg user → 70 × 35 = **2450 ml/day target**

---

## Algorithm 14: Work Type to Activity Level Mapping

**Type**: Rule-Based Algorithm (regex-based)

**Purpose**: Automatically derive activity level from free-text occupation entry.

**Implementation**: `src/lib/nutrition.ts → workTypeToActivityLevel()`

**Mapping Hierarchy** (applied in this order):
1. `light` — healthcare workers, teachers, cooks, retail staff, domestic helpers, artisans
2. `sedentary` — desk workers, managers, IT professionals, financial workers, legal professionals, academics
3. `moderate` — drivers, mechanics, electricians, factory operators, textile workers, police, waitstaff
4. `active` — farmers, agricultural workers, construction laborers, gardeners, fitness trainers, fishermen
5. `very-active` — soldiers, military, miners, steel workers, dock workers, professional athletes

**Coverage**: ~300+ occupation keywords across Indian NCO/ISCO categories with regex matching.
