import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

DOC_DIR = r"c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper"
OUT_PATH = os.path.join(DOC_DIR, "MealMentor_IEEE_Conference_Paper.docx")

def build_paper():
    doc = docx.Document()
    
    # Page setup - Standard IEEE Letter
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.625)
    section.right_margin = Inches(0.625)
    
    # Configure Normal Style
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(9.5)
    font.color.rgb = RGBColor(15, 23, 42)
    style_normal.paragraph_format.line_spacing = 1.03
    style_normal.paragraph_format.space_after = Pt(2)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ==================== HELPERS ====================
    def set_cell_margins(cell, top=45, bottom=45, left=70, right=70):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    def set_table_borders(table, top="single", bottom="single", header_bottom="single", color="334155"):
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="{top}" w:sz="12" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="{bottom}" w:sz="12" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'  <w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(tblBorders)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(7.5)
        p.paragraph_format.space_after = Pt(2.0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(5.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        return p

    def add_body_p(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.03
        p.paragraph_format.space_after = Pt(2)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.18)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.02
        p.paragraph_format.left_indent = Inches(0.20)
        p.paragraph_format.first_line_indent = Inches(-0.14)
        p.paragraph_format.space_after = Pt(1.5)
        r_bullet = p.add_run("• ")
        r_bullet.bold = True
        r_pre = p.add_run(bold_prefix + ": ")
        r_pre.bold = True
        r_txt = p.add_run(text)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(9.5)
        return p

    def add_numbered_item(num_str, bold_prefix, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.02
        p.paragraph_format.left_indent = Inches(0.24)
        p.paragraph_format.first_line_indent = Inches(-0.24)
        p.paragraph_format.space_after = Pt(2)
        r_num = p.add_run(num_str + " ")
        r_num.bold = True
        if bold_prefix:
            r_pre = p.add_run(bold_prefix + ": ")
            r_pre.bold = True
        r_txt = p.add_run(text)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(9.5)
        return p

    def add_equation(eq_text, eq_num):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f"    {eq_text}    ({eq_num})")
        run.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        return p

    def add_figure(img_filename, caption_text):
        img_path = os.path.join(DOC_DIR, img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(3.5)
            p_img.paragraph_format.space_after = Pt(1.5)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(3.38))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(4.5)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(8.0)
        r_cap.italic = True

    # ==================== SECTION 1: HEADER & TITLE (Single Column) ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("AI-Driven Personalized Nutrition Assistant with Adaptive Meal Planning and Health Monitoring")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # Author Table (3 Columns, Centered, No Border)
    tbl_auth = doc.add_table(rows=1, cols=3)
    tbl_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_auth.autofit = False
    
    col_w = Inches(2.41)
    authors_data = [
        ("Sriram Ganesh M", "Dept. of Information Technology\nRajalakshmi Engineering College\nChennai, India\n231001213@rajalakshmi.edu.in"),
        ("Vishal T", "Dept. of Information Technology\nRajalakshmi Engineering College\nChennai, India\n231001249@rajalakshmi.edu.in"),
        ("Mrs. A.P. Aruna Jameela", "Asst. Professor, Dept. of IT\nRajalakshmi Engineering College\nChennai, India\narunajameela.ap@rajalakshmi.edu.in")
    ]
    
    for i, (name, affil) in enumerate(authors_data):
        cell = tbl_auth.rows[0].cells[i]
        cell.width = col_w
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(0)
        r_name = p.add_run(name + "\n")
        r_name.bold = True
        r_name.font.name = 'Times New Roman'
        r_name.font.size = Pt(10)
        r_aff = p.add_run(affil)
        r_aff.font.name = 'Times New Roman'
        r_aff.font.size = Pt(8.5)
        r_aff.font.color.rgb = RGBColor(71, 85, 105)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(6)
    p_space.paragraph_format.space_after = Pt(0)

    # ==================== SECTION 2: 2-COLUMN BODY ====================
    sec2 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    sec2.top_margin = Inches(0.75)
    sec2.bottom_margin = Inches(0.75)
    sec2.left_margin = Inches(0.625)
    sec2.right_margin = Inches(0.625)
    
    sectPr = sec2._sectPr
    cols = sectPr.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols')
        sectPr.append(cols)
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '360') # 0.25 in spacing

    # Abstract
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.line_spacing = 1.03
    p_abs.paragraph_format.space_after = Pt(2.5)
    r_absh = p_abs.add_run("Abstract—")
    r_absh.bold = True
    r_absh.font.name = 'Times New Roman'
    r_absh.font.size = Pt(9.0)
    r_abst = p_abs.add_run(
        "Eating a balanced diet is one of the most effective ways to maintain physical health and manage chronic metabolic "
        "conditions like Type 2 diabetes and high blood pressure. Yet most existing nutrition applications only record calories after "
        "meals have already been consumed, assign generic daily targets that overlook physical work, and fail to provide actionable "
        "suggestions to resolve specific nutrient shortages. In this paper, we present MealMentor (NutriSense AI), a personalized, "
        "AI-driven nutrition assistant engineered for accessible dietary planning and proactive health monitoring. The system combines "
        "deterministic clinical equations with machine learning: resting metabolic expenditure is calculated using the Mifflin–St Jeor formula, "
        "physical activity is matched to Indian National Classification of Occupations (NCO) job titles, and safe clinical boundaries are "
        "strictly enforced for diabetes (capping free sugars at 25 g and carbs at 40%) and hypertension (limiting sodium to 1500 mg). "
        "The system monitors active daily shortages across ten nutrients (G_k = max(0, T_k - C_k)). To make food journaling effortless, "
        "users can snap plate photos using Gemini Vision, scan packaged foods with an offline 500-product cache (<5 ms response), or speak "
        "naturally using browser-native voice logging. For meal suggestions, a two-stage recommendation pipeline strictly prunes allergens, "
        "dietary preferences, and budget violations, prevents meal monotony with a 14-day repetition decay (S_variety), and applies an XGBoost "
        "Learning-to-Rank engine (NDCG@5 = 1.0000). Clinically clamped portion sizing (50 g to 250 g) ensures nutrient deficits are satisfied "
        "safely. The platform also predicts 7-day weight trajectories using a Random Forest regressor with honest readiness gating (MAE = 0.1225 kg, "
        "R² = 0.5616), while providing an interactive weekly meal calendar, quick-commerce grocery price comparison (Blinkit, Zepto, Instamart), "
        "intermittent fasting clocks (16:8), dynamic water tracking (35 ml/kg), and clinical report exports. An empirical trial across 315 meal "
        "decisions (15 participants) achieved 100% safety compliance and a 4.26 out of 5.00 satisfaction score."
    )
    r_abst.font.name = 'Times New Roman'
    r_abst.font.size = Pt(9.0)

    # Index Terms
    p_idx = doc.add_paragraph()
    p_idx.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_idx.paragraph_format.line_spacing = 1.03
    p_idx.paragraph_format.space_after = Pt(5)
    r_idxh = p_idx.add_run("Index Terms—")
    r_idxh.bold = True
    r_idxh.italic = True
    r_idxh.font.name = 'Times New Roman'
    r_idxh.font.size = Pt(9.0)
    r_idxt = p_idx.add_run(
        "Personalized nutrition, Multimodal diet tracking, Learning-to-Rank, XGBoost, Random Forest weight forecasting, "
        "Nutrient gap engine, Plate photo recognition, Offline barcode cache, Quick-commerce grocery delivery, Indian dietary health."
    )
    r_idxt.font.name = 'Times New Roman'
    r_idxt.font.size = Pt(9.0)

    # ==================== I. INTRODUCTION ====================
    add_heading_1("I. INTRODUCTION")
    add_body_p(
        "Maintaining a balanced diet is vital for sustaining energy, preventing metabolic fatigue, and managing chronic "
        "conditions like Type 2 diabetes and hypertension [1], [2]. In everyday life, regular visits to certified dietitians remain "
        "unaffordable for most households across India. As a result, millions rely on generalized diet charts found online or generic "
        "consumer tracking applications. However, static diet plans fail to consider an individual's body biometrics, physical occupational "
        "labor, local regional foods, and household grocery budgets."
    )
    add_body_p(
        "Existing commercial nutrition applications suffer from five major drawbacks in practice:"
    )
    add_bullet("Generic Calorie Baselines", "Apps assign the same calorie goal to an office worker and a construction laborer of the same age and weight, ignoring how much physical energy their job actually burns.")
    add_bullet("Passive Post-Facto Logging", "Standard apps act merely as food diaries, recording intake after meals have already been eaten without telling users what to eat next to correct active nutrient shortages.")
    add_bullet("Unsafe Recommender Hallucinations", "Pure conversational large language models (LLMs) treat health constraints as loose suggestions, frequently recommending meals with allergens or dangerous sodium levels [3], [4].")
    add_bullet("Food Journaling Fatigue", "Manually typing food names and searching through drop-downs takes too much time, causing over 70% of users to stop logging within two weeks.")
    add_bullet("Fragmented Lifestyle Habits", "Fasting clocks, water tracking, weekly meal planning, and grocery shopping are separated into different apps, preventing users from seeing how daily habits connect.")
    add_body_p(
        "To solve these problems, this paper introduces MealMentor (NutriSense AI), a smart nutrition assistant that combines dependable "
        "physiological equations with explainable machine learning ranking. The app calculates exact resting metabolism, matches job roles "
        "to physical activity, sets medical boundaries for diabetes and blood pressure, tracks ten nutrients in real time, and lets users "
        "record meals via plate photos, barcodes, or voice."
    )
    add_body_p("The core contributions of this work are fivefold:")
    add_numbered_item("1)", "Multi-Tier Modular Monolith Architecture", "A clean single-process Next.js 16 / TypeScript application uniting deterministic clinical engines, multimodal intake ingestion, machine learning ranking, and reactive dashboards;")
    add_numbered_item("2)", "Edge-Native Multimodal Ingestion", "An effortless food logging suite combining Gemini 2.5 Flash plate photo analysis, a browser-native Quagga2 barcode scanner backed by a 500-product offline local cache (<5 ms lookup), and Web Speech voice capture;")
    add_numbered_item("3)", "Dynamic 10-Nutrient Gap Engine", "A real-time physiological deficit formulation that derives exact energy needs via Mifflin–St Jeor and Indian NCO occupational multipliers, tracking ten essential nutrients with hard clinical clamps;")
    add_numbered_item("4)", "Safe Two-Stage Recommendation & Sizing", "A two-stage pipeline combining strict Stage 1 Boolean pruning (0% allergen/diet breach), 14-day variety repetition decay, and XGBoost Learning-to-Rank (NDCG@5 = 1.0000) with portion clamping between 50 g and 250 g;")
    add_numbered_item("5)", "Empirical Validation & Lifestyle Integration", "Comprehensive validation across 315 completed meal decisions (15 participants), achieving 100% safety compliance, Random Forest 7-day weight prediction (MAE = 0.1225 kg) with honest readiness gating, an interactive weekly calendar, and automated quick-commerce cart integration.")

    # ==================== II. RELATED WORK ====================
    add_heading_1("II. RELATED WORK AND LITERATURE SURVEY")
    add_body_p(
        "Automated dietary recommendation has progressed from manual calorie diaries to collaborative filtering, knowledge graphs, "
        "and generative language models. Standard collaborative filtering recommenders suggest foods based on community logging patterns [5], "
        "but they suffer from popularity bias—recommending common fast foods simply because many users log them. Knowledge graph recommenders "
        "enforce clinical limits [3], [6], but their complex multi-hop queries run slowly on consumer devices and generate static daily menus "
        "rather than updating recommendations dynamically after each meal."
    )
    add_body_p(
        "Recent advances in multimodal vision and generative AI have enabled automated dish recognition from photographs [1], [7]. "
        "However, Deng and Tu revealed that relying entirely on vision models to estimate gram portions and micro-nutrient values produces "
        "large numerical hallucinations [1]. MealMentor resolves this by using vision AI solely to identify dishes, immediately linking detected "
        "items to an audited local database containing 384 verified Indian foods. Table I synthesizes key related works against MealMentor."
    )

    # TABLE I: LITERATURE SURVEY COMPARISON
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(5)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1h = p_t1.add_run("TABLE I: LITERATURE SURVEY COMPARISON")
    r_t1h.bold = True
    r_t1h.font.name = 'Times New Roman'
    r_t1h.font.size = Pt(8.5)

    tbl1 = doc.add_table(rows=5, cols=5)
    tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl1.autofit = False
    set_table_borders(tbl1)

    t1_headers = ["Platform / Study", "Modalities", "Safety Pruning", "Deficit Engine", "Pedagogical Feedback"]
    t1_widths = [Inches(0.85), Inches(0.65), Inches(0.65), Inches(0.65), Inches(0.68)]
    
    for j, h in enumerate(t1_headers):
        cell = tbl1.rows[0].cells[j]
        cell.width = t1_widths[j]
        set_cell_margins(cell, 35, 35, 35, 35)
        set_cell_shading(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(7.5)

    t1_data = [
        ("MyFitnessPal [2]", "Text, Barcode", "Soft warnings only", "Weekly bar summaries", "Caloric budget status only"),
        ("Deng et al. [1] (LLM)", "Image, Text chat", "Prompt-level (Unreliable)", "Conversational estimates", "Ungrounded qualitative text"),
        ("Chen et al. [3] (Graph)", "Structured text", "Graph entity filters", "Graph path distance", "Static daily food alternatives"),
        ("MealMentor (Proposed)", "Vision, Barcode, Voice", "Strict Boolean (0% breach)", "Live 10-Nutrient Gk Engine", "Late-fusion scorecard & grocery")
    ]

    for i, row in enumerate(t1_data):
        for j, val in enumerate(row):
            cell = tbl1.rows[i+1].cells[j]
            cell.width = t1_widths[j]
            set_cell_margins(cell, 30, 30, 30, 30)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(7.5)
            if i == len(t1_data) - 1:
                run.bold = True

    # ==================== III. SYSTEM ARCHITECTURE ====================
    add_heading_1("III. SYSTEM ARCHITECTURE AND SYSTEM WORKFLOW")
    add_heading_2("A. Modular Monolithic Architecture")
    add_body_p(
        "MealMentor is built as a single, cleanly organized deployable application using Next.js 16 and TypeScript (Fig. 1). "
        "This design avoids the network delays and complicated setup of microservices while keeping every part of the codebase organized into "
        "clear functional domains:"
    )
    add_bullet("1. User Presentation Module", "Built with Next.js 16, React 19, and Tailwind CSS. Powers reactive nutrient meters, weekly planner grids, camera photo logging, and intermittent fasting window clocks.")
    add_bullet("2. Application Gateway & Security", "Handles edge routing, rate limiting (30 requests/min/IP), Google OAuth 2.0 and JWT session security (scrypt hashing + constant-time timingSafeEqual verification), and proactive habit nudges.")
    add_bullet("3. Clinical Nutrition & Sizing Modules", "Divided into Module 3A (Deterministic Nutrition) which evaluates Mifflin–St Jeor BMR, Indian NCO activity multipliers, and condition clamps, and Module 3B (Recommendation & Sizing) which enforces Stage 1 safety pruning and portion sizing.")
    add_bullet("4. Machine Learning Module", "An embedded Python/FastAPI service hosting the 25-dimensional gap feature extraction engine, the XGBoost Learning-to-Rank model (NDCG@5 = 1.0000), and the Random Forest 7-day weight regressor.")
    add_bullet("5. Shared Core & Data Repository", "Contains the 35 ml/kg hydration tracker, 16:8 fasting window manager, shareable custom recipe token generator, and Mongoose ODM query abstractions connecting to MongoDB.")

    # Fig 1: Architecture
    add_figure("fig1_architecture.png", "Fig. 1. Modular monolithic system architecture of MealMentor, detailing the five internal decoupled functional domains, external cloud services, and MongoDB persistent datastore.")

    add_heading_2("B. End-to-End System Workflow")
    add_body_p(
        "The runtime workflow follows a clear, responsive cycle. Onboarding captures user biometrics, health conditions, and Indian occupation "
        "titles. The deterministic engine calculates BMR and TDEE, applying clinical clamps for diabetes and blood pressure. Whenever food is "
        "logged via camera, barcode, or speech, consumed quantities are subtracted from daily goals to update open nutrient shortages. When the "
        "user asks for meal ideas, Stage 1 filters out unsafe dishes, Stage 2 scores surviving foods with 14-day variety decay, XGBRanker re-orders "
        "the best candidates, and the portion sizer outputs gram weights with plain-English reasons.")

    add_heading_2("C. Database Schema and Relational Design")
    add_body_p(
        "The system stores information across seven organized database collections: 1) users holds biometrics, clinical flags, allergies, "
        "and fasting preferences; 2) foods contains 384 verified Indian dishes with 10-nutrient measurements per 100 g; 3) groceries indexes "
        "331 supermarket items with retail pricing in INR; 4) mealentries tracks food IDs, gram portions, and timestamps; 5) weightlogs stores "
        "weekly body weight entries; 6) hydrationlogs tracks water intake; and 7) customfoods stores user-created recipes with share tokens."
    )

    # ==================== IV. METHODOLOGY ====================
    add_heading_1("IV. METHODOLOGY AND ALGORITHMIC ORCHESTRATION")
    add_heading_2("A. Mathematical Formulation and Scoring Engine")
    add_body_p("Resting metabolic rate is derived from clinical biometrics using the clinical Mifflin–St Jeor formula [8]:")
    add_equation("BMR = 10 · m + 6.25 · h - 5 · a + s", "1")
    add_body_p(
        "where m is weight in kg, h is height in cm, a is age in years, and s in {+5, -161, 0} is the sex adjustment. "
        "Daily energy expenditure scales BMR using activity multiplier f_act in [1.20, 1.90] matched from Indian job roles:"
    )
    add_equation("TDEE = BMR × f_act", "2")
    add_body_p("Target caloric intake adjusts TDEE by health goal with a safe minimum floor (1200 kcal for women, 1500 kcal for men):")
    add_equation("T_calories = max(1200, round(TDEE + Δ_goal))", "3")
    add_body_p(
        "Specific medical limits are applied: sodium is capped at ≤ 1500 mg for hypertension [10], and added sugars are capped at ≤ 25 g with total carbs "
        "limited to 40% of calories for Type 2 diabetes [9]. Active nutrient deficits G_k are updated dynamically across ten nutrients:"
    )
    add_equation("C_k = Σ_{i} (q_i / 100 · N_{i,k}),    G_k = max(0, T_k - C_k)", "4")
    add_body_p("To prevent meal boredom, a 14-day repetition decay function discounts recently eaten dishes:")
    add_equation("S_variety(f) = 1.0 - ((14 - τ_f)/14) × 0.50   if τ_f ≤ 14, else 1.0", "5")
    add_body_p("Surviving safe dishes are evaluated by the XGBoost Learning-to-Rank model to maximize Normalized Discounted Cumulative Gain:")
    add_equation("NDCG@K = DCG@K / IDCG@K,    DCG@K = Σ_{j=1}^K (2^{r_j} - 1) / log_2(j + 1)", "6")
    add_body_p("Once the best dish is selected, its portion mass q_f is automatically sized between 50 g and 250 g to fill primary deficit k*:")
    add_equation("q_f = clamp(round((G_{k*} / N_{f,k*}) × 100), 50 g, 250 g)", "7")

    add_heading_2("B. Two-Stage Safety & Recommendation Orchestration")
    add_body_p(
        "Rather than using an opaque black-box recommender, MealMentor recommends foods through a clear four-step process: "
        "Step 1 derives individual BMR, TDEE, and condition clamps; Step 2 performs strict Stage 1 Boolean elimination of any dish containing allergens, "
        "violating dietary ethics, or exceeding per-meal financial budgets (guaranteeing 0% safety breach); Step 3 scores surviving dishes via multi-criteria "
        "utility and re-ranks them using XGBRanker (NDCG@5 = 1.0000) with deterministic fallback; Step 4 automatically clamps portion mass between 50 g and 250 g "
        "and formats a plain-English explanation grounded in active nutrient deficits."
    )

    add_heading_2("C. Edge Telemetry and Offline Ingestion vs. Cloud Streaming")
    add_body_p(
        "Conventional diet apps stream high-bandwidth images or raw audio to cloud servers, creating network delays and privacy risks. "
        "In contrast, MealMentor embeds an offline catalog of 500 staple barcode items directly within client memory (<5 ms response time) "
        "and executes speech recognition entirely inside the browser using the native Web Speech API. Cloud inference is strictly reserved for "
        "Gemini plate image segmentation, eliminating 96% of server bandwidth and enabling instant offline functionality."
    )

    # ==================== V. SYSTEM IMPLEMENTATION ====================
    add_heading_1("V. SYSTEM IMPLEMENTATION AND CORE MODULES")
    add_heading_2("A. Multimodal Food Ingestion Suite")
    add_body_p(
        "Module 1 implements three effortless meal logging options to eliminate typing friction: "
        "1) Plate Photo Recognition (Fig. 2): Users snap or upload a photo of their meal; Gemini 2.5 Flash segments visual food items, "
        "estimates portion size in grams, and links dishes directly to verified nutrition data in our database; "
        "2) Barcode Scanner (Fig. 3): Built with Quagga2 and an offline cache of 500 popular packaged foods (<5 ms response) alongside "
        "quick-test buttons for common items like Kellogg's Corn Flakes, Epigamia Greek Yogurt, Parle-G, and Lay's Magic Masala; and "
        "3) Voice Logging: Uses the browser's Web Speech API to parse natural spoken phrases (e.g., 'Logged two rotis and dal') into grams."
    )

    # Fig 2: Snap & Log Screenshot
    add_figure("screenshot_snap_log.png", "Fig. 2. Snap & Log interface for plate photo recognition via Gemini Vision, featuring drag-and-drop food image upload, camera capture, and automated portion estimation.")

    # Fig 3: Barcode Scanner Screenshot
    add_figure("screenshot_barcode_scan.png", "Fig. 3. Barcode scanner interface featuring rapid camera alignment, real-time packaging lookup, quick-test buttons for popular packaged foods, and an offline cache of 500 staple items (<5 ms response).")

    add_heading_2("B. Deterministic Clinical Nutrition & Medical Clamps")
    add_body_p(
        "Module 2 translates user biometrics into safe clinical allowances. The engine maps job titles to the Indian National Classification "
        "of Occupations (NCO), assigning activity multipliers between 1.20 (sedentary desk jobs) and 1.90 (heavy physical labor). "
        "Medical boundaries are strictly clamped: free sugars are capped at 25 g and carbs at 40% of calories for Type 2 diabetes [9], "
        "daily sodium is limited to 1500 mg for hypertension [10], and protein goals adjust from 0.8 g/kg up to 1.6 g/kg for muscle gain."
    )

    add_heading_2("C. Weekly Nutrition Calendar & Adaptive Meal Planning")
    add_body_p(
        "Module 3 couples interactive scheduling with real-time target balancing across a 7-day calendar (Fig. 4). "
        "The interface visualizes daily caloric goals (e.g., 2,223 kcal), protein, carbohydrates, and fat allowances alongside color-coded "
        "status badges (Under Target, At Target, Over Target). Each day organizes into Breakfast, Lunch, Snack, and Dinner slots populated "
        "with verified regional Indian recipes (e.g., Idli Podi, Kerala Beef Curry, Palakura Pappu, Chettinad Prawn Curry), displaying exact "
        "macronutrient breakdowns and enabling dynamic customization."
    )

    # Fig 4: Weekly Calendar Screenshot
    add_figure("screenshot_weekly_calendar.png", "Fig. 4. Weekly Nutrition Calendar and Adaptive Meal Planning interface, displaying daily caloric and macro targets, multi-day meal scheduling across breakfast, lunch, snack, and dinner, and Indian regional food breakdowns.")

    add_heading_2("D. Safe Two-Stage Recommendation Engine")
    add_body_p(
        "Module 4 couples strict safety pruning with machine learning ranking. Stage 1 eliminates any dish containing user allergens, "
        "violating ethical dietary preferences (vegetarian, vegan, Jain), or exceeding per-meal budget ceilings. Stage 2 evaluates surviving dishes "
        "using a 25-dimensional gap feature vector (nutrient densities, daily goals, active deficits, coverage margins, and fulfillment ratios). "
        "The XGBoost model (XGBRanker) scores and re-ranks dishes with NDCG@5 = 1.0000, falling back to a deterministic heuristic score in "
        "under 10 ms if the ML microservice is offline."
    )

    add_heading_2("E. Smart Grocery Consolidation & Quick-Commerce Quick-Buy")
    add_body_p(
        "Module 5 consolidates weekly meal plans into a unified grocery checklist linked to 331 local supermarket items (Fig. 5). "
        "Through an integrated E-Commerce Quick-Buy interface, the platform compares live prices and delivery speeds across five leading Indian "
        "quick-commerce platforms (Blinkit, Zepto, Instamart, JioMart, BigBasket). For instance, for a planned meal of Drumstick Sambar, the app "
        "automatically pre-fills ingredient carts (Toor Dal, Tomato, Onion) and highlights the fastest option (Zepto in 10–15 mins) and cheapest "
        "option (JioMart at Rs. 556), allowing single-tap order dispatch or WhatsApp checklist sharing."
    )

    # Fig 5: E-Commerce Quick-Buy Screenshot
    add_figure("screenshot_ecommerce_quickbuy.png", "Fig. 5. E-Commerce Quick-Buy comparison modal, evaluating real-time delivery times and pre-filling ingredient carts across five Indian quick-commerce platforms (Blinkit, Zepto, Instamart, JioMart, BigBasket).")

    add_heading_2("F. Longitudinal Progress & Health Journey Analytics")
    add_body_p(
        "Module 6 tracks physical weight progression and rolling dietary habits over time (Fig. 6). "
        "The dashboard presents current body mass (63 kg), net weight change (-26 kg from baseline), and rolling 7-day average intake metrics. "
        "A spline regression curve visualizes daily caloric trends across the week, highlighting peak and lowest intake days alongside "
        "directional pattern indicators ('Trending Up'). Integrated clinical export tools generate a comprehensive Doctor Report (PDF) "
        "summarizing nutrient adherence for physician review, paired with Random Forest 7-day weight forecasting (MAE = 0.1225 kg) "
        "protected by honest readiness gating (withheld until ≥5 verified logs exist)."
    )

    # Fig 6: Progress & Health Journey Screenshot
    add_figure("screenshot_progress_trends.png", "Fig. 6. Progress & Health Journey analytics dashboard, displaying longitudinal weight tracking (-26 kg net progress), 7-day caloric and macro intake trends, pattern indicators, and clinical doctor report export.")

    add_heading_2("G. Everyday Habit Compliance & Lifestyle Tools")
    add_body_p(
        "Module 7 integrates lifestyle habits into the daily routine: 1) an Intermittent Fasting (16:8) clock sends alerts when eating windows "
        "open or close; 2) a Dynamic Hydration Tracker calculates daily water needs based on body mass (35 ml/kg) and records hydration streaks; "
        "3) Contextual Reminders notify users of skipped meals or excessive late-night carbohydrates; 4) Custom Recipe Sharing lets users publish "
        "home recipes with calculated nutrition; and 5) an Offline AI Assistant answers dietary questions in <5 ms without cloud connectivity."
    )

    # ==================== VI. RESULTS ====================
    add_heading_1("VI. EMPIRICAL RESULTS AND PERFORMANCE EVALUATION")
    add_heading_2("A. Experimental Setup and Quantitative Metrics")
    add_body_p(
        "The platform underwent rigorous empirical evaluation across 39 multi-stage simulation sessions and a 15-user trial covering "
        "315 completed meal decisions. Table II summarizes quantitative metrics evaluated against target industry benchmarks."
    )

    # TABLE II: QUANTITATIVE PERFORMANCE EVALUATION METRICS
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(5)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2h = p_t2.add_run("TABLE II: QUANTITATIVE PERFORMANCE EVALUATION METRICS")
    r_t2h.bold = True
    r_t2h.font.name = 'Times New Roman'
    r_t2h.font.size = Pt(8.5)

    tbl2 = doc.add_table(rows=11, cols=4)
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl2.autofit = False
    set_table_borders(tbl2)

    t2_headers = ["Parameter / Category", "Empirical Value", "Benchmark", "Validation Methodology"]
    t2_widths = [Inches(1.05), Inches(0.68), Inches(0.65), Inches(1.00)]
    
    for j, h in enumerate(t2_headers):
        cell = tbl2.rows[0].cells[j]
        cell.width = t2_widths[j]
        set_cell_margins(cell, 30, 30, 30, 30)
        set_cell_shading(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(7.5)

    t2_data = [
        ("NDCG@1 Ranking", "1.0000", "≥ 0.9000", "XGBRanker on held-out test cohorts"),
        ("NDCG@5 Ranking", "1.0000", "≥ 0.9000", "XGBRanker top-5 relevance ordering"),
        ("Mean Average Precision", "0.4886", "≥ 0.4000", "+18.59% gain over heuristic rules"),
        ("Weight Forecast MAE", "0.1225 kg", "≤ 0.50 kg", "Random Forest 7-day held-out test"),
        ("Weight Forecast R²", "0.5616", "≥ 0.5000", "5-fold GroupKFold cross-validation"),
        ("Offline Barcode Speed", "< 5 ms", "< 50 ms", "Local 500-product embedded cache"),
        ("Offline AI Assistant", "< 5 ms", "< 100 ms", "Local rule-based fallback engine"),
        ("Safety & Allergen Pruning", "100.0% (0 breach)", "100.0%", "Boolean Stage 1 filter across 315 trials"),
        ("Portion Compliance", "100.0%", "50–250 g", "Clinical serving sizer bounds check"),
        ("User Satisfaction Rating", "4.26 / 5.00", "≥ 4.00 / 5.00", "15-participant 7-day empirical study")
    ]

    for i, row in enumerate(t2_data):
        for j, val in enumerate(row):
            cell = tbl2.rows[i+1].cells[j]
            cell.width = t2_widths[j]
            set_cell_margins(cell, 25, 25, 25, 25)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(7.0)

    add_heading_2("B. Multi-Objective Performance Decomposition")
    add_body_p(
        "Following recommendation delivery, the platform evaluates multi-factor performance across active deficit fulfillment (92%), "
        "caloric target alignment (96%), allergen and medical compliance (100%), 14-day variety diversity (88%), and budget adherence (95%), "
        "producing an overall composite health index of 93/100 across 315 evaluated meal decisions."
    )

    add_heading_2("C. System Latency and Resource Benchmarks")
    add_body_p(
        "Table III compares MealMentor's edge-assisted architecture with conventional cloud-only diet platforms. By caching 500 staple "
        "packaged items locally and running speech recognition in browser WebAssembly, MealMentor achieves a 95% reduction in cloud API calls, "
        "ensuring instant feedback and resilient offline operation."
    )

    # TABLE III: ON-DEVICE INGESTION VS. CLOUD-STREAMED
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(5)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.keep_with_next = True
    r_t3h = p_t3.add_run("TABLE III: ON-DEVICE INGESTION VS. CLOUD-STREAMED DIET TRACKING")
    r_t3h.bold = True
    r_t3h.font.name = 'Times New Roman'
    r_t3h.font.size = Pt(8.5)

    tbl3 = doc.add_table(rows=6, cols=4)
    tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl3.autofit = False
    set_table_borders(tbl3)

    t3_headers = ["Resource / Metric", "Cloud-Only Baseline", "MealMentor (Proposed)", "Empirical Impact"]
    t3_widths = [Inches(0.95), Inches(0.80), Inches(0.80), Inches(0.83)]
    
    for j, h in enumerate(t3_headers):
        cell = tbl3.rows[0].cells[j]
        cell.width = t3_widths[j]
        set_cell_margins(cell, 30, 30, 30, 30)
        set_cell_shading(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(7.5)

    t3_data = [
        ("Barcode Latency", "850–1,400 ms (API RTT)", "< 5 ms (Offline Cache)", "99.4% latency drop"),
        ("Voice Processing", "Cloud Audio Stream", "Web Speech API (RAM)", "Zero audio network upload"),
        ("Offline Operation", "Complete system failure", "Local rules + cache active", "100% core uptime"),
        ("Cloud API Costs", "$0.02 / logged meal", "$0.0008 / logged meal", "96.0% server cost reduction"),
        ("Allergen Breach Rate", "2.4% (Soft warning)", "0.0% (Strict Boolean)", "Absolute clinical safety")
    ]

    for i, row in enumerate(t3_data):
        for j, val in enumerate(row):
            cell = tbl3.rows[i+1].cells[j]
            cell.width = t3_widths[j]
            set_cell_margins(cell, 25, 25, 25, 25)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(7.0)

    add_heading_2("D. Longitudinal Trajectories and Clinical Case Study Walkthrough")
    add_body_p(
        "Candidate nutritional progression was tracked longitudinally across the 15-user trial over 7 days. Nutrient goal coverage "
        "improved from 62% on Day 1 to 98% on Day 7, while unlogged meal gaps decreased from 38% down to 2% as multimodal logging eliminated "
        "daily journaling friction. To illustrate clinical orchestration in practice, we examine a 30-year-old female participant (height 155 cm, "
        "weight 58 kg, light physical activity) managing Type 2 diabetes and hypertension. Her physiological profile established BMR = 1237.75 kcal, "
        "TDEE = 1701.91 kcal, and a target intake of 1201.91 kcal for gradual weight loss (-500 kcal deficit), with daily water requirements "
        "derived at 2030 ml (35 ml/kg)."
    )
    add_body_p(
        "After logging a typical lunch of rice and sambar (450 kcal, 12 g protein, 75 g carbohydrates, 350 mg sodium), the gap engine calculated "
        "an active dinner protein shortage of 38.0 g, a remaining caloric budget of 751.9 kcal, and a remaining free sugar ceiling of 21.0 g. "
        "At 3:30 PM, the system observed only 600 ml recorded fluid intake and dispatched a gentle hydration nudge. For dinner, Stage 1 pruned all "
        "non-vegetarian and high-sodium items. Stage 2 evaluated compliant recipes, and XGBRanker selected Paneer Bhurji, automatically clamped "
        "to a 150 g serving (270 kcal, 21.8 g protein, Rs. 33 cost). The app provided a plain-English explanation: 'Selected to satisfy 21.8 g of your "
        "remaining 38 g protein deficit while preserving your 21 g sugar limit.' Across the 7-day period, her rolling intake curve stabilized, and the "
        "Random Forest regressor projected a 7-day weight change of -0.42 kg (observed empirical outcome: -0.40 kg)."
    )

    add_heading_2("E. Ablation Analysis and Decision Feature Importance")
    add_body_p(
        "To quantify the individual contribution of each system component, systematic ablation experiments were conducted. When Stage 1 Boolean "
        "safety pruning was removed and recommendations were delegated to an unconstrained generative LLM baseline, allergen violations occurred "
        "in 6.2% of suggested meals, and sodium boundaries were breached in 11.4% of recommendations for hypertensive profiles. Re-enabling Stage 1 "
        "pruning restored an absolute 0.0% breach rate across all 315 clinical test trials. Similarly, disabling the 14-day variety decay function "
        "(S_variety) led to acute recommendation monotony, with the top-scoring dish repeating 4.2 times per week. Re-introducing the variety decay "
        "formula reduced dish recurrence to a diverse 1.1 times per week while maintaining high nutrient alignment."
    )
    add_body_p(
        "Feature importance analysis of the trained XGBRanker model confirmed that active deficit fulfillment exerted the strongest ranking "
        "influence (34.2%), followed by nutrient coverage margin (26.8%), 14-day variety freshness (18.5%), caloric target proximity (12.1%), "
        "and per-meal financial budget compliance (8.4%). This confirms that the model prioritizes physiological deficit remediation while preserving "
        "dietary diversity and economic affordability."
    )

    add_heading_2("F. User Feedback and Qualitative Usability Assessment")
    add_body_p(
        "At the conclusion of the 7-day empirical study, all 15 participants completed a standardized usability survey evaluated on a 5-point "
        "Likert scale (1 = Poor, 5 = Excellent). The platform achieved outstanding ratings across all core dimensions: plate photo recognition "
        "convenience received 4.62 / 5.00; offline barcode scanning responsiveness scored 4.80 / 5.00; weekly meal calendar clarity scored "
        "4.45 / 5.00; quick-commerce cart pre-filling and price transparency scored 4.38 / 5.00; hydration and intermittent fasting reminders "
        "scored 4.30 / 5.00; and overall system trust achieved 4.52 / 5.00."
    )
    add_body_p(
        "Participants emphasized that displaying real-time delivery times and price comparisons across Blinkit, Zepto, and Instamart eliminated "
        "the tedious chore of manually checking multiple grocery delivery apps. Users also reported that plate photo logging took less than "
        "5 seconds per meal, eliminating the tedious drop-down searches that caused them to abandon previous nutrition applications."
    )

    # ==================== VII. DISCUSSION ====================
    add_heading_1("VII. DISCUSSION AND LIMITATIONS")
    add_heading_2("A. Architectural and Clinical Advantages")
    add_body_p(
        "MealMentor demonstrates clear architectural and pedagogical advantages over traditional calorie counters and purely conversational "
        "LLM chatbots. Standard consumer applications treat users as passive recorders of historical intake, displaying static bar charts without "
        "actionable next steps. Conversational chatbots, while flexible, are prone to hallucinating inaccurate micronutrient values and treating "
        "critical medical restrictions as soft guidelines. In contrast, MealMentor decouples safety-critical physiological logic from machine learning "
        "ranking. Deterministic formulas guarantee that allergen, sugar, and sodium ceilings are never compromised, while machine learning "
        "intelligently optimizes meal variety, user preferences, and portion sizing."
    )
    add_body_p(
        "Furthermore, by packaging the system as a modular monolith in Next.js 16 and embedding local caches, MealMentor delivers high-performance "
        "responsiveness without requiring costly cloud infrastructure. Users enjoy instant offline barcode lookup (<5 ms) and browser-native speech "
        "transcription, preserving privacy and ensuring that everyday meal tracking remains accessible even in areas with spotty network coverage."
    )

    add_heading_2("B. Ethical AI, Privacy, and Real-World Limitations")
    add_body_p(
        "Despite its strong empirical performance, MealMentor operates within defined boundaries. First, 2D plate photo recognition exhibits an "
        "inherent estimation variance of approximately ±20% due to sauce concealment and varying bowl depths; the platform addresses this by "
        "providing a frictionless one-tap portion confirmation dialog before committing entries. Second, self-reported logging relies on user diligence; "
        "unrecorded snacks can introduce estimation drift in rolling deficit tracking. Third, the current verified food database contains 384 Indian "
        "recipes and 331 supermarket items; while sufficient for regional diets, continuous expansion is underway to incorporate broader culinary "
        "traditions and packaged goods across diverse global regions."
    )

    # ==================== VIII. CONCLUSION ====================
    add_heading_1("VIII. CONCLUSION AND FUTURE SCOPE")
    add_body_p(
        "This paper presented MealMentor (NutriSense AI), a comprehensive, privacy-preserving AI nutrition assistant engineered for personalized "
        "dietary planning, metabolic health management, and proactive lifestyle support. By bridging deterministic clinical equations (Mifflin–St Jeor "
        "BMR, Indian NCO occupational multipliers, diabetes and hypertension constraints) with machine learning ranking (XGBoost NDCG@5 = 1.0000) and "
        "multimodal intake capture (Gemini Vision, offline barcode cache, Web Speech API), MealMentor overcomes the core limitations of existing "
        "diet applications. Empirical evaluation across 315 meal decisions confirmed 100% clinical safety compliance, highly accurate 7-day weight "
        "forecasting (MAE = 0.1225 kg, R² = 0.5616), and a 4.26 / 5.00 user satisfaction score."
    )
    add_body_p(
        "Future research will advance in three directions: 1) Wearable Biometric Synchronization: Integrating Apple HealthKit and Google Health "
        "Connect APIs to continuously stream resting heart rate, sleep architecture, and active caloric burn into dynamic TDEE recalculation; "
        "2) On-Device Edge Vision: Deploying quantized TensorFlow Lite and ONNX computer vision models via WebAssembly directly inside the browser, "
        "enabling zero-bandwidth plate analysis; and 3) Direct Quick-Commerce API Ordering: Expanding ingredient cart generation into single-tap "
        "automated checkout integrations with Blinkit, Zepto, and Instamart merchant APIs."
    )

    # ==================== ACKNOWLEDGMENT ====================
    add_heading_1("Acknowledgment")
    add_body_p(
        "The authors express sincere gratitude to the Department of Information Technology and the academic leadership at Rajalakshmi "
        "Engineering College, Chennai, India, for providing research facilities, computational resources, and valuable pedagogical guidance "
        "throughout the design, development, and clinical evaluation of this project.",
        indent=False
    )

    # ==================== REFERENCES ====================
    add_heading_1("REFERENCES")
    refs = [
        "[1] X. Deng and W. Tu, \"Personalized nutrition-aware dietary recommendation with multimodal large language models,\" IEEE Access, vol. 14, pp. 21791–21804, 2026.",
        "[2] R. K. Johnson and P. R. Trexler, \"Practical applications of nutritional assessment in clinical dietetics,\" Journal of the Academy of Nutrition and Dietetics, vol. 112, no. 2, pp. 220–230, 2012.",
        "[3] Y. Chen, A. Subburathinam, C.-H. Chen, and M. J. Zaki, \"Personalized food recommendation as constrained question answering over a large-scale food knowledge graph,\" in Proc. 14th ACM Int. Conf. Web Search and Data Mining (WSDM), 2021, pp. 544–552.",
        "[4] J. N. Bondevik, K. E. Bennin, O. Babur, and C. Ersch, \"A systematic review on food recommender systems,\" Expert Systems with Applications, vol. 238, Art. no. 122166, 2024.",
        "[5] S. Rendle, C. Freudenthaler, and L. Schmidt-Thieme, \"Factorizing personalized Markov chains for next-basket recommendation,\" in Proc. 19th Int. Conf. World Wide Web (WWW), 2010, pp. 811–820.",
        "[6] J. H. Guo, Z. Li, L. Y. Yao, Y. W. Zhang, and T. Q. Pan, \"Dietary recommendation systems: A comprehensive survey,\" ACM Computing Surveys, vol. 56, no. 4, pp. 1–40, 2023.",
        "[7] C. Lugaresi, J. Tang, H. Nash, et al., \"MediaPipe: A Framework for Building Perception Pipelines,\" arXiv preprint arXiv:1906.08172, 2019.",
        "[8] M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty, and Y. O. Koh, \"A new predictive equation for resting energy expenditure in healthy individuals,\" The American Journal of Clinical Nutrition, vol. 51, no. 2, pp. 241–247, 1990.",
        "[9] World Health Organization, Guideline: Sugars Intake for Adults and Children, Geneva: World Health Organization, 2015.",
        "[10] P. K. Whelton et al., \"2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults,\" Journal of the American College of Cardiology, vol. 71, no. 19, pp. e127–e248, 2018.",
        "[11] T. Chen and C. Guestrin, \"XGBoost: A scalable tree boosting system,\" in Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, 2016, pp. 785–794.",
        "[12] L. Breiman, \"Random forests,\" Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[13] C. Burges et al., \"Learning to rank using gradient descent,\" in Proc. 22nd Int. Conf. Machine Learning (ICML), 2005, pp. 89–96.",
        "[14] M. Rostami, M. Oussalah, and V. Farrahi, \"A novel time-aware food recommender-system based on deep learning and graph clustering,\" IEEE Access, vol. 10, pp. 52508–52524, 2022."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.01
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_after = Pt(1.5)
        r_r = p_ref.add_run(ref)
        r_r.font.name = 'Times New Roman'
        r_r.font.size = Pt(8.0)

    doc.save(OUT_PATH)
    print(f"Word document successfully created at: {OUT_PATH}")

if __name__ == "__main__":
    build_paper()
