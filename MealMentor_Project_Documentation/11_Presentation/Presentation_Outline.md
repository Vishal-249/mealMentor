# MealMentor — Presentation Outline and Speaker Notes

## Presentation Structure (20 Slides)

---

### Slide 1: Title Slide
**Title**: MealMentor (NutriSense AI) — An AI-Powered Personalized Nutrition Tracking and Meal Planning System

**Subtitle**: Final Year B.E./B.Tech Computer Science Project

**Content to Show**:
- Project name and subtitle
- Team names and roll numbers
- Institution name and department
- Academic year (2025–2026)
- Guide's name

**Speaker Notes**: "Good morning/afternoon. Our project is called MealMentor — a personalized nutrition tracking and meal planning system powered by machine learning and AI."

---

### Slide 2: Problem Statement
**Title**: The Problem We're Solving

**Content (3 bullet points)**:
- 📊 **Generic advice**: Most nutrition apps provide one-size-fits-all meal plans that ignore personal physiology, food preferences, allergies, and budget
- ⏰ **Manual tracking is difficult**: Logging every food item manually is tedious — most users quit within a week
- 🔍 **No real-time gap analysis**: Users don't know which specific nutrients they're missing mid-day, making informed food choices impossible

**Speaker Notes**: "The core problem is that existing nutrition apps either track what you eat — without telling you what to eat next — or they give you generic advice that ignores who you are as an individual. We set out to build a system that does both."

---

### Slide 3: Proposed Solution
**Title**: MealMentor — What We Built

**Content (3 columns or cards)**:
- 🧮 **Smart Calculations**: BMR, TDEE, and personalized nutrient targets using the Mifflin–St Jeor equation
- 🤖 **AI Recommendations**: Two-stage pipeline — Rule-based filtering + XGBoost learning-to-rank
- 📷 **AI Vision**: Google Gemini Vision for food photo nutrition analysis

**Speaker Notes**: "MealMentor solves this with three core pillars: mathematically accurate nutrition targets, AI-powered personalized meal recommendations, and computer vision for photo-based food recognition."

---

### Slide 4: System Architecture
**Title**: System Architecture Overview

**Content**: Architecture diagram showing:
- Browser (Next.js React frontend)
- Next.js API Server
- MongoDB Database
- Python ML Layer (XGBoost)
- FastAPI Backend (Random Forest)
- External APIs: Gemini, OpenFoodFacts, Google OAuth

**Speaker Notes**: "The system uses a three-tier architecture. The Next.js application handles both the frontend and the API server. MongoDB stores all user data. A Python ML layer handles XGBoost food ranking and a separate FastAPI service handles weight forecasting."

---

### Slide 5: Technology Stack
**Title**: Technology Stack

**Content**: Two-column table showing:

| Frontend | Backend |
|----------|---------|
| Next.js 16 (App Router) | MongoDB + Mongoose |
| React 19 + TypeScript | JWT Auth (jose + scrypt) |
| Tailwind CSS 4 + Shadcn/ui | Rate Limiting |
| Recharts (charts) | Python 3.11 |
| Sonner (notifications) | XGBoost + scikit-learn |
| Zod (validation) | FastAPI + uvicorn |

**Speaker Notes**: "The frontend is built with Next.js 16 using the App Router with React 19 and TypeScript. The backend is MongoDB with Mongoose ODM. The ML layer uses Python with XGBoost for ranking and FastAPI with Random Forest for weight forecasting."

---

### Slide 6: Database Design
**Title**: Database Design — MongoDB Collections

**Content**: ER Diagram or collection list:
- **users** — profile, authentication, preferences
- **foods** — 383-item nutrition dataset
- **mealentries** — daily food logs with nutrition snapshots
- **weightlogs** — weight history
- **feedbacks** — food likes/dislikes
- **generatedmeals** — cached daily meal recommendations
- **foodphotos** — Gemini Vision analysis results

**Speaker Notes**: "We use 14 MongoDB collections. Key design decisions include storing nutrition value snapshots in meal entries — this means past logs are not affected if food data is updated later."

---

### Slide 7: Dataset
**Title**: Food Nutrition Dataset

**Content**:
- **finalDatasetfood.csv**: 383 Indian food items with 14 nutritional attributes
- **finalDatasetGrocery.csv**: 331 grocery ingredients with pricing
- Dataset is seeded to MongoDB and used as the source of truth for all nutrition values

**Table showing sample records**:
| Dish Name | Type | Meal | Price/100g | Cal | Protein | Fat |
|-----------|------|------|-----------|-----|---------|-----|
| Achappam | Veg | Snack | ₹24.0 | 293 | 4.7g | 10.4g |
| Dal Makhani | Veg | Dinner | ₹22.0 | 187 | 8.9g | 8.2g |

**Speaker Notes**: "Our food dataset contains 383 Indian dishes with complete nutritional profiles — calories, macros, and micronutrients including calcium, iron, and vitamin C, all per 100 grams."

---

### Slide 8: Nutrition Calculation Engine
**Title**: How We Calculate Your Nutrition Targets

**Content**: Step-by-step formula chain with numbers:

```
Step 1 — BMR (Mifflin–St Jeor):
Male, 25y, 70kg, 175cm:
(10×70) + (6.25×175) - (5×25) + 5 = 1673.75 kcal

Step 2 — TDEE (Activity Multiplier):
Moderate activity (×1.55):
1673.75 × 1.55 = 2594.31 kcal

Step 3 — Goal Adjustment:
Weight loss (-500): 2594.31 - 500 = 2094 kcal

Step 4 — Macros:
Protein: 70 × 1.2 = 84g | Carbs: 2094×50%÷4 = 262g | Fat: 79g
```

**Speaker Notes**: "The nutrition engine uses the Mifflin–St Jeor equation to calculate BMR, multiplies by an activity factor to get TDEE, then adjusts for the health goal. Macros are calculated from the calorie target using evidence-based ratios."

---

### Slide 9: Recommendation Engine
**Title**: AI Meal Recommendation Pipeline

**Content**: Two-stage pipeline diagram:

```
Stage 1: Rule-Based Filtering & Scoring
├── Hard filter: allergies, dietary preferences, health conditions
├── Budget filter: cost per minimum portion
├── 14-day no-repeat exclusion
└── Score: nutrient gap fill × adaptive weights - penalties

Stage 2: XGBoost Learning-to-Rank
├── Feature matrix: calories, protein, carbs, fat, fiber + gap ratios
├── XGBRanker (rank:ndcg, 100 estimators, depth 5)
├── Logistic transform → (0,1) score
└── Sort descending → Top-N recommendations
```

**Speaker Notes**: "Recommendations use a two-stage pipeline. First, rule-based filtering removes ineligible foods and scores the rest by how well they fill the user's remaining nutrient gaps. Then an XGBoost learning-to-rank model re-orders these candidates using learned patterns."

---

### Slide 10: XGBoost Model Details
**Title**: XGBoost Learning-to-Rank

**Content**:
- **Objective**: rank:ndcg (Normalized Discounted Cumulative Gain)
- **Training**: 120 synthetic user queries × 383 foods = 45,960 (query, food) pairs
- **Labeling**: 0–4 relevance from rule-based gap-fit formula (no random labels)
- **Split**: Group-aware 80/20 (prevents data leakage between queries)
- **Hyperparameters**: n_estimators=100, learning_rate=0.1, max_depth=5
- **Inference**: <10ms per candidate set
- **Fallback**: Rule-based scoring if model unavailable

**Speaker Notes**: "The XGBoost model was trained with synthetic user queries that cover diverse nutritional needs. Labels come from the same rule-based formula — not random — so the model learns meaningful relationships. Crucially, the model only learns ranking, not nutrition values."

---

### Slide 11: Food Photo Analysis
**Title**: AI Food Photo Recognition — Gemini Vision

**Content**: Flow diagram:
1. User uploads food photo → base64 encoded
2. Sent to Gemini Vision API with structured prompt
3. AI returns: food names, portion grams, per-100g nutrition
4. Values parsed, sanitized, and scaled to actual portion
5. User confirms → logged to food diary

**Screenshot** of the food photo analysis result screen

**Speaker Notes**: "Users can photograph their meal and let Gemini Vision AI automatically identify foods and estimate nutrition. The system displays confidence scores and lets users correct estimates before logging."

---

### Slide 12: AI Nutrition Chatbot
**Title**: AI Nutrition Assistant

**Content**: Chat screenshot showing:
- User question: "What should I eat for dinner to hit my protein target?"
- AI response with personalized advice based on current intake and remaining gaps

**Features listed**:
- Context: user profile + today's intake injected into every query
- Primary: Google Gemini (gemini-3.8-flash)
- Fallback: Local deterministic engine (always works, no API needed)
- 2.5 second SLA timeout

**Speaker Notes**: "The AI chatbot has full context of the user's profile and today's intake. It answers questions like 'how much protein do I still need' or 'explain my BMR' with personalized responses. If Gemini is unavailable, the local engine handles common questions correctly."

---

### Slide 13: Additional AI Features
**Title**: Additional Smart Features

**Three-column layout**:
- **Barcode Scanning**: Camera-based EAN barcode scanner using Quagga2 + OpenFoodFacts API with ~500 product offline cache
- **Voice Input**: Web Speech API with wake word detection ("Hey MealMentor") — recognizes log_meal, navigate, daily_summary, suggest_recipe, chat intents
- **7-Day Weight Forecast**: Random Forest regression (FastAPI backend) predicts weight change from 19 biometric + intake features

**Speaker Notes**: "Beyond the main recommendation and tracking features, MealMentor includes barcode scanning for packaged foods, voice-based meal logging, and a 7-day weight change prediction."

---

### Slide 14: Security Implementation
**Title**: Security Architecture

**Content**:
| Security Feature | Implementation |
|-----------------|---------------|
| Password Hashing | Node.js scrypt (memory-hard) + random salt + timingSafeEqual |
| Authentication | JWT (HS256, jose) in HTTP-only cookie, 7-day expiry |
| Session Invalidation | tokenVersion incremented on password change |
| Password Reset | SHA-256 hashed token + 1-hour expiry |
| Rate Limiting | Sliding-window bucket (30 req/60s per user+IP) |
| Data Isolation | All queries filtered by user._id |
| Input Validation | Zod schema + Mongoose constraints |

**Speaker Notes**: "Security is implemented at multiple layers. Passwords use memory-hard scrypt hashing. JWT sessions are stored in HTTP-only cookies to prevent XSS access. Token versioning invalidates all sessions on password change."

---

### Slide 15: System Screenshots (Dashboard + Nutrition)
**Title**: Application Screenshots — Dashboard and Nutrition Tracking

**Content**: Two side-by-side screenshots:
- Left: Main dashboard with calorie ring, macro bars, streak, hydration
- Right: Nutrition page with all 10 nutrient progress bars showing graded statuses

**Speaker Notes**: "Here is the main dashboard showing real-time calorie and macro tracking. The nutrition page shows all 10 nutrients with graded status indicators — Deficient, Low, Near-Target, Adequate, or Over."

---

### Slide 16: System Screenshots (Meal Plan + Food Tracking)
**Title**: Application Screenshots — Recommendations and Food Logging

**Content**: Two screenshots:
- Left: Meal plan page with recommendation cards
- Right: Food tracking page with search and today's log

**Speaker Notes**: "The meal plan page shows AI-generated recommendations with serving sizes, nutrition per serving, estimated cost, and like/dislike feedback buttons. The food tracking page allows searching the 383-item database."

---

### Slide 17: Testing
**Title**: Testing Strategy and Coverage

**Content**:
| Test Category | Tool | Count | Coverage |
|--------------|------|-------|---------|
| Unit Tests | Vitest | 29 test files | BMR/TDEE formulas, recommendation scoring, gap calculation, auth, streaks, hydration, voice intent, rate limiter |
| Integration Tests | Vitest | Part of 29 files | Food logging CRUD, XGBoost integration, barcode lookup, AI chat |
| E2E Tests | Playwright | 1 spec | Responsive design across breakpoints |

**Run commands**:
```bash
npm run test          # Vitest unit/integration
npm run test:e2e      # Playwright E2E
```

**Speaker Notes**: "The project includes 29 test files using Vitest covering all core algorithms including BMR formulas, recommendation scoring, and authentication. Playwright tests validate responsive design."

---

### Slide 18: Challenges and Solutions
**Title**: Key Challenges and How We Solved Them

**Three-card layout**:

**Challenge 1 — ML Cold Start**
"No real user data existed when building the recommendation system."
**Solution**: Synthetic query generation covering diverse nutritional scenarios; XGBoost learns from gap-fit formula patterns.

**Challenge 2 — Python-Node.js Integration**
"Integrating Python ML into a Next.js application without framework conflicts."
**Solution**: JSON over stdin/stdout subprocess communication with graceful fallback to rule-based TypeScript engine.

**Challenge 3 — Food Photo Accuracy**
"AI nutrition estimates for photos can vary significantly."
**Solution**: Confidence score display, manual correction interface, and the advice to confirm estimates before logging.

**Speaker Notes**: "Three major challenges defined our design decisions: cold-start ML, language interoperability, and AI estimation accuracy. Each solution is practical and honest about the system's limitations."

---

### Slide 19: Scope for Future Work
**Title**: Limitations and Future Enhancements

**Current Limitations**:
- 383-item dataset is primarily Indian cuisine
- XGBoost trained on synthetic data (not real user preferences)
- Weight forecast requires historical data and separate FastAPI service
- Not medically validated (estimates only)

**Future Enhancements**:
- Collaborative filtering from similar user profiles
- Regional Indian language support (Hindi, Tamil, Telugu)
- Wearable device integration (Apple Watch, Fitbit)
- Nutritionist-verified meal plan templates
- Restaurant menu integration

**Speaker Notes**: "We're transparent about limitations. The core ML pipeline works well, but real-world validation with actual user preference data would significantly improve recommendation quality. The architecture makes these enhancements straightforward to add."

---

### Slide 20: Conclusion and Takeaways
**Title**: Conclusion

**Achievement Summary**:
✅ BMR/TDEE/macro calculation engine (Mifflin–St Jeor)
✅ Two-stage AI recommendation pipeline (Rule-based + XGBoost)
✅ Food photo recognition (Gemini Vision)
✅ Barcode scanning (OpenFoodFacts)
✅ AI nutrition chatbot (Gemini + local fallback)
✅ 7-day weight forecast (Random Forest)
✅ Water tracking, streaks, proactive nudges
✅ Custom food creation with ingredient-level nutrition
✅ 29 test files with Vitest + Playwright

**Closing Quote**: "MealMentor transforms generic dietary advice into personalized, data-driven nutrition guidance — making healthy eating accessible, intelligent, and practical."

---

## Presentation Tips

1. **Time management**: 20 slides × ~1.5 min = ~30 minutes. Practice to ensure you finish within your allocated time.
2. **Demo readiness**: Have the app running locally (or on a deployed URL) before the presentation. Have sample food photos and a pre-filled profile ready.
3. **Dry runs**: Memorize the BMR dry-run calculation (Male 25y 70kg 175cm → BMR = 1673.75) — examiners often ask you to compute one live.
4. **Backup slides**: Prepare 3–4 extra backup slides with: algorithm pseudocode, ER diagram, API endpoint table, and model training details for deep-dive questions.
5. **Talking about AI honestly**: Always say "AI-estimated" not "AI-detected" for food photos. Say "personalized recommendation" not "AI prescribes" for the meal plan. Never claim medical validation.
