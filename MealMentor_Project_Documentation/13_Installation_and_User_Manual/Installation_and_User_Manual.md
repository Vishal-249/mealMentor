# MealMentor — Installation and User Manual

## Part A: Installation Guide

### System Requirements

**Development Environment**:
- OS: Windows 10/11, macOS 12+, or Ubuntu 20.04+
- Node.js: v20 or later
- npm: v10 or later (comes with Node.js)
- Python: 3.11 or later
- MongoDB: 7.0 or later (or MongoDB Atlas cloud account)
- RAM: 4 GB minimum, 8 GB recommended
- Storage: 2 GB for application + dependencies

**Production Deployment** (Vercel recommended):
- MongoDB Atlas account
- Vercel account
- Google Cloud account (for Gemini API and OAuth)
- Resend account (optional, for email)

---

### Step 1: Install Prerequisites

**Windows**:
1. Download Node.js 20 from https://nodejs.org/
2. Download Python 3.11+ from https://python.org/
3. Download MongoDB Community Server from https://mongodb.com/try/download/community
4. Start MongoDB: `mongod --dbpath C:\data\db`

**macOS/Linux**:
```bash
# Install Node.js 20 (via nvm recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20

# Install Python 3.11+
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11

# Install MongoDB
# See: https://www.mongodb.com/docs/manual/administration/install-community/
```

---

### Step 2: Clone and Navigate

```bash
cd path/to/mealmentor/nutrisense-ai
```

---

### Step 3: Install Node.js Dependencies

```bash
npm install
```

This installs all dependencies listed in `package.json` including Next.js, React, Mongoose, jose, Zod, Recharts, etc.

---

### Step 4: Install Python ML Dependencies

```bash
cd ml
pip install -r requirements.txt
cd ..
```

Requirements: `pandas>=2.0`, `numpy>=1.24`, `scikit-learn>=1.3`, `xgboost>=2.0`, `joblib>=1.3`

---

### Step 5 (Optional): Install FastAPI Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

Requirements: `fastapi>=0.111`, `uvicorn[standard]>=0.30`, `pydantic>=2.5`, `pandas>=2.2`, `numpy>=1.26`, `scikit-learn>=1.4`, `joblib>=1.3`, `pymongo>=4.6`

---

### Step 6: Configure Environment Variables

```bash
# Copy the template
cp .env.example .env.local
```

Edit `.env.local` with your actual values:
```env
# Required
MONGODB_URI=mongodb://127.0.0.1:27017/mealmentor
AUTH_SECRET=<generate with: node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))">
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Optional - for Google Sign-In
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional - for AI features (food photo analysis, chatbot)
GEMINI_API_KEY=your-gemini-api-key

# Optional - for email delivery (falls back to console log)
RESEND_API_KEY=your-resend-api-key

# Optional - ML Python path (default: python3)
ML_PYTHON=python3
```

---

### Step 7: Seed the Database

```bash
# Seed food items from finalDatasetfood.csv
npm run seed:foods

# Seed grocery items from finalDatasetGrocery.csv
npm run seed:groceries
```

---

### Step 8 (Optional): Train the ML Model

```bash
cd ml
python train_xgb_rank.py
cd ..
```

This trains the XGBoost learning-to-rank model and saves it to `ml/models/xgboost_ranker.pkl`. If this step is skipped, the recommendation engine falls back to rule-based scoring.

---

### Step 9: Start the Application

**Terminal 1 — Next.js Development Server**:
```bash
npm run dev
```
App available at: http://localhost:3000

**Terminal 2 (Optional) — FastAPI ML Backend** (for weight forecast):
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
FastAPI available at: http://127.0.0.1:8000

---

### Step 10: Access the Application

Open your browser and navigate to: **http://localhost:3000**

---

## Part B: User Manual

### Getting Started

#### Step 1: Create an Account
1. Click **"Create an account"** on the login page
2. Enter your full name, email address, and a secure password
3. Click **"Create account"**
4. You will be automatically logged in and redirected to the dashboard
5. Alternatively, click **"Sign in with Google"** to use Google authentication

#### Step 2: Complete Your Profile
1. After login, a banner prompts you to complete your profile — click it
2. Navigate to **Profile** in the sidebar
3. Fill in:
   - Age, gender, height (cm), weight (kg)
   - Work type (free-text, e.g., "Software Engineer") — automatically mapped to activity level
   - Activity level (can be set manually too)
   - Health goal (weight loss, weight gain, muscle building, etc.)
   - Food preference (vegetarian, non-vegetarian, vegan, eggetarian)
   - Cuisine preference (south-indian, north-indian, chinese, continental)
   - Allergies and avoided foods (enter each and press Enter)
   - Health conditions (diabetes, hypertension)
   - Daily budget (optional)
4. Click **"Save Profile"**
5. Your BMR, TDEE, and calorie targets are now automatically calculated

---

### Daily Usage

#### Logging Food
1. Go to **Food Tracking** in the sidebar
2. Type a food name in the search bar (e.g., "idli", "dal makhani")
3. Click a food from the results
4. Select the meal type (Breakfast / Lunch / Snack / Dinner)
5. Enter the quantity in grams
6. Click **"Log"**

#### Scanning a Barcode
1. Go to **Barcode Scan** in the sidebar
2. Allow camera access when prompted
3. Hold the barcode of a packaged food in front of the camera
4. The product nutrition will be retrieved automatically
5. Set quantity and meal type, then click **"Log"**

#### Analyzing a Food Photo
1. Go to **Food Photo** in the sidebar
2. Click **"Upload Photo"** or **"Take Photo"**
3. Select a clear food image
4. Wait for Gemini Vision AI to analyze (usually 2-5 seconds)
5. Review the detected food items and confidence scores
6. Edit any incorrect portion estimates
7. Click **"Log Detected Foods"** to add all items to your food log

#### Viewing Meal Recommendations
1. Go to **Meal Plan** in the sidebar
2. Click **"Generate Plan"** or view the auto-generated recommendations
3. Recommendations are personalized for your current nutrient gaps and budget
4. Click 👍 (like) or 👎 (dislike) on any food to influence future recommendations
5. Click **"Generate Grocery List"** to get a shopping list from the meal plan

#### Tracking Water Intake
1. On the **Dashboard**, find the Hydration section
2. Click the **"+ Add Water"** button
3. Select the amount (in ml, cups, or liters)
4. Select a tag (morning, with-meal, etc.)
5. Your water progress bar will update immediately

#### Logging Weight
1. Go to **Progress** in the sidebar
2. Click **"Log Weight"**
3. Enter your current weight in kg (or lb if using imperial)
4. Click **"Save"**
5. Your weight chart will update

#### Using the AI Nutrition Assistant
1. Go to **AI Assistant** in the sidebar
2. Type a nutrition question in the chat box, for example:
   - "What should I eat for dinner to hit my protein target?"
   - "Explain my BMR and TDEE"
   - "How can I improve my calcium intake?"
   - "How am I tracking toward my weight loss goal?"
3. Press Enter or click the send button
4. The AI will respond with personalized advice based on your profile and today's intake

#### Voice Input
1. Click the microphone icon (available in food tracking and other pages)
2. Allow microphone access
3. Say a wake word followed by your command, for example:
   - "Hey MealMentor, log 150 grams of rice for lunch"
   - "Nutrisense, go to meal plan"
4. Confirm the action if prompted

---

### Profile Management

#### Changing Your Password
1. Go to **Settings** in the sidebar
2. Click **"Change Password"**
3. Enter your current password and the new password
4. Click **"Update Password"**

#### Forgot Password
1. On the login page, click **"Forgot password?"**
2. Enter your email address
3. Check your email for a reset link (or check the server console in development)
4. Click the link and enter your new password
5. The link expires in 1 hour

#### Updating Your Display Name
1. Go to **Settings**
2. Click **"Edit Name"**
3. Enter your new name and save

---

### Creating Custom Foods
1. Go to **My Recipes** in the sidebar
2. Click **"Create Custom Food"**
3. Enter the food name, meal type, and food type
4. Choose nutrition source:
   - **Manual**: Enter per-serving nutrition values directly
   - **Auto from Ingredients**: Add ingredients and nutrition is auto-calculated
5. Set serving size (e.g., 1 cup = 240g)
6. Click **"Save Food"**
7. Your custom food is now available in food search

#### Sharing a Custom Recipe
1. Find your custom food in **My Recipes**
2. Click **"Share"** to generate a shareable link
3. Share the link with others — they can import the recipe into their account

---

### Meal Timing (Intermittent Fasting)
1. Go to **Profile** → Meal Timing section
2. Select a preset:
   - **Standard 3-meal** (default)
   - **Intermittent Fasting 16:8**: Set eating window (e.g., 12:00–20:00)
   - **5 Small Meals**
   - **Custom**: Add your own meal slots with times
3. Enable meal reminders if desired

---

### Understanding Your Dashboard

| Element | What It Shows |
|---------|--------------|
| Calorie Ring | Calories consumed vs daily target |
| Macro Bars | Protein, carbs, fat consumed vs targets |
| Nutrient Status | Graded status (Deficient/Low/Near-Target/Adequate/Over) |
| Streak Strip | Current and longest daily logging streak + next milestone |
| Hydration Bar | Water consumed vs daily target |
| Forecast Card | Predicted 7-day weight change (requires weight history) |
| Nudge Cards | Personalized behavioral reminders |

---

## Part C: Production Deployment

### Vercel Deployment
1. Push code to a GitHub repository
2. Connect repository to Vercel (https://vercel.com)
3. Add all environment variables in Vercel Dashboard → Settings → Environment Variables
4. Deploy — Vercel handles building automatically

### MongoDB Atlas Setup
1. Create a free cluster at https://mongodb.com/cloud/atlas
2. Create a database named `mealmentor`
3. Add your Vercel deployment IP to the IP whitelist (or allow all IPs: 0.0.0.0/0)
4. Set `MONGODB_URI` environment variable to the Atlas connection string

### FastAPI ML Backend (Optional)
1. Deploy to a VPS (e.g., DigitalOcean Droplet, EC2)
2. Install Python, dependencies, and run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Set `ML_BACKEND_URL` in Vercel environment to the server's public URL

---

## Part D: Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|---------|
| "Cannot connect to database" | MongoDB not running or wrong URI | Start MongoDB or check MONGODB_URI |
| "AUTH_SECRET environment variable is not set" | Missing .env.local | Copy .env.example → .env.local, set AUTH_SECRET |
| "Gemini API key not configured" | Missing GEMINI_API_KEY | Add GEMINI_API_KEY to .env.local |
| AI chatbot gives basic responses | Gemini key missing → local fallback active | Works correctly; add GEMINI_API_KEY for full AI |
| XGBoost recommendations falling back | Model not trained | Run `python ml/train_xgb_rank.py` |
| Weight forecast unavailable | FastAPI not running or no weight history | Start FastAPI; log at least 3 weight entries |
| Barcode not recognized | Camera permissions denied or barcode unclear | Grant camera access; hold barcode steady |
| Food not found in search | Food not in dataset | Use "Create Custom Food" to add it |
| "Too many requests" | Rate limit exceeded | Wait 60 seconds then retry |
