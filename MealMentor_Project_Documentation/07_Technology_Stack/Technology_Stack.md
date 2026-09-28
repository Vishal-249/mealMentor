# MealMentor — Technology Stack Documentation

## Complete Technology Stack Table

| Technology / Tool | Version | Category | Purpose | Actual Usage | Relevant File |
|-------------------|---------|----------|---------|--------------|---------------|
| Next.js | 16.3.3 | Frontend Framework | Full-stack React framework with App Router | All pages, API routes, SSR | `next.config.ts` |
| React | 19.2.8 | UI Library | Component-based UI rendering | All UI components | All `.tsx` files |
| TypeScript | ^5 | Language | Type-safe JavaScript for frontend and backend | Entire `src/` codebase | `tsconfig.json` |
| Tailwind CSS | ^4 | CSS Framework | Utility-first styling | All component styles | `postcss.config.mjs` |
| Shadcn/ui | ^4.19.0 | UI Component Library | Pre-built, accessible UI primitives | Button, Card, Select, Dialog, etc. | `components.json`, `src/components/ui/` |
| Recharts | ^3.10.1 | Data Visualization | Charts for nutrition progress and weight trends | Progress page, dashboard | `src/app/(dashboard)/progress/` |
| Lucide React | ^1.34.0 | Icon Library | SVG icons throughout the UI | All pages and components | Multiple component files |
| Sonner | ^2.0.8 | Toast Notifications | User feedback messages | All interactive actions | `src/app/layout.tsx` |
| Zod | ^4.4.3 | Validation Library | Schema validation for forms and API inputs | Profile, food logging, auth | `src/lib/validation.ts` |
| react-markdown | ^10.1.0 | Markdown Renderer | Renders AI chatbot responses | AI assistant page | `src/components/markdown.tsx` |
| @base-ui/react | ^1.7.0 | UI Primitives | Accessible base components | Select, Tooltip, etc. | UI components |
| MongoDB | 7+ | Database | Document store for all application data | All collections | `src/lib/db.ts` |
| Mongoose | ^9.9.4 | ODM | MongoDB object modeling and schema | All models | `src/models/*.ts` |
| jose | ^6.2.10 | JWT Library | JWT creation and verification (HS256) | Authentication | `src/lib/auth.ts` |
| Node.js crypto | Built-in | Hashing | Password hashing (scrypt), token generation | Password management | `src/lib/hash.ts` |
| @ericblade/quagga2 | ^1.12.1 | Barcode Scanner | Camera-based barcode scanning | Barcode scan page | `src/components/barcode/` |
| @google/generative-ai | ^0.24.1 | AI SDK | Google Gemini API client | Food photo analysis, chatbot | `src/lib/gemini-vision.ts` |
| class-variance-authority | ^0.7.1 | CSS Utilities | Component variant styling | UI components | Component files |
| clsx + tailwind-merge | — | CSS Utilities | Conditional and merged class names | All components | `src/lib/utils.ts` |
| tw-animate-css | ^1.4.0 | Animations | CSS animation utilities | UI transitions | CSS imports |
| Python | 3.11+ | Language | ML layer scripts and FastAPI backend | `ml/` and `backend/` directories | `ml/*.py`, `backend/*.py` |
| pandas | ^2.0 | Data Processing | Food CSV loading and preprocessing | `ml/preprocessing.py` | `ml/requirements.txt` |
| numpy | ^1.24 | Numerical Computing | Array operations for ML training | Training and inference | ML scripts |
| scikit-learn | ^1.3 | ML Library | Ridge regression, Random Forest, evaluation metrics | Supporting models, evaluation | `ml/train_models.py`, `ml/evaluate_models.py` |
| xgboost | ^2.0 | ML Library | XGBoost learning-to-rank model | Food recommendation ranking | `ml/train_xgb_rank.py`, `ml/rank_food.py` |
| joblib | ^1.3 | Model Persistence | Save/load trained ML models (.pkl) | Model artifacts | `ml/model_utils.py` |
| FastAPI | ^0.111 | API Framework | Python REST API for ML forecasting service | Weight forecast endpoint | `backend/app/main.py` |
| uvicorn | ^0.30 | ASGI Server | Run FastAPI application | Dev and prod serving | Backend startup |
| pydantic | ^2.5 | Data Validation | Request/response validation in FastAPI | Backend schemas | `backend/app/schemas.py` |
| pymongo | ^4.6 | MongoDB Driver | Direct MongoDB access from Python backend | Training data queries | Backend ML |
| Google Gemini API | gemini-3.8-flash | External AI | LLM for food recognition and chatbot | Vision + chat routes | `src/lib/gemini-vision.ts`, `src/app/api/ai/chat/` |
| OpenFoodFacts API | v0 | External API | Barcode product nutrition lookup | Barcode scanning | `src/lib/openfoodfacts.ts` |
| Google OAuth 2.0 | — | Authentication | Social login | Login with Google | `src/app/api/auth/google/` |
| Resend API | — | Email Service | Password reset email delivery | Forgot password flow | `src/lib/email.ts` |
| Google Custom Search | — | External API | Recipe ingredient fallback lookup | Recipe fetcher | `src/lib/recipe-fetcher.ts` |
| Web Speech API | Browser native | Voice Input | Voice-to-text for meal logging | Voice component | `src/lib/voice-intent.ts` |
| Vitest | ^4.1.11 | Testing | Unit and integration testing | 29 test files | `vitest.config.mjs` |
| Playwright | ^1.63.0 | E2E Testing | End-to-end browser testing | Responsive design tests | `playwright.config.ts` |
| ESLint | ^9 | Code Quality | JavaScript/TypeScript linting | Dev workflow | `eslint.config.mjs` |

---

## Technology Architecture Rationale

### Why Next.js 16 with App Router?
- Server Components reduce JavaScript bundle sent to browser
- Built-in API routes eliminate need for a separate Express/Node.js backend
- Edge-compatible routing for performance
- Type-safe with TypeScript out of the box
- Streaming, Suspense, and concurrent rendering support

### Why MongoDB?
- Flexible document schema accommodates diverse nutrition data structures
- Profile sub-document (nested object) fits naturally in a document model
- Easy horizontal scaling for analytics and user data growth
- Mongoose ODM provides TypeScript-safe schema definitions with validation

### Why XGBoost Learning-to-Rank?
- Purpose-built for ranking problems (rank:ndcg objective)
- Handles the implicit preference signals (food logs, likes) naturally
- Fast inference: <10ms per candidate set
- Feature importance provides explainability for recommendations
- Robust to missing values and noisy features

### Why Python + subprocess spawn for ML?
- Zero network latency in local development
- Language-agnostic contract: JSON over stdin/stdout
- No Python dependencies in Node.js process
- Easy migration path to FastAPI microservice (swap spawn for HTTP)

### Why Gemini Vision for Food Photo Analysis?
- Supports multimodal input (image + text prompt) natively
- Produces structured JSON output with nutrition per 100g
- Handles Indian and international cuisines well
- Model fallback chain provides resilience

### Why jose for JWT?
- Web Crypto API-based, no native addons required
- Works in Node.js, Edge runtime, and Deno
- HS256 algorithm suitable for server-side JWT signing

### Why scrypt for Password Hashing?
- Node.js built-in, no external dependency
- Memory-hard function resistant to brute-force and GPU attacks
- timingSafeEqual prevents timing attacks on comparison

### Why In-Memory Rate Limiting?
- Zero external dependency (no Redis required)
- Sufficient for single-instance deployments
- Self-sweeping bucket map prevents memory leaks
- Bounded at 10,000 buckets with LRU eviction

---

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| MONGODB_URI | Yes | MongoDB connection string |
| AUTH_SECRET | Yes | JWT signing secret (≥32 bytes) |
| GOOGLE_CLIENT_ID | Optional | Google OAuth client ID |
| GOOGLE_CLIENT_SECRET | Optional | Google OAuth client secret |
| NEXT_PUBLIC_APP_URL | Yes | Public app URL for OAuth redirects |
| ML_PYTHON | Optional | Python interpreter path (default: python3) |
| ML_BACKEND_URL | Optional | FastAPI service URL (default: http://127.0.0.1:8000) |
| GOOGLE_API_KEY | Optional | Google Custom Search API key |
| GOOGLE_SEARCH_CX | Optional | Google Custom Search engine ID |
| GEMINI_API_KEY | Optional | Gemini API key (required for AI features) |
| OPENAI_API_KEY | Optional | OpenAI key (fallback, not currently used in core path) |
| RESEND_API_KEY | Optional | Email delivery (falls back to console logging) |
| EMAIL_FROM | Optional | Sender email address for reset emails |
