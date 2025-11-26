# Major Power Outage Data Science Project  
### SIMPLE PROJECT PLAN (README)

## 📌 Project Title
**Predicting the Severity of Major Power Outages in the Continental U.S.**

---

## 📌 Project Objectives
- Explore where, when, and why major outages occur.
- Identify factors associated with severe outages.
- Perform **two hypothesis tests**.
- Build a **baseline model** and a **final model** to predict outage severity.

---

## 📌 Dataset
Source: *Major Power Outage Events in the Continental U.S.* (ScienceDirect)

Includes:
- Outage duration  
- Customers affected  
- Cause type  
- Climate + geographic characteristics  
- Economic + land-use features  
- Date/time of outage  
- State-level attributes  

---

## 📌 Project Workflow

### **1. Data Cleaning**
- Load dataset  
- Handle missing values  
- Convert date, numeric, and categorical fields  
- Create new variables (season, year, weather_flag, etc.)

---

### **2. Exploratory Data Analysis (EDA)**
- Outage frequency by state  
- Severity distribution (duration, customers)  
- Cause categories  
- Time trends  
- Geographic heatmaps  
- Correlation analysis  

---

### **3. Hypothesis Testing**

#### **Hypothesis Test 1: Climate Region → Outage Duration**  
- **H₀:** Mean outage duration is the same across climate regions  
- **H₁:** At least one region differs  
- **Test:** One-way ANOVA (or Kruskal–Wallis)

#### **Hypothesis Test 2: Weather vs. Non-Weather → Customers Affected**  
- **H₀:** Weather-caused and non-weather outages affect the same number of customers  
- **H₁:** They differ  
- **Test:** Two-sample t-test (or Mann–Whitney)

---

### **4. Feature Engineering**
- Encode cause type  
- Create climate zone variables  
- Create “season” from date  
- Population/economic normalization  
- Log-transform severity (if skewed)

---

## 📌 Modeling

### **5. Baseline Model**
**Linear Regression**  
- Predict severity (duration OR customers affected)  
- Basic benchmark for performance  

Metrics:
- RMSE  
- MAE  
- R²  

---

### **6. Final Model**
**Random Forest Regressor** (or XGBoost)  
- Handles nonlinear effects  
- Typically more accurate  
- Perform hyperparameter tuning  

Metrics:
- RMSE  
- MAE  
- R²  
- Compare improvement over baseline  

---

## 📌 7. Evaluation & Interpretation
- Compare baseline vs. final model performance  
- Plot predicted vs. actual values  
- Show feature importances  
- Summarize key predictors of outage severity  

---

## 📌 8. Deliverables
- README.md  
- Jupyter Notebook (.ipynb)  
- Data cleaning + EDA  
- Hypothesis test results  
- Baseline model  
- Final model  
- Visualizations and conclusions  

---

## 📌 9. Conclusion
Summarize:
- Where and when outages occur most  
- Which features strongly predict severity  
- Whether hypotheses were rejected or accepted  
- How the final model improves over baseline  

---
