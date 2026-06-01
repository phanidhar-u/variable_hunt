# Variable Hunt 🔍

A research methodology assistant specializing in quantitative social science that helps researchers identify the most important **independent variables, covariates, and control variables** for a given dependent variable, based on published empirical literature.

## ✨ Features

- **Evidence-Based Variable Selection**: Every suggested variable backed by published studies (no invented variables)
- **Three-Category Classification**:
  - **INDEPENDENT VARIABLE**: Theoretically central, directly tests the main hypothesis
  - **COVARIATE**: Theoretically relevant but not the primary focus
  - **CONTROL VARIABLE**: Included to address confounding, standard in literature
- **Discipline-Aware Recommendations**:
  - **Econometrics**: Identification and causal inference focus
  - **Sociology**: Theory and social mechanisms emphasis
  - **Public Health**: Confounders and health determinants priority
- **Complete Variable Documentation**: Names, mechanisms, citations, data sources, endogeneity flags
- **CrossRef API Integration**: Search published literature automatically (no API key needed)
- **Interactive Variable Builder**: Create custom variables with full documentation
- **Citation Management**: Support for APA, Chicago, Harvard, and BibTeX formats
- **Export Options**: CSV, citation files, and selection summaries

## 🎯 Core Rules

1. ✅ **Evidence-Based**: Every variable backed by published empirical research
2. 📋 **Clear Classification**: Each variable in exactly one category
3. 📚 **Complete Documentation**: Mechanism, citations, data source for each variable
4. ⚠️ **Endogeneity Flagging**: Identifies variables causing identification problems
5. 📊 **Evidence-Ordered**: Variables ranked by literature strength within category
6. 🎓 **Discipline-Aware**: Tailored to econometrics, sociology, or public health

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/phanidhar-u/variable_hunt.git
cd variable_hunt

# Create virtual environment
py -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app opens at `http://localhost:8501`

### First Steps

1. **Select your discipline** (Econometrics, Sociology, or Public Health)
2. **Enter dependent variable** (what outcome are you explaining?)
3. **Browse pre-populated variables** organized by category
4. **Search literature** via CrossRef for evidence
5. **Build custom variables** if needed
6. **Export selection** as CSV or citations

## 🔧 API Configuration

### CrossRef API
- **No API key required** - completely free
- **Rate limit**: 50 requests per second
- **Base URL**: `https://api.crossref.org/v1/`
- **Coverage**: 100+ million journal articles
- **Docs**: https://github.com/CrossRef/rest-api-doc

**Why CrossRef?**
- Largest open metadata database for research
- No authentication required
- Excellent search functionality
- Reliable and well-maintained
- Perfect for discovering published research

## 📁 Project Structure

```
variable_hunt/
├── app.py                    # Main Streamlit application
├── config.py                # Configuration settings
├── utils.py                 # CrossRef search & citation utilities
├── citations.py             # Citation formatting (APA, Chicago, etc)
├── variable_database.py     # Pre-populated examples
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── .streamlit/
│   └── config.toml        # Streamlit UI configuration
├── README.md              # This file
└── LICENSE                # MIT License
```

## 💡 Example Usage

### Econometrics: Wage Inequality
```
Discipline: Econometrics
Dependent Variable: Wage Inequality

INDEPENDENT VARIABLES:
- Educational Attainment (human capital theory)
- Technical Skill Proficiency (skill-biased tech change)

COVARIATES:
- Labor Market Experience (learning-by-doing)
- Sector/Industry (productivity differences)

CONTROL VARIABLES:
- Age/Cohort (lifecycle effects)
- Gender (discrimination controls)
- Race/Ethnicity (racial inequality controls)
```

### Public Health: Cardiovascular Disease
```
Discipline: Public Health
Dependent Variable: Cardiovascular Disease

INDEPENDENT VARIABLES:
- Smoking Status (arterial damage mechanism)
- Hypertension (blood pressure effects)

COVARIATES:
- Physical Activity (cardiovascular function)
- Diet Quality (lipid profiles)

CONTROL VARIABLES:
- Age (strongest demographic risk factor)
- Biological Sex (gender-specific risks)
- Family History (genetic predisposition)
```

## 🎓 Supported Disciplines

### Econometrics
- Emphasis: Identification strategy, causal inference, endogeneity
- Key journals: Econometrica, Journal of Econometrics, Review of Economics and Statistics
- Variable focus: Causal mechanisms, instrumental variables, RDD

### Sociology
- Emphasis: Theoretical mechanisms, social structures, institutions
- Key journals: American Sociological Review, Sociology of Education, Social Forces
- Variable focus: Social capital, networks, institutional factors

### Public Health
- Emphasis: Confounders, health determinants, population effects
- Key journals: American Journal of Public Health, Epidemiology, Lancet
- Variable focus: Risk factors, determinants, prevention strategies

## 📖 Citation Formats

Export your selected variables and citations in multiple formats:

- **APA**: `Author (Year). Title. Journal. Volume(Issue), Pages.`
- **Chicago**: `Author. "Title." Journal Year, vol. X, no. Y: pp.`
- **Harvard**: `Author Year Title. Journal, Volume(Issue), pp.`
- **BibTeX**: `@article{key, author={}, year={}, ...}`

## 🔗 Useful Resources

- [CrossRef API Docs](https://github.com/CrossRef/rest-api-doc)
- [Econometrics Best Practices](https://www.aeaweb.org/)
- [SAGE Research Methods](https://methods.sagepub.com/)
- [Public Health Resources](https://www.cdc.gov/DataStatistics/)
- [Causal Inference Handbook](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)

## 📊 Pre-populated Examples

The database includes curated examples:
- **Econometrics**: Wage inequality variables with 9+ citations
- **Sociology**: Social capital variables with 5+ citations
- **Public Health**: Cardiovascular disease risk factors with 8+ citations

All examples from major peer-reviewed journals and leading research institutions.

## 🐛 Troubleshooting

**CrossRef search returns no results?**
- Try simpler keywords
- Add discipline-specific terms
- Check for typos in variable name

**Can't see pre-populated variables?**
- Ensure discipline and outcome are correctly selected
- Check if outcome is in the database (Wage Inequality, Social Capital, CVD)
- Refresh the page

**Installation fails with numpy error?**
- Delete venv folder: `rmdir /s venv`
- Create fresh: `py -m venv venv`
- Activate: `venv\Scripts\activate`
- Upgrade pip: `python -m pip install --upgrade pip setuptools wheel`
- Install: `pip install -r requirements.txt`

**Module not found errors?**
- Ensure virtual environment is activated (see `(venv)` at start of command line)
- Run: `pip install -r requirements.txt` again

## 🤝 Contributing

We welcome contributions!

- **Add variables**: Submit PRs with new variables and citations
- **Improve search**: Enhance CrossRef integration
- **New disciplines**: Add examples for other social science fields
- **Bug reports**: Open issues for any problems

## 📝 Citation

If you use Variable Hunt in your research:

```bibtex
@software{phanidhar_variable_hunt,
  author = {Phanidhar Upadhyaya},
  title = {Variable Hunt: Research Methodology Assistant for Quantitative Social Science},
  url = {https://github.com/phanidhar-u/variable_hunt},
  year = {2025}
}
```

## 📄 License

MIT License - See LICENSE file for full text

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/phanidhar-u/variable_hunt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/phanidhar-u/variable_hunt/discussions)
- **Email**: See GitHub profile

---

**Note**: This tool assists in literature review and variable selection. Always conduct thorough peer review and theoretical development alongside automated suggestions.

**Version**: 1.0.0  
**Last Updated**: June 2025  
**Python**: 3.8+  
**License**: MIT
