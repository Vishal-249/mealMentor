# MealMentor — Screenshot Checklist for Academic Report

## Instructions
Use this checklist to capture the required screenshots from the running application for your project report. Annotate each screenshot with the figure number and caption before adding to your report.

---

## Screenshot List

| # | Page / Feature | URL (Local) | What Must Be Visible | Report Section | Caption |
|---|---------------|-------------|---------------------|----------------|---------|
| 1 | Login Page | `/login` | Logo, email/password fields, Google Sign-in button, "Forgot password" link | Chapter 6.7 | **Fig 6.1:** MealMentor Login Page showing email/password authentication and Google OAuth option |
| 2 | Registration Page | `/register` | Name, email, password fields, registration form | Chapter 6.7 | **Fig 6.2:** User Registration form |
| 3 | Profile Setup | `/profile` | Age, height, weight, gender, activity level, goal, food preference dropdowns; allergies and health condition fields | Chapter 6.7 | **Fig 6.3:** User Profile Setup — Biometric and dietary preference input form |
| 4 | Main Dashboard | `/dashboard` | Calorie ring/progress, macro progress bars, streak strip, hydration summary, forecast card, nudges | Chapter 6.7 | **Fig 6.4:** Main Dashboard — Daily nutrition overview with calorie target, macros, streaks, and water tracking |
| 5 | Nutrition Targets Page | `/nutrition` | All 10 nutrient progress bars (calories, protein, carbs, fat, fiber, sugar, sodium, calcium, iron, vitamin C) with graded statuses | Chapter 6.7 | **Fig 6.5:** Nutrition Tracking Page — Real-time nutrient gap progress bars with deficiency status indicators |
| 6 | Meal Plan Page | `/meal-plan` | AI-generated breakfast, lunch, snack, dinner cards with food name, serving size, nutrition, cost, like/dislike buttons | Chapter 6.7 | **Fig 6.6:** AI Meal Plan — XGBoost-ranked meal recommendations with portion optimization |
| 7 | Food Tracking — Search | `/food-tracking` | Search bar with food results, quantity input, meal type selector | Chapter 6.7 | **Fig 6.7:** Food Tracking — Meal logging interface with food search |
| 8 | Food Tracking — Logged Today | `/food-tracking` | List of today's logged food items with per-item nutrition summary | Chapter 6.7 | **Fig 6.8:** Today's food log showing logged meals with quantity-scaled nutrition |
| 9 | Barcode Scan Page | `/barcode-scan` | Camera feed with scan overlay, product result card showing nutrition info | Chapter 6.7 | **Fig 6.9:** Barcode Scanning feature showing packaged food nutrition lookup via OpenFoodFacts |
| 10 | Food Photo Analysis | `/food-photo` | Upload area or camera view; analysis result showing detected foods, confidence scores, nutrition estimates | Chapter 6.7 | **Fig 6.10:** Food Photo Analysis — Gemini Vision AI identifying food items from an uploaded image |
| 11 | AI Assistant Chat | `/ai-assistant` | Chat interface with user message and AI response showing BMR/TDEE/nutrition advice | Chapter 6.7 | **Fig 6.11:** AI Nutrition Chatbot — Personalized dietary advice powered by Google Gemini (with local fallback) |
| 12 | Progress Page — Weight Chart | `/progress` | Line chart of weight history, add weight entry button | Chapter 6.7 | **Fig 6.12:** Weight Progress Chart — Historical weight trend visualization |
| 13 | Progress Page — 7-Day Nutrition | `/progress` | 7-day nutrition intake vs targets area chart for all macros | Chapter 6.7 | **Fig 6.13:** 7-Day Nutrition History — Weekly intake averages vs daily targets |
| 14 | Weight Forecast Card | `/dashboard` or `/progress` | Forecast card showing predicted 7-day weight change with current weight | Chapter 6.7 | **Fig 6.14:** 7-Day Weight Forecast — Random Forest ML prediction of weight change |
| 15 | Grocery List | `/grocery` | Generated ingredient list from meal plan with item names, quantities, estimated prices | Chapter 6.7 | **Fig 6.15:** Auto-Generated Grocery List based on today's meal plan |
| 16 | Custom Food Creation | `/my-recipes` | Form to create custom food with name, nutrition, ingredient list | Chapter 6.7 | **Fig 6.16:** Custom Food Creation form with ingredient-based nutrition auto-calculation |
| 17 | Streak Display | `/dashboard` | Streak strip showing current streak, longest streak, next milestone | Chapter 6.7 | **Fig 6.17:** Habit Streak Tracking — Daily logging streak with milestone gamification |
| 18 | Hydration Tracker | `/dashboard` | Water intake progress bar, add water button, daily target | Chapter 6.7 | **Fig 6.18:** Water Intake Tracking with weight-based daily target |
| 19 | Settings Page | `/settings` | Account settings, name change, password change | Chapter 6.7 | **Fig 6.19:** Account Settings Page |
| 20 | Mobile Responsive View | Any page | Sidebar collapsed, mobile-friendly layout | Chapter 6.7 | **Fig 6.20:** Responsive Design — Mobile view of MealMentor dashboard |

---

## Screenshot Capture Instructions

### Requirements
- Use Google Chrome or Firefox
- Set browser zoom to 100%
- Use a consistent window size: 1440×900 for desktop, 390×844 for mobile simulation
- Ensure you are logged in with a profile that has all fields filled (age, weight, goal, etc.) for the best screenshots
- Clear any test data from the nutrition tracking page before taking the dashboard screenshot, or ensure some realistic data is logged

### How to Simulate Mobile View
1. Press F12 to open Developer Tools
2. Click the "Toggle Device Toolbar" icon (or Ctrl+Shift+M)
3. Select "iPhone 14 Pro" from the device dropdown
4. Navigate to the desired page

### Screenshot Tool Options (Windows)
- **Snipping Tool**: Search "Snipping Tool" in Start → New → Select area
- **Greenshot** (free): Install from greenshot.org — screenshot + annotation
- **ShareX** (free): Advanced screenshot with annotation capabilities
- **Win+Shift+S**: Windows built-in screenshot to clipboard

### Annotation Recommendations
- Add a red or orange border/box to highlight the specific feature being demonstrated
- Add figure numbers in the bottom-left corner
- Crop to remove browser chrome unless browser chrome adds context

---

## Figure Numbering Convention for Report

Use sequential numbering within each chapter:
- Chapter 3 figures: Fig 3.1, Fig 3.2, ...
- Chapter 4 figures: Fig 4.1, Fig 4.2, ...
- Chapter 5 figures: Fig 5.1, Fig 5.2, ...
- Chapter 6 figures: Fig 6.1, Fig 6.2, ... (screenshots mainly go here)

Always include a List of Figures page after the Table of Contents listing all figures with page numbers.
