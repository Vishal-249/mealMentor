# MealMentor — Viva Preparation and Q&A Guide

## Part A: Project Explanation in Simple English

MealMentor is a smart nutrition tracking website that helps you eat healthier by:
1. **Knowing your body**: You enter your age, height, weight, and daily activity — the app calculates exactly how many calories and nutrients your body needs each day.
2. **Tracking what you eat**: You can search for foods, scan barcodes, or photograph your meal — the app calculates exactly how much protein, carbs, fat, fiber, calcium, iron, and vitamin C you consumed.
3. **Showing what's missing**: In real time, the app shows you which nutrients you still need for the day and which you've already met.
4. **Recommending what to eat next**: An AI system (combining rules and a machine learning model) suggests foods that will fill your remaining nutrient gaps, fit your food preference, and stay within your budget.
5. **Helping you chat**: You can ask a chatbot "what should I eat for dinner?" and it gives personalized advice based on your current intake.
6. **Tracking progress**: You can log your weight daily and see trends over time, with a 7-day weight prediction.

---

## Part B: One-Minute Project Introduction

"MealMentor, also called NutriSense AI, is a personalized nutrition tracking and meal planning web application. It is built using Next.js on the frontend and backend, MongoDB for data storage, and a Python machine learning layer using XGBoost. The app calculates your daily calorie and nutrient targets using the Mifflin–St Jeor BMR formula, adjusted for your activity level and health goal. It tracks every meal you log and shows you in real time which nutrients you still need. To recommend what to eat next, it uses a two-stage system: first, a rule-based algorithm filters and scores foods from a 383-item dataset based on your current nutrient gaps; then, a trained XGBoost ranking model re-orders the best options. You can also photograph food for AI recognition using Google Gemini Vision, chat with an AI nutritionist, scan product barcodes, and track water intake. The system is designed to be practical, accessible, and privacy-respecting, running most features locally with external AI as an enhancement."

---

## Part C: Three-Minute Project Explanation

"The problem we're solving is that existing nutrition apps either give generic advice or only track what you eat without telling you what to eat next. MealMentor addresses this by combining physiological calculations, machine learning, and AI vision into one coherent system.

The system starts with the user's profile — age, height, weight, gender, activity level, health goal, food preferences, allergies, and daily budget. From this, the backend calculates the Basal Metabolic Rate using the Mifflin–St Jeor equation, then multiplies by an activity factor to get the Total Daily Energy Expenditure. The calorie target is then adjusted for the user's goal — for example, a 500 calorie deficit for weight loss or a 250 surplus for muscle building.

When the user logs a meal — by searching, barcode scanning, or photographing — the app multiplies the per-100g nutrition values from the food dataset by the quantity consumed. For example, 150g of Idli at 39 calories per 100g gives 58.5 calories. This is summed across all meals to calculate today's intake.

The recommendation engine then computes nutrient gaps — what's still missing from the daily targets. It scores each food in the database by how efficiently it fills the most critical gaps, penalizing foods that are too calorie-dense, too sugary, or too salty. A trained XGBoost learning-to-rank model then re-orders these candidates to further personalize the ranking. The system also enforces a 14-day no-repeat rule and incorporates user feedback — liked foods get a score boost.

For food photos, the app sends the image to Google's Gemini Vision model, which returns estimated per-100g nutrition for each detected food item. The user can review and confirm before logging.

The AI chatbot uses the Gemini language model with the user's current profile and today's intake as context — but always falls back to a deterministic local engine if the API is unavailable.

Finally, a FastAPI-served Random Forest model predicts 7-day weight change based on recent nutrition history and the user's biometric profile."

---

## Part D: Five-Minute Demo Script

1. **Open the dashboard** (30 seconds): Show the main dashboard — "Here you can see my daily calorie ring showing 1,200 of my 2,094 calorie target consumed. The green bars show my macros, and the hydration tracker shows 800ml of my 2,450ml target. The streak shows I've logged for 5 consecutive days."

2. **Show nutrition targets** (30 seconds): Navigate to Nutrition page — "These graded progress bars show all 10 nutrients. Protein is 'Low' at 38% of target, fiber is 'Deficient'. The app identifies exactly what I need."

3. **Log a food item** (45 seconds): Go to Food Tracking → search "paneer tikka" → select 150g for lunch → show how calories and protein are calculated and the bars update in real time.

4. **Show meal recommendations** (60 seconds): Navigate to Meal Plan → "The system has recommended Dal Makhani for lunch because my protein gap is 40g and this food provides 8.9g protein per 100g at ₹18 per 100g. The XGBoost model ranked it highest considering my vegetarian preference and remaining budget. I can like it to boost future recommendations."

5. **Demonstrate food photo** (45 seconds): Go to Food Photo → upload a sample image → wait for analysis → show detected items with confidence scores and nutrition estimates.

6. **Ask the AI chatbot** (30 seconds): Go to AI Assistant → type "What should I eat for dinner to hit my protein target?" → show the personalized response with remaining protein deficit and food suggestions.

7. **Show progress charts** (30 seconds): Navigate to Progress → show weight history chart and 7-day nutrition summary chart → briefly mention the 7-day weight forecast card.

8. **Wrap up**: "MealMentor combines accurate physiological calculations, machine learning, and AI vision into a complete nutrition management system. All nutrition values come from a verified 383-item food dataset, and the ML models only personalize the recommendations — they don't fabricate nutrition values."

---

## Part E: Problem Statement and Solution in Simple Words

**The Problem**: When you try to eat healthier, you face three problems:
1. You don't know exactly how many calories and nutrients your specific body needs
2. You don't know which nutrients you're missing during the day
3. Generic meal suggestions don't fit your diet preferences, allergies, or budget

**The Solution**: MealMentor:
1. Calculates YOUR specific calorie needs using a medical formula (BMR + activity level + health goal)
2. Tracks every food you eat and shows you exactly what nutrients are still missing
3. Recommends foods that specifically fill your gaps, match your preferences, and fit your budget
4. Uses AI to let you photograph food and automatically get nutrition information
5. Lets you chat with an AI nutritionist about your specific diet questions

---

## Part F: Module-by-Module Explanations

**Module: BMR Calculation**
"BMR is how many calories your body burns just to stay alive — breathing, heartbeat, digestion — without any movement. We use the Mifflin–St Jeor formula: 10×weight + 6.25×height - 5×age + 5 for males, or -161 for females."

**Module: TDEE**
"TDEE is BMR multiplied by an activity factor. A sedentary person (desk job, no exercise) multiplies BMR by 1.2. A very active person (soldier, athlete) multiplies by 1.9. This gives the actual daily calorie burn."

**Module: Calorie Target**
"The calorie target is TDEE plus a goal adjustment. For weight loss, we subtract 500 calories. For weight gain, add 500. For muscle building, add 250. The minimum is always 1,200 kcal."

**Module: Food Logging**
"When you log 150g of paneer, we take the per-100g nutrition from the database and scale it: calories = 265 × (150/100) = 397.5 kcal. Same formula for every nutrient."

**Module: Recommendation Engine**
"The engine first removes foods that match your allergies, dietary restrictions, or recent meals. Then it scores each remaining food by how efficiently it fills your biggest nutrient gaps. The XGBoost model re-ranks these candidates based on learned patterns from synthetic training data. Finally, the serving size is calculated to close your most important gap."

**Module: Gemini Vision**
"We send the food photo to Google's Gemini multimodal AI with a structured prompt asking for specific nutrition estimates per 100g for each detected food. The model returns JSON, which we parse and scale by the estimated portion weight."

**Module: AI Chatbot**
"The chatbot receives your message plus a context document containing your profile, targets, and today's intake. It sends all this to Gemini and returns the response. If Gemini is unavailable, a local rule engine handles common questions about BMR, TDEE, protein gaps, and food suggestions — always successfully."

**Module: XGBoost Ranker**
"XGBoost is a gradient-boosted decision tree algorithm. We train it with synthetic 'user queries' (varied nutritional needs and gaps) paired with every food in our dataset, labeled 0-4 based on how well the food fits the query. The model learns which food features predict high suitability. At runtime, it re-ranks rule-filtered candidates by predicted suitability score."

---

## Part G: Technology Stack Explanations

**Next.js**: "A React framework that handles both the user interface and the server-side API in a single project. It uses the App Router with Server Components — parts of the UI render on the server, reducing load on the browser."

**MongoDB**: "A NoSQL database that stores data as JSON-like documents rather than rows in a table. This is ideal for our user profiles, which have optional and nested fields like meal timing preferences and macro splits."

**Mongoose**: "A library that defines schemas for MongoDB documents, adding TypeScript types and validation. For example, it ensures `weightKg` must be between 20 and 400 before saving."

**jose**: "A JavaScript library for JWT (JSON Web Token) authentication. JWTs are signed tokens stored in HTTP-only cookies that identify the logged-in user securely."

**XGBoost**: "An industry-leading gradient-boosted tree algorithm. We use its learning-to-rank variant (XGBRanker with rank:ndcg objective) which is specifically designed for ordering items by relevance — exactly what food recommendation needs."

**Gemini Vision**: "Google's multimodal AI model that can analyze both images and text. We send it a food photo with a structured prompt requesting nutrition values, and it returns a JSON object we can parse."

---

## Part H: Algorithm Dry Runs

**BMR Dry Run**:
Input: Male, 25 years, 70 kg, 175 cm
- base = (10×70) + (6.25×175) - (5×25) = 700 + 1093.75 - 125 = 1668.75
- BMR = 1668.75 + 5 = **1673.75 kcal/day**

**TDEE Dry Run**:
BMR = 1673.75, Activity = moderate (1.55)
- TDEE = 1673.75 × 1.55 = **2594.31 kcal/day**

**Calorie Target Dry Run**:
TDEE = 2594.31, Goal = weight-loss (-500)
- Target = max(1200, 2594.31 - 500) = max(1200, 2094.31) = **2094 kcal/day**

**Nutrient Intake Dry Run**:
Food: Achappam (protein = 4.7g per 100g), Quantity = 100g
- Protein consumed = (100/100) × 4.7 = **4.7g**

**Nutrient Gap Dry Run**:
Protein target = 84g, Protein consumed = 22g
- Protein gap = max(0, 84 - 22) = **62g remaining**

**Water Target Dry Run**:
Weight = 70 kg
- Target = 70 × 35 = **2450 ml/day**

---

## Part I: 50 Viva Questions with Answers

### Architecture Questions

**Q1. What is the overall architecture of MealMentor?**
A: MealMentor uses a three-tier architecture: (1) Next.js with React frontend for the user interface, (2) Next.js API routes as the backend server handling database operations, authentication, and ML integration, (3) MongoDB as the database. An optional fourth tier is the FastAPI Python backend for Random Forest weight forecasting. The ML layer uses Python subprocess spawn for XGBoost recommendations.

**Q2. Why did you choose Next.js instead of a separate React frontend and Express backend?**
A: Next.js integrates both frontend and API routes in a single project. Server Components reduce client-side JavaScript bundle size. Built-in API routes eliminate the need for a separate Express server. The App Router supports server-side rendering, streaming, and edge compatibility.

**Q3. What is the App Router in Next.js?**
A: The App Router is a file-system-based routing system in Next.js 13+. Files inside `app/` define routes. Route groups like `(auth)` and `(dashboard)` allow shared layouts without affecting the URL. Server Components run on the server and don't ship JavaScript to the browser unless marked "use client".

**Q4. How does the Python ML layer communicate with the Next.js application?**
A: Using process spawning (Node.js `child_process.spawn`). The Next.js API route spawns a Python script as a child process, sends a JSON payload over stdin, and reads the JSON result from stdout. This is handled in `src/lib/ml.ts → runScript()`. The timeout is 30 seconds. If the subprocess fails, the API falls back to the rule-based recommendation engine.

**Q5. What databases are used in this project?**
A: MongoDB, accessed via Mongoose ODM. MongoDB stores 14 collections: users, foods, mealentries, weightlogs, foodphotos, customfoods, feedbacks, generatedmeals, hydrationlogs, nudges, scannedbarcodes, groceryitems, aimodelversions, and aipredictionfeedbacks.

### Database Questions

**Q6. Why choose MongoDB over MySQL/PostgreSQL?**
A: MongoDB's flexible document model suits the varied user profile structure (with optional nested fields like meal timing preferences and macro splits). It scales horizontally and handles evolving schemas without migrations. The project stores JSON-structured nutrition data which maps naturally to MongoDB documents.

**Q7. What is Mongoose and why is it used?**
A: Mongoose is an Object Data Modeling (ODM) library for MongoDB and Node.js. It provides TypeScript-typed schema definitions, validation rules (required, enum, min, max), automatic timestamps, and compound indexes — making database interactions type-safe and consistent.

**Q8. How is data isolation ensured between users?**
A: Every database query includes a `user: user._id` filter. For example, `MealEntry.find({ user: user._id, date: {...} })`. This ensures one user cannot access another user's meal entries, weight logs, or photos.

**Q9. What indexes exist on the MealEntry collection?**
A: A compound index on `(user, date)` for efficient daily food log queries. This allows `MealEntry.find({ user: X, date: { $gte: startOfDay, $lte: endOfDay } })` to run without a full collection scan.

**Q10. What is the food dataset, and how is it structured?**
A: `finalDatasetfood.csv` contains 383 food items with 14 columns: Dish_Name, Food_Type (veg/non-veg/vegan), Meal_Type, Price_per_100g, Calories, Carbs_g, Protein_g, Fat_g, Fibre_g, Sugar(g), Sodium(mg), Calcium(mg), Iron(mg), Vit C(mg). All nutrition values are per 100g. The dataset is seeded to MongoDB for production use.

### Algorithm Questions

**Q11. What BMR formula does MealMentor use?**
A: The Mifflin–St Jeor equation. For males: (10×weight) + (6.25×height) - (5×age) + 5. For females: (10×weight) + (6.25×height) - (5×age) - 161. For "other" gender: no sex adjustment. Source: `src/lib/nutrition.ts → calcBMR()`.

**Q12. How is the TDEE calculated?**
A: TDEE = BMR × Activity Factor. The activity factors are: sedentary=1.2, light=1.375, moderate=1.55, active=1.725, very-active=1.9. These are standard Harris-Benedict-style multipliers. Source: `src/lib/nutrition.ts → calcTDEE()`.

**Q13. How are calorie targets adjusted for health goals?**
A: Weight-loss subtracts 500 kcal, weight-gain adds 500, muscle-building adds 250, maintain-weight/improve-energy/healthy-lifestyle add 0. The result is always floored at 1200 kcal minimum. Source: `GOAL_DELTA` constant in `src/lib/nutrition.ts`.

**Q14. How is protein target calculated?**
A: Using a body-weight-based factor multiplied by body weight in kg. The factor is 1.6 g/kg for muscle-building, 1.2 g/kg for weight-loss or diabetes, 1.0 g/kg for weight-gain, and 0.8 g/kg for others. Minimum is 40g. Source: `calcProteinFactor()` in `src/lib/nutrition.ts`.

**Q15. How does the recommendation scoring algorithm work?**
A: For each food in the database, the engine calculates a "fill efficiency" for each gap nutrient (protein, fiber, calcium, iron, vitamin C) — how much of the remaining gap 100g of that food covers, capped at 1. These are weighted by adaptive gap-importance weights (nutrients with bigger gaps get higher weights). Penalties are applied for calorie density, high sugar, and high sodium. The XGBoost model then re-ranks the top candidates.

**Q16. What is the serving size optimization?**
A: The engine selects the serving size that closes the user's most important gap for that food. For example, if protein gap is 40g and the food has 10g protein per 100g, the ideal serving is 400g. This is clamped to 50g–250g. If the food is expensive and the remaining budget is limited, the serving is further reduced.

**Q17. What is the 14-day no-repeat rule?**
A: Foods that appear in the user's meal history within the past 14 days are hard-excluded from recommendations. This prevents the same meal from being suggested repeatedly. If this exclusion leaves too few options, the least-recently-eaten excluded foods are re-admitted as fallback candidates with a recency-based score discount.

**Q18. How does the system handle health conditions?**
A: Diabetes: sugar limit is reduced from 50g to 30g/day; carb percentage reduced from 50% to 40% of calories; protein factor increased to 1.2. Hypertension: sodium limit reduced from 2300mg to 1500mg/day. Foods with high sugar (>15g/100g) or high sodium (>400mg/100g) are rejected for users with these conditions.

### AI/ML Questions

**Q19. What is XGBoost?**
A: XGBoost (Extreme Gradient Boosting) is a scalable, distributed gradient-boosted decision tree algorithm. It builds an ensemble of decision trees sequentially, where each tree corrects the errors of the previous one. The learning-to-rank variant (XGBRanker) is specifically designed to order items by relevance.

**Q20. How was the XGBoost model trained?**
A: 120 synthetic "user queries" were generated with varied calorie/protein/carb/fat/fiber targets and gaps. For each query, every food in the dataset was labeled with a 0-4 relevance score using the rule-based gap-fit logic. The model was trained with these labeled (query, food) pairs using rank:ndcg objective. Training used 80% of query groups, testing on the remaining 20%.

**Q21. What is NDCG and why is it used as the training objective?**
A: NDCG (Normalized Discounted Cumulative Gain) measures ranking quality by rewarding relevant items ranked at the top more than relevant items ranked lower. It's the standard metric for learning-to-rank problems because it directly measures whether the most suitable items appear first.

**Q22. What is the Random Forest used for?**
A: Random Forest regression is used for 7-day weight change prediction. The FastAPI backend receives 19 features (user biometrics, calculated targets, and 7-day average intake) and returns a predicted weight change in kg. It uses honest gating — returns {available: false} if the model hasn't been trained or there's insufficient historical data.

**Q23. What is Gemini Vision and how is it integrated?**
A: Gemini Vision is Google's multimodal AI that processes both images and text. The integration sends the food photo as a base64-encoded image along with a structured prompt via the Generative Language API. The prompt instructs Gemini to return JSON with food names, portion grams, and per-100g nutrition values. The response is parsed and sanitized in `src/lib/gemini-vision.ts`.

**Q24. What happens if the Gemini API is unavailable?**
A: For the chatbot: the local deterministic engine (`generateContextualReply()`) handles common nutrition questions. For food photo analysis: an error is returned (the feature requires the API). For vision: a fallback model chain (gemini-3.8-flash → gemini-3.8-flash-lite) handles 503 overloads.

**Q25. Is the XGBoost model making nutrition value predictions?**
A: No. The XGBoost ranker only predicts ranking scores (suitability order) — it does not predict nutrition values. All nutrition values come directly from the food dataset. The model only decides which order to present the foods in.

### Security Questions

**Q26. How are passwords stored?**
A: Using Node.js's built-in `crypto.scrypt` function with a 16-byte random salt and 64-byte key length. The stored format is `salt:derivedKey` (both hex-encoded). The scrypt algorithm is memory-hard, making brute-force attacks computationally expensive.

**Q27. Why not use bcrypt?**
A: The implementation uses Node.js built-in `scrypt` instead of a third-party bcrypt library. Scrypt is similarly memory-hard to bcrypt and requires no external dependency — Node.js crypto is trusted and maintained by the Node.js project.

**Q28. How is timing attack prevention implemented?**
A: The `crypto.timingSafeEqual()` function is used for password comparison. Regular string comparison (===) exits early on the first mismatched character, revealing timing information about how close the guess was. `timingSafeEqual` always takes the same amount of time regardless of where a mismatch occurs.

**Q29. What is the tokenVersion field and why is it used?**
A: `tokenVersion` is an integer stored in the User document. It is included in the JWT payload. When the user changes their password, `tokenVersion` is incremented. Any existing JWTs with the old version number are rejected by `getCurrentUser()`, effectively invalidating all previous sessions on password change.

**Q30. How does the rate limiter work?**
A: An in-memory sliding-window bucket algorithm is implemented in `src/lib/rate-limit.ts`. Each request creates or updates a bucket keyed by user ID + IP. If the bucket's count exceeds the limit within the window (e.g., 30 requests per 60 seconds), the request is rejected with HTTP 429. The bucket automatically expires after the window. A max of 10,000 buckets are maintained to prevent memory exhaustion.

### Frontend Questions

**Q31. What is the difference between Server Components and Client Components in Next.js?**
A: Server Components run on the server and send only HTML to the browser — they cannot have event handlers or browser APIs. They can directly access databases and environment variables. Client Components are marked with "use client" and run in the browser — they can use useState, useEffect, onClick, and browser APIs like the Web Speech API for voice input.

**Q32. What charting library is used and for what?**
A: Recharts is used for all data visualizations: line charts for weight history, area charts for 7-day nutrition history, and progress bar visualizations for daily nutrient intake tracking.

**Q33. How is form validation implemented?**
A: Zod schema validation is used both on the frontend (before submission) and in API routes (before database operations). Mongoose schema constraints (required, enum, min, max) provide a final validation layer at the database level.

**Q34. How is the theme (dark/light mode) implemented?**
A: A theme toggle component reads and writes a localStorage preference and applies a CSS class to the root element. CSS custom properties (variables) are used for all colors, so switching the class updates the entire color palette.

### Testing Questions

**Q35. What testing framework is used?**
A: Vitest for unit and integration tests, Playwright for end-to-end browser tests.

**Q36. How many test files exist?**
A: 29 unit/integration test files and 1 E2E test file.

**Q37. What does the nutrition-engine.test.ts file test?**
A: It tests the BMR calculation formula, TDEE calculation with different activity levels, calorie target adjustment for all 6 goal types, macro calculation in auto mode and custom mode, micronutrient targets for different ages and genders, and health condition adjustments for diabetes and hypertension.

**Q38. What does the recommend.test.ts test?**
A: It tests the rule-based food scoring function (checking that gap fill efficiency is calculated correctly), the 14-day no-repeat exclusion logic, the favorite/liked food boost, the serving size optimization, the budget constraint enforcement, and the rejected food penalty.

### Deployment Questions

**Q39. How is the app deployed?**
A: Next.js app on Vercel (serverless), MongoDB on Atlas (cloud), FastAPI ML service on a separate VPS (optional). Environment variables are set in Vercel Dashboard.

**Q40. What happens to the Python ML layer on Vercel?**
A: Vercel runs serverless functions in a Node.js environment only — Python subprocesses are not supported directly. The recommendation falls back to the rule-based TypeScript engine (`src/lib/recommend.ts`) when the Python layer is unavailable. For full XGBoost ranking on production, the FastAPI backend service must be deployed separately and `ML_BACKEND_URL` set.

### Advanced Questions

**Q41. How does the food caching work?**
A: The food catalog (383 items from MongoDB) is cached in memory using `src/lib/data-cache.ts`. This avoids querying MongoDB for every recommendation request. For daily meal plans, the top recommendation per mealtime is cached in the `generatedmeals` MongoDB collection, so the same meal is served to the user throughout the day without recomputation.

**Q42. What is the meal timing / intermittent fasting feature?**
A: Users can select from presets: standard 3-meal, 16:8 intermittent fasting (with configurable eating window start/end times), 5 small meals, or custom. Each preset defines meal slots with labels, types, and times. The app uses `mealTypeForNow()` to auto-select the current mealtime based on the user's meal slot configuration.

**Q43. How does the feedback loop work in recommendations?**
A: When a user likes or dislikes a food recommendation, a `Feedback` document is created with action: accept/reject/like/dislike. The recommendation API reads all feedback for the user and applies: +0.05 score boost for liked/accepted foods, -0.15 penalty for rejected/disliked foods. This ensures user preferences are learned over time.

**Q44. What is the retraining pipeline?**
A: `src/lib/retraining-pipeline.ts` monitors model performance metrics. When performance degrades below thresholds, it triggers retraining of the ML models. The `POST /api/retraining` route can also be called manually to trigger retraining.

**Q45. How does the voice intent recognition work?**
A: The Web Speech API (browser-native) converts speech to text. `src/lib/voice-intent.ts` then parses the transcript using deterministic rules: wake word detection, action classification (log_meal, navigate, daily_summary, suggest_recipe, chat), entity extraction (meal type, food item, portion). Confidence below 0.75 requires user confirmation.

**Q46. How are shared recipes implemented?**
A: When a user enables sharing on a custom food, a unique token is generated (`randomBytes`) and stored as `shareToken`. The food is accessible at `/api/shared-foods/{token}`. Another user can import the recipe, which copies it to their own CustomFood collection with `originFoodId` set to the original.

**Q47. What is the OpenFoodFacts integration?**
A: OpenFoodFacts is a free, open database of packaged food nutrition. The barcode lookup makes a GET request to `https://world.openfoodfacts.org/api/v0/product/{ean}.json`. The response is normalized to the app's standard nutrition format. An offline cache of ~500 products is included in the codebase for instant responses and offline resilience.

**Q48. How is the email for password reset sent?**
A: If `RESEND_API_KEY` is configured, the email is sent via Resend's API with an HTML template. If not configured (common in development), the reset URL is logged to the server console. The implementation is in `src/lib/email.ts`. The reset token is hashed before storage and expires in 1 hour.

**Q49. How does the macro split work for diabetic users?**
A: Diabetes reduces carb percentage from 50% to 40% of calories (to manage blood sugar), increases protein factor to 1.2 g/kg (protein doesn't spike blood sugar and promotes satiety), reduces sugar limit from 50g to 30g/day, and rejects foods with >15g sugar per 100g in recommendations.

**Q50. What are the limitations of the MealMentor system?**
A: (1) The food dataset (383 items) is primarily Indian cuisine — limited international diversity. (2) BMR/TDEE formulas are population estimates, not individually accurate. (3) Gemini Vision food recognition may be inaccurate for uncommon dishes. (4) The XGBoost model was trained on synthetic data, not real user preference logs. (5) Weight forecast requires sufficient historical data and a running FastAPI service. (6) Rate limiting is in-memory and resets on server restart. (7) Not medically validated and should not replace dietitian advice.

---

## Part J: 20 Challenging External Examiner Questions

**Q1. Your XGBoost model was trained on synthetic queries, not real user feedback. How does this affect recommendation quality?**
A: The synthetic training data represents varied nutritional needs and gaps, teaching the model the relationship between food properties and nutritional suitability. However, it doesn't capture personal taste preferences or cultural factors. The feedback loop (liked/disliked foods) partially compensates by applying soft score adjustments. In production with real user data, the model would be retrained on actual preference signals using the retraining pipeline.

**Q2. The Mifflin–St Jeor equation was derived from specific population studies. How valid is it for Indian users?**
A: The equation was validated primarily on American and European populations. For Indian users, body composition and metabolic rate may differ. The system uses the formula as a starting estimate — the work type and activity level adjusters provide meaningful personalization even if the baseline BMR estimate has some error. Future work could integrate population-specific calibration.

**Q3. How would you scale this application to 100,000 concurrent users?**
A: MongoDB Atlas auto-scales horizontally with sharding. The in-memory rate limiter would need replacement with Redis for shared state across multiple server instances. Vercel serverless functions scale automatically. The Python ML subprocess spawn is a bottleneck at scale and would need migration to a persistent FastAPI service with a connection pool or queue. The food catalog cache is already in-memory and scales well.

**Q4. How do you prevent a user from gaming the recommendation system by always liking foods?**
A: Liked foods receive a +0.05 score boost — a small, bounded adjustment. The dominant driver remains nutrient-gap alignment (40% weight) and calorie balance (20%). Even a liked food will score low if it doesn't fill the user's gaps. Rejected foods have a larger -0.15 penalty, which is intentionally asymmetric — we trust negative feedback more than positive.

**Q5. The security audit reveals your rate limiter is in-memory. What attack vectors does this leave open?**
A: (1) Distributed attacks across multiple IPs bypass per-IP limits. (2) Server restart clears all buckets. (3) In a multi-instance deployment, per-user limits are not enforced globally. The solution is Redis-based rate limiting with atomic increment operations. The current implementation is appropriate for single-instance development/staging.

**Q6. Gemini Vision returns calorie estimates for detected food. How do you verify these are accurate?**
A: We don't verify them independently — the estimates come from the model's training data. We display a confidence score (0-1) to the user and allow manual correction of portion estimates. The system explicitly labels AI-estimated values as approximations and recommends cross-referencing with the food database for common dishes.

**Q7. Your password reset token is hashed before storage. But you're using SHA-256 instead of bcrypt for the token. Is this a security concern?**
A: Password reset tokens are high-entropy random values (generated with `randomBytes`) rather than user-chosen passwords. SHA-256 is appropriate for hashing high-entropy tokens because they don't benefit from the slow hashing that makes bcrypt necessary for passwords. A brute-force on a 32-byte random token is computationally infeasible regardless of hash speed.

**Q8. What is the computational complexity of the recommendation algorithm?**
A: Rule-based scoring: O(n) where n is the number of foods in the filtered catalog (≤383). XGBoost inference: O(m × t) where m is the candidate count and t is the number of trees (100). Total: approximately O(383) per recommendation request, which is fast enough for real-time use.

**Q9. How does the system handle imperial unit inputs for height and weight?**
A: The user can set `unitSystem: "imperial"` in their profile. The frontend converts lbs to kg and feet/inches to cm before sending to the API. All backend calculations use metric internally. Verified by the `profile-imperial-macro.test.ts` test file.

**Q10. What would happen to existing users if you changed the BMR formula?**
A: Their nutrition targets would be recalculated from the new formula. Since targets are calculated on-the-fly from the stored profile (not pre-stored), changing the formula in `calcBMR()` automatically updates all users' targets. This is a feature of the design — targets are computed, not cached in the database.

**Q11. How does the 14-day no-repeat rule interact with a small food database?**
A: With only 383 items and a meal-type filter (e.g., only breakfast items), active users may exhaust the pool quickly. A fallback mechanism re-admits the least-recently-eaten items when the primary pool is empty, sorted by oldest-eaten-first with a recency discount applied to their score. This ensures recommendations always succeed while still preferring variety.

**Q12. Your chatbot falls back to deterministic responses. Could this mislead users about the AI's capabilities?**
A: The API response includes a `source` field ("ai" or "local") to distinguish. The frontend could display a badge indicating which engine responded. The local engine's responses are factually derived from calculated targets and actual today's intake — they're not random or wrong, just not conversational.

**Q13. How do you ensure the food dataset values are accurate?**
A: The dataset values are used as-is — we don't independently validate each nutrition value. The dataset appears to be a curated project-specific collection. The code explicitly states "dataset nutrition values are the source of truth" and adds a disclaimer that the app is "not medical advice." Future work could cross-validate against established databases like USDA or IFCT.

**Q14. What happens if MongoDB connection fails during a recommendation request?**
A: The `connectToDatabase()` call in `src/lib/db.ts` throws an error which propagates up to the API route's try-catch block, returning HTTP 500 with "Internal server error". The error is logged. There's no automatic retry — this is expected behavior for a transient database failure.

**Q15. The `tokenVersion` mechanism invalidates sessions on password change. Does it work for Google OAuth users?**
A: Google OAuth users have `passwordHash` but may not use it. The `tokenVersion` is incremented by the change-password route, but Google OAuth users who don't have a password cannot use that route. Their sessions persist until the 7-day JWT expiry. Logout explicitly clears the cookie, providing a manual session termination.

**Q16. How would you add a new nutrient (e.g., vitamin D) to the system?**
A: Add it to: (1) `IFood` interface and `FoodSchema`, (2) `NutritionTargets` interface, (3) `microTargets()` formula in `nutrition.ts`, (4) `NutrientIntake` interface in `intake.ts`, (5) `computeIntake()` computation, (6) `Gaps` interface and `calcGaps()`, (7) `scoreFood()` in `recommend.ts`. The dataset CSV would also need a new column, and seeding scripts updated.

**Q17. How does serving size clamping affect nutritional accuracy?**
A: Clamping the serving to 50–250g means the recommended portion may not exactly close the gap. For example, if the gap requires 400g of a food but it's capped at 250g, the user will still have a deficit after eating the recommended serving. The remaining gap is recalculated when the user returns later in the day. This is an intentional trade-off — portions beyond 250g for a single serving are impractical.

**Q18. The nudge engine uses time-based conditions. What timezone does it use?**
A: The application uses JavaScript's `Date.now()` which returns UTC milliseconds. The `startOfDay(date)` function sets hours to 00:00:00 in the server's local time. In production, this should be the user's local timezone — a future enhancement would store the user's timezone and convert before evaluating nudge conditions.

**Q19. How does the quick-buy catalog differ from grocery list generation?**
A: The grocery list (`/api/grocery/generate`) derives ingredient shopping needs from the day's meal plan by looking up dish ingredients from `dish-ingredients.ts`. The quick-buy catalog (`src/data/quick-buy-catalog.ts`) is a pre-curated list of readily available grocery products with pricing, used for suggesting quick shopping options rather than recipe-derived ingredients.

**Q20. If you had to redesign the recommendation system, what would you do differently?**
A: (1) Use collaborative filtering to learn from similar users' successful diets. (2) Train XGBoost on real user acceptance data (not synthetic), using logged meals as implicit positive signals. (3) Add nutritionist-verified meal plan templates as high-quality seeds. (4) Implement A/B testing to compare rule-based vs XGBoost outcomes. (5) Store user preference embeddings for faster candidate retrieval at scale.

---

## Part K: Possible Examiner Concerns and Honest Answers

| Concern | Honest Explanation |
|---------|-------------------|
| "Is the AI medically validated?" | No. The system provides estimates based on general nutritional guidelines and user-provided data. It is not clinically validated and should not replace a registered dietitian. The app explicitly states this in the README and API note. |
| "Are the nutrition values in the dataset verified?" | The dataset is a project-compiled CSV file. The exact source provenance is not documented in the code. We use these values as the source of truth for this application. Independent clinical validation was not performed. |
| "The XGBoost model is trained on synthetic data — is this valid?" | Synthetic training data provides diverse coverage of nutritional scenarios and teaches the model the relationship between food properties and gap-filling suitability. It's a valid approach for cold-start ML when real user data is unavailable. The recommendation always falls back to rule-based scoring if XGBoost fails. |
| "What about privacy? Photos are stored in the database." | Food photos are stored as base64 data URLs or cloud URLs in the user's own FoodPhoto collection. They are only accessible to the authenticated user (user._id filter enforced). Gemini sends the photo to Google's API — this should be disclosed to users. |
| "How accurate is Gemini Vision for Indian food?" | The accuracy varies by dish. Common Indian dishes are well-represented in Gemini's training data. Unusual regional dishes may have lower confidence scores. The system displays confidence scores so users can judge and correct estimates. |
| "Why doesn't the system integrate real medical data?" | This is a final-year project scope limitation. Medical integration would require HIPAA/PDPA compliance, clinical validation, and partnerships with healthcare providers. The current scope demonstrates the technical feasibility of the recommendation and tracking pipeline. |
