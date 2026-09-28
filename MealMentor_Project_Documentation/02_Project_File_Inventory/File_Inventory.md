# MealMentor — Complete Project File Inventory

## Overall Folder Structure

```
mealmentor/
├── package.json                          # Root workspace package
└── nutrisense-ai/                        # Main Next.js application
    ├── .env.example                      # Environment variable template
    ├── .env.local                        # Actual env config (not committed)
    ├── README.md                         # Developer README
    ├── AGENTS.md                         # AI agent instructions
    ├── finalDatasetfood.csv              # Food nutrition dataset (384 items)
    ├── finalDatasetGrocery.csv           # Grocery ingredient price dataset (331 items)
    ├── MealMentor_IEEE_Paper.pdf         # IEEE paper (project reference)
    ├── package.json                      # Node.js dependencies
    ├── tsconfig.json                     # TypeScript configuration
    ├── next.config.ts                    # Next.js configuration
    ├── playwright.config.ts              # E2E test configuration
    ├── vitest.config.mjs                 # Unit test configuration
    ├── components.json                   # Shadcn/ui component config
    ├── src/                              # Source code
    │   ├── app/                          # Next.js App Router pages
    │   ├── components/                   # React components
    │   ├── lib/                          # Utility and business logic
    │   ├── models/                       # Mongoose database models
    │   ├── data/                         # Static data files
    │   └── types/                        # TypeScript type definitions
    ├── ml/                               # Python ML layer
    ├── backend/                          # FastAPI Python backend
    ├── tests/                            # Vitest unit + Playwright E2E tests
    ├── scripts/                          # Database seeding scripts
    └── public/                           # Static assets
```

---

## A. Frontend Source Code

### Pages (Next.js App Router)

| File Path | Purpose | Features Supported |
|-----------|---------|-------------------|
| `src/app/layout.tsx` | Root layout with font, theme, toast provider | All pages |
| `src/app/globals.css` | Global CSS variables, Tailwind base | All pages |
| `src/app/(auth)/layout.tsx` | Auth layout (unauthenticated) | Login, Register |
| `src/app/(auth)/login/page.tsx` | Login page | User authentication |
| `src/app/(auth)/register/page.tsx` | Registration page | User registration |
| `src/app/(auth)/reset-password/page.tsx` | Password reset page | Password recovery |
| `src/app/(dashboard)/layout.tsx` | Dashboard layout with sidebar + header | All protected pages |
| `src/app/(dashboard)/dashboard/page.tsx` | Main dashboard with overview cards | Nutrition summary, forecast |
| `src/app/(dashboard)/nutrition/page.tsx` | Nutrition targets and progress | Nutrient gap tracking |
| `src/app/(dashboard)/meal-plan/page.tsx` | AI meal plan generation | Meal recommendations |
| `src/app/(dashboard)/food-tracking/page.tsx` | Food logging and search | Food logging |
| `src/app/(dashboard)/grocery/page.tsx` | Grocery list generation | Grocery planning |
| `src/app/(dashboard)/progress/page.tsx` | Weight trends and 7-day history | Progress tracking |
| `src/app/(dashboard)/ai-assistant/page.tsx` | AI nutrition chatbot | AI chat |
| `src/app/(dashboard)/profile/page.tsx` | User profile management | Profile setup |
| `src/app/(dashboard)/settings/page.tsx` | Account settings | Account management |
| `src/app/(dashboard)/food-photo/page.tsx` | Food photo analysis | Gemini Vision |
| `src/app/(dashboard)/barcode-scan/page.tsx` | Barcode scanner | OpenFoodFacts |
| `src/app/(dashboard)/my-recipes/page.tsx` | Custom recipe/food management | Custom food |

### Components

| File/Folder | Purpose | Used By |
|-------------|---------|---------|
| `src/components/layout/` | Sidebar, header, navigation | Dashboard layout |
| `src/components/auth/forgot-password-modal.tsx` | Password reset modal | Login page |
| `src/components/nutrition/` | Nutrition progress bars, targets display | Nutrition page |
| `src/components/meal-plan/` | Recommendation cards, meal plan UI | Meal plan page |
| `src/components/food-tracking/` | Food search, log entry components | Food tracking page |
| `src/components/food-photo/` | Camera upload, analysis results | Food photo page |
| `src/components/barcode/` | Camera barcode scanner | Barcode scan page |
| `src/components/grocery/` | Grocery list UI | Grocery page |
| `src/components/hydration/` | Water tracking UI | Dashboard |
| `src/components/budget/` | Budget input and display | Profile, meal plan |
| `src/components/custom-food/` | Custom food form | My recipes page |
| `src/components/forecast-card.tsx` | 7-day weight forecast card | Dashboard |
| `src/components/streak-strip.tsx` | Streak display UI | Dashboard |
| `src/components/activity-level-calculator.tsx` | Activity level helper | Profile |
| `src/components/daily-targets-table.tsx` | Targets summary table | Nutrition |
| `src/components/food-search.tsx` | Food search bar | Food tracking |
| `src/components/markdown.tsx` | Markdown renderer for AI responses | AI assistant |
| `src/components/theme-toggle.tsx` | Light/dark mode toggle | Header |
| `src/components/voice/` | Voice input component | Multiple pages |
| `src/components/nudges/` | Proactive nudge display | Dashboard |
| `src/components/meal-timing/` | Meal timing preferences UI | Profile |
| `src/components/feedback/` | Like/dislike food feedback | Meal plan |
| `src/components/ui/` | Shadcn/ui primitives (Button, Card, Select, etc.) | All components |

---

## B. Backend Source Code (API Routes)

| API Route | Method | Purpose |
|-----------|--------|---------|
| `src/app/api/auth/login/route.ts` | POST | Email/password authentication, JWT creation |
| `src/app/api/auth/register/route.ts` | POST | New user registration with password hashing |
| `src/app/api/auth/logout/route.ts` | POST | Clear session cookie |
| `src/app/api/auth/me/route.ts` | GET | Return current authenticated user |
| `src/app/api/auth/google/route.ts` | GET | Initiate Google OAuth flow |
| `src/app/api/auth/google/callback/route.ts` | GET | Google OAuth callback handler |
| `src/app/api/auth/forgot-password/route.ts` | POST | Initiate password reset |
| `src/app/api/auth/reset-password/route.ts` | POST | Complete password reset with token |
| `src/app/api/auth/account/route.ts` | PATCH | Update display name |
| `src/app/api/auth/change-password/route.ts` | POST | Change authenticated user's password |
| `src/app/api/profile/route.ts` | GET/PUT | Get and update user profile |
| `src/app/api/foods/route.ts` | GET | Search food database |
| `src/app/api/foods/[id]/route.ts` | GET | Get specific food item |
| `src/app/api/tracking/route.ts` | GET/POST | Get today's logs; log a food entry |
| `src/app/api/tracking/[id]/route.ts` | DELETE | Remove a food log entry |
| `src/app/api/recommend-xgb/route.ts` | POST | Generate XGBoost meal recommendations |
| `src/app/api/nutrition/route.ts` | GET | Get nutrition targets and today's status |
| `src/app/api/progress/weight/route.ts` | GET/POST | Weight log CRUD |
| `src/app/api/progress/weight/[id]/route.ts` | DELETE | Delete weight entry |
| `src/app/api/progress/summary/route.ts` | GET | 7-day nutrition history summary |
| `src/app/api/ml/forecast/route.ts` | GET | 7-day weight change forecast |
| `src/app/api/ai/chat/route.ts` | POST | AI nutrition chatbot |
| `src/app/api/food-photo/route.ts` | POST | Analyze food photo with Gemini Vision |
| `src/app/api/food-photo/log/route.ts` | POST | Log confirmed photo analysis as meal entries |
| `src/app/api/barcode/route.ts` | GET | Barcode lookup (OpenFoodFacts + offline cache) |
| `src/app/api/grocery/generate/route.ts` | GET/POST | Grocery list generation |
| `src/app/api/hydration/route.ts` | GET/POST | Water intake logging |
| `src/app/api/custom-foods/route.ts` | GET/POST | Custom food CRUD |
| `src/app/api/custom-foods/[id]/route.ts` | PUT/DELETE | Update/delete custom food |
| `src/app/api/shared-foods/[token]/route.ts` | GET | Access shared food recipe by token |
| `src/app/api/analytics/route.ts` | GET | Usage analytics |
| `src/app/api/nudges/route.ts` | GET/POST | Proactive nudge management |
| `src/app/api/feedback/route.ts` | POST | Like/dislike food feedback |
| `src/app/api/meal-timing/route.ts` | GET/PUT | Meal timing preferences |
| `src/app/api/recipes/route.ts` | GET | Fetch external recipes |
| `src/app/api/retraining/route.ts` | POST | Trigger ML model retraining |

---

## C. Database Models (Mongoose)

| Model File | Collection | Purpose |
|-----------|-----------|---------|
| `src/models/User.ts` | `users` | User accounts, profiles, authentication |
| `src/models/Food.ts` | `foods` | Food items with nutrition data (seeded from CSV) |
| `src/models/MealEntry.ts` | `mealentries` | Daily food log entries |
| `src/models/WeightLog.ts` | `weightlogs` | Weight tracking entries |
| `src/models/FoodPhoto.ts` | `foodphotos` | Photo analysis results |
| `src/models/CustomFood.ts` | `customfoods` | User-created custom foods and recipes |
| `src/models/Feedback.ts` | `feedbacks` | User like/dislike on food recommendations |
| `src/models/GeneratedMeal.ts` | `generatedmeals` | Cached daily meal plan recommendations |
| `src/models/HydrationLog.ts` | `hydrationlogs` | Water intake logs |
| `src/models/Nudge.ts` | `nudges` | Proactive notification records |
| `src/models/ScannedBarcode.ts` | `scannedbarcodes` | Barcode scan history |
| `src/models/GroceryItem.ts` | `groceryitems` | Grocery list items |
| `src/models/AIModelVersion.ts` | `aimodelversions` | ML model version tracking |
| `src/models/AIPredictionFeedback.ts` | `aipredictionfeedbacks` | ML prediction accuracy feedback |

---

## D. AI and ML Files

| File | Language | Purpose |
|------|---------|---------|
| `src/lib/gemini-vision.ts` | TypeScript | Gemini Vision API client for food photo analysis |
| `src/lib/ml.ts` | TypeScript | Python ML layer client (spawn-based subprocess) |
| `src/lib/recommend.ts` | TypeScript | Rule-based food scoring and recommendation engine |
| `ml/recommend_service.py` | Python | Rule-based scoring + XGBoost re-ranking service |
| `ml/train_xgb_rank.py` | Python | XGBoost learning-to-rank training pipeline |
| `ml/rank_food.py` | Python | XGBoost inference entry point (called at runtime) |
| `ml/predict_calories.py` | Python | Ridge regression calorie prediction |
| `ml/predict_meal_type.py` | Python | Random Forest meal type classification |
| `ml/predict_protein.py` | Python | XGBoost protein content prediction |
| `ml/preprocessing.py` | Python | Food dataset loading and cleaning |
| `ml/calibration_models.py` | Python | Model probability calibration |
| `ml/model_utils.py` | Python | Model loading/saving utilities |
| `ml/evaluate_models.py` | Python | Model evaluation script |
| `ml/train_models.py` | Python | Supporting model training (Ridge, RandomForest) |
| `ml/ranker/` | Python | XGBoost ranker module (features, relevance, predict) |
| `ml/models/` | Binary | Trained model artifacts (.pkl files) |
| `ml/evaluation_metrics.json` | JSON | Stored evaluation metrics |
| `backend/app/main.py` | Python | FastAPI entry point for ML backend service |
| `backend/app/api/routes.py` | Python | FastAPI routes (/predict, /train, /health) |
| `backend/app/ml/` | Python | Random Forest weight forecast model |

---

## E. Dataset Files

| File | Format | Records | Purpose |
|------|--------|---------|---------|
| `finalDatasetfood.csv` | CSV | 384 rows (383 foods + header) | Food nutrition database (source of truth) |
| `finalDatasetGrocery.csv` | CSV | 331 rows (330 items + header) | Grocery ingredient price reference |
| `src/data/dish-metadata.json` | JSON | ~274 KB | Rich dish metadata (ingredients, cuisine) |
| `src/data/dish-ingredients.ts` | TypeScript | ~18 KB | Dish-to-ingredient mappings |
| `src/data/quick-buy-catalog.ts` | TypeScript | ~38 KB | Quick-buy grocery catalog |
| `src/data/barcode-cache.ts` | TypeScript | ~303 KB | Offline barcode product cache (~500 items) |

---

## F. Authentication and Security

| File | Purpose |
|------|---------|
| `src/lib/auth.ts` | JWT creation/verification using `jose` (HS256) |
| `src/lib/session.ts` | Cookie-based session management and user lookup |
| `src/lib/hash.ts` | Password hashing/verification using Node.js scrypt |
| `src/lib/rate-limit.ts` | In-memory sliding-window rate limiter |
| `src/lib/validation.ts` | Input validation schemas (Zod) |
| `src/middleware.ts` / `src/proxy.ts` | Request routing and auth guard |

---

## G. Configuration and Deployment

| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template (MONGODB_URI, AUTH_SECRET, GEMINI_API_KEY, etc.) |
| `next.config.ts` | Next.js build configuration |
| `tsconfig.json` | TypeScript compiler settings |
| `postcss.config.mjs` | PostCSS/Tailwind build pipeline |
| `eslint.config.mjs` | ESLint linting rules |
| `playwright.config.ts` | Playwright E2E test configuration |
| `vitest.config.mjs` | Vitest unit test configuration |
| `scripts/seed-foods.mjs` | Seeds `foods` collection from `finalDatasetfood.csv` |
| `scripts/seed-groceries.mjs` | Seeds grocery data |
| `.github/` | GitHub Actions CI/CD workflows |

---

## H. Testing and Documentation

### Unit Tests (Vitest)

| Test File | What Is Tested |
|-----------|---------------|
| `tests/recommend.test.ts` | Rule-based recommendation engine logic |
| `tests/nutrition-engine.test.ts` | BMR/TDEE/calorie calculation formulas |
| `tests/auth.test.ts` | Login, register, and JWT session |
| `tests/worktype.test.ts` | Work-type to activity-level mapping |
| `tests/foods-tracking.test.ts` | Food log CRUD operations |
| `tests/food-photo-recognition.test.ts` | Gemini Vision photo analysis |
| `tests/barcode-scan.test.ts` | Barcode lookup and parsing |
| `tests/hydration.test.ts` | Water target and unit conversion |
| `tests/meal-timing.test.ts` | Meal slot and timing preferences |
| `tests/proactive-nudges.test.ts` | Nudge evaluation logic |
| `tests/xgb-recommend.test.ts` | XGBoost ranking integration |
| `tests/retraining-pipeline.test.ts` | ML retraining pipeline |
| `tests/streaks.test.ts` | Streak computation |
| `tests/rate-limit.test.ts` | Rate limiter logic |
| `tests/swap-meal.test.ts` | Meal swap feature |
| `tests/quick-buy.test.ts` | Quick-buy catalog |
| `tests/recipe-fetcher.test.ts` | Recipe fetching |
| `tests/crud.test.ts` | Generic CRUD operations |
| `tests/acid.test.ts` | Database ACID properties |
| `tests/activity-level.test.ts` | Activity level calculations |
| `tests/budget.test.ts` | Budget calculation |
| `tests/intake-helpers.test.ts` | Intake computation helpers |

### E2E Tests (Playwright)

| Test File | What Is Tested |
|-----------|---------------|
| `tests/e2e/responsive.spec.ts` | Responsive design across breakpoints |

### Documentation

| File | Content |
|------|---------|
| `README.md` | Developer setup guide, API reference, architecture decisions |
| `backend/README.md` | FastAPI backend setup and ML service documentation |
| `ml/README.md` | ML layer usage, training, and evaluation |
| `docs/` | Additional developer documentation |
| `MealMentor_IEEE_Paper.pdf` | IEEE-format academic paper |
