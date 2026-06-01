"""
Configuration settings for Variable Hunt application
"""

# CrossRef API Configuration
CROSSREF_API_BASE = "https://api.crossref.org/v1/"
CROSSREF_EMAIL = "your-email@example.com"  # Best practice for CrossRef
CROSSREF_TIMEOUT = 10  # seconds

# Streamlit Configuration
APP_TITLE = "Variable Hunt 🔍"
APP_DESCRIPTION = "Research Methodology Assistant for Quantitative Social Science"

# Discipline Configurations
DISCIPLINES = {
    "Econometrics": {
        "description": "Focuses on identification strategy, causal inference, and endogeneity issues",
        "priority": ["identification", "causal_inference", "endogeneity"],
        "key_journals": ["Econometrica", "Journal of Econometrics", "Review of Economics and Statistics"]
    },
    "Sociology": {
        "description": "Emphasizes theoretical mechanisms, social structures, and institutional factors",
        "priority": ["theory", "mechanism", "institution"],
        "key_journals": ["American Sociological Review", "Sociology of Education", "Social Forces"]
    },
    "Public Health": {
        "description": "Prioritizes confounders, health determinants, and population-level effects",
        "priority": ["confounder", "health_determinant", "population"],
        "key_journals": ["American Journal of Public Health", "Epidemiology", "Lancet"]
    }
}

# Variable Categories
VARIABLE_CATEGORIES = {
    "INDEPENDENT_VARIABLE": "Theoretically central, directly tests the main hypothesis",
    "COVARIATE": "Theoretically relevant but not the primary focus",
    "CONTROL_VARIABLE": "Included to address confounding, standard in the literature"
}

# Minimum Evidence Requirements
MIN_CITATIONS_FOR_SUGGESTION = 1
MIN_CITATION_YEAR = 2000  # Only suggest variables from recent literature

# Endogeneity Risk Flags
ENDOGENEITY_KEYWORDS = [
    "reverse causality",
    "simultaneity",
    "measurement error",
    "omitted variable bias",
    "selection bias",
    "endogenous",
    "lagged dependent"
]

# Data Source Types
DATA_SOURCES = [
    "Survey",
    "Administrative Data",
    "Experimental Data",
    "Census",
    "Longitudinal Panel",
    "Register Data",
    "Web/Big Data",
    "Mixed Methods"
]

# Literature Search Settings
MAX_SEARCH_RESULTS = 20
SEARCH_TIMEOUT = 30

# Caching
CACHE_DURATION = 3600  # 1 hour in seconds

print("✅ Configuration loaded successfully")
