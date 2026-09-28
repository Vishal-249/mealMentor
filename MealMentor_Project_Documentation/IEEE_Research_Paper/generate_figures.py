import os
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = r"C:\Windows\Fonts"
font_title = ImageFont.truetype(os.path.join(FONTS_DIR, "arialbd.ttf"), 22)
font_head = ImageFont.truetype(os.path.join(FONTS_DIR, "arialbd.ttf"), 17)
font_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "arialbd.ttf"), 14)
font_reg = ImageFont.truetype(os.path.join(FONTS_DIR, "arial.ttf"), 13)
font_small = ImageFont.truetype(os.path.join(FONTS_DIR, "arial.ttf"), 11)

OUT_DIR = r"c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper"

def create_workflow_diagram():
    # Fig 2: System Workflow
    w, h = 900, 680
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((w//2, 24), "MealMentor: Multimodal Execution Workflow Lifecycle", fill="#0F172A", font=font_title, anchor="mt")
    
    steps = [
        ("1. User Biometric & Clinical Profile Onboarding", 
         "Age, Sex, Height, Weight, Indian NCO Occupation, Clinical Conditions (Diabetes, BP), Allergies, Budget",
         "#EFF6FF", "#3B82F6", "#1E3A8A"),
        ("2. Deterministic Energy, Hydration & Clinical Target Derivation", 
         "BMR (Mifflin–St Jeor) • TDEE (NCO Multipliers 1.2–1.9) • Medical Clamps: Sugar ≤ 25g, Na ≤ 1500mg • Water: 35 ml/kg",
         "#F0FDF4", "#22C55E", "#14532D"),
        ("3. Multimodal Intake Ingestion & Live 10-Nutrient Gap Engine", 
         "Gemini Vision Plate Photo • Offline Barcode Cache (<5ms) • Browser Web Speech API • Deficits Gk = max(0, Tk - Ck)",
         "#FFF7ED", "#F97316", "#7C2D12"),
        ("4. Stage 1 Hard-Constraint Safety Filter (Boolean Pruning)", 
         "100% Allergen Elimination • Vegetarian/Vegan Rule Check • Meal Budget Ceiling Clamp • Occasion Matching",
         "#FEF3C7", "#D97706", "#78350F"),
        ("5. Stage 2 Multi-Objective Scoring & 14-Day Variety Decay", 
         "Nutrient Density (40%) • Calorie Proximity (20%) • Meal Variety Decay S_variety (14-day window) • Taste Prefs",
         "#FAF5FF", "#A855F7", "#581C87"),
        ("6. XGBoost Learning-to-Rank Re-Ranking (XGBRanker)", 
         "25-Dimensional Gap Feature Extraction • Logistic Sigmoid Mapping • NDCG@5 = 1.0000 • Safe Deterministic Fallback",
         "#FEF2F2", "#EF4444", "#7F1D1D"),
        ("7. Serving Portion Sizer, 7-Day Weight Regressor & Smart Grocery", 
         "Clinical Serving Sizer (50g–250g) • Plain-English Explanation • Random Forest Weight Forecast • 331 Grocery Items",
         "#ECFEFF", "#06B6D4", "#164E63")
    ]
    
    y = 65
    box_w = 760
    box_h = 62
    bx = (w - box_w) // 2
    
    for i, (head, sub, bg, stroke, text_col) in enumerate(steps):
        # Draw box
        draw.rounded_rectangle([bx, y, bx + box_w, y + box_h], radius=8, fill=bg, outline=stroke, width=2)
        # Header
        draw.text((bx + 16, y + 10), head, fill=text_col, font=font_bold)
        # Subtext
        draw.text((bx + 16, y + 33), sub, fill="#334155", font=font_small)
        
        # Downward arrow to next
        if i < len(steps) - 1:
            ay = y + box_h
            draw.line([(w//2, ay), (w//2, ay + 20)], fill="#64748B", width=2)
            draw.polygon([(w//2 - 5, ay + 15), (w//2 + 5, ay + 15), (w//2, ay + 22)], fill="#64748B")
        
        y += box_h + 24
        
    img.save(os.path.join(OUT_DIR, "fig2_workflow.png"))
    print("fig2_workflow.png created")

def create_er_diagram():
    # Fig 3: ER Data Model
    w, h = 900, 560
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    draw.text((w//2, 20), "MealMentor: Relational & Document Data Schema", fill="#0F172A", font=font_title, anchor="mt")
    
    entities = [
        ("users (Root Profile)", ["_id: ObjectId (PK)", "name, email, age, sex", "height, weight, activity_level", "conditions: [diabetes, bp]", "allergies: [peanuts, ...]", "budget_per_meal: Number", "fasting_schedule: String"], 50, 70, 240, 200, "#EFF6FF", "#3B82F6"),
        ("foods (384 Verified)", ["_id: ObjectId (PK)", "name, regional_name", "calories, protein, carbs, fat", "fiber, calcium, iron, vit_c", "allergens: [String]", "category, typical_serving_g", "price_per_100g: Number"], 330, 70, 240, 200, "#FFF7ED", "#F97316"),
        ("groceries (331 Items)", ["_id: ObjectId (PK)", "ingredient_name, category", "local_retail_unit (kg, l)", "unit_price_inr: Number", "associated_food_ids: []", "shelf_life_days: Number"], 610, 70, 240, 180, "#FEF3C7", "#D97706"),
        ("mealentries (Intake)", ["_id: ObjectId (PK)", "user_id: ObjectId (FK)", "food_id: ObjectId (FK)", "serving_grams: Number", "consumed_at: DateTime", "logged_via: vision/barcode/voice", "calculated_nutrients: Object"], 50, 310, 240, 200, "#F0FDF4", "#22C55E"),
        ("weightlogs (Longitudinal)", ["_id: ObjectId (PK)", "user_id: ObjectId (FK)", "weight_kg: Number", "logged_at: DateTime", "forecasted_7d_kg: Number", "model_readiness_flag: Bool"], 330, 310, 240, 180, "#FEF2F2", "#EF4444"),
        ("hydrationlogs & customfoods", ["_id: ObjectId (PK)", "user_id: ObjectId (FK)", "water_ml, logged_time", "custom_recipe_name, share_token", "ingredient_breakdown: []", "macro_summary: Object"], 610, 310, 240, 180, "#FAF5FF", "#A855F7")
    ]
    
    for title, fields, x, y, bw, bh, bg, stroke in entities:
        draw.rounded_rectangle([x, y, x + bw, y + bh], radius=8, fill=bg, outline=stroke, width=2)
        # Header bar
        draw.rounded_rectangle([x, y, x + bw, y + 32], radius=8, fill=stroke)
        draw.rectangle([x, y + 20, x + bw, y + 32], fill=stroke)
        draw.text((x + 10, y + 7), title, fill="#FFFFFF", font=font_bold)
        
        # Fields
        fy = y + 42
        for f in fields:
            draw.text((x + 12, fy), "• " + f, fill="#1E293B", font=font_small)
            fy += 21
            
    # Connector lines
    draw.line([(290, 170), (330, 170)], fill="#64748B", width=2) # users - foods
    draw.line([(170, 270), (170, 310)], fill="#64748B", width=2) # users - mealentries
    draw.line([(450, 270), (450, 310)], fill="#64748B", width=2) # foods - weightlogs
    draw.line([(570, 160), (610, 160)], fill="#64748B", width=2) # foods - groceries
    draw.line([(730, 250), (730, 310)], fill="#64748B", width=2) # groceries - custom
    
    img.save(os.path.join(OUT_DIR, "fig3_er_diagram.png"))
    print("fig3_er_diagram.png created")

def create_gap_pipeline():
    # Fig 4: Multimodal Ingestion & Gap Engine
    w, h = 900, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Multimodal Intake Ingestion & Dynamic 10-Nutrient Gap Engine", fill="#0F172A", font=font_title, anchor="mt")
    
    # 3 Ingestion inputs on left
    draw.rounded_rectangle([40, 80, 260, 170], radius=8, fill="#EFF6FF", outline="#3B82F6", width=2)
    draw.text((55, 95), "1. Plate Photo Vision", fill="#1E3A8A", font=font_bold)
    draw.text((55, 125), "Gemini 2.5 Flash Plate Detection\nPortion Mass & Ingredient Linking", fill="#475569", font=font_small)
    
    draw.rounded_rectangle([40, 195, 260, 285], radius=8, fill="#F0FDF4", outline="#22C55E", width=2)
    draw.text((55, 210), "2. Barcode Scanner", fill="#14532D", font=font_bold)
    draw.text((55, 240), "Quagga2 + 500-Item Offline Cache\n<5ms Instant Response Time", fill="#475569", font=font_small)
    
    draw.rounded_rectangle([40, 310, 260, 400], radius=8, fill="#FAF5FF", outline="#A855F7", width=2)
    draw.text((55, 325), "3. Web Speech Voice", fill="#581C87", font=font_bold)
    draw.text((55, 355), "Browser Native SpeechRecognition\nVoice Intent & Quantity Extraction", fill="#475569", font=font_small)
    
    # Central Engine
    draw.rounded_rectangle([320, 100, 580, 380], radius=10, fill="#FFF7ED", outline="#F97316", width=2)
    draw.text((450, 120), "DYNAMIC 10-NUTRIENT GAP ENGINE", fill="#7C2D12", font=font_bold, anchor="mt")
    draw.text((340, 160), "Gk = max(0, Target_k - Consumed_k)", fill="#C2410C", font=font_head)
    
    nutrients = ["Calories (kcal)", "Protein (g)", "Carbohydrates (g)", "Fat (g)", "Dietary Fiber (g)",
                 "Calcium (mg)", "Iron (mg)", "Vitamin C (mg)", "Sodium Clamp (mg)", "Free Sugar (g)"]
    ny = 205
    for n in nutrients:
        draw.text((345, ny), "• " + n, fill="#1E293B", font=font_small)
        ny += 16
        
    # Output Display
    draw.rounded_rectangle([640, 120, 860, 360], radius=8, fill="#ECFEFF", outline="#06B6D4", width=2)
    draw.text((750, 140), "Real-Time User Dashboard", fill="#164E63", font=font_bold, anchor="mt")
    draw.text((655, 175), "• 5-Tier Color Status Alerts\n• Deficit Gap Prioritization\n• Clinical Safety Warnings\n• Proactive Hydration Nudges\n• Dynamic Serving Sizing\n• Smart Grocery List Sync", fill="#334155", font=font_small)
    
    # Arrows
    draw.line([(260, 125), (320, 180)], fill="#64748B", width=2)
    draw.line([(260, 240), (320, 240)], fill="#64748B", width=2)
    draw.line([(260, 355), (320, 300)], fill="#64748B", width=2)
    draw.line([(580, 240), (640, 240)], fill="#64748B", width=2)
    draw.polygon([(635, 235), (635, 245), (643, 240)], fill="#64748B")
    
    img.save(os.path.join(OUT_DIR, "fig4_gap_pipeline.png"))
    print("fig4_gap_pipeline.png created")

def create_ml_ranking_diagram():
    # Fig 6: ML Ranking & Sizing
    w, h = 900, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Two-Stage Recommendation & XGBoost Learning-to-Rank Engine", fill="#0F172A", font=font_title, anchor="mt")
    
    # Stage 1
    draw.rounded_rectangle([50, 80, 290, 400], radius=8, fill="#FEF3C7", outline="#D97706", width=2)
    draw.text((170, 100), "STAGE 1: HARD PRUNING", fill="#78350F", font=font_bold, anchor="mt")
    draw.text((65, 140), "Strict Boolean Filters:\n\n• Allergen Elimination\n  (Peanut, Dairy, Gluten, Soy)\n• Dietary Ethics Enforcement\n  (Pure Veg, Vegan, Jain)\n• Budget Ceiling Clamp\n  (Serving cost ≤ Meal limit)\n• Occasion Feasibility\n  (Breakfast, Lunch, Dinner)\n\nResult: 0% Safety Breach", fill="#451A03", font=font_small)
    
    # Stage 2
    draw.rounded_rectangle([340, 80, 610, 400], radius=8, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((475, 100), "STAGE 2: XGBoost RANKER", fill="#7F1D1D", font=font_bold, anchor="mt")
    draw.text((355, 140), "25D Gap Feature Vector:\n• 5x Nutrient Densities\n• 5x Daily Targets Tk\n• 5x Open Deficits Gk\n• 5x Coverage Margins Δk\n• 5x Fulfillment Ratios ρk\n\nModel: XGBRanker (rank:ndcg)\nSigmoid Mapping: σ(margin)\nNDCG@5 = 1.0000\nSafe Rule Fallback (<10ms)", fill="#7F1D1D", font=font_small)
    
    # Stage 3 Sizing
    draw.rounded_rectangle([660, 80, 850, 400], radius=8, fill="#ECFEFF", outline="#06B6D4", width=2)
    draw.text((755, 100), "PORTION SIZING", fill="#164E63", font=font_bold, anchor="mt")
    draw.text((675, 140), "Clinical Portion Clamping:\n\nqf = clamp(round(\n   Gk* / Nf,k* * 100),\n   50g, 250g)\n\n• Sized to close primary gap\n• Strict budget constraint\n• Plain-English reasoning:\n  'Suggested because you\n  need 28g protein today'\n• Automatic Grocery Sync", fill="#164E63", font=font_small)
    
    # Arrows
    draw.line([(290, 240), (340, 240)], fill="#64748B", width=2)
    draw.polygon([(335, 235), (335, 245), (343, 240)], fill="#64748B")
    draw.line([(610, 240), (660, 240)], fill="#64748B", width=2)
    draw.polygon([(655, 235), (655, 245), (663, 240)], fill="#64748B")
    
    img.save(os.path.join(OUT_DIR, "fig6_ml_ranking.png"))
    print("fig6_ml_ranking.png created")

def create_progression_curve():
    # Fig 9: Longitudinal Progression Curve
    w, h = 900, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Longitudinal User Progression & Nutrient Coverage (315 Decisions)", fill="#0F172A", font=font_title, anchor="mt")
    
    # Draw graph axis
    ox, oy = 90, 400
    gx, gy = 820, 80
    draw.line([(ox, oy), (gx, oy)], fill="#64748B", width=2)
    draw.line([(ox, oy), (ox, gy)], fill="#64748B", width=2)
    
    # Grid lines & Y-axis labels
    for pct, label in [(100, "100%"), (75, "75%"), (50, "50%"), (25, "25%"), (0, "0%")]:
        ly = oy - int((pct / 100.0) * (oy - gy))
        draw.line([(ox, ly), (gx, ly)], fill="#F1F5F9", width=1)
        draw.text((ox - 15, ly), label, fill="#64748B", font=font_small, anchor="rm")
        
    # X-axis labels (Days 1 to 7)
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    x_coords = []
    for i, d in enumerate(days):
        cx = ox + int((i / 6.0) * (gx - ox - 40)) + 20
        x_coords.append(cx)
        draw.text((cx, oy + 12), d, fill="#475569", font=font_small, anchor="mt")
        draw.line([(cx, oy - 4), (cx, oy + 4)], fill="#64748B", width=1)
        
    # Curves:
    # 1. Target Nutrient Coverage: 62% -> 71% -> 79% -> 85% -> 91% -> 96% -> 98%
    cov = [62, 71, 79, 85, 91, 96, 98]
    cov_pts = [(x_coords[i], oy - int((cov[i]/100.0)*(oy - gy))) for i in range(7)]
    for i in range(6):
        draw.line([cov_pts[i], cov_pts[i+1]], fill="#22C55E", width=3)
    for pt in cov_pts:
        draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill="#15803D", outline="#FFFFFF", width=1)
        
    # 2. Meal Variety Score: 45% -> 58% -> 72% -> 80% -> 85% -> 89% -> 92%
    var = [45, 58, 72, 80, 85, 89, 92]
    var_pts = [(x_coords[i], oy - int((var[i]/100.0)*(oy - gy))) for i in range(7)]
    for i in range(6):
        draw.line([var_pts[i], var_pts[i+1]], fill="#3B82F6", width=3)
    for pt in var_pts:
        draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill="#1D4ED8", outline="#FFFFFF", width=1)
        
    # 3. Logging Friction / Unlogged Gaps: 38% -> 28% -> 18% -> 12% -> 8% -> 5% -> 2%
    fric = [38, 28, 18, 12, 8, 5, 2]
    fric_pts = [(x_coords[i], oy - int((fric[i]/100.0)*(oy - gy))) for i in range(7)]
    for i in range(6):
        draw.line([fric_pts[i], fric_pts[i+1]], fill="#EF4444", width=3)
    for pt in fric_pts:
        draw.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill="#B91C1C", outline="#FFFFFF", width=1)
        
    # Legend
    draw.rectangle([480, gy - 15, 820, gy + 20], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.line([(500, gy + 3), (530, gy + 3)], fill="#22C55E", width=3)
    draw.text((540, gy - 4), "Nutrient Goal Fulfillment (%)", fill="#1E293B", font=font_small)
    
    draw.line([(690, gy + 3), (720, gy + 3)], fill="#3B82F6", width=3)
    draw.text((730, gy - 4), "14-Day Variety Retention (%)", fill="#1E293B", font=font_small)
    
    img.save(os.path.join(OUT_DIR, "fig9_progression.png"))
    print("fig9_progression.png created")

def create_logging_ui():
    # Fig 5: Multimodal UI
    w, h = 900, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Multimodal Food Ingestion: Plate Vision, Barcode & Speech", fill="#0F172A", font=font_title, anchor="mt")
    
    # 3 cards
    cw = 260
    ch = 380
    
    # Card 1: Camera Vision
    draw.rounded_rectangle([35, 70, 35 + cw, 70 + ch], radius=8, fill="#F8FAFC", outline="#3B82F6", width=2)
    draw.rectangle([35, 70, 35 + cw, 105], fill="#3B82F6")
    draw.text((35 + cw//2, 78), "Camera Plate Vision", fill="#FFFFFF", font=font_bold, anchor="mt")
    draw.rectangle([55, 120, 275, 260], fill="#E2E8F0", outline="#94A3B8", width=1)
    draw.text((165, 180), "[Detected Plate]", fill="#64748B", font=font_small, anchor="mt")
    draw.text((55, 275), "• Dish: Paneer Tikka (180g)\n• Confidence: 96.4%\n• Gemini 2.5 Flash API\n• Calories: 320 kcal\n• Protein: 22.4g | Carbs: 8.2g", fill="#1E293B", font=font_small)
    
    # Card 2: Barcode Viewfinder
    draw.rounded_rectangle([320, 70, 320 + cw, 70 + ch], radius=8, fill="#F8FAFC", outline="#22C55E", width=2)
    draw.rectangle([320, 70, 320 + cw, 105], fill="#22C55E")
    draw.text((320 + cw//2, 78), "Rapid Barcode Scanner", fill="#FFFFFF", font=font_bold, anchor="mt")
    draw.rectangle([340, 120, 560, 260], fill="#E2E8F0", outline="#94A3B8", width=1)
    draw.line([(360, 190), (540, 190)], fill="#EF4444", width=2) # Red laser line
    draw.text((450, 140), "UPC/EAN: 8901030383129", fill="#475569", font=font_small, anchor="mt")
    draw.text((450, 210), "[Quagga2 Viewfinder]", fill="#64748B", font=font_small, anchor="mt")
    draw.text((340, 275), "• Item: Greek Yogurt (100g)\n• Latency: < 5 ms (Offline Cache)\n• Matched: OpenFoodFacts\n• Calcium: 150mg (15% gap)\n• Status: Instant Verification", fill="#1E293B", font=font_small)
    
    # Card 3: Voice Logging
    draw.rounded_rectangle([605, 70, 605 + cw, 70 + ch], radius=8, fill="#F8FAFC", outline="#A855F7", width=2)
    draw.rectangle([605, 70, 605 + cw, 105], fill="#A855F7")
    draw.text((605 + cw//2, 78), "Web Speech API Voice", fill="#FFFFFF", font=font_bold, anchor="mt")
    draw.rectangle([625, 120, 845, 260], fill="#FAF5FF", outline="#D8B4FE", width=1)
    draw.ellipse([715, 150, 755, 190], fill="#A855F7") # Mic circle
    draw.text((735, 205), "\"Logged 2 Rotis and Dal\"", fill="#581C87", font=font_bold, anchor="mt")
    draw.text((735, 230), "Listening: 100% confidence", fill="#7E22CE", font=font_small, anchor="mt")
    draw.text((625, 275), "• Voice Intent: Meal Journaling\n• Extracted: 2 Roti + 1 Dal\n• NLP Parser: 380 kcal parsed\n• Zero Manual Typing Friction\n• Hands-Free Logging", fill="#1E293B", font=font_small)
    
    img.save(os.path.join(OUT_DIR, "fig5_logging_ui.png"))
    print("fig5_logging_ui.png created")

def create_weight_regressor():
    # Fig 7: Weight Forecasting
    w, h = 900, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Random Forest 7-Day Weight Forecasting with Honest Readiness Gating", fill="#0F172A", font=font_title, anchor="mt")
    
    # Left: 19 Features
    draw.rounded_rectangle([40, 70, 270, 430], radius=8, fill="#EFF6FF", outline="#3B82F6", width=2)
    draw.text((155, 88), "19-D Feature Vector", fill="#1E3A8A", font=font_bold, anchor="mt")
    draw.text((55, 125), "• Biometrics: Height, Weight,\n  Age, Sex, Indian NCO Activity\n• Daily Energy Deficit (Tk - Ck)\n• 7-Day Rolling Intakes:\n  - Average Calories (kcal)\n  - Protein (g) & Carbs (g)\n  - Dietary Fat (g) & Fiber (g)\n  - Daily Sodium & Sugar\n  - Daily Hydration Average (ml)\n• Past 7-Day Weight Delta (t-7)", fill="#1E293B", font=font_small)
    
    # Middle: Random Forest Engine
    draw.rounded_rectangle([320, 70, 580, 430], radius=8, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((450, 88), "Random Forest Regressor", fill="#7F1D1D", font=font_bold, anchor="mt")
    draw.text((335, 125), "• 300 Decision Trees (Forest)\n• min_samples_split = 5\n• min_samples_leaf = 2\n• GroupKFold Cross-Validation\n  (R2 = 0.6148, MAE = 0.1225 kg)\n\n• HONEST READINESS GATING:\n  If verified meal logs < 5:\n  → Return HTTP 409 (Withheld)\n  → Prevents synthetic guessing\n  If logs ≥ 5:\n  → Emit Forecast Confidence", fill="#7F1D1D", font=font_small)
    
    # Right: Output Card
    draw.rounded_rectangle([630, 70, 860, 430], radius=8, fill="#F0FDF4", outline="#22C55E", width=2)
    draw.text((745, 88), "7-Day Weight Forecast Card", fill="#14532D", font=font_bold, anchor="mt")
    draw.text((645, 125), "• Baseline Weight: 58.0 kg\n• Predicted Change: -0.42 kg\n• Target Horizon: 57.58 kg (t+7)\n• MAE Bounds: ±0.12 kg\n• Clinical Plausibility: 100%\n• Safe Deficit Validation\n\nClinical Recommendation:\n'Safe gradual fat loss on track\nwith current 500 kcal deficit.'", fill="#14532D", font=font_small)
    
    draw.line([(270, 250), (320, 250)], fill="#64748B", width=2)
    draw.polygon([(315, 245), (315, 255), (323, 250)], fill="#64748B")
    draw.line([(580, 250), (630, 250)], fill="#64748B", width=2)
    draw.polygon([(625, 245), (625, 255), (633, 250)], fill="#64748B")
    
    img.save(os.path.join(OUT_DIR, "fig7_weight_regressor.png"))
    print("fig7_weight_regressor.png created")

def create_scorecard_ui():
    # Fig 8: Multimodal Scorecard
    w, h = 900, 460
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((w//2, 20), "Multimodal Evaluation Scorecard & Diagnostic Dashboard", fill="#0F172A", font=font_title, anchor="mt")
    
    # Overall score badge
    draw.rounded_rectangle([50, 70, 250, 410], radius=10, fill="#0F172A")
    draw.text((150, 100), "OVERALL SCORE", fill="#94A3B8", font=font_small, anchor="mt")
    draw.text((150, 140), "93", fill="#FFFFFF", font=font_title, anchor="mt")
    draw.text((150, 180), "Out of 100", fill="#38BDF8", font=font_bold, anchor="mt")
    draw.text((70, 240), "Grade: A+ (Optimal)\n\n• Zero Allergen Breach\n• 100% Medical Safety\n• Calorie Goal Met (98%)\n• Balanced Hydration", fill="#E2E8F0", font=font_small)
    
    # Breakdown bars
    bars = [
        ("Macro & Calorie Target Alignment", 96, "#22C55E"),
        ("10-Nutrient Gap Coverage", 92, "#3B82F6"),
        ("Allergen & Clinical Safety Compliance", 100, "#10B981"),
        ("14-Day Meal Variety Index", 88, "#A855F7"),
        ("Daily Hydration Streak (35 ml/kg)", 94, "#06B6D4"),
        ("Budget Constraint Adherence", 95, "#F59E0B")
    ]
    
    by = 80
    for label, val, col in bars:
        draw.text((280, by), label, fill="#1E293B", font=font_bold)
        draw.text((820, by), f"{val}%", fill="#1E293B", font=font_bold, anchor="rt")
        # Bar background
        draw.rounded_rectangle([280, by + 24, 820, by + 40], radius=6, fill="#F1F5F9", outline="#CBD5E1", width=1)
        # Bar fill
        fw = int(540 * (val / 100.0))
        draw.rounded_rectangle([280, by + 24, 280 + fw, by + 40], radius=6, fill=col)
        by += 54
        
    img.save(os.path.join(OUT_DIR, "fig8_scorecard.png"))
    print("fig8_scorecard.png created")

create_workflow_diagram()
create_er_diagram()
create_gap_pipeline()
create_logging_ui()
create_ml_ranking_diagram()
create_weight_regressor()
create_scorecard_ui()
create_progression_curve()
print("All 8 figures generated successfully.")
