# MealMentor — Functional Module Analysis

## Complete User Journey

1. **First Visit**: User opens the app → redirected to login page
2. **Register**: User fills name, email, password → account created → redirected to dashboard
3. **Profile Setup**: Banner prompts user to complete profile → user enters age, height, weight, activity level, food preferences, health goals, allergies, budget
4. **Dashboard**: BMR/TDEE/calorie targets calculated automatically → nutrient gap display shown
5. **Daily Use**: User logs meals → AI recommends what to eat next → water tracked → weight logged
6. **Progress Review**: User views 7-day nutrition history + weight trend chart + streak

---

## Module 1: User Registration and Login

**Purpose**: Create and authenticate user accounts.

**Input**: Name, email, password (registration); Email, password or Google OAuth token (login)

**Processing Logic**:
- Registration: Validate email uniqueness, hash password using Node.js `scrypt` (KEY_LENGTH=64, 16-byte random salt), create `User` document
- Login: Find user by email, compare password using `timingSafeEqual`, generate HS256 JWT (7-day expiry), set HTTP-only cookie
- Google OAuth: Exchange authorization code for Google profile, upsert user by googleId/email

**Output**: Authenticated session cookie (`mealmentor_session`)

**Source Files**: `src/lib/auth.ts`, `src/lib/hash.ts`, `src/lib/session.ts`, `src/app/api/auth/`

**Step-by-Step Flow**:
1. POST `/api/auth/register` → validate → hash password → `User.create()` → `createSessionToken()` → set cookie
2. POST `/api/auth/login` → `User.findOne({email})` → `verifyPassword()` → `createSessionToken()` → set cookie
3. Subsequent requests → `getCurrentUser()` → `verifySessionToken()` → `User.findById()`

---

## Module 2: User Profile Management

**Purpose**: Store and manage all personal, lifestyle, and dietary data required for nutrition calculations.

**Input**: Age, gender, height (cm), weight (kg), work type (free text), activity level, health goal, food preference, cuisine, allergies (array), avoided foods (array), favorite foods (array), health conditions (array), daily budget, budget period, unit system (metric/imperial), custom macro split

**Processing Logic**:
- PUT `/api/profile` → validate → `User.findByIdAndUpdate({profile: ...})`
- Work type is automatically mapped to activity level using `workTypeToActivityLevel()` which uses regex patterns matching Indian National Classification of Occupations (NCO) categories

**Supported Goals**: weight-loss, weight-gain, muscle-building, maintain-weight, improve-energy, general-healthy-lifestyle

**Supported Health Conditions**: none, diabetes, hypertension, other

**Source Files**: `src/models/User.ts`, `src/lib/nutrition.ts`, `src/app/api/profile/`

---

## Module 3: BMR Calculation

**Purpose**: Calculate the user's Basal Metabolic Rate — energy burned at complete rest.

**Formula Used (Mifflin–St Jeor Equation)**:
```
base = (10 × weightKg) + (6.25 × heightCm) - (5 × age)
Male:   BMR = base + 5
Female: BMR = base - 161
Other:  BMR = base  (no sex adjustment)
```

**Source**: `src/lib/nutrition.ts → calcBMR()` (lines 114–122)

**Example**:
- Male, 25 years, 70 kg, 175 cm
- base = (10 × 70) + (6.25 × 175) - (5 × 25) = 700 + 1093.75 - 125 = 1668.75
- BMR = 1668.75 + 5 = **1673.75 kcal/day**

**Validation**: Throws error if weightKg, heightCm, or age are missing.

---

## Module 4: TDEE Calculation

**Purpose**: Calculate Total Daily Energy Expenditure — energy burned including physical activity.

**Formula**:
```
TDEE = BMR × Activity Factor
```

**Activity Factors** (verified from `src/lib/nutrition.ts`):
| Activity Level | Factor |
|---------------|--------|
| sedentary | 1.2 |
| light | 1.375 |
| moderate | 1.55 |
| active | 1.725 |
| very-active | 1.9 |

**Source**: `src/lib/nutrition.ts → calcTDEE()` (lines 124–133)

**Example** (continuing from BMR example):
- BMR = 1673.75, Activity Level = moderate (1.55)
- TDEE = 1673.75 × 1.55 = **2594.31 kcal/day**

**Work Type Fallback**: If activityLevel is not set, `workTypeToActivityLevel()` maps free-text occupation to an activity level using an extensive regex matcher covering Indian NCO job categories.

---

## Module 5: Daily Calorie Target Calculation

**Purpose**: Adjust TDEE for the user's health goal.

**Formula**:
```
Calorie Target = max(1200, round(TDEE + Goal Delta))
```

**Goal Deltas** (verified from `src/lib/nutrition.ts`):
| Goal | Delta (kcal) |
|------|-------------|
| weight-loss | -500 |
| weight-gain | +500 |
| muscle-building | +250 |
| maintain-weight | 0 |
| improve-energy | 0 |
| general-healthy-lifestyle | 0 |

**Minimum Floor**: 1200 kcal (never returns a value below this)

**Source**: `src/lib/nutrition.ts → calcCalorieTarget()` (lines 192–195)

**Example** (continuing):
- TDEE = 2594.31, Goal = weight-loss
- Target = max(1200, round(2594.31 - 500)) = max(1200, 2094) = **2094 kcal/day**

---

## Module 6: Macronutrient Target Calculation

**Purpose**: Calculate daily protein, carbohydrate, and fat targets.

**Auto Mode (verified formula)**:
```
Protein Factor:
  - muscle-building: 1.6 g/kg
  - weight-loss or diabetes: 1.2 g/kg
  - weight-gain: 1.0 g/kg
  - default: 0.8 g/kg

Protein (g) = max(40, round(weightKg × protein_factor))

Carbs Percent:
  - diabetes: 40% of calories
  - all others: 50% of calories
Carbs (g) = round(calorieTarget × carbs_percent / 4)

Fat (g) = max(0, round((calorieTarget - protein_kcal - carbs_kcal) / 9))
```

**Custom Mode**: User can set custom protein%, carbs%, fat% → macros are calculated from percentages directly.

**Source**: `src/lib/nutrition.ts → calcMacroTargets()` (lines 214–263)

**Example**:
- Calorie Target = 2094, Weight = 70 kg, Goal = weight-loss
- Protein = max(40, round(70 × 1.2)) = max(40, 84) = **84g**
- Carbs = round(2094 × 0.5 / 4) = round(261.75) = **262g**
- Fat = max(0, round((2094 - 336 - 1048) / 9)) = round(710 / 9) = **79g**

---

## Module 7: Micronutrient Target Calculation

**Purpose**: Calculate daily fiber, calcium, iron, and vitamin C targets.

**Formula (verified from `src/lib/nutrition.ts → microTargets()`)**:
| Nutrient | Standard Adult | Teen (10–17) | Older Adult (51+) | Female specific |
|----------|---------------|-------------|------------------|----------------|
| Calcium | 1000 mg | 1300 mg | 1200 mg | — |
| Iron | 8 mg (male) | 11 mg (male), 15 mg (female) | 8 mg | 18 mg (18–50) |
| Vitamin C | 75 mg | 75 mg | 75 mg | — |
| Fiber | 38 g (male) | 38 g (male), 26 g (female) | — | 25 g |

**Health Condition Adjustments**:
- Diabetes: Sugar limit reduced from 50g to 30g
- Hypertension: Sodium limit reduced from 2300mg to 1500mg

---

## Module 8: Nutrient Gap Calculation

**Purpose**: Real-time calculation of what nutrients the user still needs today.

**Formula (verified from `src/lib/gaps.ts → calcGaps()`)**:
```
Gap = max(0, Target - Consumed)
```

**Nutrients Tracked**: calories, protein, carbs, fat, fiber, calcium, iron, vitamin C, plus sugar-remaining and sodium-remaining (upper limits)

**Graded Status** (verified thresholds):
| % of Target Consumed | Status |
|---------------------|--------|
| ≥ 130% | over |
| ≥ 100% | adequate |
| ≥ 75% | near-target |
| ≥ 40% | low |
| < 40% | deficient |

**Adaptive Weights**: Nutrients with larger percentage gaps receive higher importance weights in recommendation scoring (normalized so all weights sum to 1).

---

## Module 9: Food Logging and Nutrition Tracking

**Purpose**: Allow users to log meals and track daily intake.

**Input**: Food ID, meal type (breakfast/lunch/snack/dinner), quantity in grams

**Processing**:
```
Nutrient Intake = (qtyG / 100) × per-100g value
```

**Example**: 150g of Achappam (293 kcal/100g):
- Calories = (150/100) × 293 = 439.5 kcal

**Data Stored**: A `MealEntry` document stores a snapshot of all per-100g nutrient values at the time of logging (so future food data changes do not retroactively affect logs).

**Source**: `src/lib/intake.ts → computeIntake()`, `src/app/api/tracking/`

---

## Module 10: Meal Recommendations

**Purpose**: Generate personalized meal suggestions filling remaining nutrient gaps.

**Two-Stage Pipeline**:

**Stage 1 — Rule-Based Filtering and Scoring** (`src/lib/recommend.ts`):
1. Hard-filter: Remove foods matching allergies, avoided foods, dietary restrictions, disliked foods
2. Budget filter: Remove foods whose minimum portion (50g) exceeds remaining budget
3. 14-day no-repeat: Exclude recently eaten foods (hard exclusion, fallback re-admits oldest)
4. Score each food using nutrient-gap fill efficiency (capped at 1 per nutrient)
5. Apply penalties for calorie density, sugar excess, sodium excess
6. Apply boosts for favorite/liked foods (+0.05), penalties for rejected foods (-0.15)
7. Apply recency discount for re-admitted fallback foods

**Stage 2 — XGBoost Re-ranking** (`ml/rank_food.py`, `ml/ranker/`):
1. Build feature matrix from candidate foods (calories, protein, carbs, fat, fiber + gap deltas)
2. Load trained XGBRanker model (`ml/models/xgboost_ranker.pkl`)
3. Predict ranking scores → logistic transform to (0,1) range
4. Sort descending → top-N returned

**Serving Size Optimization**:
- Pick the serving size that closes the most important remaining gap
- Constrain to 50g–250g range
- Further constrain by budget if applicable

**Output**: List of `Recommendation` objects with food, score, serving size (grams), per-serving nutrition, reason text, cost

**Source**: `src/lib/recommend.ts`, `src/app/api/recommend-xgb/route.ts`, `ml/recommend_service.py`

---

## Module 11: Food Image Analysis

**Purpose**: Photograph a meal and automatically identify foods and estimate nutrition.

**Input**: Base64-encoded food image (JPEG/PNG)

**Processing**:
1. POST to Gemini Vision API (`gemini-3.8-flash`) with structured prompt
2. Prompt requests: food item names, portion grams (actual weight in image), per-100g nutrition values
3. Response parsed from JSON, values sanitized and clamped
4. Per-item scaled nutrients: `calories = item.calories × (portionGrams / 100)`
5. Model fallback chain: primary → lite model if 503 error
6. Results stored in `FoodPhoto` document

**Output**: List of detected food items with name, portion estimate, confidence score (0-1), per-100g nutrition

**Confidence Thresholds**: ≥0.9 = high, ≥0.7 = medium, <0.7 = low

**Source**: `src/lib/gemini-vision.ts`, `src/app/api/food-photo/`

---

## Module 12: Barcode Scanning

**Purpose**: Scan packaged food barcodes to retrieve nutrition information.

**Input**: EAN barcode number (8+ digits)

**Processing Pipeline**:
1. Check offline barcode cache (`src/data/barcode-cache.ts`) — ~500 products, instant response
2. If not found: fetch from OpenFoodFacts API (`https://world.openfoodfacts.org/api/v0/product/{ean}.json`)
3. Parse nutriments (energy-kcal_100g, proteins_100g, carbohydrates_100g, fat_100g, etc.)
4. Handle kJ → kcal conversion (÷4.184), salt → sodium conversion (÷2.5 × 1000)
5. Return NutriScore grade and NOVA group if available

**Implemented via**: Quagga2 library for camera-based scanning, `src/lib/openfoodfacts.ts` for lookup

---

## Module 13: AI Nutrition Chatbot

**Purpose**: Answer user questions about nutrition, BMR, TDEE, deficiencies, and diet recommendations.

**Architecture**:
1. **Primary**: Gemini API (`gemini-3.8-flash`) with user profile + today's intake as system context, 2.5s SLA timeout
2. **Fallback**: Local deterministic engine (`generateContextualReply()`) — always succeeds in <5ms

**Context Injected into Gemini Prompt**:
- User name and profile
- Calculated daily targets (BMR, TDEE, calorie target, macros, micros)
- Today's consumed intake
- Graded nutrient deficiency statuses

**Local Fallback Categories**:
- Meal/food questions → calculates remaining calories, protein, fiber deficits; gives suggestions
- BMR/TDEE/calorie questions → returns exact computed values
- Micronutrient questions → lists today's intake vs targets; flags deficiencies
- Weight/goal questions → summarizes targets and progress tracking tip
- Default → general introduction with example questions

**Source**: `src/app/api/ai/chat/route.ts`

---

## Module 14: Water Intake Tracking

**Purpose**: Track daily water consumption against a weight-based target.

**Water Target Formula** (verified from `src/lib/hydration.ts`):
```
Daily Water Target (ml) = weightKg × 35
Default (if no weight): 65 kg × 35 = 2275 ml
Custom override takes precedence if set.
```

**Supported Units**: ml, cups (1 cup = 240ml), liters

**Features**: Streak tracking, hydration tags (morning, with-meal, post-workout, evening, general), reminder preferences stored in user profile

---

## Module 15: Weight Logging and Progress Tracking

**Purpose**: Track body weight over time and visualize trends.

**Input**: Weight in kg (or lb with imperial conversion), optional date, notes

**Validation**: Weight must be 20–400 kg range

**Progress Charts**: Recharts library renders:
- Line chart of weight history
- Area chart of 7-day nutrition intake vs targets

**7-Day Weight Forecast**:
- FastAPI service receives 19 features (profile biometrics + 7-day average intake + targets)
- Random Forest model predicts kg change over next 7 days
- Returns `{available: false}` if model not yet trained (honest gating)

**Source**: `src/models/WeightLog.ts`, `src/app/api/progress/`, `backend/app/`

---

## Module 16: Streak and Habit Tracking

**Purpose**: Motivate consistent daily usage through streak monitoring.

**Computed By**: `src/lib/streaks.ts → computeStreak()`

**Streak Logic**:
- `current`: consecutive days ending at yesterday (today extends it)
- `longest`: maximum run seen in history
- `atRiskDays`: consecutive days missed at tail
- `nextMilestone`: next achievement (3, 7, 14, 30, 60, 100, 180, 365 days)

---

## Module 17: Custom Food Creation

**Purpose**: Allow users to create their own food entries with manual or ingredient-based nutrition.

**Nutrition Sources**:
- `auto-ingredients`: Nutrition auto-calculated from ingredient list (matched to food DB)
- `manual`: User manually enters per-serving nutrition values
- `ingredients-override`: Auto-calculated but user can override

**Sharing**: Custom foods can be shared via a unique token URL; other users can import them.

**Source**: `src/models/CustomFood.ts`, `src/lib/custom-food.ts`

---

## Module 18: Grocery List Generation

**Purpose**: Automatically generate grocery lists from the daily meal plan.

**Input**: Generated meal plan for the day (breakfast, lunch, snack, dinner)

**Processing**: 
1. Fetch dish ingredients from `src/data/dish-ingredients.ts`
2. Map ingredients to grocery prices from `finalDatasetGrocery.csv` (331 items)
3. Aggregate quantities across meals
4. Return ingredient list with prices and total cost estimate

**Source**: `src/app/api/grocery/`, `src/lib/quick-buy.ts`

---

## Module 19: Proactive Nudges

**Purpose**: Send contextual notifications to encourage healthy habits.

**Nudge Types**: missedMeal, hydration, macro imbalance, streak celebration

**Evaluation Logic** (verified from `src/lib/proactive-nudges.ts`):
- Missed meal: last meal logged >3 hours ago during meal hours
- Hydration: consumed < 60% of water target and afternoon
- Macro: day is carb-heavy (>70% calories from carbs)
- Streak: milestone days (3, 7, 14, 30...)

---

## Module 20: Meal Timing and Intermittent Fasting Support

**Purpose**: Allow users to configure meal slots and timing, including IF protocols.

**Supported Presets**:
- Standard 3-meal (default)
- Intermittent Fasting 16:8 (configurable eating window, e.g. 12:00–20:00)
- 5 small meals
- Custom slots

**Storage**: Meal timing preferences stored in `user.profile.mealTimingPreferences`

**Source**: `src/lib/meal-timing.ts`, `src/models/User.ts`

---

## Module 21: Voice Input

**Purpose**: Allow users to log meals and navigate using voice commands.

**Technology**: Web Speech API (browser-native, no external API required)

**Wake Words**: "hey nutrisense", "hey mealmentor", "mealmentor", "hey assistant", "nutrisense"

**Recognized Actions**:
- `log_meal`: "log 200 grams of rice for lunch"
- `navigate`: "go to meal plan"
- `daily_summary`: "what did I eat today"
- `suggest_recipe`: "suggest a breakfast recipe"
- `chat`: "ask the AI assistant..."

**Confidence Threshold**: <0.75 = low confidence, requires confirmation

**Source**: `src/lib/voice-intent.ts`
