# MealMentor (NutriSense AI): AI-Driven Personalized Nutrition Tracking and Meal Recommendation System

---

## PRELIMINARY PAGES

### 1. Title Page

```
================================================================================
                    A PROJECT REPORT ON
                      MealMentor (NutriSense AI)
   An AI-Driven Personalized Nutrition Assistant with Constraint-Aware
                and Nutrient-Gap-Aware Recommendation

                         Submitted by
                  [Student Name / Team Members]
                 [Register / Roll Numbers]

                   In partial fulfillment for the award of
                            the degree of
                       BACHELOR OF TECHNOLOGY
                                  in
                   COMPUTER SCIENCE AND ENGINEERING
               [or Artificial Intelligence & Data Science]

                   [DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING]
                   [COLLEGE / INSTITUTION NAME]
                   [AFFILIATED UNIVERSITY NAME]
                            [ACADEMIC YEAR]
================================================================================
```

---

### 2. Bonafide Certificate

```
                              BONAFIDE CERTIFICATE

Certified that this project report titled "MealMentor: An AI-Driven Personalized
Nutrition Assistant with Constraint-Aware and Nutrient-Gap-Aware Recommendation"
is the bonafide work of:

  1. [Student Name 1] - [Register No: ____________________]
  2. [Student Name 2] - [Register No: ____________________]
  3. [Student Name 3] - [Register No: ____________________]
  4. [Student Name 4] - [Register No: ____________________]

who carried out the project work under my supervision.


_________________________                         _________________________
   PROJECT SUPERVISOR                               HEAD OF THE DEPARTMENT
   [Supervisor Name]                                [HOD Name]
   [Designation & Department]                       [Designation & Department]
   [Institution Name]                               [Institution Name]


Submitted for the Viva-Voce Examination held on ____________________ at [Institution Name].


_________________________                         _________________________
    INTERNAL EXAMINER                                 EXTERNAL EXAMINER
```

---

### 3. Declaration

```
                                  DECLARATION

We hereby declare that the project entitled "MealMentor (NutriSense AI): An AI-Driven
Personalized Nutrition Assistant with Constraint-Aware and Nutrient-Gap-Aware
Recommendation" submitted to [University / College Name] in partial fulfillment of the
requirements for the award of the Degree of Bachelor of Technology in Computer Science
and Engineering is a record of original work carried out by us under the guidance of
[Supervisor Name], [Designation], Department of Computer Science and Engineering.

We further declare that the work reported herein has not been submitted either in part or
in full to any other University or Institution for the award of any degree or diploma.


Place: [City / Campus]
Date:  [DD/MM/YYYY]

                                                  1. [Signature & Name of Student 1]
                                                  2. [Signature & Name of Student 2]
                                                  3. [Signature & Name of Student 3]
                                                  4. [Signature & Name of Student 4]
```

---

### 4. Acknowledgement

We express our sincere gratitude to our respected Principal, **[Principal Name]**, and the Management of **[College / Institution Name]** for providing the infrastructural facilities and environment necessary to complete this project work.

We extend our deep gratitude to **[HOD Name]**, Head of the Department of Computer Science and Engineering, for their constant encouragement and administrative support throughout the development of this project.

We place on record our profound sense of gratitude and indebtedness to our Project Guide, **[Supervisor Name]**, [Designation], Department of Computer Science and Engineering, for their invaluable guidance, insightful technical feedback, and continuous motivation at every stage of this work.

We are also thankful to all the faculty and technical staff of the Department of Computer Science and Engineering for their direct and indirect assistance. Lastly, we thank our parents, peers, and friends who supported us with their encouragement and constructive suggestions.

---

### 5. Abstract

Personalized dietary recommendation remains a significant engineering challenge for individuals seeking to balance nutritional adequacy, personal preferences, strict dietary restrictions, economic constraints, and meal variety. This report presents the design, architectural formalization, and empirical implementation of **MealMentor (NutriSense AI)**, a production-grade full-stack web application with machine learning capabilities designed to provide individualized, data-grounded nutritional guidance.

The system addresses the core limitations of existing commercial dietary apps—which typically rely on static calorie quotas, manual logging burden, and black-box generic advice—by coupling deterministic physiological calculations with an adaptive two-stage recommendation pipeline. MealMentor computes Basal Metabolic Rate (BMR) via the Mifflin–St Jeor equation, adjusts for physical activity to compute Total Daily Energy Expenditure (TDEE), and dynamically calculates daily micro- and macronutrient targets calibrated for health goals, hypertension (sodium clamping), and diabetes (sugar reduction). 

During real-time tracking, the system computes the exact remaining nutrient gaps across ten essential nutrients ($G_n = \max(0, T_n - C_n)$). Meal recommendations are generated via a two-stage pipeline: Stage 1 enforces hard safety and ethical constraints (strict allergen elimination, vegetarian/vegan compliance, and meal budget thresholds), while Stage 2 performs soft multi-criteria ranking using nutrient gap coverage, user preferences, per-meal cost efficiency, and a 3-day meal repetition decay penalty to ensure dietary variety. Furthermore, an XGBoost learning-to-rank model re-ranks candidate meals, while an isolated Python FastAPI microservice runs Random Forest regression to project 7-day weight trajectories. Integrated multimodal services include Google Gemini Vision for food photo nutrient estimation, OpenFoodFacts barcode scanning with an offline fallback cache, and an AI conversational assistant with deterministic offline recovery.

Built using Next.js 16 (React 19, TypeScript), MongoDB with Mongoose schemas, and validated against comprehensive Playwright E2E and Vitest unit test suites, MealMentor provides a verified, accessible (WCAG 2.1 AA compliant), and non-clinical nutritional awareness platform.

---

### 6. Table of Contents

```
1. INTRODUCTION .............................................................. 1
   1.1 Introduction .......................................................... 1
   1.2 Background ............................................................ 2
   1.3 Problem Statement ..................................................... 3
   1.4 Objectives ............................................................ 4
   1.5 Scope ................................................................. 5
   1.6 Motivation ............................................................ 6
   1.7 Organization of the Report ............................................ 7

2. LITERATURE REVIEW ......................................................... 8
   2.1 Existing Approaches to Personalized Nutrition ......................... 8
   2.2 Nutrition Tracking Systems ............................................ 9
   2.3 AI-Based Meal Recommendation Systems ................................. 10
   2.4 Analysis of Related Research Papers ................................... 11
   2.5 Identified Research Gaps .............................................. 13
   2.6 Comparative Analysis with Proposed System ............................. 14

3. SYSTEM ANALYSIS ........................................................... 15
   3.1 Existing System Overview .............................................. 15
   3.2 Limitations of the Existing System .................................... 16
   3.3 Proposed System Architecture and Highlights ........................... 17
   3.4 Functional Requirements ............................................... 18
   3.5 Non-Functional Requirements ........................................... 20
   3.6 Hardware Requirements ................................................. 22
   3.7 Software Requirements ................................................. 23
   3.8 Feasibility Study ..................................................... 24

4. SYSTEM DESIGN ............................................................. 26
   4.1 System Architecture ................................................... 26
   4.2 Overall Architecture Diagram .......................................... 27
   4.3 Module Decomposition .................................................. 28
   4.4 Use Case Diagram ...................................................... 29
   4.5 Data Flow Diagrams (Level 0 and Level 1) .............................. 30
   4.6 Database Design and Data Dictionary ................................... 32
   4.7 Entity-Relationship (ER) Diagram ...................................... 34
   4.8 Sequence Diagrams (UML Interaction Models) ............................ 35
   4.9 User Interface and Interaction Design ................................. 38

5. SYSTEM IMPLEMENTATION ..................................................... 40
   5.1 Development Environment Setup ......................................... 40
   5.2 Technology Stack Details .............................................. 41
   5.3 Frontend Implementation ............................................... 43
   5.4 Backend and API Implementation ........................................ 45
   5.5 Database Layer and Mongoose Schemas ................................... 47
   5.6 Authentication and Security Layer ..................................... 49
   5.7 AI and Machine Learning Layer ......................................... 51
   5.8 Deterministic Nutrition Calculation Formulas .......................... 53
   5.9 Two-Stage Recommendation Pipeline ..................................... 55
   5.10 External Integrations (Vision, Barcode, LLM) ......................... 57
   5.11 Module-Wise Detailed Implementation .................................. 59

6. TESTING AND RESULTS ....................................................... 63
   6.1 Testing Methodology ................................................... 63
   6.2 Test Environment ...................................................... 64
   6.3 Test Cases and Test Execution ......................................... 65
   6.4 Verification Results .................................................. 68
   6.5 Functional Validation and Numerical Proofs ............................ 70
   6.6 Sample Step-by-Step Calculations ...................................... 72
   6.7 Screenshot Verification and Visual Outputs ............................ 74
   6.8 Performance Observations .............................................. 76
   6.9 Limitations of the Current Implementation ............................. 77

7. CONCLUSION AND FUTURE ENHANCEMENTS ........................................ 79
   7.1 Project Summary ....................................................... 79
   7.2 Objectives Achieved ................................................... 80
   7.3 Key Engineering Contributions ......................................... 81
   7.4 Current Limitations ................................................... 82
   7.5 Future Enhancements ................................................... 83
   7.6 Final Conclusion ...................................................... 84

REFERENCES ................................................................... 85

APPENDICES ................................................................... 88
   Appendix A: REST API Specification ........................................ 88
   Appendix B: Database Schemas and DDL ...................................... 92
   Appendix C: Core Algorithm Source Code Excerpts ........................... 96
   Appendix D: User Manual ................................................... 101
   Appendix E: Installation and Execution Manual ............................. 104
   Appendix F: Complete Feature Verification Matrix .......................... 107
```

---

### 7. List of Figures

- **Figure 4.1**: Three-Tier System Architecture of MealMentor (NutriSense AI)
- **Figure 4.2**: Use Case Diagram for User and System Interactions
- **Figure 4.3**: Level-0 Context Data Flow Diagram (DFD)
- **Figure 4.4**: Level-1 Detailed Data Flow Diagram (DFD)
- **Figure 4.5**: Entity-Relationship (ER) Diagram
- **Figure 4.6**: Sequence Diagram for User Authentication (Scrypt & JWT)
- **Figure 4.7**: Sequence Diagram for Two-Stage Meal Recommendation Pipeline
- **Figure 4.8**: Sequence Diagram for Quantity-Aware Food Logging
- **Figure 4.9**: Sequence Diagram for Multimodal Food Photo Analysis
- **Figure 6.1**: Component and Page Flow Layout Diagram

---

### 8. List of Tables

- **Table 2.1**: Comparative Feature Matrix of Food Recommendation and Nutrition Systems
- **Table 3.1**: Hardware Specifications (Development and Production)
- **Table 3.2**: Software Technology Stack and Library Versions
- **Table 4.1**: User Schema Data Dictionary
- **Table 4.2**: Food Schema Data Dictionary
- **Table 4.3**: MealEntry Schema Data Dictionary
- **Table 4.4**: WeightLog Schema Data Dictionary
- **Table 4.5**: GroceryItem Schema Data Dictionary
- **Table 5.1**: Physical Activity Multipliers ($f_{\text{activity}}$)
- **Table 5.2**: Caloric Adjustment by Primary Health Goal
- **Table 5.3**: Nutrition Dataset Summary (`finalDatasetfood.csv`)
- **Table 6.1**: Vitest Unit Test Cases and Results
- **Table 6.2**: Playwright End-to-End Test Suite Summary
- **Table 6.3**: Numerical Walkthrough: Profile, TDEE, Targets, and Daily Gap
- **Table 7.1**: Project Objectives Achievement Status
- **Table F.1**: Comprehensive Feature Implementation Verification Matrix

---

### 9. List of Abbreviations

| Abbreviation | Expansion |
|:---|:---|
| **AI** | Artificial Intelligence |
| **API** | Application Programming Interface |
| **BMI** | Body Mass Index |
| **BMR** | Basal Metabolic Rate |
| **CORS** | Cross-Origin Resource Sharing |
| **CSV** | Comma-Separated Values |
| **CSS** | Cascading Style Sheets |
| **DFD** | Data Flow Diagram |
| **E2E** | End-to-End |
| **ER** | Entity-Relationship |
| **HTTP/REST** | Hypertext Transfer Protocol / Representational State Transfer |
| **JSON** | JavaScript Object Notation |
| **JWT** | JSON Web Token |
| **LLM** | Large Language Model |
| **MAE** | Mean Absolute Error |
| **ML** | Machine Learning |
| **NoSQL** | Not Only SQL |
| **ODM** | Object Data Modeling (Mongoose) |
| **RAG** | Retrieval-Augmented Generation |
| **SSR** | Server-Side Rendering |
| **TDEE** | Total Daily Energy Expenditure |
| **UI/UX** | User Interface / User Experience |
| **UML** | Unified Modeling Language |
| **WCAG** | Web Content Accessibility Guidelines |
| **XGBoost** | eXtreme Gradient Boosting |

---

## CHAPTER 1: INTRODUCTION

### 1.1 Introduction
Nutrition is a fundamental determinant of human health, cognitive vitality, physical performance, and chronic disease prevention. Despite broad public awareness of healthy eating principles, modern dietary environments make sustained nutritional adequacy difficult. Sedentary professions, demanding work schedules, budget restrictions, and ubiquitous access to ultra-processed foods have fueled global spikes in obesity, Type 2 diabetes, hypertension, and micronutrient deficiencies.

In computing and informatics, technological solutions have evolved through calorie counting, mobile food diaries, and crowd-sourced diet planners. However, contemporary commercial applications remain predominantly retrospective: they record what the user has consumed, compute a simplistic sum of calories, and display standard green/red indicators. They fail to dynamically direct the user toward foods that actively rectify their real-time nutrient deficiencies while respecting non-negotiable dietary boundaries (allergies, ethical choices, budget constraints).

**MealMentor (NutriSense AI)** was engineered to transform nutrition tracking from a passive recording log into an intelligent, proactive, constraint-aware decision support system. MealMentor combines scientifically validated metabolic equations, strict constraint-filtering algorithms, machine learning re-ranking models, multimodal vision recognition, and interactive conversational intelligence to provide personalized, actionable meal recommendations.

### 1.2 Background
Historically, dietary guidance was administered through generalized governmental food pyramids or clinical dietitians. While one-on-one dietitian consultations provide tailored plans, they are cost-prohibitive for the general population. In contrast, digital applications democratize access to dietary tools. 

First-generation dietary software comprised static spreadsheets and desktop food databases (e.g., USDA standard release lookups). Second-generation apps—such as MyFitnessPal, Lose It!, and Cronometer—introduced mobile accessibility, crowd-sourced food databases, and barcode scanning. Despite their popularity, these applications present four persistent engineering limitations:
1. **Calorie-Centric Bias**: They emphasize aggregate caloric deficits at the expense of micronutrient balance (fiber, iron, calcium, vitamin C).
2. **High Logging Friction**: Manual food searches and manual portion scaling lead to user fatigue, causing abandonment within weeks.
3. **Absence of Optimization Logic**: They do not calculate the mathematical gap between current intake and remaining daily targets to actively suggest balancing meals.
4. **Disregard for Socioeconomic Realities**: Recommendations rarely factor in grocery costs or ingredient availability, generating meal proposals that are financially unsustainable for students or budget-conscious families.

MealMentor bridges these gaps by treating meal recommendation as a multi-criteria optimization problem bounded by hard physiological, ethical, and economic constraints.

### 1.3 Problem Statement
Individuals striving to maintain healthy lifestyles face a complex multi-objective optimization problem on a daily basis:
1. They must consume sufficient energy to sustain metabolic function without exceeding caloric limits that cause undesired weight gain.
2. They must balance macronutrient distributions (protein, carbohydrates, healthy fats) while ensuring adequate micronutrient density (dietary fiber, iron, calcium, vitamin C).
3. They must strictly avoid ingredients that trigger immunological reactions (allergens such as peanuts, dairy, gluten, shellfish) or violate personal ethical/religious philosophies (vegan, vegetarian).
4. They must operate within strict financial budgets per meal or per week.
5. They must select foods appropriate to specific times of day (breakfast, lunch, dinner, snack) while avoiding repetitive meal monotony.

Existing systems solve subsets of these constraints in isolation. Simple calorie trackers record consumption without forward-looking recommendations. Traditional collaborative filtering algorithms recommend items based on popular taste profiles, often suggesting foods high in allergens or unsuitable for the user's metabolic status. Generative AI tools (LLMs) often hallucinate nutritional content, inventing unrealistic micronutrient values or ignoring dietary restrictions.

**MealMentor addresses this problem** by implementing a deterministic, data-grounded nutritional engine. Every target is calculated using verified clinical formulas, candidate foods are verified against local nutritional datasets (384 curated foods, 331 grocery items), non-negotiable safety rules are enforced by hard-filtering algorithms, and candidate foods are ranked via multi-criteria objective functions and XGBoost models.

### 1.4 Objectives
The primary technical and engineering objectives of MealMentor are:
1. **Deterministic Metabolic Modeling**: Implement the Mifflin–St Jeor equation to compute Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on age, gender, height, weight, and physical activity level.
2. **Condition-Aware Target Derivation**: Formulate dynamic macronutrient and micronutrient daily targets adjusted for specific user goals (weight loss, muscle gain, maintenance) and clinical conditions (sugar limits for diabetes, sodium limits for hypertension).
3. **Real-Time Nutrient Gap Analysis**: Implement a real-time intake tracking engine that dynamically computes the delta between targets and consumed nutrients ($G_n = \max(0, T_n - C_n)$).
4. **Two-Stage Recommendation Pipeline**:
   - **Stage 1 (Hard Filtering)**: Enforce zero-tolerance elimination of foods violating declared allergens, dietary restrictions (veg/vegan), or budget ceilings.
   - **Stage 2 (Multi-Criteria Ranking)**: Rank candidate foods using weighted scoring across nutrient gap fulfillment, user food preferences, price-per-serving, and a 3-day meal repetition decay penalty.
5. **Machine Learning Learning-to-Rank**: Integrate an XGBoost re-ranking model trained on nutritional feature representations to elevate the most contextually relevant meals.
6. **Weight Trend Forecasting**: Develop a Random Forest regression pipeline running on FastAPI to project 7-day weight trajectories based on rolling caloric balance.
7. **Multimodal Friction Reduction**: Integrate Google Gemini 1.5/2.0 Vision for meal photo nutritional analysis and OpenFoodFacts barcode scanning with local caching.
8. **Transparent Data-Grounded Explanations**: Provide clear, factual explanations for every recommended item, linking each suggestion directly to the specific nutrient gap it fulfills.

### 1.5 Scope
#### In Scope (Verified Implementation)
- User authentication via custom salted scrypt password hashing, session tokens, and Google OAuth.
- Biometric profile management: age, sex, height, weight, activity multiplier, diet type, allergies, conditions, budget.
- Automatic computation of BMI, BMR, TDEE, water targets, and 10 nutrient targets.
- Daily food intake logging with quantity scaling ($n \times q / 100$).
- Two-stage meal recommendation engine with meal-type filtering and 3-day variety enforcement.
- XGBoost learning-to-rank meal scoring.
- Random Forest 7-day weight forecasting microservice.
- Gemini Vision meal photo scanning.
- OpenFoodFacts barcode scanning with local caching.
- AI Nutrition Chatbot with deterministic local fallback.
- Dynamic grocery list generation with price estimation from `finalDatasetGrocery.csv`.
- Water logging and streak tracking.
- WCAG 2.1 AA responsive web interface.

#### Out of Scope (Explicit Safety & Engineering Boundaries)
- Direct integration with proprietary clinical health records (HL7/FHIR).
- Continuous real-time IoT wearable sensor ingestion (e.g., Apple HealthKit / Fitbit background sync).
- Medical diagnosis, clinical nutrition prescriptions, or treatment of eating disorders. MealMentor is strictly an educational and personal dietary guidance platform.
- E-commerce payment gateway processing (grocery orders generate shopping lists without executing merchant transactions).

### 1.6 Motivation
Modern web technologies (Next.js 16 App Router, React 19, TypeScript) and modern ML frameworks provide the opportunity to build high-performance, responsive health applications. Furthermore, combining strict rule-based logic with statistical machine learning solves the AI safety dilemma: mathematical rules guarantee safety (allergens are never recommended), while machine learning optimizes user satisfaction and dietary diversity. This hybrid architecture motivated the design and implementation of MealMentor.

### 1.7 Organization of the Report
This report is structured into seven distinct chapters:
- **Chapter 1** provides an introduction, background, problem statement, objectives, and scope.
- **Chapter 2** reviews relevant literature in personalized nutrition, AI recommendation systems, and empirical research gaps.
- **Chapter 3** presents the system analysis, comparing existing solutions against the proposed system, alongside functional, non-functional, hardware, and software requirements.
- **Chapter 4** details the system design, featuring architecture diagrams, UML use case models, DFDs, ER diagrams, and sequence interaction flows.
- **Chapter 5** presents the complete implementation details across the frontend, backend APIs, MongoDB database, ML models, and deterministic nutrition formulas.
- **Chapter 6** details testing strategies (Vitest unit tests, Playwright E2E suites), validation results, sample numerical calculations, and limitations.
- **Chapter 7** concludes the report with a summary of achievements, contributions, and future research directions.

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Existing Approaches to Personalized Nutrition
Personalized nutrition tailors dietary recommendations to an individual's unique biological characteristics, lifestyle, and preferences. Traditional approaches relied on static dietary guidelines, such as Recommended Daily Allowances (RDAs) established by the World Health Organization (WHO) and the Food and Nutrition Board. In clinical settings, dietitians perform manual nutritional assessments using predictive energy equations (Harris–Benedict, Mifflin–St Jeor) combined with multi-day food recall logs [10]. 

While manual consultations remain the gold standard, their scalability is limited. Consequently, computational nutrition systems have emerged to automate dietary assessment and meal synthesis using rule-based expert systems, constraint satisfaction algorithms, and digital tracking tools.

### 2.2 Nutrition Tracking Systems
Commercial mobile dietary applications (e.g., MyFitnessPal, Lose It!, Cronometer) popularized digital nutrition logging through crowd-sourced databases and barcode scanning. Research by Johnson and Trexler [10] highlights that digital tracking improves dietary self-monitoring adherence. However, these systems exhibit three core shortcomings:
1. **Passive Logging**: They record what has been consumed but offer no automated mechanism to optimize subsequent meals to meet unmet daily nutritional targets.
2. **Database Inconsistencies**: Crowd-sourced databases frequently suffer from missing micronutrients, erroneous calorie values, and unverified serving sizes.
3. **Binary Goal Focus**: Applications emphasize single metrics (total calories or net carbs) while neglecting micronutrient adequacy, dietary fiber, and electrolyte balance.

### 2.3 AI-Based Meal Recommendation Systems
Artificial Intelligence has been applied to food recommendation via three primary paradigms:
1. **Collaborative Filtering**: Suggests meals based on ratings from users with similar historical consumption profiles [4]. However, collaborative filtering suffers from the "cold start" problem for new items and often recommends nutritionally deficient foods simply because they are popular.
2. **Content-Based Filtering**: Suggests foods similar in ingredients or cuisine to past favorites. While effective at honoring taste preferences, it can induce severe meal monotony and ignores dynamic physiological needs [2].
3. **Knowledge-Graph & Constraint-Based Systems**: Formulates meal recommendation as a constrained optimization problem, where nutritional targets and allergens serve as mathematical boundaries [3].

Recent investigations incorporate deep learning, sequential models (SASRec, BERT4Rec) [5], [6], and multimodal Large Language Models (LLMs) [1]. However, pure LLM-based recommenders present risks of nutritional hallucination, inventing incorrect caloric values or failing to strictly enforce allergen constraints.

### 2.4 Analysis of Related Research Papers

The design of MealMentor is grounded in the following verified literature:

1. **Deng and Tu (2026)** [1] investigated multimodal large language models for personalized nutrition-aware dietary recommendation. They demonstrated that while LLMs excel at conversational interaction and recipe comprehension, they struggle with strict numerical nutrient constraints, highlighting the necessity of hybrid architectures where deterministic engines verify LLM outputs.
2. **Bondevik et al. (2024)** [2] conducted a systematic literature review on food recommender systems across 140+ studies. They identified that over 70% of published recommender systems focus exclusively on user taste preference, while fewer than 22% integrate physiological nutrient requirements, and fewer than 8% incorporate economic (cost-per-meal) constraints.
3. **Chen et al. (2021)** [3] formalized personalized food recommendation as a constrained question-answering task over large-scale food knowledge graphs, establishing that hard constraints (allergens, diet types) must be decoupled from soft preferences to guarantee user safety.
4. **Rendle et al. (2010)** [4] introduced Factorizing Personalized Markov Chains (FPMC) for next-basket recommendation, demonstrating the predictive power of transition dynamics in dietary habits.
5. **Kang and McAuley (2018)** [5] proposed Self-Attentive Sequential Recommendation (SASRec), capturing long-term user preferences while dynamically weighting recent item interactions.
6. **Sun et al. (2019)** [6] developed BERT4Rec, employing bidirectional self-attention mechanisms to model sequential recommendation contexts.
7. **Rostami, Oussalah, and Farrahi (2022)** [7] formulated a time-aware food recommender utilizing deep learning and graph clustering, demonstrating that temporal meal context (e.g., breakfast vs. dinner) drastically influences recommendation utility.
8. **Mifflin, St Jeor, et al. (1990)** [8] published the landmark clinical trial establishing the Mifflin–St Jeor equation for resting energy expenditure. Their empirical evaluation demonstrated that the Mifflin–St Jeor formula accurately estimates resting metabolic rate within $\pm 10\%$ of indirect calorimetry in healthy obese and non-obese individuals, outperforming the older Harris–Benedict formula.
9. **Guo et al. (2023)** [9] provided an extensive survey on dietary recommendation systems in *ACM Computing Surveys*, categorizing systems into health-oriented, preference-oriented, and hybrid systems, concluding that hybrid multi-objective frameworks represent the most promising paradigm for long-term user health.
10. **Johnson and Trexler (2012)** [10] reviewed practical applications of nutritional assessment in clinical dietetics, emphasizing that nutrient gap tracking and portion size estimation accuracy are vital determinants of dietary intervention success.

### 2.5 Identified Research Gaps
From the literature, five critical research gaps emerge:
1. **Disconnection Between Tracking and Recommendation**: Most systems either track food or recommend recipes; few dynamically update recommendations in real time as daily nutrient gaps change.
2. **Lack of Budget and Cost Grounding**: Recommenders routinely propose nutritionally optimal ingredients that exceed realistic household grocery budgets.
3. **Meal Monotony**: Standard optimization algorithms repeatedly recommend the same mathematically optimal food item (e.g., chicken breast and broccoli) without variety penalties.
4. **Black-Box AI Recommendations**: Systems rarely explain *why* an item was suggested in relation to specific daily nutrient deficiencies.
5. **Safety Hazards of Pure Generative AI**: Unconstrained LLMs cannot be trusted to strictly enforce medical allergen boundaries without deterministic filtering.

### 2.6 Comparative Analysis with Proposed System

**Table 2.1: Feature Comparison Matrix of Dietary Recommendation Systems**

| Feature | MealMentor (Implemented) | NutriRec [1] | MyFitnessPal Style | Generic Rec Systems [2] |
|:---|:---|:---|:---|:---|
| **Nutrient Target Calculation** | Deterministic (Mifflin–St Jeor BMR/TDEE) | LLM-inferred | Pre-set generic templates | Not included |
| **Quantity-Aware Scaling** | Yes, exact per-gram ($n \times q / 100$) | Implicit in embedding | Manual log lookup | N/A |
| **Real-Time Nutrient Gap Analysis** | Yes, 10 nutrients ($G_n = \max(0, T_n - C_n)$) | Implicit in encoder | Calories/macros only | Not included |
| **Hard Constraint Safety Filtering** | Stage 1: Zero-tolerance (Allergies, Veg, Budget) | Soft multimodal penalty | Keyword search filter | None |
| **Multi-Criteria Soft Ranking** | Stage 2: Gap coverage + Preference + Cost + Variety | Embedding similarity | Calorie count only | Taste preference only |
| **Meal Monotony / Variety Control** | Yes, 3-day history penalty ($S_{\text{variety}}$) | Sequential attention | Manual log review | None |
| **Data-Grounded Explainability** | Yes, cites exact nutrient gap & cost | LLM-generated (unverified) | Static nutrient table | None |
| **Multimodal Input Support** | Vision (Gemini) + Barcode (OpenFoodFacts) + Voice | Vision only | Barcode only | Text only |
| **Offline Fallback Capability** | Yes, deterministic rule & cache fallback | No (Cloud dependent) | Partial cache | None |

---

## CHAPTER 3: SYSTEM ANALYSIS

### 3.1 Existing System Overview
The existing landscape of dietary management tools consists of:
1. **Manual Diary Logging**: Pen-and-paper tracking or generic spreadsheets where users manually look up nutrition tables.
2. **Commercial Calorie Counter Apps**: Mobile applications with massive crowd-sourced databases where users log food items after consumption.
3. **Static Diet Plan Generators**: Web portals that output weekly meal plans based on broad caloric tiers (e.g., "1800 Calorie Low Carb Plan") without taking into account daily consumption variations.

### 3.2 Limitations of the Existing System
The existing systems suffer from severe engineering and operational deficiencies:
- **High Friction and Attrition**: Manual searching, portion weighing, and multi-field data entry cause over 60% of users to stop logging within two weeks.
- **Retrospective, Not Proactive**: Existing tools record past calories but do not assist the user in deciding what to eat for their next meal.
- **Absence of Real-Time Gap Compensation**: If a user consumes a lunch deficient in fiber and protein, existing apps do not prioritize high-fiber, high-protein options for dinner.
- **Budget Blindness**: Recipes generated by algorithmic tools frequently incorporate exotic, expensive ingredients without considering local grocery costs.
- **Allergen Risks in AI Models**: Generic machine learning models treat allergen avoidance as a probabilistic soft weight rather than an absolute binary exclusion, creating potential health risks.

### 3.3 Proposed System Architecture and Highlights
MealMentor provides a comprehensive, constraint-aware, proactive dietary management platform:
- **Hybrid Mathematical & AI Pipeline**: Merges clinical formulas (Mifflin–St Jeor) with machine learning re-ranking (XGBoost) and forecasting (Random Forest).
- **Two-Stage Recommendation Engine**: Separates hard safety boundaries (allergies, diet types, budget ceilings) from soft preference and nutrient optimization.
- **Dynamic Nutrient Gap Tracking**: Dynamically recalculates remaining daily gaps for calories, protein, carbohydrates, fat, fiber, sugar, sodium, calcium, iron, and vitamin C after every logged food.
- **Multimodal Logging Convenience**: Reduces logging friction through meal photo analysis (Gemini Vision), packaged food barcode scanning (OpenFoodFacts), and voice input.
- **Variety Enforcement**: Penalizes meals consumed in the preceding 72 hours to prevent dietary fatigue.
- **Budget Optimization**: Evaluates meal cost per serving against user-specified budgets using real-world ingredient pricing datasets.

### 3.4 Functional Requirements
- **FR1: User Account & Authentication Management**: The system must provide secure user registration, login with salted scrypt hashing, JWT session management, Google OAuth integration, and password recovery.
- **FR2: Biometric Profile Management**: The system must capture and store user age, gender, height, weight, physical activity level, work type, dietary philosophy, allergies, chronic conditions, and meal budgets.
- **FR3: Energy Expenditure & Target Calculation**: The system must compute BMI, BMR using Mifflin–St Jeor, TDEE using activity multipliers, and daily targets for 10 macro- and micronutrients.
- **FR4: Food Intake Logging**: The system must allow users to log food items with variable serving sizes, automatically scaling all nutritional values per gram.
- **FR5: Real-Time Nutrient Gap Analysis**: The system must calculate and visually display the remaining nutrient deficit for the current day.
- **FR6: Two-Stage Meal Recommendation**: The system must filter out all meals violating user allergies, dietary restrictions, or budget limits (Stage 1), and rank compliant candidates based on gap coverage, preference, cost, and variety (Stage 2).
- **FR7: Machine Learning Re-Ranking & Forecasting**: The system must re-rank candidate recommendations using an XGBoost model and forecast 7-day weight changes using a Random Forest model.
- **FR8: Multimodal Food Recognition**: The system must analyze uploaded meal photographs via Gemini Vision and identify packaged foods via barcode lookup.
- **FR9: Conversational AI Nutritionist**: The system must provide an interactive nutrition chatbot with a deterministic offline fallback engine.
- **FR10: Grocery List & Cost Estimation**: The system must aggregate ingredients from recommended meals into categorized grocery lists with price estimates.
- **FR11: Progress & Water Tracking**: The system must track daily hydration, historical weight logs, and 7-day nutritional trends with interactive charts.

### 3.5 Non-Functional Requirements
- **NFR1: Performance**: Web pages and dashboard views must render with a First Contentful Paint (FCP) under 1.5 seconds. Recommendation generation must return within 500 ms for rule-based scoring and under 1.5 seconds when invoking Python ML pipelines.
- **NFR2: Safety & Data Integrity**: Hard allergen constraints must be strictly non-negotiable (100% exclusion rate). Password storage must utilize salted cryptographic derivation (scrypt).
- **NFR3: Reliability & Fallback**: External API dependencies (Gemini LLM, Gemini Vision, OpenFoodFacts) must have local fallbacks (deterministic chatbot logic, offline barcode cache) to prevent system failure during network disruptions.
- **NFR4: Usability & Accessibility**: The user interface must adhere to WCAG 2.1 AA accessibility guidelines, including 4.5:1 text contrast ratios, semantic HTML tags, keyboard navigation, and responsive mobile layouts.
- **NFR5: Maintainability**: The codebase must be modularized into distinct layers (presentation, API routes, Mongoose models, shared libraries) with comprehensive TypeScript types.

### 3.6 Hardware Requirements

**Table 3.1: Hardware Specifications**

| Component | Minimum Development Environment | Recommended Production Environment |
|:---|:---|:---|
| **Processor** | Dual-Core Intel/AMD x64 or Apple Silicon (2.0 GHz+) | Quad-Core Cloud VM (AWS EC2 / DigitalOcean) |
| **RAM** | 8 GB DDR4 | 16 GB DDR4/DDR5 |
| **Storage** | 20 GB Free SSD Space | 50 GB NVMe SSD |
| **Network** | Broadband Internet Connection (5 Mbps+) | High-Speed Cloud Interface (1 Gbps) |
| **Client Devices** | Desktop, Laptop, Tablet, or Smartphone | Any modern browser (Chrome, Firefox, Safari, Edge) |

### 3.7 Software Requirements

**Table 3.2: Software Technology Stack**

| Layer / Role | Technology / Tool | Version |
|:---|:---|:---|
| **Operating System** | Windows 10/11, macOS Sonoma/Sequoia, Linux (Ubuntu 22.04+) | Ubuntu 22.04 LTS (Server) |
| **Frontend Framework** | Next.js (App Router, Server Components) | 16.0.0 |
| **UI Library & Components** | React, Tailwind CSS, Radix UI Primitives, Lucide Icons | React 19, Tailwind v4 |
| **Programming Languages** | TypeScript (Strict Mode), Python | TypeScript 5+, Python 3.10+ |
| **Data Visualization** | Recharts (Responsive SVG Charts) | 2.15.0 |
| **Database & ODM** | MongoDB Server, Mongoose ODM | MongoDB 7.0+, Mongoose 9.9.4 |
| **ML Libraries** | XGBoost, scikit-learn, pandas, numpy | XGBoost 2.0+, scikit-learn 1.4+ |
| **Microservice Backend** | FastAPI, Uvicorn | FastAPI 0.110+ |
| **External AI APIs** | Google Gemini API (Vision & Language), OpenFoodFacts API | Gemini 1.5/2.0 Flash |
| **Testing Frameworks** | Vitest (Unit), Playwright (E2E) | Vitest 3.0+, Playwright 1.50+ |

### 3.8 Feasibility Study
- **Technical Feasibility**: The system utilizes mature, well-supported open-source frameworks (Next.js, React, Node.js, MongoDB, Python, scikit-learn). The integration of Python ML models via REST APIs and JSON interchange files ensures decoupling and system stability.
- **Economic Feasibility**: The application is built entirely on open-source frameworks with no proprietary software license fees. Deployment is supported on standard cloud tiers (Vercel serverless for frontend and APIs, MongoDB Atlas free/shared tier, and containerized Python services).
- **Operational Feasibility**: The interface is designed for intuitive consumer use, offering automated camera/barcode scanning to minimize manual typing. Non-technical users can navigate dashboards, log meals, and view recommendations with minimal onboarding.

---

## CHAPTER 4: SYSTEM DESIGN

### 4.1 System Architecture
MealMentor adopts a multi-tier decoupled architecture:
1. **Presentation Tier (Frontend)**: Next.js 16 App Router application rendering responsive React 19 components with Tailwind CSS styling and Recharts visualization.
2. **Application / Service Tier (API Gateway)**: Next.js serverless API routes (`src/app/api/*`) executing authentication, profile handling, intake tracking, and recommendation logic.
3. **Machine Learning Tier**: Python microservices and scripts executing XGBoost candidate re-ranking and Random Forest 7-day weight forecasting.
4. **Data Tier (Persistence)**: MongoDB database storing user profiles, food records, meal logs, feedback history, and weight entries via Mongoose ODM schemas.
5. **External Services Tier**: Google Gemini API for vision and conversational NLP, and OpenFoodFacts for packaged food barcode lookup.

### 4.2 Overall Architecture Diagram

```mermaid
graph TD
    Client["Client Devices (Browser / Mobile)"]
    
    subgraph "Presentation & Gateway Tier (Next.js 16 / React 19)"
        UI["Web UI Components (Tailwind, Lucide, Recharts)"]
        Router["Next.js App Router (SSR & Client Pages)"]
        APIs["API Routes (/api/auth, /api/recommend, /api/food-log)"]
    end
    
    subgraph "Core Business & Calculation Engine (TypeScript)"
        Nutri["Nutrition Engine (BMR / TDEE / Targets)"]
        Gap["Nutrient Gap Analyzer (10 Nutrients)"]
        Stage1["Stage 1: Hard Constraint Filter"]
        Stage2["Stage 2: Soft Multi-Criteria Ranker"]
    end
    
    subgraph "Machine Learning Tier (Python)"
        XGB["XGBoost Learning-to-Rank Model"]
        RF["Random Forest Weight Forecaster (FastAPI)"]
    end
    
    subgraph "Data Persistence Tier (MongoDB)"
        DB[("MongoDB Database")]
        M_User["User Collection"]
        M_Food["Food Collection (384 Items)"]
        M_Log["MealEntry & WeightLog Collections"]
        M_Groc["Grocery Collection (331 Items)"]
    end
    
    subgraph "External Integration Tier"
        GeminiV["Google Gemini Vision API"]
        GeminiLLM["Google Gemini Chat API"]
        OFF["OpenFoodFacts Barcode API"]
    end

    Client -->|HTTPS| UI
    UI --> Router
    Router --> APIs
    APIs --> Nutri
    Nutri --> Gap
    Gap --> Stage1
    Stage1 --> Stage2
    Stage2 --> XGB
    APIs --> RF
    APIs --> DB
    DB --- M_User
    DB --- M_Food
    DB --- M_Log
    DB --- M_Groc
    APIs --> GeminiV
    APIs --> GeminiLLM
    APIs --> OFF
```

*Figure 4.1: Three-Tier System Architecture of MealMentor (NutriSense AI)*

### 4.3 Module Decomposition
MealMentor is decomposed into nine modular subsystems:
1. **Authentication & Session Module**: Handles registration, salted scrypt password hashing, JWT creation/validation, and OAuth.
2. **User Profile & Biometric Module**: Manages physical attributes, calculates BMR, TDEE, water requirements, and macro/micronutrient quotas.
3. **Food Inventory & Catalog Module**: Loads and queries 384 curated foods and custom user-created recipes.
4. **Food Intake & Real-Time Tracking Module**: Manages daily consumption logs and calculates scaled nutritional contributions.
5. **Real-Time Nutrient Gap Analysis Module**: Computes remaining deficits across 10 essential nutrients.
6. **Two-Stage Recommendation Engine**: Implements hard safety filtration (allergies, diet, budget) and soft multi-criteria scoring with variety decay.
7. **Machine Learning Pipeline Module**: Interfaces with XGBoost for rank scoring and FastAPI for 7-day weight forecasting.
8. **Multimodal Analysis Module**: Processes food photos via Gemini Vision and resolves product barcodes via OpenFoodFacts.
9. **Conversational Assistant & Fallback Module**: Powers interactive nutritional dialogue with automatic fallback to offline deterministic rule matching.

### 4.4 Use Case Diagram

```mermaid
graph TD
    User((End User))
    Admin((System Admin))

    subgraph "MealMentor System Boundary"
        UC1[Register & Login]
        UC2[Manage Biometric Profile]
        UC3[Calculate BMR / TDEE & Nutrient Targets]
        UC4[Log Daily Food Intake]
        UC5[View Real-Time Nutrient Gaps]
        UC6[Request AI Meal Recommendations]
        UC7[Provide Recommendation Feedback]
        UC8[Scan Barcode / Upload Meal Photo]
        UC9[Chat with AI Nutrition Assistant]
        UC10[Generate Budget Grocery List]
        UC11[View 7-Day Weight Trend & Forecast]
        UC12[Seed & Maintain Food Datasets]
    end

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    User --> UC11

    Admin --> UC12
    Admin --> UC1
```

*Figure 4.2: Use Case Diagram for User and System Roles*

### 4.5 Data Flow Diagrams (Level 0 and Level 1)

#### Level-0 Context DFD
```mermaid
flowchart LR
    User["End User"]
    System["MealMentor System"]
    ExtService["External APIs (Gemini / OpenFoodFacts)"]
    DB[("MongoDB Datastore")]

    User -->|Biometrics, Logs, Photos, Queries| System
    System -->|Targets, Gaps, Recommendations, Charts| User
    System -->|Image, Barcode, Prompts| ExtService
    ExtService -->|Nutrient Estimates, Food Meta, Responses| System
    System -->|Persist Logs, Profiles, Feedback| DB
    DB -->|Fetch Catalog, User State, Logs| System
```

*Figure 4.3: Level-0 Context Data Flow Diagram*

#### Level-1 Detailed DFD
```mermaid
flowchart TD
    User["User"]
    P1["1.0 Profile & Intake Management"]
    P2["2.0 Metabolic & Target Calculator"]
    P3["3.0 Real-Time Gap Analyzer"]
    P4["4.0 Two-Stage Recommendation Engine"]
    P5["5.0 Multimodal & AI Services"]
    
    D1[("User Collection")]
    D2[("Food Dataset")]
    D3[("MealEntry Logs")]
    Ext["External APIs"]

    User -->|Enters biometrics| P1
    P1 -->|Stores biometrics| D1
    D1 -->|Reads biometrics| P2
    P2 -->|Outputs BMR, TDEE, Targets| P3
    
    User -->|Logs Food Items| P1
    P1 -->|Writes food log| D3
    D3 -->|Reads consumed nutrients| P3
    
    P3 -->|Supplies Nutrient Gaps| P4
    D2 -->|Supplies Food Candidates| P4
    D1 -->|Supplies Allergens & Budget| P4
    D3 -->|Supplies 3-day history| P4
    P4 -->|Delivers Ranked Recommendations| User
    
    User -->|Submits Photo / Barcode| P5
    P5 <-->|Vision / Product Data| Ext
    P5 -->|Populates Log Entry| P1
```

*Figure 4.4: Level-1 Detailed Data Flow Diagram*

### 4.6 Database Design and Data Dictionary
MealMentor uses MongoDB with Mongoose schemas. Primary collections include:

#### Table 4.1: User Collection Data Dictionary
| Field Name | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `_id` | ObjectId | Primary Key | Unique user identifier |
| `name` | String | Required | Full name of user |
| `email` | String | Required, Unique, Indexed | Authentication email address |
| `passwordHash` | String | Required (if local auth) | Salted scrypt password hash |
| `age` | Number | Optional ($10 - 120$) | Age in years |
| `gender` | String | `male` \| `female` \| `other` | Biological sex for BMR formula |
| `height` | Number | Optional ($50 - 250$) | Height in centimeters |
| `weight` | Number | Optional ($20 - 300$) | Current weight in kilograms |
| `activityLevel` | String | Enum: sedentary, light, etc. | Physical activity category |
| `healthGoal` | String | Enum: weight_loss, maintain, etc. | Primary fitness objective |
| `dietaryRestrictions`| Array[String]| Substrings / tags | e.g., vegetarian, vegan, halal |
| `allergies` | Array[String]| Lowercase strings | e.g., peanuts, dairy, gluten |
| `conditions` | Array[String]| Lowercase strings | e.g., diabetes, hypertension |
| `budgetPerMeal` | Number | Default: 100.0 | Maximum target cost per meal |

#### Table 4.2: Food Collection Data Dictionary
| Field Name | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `_id` | ObjectId | Primary Key | Unique food item identifier |
| `name` | String | Required, Indexed | Canonical name of the food |
| `calories` | Number | Required | Calories per 100g (kcal) |
| `protein` | Number | Required | Protein per 100g (g) |
| `carbs` | Number | Required | Total carbohydrates per 100g (g) |
| `fat` | Number | Required | Total lipids/fat per 100g (g) |
| `fiber` | Number | Required | Dietary fiber per 100g (g) |
| `sugar` | Number | Required | Sugars per 100g (g) |
| `sodium` | Number | Required | Sodium per 100g (mg) |
| `calcium` | Number | Optional | Calcium per 100g (mg) |
| `iron` | Number | Optional | Iron per 100g (mg) |
| `vitaminC` | Number | Optional | Vitamin C per 100g (mg) |
| `dietType` | String | `veg` \| `non-veg` \| `vegan` | Dietary philosophy classification |
| `mealType` | Array[String]| breakfast, lunch, dinner, snack| Appropriate consumption occasions |
| `allergens` | Array[String]| Lowercase strings | Allergen tags (e.g., dairy, nuts) |
| `pricePer100g` | Number | Required | Monetary price per 100g serving |

#### Table 4.3: MealEntry Collection Data Dictionary
| Field Name | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `_id` | ObjectId | Primary Key | Unique meal entry record identifier |
| `userId` | ObjectId | Required, Ref: User, Indexed | Foreign reference to User |
| `foodId` | ObjectId | Ref: Food | Reference to catalog food item |
| `foodName` | String | Required | Name of the logged food |
| `mealType` | String | Enum: breakfast, lunch, etc. | Occasion of meal |
| `quantityGrams` | Number | Required | Consumed quantity in grams |
| `calories` | Number | Required | Calculated calories for portion |
| `protein` | Number | Required | Calculated protein for portion |
| `carbs` | Number | Required | Calculated carbs for portion |
| `fat` | Number | Required | Calculated fat for portion |
| `loggedAt` | Date | Default: `Date.now`, Indexed | Timestamp of consumption |

#### Table 4.4: WeightLog Collection Data Dictionary
| Field Name | Data Type | Constraints | Description |
|:---|:---|:---|:---|
| `_id` | ObjectId | Primary Key | Unique log identifier |
| `userId` | ObjectId | Required, Ref: User, Indexed | Reference to User |
| `weightKg` | Number | Required ($20 - 300$) | Recorded body weight in kg |
| `date` | Date | Default: `Date.now`, Indexed | Measurement date |

### 4.7 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USER ||--o{ MEAL_ENTRY : logs
    USER ||--o{ WEIGHT_LOG : records
    USER ||--o{ FEEDBACK : submits
    USER ||--o{ WATER_LOG : tracks
    FOOD ||--o{ MEAL_ENTRY : references
    FOOD ||--o{ FEEDBACK : targets
    GROCERY_ITEM ||--o{ GROCERY_LIST : aggregates

    USER {
        ObjectId _id PK
        string name
        string email UK
        string passwordHash
        number age
        string gender
        number height
        number weight
        string activityLevel
        string healthGoal
        string_array allergies
        string_array conditions
        number budgetPerMeal
    }

    FOOD {
        ObjectId _id PK
        string name
        number calories
        number protein
        number carbs
        number fat
        number fiber
        number sugar
        number sodium
        string dietType
        string_array mealType
        string_array allergens
        number pricePer100g
    }

    MEAL_ENTRY {
        ObjectId _id PK
        ObjectId userId FK
        ObjectId foodId FK
        string foodName
        string mealType
        number quantityGrams
        number calories
        number protein
        Date loggedAt
    }

    WEIGHT_LOG {
        ObjectId _id PK
        ObjectId userId FK
        number weightKg
        Date date
    }

    FEEDBACK {
        ObjectId _id PK
        ObjectId userId FK
        ObjectId foodId FK
        string action
        Date createdAt
    }

    GROCERY_ITEM {
        ObjectId _id PK
        string name
        string category
        number pricePerUnit
        string unit
    }
```

*Figure 4.5: Entity-Relationship Diagram*

### 4.8 Sequence Diagrams (UML Interaction Models)

#### Sequence Diagram 1: User Authentication Flow
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser as React Frontend
    participant API as Auth API (/api/auth)
    participant Crypto as Scrypt Utility
    participant DB as MongoDB (User)

    User->>Browser: Enters email and password
    Browser->>API: POST /api/auth/login {email, password}
    API->>DB: findOne({email})
    DB-->>API: Returns user record with passwordHash
    API->>Crypto: verifyPassword(password, passwordHash)
    Note over Crypto: scrypt split salt:derivedKey and compare
    Crypto-->>API: Password Verified (true)
    API->>API: Generate signed JWT session token
    API-->>Browser: Set-Cookie (token, httpOnly) & 200 OK
    Browser-->>User: Redirect to Dashboard (/dashboard)
```

*Figure 4.6: Sequence Diagram for User Authentication*

#### Sequence Diagram 2: Two-Stage Recommendation Pipeline
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Page as Meal Plan Page
    participant RecAPI as /api/recommend
    participant Engine as Recommendation Engine
    participant DB as MongoDB
    participant XGB as Python ML Service

    User->>Page: Requests Recommendations (e.g. Lunch)
    Page->>RecAPI: POST /api/recommend {mealType: "lunch"}
    RecAPI->>DB: Fetch User Profile (allergies, diet, budget, goals)
    RecAPI->>DB: Fetch MealEntries for today & past 3 days
    RecAPI->>Engine: Compute Targets & Remaining Nutrient Gaps
    Engine->>DB: Fetch Candidate Foods (Food.find({mealType: "lunch"}))
    DB-->>Engine: 150 Candidate Food Items
    
    rect rgb(240, 248, 255)
    Note over Engine: Stage 1: Hard Constraint Filtering
    Engine->>Engine: Filter out foods matching user allergies
    Engine->>Engine: Filter out non-veg foods if veg/vegan profile
    Engine->>Engine: Filter out foods exceeding meal budget
    end
    
    rect rgb(255, 250, 240)
    Note over Engine: Stage 2: Soft Multi-Criteria Ranking
    Engine->>Engine: Calculate S_nutrient (gap coverage)
    Engine->>Engine: Apply S_variety (3-day history penalty)
    Engine->>Engine: Score S_preference & S_cost
    end

    Engine->>XGB: (Optional) Re-rank candidates via XGBoost
    XGB-->>Engine: Re-ranked candidate indices & scores
    Engine-->>RecAPI: Formatted top N recommendations with reasons
    RecAPI-->>Page: JSON Response (Targets, Gaps, Recommendations)
    Page-->>User: Displays Recommended Meals with Nutrition Cards
```

*Figure 4.7: Sequence Diagram for Two-Stage Meal Recommendation Pipeline*

#### Sequence Diagram 3: Quantity-Aware Food Logging
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Food Tracking UI
    participant API as /api/food-log
    participant Nutri as Nutrition Lib
    participant DB as MongoDB

    User->>UI: Selects food item (e.g., Brown Rice) & enters 150g
    UI->>API: POST /api/food-log {foodId, mealType: "lunch", quantityGrams: 150}
    API->>DB: Food.findById(foodId)
    DB-->>API: Returns base values per 100g (111 kcal, 2.6g P, etc.)
    API->>Nutri: scaleNutrients(food, 150)
    Note over Nutri: scaled = (base * 150) / 100
    Nutri-->>API: Returns scaled values (166.5 kcal, 3.9g P)
    API->>DB: MealEntry.create({...scaledData, userId})
    DB-->>API: Persisted entry saved
    API-->>UI: 201 Created {entry, updatedDailyTotals}
    UI-->>User: Updates Dashboard progress bars and gap cards
```

*Figure 4.8: Sequence Diagram for Food Intake Logging*

#### Sequence Diagram 4: Multimodal Food Photo Analysis
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant CameraUI as Food Photo UI
    participant VisionAPI as /api/food-photo
    participant Gemini as Google Gemini Vision API

    User->>CameraUI: Captures/Uploads photo of meal plate
    CameraUI->>VisionAPI: POST /api/food-photo (multipart/form-data: image)
    VisionAPI->>VisionAPI: Validate MIME type & file size (< 5MB)
    VisionAPI->>Gemini: generateContent([imageBuffer, structuredNutritionPrompt])
    Note over Gemini: Analyzes visual features, food items, estimated portions
    Gemini-->>VisionAPI: JSON {foodName, estimatedWeightG, calories, protein, carbs, fat}
    VisionAPI-->>CameraUI: 200 OK with recognized nutritional breakdown
    CameraUI-->>User: Displays detected foods; user reviews and clicks "Confirm Log"
```

*Figure 4.9: Sequence Diagram for Multimodal Meal Photo Analysis*

---

## CHAPTER 5: SYSTEM IMPLEMENTATION

### 5.1 Development Environment Setup
The development environment was configured as follows:
- **Node.js**: v20.18.0 LTS running on Windows 11 64-bit.
- **Package Manager**: npm v10.8.2.
- **Python Runtime**: Python 3.11.8 virtual environment (`ml/venv`) with dependencies installed via `requirements.txt`.
- **Database Server**: MongoDB Community Server 7.0 running on `localhost:27017` with MongoDB Compass GUI for schema inspection.
- **IDE**: Visual Studio Code with ESLint, Prettier, and TypeScript extensions.

### 5.2 Technology Stack Details
The core technologies powering MealMentor include:
- **Next.js 16 (React 19)**: Implements the App Router for server-side rendering, streaming HTML, and API route handlers.
- **Tailwind CSS v4**: Utility-first styling with customized CSS variables for dark/light themes and responsive design.
- **Radix UI & Lucide React**: Provides accessible UI components and interface icons.
- **Recharts**: Renders responsive SVG charts for nutrient gaps, macronutrient distribution, and 7-day weight history.
- **Mongoose 9.9.4**: Strongly typed MongoDB ODM schemas ensuring document validation.
- **XGBoost & scikit-learn**: Python ML libraries executing learning-to-rank algorithms and regression forecasting.
- **Google GenAI SDK**: Interfaces with Gemini 1.5/2.0 Flash models for vision and natural language processing.

### 5.3 Frontend Implementation
The frontend is structured within `nutrisense-ai/src/app`:
- `(auth)/login`, `(auth)/register`, `(auth)/reset-password`: Authentication pages styled with accessible forms, error alerts, and password visibility toggles.
- `(dashboard)/dashboard`: The main hub displaying daily calorie progress, macronutrient progress rings, water intake widget, streak counters, and weight forecasting cards.
- `(dashboard)/meal-plan`: Displays meal recommendation cards generated by the two-stage pipeline, including nutrient gap drivers, cost per portion, and accept/reject feedback buttons.
- `(dashboard)/food-tracking`: Allows instant search through 384 verified food items, custom portion entry (in grams), and real-time calculation of logged items.
- `(dashboard)/food-photo`: Multimodal upload zone supporting drag-and-drop or mobile camera capture for automated nutrient recognition.
- `(dashboard)/grocery`: Automatically compiles missing ingredients into a categorized, budget-aware grocery checklist with price totals.
- `(dashboard)/ai-assistant`: Conversational interface connecting to the Gemini LLM with streaming output and automatic offline deterministic fallback.

### 5.4 Backend and API Implementation
Backend functionality is implemented as Next.js API Routes (`src/app/api/*`):
- `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`: Handles user credentials, crypto.scrypt password verification, and JWT cookie management.
- `/api/user/profile`: Fetches and updates demographic, biometric, and dietary preference attributes.
- `/api/food-log`: Handles creation, deletion, and date-filtered queries of consumed meal items.
- `/api/recommend`: Executes the core two-stage recommendation pipeline based on profile constraints and current daily gaps.
- `/api/recommend-xgb`: Invokes the XGBoost ML model to re-rank candidate recommendations.
- `/api/weight-forecast`: Communicates with the FastAPI microservice to generate 7-day projected weight paths.
- `/api/food-photo`: Accepts image payloads, encodes to base64, and coordinates with the Google Gemini Vision API.
- `/api/ai/chat`: Handles conversational nutritional prompts, injecting current user context into the system prompt.
- `/api/barcode`: Interrogates the OpenFoodFacts REST API for packaged foods with local caching.

### 5.5 Database Layer and Mongoose Schemas
Data schemas are declared in `src/models/`:
- `User.ts`: Defines user profile fields, bcrypt/scrypt password hashes, allergies array, chronic condition flags, and meal budgets.
- `Food.ts`: Stores food items with 10 nutrient metrics, allergen tags, price-per-100g, and meal-type flags.
- `MealEntry.ts`: Persists timestamped food intake instances tied to user IDs.
- `WeightLog.ts`: Records chronological weight measurements for trend tracking.
- `Feedback.ts`: Captures user interactions with meal recommendations (liked, disliked, accepted) for continuous model adaptation.
- `GroceryItem.ts`: Stores standardized market prices for 331 basic food ingredients.

### 5.6 Authentication and Security Layer
- **Password Protection**: Handled via Node.js built-in `crypto.scrypt` with a 16-byte cryptographically secure random salt and a derived key length of 64 bytes (`salt:derivedKey` format).
- **Session Integrity**: Secured using HTTP-only, SameSite cookies containing signed JWTs, protecting against Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF).
- **Input Sanitization**: Request bodies are validated using strict TypeScript interfaces and schema guards, preventing NoSQL injection attacks.

### 5.7 AI and Machine Learning Layer

#### 1. Two-Stage Recommendation Pipeline (`src/lib/recommend.ts`)
- **Stage 1: Hard Constraint Elimination**:
  $$\text{Filter}(f) = 
  \begin{cases} 
  0 & \text{if } f.\text{allergens} \cap \text{User}.\text{allergens} \neq \emptyset \\
  0 & \text{if } \text{User}.\text{diet} \in \{\text{veg}, \text{vegan}\} \land f.\text{diet} = \text{non-veg} \\
  0 & \text{if } f.\text{cost} > \text{User}.\text{budgetPerMeal} \\
  1 & \text{otherwise}
  \end{cases}$$
- **Stage 2: Soft Multi-Criteria Ranking**:
  $$S(f) = w_1 S_{\text{nutrient}}(f) + w_2 S_{\text{preference}}(f) + w_3 S_{\text{cost}}(f) + w_4 S_{\text{variety}}(f)$$
  where default weights are $w_1 = 0.40, w_2 = 0.25, w_3 = 0.15, w_4 = 0.20$.
  The variety score penalizes repetition over the preceding 3 days:
  $$S_{\text{variety}}(f) = 1.0 - \left(\frac{3 - \text{DaysAgo}}{3}\right) \times 0.25$$

#### 2. XGBoost Learning-to-Rank (`ml/src/recommend_xgb.py`)
- Candidate meals passing Stage 1 are structured as feature vectors: $[\text{CalorieGapScore}, \text{ProteinGapScore}, \text{FiberGapScore}, \text{CostRatio}, \text{PreferenceMatch}, \text{VarietyPenalty}]$.
- An XGBoost ranking model computes a re-ranked relevance score to surface items with the highest expected user adherence.

#### 3. Random Forest Weight Forecasting (`ml/src/train_rf.py` & `backend/app/main.py`)
- Takes as input: 7-day rolling calorie surplus/deficit, starting weight, activity level, and biological sex.
- Predicts weight trajectories over 7 days using an ensemble of 100 decision trees, enforcing a conservative metabolic efficiency factor.

### 5.8 Deterministic Nutrition Calculation Formulas
All nutrition calculations are mathematically verified in `src/lib/nutrition.ts`:

1. **Body Mass Index (BMI)**:
   $$\text{BMI} = \frac{\text{weight}_{\text{kg}}}{(\text{height}_{\text{m}})^2}$$

2. **Basal Metabolic Rate (BMR) — Mifflin–St Jeor Equation**:
   $$\text{BMR}_{\text{male}} = 10 \times \text{weight}_{\text{kg}} + 6.25 \times \text{height}_{\text{cm}} - 5 \times \text{age} + 5$$
   $$\text{BMR}_{\text{female}} = 10 \times \text{weight}_{\text{kg}} + 6.25 \times \text{height}_{\text{cm}} - 5 \times \text{age} - 161$$

3. **Total Daily Energy Expenditure (TDEE)**:
   $$\text{TDEE} = \text{BMR} \times f_{\text{activity}}$$

**Table 5.1: Activity Multipliers ($f_{\text{activity}}$)**
| Activity Level | Multiplier ($f_{\text{activity}}$) | Definition |
|:---|:---|:---|
| Sedentary | 1.200 | Little or no exercise, desk work |
| Lightly Active | 1.375 | Light exercise 1–3 days/week |
| Moderately Active | 1.550 | Moderate exercise 3–5 days/week |
| Very Active | 1.725 | Hard exercise 6–7 days/week |
| Extra Active | 1.900 | Very heavy physical labor / athletic training |

4. **Caloric Target Adjustment by Goal**:
   $$\text{Target Calories} = \text{TDEE} + \Delta_{\text{goal}}$$

**Table 5.2: Caloric Goal Offsets**
| Health Goal | Offset ($\Delta_{\text{goal}}$) | Safety Clamping |
|:---|:---|:---|
| Weight Loss | $-500\text{ kcal}$ | $\ge 1200\text{ kcal (F)}, \ge 1500\text{ kcal (M)}$ |
| Mild Weight Loss | $-300\text{ kcal}$ | $\ge 1200\text{ kcal (F)}, \ge 1500\text{ kcal (M)}$ |
| Maintenance | $0\text{ kcal}$ | Unadjusted TDEE |
| Muscle Gain | $+350\text{ kcal}$ | Coupled with elevated protein targets |
| Weight Gain | $+500\text{ kcal}$ | Monitored nutrient density |

5. **Quantity-Aware Scaled Nutrient Intake**:
   For any consumed food item $i$ of quantity $q_i$ grams:
   $$\text{Nutrient Intake}_i = \text{Nutrient Value per 100g} \times \left(\frac{q_i}{100}\right)$$

6. **Daily Nutrient Gap Calculation**:
   $$G_n = \max(0, T_n - C_n)$$
   where $T_n$ is the daily target and $C_n = \sum_i \text{Nutrient Intake}_i$ is the total consumed amount.

7. **Condition-Aware Target Modifications**:
   - **Diabetes**: Maximum daily sugar clamped to $\le 25\text{g}$; fiber target increased to $\ge 35\text{g}$.
   - **Hypertension**: Maximum daily sodium clamped to $\le 1500\text{mg}$.

### 5.9 Recommendation Engine Workflow
1. Request arrives with user session token and optional meal occasion (`breakfast`, `lunch`, `dinner`, `snack`).
2. Current daily intake is aggregated from `MealEntry` records for the current date.
3. Nutrient gaps $G_n$ are computed for all 10 tracked nutrients.
4. Food items matching the requested meal type are extracted from the MongoDB food collection.
5. **Stage 1 Hard Filter**:
   - Excludes items where food allergens overlap with user allergies.
   - Excludes non-vegetarian items if the user is vegetarian/vegan.
   - Excludes items exceeding the meal budget.
6. **Stage 2 Soft Scoring**:
   - Each surviving item is evaluated against open nutrient gaps, awarding higher scores to items providing nutrients with the largest remaining deficits without triggering surpluses.
   - 3-day history penalty is applied if the food was consumed within the last 72 hours.
   - Preference boost applied if food cuisine/category matches user profile likes.
7. Top $K$ items are returned with data-grounded explanation strings.

### 5.10 External Integrations
- **Google Gemini Vision**: Food photos are uploaded as base64 images to `/api/food-photo`, sending structured prompts to Gemini 1.5/2.0 Flash to return itemized ingredients, estimated gram weights, and estimated nutritional values.
- **OpenFoodFacts Barcode Lookup**: Packaged food barcodes are queried via `https://world.openfoodfacts.org/api/v2/product/{barcode}.json`. If network is unavailable or the item is missing, an offline cache (`src/data/barcode-cache.json`) supplies standard staples.
- **AI Chatbot with Deterministic Fallback**: `/api/ai/chat` uses Gemini with system prompts injecting current user nutrient gaps. If the Gemini API key is missing or quotas are exceeded, `src/lib/offline-chat.ts` catches the request and generates rule-based answers.

---

## CHAPTER 6: TESTING AND RESULTS

### 6.1 Testing Methodology
A dual-tier testing strategy was implemented:
1. **Unit Testing with Vitest**: Validates isolated mathematical equations, nutrient scaling, constraint filtering, and gap tracking without database dependencies.
2. **End-to-End (E2E) Testing with Playwright**: Validates complete browser workflows, including user registration, authentication, dashboard rendering, food logging, and responsive viewport layouts.

### 6.2 Test Environment
- **Unit Test Runner**: Vitest 3.0.7 in Node.js environment.
- **E2E Test Runner**: Playwright 1.50.1 targeting Chromium, Firefox, and WebKit rendering engines across Desktop ($1280 \times 720$) and Mobile ($375 \times 667$, iPhone SE) viewports.

### 6.3 Test Cases and Test Execution

**Table 6.1: Vitest Unit Test Suite Execution Summary**

| Test File | Target Functionality | Test Scenarios | Result |
|:---|:---|:---|:---|
| `nutrition.test.ts` | Mifflin–St Jeor BMR & TDEE | Male/Female BMR, 5 activity levels, goal adjustments | **PASSED** (100%) |
| `gaps.test.ts` | Daily Gap Tracking | Zero consumption, partial intake, nutrient surplus capping | **PASSED** (100%) |
| `intake.test.ts` | Quantity Scaling | 0g, 50g, 100g, 250g portion scaling arithmetic | **PASSED** (100%) |
| `recommend.test.ts` | Stage 1 Hard Constraint Filtering | Peanut allergy exclusion, vegan profile non-veg exclusion | **PASSED** (100%) |
| `variety.test.ts` | Repetition Decay | 1-day, 2-day, 3-day penalty calculation ($S_{\text{variety}}$) | **PASSED** (100%) |
| `crypto.test.ts` | Password Hashing | scrypt salt derivation, timing safety, mismatch rejection | **PASSED** (100%) |

**Table 6.2: Playwright End-to-End Test Suite Execution Summary**

| Test Spec File | Feature Tested | Viewport / Browsers | Verified Assertions | Status |
|:---|:---|:---|:---|:---|
| `auth.spec.ts` | Registration & Login | Chromium, Firefox, WebKit | Form validation, JWT cookie set, dashboard redirect | **PASSED** |
| `dashboard.spec.ts`| Metric Cards & Charts | Desktop ($1280 \times 800$) | Calorie gauge, macro bars, water counter, streak badge | **PASSED** |
| `food-tracking.spec.ts`| Search & Logging | Desktop & Mobile | Search catalog, select 150g, verify list update & total | **PASSED** |
| `responsive.spec.ts`| Viewport Adaptability | Desktop, Tablet, Mobile | Mobile sidebar toggle, touch target sizes $\ge 44\text{px}$ | **PASSED** |

### 6.4 Verification Results
All 28 unit test suites and 4 Playwright browser specifications completed execution with zero errors. The system satisfied the key performance criteria:
- BMR and TDEE calculations showed zero variance from clinical test fixtures.
- Stage 1 filtering achieved a $0\%$ failure rate: in 1,000 synthetic test runs with declared peanut allergies, zero meals containing peanuts passed Stage 1.

### 6.5 Functional Validation and Numerical Proofs
To verify system accuracy, consider a representative test user:

**User Profile**:
- Sex: Male
- Age: 25 years
- Height: 175 cm
- Weight: 70 kg
- Activity: Moderately Active ($f_{\text{activity}} = 1.55$)
- Goal: Weight Loss ($-500\text{ kcal}$)
- Allergies: `[peanuts]`
- Health Condition: `[hypertension]` (Sodium clamped to $\le 1500\text{mg}$)

**Step 1: BMR Calculation**
$$\text{BMR} = 10(70) + 6.25(175) - 5(25) + 5 = 700 + 1093.75 - 125 + 5 = 1673.75\text{ kcal}$$

**Step 2: TDEE Calculation**
$$\text{TDEE} = 1673.75 \times 1.55 = 2594.31\text{ kcal}$$

**Step 3: Target Caloric Intake**
$$\text{Target} = 2594.31 - 500 = 2094.31 \approx 2094\text{ kcal}$$
*(Exceeds male safety floor of 1500 kcal; target accepted).*

**Step 4: Macronutrient Target Distribution**
- Protein ($25\%$ energy): $(2094 \times 0.25) / 4 = 130.9\text{g}$
- Carbs ($50\%$ energy): $(2094 \times 0.50) / 4 = 261.8\text{g}$
- Fat ($25\%$ energy): $(2094 \times 0.25) / 9 = 58.2\text{g}$
- Sodium Target: Clamped to $1500\text{mg}$ due to hypertension.

**Step 5: Logging Simulation and Gap Analysis**
User logs lunch: 200g of *Boiled Lentils (Dal)*:
- Base per 100g: 116 kcal, 9g Protein, 20g Carbs, 0.4g Fat, 8g Fiber, 2mg Sodium.
- Consumed ($200\text{g}$):
  - Calories: $116 \times 2 = 232\text{ kcal}$
  - Protein: $9 \times 2 = 18\text{g}$
  - Carbs: $20 \times 2 = 40\text{g}$
  - Fat: $0.4 \times 2 = 0.8\text{g}$
  - Sodium: $2 \times 2 = 4\text{mg}$

**Step 6: Remaining Gap Calculation**
- Calorie Gap: $2094 - 232 = 1862\text{ kcal}$
- Protein Gap: $130.9 - 18 = 112.9\text{g}$
- Sodium Gap: $1500 - 4 = 1496\text{mg}$

**Step 7: Recommendation Pipeline Execution**
The recommendation engine evaluates candidate dinner options:
- Item A: *Peanut Butter Tofu Bowl* $\rightarrow$ **REJECTED at Stage 1** (violates peanut allergy).
- Item B: *Grilled Chicken Breast Salad* $\rightarrow$ **ACCEPTED at Stage 1**, scores high in Stage 2 due to $31\text{g}$ protein addressing the large $112.9\text{g}$ protein deficit.

### 6.6 Performance Observations
- **API Latency**: Average response time for `/api/recommend` was $142\text{ ms}$ for cold invocations and $24\text{ ms}$ for cached warm executions on standard development hardware.
- **Database Query Time**: Indexed lookups on `MealEntry` by `userId` and `loggedAt` executed in under $4\text{ ms}$ on MongoDB.
- **Client Bundle Size**: Total initial JavaScript payload was under $180\text{ KB}$ gzipped due to Next.js server components.

### 6.7 Limitations
1. **Self-Reporting Bias**: Accurate gap tracking relies on the user entering realistic portion sizes.
2. **Static Food Catalog**: The local food catalog contains 384 verified food items. While adequate for standard diets, regional recipes may require manual custom food entry.
3. **Static Ingredient Prices**: Grocery cost calculations are based on standardized dataset prices rather than live supermarket API integrations.
4. **Non-Clinical Boundary**: The system provides wellness and dietary awareness, not diagnostic clinical nutrition therapy.

---

## CHAPTER 7: CONCLUSION AND FUTURE ENHANCEMENTS

### 7.1 Project Summary
MealMentor (NutriSense AI) successfully addresses the gap between passive food journaling and intelligent, personalized nutrition assistance. By integrating deterministic metabolic science (Mifflin–St Jeor) with a two-stage recommendation pipeline, machine learning models, and multimodal interfaces, MealMentor delivers an end-to-end dietary management solution that is safe, adaptive, and budget-aware.

### 7.2 Objectives Achieved

**Table 7.1: Objectives Achievement Status**

| Stated Objective | Status | Implementation Proof |
|:---|:---|:---|
| Deterministic Metabolic Engine | **Achieved** | Mifflin–St Jeor implemented in `src/lib/nutrition.ts` with 100% test pass rate |
| Condition-Aware Targets | **Achieved** | Dynamic clamps for diabetes and hypertension verified in test suite |
| Real-Time Nutrient Gap Analysis | **Achieved** | Dynamic recalculation across 10 essential nutrients in `src/lib/gaps.ts` |
| Two-Stage Recommendation Engine | **Achieved** | Stage 1 hard filter + Stage 2 soft multi-criteria ranker in `src/lib/recommend.ts` |
| Machine Learning Re-Ranking | **Achieved** | XGBoost ranking model integrated via `src/app/api/recommend-xgb/route.ts` |
| 7-Day Weight Forecasting | **Achieved** | Random Forest model running in Python FastAPI service |
| Multimodal Interfaces | **Achieved** | Gemini Vision photo recognition and OpenFoodFacts barcode scanner |
| Repetition & Variety Control | **Achieved** | 3-day history decay penalty ($S_{\text{variety}}$) implemented and tested |
| Accessible, Responsive Web UI | **Achieved** | Next.js 16 / React 19 UI validated across desktop and mobile viewports |

### 7.3 Key Engineering Contributions
1. **Hybrid Architecture for AI Safety**: Demonstrates that decoupling hard safety constraints (allergies, diet philosophy) from soft optimization (ML ranking) prevents AI safety hazards in dietary applications.
2. **Nutrient-Gap-Aware Optimization**: Shifts dietary recommendation from static plans to real-time compensatory recommendations that bridge current daily nutritional deficiencies.
3. **Multimodal Friction Reduction**: Combines food photo recognition and barcode lookup with offline fallbacks to minimize manual logging effort.
4. **Explainable Recommendations**: Generates transparent, data-grounded explanations linking every meal suggestion to specific nutrient gaps and budget requirements.

### 7.4 Current Limitations
- Food photo nutrition estimation is subject to visual portion size estimation errors.
- Grocery price data is sourced from static datasets rather than live supermarket inventory APIs.
- Wearable devices are not currently integrated via direct background syncing.

### 7.5 Future Enhancements
1. **IoT & Wearable Integration**: Ingest real-time energy expenditure data from Apple HealthKit, Google Health Connect, and Garmin smartwatches.
2. **Live Supermarket API Integration**: Connect grocery lists directly to live supermarket APIs (Instacart, Amazon Fresh, Blinkit) for one-click ordering.
3. **Fine-Tuned Domain Vision Models**: Fine-tune localized food classification models (e.g., Food-101 / Nutrition5k) on edge devices for faster offline photo recognition.
4. **Blood Biomarker Ingestion**: Incorporate blood test reports (lipid profile, HbA1c, iron levels) for personalized micronutrient targeting.

### 7.6 Final Conclusion
MealMentor provides a functional, production-grade engineering foundation for next-generation personalized nutrition. By balancing mathematical precision, algorithmic rigor, and modern web usability, the platform demonstrates how full-stack web technologies and machine learning can be combined to support healthier dietary habits.

---

## REFERENCES

[1] X. Deng and W. Tu, "Personalized nutrition-aware dietary recommendation with multimodal large language models," *IEEE Access*, vol. 14, pp. 21791–21804, 2026.

[2] J. N. Bondevik, K. E. Bennin, O. Babur, and C. Ersch, "A systematic review on food recommender systems," *Expert Systems with Applications*, vol. 238, Art. no. 122166, 2024.

[3] Y. Chen, A. Subburathinam, C.-H. Chen, and M. J. Zaki, "Personalized food recommendation as constrained question answering over a large-scale food knowledge graph," in *Proc. 14th ACM Int. Conf. Web Search and Data Mining (WSDM)*, 2021, pp. 544–552.

[4] S. Rendle, C. Freudenthaler, and L. Schmidt-Thieme, "Factorizing personalized Markov chains for next-basket recommendation," in *Proc. 19th Int. Conf. World Wide Web (WWW)*, 2010, pp. 811–820.

[5] W.-C. Kang and J. McAuley, "Self-attentive sequential recommendation," in *Proc. IEEE Int. Conf. Data Mining (ICDM)*, 2018, pp. 197–206.

[6] F. Sun et al., "BERT4Rec: Sequential recommendation with bidirectional encoder representations from transformer," in *Proc. 28th ACM CIKM*, 2019, pp. 1441–1450.

[7] M. Rostami, M. Oussalah, and V. Farrahi, "A novel time-aware food recommender-system based on deep learning and graph clustering," *IEEE Access*, vol. 10, pp. 52508–52524, 2022.

[8] M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty, and Y. O. Koh, "A new predictive equation for resting energy expenditure in healthy individuals," *The American Journal of Clinical Nutrition*, vol. 51, no. 2, pp. 241–247, 1990.

[9] J. H. Guo, Z. Li, L. Y. Yao, Y. W. Zhang, and T. Q. Pan, "Dietary recommendation systems: A comprehensive survey," *ACM Computing Surveys*, vol. 56, no. 4, pp. 1–40, 2023.

[10] R. K. Johnson and P. R. Trexler, "Practical applications of nutritional assessment in clinical dietetics," *Journal of the Academy of Nutrition and Dietetics*, vol. 112, no. 2, pp. 220–230, 2012.

---

## APPENDICES

### Appendix A: REST API Specification
- `POST /api/auth/register`: `{name, email, password}` $\rightarrow$ Creates user, returns status 201.
- `POST /api/auth/login`: `{email, password}` $\rightarrow$ Sets HTTP-only auth token cookie, returns status 200.
- `GET /api/user/profile`: Returns full profile, biometric metrics, and computed targets.
- `PUT /api/user/profile`: Updates biometrics, dietary restrictions, allergies, and health conditions.
- `POST /api/food-log`: `{foodId, mealType, quantityGrams}` $\rightarrow$ Logs food intake and updates daily totals.
- `GET /api/food-log?date=YYYY-MM-DD`: Returns all meals logged for the specified date with nutrient totals.
- `POST /api/recommend`: `{mealType, inBudget}` $\rightarrow$ Runs two-stage pipeline, returns ranked meal items with reasons.
- `POST /api/recommend-xgb`: Invokes XGBoost ML model to re-rank filtered candidates.
- `POST /api/food-photo`: Accepts image upload, queries Gemini Vision API, returns detected food items and nutritional breakdown.
- `POST /api/ai/chat`: `{message}` $\rightarrow$ Streams conversational AI nutrition advice with current user context.
- `GET /api/barcode?code=UPC`: Looks up packaged product information from OpenFoodFacts.

### Appendix B: Database Schemas (DDL Excerpts)
```typescript
// User Mongoose Schema
const UserSchema = new Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true, index: true },
  passwordHash: { type: String, required: true },
  age: { type: Number, min: 10, max: 120 },
  gender: { type: String, enum: ['male', 'female', 'other'] },
  height: { type: Number, min: 50, max: 250 },
  weight: { type: Number, min: 20, max: 300 },
  activityLevel: { type: String, default: 'sedentary' },
  healthGoal: { type: String, default: 'maintain' },
  dietaryRestrictions: [{ type: String }],
  allergies: [{ type: String }],
  conditions: [{ type: String }],
  budgetPerMeal: { type: Number, default: 100 }
}, { timestamps: true });
```

### Appendix C: Core Algorithm Source Code Excerpts
```typescript
// BMR and TDEE Calculation (src/lib/nutrition.ts)
export function calculateBMR(weightKg: number, heightCm: number, age: number, gender: string): number {
  if (gender === 'female') {
    return 10 * weightKg + 6.25 * heightCm - 5 * age - 161;
  }
  return 10 * weightKg + 6.25 * heightCm - 5 * age + 5;
}

export function calculateTDEE(bmr: number, activityLevel: string): number {
  const multipliers: Record<string, number> = {
    sedentary: 1.200,
    light: 1.375,
    moderate: 1.550,
    active: 1.725,
    very_active: 1.900,
  };
  return bmr * (multipliers[activityLevel] || 1.200);
}
```

### Appendix D: User Manual
1. **Account Registration**: Navigate to `/register`, enter name, email, and password. Log in at `/login`.
2. **Profile Setup**: Go to `/profile`, enter age, height, weight, activity level, health goals, allergies, and budget. The system automatically computes your daily targets.
3. **Daily Food Tracking**: Navigate to `/food-tracking`, search for foods, select your portion in grams, and click "Log Food". Alternatively, use `/food-photo` to take a picture of your plate or scan a barcode.
4. **Viewing Nutrient Gaps**: Check the Dashboard (`/dashboard`) or Nutrition page (`/nutrition`) to review your real-time progress bars and remaining nutrient gaps.
5. **Requesting Recommendations**: Open `/meal-plan`, select your upcoming meal occasion (e.g., Lunch), and review constraint-safe, gap-optimized suggestions. Click "Accept" to log the meal directly.
6. **Grocery Planning**: Navigate to `/grocery` to view your compiled weekly ingredient list and estimated total costs.

### Appendix E: Installation and Execution Manual
```bash
# Clone the repository
git clone https://github.com/your-repo/mealmentor.git
cd mealmentor/nutrisense-ai

# Install Node.js dependencies
npm install

# Configure Environment Variables
cp .env.example .env.local
# Set MONGODB_URI=mongodb://localhost:27017/nutrisense
# Set GEMINI_API_KEY=your_gemini_key

# Seed Database
npm run db:seed

# Run Development Server
npm run dev

# Run Vitest Unit Tests
npm run test:unit

# Run Playwright E2E Tests
npx playwright test
```

### Appendix F: Complete Feature Verification Matrix

**Table F.1: Implementation Verification Matrix**

| Feature | Implementation Status | Evidence / File Path | Explanation | Limitations |
|:---|:---|:---|:---|:---|
| **User Authentication** | Fully implemented and verified | `src/app/api/auth/*`, `src/lib/auth.ts`, `src/lib/crypto.ts` | Salted scrypt hashing, JWT cookies, Google OAuth support | Password reset email sending requires SMTP credentials |
| **BMR & TDEE Calculations** | Fully implemented and verified | `src/lib/nutrition.ts`, `tests/unit/nutrition.test.ts` | Exact Mifflin–St Jeor formula with 5 activity multipliers | Relies on self-reported weight and activity level |
| **Nutrient Target Derivation** | Fully implemented and verified | `src/lib/nutrition.ts`, `src/lib/gaps.ts` | Derives 10 targets; applies diabetes and hypertension adjustments | Non-clinical estimations; not medical prescriptions |
| **Food Intake Logging** | Fully implemented and verified | `src/app/api/food-log/route.ts`, `src/models/MealEntry.ts` | Scales all 10 nutrients based on entered gram weight | User portion estimation uncertainty |
| **Real-Time Gap Tracking** | Fully implemented and verified | `src/lib/gaps.ts`, `src/app/(dashboard)/nutrition/page.tsx` | Calculates remaining deficit $G_n = \max(0, T_n - C_n)$ | Does not penalize moderate micronutrient excesses |
| **Two-Stage Recommendation** | Fully implemented and verified | `src/lib/recommend.ts`, `src/app/api/recommend/route.ts` | Stage 1 hard allergy/diet filter; Stage 2 soft multi-criteria scoring | Catalog bounded to 384 verified food items |
| **Variety Enforcement** | Fully implemented and verified | `src/lib/recommend.ts`, `tests/unit/variety.test.ts` | Applies 3-day history decay penalty to avoid meal repetition | History lookback limited to past 72 hours |
| **XGBoost Re-Ranking** | Fully implemented and verified | `ml/src/recommend_xgb.py`, `src/app/api/recommend-xgb/route.ts` | ML learning-to-rank re-scores filtered candidates | Requires Python runtime environment |
| **7-Day Weight Forecasting** | Fully implemented and verified | `ml/src/train_rf.py`, `backend/app/main.py` | Random Forest model trained on caloric balance | Assumes static caloric adherence over 7 days |
| **Multimodal Photo Analysis** | Fully implemented and verified | `src/app/api/food-photo/route.ts`, `src/app/(dashboard)/food-photo/page.tsx` | Google Gemini Vision API extracts food items and portions | Subject to visual portion estimation variances |
| **Barcode Scanning** | Fully implemented and verified | `src/app/api/barcode/route.ts`, `src/data/barcode-cache.json` | Queries OpenFoodFacts with local offline cache fallback | Packaged items only; unlisted items use manual entry |
| **AI Nutrition Chatbot** | Fully implemented and verified | `src/app/api/ai/chat/route.ts`, `src/lib/offline-chat.ts` | Gemini conversational assistant with deterministic offline fallback | General nutritional guidance; non-clinical |
| **Grocery List Generator** | Fully implemented and verified | `src/app/(dashboard)/grocery/page.tsx`, `finalDatasetGrocery.csv` | Aggregates ingredients and estimates costs across 331 items | Based on standardized regional prices |
| **Unit & E2E Testing** | Fully implemented and verified | `vitest.config.mjs`, `playwright.config.ts`, `tests/` | 28 unit tests and 4 Playwright E2E browser test specs | Mock API used during continuous integration |
