# MealMentor — System Architecture Documentation

## 1. Overall System Architecture

MealMentor uses a three-tier architecture with an optional fourth ML service tier:

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                        │
│  React 19 + Next.js 16 App Router (Client Components)   │
│  - Web Speech API (voice input)                          │
│  - Quagga2 (barcode camera scanning)                     │
│  - Recharts (data visualization)                          │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────┐
│                NEXT.JS APPLICATION SERVER                │
│  - Server Components (SSR/SSG)                           │
│  - API Routes (RESTful backend)                          │
│  - JWT Session Validation (jose)                         │
│  - Rate Limiting (in-memory)                             │
│  - Mongoose ODM                                          │
└────────┬───────────────┬──────────────┬─────────────────┘
         │               │              │
         │ Mongoose  Spawn subprocess  Fetch HTTP
         ▼               ▼              ▼
┌────────────┐  ┌─────────────────┐  ┌──────────────────────┐
│  MongoDB   │  │  Python ML      │  │  External APIs        │
│  Database  │  │  Layer (ml/)    │  │  - Gemini Vision      │
│  (Atlas or │  │  - recommend_   │  │  - Gemini Chat        │
│   Local)   │  │    service.py   │  │  - OpenFoodFacts       │
│            │  │  - rank_food.py │  │  - Google OAuth       │
│            │  │  - XGBoost      │  │  - Google Search API  │
│            │  │    models (.pkl)│  │  - Resend (email)     │
└────────────┘  └────────┬────────┘  └──────────────────────┘
                         │ Optional
                ┌────────▼────────┐
                │  FastAPI        │
                │  Backend        │
                │  (backend/)     │
                │  - Random Forest│
                │    Forecast     │
                │  Port 8000      │
                └─────────────────┘
```

---

## 2. Frontend Architecture

- **Framework**: Next.js 16 with App Router
- **Rendering Strategy**: Mixed — Server Components for data fetching, Client Components for interactivity
- **Routing**: File-system routing with route groups:
  - `(auth)` — unauthenticated pages (login, register, reset-password)
  - `(dashboard)` — authenticated pages with sidebar layout
- **State Management**: React local state + server actions (no external state library)
- **Styling**: Tailwind CSS 4 + CSS custom properties + Shadcn/ui component library
- **Charts**: Recharts library for progress bars, line charts, and area charts
- **Notifications**: Sonner toast library
- **Validation**: Zod schema validation on both client and server

---

## 3. Backend Architecture

- **API Layer**: Next.js API Routes (RESTful, server-side)
- **Authentication**: JWT tokens (HS256) stored in HTTP-only cookies, 7-day expiry
- **Database**: MongoDB with Mongoose ODM, connection pooling via `src/lib/db.ts`
- **Rate Limiting**: In-memory sliding-window bucket algorithm (per-user + IP)
- **Performance Monitoring**: `PerformanceTracker` class adds `Server-Timing` headers
- **ML Integration**: Python subprocess spawn with JSON over stdin/stdout
- **Caching**: 
  - In-memory food catalog cache (`src/lib/data-cache.ts`)
  - Per-day generated meal cache in MongoDB (`GeneratedMeal` collection)
  - Offline barcode cache (`src/data/barcode-cache.ts`)

---

## 4. Database Architecture

- **Database**: MongoDB (flexible document store)
- **ODM**: Mongoose v9 with TypeScript interfaces
- **Connection**: Single connection pool via `src/lib/db.ts` with connection reuse
- **Collections**: 14 collections (see Database Documentation section)
- **Indexes**: Compound indexes for common query patterns (user + date, meal type + price)

---

## 5. AI/ML Architecture

### Recommendation Pipeline
```
User Profile + Today's Intake
         ↓
    BMR/TDEE/Target Calculation  [nutrition.ts]
         ↓
    Nutrient Gap Calculation     [gaps.ts]
         ↓
    Rule-Based Pre-filtering     [recommend.ts / recommend_service.py]
    (hard constraints: allergies, budget, dietary preference, health conditions)
         ↓
    XGBoost Learning-to-Rank     [rank_food.py / ranker/predict.py]
    (or rule-based fallback if model unavailable)
         ↓
    Serving Size Optimization    [recommend.ts → pickServing()]
         ↓
    Result Caching               [GeneratedMeal collection]
         ↓
    Recommendation Response      [API → React UI]
```

### Photo Analysis Pipeline
```
User Uploads Photo
         ↓
    Base64 Encoding (client-side)
         ↓
    POST /api/food-photo
         ↓
    analyzePhotoWithGemini()     [gemini-vision.ts]
    (Primary: gemini-3.8-flash → Fallback: gemini-3.8-flash-lite)
         ↓
    JSON Parsing + Sanitization
         ↓
    FoodPhoto document saved (MongoDB)
         ↓
    User Reviews & Confirms
         ↓
    POST /api/food-photo/log → MealEntry documents created
```

### Weight Forecast Pipeline
```
GET /api/ml/forecast
         ↓
    Try FastAPI: POST http://127.0.0.1:8000/api/v1/predict
    (19 features: profile + 7-day intake averages + targets)
         ↓
    If FastAPI unavailable: spawn Python subprocess
         ↓
    Random Forest model inference
         ↓
    Return 7-day weight change prediction (kg)
```

---

## 6. Authentication Flow

```
User submits login form
         ↓
    POST /api/auth/login
         ↓
    Find user by email (MongoDB)
         ↓
    verifyPassword() [hash.ts] — scrypt comparison
         ↓
    If valid: createSessionToken() [auth.ts] — SignJWT (HS256, 7 days)
         ↓
    Set HTTP-only cookie: mealmentor_session
         ↓
    Return 200 + user object
         ↓
    Subsequent requests: getCurrentUser() [session.ts]
    reads cookie → verifySessionToken() → User.findById()
```

### Google OAuth Flow
```
Click "Sign in with Google"
         ↓
    GET /api/auth/google → Build Google OAuth URL
         ↓
    Browser → Google OAuth consent page
         ↓
    Google → GET /api/auth/google/callback?code=...
         ↓
    Exchange code for Google access token
         ↓
    Fetch Google profile (email, name, googleId)
         ↓
    Upsert User document (create if new, link if existing)
         ↓
    Create JWT session → Set cookie → Redirect to dashboard
```

---

## 7. Mermaid Diagrams

### A. System Architecture Diagram

```mermaid
graph TB
    Browser["Browser\n(React 19 + Next.js)"]
    NextJS["Next.js Application Server\n(API Routes + Server Components)"]
    MongoDB["MongoDB Database\n(14 collections)"]
    PythonML["Python ML Layer\n(XGBoost + Rule-based)"]
    FastAPI["FastAPI Backend\n(Random Forest)"]
    GeminiVision["Gemini Vision API\n(Food Photo Analysis)"]
    GeminiChat["Gemini Chat API\n(AI Assistant)"]
    OpenFoodFacts["OpenFoodFacts API\n(Barcode Lookup)"]
    GoogleOAuth["Google OAuth 2.0\n(Authentication)"]
    
    Browser -->|HTTPS| NextJS
    NextJS -->|Mongoose| MongoDB
    NextJS -->|subprocess spawn| PythonML
    NextJS -->|HTTP optional| FastAPI
    NextJS -->|HTTPS API| GeminiVision
    NextJS -->|HTTPS API| GeminiChat
    NextJS -->|HTTPS API| OpenFoodFacts
    Browser -->|OAuth redirect| GoogleOAuth
    GoogleOAuth -->|callback| NextJS
```

### B. Use Case Diagram

```mermaid
graph LR
    User(("User"))
    
    User --> UC1["Register / Login"]
    User --> UC2["Set Up Profile\n(age, weight, goals)"]
    User --> UC3["Log Food Manually"]
    User --> UC4["Scan Barcode"]
    User --> UC5["Upload Food Photo"]
    User --> UC6["View Meal Recommendations"]
    User --> UC7["Track Water Intake"]
    User --> UC8["Log Weight"]
    User --> UC9["Chat with AI Nutritionist"]
    User --> UC10["View Progress Dashboard"]
    User --> UC11["Generate Grocery List"]
    User --> UC12["Create Custom Food"]
    User --> UC13["Set Meal Timing\n(Intermittent Fasting)"]
    User --> UC14["Like / Dislike Food"]
    User --> UC15["View 7-Day Forecast"]
```

### C. Data Flow Diagram — Level 0

```mermaid
graph LR
    User(("User"))
    MealMentor["MealMentor\nSystem"]
    External["External Services\n(Gemini, OpenFoodFacts,\nGoogle OAuth)"]
    
    User -->|"Profile, food logs,\nweight, photos"| MealMentor
    MealMentor -->|"Recommendations,\ntargets, reports"| User
    MealMentor -->|"Photo, barcode,\nOAuth, chat queries"| External
    External -->|"Nutrition data,\nuser identity, AI responses"| MealMentor
```

### D. Data Flow Diagram — Level 1

```mermaid
graph TB
    User(("User"))
    
    P1["1.0 Authentication\n& Profile Module"]
    P2["2.0 Nutrition\nCalculation Engine"]
    P3["3.0 Food Logging\nModule"]
    P4["4.0 Recommendation\nEngine"]
    P5["5.0 AI Services\nModule"]
    P6["6.0 Progress\nTracking Module"]
    
    D1[("users\ncollection")]
    D2[("foods\ncollection")]
    D3[("mealentries\ncollection")]
    D4[("generatedmeals\ncollection")]
    D5[("weightlogs\ncollection")]
    
    User -->|credentials/profile| P1
    P1 <-->|read/write| D1
    P1 -->|profile data| P2
    P2 -->|targets & gaps| P4
    P2 -->|targets| P5
    User -->|food selection/qty| P3
    P3 <-->|food lookup| D2
    P3 -->|log entries| D3
    D3 -->|today's intake| P2
    P4 <-->|food catalog| D2
    P4 -->|recommendations| D4
    P4 -->|meal plan| User
    User -->|photo/barcode/text| P5
    P5 -->|nutrition/advice| User
    User -->|weight entry| P6
    P6 <-->|weight data| D5
    P6 -->|trends/forecast| User
```

### E. Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        ObjectId _id PK
        string email UK
        string name
        string passwordHash
        string googleId
        string resetPasswordTokenHash
        Date resetPasswordExpires
        int tokenVersion
        object profile
        Date createdAt
        Date updatedAt
    }
    
    FOOD {
        ObjectId _id PK
        string name UK
        string foodType
        string mealType
        float pricePer100g
        float calories
        float carbsG
        float proteinG
        float fatG
        float fiberG
        float sugarG
        float sodiumMg
        float calciumMg
        float ironMg
        float vitaminCMg
    }
    
    MEALENTRY {
        ObjectId _id PK
        ObjectId user FK
        ObjectId foodId FK
        string foodName
        string mealType
        float qtyG
        Date date
        float calories
        float proteinG
        float carbsG
        float fatG
    }
    
    WEIGHTLOG {
        ObjectId _id PK
        ObjectId user FK
        float weightKg
        Date date
        string notes
    }
    
    FOODPHOTO {
        ObjectId _id PK
        ObjectId user FK
        string photoDataUrl
        float overallConfidence
        array detectedItems
        boolean logged
        array mealEntryIds
        string modelUsed
    }
    
    CUSTOMFOOD {
        ObjectId _id PK
        ObjectId user FK
        string name
        string mealType
        string foodType
        float calories
        array ingredients
        boolean shareEnabled
        string shareToken
    }
    
    FEEDBACK {
        ObjectId _id PK
        ObjectId user FK
        ObjectId foodId FK
        string foodName
        string action
        Date timestamp
    }
    
    GENERATEDMEAL {
        ObjectId _id PK
        ObjectId user FK
        string mealType
        Date date
        object food
        float score
        string ranking
        float servingG
    }
    
    HYDRATIONLOG {
        ObjectId _id PK
        ObjectId user FK
        float amountMl
        string tag
        Date timestamp
    }
    
    NUDGE {
        ObjectId _id PK
        ObjectId user FK
        string type
        string message
        boolean dismissed
        Date timestamp
    }
    
    USER ||--o{ MEALENTRY : "logs"
    USER ||--o{ WEIGHTLOG : "tracks"
    USER ||--o{ FOODPHOTO : "uploads"
    USER ||--o{ CUSTOMFOOD : "creates"
    USER ||--o{ FEEDBACK : "gives"
    USER ||--o{ GENERATEDMEAL : "receives"
    USER ||--o{ HYDRATIONLOG : "records"
    USER ||--o{ NUDGE : "receives"
    FOOD ||--o{ MEALENTRY : "logged_as"
    FOOD ||--o{ FEEDBACK : "rated_in"
```

### F. Application Workflow Diagram

```mermaid
flowchart TD
    A[User Opens App] --> B{Authenticated?}
    B -->|No| C[Login / Register]
    C --> D{Profile Complete?}
    B -->|Yes| D
    D -->|No| E[Complete Profile Setup\nage, weight, goals, preferences]
    E --> F[Calculate BMR, TDEE, Targets]
    D -->|Yes| F
    F --> G[Dashboard]
    G --> H{User Action}
    H --> I[View Nutrition Targets]
    H --> J[Log Food\nSearch / Barcode / Photo / Voice]
    H --> K[View Meal Recommendations]
    H --> L[Chat with AI Assistant]
    H --> M[Log Water Intake]
    H --> N[Log Weight]
    H --> O[Generate Grocery List]
    J --> P[Update Daily Intake]
    P --> Q[Recalculate Nutrient Gaps]
    Q --> R[Update Recommendations]
    K --> R
    R --> G
```

### G. Sequence Diagram — User Authentication

```mermaid
sequenceDiagram
    participant Browser
    participant NextJS as Next.js API
    participant DB as MongoDB
    
    Browser->>NextJS: POST /api/auth/login {email, password}
    NextJS->>DB: User.findOne({email})
    DB-->>NextJS: User document (with passwordHash)
    NextJS->>NextJS: verifyPassword(password, passwordHash)
    Note over NextJS: Uses scrypt for comparison
    NextJS->>NextJS: createSessionToken({userId, email, tokenVersion})
    Note over NextJS: SignJWT HS256, 7 days
    NextJS-->>Browser: 200 OK + Set-Cookie: mealmentor_session=<JWT>
    
    Browser->>NextJS: GET /api/profile (with cookie)
    NextJS->>NextJS: getCurrentUser() → verifySessionToken()
    NextJS->>DB: User.findById(userId)
    DB-->>NextJS: User document
    NextJS-->>Browser: 200 + user profile
```

### H. Sequence Diagram — Meal Recommendation Generation

```mermaid
sequenceDiagram
    participant Browser
    participant NextJS as API Route
    participant Cache as In-Memory Cache
    participant DB as MongoDB
    participant Python as Python ML Layer
    
    Browser->>NextJS: POST /api/recommend-xgb {mealTypes: ["breakfast","lunch",...]}
    NextJS->>NextJS: getCurrentUser() + rate limit check
    NextJS->>Cache: getCachedFoods()
    Cache-->>NextJS: Food catalog (384 items)
    NextJS->>DB: GeneratedMeal.findOne({user, mealType, date})
    DB-->>NextJS: Cached meal (if exists)
    NextJS->>DB: MealEntry.find({user, date range}) [today's intake]
    NextJS->>NextJS: calcAllTargets(profile) → targets
    NextJS->>NextJS: calcGaps(targets, consumed) → gaps
    NextJS->>Python: spawn rank_food.py with JSON payload
    Note over Python: Rule-based scoring → XGBoost re-ranking
    Python-->>NextJS: Ranked food names + scores
    NextJS->>NextJS: hydrateRankedCandidates() → full Recommendation[]
    NextJS->>DB: GeneratedMeal.findOneAndUpdate (cache top pick)
    NextJS-->>Browser: {complete, targets, consumed, gaps, meals}
```

### I. Sequence Diagram — Food Logging

```mermaid
sequenceDiagram
    participant Browser
    participant NextJS as API Route
    participant DB as MongoDB
    
    Browser->>NextJS: GET /api/foods?q=chicken
    NextJS->>DB: Food.find({name: /chicken/i})
    DB-->>NextJS: Matching food items
    NextJS-->>Browser: Food search results
    
    Browser->>NextJS: POST /api/tracking {foodId, mealType, qtyG}
    NextJS->>DB: Food.findById(foodId)
    DB-->>NextJS: Food document (per-100g values)
    NextJS->>NextJS: computeIntake(food, qtyG)
    Note over NextJS: calories = food.calories * (qtyG/100)
    NextJS->>DB: MealEntry.create({user, food, intake snapshot})
    DB-->>NextJS: Saved MealEntry
    NextJS-->>Browser: 201 + entry with computed nutrients
```

### J. Sequence Diagram — Food Photo Analysis

```mermaid
sequenceDiagram
    participant Browser
    participant NextJS as API Route
    participant GeminiAPI as Gemini Vision API
    participant DB as MongoDB
    
    Browser->>NextJS: POST /api/food-photo {imageBase64, mimeType}
    NextJS->>GeminiAPI: POST generateContent (image + structured prompt)
    Note over GeminiAPI: Model: gemini-3.8-flash\n(fallback: gemini-3.8-flash-lite)
    GeminiAPI-->>NextJS: JSON with detected food items + nutrition per 100g
    NextJS->>NextJS: Parse + sanitize + clamp values
    NextJS->>NextJS: scaledNutrients() for each item (portion × 100g values)
    NextJS->>DB: FoodPhoto.create({user, items, confidence, modelUsed})
    NextJS-->>Browser: Analysis results (items, confidence, nutrition)
    
    Browser->>NextJS: POST /api/food-photo/log {photoId, mealType}
    NextJS->>DB: FoodPhoto.findById(photoId) → detectedItems
    NextJS->>DB: MealEntry.create (one per detected item)
    NextJS->>DB: FoodPhoto.updateOne({logged: true, mealEntryIds})
    NextJS-->>Browser: 201 + created meal entries
```

### K. Deployment Architecture Diagram

```mermaid
graph TB
    subgraph "Production - Vercel"
        NextApp["Next.js App\n(Serverless Functions)"]
    end
    
    subgraph "Database - MongoDB Atlas"
        Atlas["MongoDB Atlas\nCloud Database"]
    end
    
    subgraph "ML Service - Optional VPS"
        FastAPI["FastAPI Backend\n(uvicorn, port 8000)"]
        Python["Python ML Scripts\n(subprocess fallback)"]
    end
    
    subgraph "External APIs"
        Gemini["Google Gemini API"]
        OFF["OpenFoodFacts API"]
        GoogleOAuth["Google OAuth 2.0"]
        Resend["Resend Email API"]
    end
    
    NextApp -->|MONGODB_URI| Atlas
    NextApp -->|ML_BACKEND_URL| FastAPI
    NextApp -->|subprocess fallback| Python
    NextApp -->|GEMINI_API_KEY| Gemini
    NextApp --> OFF
    NextApp -->|GOOGLE_CLIENT_ID/SECRET| GoogleOAuth
    NextApp -->|RESEND_API_KEY| Resend
```
