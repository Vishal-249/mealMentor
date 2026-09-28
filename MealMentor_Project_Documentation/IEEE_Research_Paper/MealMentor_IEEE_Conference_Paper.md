# AI-Driven Personalized Nutrition Assistant with Adaptive Meal Planning and Health Monitoring

**Sriram Ganesh M**$^1$, **Vishal T**$^2$, **Mrs. A.P. Aruna Jameela**$^3$  
*Department of Information Technology, Rajalakshmi Engineering College, Chennai, India*  
*Email: $^1$231001213@rajalakshmi.edu.in, $^2$231001249@rajalakshmi.edu.in, $^3$arunajameela.ap@rajalakshmi.edu.in*

---

### Abstract
Eating healthy is one of the best ways to feel energetic and manage chronic conditions like diabetes and high blood pressure. Yet most existing nutrition apps only count calories after meals are already eaten, give generic advice that ignores daily physical work, and fail to suggest practical meals that fill specific nutrient shortages. In this paper, we present **MealMentor (NutriSense AI)**, an easy-to-use, AI-powered nutrition assistant designed to give clear, personalized, and safe dietary guidance. Rather than using confusing black-box models, MealMentor starts with reliable health rules: it calculates resting calorie burn using the Mifflin–St Jeor formula, adjusts targets to real jobs using an Indian occupation matcher, and sets safe medical limits for diabetes (capping free sugars at 25 g) and hypertension (limiting sodium to 1500 mg). The system tracks active daily shortages across ten nutrients (protein, carbs, fat, fiber, calcium, iron, vitamin C, sugar, and sodium). To make logging food effortless, users can snap a photo of their plate using Google Gemini Vision, scan a packaged food barcode with an offline 500-item cache, or speak naturally using browser-native voice recognition. When suggesting meals, MealMentor strictly removes allergens and expensive items, ensures meals do not repeat too often over 14 days, and uses an XGBoost machine learning model to rank the best options. Portion sizes are automatically calculated between 50 g and 250 g to fill open nutrient gaps within budget. The app also predicts 7-day weight changes using a Random Forest model, while including everyday features like a 16:8 intermittent fasting timer, dynamic water tracking ($35\text{ ml/kg}$), timely reminders, automatic weekly grocery shopping lists for 331 local store items, and an offline AI chat assistant. A user trial with 15 participants over 315 meal decisions achieved 100% safety and an average satisfaction rating of 4.26 out of 5.00.

***Index Terms*—Personalized nutrition, food recommendation, learning-to-rank, nutrient gap analysis, XGBoost, Random Forest, weight forecasting, Mifflin–St Jeor, plate photo recognition, barcode scanner, voice logging, water tracking, intermittent fasting, grocery planning, explainable AI.**

---

## I. INTRODUCTION
Eating a balanced diet is vital for good health, but chronic conditions like Type 2 diabetes and high blood pressure continue to affect millions of families across India and the world [8], [10]. In everyday life, regular visits to a professional dietitian are expensive and inaccessible for most people. Meanwhile, broad advice found online fails to account for a person's body type, physical daily labor, medical history, local food availability, and grocery budget.

Most commercial diet-tracking apps suffer from five common drawbacks:
1. *Generic Calorie Targets*: Apps assign the same calorie goal to an office worker and a construction laborer of the same age and weight, ignoring how much physical energy their job burns.
2. *Passive Logging Without Guidance*: Apps act like a diary, recording food after it has been eaten, but never tell the user what to eat next to fix open nutrient shortages.
3. *Unsafe Recommendations*: Pure machine learning systems can accidentally suggest meals with allergens or harmful ingredients because they treat health limits as loose mathematical goals rather than strict safety rules [1], [2].
4. *Tiresome Manual Typing*: Typing every ingredient into a search box takes too much time, causing most people to stop logging after two weeks.
5. *Ignoring Daily Routine*: Everyday habits like fasting hours, drinking enough water, avoiding late-night snacking, and buying affordable groceries are usually separated into different apps.

To solve these problems, we created **MealMentor**, a smart nutrition assistant that combines dependable physiological formulas with machine learning. The app calculates exact resting metabolism, matches job titles to physical activity, sets medical boundaries for diabetes and blood pressure, tracks ten nutrients in real time, and lets users record meals with pictures, barcodes, or voice.

**Key features of MealMentor**:
- **Personalized Energy Needs**: Uses the clinical Mifflin–St Jeor formula and an Indian job matcher to calculate resting and daily energy needs, with hard limits on sodium ($\le 1500\text{ mg}$) and sugar ($\le 25\text{ g}$).
- **Live 10-Nutrient Gap Tracker**: Continuously tracks shortages across ten nutrients ($G_k = \max(0, T_k - C_k)$) to show what the body still needs today.
- **Three Easy Ways to Log Food**: Plate photo recognition using Google Gemini Vision, rapid barcode scanning with a 500-product offline cache, and hands-free voice logging.
- **Safe Two-Stage Meal Suggestions**: Stage 1 eliminates allergens, dietary conflicts, and high costs with a 14-day repetition check. Stage 2 scores dishes and uses an XGBoost ranker (NDCG@5 = 1.0000) with a safe offline rule fallback.
- **Smart Portion Sizing**: Calculates portions between 50 g and 250 g to satisfy the biggest nutrient gap within budget.
- **Honest Weight Predictions**: Uses Random Forest to forecast 7-day weight change (MAE = 0.1225 kg), holding back results until enough real user logs exist.
- **Everyday Lifestyle Tools**: Includes intermittent fasting clocks (16:8), daily water goals ($35\text{ ml/kg}$), smart reminders, 331-item local grocery lists, custom recipe sharing, and an offline AI chat helper.
- **Proven Reliability**: Verified through 11 automated test suites and a trial with 15 users over 315 meal decisions.

---

## II. PROBLEM STATEMENT AND MOTIVATION

### A. Why Generic Meal Plans Fail
Traditional meal planners rely on fixed calorie goals. This overlooks the huge differences in energy burned during work. For instance, a farmer burns vastly more calories than an office analyst of the same height and weight. Furthermore, generic plans often suggest expensive, unfamiliar foods that do not fit local household grocery budgets.

### B. The Need for Comprehensive Personalization
Proper nutrition requires looking beyond calories alone. A safe diet must take into account age, sex, height, weight, physical exertion, medical conditions (like diabetes and hypertension), dietary choices (vegetarian or vegan), and food allergies. Relying solely on calories can easily lead to meals that trigger allergic reactions or dangerous blood sugar spikes.

### C. Finding and Fixing Daily Nutrient Shortages
Most people have no easy way of knowing if they are getting enough fiber, calcium, iron, or vitamin C. Because micronutrient shortages build up quietly over weeks without obvious immediate symptoms, people feel tired without knowing why. An automated tracker that compares intake against goals after every meal helps users choose dishes that immediately solve these shortages.

### D. Removing Friction in Food Journaling
Typing food names into a search box multiple times a day is tiring. Users need simpler ways to record meals: taking a quick photo of their plate, scanning a packaged snack barcode with instant offline results, or speaking a simple sentence while cooking or eating.

### E. Connecting Food Plans to Real-Life Routines
Health is more than just single dishes. When people eat (such as an intermittent fasting window) affects blood sugar stability. Drinking enough water aids metabolism and digestion. Helpful reminders stop users from skipping meals or eating carb-heavy snacks late at night. Finally, a diet plan is only helpful if users can easily buy the ingredients at fair local market prices.

---

## III. RELATED WORK AND LITERATURE REVIEW

### A. Food Recommender Systems
Recommending food is very different from recommending movies or shopping items because food intake directly impacts health and safety [2], [9]. Standard collaborative filtering methods often recommend popular junk foods simply because many people log them [4]. Content-based filters match food tags but often get stuck recommending the exact same meal repeatedly unless variety rules are added [2].

### B. Health-Aware Recommenders
Researchers have used knowledge graphs and multi-objective optimization to enforce health limits [3], [9]. Chen et al. showed that allergen elimination must be treated as a strict rule rather than a soft mathematical goal [3]. However, most existing tools compute recommendations only once a day rather than updating recommendations in real time as each meal is logged.

### C. Meal Monotony and Repetition Decay
People dislike eating the exact same meal several days in a row. While complex deep-learning models (like SASRec [5] and BERT4Rec [6]) can track sequential habits, they require millions of user logs that consumer wellness apps simply do not have [7]. MealMentor solves this by combining a simple 14-day variety decay rule with machine learning ranking.

### D. Image Recognition and Large Language Models
Multimodal AI models (such as Google Gemini and GPT-4V) can discuss recipes and identify foods in pictures [1]. However, Deng and Tu showed that relying entirely on AI vision models to guess nutrient numbers leads to inaccurate calculations [1]. MealMentor uses vision AI solely to recognize dish names and portions on the plate, while pulling verified nutrition data from an audited local database.

**TABLE I: HOW MEALMENTOR COMPARES WITH EXISTING DIETARY APPROACHES**

| Feature | Standard Trackers (e.g., MyFitnessPal) | Pure LLM Helpers [1] | Knowledge Graph Models [3] | MealMentor (This Work) |
|:---|:---|:---|:---|:---|
| **Calorie Calculations** | Static preset daily templates | Rough conversational guesses | Fixed mathematical tables | Mifflin–St Jeor + Indian NCO Work Multipliers |
| **Nutrient Gap Tracking** | Weekly summary charts only | Vague mentions in text | Graph path queries | Live 10-nutrient deficit tracking ($G_k = \max(0, T_k - C_k)$) |
| **Allergen Safety** | Soft warnings / Manual checking | Unreliable (Risk of hallucination) | Hard entity filters in graph | Strict Stage 1 Boolean elimination ($0\%$ breach) |
| **Food Ranking** | Unordered keyword search | Generated conversational text | Graph distance matching | XGBoost Learning-to-Rank (`rank:ndcg`) |
| **Meal Variety** | None (Manual user choice) | Casual prompt reminders | Graph diversity penalties | Built-in 14-day variety decay ($S_{\text{variety}}$) |
| **Weight Forecast** | None | Unreliable text estimates | None | Random Forest 7-day weight prediction with honest gating |
| **Meal Logging Options** | Barcode scanning only | Photo-to-recipe text description | Plain text input only | Multimodal: Gemini Vision + Offline Barcode + Voice |
| **Everyday Habits** | Basic water counter | General conversational advice | None | Intermittent Fasting (16:8) + Hydration + Reminders + Grocery |

---

## IV. SYSTEM ARCHITECTURE AND DESIGN METHODOLOGY

### A. Modular Monolithic Architecture
MealMentor is built as a single, cleanly organized deployable application using Next.js 16 and TypeScript (Fig. 1). This design avoids the network delays and complicated setup of microservices while keeping every part of the codebase organized into clear functional domains.

```
MealMentor: Modular Monolithic System Architecture
Single Deployable Next.js 16 / TypeScript Process with Decoupled Functional Modules

.---------------------------------------------------------------------------------------------------------.
|                  MEALMENTOR MODULAR MONOLITH (Single Deployable Application Process)                    |
|                                                                                                         |
|  +---------------------------------------------------------------------------------------------------+  |
|  |                1. USER PRESENTATION MODULE (Next.js 16 / React 19 / Client Dashboard)             |  |
|  |  Meal Journaling · Real-Time 10-Nutrient Gaps · Multimodal Ingestion (Vision/Barcode/Voice) · IF  |  |
|  |             Hydration Tracker (35 ml/kg) · Smart Grocery List · 7-Day Weight Forecast Card        |  |
|  +---------------------------------------------------------------------------------------------------+  |
                                                     |
                                                     | UI Events & Multimodal State
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                  2. APPLICATION GATEWAY & SECURITY MODULE (Edge & API Route Handlers)                   |
|  JWT Session Security (Scrypt + TimingSafeEqual) · Google OAuth 2.0 · Rate Limiting (30 req/min/IP)     |
|              Hybrid AI Assistant (Gemini 3.8 Flash + <5ms Fallback) · Proactive Contextual Nudges       |
+---------------------------------------------------------------------------------------------------------+
             |                                                       |
             v                                                       v
+------------------------------------------+       Nutrient        +------------------------------------------+
|    3A. DETERMINISTIC NUTRITION MODULE    |       Deficits        |    3B. RECOMMENDATION & SIZING MODULE    |
| • Mifflin-St Jeor BMR & TDEE (NCO Roles) |---------------------->| • Stage 1 Hard Safety Mask (Allergens)   |
| • Dynamic 10-Nutrient Gap Engine (Gk)    |         (Gk)          | • Stage 2 Utility & 14-Day Variety Decay |
| • Diabetes & BP Clinical Clamps          |                       | • Clinical Portion Sizer (50g–250g)      |
+------------------------------------------+                       +------------------------------------------+
                                                                                     |
                                                                                     | Filtered Candidates
                                                                                     v
+---------------------------------------------------------------------------------------------------------+
|                    4. MACHINE LEARNING MODULE (Embedded Python Service / FastAPI)                       |
| • 25-Dimensional Gap Feature Extraction Engine                                                          |
| • XGBoost Learning-to-Rank Engine (rank:ndcg + Logistic Sigmoid Mapping) [NDCG@5 = 1.0000]              |
| • Random Forest 7-Day Weight Regressor (19 Features, Honest Readiness Gated) [MAE: 0.1225 kg, R²: 0.5616]|
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                                5. SHARED CORE & DATA REPOSITORY LAYER                                   |
|          Hydration Engine (35 ml/kg) · IF 16:8 Window Manager · Recipe Token Sharing · Health Utilities  |
+---------------------------------------------------------------------------------------------------------+
'---------------------------------------------------------------------------------------------------------'
             |                                                                       |
             | Images, Barcodes &                                                    | Mongoose ODM
             | Voice Commands                                                        | Queries
             v                                                                       v
+----------------------------------------------------+         +----------------------------------------------------+
|        EXTERNAL INGESTION & CLOUD SERVICES         |         |            MONGODB PERSISTENT DATASTORE            |
| • Google Gemini Vision API (Plate Image Analysis)  |         | • User Biometric Profiles & Indian NCO Roles       |
| • OpenFoodFacts API (UPC/EAN Barcode Lookup)       |         | • 384 Verified Indian Foods & 331 Grocery Items    |
| • Offline Local Barcode Cache (~500 Products)      |         | • Longitudinal Weight Logs (t and t+7) & Intakes   |
| • Browser-Native Web Speech API (Voice Logging)    |         | • Hydration Tracking Logs & Custom Recipe Entries  |
+----------------------------------------------------+         +----------------------------------------------------+
```
*Fig. 1. MealMentor modular monolithic system architecture: 5 internal decoupled functional domains within a single deployable process, integrated with external multimodal ingestion services and local MongoDB datastore.*

### B. Database Structure and Food Datasets
The system stores information across seven organized database collections:
- `users`: Holds age, sex, height, weight, job titles, diet choices, food allergies, medical conditions, fasting preferences, and budgets.
- `foods`: 384 verified food items in `finalDatasetfood.csv`, with ten nutrient measurements per 100 g, meal categories, allergens, and costs.
- `groceries`: 331 local supermarket items in `finalDatasetGrocery.csv` that connect meal recipes to market ingredient prices.
- `weightlogs`: Weekly body weight entries ($t, t+7$).
- `mealentries`: Historical intake records storing food IDs, gram portions, meal times, and nutrient snapshots.
- `hydrationlogs`: Daily water entries tagged by time of day.
- `customfoods`: User-created recipes with calculated nutrition and shareable web links.

### C. Feature Space Construction
For candidate meal $f$ and user state $U$, the recommendation module builds a 25-dimensional feature vector $\mathbf{x} \in \mathbb{R}^{25}$ across calories, protein, carbohydrates, fat, and fiber:
1. *Nutrient Densities (5)*: Nutrient quantities per 100 g.
2. *Target Allowances (5)*: The user's daily goals $T_k$.
3. *Active Deficits (5)*: Unfilled nutrient shortages $G_k$.
4. *Coverage Margins (5)*: Difference $\Delta_k = \text{FoodValue}_k - G_k$.
5. *Fulfillment Ratios (5)*: $\rho_k = \min\left(1.0, \frac{\text{FoodValue}_k}{\max(1.0, G_k)}\right)$.

To predict 7-day weight change, a 19-dimensional feature vector is built from user body biometrics, daily energy targets, and 7-day rolling intake averages (calories, protein, carbs, fat, sodium, sugar, fiber, and water).

---

## V. HOW THE SYSTEM RECOMMENDS MEALS

Rather than using a complicated mathematical black box, MealMentor recommends foods through a clear, transparent two-stage process that prioritizes health safety first, and then optimizes for taste, variety, and nutrient balance.

### A. Step 1: Setting Daily Targets and Finding Open Shortages
When a user sets up their profile, the app calculates resting energy expenditure using the clinical Mifflin–St Jeor formula [8]:
$$\text{BMR} = 10 \cdot m + 6.25 \cdot h - 5 \cdot a + s \tag{1}$$
where $m$ is weight in kg, $h$ is height in cm, $a$ is age in years, and $s \in \{+5, -161, 0\}$ is the sex adjustment factor. Total daily expenditure scales BMR using activity multiplier $f_{\text{act}} \in [1.20, 1.90]$ matched from Indian job roles:
$$\text{TDEE} = \text{BMR} \times f_{\text{act}} \tag{2}$$
Target calories adjust TDEE by health goal ($\Delta_{\text{goal}} = -500\text{ kcal}$ for weight loss, $+500\text{ kcal}$ for weight gain, $+250\text{ kcal}$ for muscle building) with a safe minimum floor of 1200 kcal for women and 1500 kcal for men:
$$T_{\text{calories}} = \max(1200, \text{round}(\text{TDEE} + \Delta_{\text{goal}})) \tag{3}$$
Specific limits are then applied for medical conditions: sodium is capped at $\le 1500\text{ mg}$ for hypertension [14], and added sugars are capped at $\le 25\text{ g}$ with carbs limited to $40\%$ for diabetes [13].

Whenever a meal is logged, consumed quantities $C_k$ are subtracted from daily goals $T_k$ to find active open shortages $G_k$:
$$C_k = \sum_{i \in \text{Logs}} \left( \frac{q_i}{100} \cdot N_{i,k} \right), \quad G_k = \max(0, T_k - C_k) \tag{4}$$
Nutrients with larger percentage gaps are automatically given higher priority.

### B. Step 2: Strict Safety Filtering (Stage 1)
Before scoring any dishes, MealMentor filters out any food that violates safety rules:
- Any dish containing ingredients the user is allergic to is eliminated immediately.
- Any meat dish is removed if the user is vegetarian or vegan.
- Any dish whose minimum portion exceeds the user's per-meal budget is discarded.
- Dishes inappropriate for the current meal occasion (e.g., breakfast vs. dinner) are removed.

### C. Step 3: Multi-Factor Scoring and Machine Learning Ranking (Stage 2)
Surviving safe dishes are evaluated based on how well they satisfy open nutrient shortages, match user taste preferences, stay within budget, and offer fresh variety. To prevent meal boredom, a 14-day variety discount is applied:
$$S_{\text{variety}}(f) = 
\begin{cases} 
1.0 - \left(\frac{14 - \tau_f}{14}\right) \times 0.50, & \text{if } \tau_f \le 14 \\
1.0, & \text{if } \tau_f > 14 \text{ or unlogged}
\end{cases} \tag{5}$$
where $\tau_f$ is days elapsed since the dish was last eaten.

Next, an XGBoost learning-to-rank model (`XGBRanker`) takes the 25-dimensional gap feature vector for each candidate dish and predicts its ranking score, maximizing Normalized Discounted Cumulative Gain (NDCG) [11], [15]:
$$\text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}, \quad \text{DCG@K} = \sum_{j=1}^K \frac{2^{r_j} - 1}{\log_2(j + 1)} \tag{6}$$
If the machine learning service is offline, the app smoothly falls back to the deterministic rule score, ensuring recommendations are always available without internet dependence.

### D. Step 4: Smart Portion Sizing and Clear Explanations
Once the best dish is selected, its portion mass $q_f$ is automatically sized between 50 g and 250 g to fill the user's primary nutrient deficiency $k^*$:
$$q_f = \text{clamp}\left( \text{round}\left( \frac{G_{k^*}}{N_{f,k^*}} \times 100 \right), 50\text{ g}, 250\text{ g} \right) \tag{7}$$
ensuring the cost stays within the per-meal budget. The app displays the recommended portion alongside a clear, plain-English reason explaining why this meal was picked (e.g., "Recommended because you still need 28g of protein today").

---

## VI. CORE FEATURES OF MEALMENTOR

MealMentor unites fifteen clear, fully implemented features:

1. **User Login & Security**: Protects user accounts with HTTP-only session cookies, strong Node.js password hashing via `scrypt`, constant-time password verification to prevent timing attacks, Google login, and a 30 req/min rate limiter.
2. **User Profile & Job Matching**: Records user biometrics, diet preferences, and allergies, and uses a smart text matcher for Indian occupations (such as teacher, driver, or nurse) to automatically set physical activity levels ($1.2–1.9$).
3. **Energy Expenditure Engine**: Computes BMR and daily calorie goals tailored to weight loss, muscle building, or maintenance, with a safe minimum floor (1200 kcal for women, 1500 kcal for men).
4. **Condition-Specific Targets**: Sets protein goals ($1.6\text{ g/kg}$ for muscle gain, $1.2\text{ g/kg}$ for weight loss or diabetes, $0.8\text{ g/kg}$ baseline), limits carbs for diabetes ($40\%$), and sets safe ceilings for salt and sugar.
5. **Live 10-Nutrient Gap Tracker**: Continuously tracks consumption across 10 nutrients, displaying clean progress bars with 5-tier colored status alerts.
6. **Easy Multimodal Meal Logging**:
   - *Plate Photo Logging*: Users snap a photo; Gemini Vision identifies foods, estimates portion size in grams, and links to verified database nutrition.
   - *Barcode Scanner*: Scans packaged snacks instantly using an offline cache of 500 items ($<5\text{ ms}$ response) or queries OpenFoodFacts.
   - *Voice Logging*: Uses native browser speech recognition (Web Speech API) with wake words ("Hey MealMentor") for hands-free meal journaling.
7. **Safe Two-Stage Recommendation**: Eliminates allergen and budget conflicts in Stage 1, and uses multi-factor scoring with XGBoost ranking in Stage 2.
8. **Smart Portion Sizer & Explanation**: Sizes meals between 50 g and 250 g to solve the biggest nutrient deficiency and gives plain-English explanations.
9. **7-Day Weight Prediction with Honest Gating**: Uses Random Forest regression to predict weight changes over seven days ($\Delta W$), withholding predictions (HTTP 409) until at least 5 verified user logs exist to prevent made-up numbers.
10. **Intermittent Fasting & Meal Timing**: Tracks fasting windows (e.g., 16:8 schedule from 12:00 PM to 8:00 PM) and sends reminders when eating windows open or close.
11. **Daily Water Tracker**: Computes water targets based on body weight ($H_{\text{target}} = m\text{ [kg]} \times 35\text{ ml}$), supports one-tap logging (ml, cups, liters), and tracks daily hydration streaks.
12. **Helpful Habit Reminders**: Sends timely alerts for skipped meals ($>3\text{h}$ delay), low afternoon water intake ($<60\%$), or high-carb meals ($>70\%$).
13. **Automatic Grocery Shopping List**: Turns weekly meal plans into a consolidated shopping list linked to 331 local grocery items, calculating the estimated cost in Indian Rupees (₹).
14. **Custom Recipes & Sharing**: Lets users create custom home recipes with auto-calculated nutrition and share them via unique web links.
15. **24/7 AI Chat Assistant**: Combines Google Gemini for detailed nutrition Q&A with a $<5\text{ ms}$ offline fallback engine that answers questions even without an internet connection.

---

## VII. EVALUATION AND RESULTS

### A. Automated Formula Test Suites
Eleven automated test suites (covering BMR, calorie targets, macro/micro allocations, 10-nutrient gaps, portion sizing, budget rules, meal timing, Indian job matching, rate limits, and intake flows) verified that every calculation matches analytical formulas with 0% error.

### B. XGBoost Ranking Performance
The XGBoost ranking model was trained across 120 synthetic user cohorts (46,080 food interaction pairs) split into 96 training groups and 24 held-out test groups (`n_estimators=100`, `learning_rate=0.1`, `max_depth=5`, objective `'rank:ndcg'`).

**TABLE II: XGBOOST FOOD RANKING PERFORMANCE ON TEST GROUPS**

| Metric | XGBRanker | Rule Baseline | Improvement |
|:---|:---|:---|:---|
| **NDCG@1** | **1.0000** | 0.8842 | $+13.09\%$ |
| **NDCG@3** | **1.0000** | 0.8915 | $+12.17\%$ |
| **NDCG@5** | **1.0000** | 0.9024 | $+10.81\%$ |
| **Mean Average Precision (MAP)** | **0.4886** | 0.4120 | $+18.59\%$ |
| **Precision@5** | **0.5000** | 0.4375 | $+14.28\%$ |
| **Cohorts** | \multicolumn{3}{c}{96 Training Groups (36,864) / 24 Test Groups (9,216)} |

### C. 7-Day Weight Forecasting Evaluation
The Random Forest model was trained on 120 verified 7-day intervals from 20 diverse user cohorts (140 weight entries, 2,520 meal logs). We used an 80/20 user-grouped split (16 train / 4 test users) so that data from the same person never appeared in both training and testing sets (`n_estimators=300`, `min_samples_leaf=2`, `min_samples_split=5`):
- **Mean Absolute Error (MAE)**: **0.1225 kg** (target $\le 0.50\text{ kg}$).
- **Root Mean Squared Error (RMSE)**: **0.1522 kg**.
- **Test Goodness of Fit ($R^2$)**: **0.5616**.
- **5-Fold GroupKFold Cross-Validation $R^2$**: **0.6148** ($\pm 0.354$).

**TABLE III: SYSTEM LATENCY AND TARGET METRIC VERIFICATION**

| Metric | Target Goal | Achieved Result | Status |
|:---|:---|:---|:---|
| **Offline AI Chat Speed** | $< 5\text{ ms}$ | $< 5\text{ ms}$ | Exceeded |
| **XGBoost Ranking Speed** | $< 10\text{ ms}$ | $< 10\text{ ms}$ | Achieved |
| **Meal Plan Database Query** | Single DB pass | Single DB pass | Achieved |
| **API Rate Limiting** | 30 req/min/IP | Enforced | Achieved |
| **Portion Sizing Bounds** | 50–250 g | 50–250 g | Achieved |
| **Budget Calculation Errors** | 0 | 0 | Achieved |
| **Weight Forecast MAE** | $\le 0.50\text{ kg}$ | **0.1225 kg** | **Achieved** |
| **Weight Forecast $R^2$** | $\ge 0.50$ | **0.5616** | **Achieved** |
| **Target Nutrient Coverage** | $\ge 75\%$ | **100.0%** | **Achieved** |

### D. 15-User Empirical Study
We tested the platform with fifteen diverse participants across 315 meal decisions over a 7-day period:
1. **Safety & Compliance**: 100.0% safety (zero allergen breaches, zero dietary conflicts).
2. **Portion Compliance**: 100.0% of suggested meals stayed within 50–250 g.
3. **Meal Variety**: 38.1% unique dishes across 21 meals per person over the week.
4. **Nutrient Satisfaction**: 100.0% of users met at least $80\%$ of their daily targets, achieving an overall user satisfaction score of **4.26 out of 5.00**.

### E. Real-World Case Study Walkthrough
Consider a 30-year-old woman ($h = 155\text{ cm}$, $m = 58\text{ kg}$, light activity) who wants to lose weight while managing Type 2 diabetes. After logging a lunch of rice and dal (450 kcal, 12 g protein, 75 g carbs, 350 mg sodium):
- $\text{BMR} = 10(58) + 6.25(155) - 5(30) - 161 = 1237.75\text{ kcal}$.
- $\text{TDEE} = 1237.75 \times 1.375 = 1701.91\text{ kcal}$.
- Calorie Goal $= \max(1200, 1701.91 - 500) = 1201.91\text{ kcal}$.
- Daily Water Goal $= 58 \times 35 = 2030\text{ ml}$.
- Open Deficits for Dinner: Protein shortage $= 38.0\text{ g}$, Calorie balance $= 751.9\text{ kcal}$, Remaining sugar allowance $\le 21\text{ g}$.

At 3:30 PM, the system notices she has only logged 600 ml of water and sends a friendly hydration reminder. For dinner, non-vegetarian and allergen foods are filtered out in Stage 1. The XGBoost model recommends *Paneer Bhurji*, sized to $150\text{ g}$ ($270\text{ kcal}$, $21.8\text{ g}$ protein, costing ₹33). The app clearly tells her the dish was picked to help fill her 38 g protein deficit, while the Random Forest service estimates a 7-day weight loss of $-0.42\text{ kg}$. The required ingredients for the week are automatically added to her grocery checklist.

---

## VIII. DISCUSSION AND LIMITATIONS

### A. Educational and Lifestyle Scope
MealMentor is intended as an everyday dietary awareness and decision-support assistant. It does not provide medical diagnoses or replace clinical dietitians. The formulas provide reliable population estimates, but individual metabolism can vary based on hormones and body composition.

### B. Real-World Considerations
1. *Self-Reporting Accuracy*: The system relies on users logging meals honestly; forgetting snacks can make remaining nutrient calculations slightly less accurate.
2. *Photo Portion Estimation*: While Gemini Vision identifies food items accurately, guessing portion weight from a 2D camera photo has a typical variation of $\pm 20\%$. Users can quickly confirm or adjust the weight before saving.
3. *Catalog Size*: Our database contains 384 popular Indian dishes and 331 supermarket items, which will expand to cover other international cuisines over time.

---

## IX. CONCLUSION
In this paper, we presented **MealMentor (NutriSense AI)**, a practical, AI-driven nutrition assistant that combines dependable physiological formulas with machine learning and healthy daily routines. By separating hard safety rules (allergens, dietary ethics, and medical limits) from ranking algorithms, MealMentor ensures that suggestions are always safe, appropriate, and medically sensible.

The platform combines Mifflin–St Jeor energy calculations and Indian job matching with real-time tracking across 10 nutrients. An XGBoost ranker re-orders the best meals (NDCG@5 = 1.0000), while a Random Forest model predicts 7-day weight trends (MAE = 0.1225 kg). Easy logging via plate photos, barcodes, and voice removes everyday journaling hassle. With built-in intermittent fasting clocks, water tracking, helpful reminders, and smart grocery shopping lists, MealMentor provides an all-in-one assistant for healthier living.

Future work includes connecting wearable fitness bands (Apple HealthKit and Google Health Connect), running lightweight vision models directly on phones without an internet connection, and linking shopping lists to online grocery delivery services.

---

## REFERENCES
[1] X. Deng and W. Tu, "Personalized nutrition-aware dietary recommendation with multimodal large language models," *IEEE Access*, vol. 14, pp. 21791–21804, 2026.

[2] J. N. Bondevik, K. E. Bennin, O. Babur, and C. Ersch, "A systematic review on food recommender systems," *Expert Systems with Applications*, vol. 238, Art. no. 122166, 2024.

[3] Y. Chen, A. Subburathinam, C.-H. Chen, and M. J. Zaki, "Personalized food recommendation as constrained question answering over a large-scale food knowledge graph," in *Proc. 14th ACM Int. Conf. Web Search and Data Mining (WSDM)*, 2021, pp. 544–552.

[4] S. Rendle, C. Freudenthaler, and L. Schmidt-Thieme, "Factorizing personalized Markov chains for next-basket recommendation," in *Proc. 19th Int. Conf. World Wide Web (WWW)*, 2010, pp. 811–820.

[5] W.-C. Kang and J. McAuley, "Self-attentive sequential recommendation," in *Proc. IEEE Int. Conf. Data Mining (ICDM)*, 2018, pp. 197–206.

[6] F. Sun et al., "BERT4Rec: Sequential recommendation with bidirectional encoder representations from transformer," in *Proc. 28th ACM CIKM*, 2019, pp. 1441–1450.

[7] M. Rostami, M. Oussalah, and V. Farrahi, "A novel time-aware food recommender-system based on deep learning and graph clustering," *IEEE Access*, vol. 10, pp. 52508–52524, 2022.

[8] M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty, and Y. O. Koh, "A new predictive equation for resting energy expenditure in healthy individuals," *The American Journal of Clinical Nutrition*, vol. 51, no. 2, pp. 241–247, 1990.

[9] J. H. Guo, Z. Li, L. Y. Yao, Y. W. Zhang, and T. Q. Pan, "Dietary recommendation systems: A comprehensive survey," *ACM Computing Surveys*, vol. 56, no. 4, pp. 1–40, 2023.

[10] R. K. Johnson and P. R. Trexler, "Practical applications of nutritional assessment in clinical dietetics," *Journal of the Academy of Nutrition and Dietetics*, vol. 112, no. 2, pp. 220–230, 2012.

[11] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, 2016, pp. 785–794.

[12] L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.

[13] World Health Organization, *Guideline: Sugars Intake for Adults and Children*, Geneva: World Health Organization, 2015.

[14] P. K. Whelton et al., "2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults," *Journal of the American College of Cardiology*, vol. 71, no. 19, pp. e127–e248, 2018.

[15] C. Burges et al., "Learning to rank using gradient descent," in *Proc. 22nd Int. Conf. Machine Learning (ICML)*, 2005, pp. 89–96.
