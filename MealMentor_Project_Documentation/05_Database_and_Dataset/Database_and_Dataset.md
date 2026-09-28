# MealMentor — Database and Dataset Documentation

## 1. Database Technology

- **Database**: MongoDB (document-oriented NoSQL)
- **Version**: MongoDB 7+ (recommended)
- **ODM**: Mongoose v9.9.4 with TypeScript interfaces
- **Connection**: Managed via `src/lib/db.ts` with connection pool reuse
- **URI Pattern**: `mongodb://127.0.0.1:27017/mealmentor` (local) or MongoDB Atlas cloud URI

---

## 2. Complete Collection Schemas

### Collection 1: users

**Purpose**: Stores user accounts, authentication data, and the nested profile document.

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| _id | ObjectId | Yes | PK | Auto-generated |
| email | String | Yes | Unique, lowercase, trimmed | Email-based identity |
| name | String | Yes | Trimmed | Display name |
| passwordHash | String | Yes | — | scrypt-derived hash (salt:key) |
| googleId | String | No | Trimmed | Google OAuth user ID |
| resetPasswordTokenHash | String | No | Indexed | Hashed reset token |
| resetPasswordExpires | Date | No | — | Token expiry (1 hour from issue) |
| resetPasswordRequestedAt | Date | No | — | When reset was requested |
| tokenVersion | Number | No | Default: 0 | Incremented to invalidate old tokens |
| profile | Object | No | Nested schema | All nutrition/lifestyle fields |
| createdAt | Date | Auto | — | Mongoose timestamps |
| updatedAt | Date | Auto | — | Mongoose timestamps |

**Profile Sub-document Fields**:
| Field | Type | Enum Values | Notes |
|-------|------|------------|-------|
| unitSystem | String | metric, imperial | Default: metric |
| age | Number | — | Years |
| gender | String | male, female, other | — |
| heightCm | Number | — | Centimeters |
| weightKg | Number | — | Kilograms |
| workType | String | Free text | Matched to activity level via regex |
| activityLevel | String | sedentary, light, moderate, active, very-active | — |
| goal | String | weight-loss, weight-gain, muscle-building, maintain-weight, improve-energy, general-healthy-lifestyle | — |
| foodPreference | String | vegetarian, non-vegetarian, vegan, eggetarian | — |
| cuisine | String | south-indian, north-indian, chinese, continental | — |
| allergies | [String] | — | Array of allergen names |
| avoidedFoods | [String] | — | Foods to exclude from recommendations |
| favoriteFoods | [String] | — | Foods to boost in recommendations |
| dailyBudget | Number | — | Budget amount in app currency |
| budgetPeriod | String | day, week, month | Default: day |
| healthConditions | [String] | none, diabetes, hypertension, other | Affects limits |
| macroSplit.method | String | auto, custom | — |
| macroSplit.proteinPct | Number | — | Used if method=custom |
| macroSplit.carbsPct | Number | — | Used if method=custom |
| macroSplit.fatPct | Number | — | Used if method=custom |
| hydrationPreferences | Object | — | Water tracking settings |
| mealTimingPreferences | Object | — | Meal slot configuration |

---

### Collection 2: foods

**Purpose**: Stores the food catalog seeded from `finalDatasetfood.csv`. These are the source of truth for nutrition values used in recommendations and logging.

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| _id | ObjectId | Yes | PK | — |
| name | String | Yes | Indexed, trimmed | Dish name |
| foodType | String | Yes | Indexed, enum | veg, non-veg, vegan |
| mealType | String | Yes | Indexed, enum | breakfast, lunch, snack, dinner, dessert, beverage |
| pricePer100g | Number | Yes | — | Price in app currency |
| calories | Number | Yes | — | kcal per 100g |
| carbsG | Number | Yes | — | Carbohydrates (g/100g) |
| proteinG | Number | Yes | — | Protein (g/100g) |
| fatG | Number | Yes | — | Fat (g/100g) |
| fiberG | Number | Yes | — | Dietary fiber (g/100g) |
| sugarG | Number | Yes | — | Sugar (g/100g) |
| sodiumMg | Number | Yes | — | Sodium (mg/100g) |
| calciumMg | Number | Yes | — | Calcium (mg/100g) |
| ironMg | Number | Yes | — | Iron (mg/100g) |
| vitaminCMg | Number | Yes | — | Vitamin C (mg/100g) |
| servingSizeG | Number | No | min: 1 | Typical serving in grams |
| pricePerServing | Number | No | Indexed | — |
| ingredients | [{name, qty, unit}] | No | — | Ingredient list |
| description | String | No | — | Dish description |
| prepTimeMinutes | Number | No | min: 1 | — |
| cookingInstructions | [String] | No | — | — |
| dietaryTags | [String] | No | — | e.g., ["gluten-free"] |

**Compound Indexes**: (mealType, pricePerServing), (foodType, pricePerServing)

---

### Collection 3: mealentries

**Purpose**: Records every food item a user logs for a day.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| _id | ObjectId | Yes | PK |
| user | ObjectId | Yes | Ref: User, Indexed |
| foodId | ObjectId | Yes | Ref: Food |
| foodName | String | Yes | Snapshot of name at log time |
| mealType | String | Yes | breakfast/lunch/snack/dinner/dessert/beverage |
| qtyG | Number | Yes | min: 1 — quantity consumed in grams |
| date | Date | Yes | Indexed, default: now |
| calories | Number | Yes | Per-100g value snapshot |
| carbsG | Number | Yes | Per-100g snapshot |
| proteinG | Number | Yes | Per-100g snapshot |
| fatG | Number | Yes | Per-100g snapshot |
| fiberG | Number | Yes | Per-100g snapshot |
| sugarG | Number | Yes | Per-100g snapshot |
| sodiumMg | Number | Yes | Per-100g snapshot |
| calciumMg | Number | Yes | Per-100g snapshot |
| ironMg | Number | Yes | Per-100g snapshot |
| vitaminCMg | Number | Yes | Per-100g snapshot |

> **Design Note**: Nutrition values are snapshotted at log time. Actual consumed amount = (qtyG / 100) × stored value.

**Compound Index**: (user, date)

---

### Collection 4: weightlogs

**Purpose**: Historical weight measurements for trend analysis and forecast.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| _id | ObjectId | Yes | PK |
| user | ObjectId | Yes | Ref: User, Indexed |
| weightKg | Number | Yes | min: 20, max: 400 |
| date | Date | Yes | Default: now |
| notes | String | No | max: 200 chars |

**Compound Index**: (user, date DESC)

---

### Collection 5: foodphotos

**Purpose**: Stores food photo analysis results from Gemini Vision.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| _id | ObjectId | Yes | PK |
| user | ObjectId | Yes | Ref: User, Indexed |
| photoDataUrl | String | Yes | Base64 data-URL or cloud storage URL |
| overallConfidence | Number | Yes | 0–1 |
| detectedItems | [Object] | Yes | Array of detected food items |
| logged | Boolean | Yes | Default: false |
| mealEntryIds | [ObjectId] | No | Refs to created MealEntry docs |
| analysisMs | Number | Yes | Processing time in ms |
| modelUsed | String | Yes | Default: gemini-3.8-flash |
| rawGeminiResponse | String | No | Raw JSON for debugging |
| error | String | No | Error message if analysis failed |

**Detected Item Fields**: name, portionGrams, confidence, calories, proteinG, carbsG, fatG, fiberG, sugarG, sodiumMg, manualCorrection (optional)

**Index**: (user, createdAt DESC)

---

### Collection 6: customfoods

**Purpose**: User-created food entries with ingredient-based or manual nutrition.

| Key Fields | Notes |
|-----------|-------|
| user | Owner reference |
| name | Food name (indexed) |
| mealType, foodType | Classification |
| servingSize, servingUnit, servingSizeGrams | Portion definition |
| nutritionSource | auto-ingredients, manual, or ingredients-override |
| calories, proteinG, ... | Per-serving nutrition values |
| ingredients | Array of ingredient objects with qty, unit, grams, and per-100g values |
| favorite, usageCount, lastUsedAt | Usage tracking |
| shareEnabled, shareToken, shareUsageCount | Sharing feature |

---

### Collection 7: feedbacks

**Purpose**: Records user like/dislike/accept/reject actions on recommendations.

| Field | Type | Notes |
|-------|------|-------|
| user | ObjectId | Ref: User |
| foodId | ObjectId | Ref: Food |
| foodName | String | |
| action | String | accept, reject, like, dislike |
| mealType | String | Optional |
| timestamp | Date | Indexed |

**Used By**: Recommendation engine to boost liked (+0.05 score) and penalize rejected (-0.15 score) foods.

---

### Collection 8: generatedmeals

**Purpose**: Caches the top daily meal recommendation per mealtime per user to avoid recomputation.

| Field | Type | Notes |
|-------|------|-------|
| user | ObjectId | Ref: User |
| mealType | String | breakfast/lunch/snack/dinner |
| date | Date | Start of day |
| food | Object | Full food object snapshot |
| score | Number | Ranking score |
| reason | String | Explanation text |
| ranking | String | xgboost or rule-based |
| servingG | Number | Recommended serving in grams |
| breakdown | Object | Per-nutrient contribution |
| servingIntake | Object | Computed per-serving nutrition |
| cost | Number | Estimated cost |

---

### Collection 9: hydrationlogs

**Purpose**: Water intake entries.

| Field | Type | Notes |
|-------|------|-------|
| user | ObjectId | Ref: User |
| amountMl | Number | Normalized to ml |
| tag | String | morning/with-meal/post-workout/evening/general |
| timestamp | Date | |
| notes | String | Optional |

---

### Collection 10: nudges

**Purpose**: Proactive notification records sent to users.

| Field | Type | Notes |
|-------|------|-------|
| user | ObjectId | Ref: User |
| type | String | missedMeal/hydration/pattern/macro/streak |
| message | String | Notification text |
| actionUrl | String | Deep link to relevant page |
| dismissed | Boolean | |
| actionTaken | Boolean | |
| snoozedUntil | Date | |
| timestamp | Date | |

---

## 3. Dataset Documentation

### Dataset 1: finalDatasetfood.csv

**Format**: CSV with header row
**Location**: `nutrisense-ai/finalDatasetfood.csv`
**Total Records**: 384 rows (383 food items + 1 header row)

**Column Definitions**:
| Column | Data Type | Unit | Description |
|--------|-----------|------|-------------|
| Dish_Name | String | — | Name of the food/dish |
| Food_Type | String | — | veg, non-veg, or vegan |
| Meal_Type | String | — | Breakfast/Lunch/Dinner/Snack/Dessert/Beverage |
| Price_per_100g | Float | ₹ (Rupees) | Price per 100 grams |
| Calories | Integer | kcal/100g | Caloric content |
| Carbs_g | Float | g/100g | Carbohydrates |
| Protein_g | Float | g/100g | Protein |
| Fat_g | Float | g/100g | Total fat |
| Fibre_g | Float | g/100g | Dietary fiber |
| Sugar (g) | Float | g/100g | Sugar content |
| Sodium (mg) | Float | mg/100g | Sodium |
| Calcium (mg) | Float | mg/100g | Calcium |
| Iron (mg) | Float | mg/100g | Iron |
| Vit C (mg) | Float | mg/100g | Vitamin C |

**Sample Records**:
| Dish_Name | Food_Type | Meal_Type | Price | Calories | Carbs | Protein | Fat |
|-----------|-----------|-----------|-------|----------|-------|---------|-----|
| Achappam | Veg | Snack | 24.0 | 293 | 29 | 4.7 | 10.4 |
| Ada Pradhaman | Veg | Dessert | 30.7 | 306 | 34 | 4.6 | 18.2 |
| Adai Aviyal | Veg | Dinner | 19.6 | 198 | 28 | 5.5 | 5.0 |

**Data Quality**:
- Preprocessing: Drop rows where Dish_Name is null, deduplicate on Dish_Name (keep first)
- Coerce numeric columns, drop rows where Calories is null/non-numeric
- Source: Project-specific curated dataset (primarily Indian cuisine). Source provenance cannot be verified from source code beyond being a project-compiled CSV file.

**Dataset Access**: Loaded via `ml/preprocessing.py → load_food_data()`, seeded to MongoDB via `scripts/seed-foods.mjs`

---

### Dataset 2: finalDatasetGrocery.csv

**Format**: CSV with header row
**Location**: `nutrisense-ai/finalDatasetGrocery.csv`
**Total Records**: 331 rows (330 grocery ingredients + 1 header row)

**Column Definitions**:
| Column | Data Type | Unit | Description |
|--------|-----------|------|-------------|
| Ingredient | String | — | Ingredient name |
| Price | Float | ₹ | Price |
| Unit | String | — | Unit of measure (e.g., 100ml, 100g, 1 kg) |

**Sample Records**:
- Alfredo Sauce: ₹12.0 per 100ml
- Almond Extract: ₹75.0 per 100ml

**Usage**: Referenced by grocery list generation and `src/lib/quick-buy.ts`

---

### Dataset 3: Offline Barcode Cache (barcode-cache.ts)

**Format**: TypeScript object (~303 KB)
**Location**: `src/data/barcode-cache.ts`
**Estimated Size**: ~500 barcode-to-product mappings
**Fields**: ean, productName, manufacturer, imageUrl, nutritionFacts (calories, protein, carbs, fat, fiber, sugar, sodium, servingSizeG)

**Source**: Pre-populated offline cache for common packaged products (actual source provenance not documented in code)
