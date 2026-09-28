# MealMentor — Security, Testing, and Performance Documentation

## 1. Security Mechanisms

### 1.1 Password Hashing
- **Implementation**: Node.js built-in `crypto.scrypt` with 16-byte random salt, KEY_LENGTH=64
- **Format**: `salt:derivedKey` (both hex-encoded), stored in `passwordHash` field
- **Verification**: `timingSafeEqual()` prevents timing-based side-channel attacks
- **Source**: `src/lib/hash.ts`

**Verified Code**:
```typescript
// hashPassword: generates salt + scrypt key
const salt = randomBytes(16).toString("hex")
const derivedKey = (await scrypt(password, salt, KEY_LENGTH)) as Buffer
return `${salt}:${derivedKey.toString("hex")}`

// verifyPassword: uses timingSafeEqual
return timingSafeEqual(derivedKey, keyBuffer)
```

### 1.2 JWT Session Management
- **Library**: `jose` (Web Crypto API-based)
- **Algorithm**: HS256 (HMAC-SHA256)
- **Expiry**: 7 days (`SESSION_DURATION_SECONDS = 60 * 60 * 24 * 7`)
- **Cookie**: HTTP-only (`httpOnly: true`), `secure: true` in production, `sameSite: "lax"`
- **Cookie Name**: `mealmentor_session`
- **Token Version**: `tokenVersion` field in User model invalidates all old sessions on password change
- **Source**: `src/lib/auth.ts`, `src/lib/session.ts`

### 1.3 Authentication Guard
- `getCurrentUser()` called in every protected API route
- Returns `null` if cookie missing, JWT invalid, token version mismatch, or user not found
- All protected routes return 401 if user is null

### 1.4 Password Reset Security
- Token generated using `randomBytes()` → hashed with SHA-256 before storage
- Only the hash is stored (`resetPasswordTokenHash`)
- Token expires in 1 hour (`resetPasswordExpires`)
- `resetPasswordRequestedAt` limits request rate
- Token is one-use: cleared after successful reset
- Source: `src/app/api/auth/forgot-password/`, `src/app/api/auth/reset-password/`

### 1.5 Google OAuth
- Authorization code exchange on server side only
- Google profile fetched server-side; client never receives raw OAuth token
- User identified by `googleId` (upsert pattern)

### 1.6 Rate Limiting
- **Type**: In-memory sliding-window token bucket
- **Limits** (per-user + IP):
  - ML recommendations: 30 requests per 60 seconds
  - Other endpoints: varies per route
- **Eviction**: Max 10,000 buckets; expired entries swept; oldest evicted when full
- **Client IP**: Uses `x-real-ip` → single-hop `x-forwarded-for` → hashed multi-hop XFF
- **Source**: `src/lib/rate-limit.ts`

### 1.7 Input Validation
- **Library**: Zod schema validation
- API routes validate request body shape and field constraints before processing
- Mongoose schema constraints (required, enum, min, max) provide database-level validation
- Password requirements: minimum length enforced

### 1.8 API Protection
- All database-writing routes require authentication
- Admin operations gated behind role check (where applicable)
- No public write endpoints

### 1.9 Environment Variables
- Sensitive values (AUTH_SECRET, GEMINI_API_KEY, MONGODB_URI, Google OAuth credentials) are read only from `process.env`
- Never exposed to the client; Next.js server-only API routes handle all sensitive operations
- `.env.local` is gitignored

### 1.10 Data Isolation
- All database queries include `user: user._id` filter to prevent cross-user data access
- Users can only read/write their own meal logs, weight entries, photos, and custom foods

---

## 2. Identified Security Considerations

| Concern | Status | Notes |
|---------|--------|-------|
| Password hashing | ✅ Implemented | scrypt with random salt, timingSafeEqual |
| JWT security | ✅ Implemented | HTTP-only cookie, HS256, 7-day expiry |
| Session invalidation | ✅ Implemented | tokenVersion incremented on password change |
| Password reset token | ✅ Implemented | Hashed before storage, 1-hour expiry |
| Rate limiting | ✅ Implemented | Per-user + IP, in-memory |
| Input validation | ✅ Implemented | Zod + Mongoose |
| Cross-user data access | ✅ Prevented | All queries filtered by user._id |
| SQL Injection | N/A | MongoDB document queries, not SQL |
| CSRF | Partial | SameSite=Lax cookie provides basic CSRF protection |
| HTTPS | Deployment-dependent | Recommended for production |
| XSS | Framework-handled | React escapes JSX output by default |
| API key exposure | ✅ Server-side only | Gemini/OpenFoodFacts keys in server env only |

---

## 3. Testing Documentation

### Testing Framework
- **Unit/Integration Tests**: Vitest (^4.1.11) — runs in Node.js environment
- **End-to-End Tests**: Playwright (^1.63.0) — browser automation

### Unit Test Coverage (29 test files in `tests/`)

| Test File | Features Tested | Type |
|-----------|----------------|------|
| `nutrition-engine.test.ts` | BMR/TDEE/calorie/macro formulas, goal adjustments, health condition adjustments | Unit |
| `recommend.test.ts` | Rule-based scoring, gap-fill efficiency, serving size calculation, 14-day no-repeat | Unit |
| `worktype.test.ts` | Work type → activity level mapping (extensive regex coverage) | Unit |
| `auth.test.ts` | Login, register, session management, token validation | Integration |
| `foods-tracking.test.ts` | Food log CRUD, intake computation | Integration |
| `food-photo-recognition.test.ts` | Gemini Vision analysis, response parsing, error handling | Integration |
| `barcode-scan.test.ts` | Barcode lookup, OpenFoodFacts parsing, offline cache | Unit/Integration |
| `xgb-recommend.test.ts` | XGBoost ranking integration and fallback | Integration |
| `retraining-pipeline.test.ts` | ML retraining pipeline (model monitoring, trigger conditions) | Integration |
| `meal-timing.test.ts` | Meal slot creation, IF presets, reminder preferences | Unit |
| `proactive-nudges.test.ts` | Nudge evaluation logic, conditions, deduplication | Unit |
| `streaks.test.ts` | Streak computation, milestone detection, at-risk calculation | Unit |
| `hydration.test.ts` | Water target calculation, unit conversions, streak integration | Unit |
| `intake-helpers.test.ts` | Intake computation, sumFromEntries, date utilities | Unit |
| `rate-limit.test.ts` | Rate limiter sliding window, eviction, client IP parsing | Unit |
| `swap-meal.test.ts` | Meal swap feature logic | Unit |
| `quick-buy.test.ts` | Quick-buy catalog functionality | Unit |
| `recipe-fetcher.test.ts` | Recipe fetching, ingredient parsing | Unit |
| `grocery-stores.test.ts` | Grocery store data | Unit |
| `meal-plan-grocery.test.ts` | Grocery generation from meal plan | Integration |
| `ingredient-categories.test.ts` | Ingredient category classification | Unit |
| `mealtime.test.ts` | Mealtime selection (time-based) | Unit |
| `activity-level.test.ts` | Activity level calculation from work type | Unit |
| `budget.test.ts` | Daily budget calculation | Unit |
| `medium-priority-gaps.test.ts` | Nutrient gap prioritization | Unit |
| `profile-imperial-macro.test.ts` | Imperial units + custom macro calculation | Unit |
| `crud.test.ts` | Generic collection CRUD | Integration |
| `acid.test.ts` | Database transaction properties | Integration |
| `voice-intent.test.ts` | Voice command parsing and intent extraction | Unit |

### E2E Tests

| Test File | What Is Tested |
|-----------|---------------|
| `tests/e2e/responsive.spec.ts` | Responsive design across mobile, tablet, desktop breakpoints |

### How to Run Tests

```bash
# Run all Vitest unit tests
npm run test

# Run specific test file
npm run test -- tests/recommend.test.ts

# Run with coverage
npm run test -- --coverage

# Run Playwright E2E tests
npm run test:e2e
```

> **Important Note**: Test results are not available from source code inspection alone. The actual test execution output cannot be confirmed without running the tests. Do not claim tests passed without actually executing them.

---

## 4. Performance Monitoring

The `PerformanceTracker` class (`src/lib/performance.ts`) adds `Server-Timing` and `X-Response-Time-Ms` headers to instrumented API responses.

**Instrumented Endpoints**:
- `POST /api/recommend-xgb` — tracks connect-db, targets-from-profile, calc-gaps, get-cached-foods, XGBoost subprocess call
- `POST /api/ai/chat` — tracks auth, calc_targets, load_intake, external_ai_fetch
- `GET /api/profile` — tracks connect-db, load-profile, calc-targets

**Example Response Header**:
```
Server-Timing: connect-db;dur=12.34, load-today-intake;dur=45.67, total;dur=234.56
X-Response-Time-Ms: 234.56
```

> **Note**: No actual production performance benchmarks are available from source code inspection. The monitoring infrastructure is implemented but actual measurements require deployment.

---

## 5. Feature Verification Table

| Feature | Implementation Status | Evidence | Limitations |
|---------|----------------------|----------|-------------|
| User Registration | ✅ Fully Implemented | `src/app/api/auth/register/` | — |
| Email/Password Login | ✅ Fully Implemented | `src/lib/hash.ts`, `src/lib/auth.ts` | — |
| Google OAuth Login | ✅ Fully Implemented | `src/app/api/auth/google/` | Requires GOOGLE_CLIENT_ID/SECRET in env |
| Password Reset | ✅ Fully Implemented | `src/lib/email.ts`, reset routes | Email requires RESEND_API_KEY or falls back to console |
| User Profile | ✅ Fully Implemented | `src/models/User.ts`, profile API | — |
| BMR Calculation | ✅ Fully Implemented | `src/lib/nutrition.ts:calcBMR()` | Estimation only; not clinical |
| TDEE Calculation | ✅ Fully Implemented | `src/lib/nutrition.ts:calcTDEE()` | — |
| Calorie Target | ✅ Fully Implemented | `src/lib/nutrition.ts:calcCalorieTarget()` | Min floor of 1200 kcal |
| Macro Targets | ✅ Fully Implemented | `src/lib/nutrition.ts:calcMacroTargets()` | Custom split supported |
| Micronutrient Targets | ✅ Fully Implemented | `src/lib/nutrition.ts:microTargets()` | Based on US DRI/RDA guidelines |
| Food Database | ✅ Fully Implemented | `finalDatasetfood.csv`, 383 items | Primarily Indian cuisine |
| Food Logging | ✅ Fully Implemented | `src/app/api/tracking/` | — |
| Nutrient Gap Tracking | ✅ Fully Implemented | `src/lib/gaps.ts` | — |
| Rule-Based Recommendations | ✅ Fully Implemented | `src/lib/recommend.ts` | — |
| XGBoost Recommendations | ✅ Fully Implemented | `ml/train_xgb_rank.py`, `ml/rank_food.py` | Requires Python + model training; fallback to rule-based |
| Food Photo Analysis | ✅ Fully Implemented | `src/lib/gemini-vision.ts` | Requires GEMINI_API_KEY; AI estimates may vary |
| Barcode Scanning | ✅ Fully Implemented | `src/lib/openfoodfacts.ts`, `src/data/barcode-cache.ts` | Live lookup requires internet |
| AI Chatbot | ✅ Fully Implemented | `src/app/api/ai/chat/route.ts` | Full AI requires GEMINI_API_KEY; local fallback always works |
| Water Tracking | ✅ Fully Implemented | `src/lib/hydration.ts`, hydration API | — |
| Weight Logging | ✅ Fully Implemented | `src/models/WeightLog.ts`, progress API | — |
| Weight Forecast | ✅ Implemented | `backend/app/` | Requires FastAPI running + model trained + historical data |
| Streak Tracking | ✅ Fully Implemented | `src/lib/streaks.ts` | — |
| Proactive Nudges | ✅ Fully Implemented | `src/lib/proactive-nudges.ts` | — |
| Custom Food Creation | ✅ Fully Implemented | `src/models/CustomFood.ts`, `src/lib/custom-food.ts` | — |
| Recipe Sharing | ✅ Fully Implemented | `src/app/api/shared-foods/` | Via share token URL |
| Grocery List Generation | ✅ Fully Implemented | `src/app/api/grocery/` | — |
| Voice Input | ✅ Fully Implemented | `src/lib/voice-intent.ts` | Browser Web Speech API required |
| Meal Timing / IF | ✅ Fully Implemented | `src/lib/meal-timing.ts`, `src/models/User.ts` | — |
| Dark/Light Theme | ✅ Fully Implemented | `src/lib/theme.ts`, `src/components/theme-toggle.tsx` | — |
| Rate Limiting | ✅ Fully Implemented | `src/lib/rate-limit.ts` | In-memory only; resets on server restart |
| Performance Monitoring | ✅ Fully Implemented | `src/lib/performance.ts` | Development/logging tool; no external APM |
| WCAG 2.1 AA Accessibility | ✅ Implemented (claimed) | README checklist | Not independently audited from source code |
| ML Model Retraining | ✅ Implemented | `src/lib/retraining-pipeline.ts`, `src/app/api/retraining/` | Manual trigger; requires historical data |
