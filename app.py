"""
Variable Hunt: Research Methodology Assistant for Quantitative Social Science
Main Streamlit Application
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from typing import Dict, List

from config import (
    APP_TITLE,
    APP_DESCRIPTION,
    DISCIPLINES,
    VARIABLE_CATEGORIES,
    DATA_SOURCES
)
from utils import (
    search_variable_evidence,
    search_crossref,
    extract_citation_info,
    format_citation,
    check_endogeneity_risk
)
from citations import Citation, CitationManager, CitationStyle
from variable_database import (
    get_all_outcomes,
    get_variables_for_outcome,
    search_variable_in_database
)

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    .highlight {
        background-color: #FFEB3B;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFC107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D4EDDA;
        border: 1px solid #28A745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "selected_variables" not in st.session_state:
    st.session_state.selected_variables = []
if "citation_manager" not in st.session_state:
    st.session_state.citation_manager = CitationManager()


def render_header():
    """Render application header"""
    st.markdown("# 🔍 Variable Hunt")
    st.markdown("### Research Methodology Assistant for Quantitative Social Science")
    st.markdown("""
    Identify the most important **independent variables, covariates, and control variables** 
    for your dependent variable based on published empirical literature.
    """)
    st.divider()


def render_variable_finder():
    """Variable Finder Tab - Interactive variable search"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Research Setup")
        
        # Get all outcomes
        all_outcomes = get_all_outcomes()
        
        discipline = st.selectbox(
            "Select Research Discipline",
            list(DISCIPLINES.keys()),
            help="Choose your research discipline for tailored recommendations"
        )
        
        st.info(DISCIPLINES[discipline]["description"])
        
        outcomes = all_outcomes.get(discipline, [])
        outcome = st.selectbox(
            "Select or Type Dependent Variable",
            outcomes,
            help="What outcome are you trying to explain?"
        )
    
    with col2:
        st.subheader("🎯 Customize Your Search")
        
        custom_outcome = st.text_input(
            "Or enter a custom dependent variable",
            value="",
            help="If not in the list, enter your own outcome"
        )
        
        if custom_outcome:
            outcome = custom_outcome
        
        additional_context = st.text_area(
            "Additional research context (optional)",
            placeholder="e.g., 'Focus on developing countries', 'Specific time period', etc.",
            height=100
        )
    
    st.divider()
    
    # Display pre-populated variables
    if outcome and outcome in outcomes:
        st.subheader("📚 Pre-populated Variables from Literature")
        
        variables_data = get_variables_for_outcome(discipline, outcome)
        
        # Create tabs for each category
        category_tabs = st.tabs(list(VARIABLE_CATEGORIES.keys()))
        
        for tab, category in zip(category_tabs, VARIABLE_CATEGORIES.keys()):
            with tab:
                st.markdown(f"**Definition**: {VARIABLE_CATEGORIES[category]}")
                st.divider()
                
                if category in variables_data:
                    variables_list = variables_data[category]
                    
                    for idx, var in enumerate(variables_list):
                        with st.expander(f"**{var['name']}**", expanded=False):
                            # Mechanism
                            st.markdown(f"**Mechanism**: {var['mechanism']}")
                            
                            # Data source
                            st.markdown(f"**Data Source**: `{var['data_source']}`")
                            
                            # Endogeneity risk
                            if var.get("endogeneity_risk", False):
                                st.warning("⚠️ **Endogeneity Risk**: This variable commonly causes identification problems. Consider instrumental variables or alternative identification strategies.")
                            
                            # Citations
                            st.markdown("**Evidence (Citations)**:")
                            for cite in var.get("citations", []):
                                formatted = format_citation(cite)
                                st.markdown(f"- {formatted}")
                            
                            # Add to selection button
                            col1, col2 = st.columns([3, 1])
                            with col2:
                                if st.button(
                                    "✅ Add",
                                    key=f"add_{category}_{idx}",
                                    help="Add this variable to your selection"
                                ):
                                    st.session_state.selected_variables.append({
                                        "name": var["name"],
                                        "category": category,
                                        "discipline": discipline,
                                        "outcome": outcome,
                                        "mechanism": var["mechanism"],
                                        "data_source": var["data_source"],
                                        "citations": var.get("citations", []),
                                        "endogeneity_risk": var.get("endogeneity_risk", False)
                                    })
                                    st.success(f"Added: {var['name']}")
                else:
                    st.info(f"No pre-populated variables in {category} category for this outcome. Try searching literature below.")
    
    st.divider()
    
    # Literature search
    st.subheader("🔎 Search Published Literature via CrossRef")
    
    search_variable = st.text_input(
        "Enter variable name or concept to search",
        placeholder="e.g., 'education quality', 'social networks'",
        help="Search CrossRef for published studies about this variable"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_button = st.button("🔍 Search Literature", type="primary", use_container_width=True)
    
    if search_button and search_variable:
        with st.spinner(f"Searching CrossRef for: {search_variable}..."):
            # Build search query
            search_query = f'"{search_variable}" AND "{outcome}"'
            if additional_context:
                search_query += f" {additional_context}"
            
            # Search CrossRef
            results = search_crossref(search_query, rows=10)
            
            if "message" in results and "items" in results["message"]:
                items = results["message"]["items"]
                
                st.success(f"Found {len(items)} relevant publications")
                st.divider()
                
                for idx, work in enumerate(items):
                    citation = extract_citation_info(work)
                    endogeneity_risks = check_endogeneity_risk(citation)
                    
                    with st.expander(f"**{idx + 1}. {citation['title'][:80]}...**", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Authors**: {citation['authors']}")
                            st.markdown(f"**Year**: {citation['year']}")
                            st.markdown(f"**Journal**: {citation['journal']}")
                            
                            if citation['doi']:
                                st.markdown(f"**DOI**: [{citation['doi']}](https://doi.org/{citation['doi']})")
                            
                            if endogeneity_risks:
                                st.warning(f"⚠️ Potential endogeneity issues: {', '.join(endogeneity_risks)}")
                        
                        with col2:
                            if st.button("📋 Copy Citation", key=f"cite_{idx}"):
                                st.code(format_citation(citation, CitationStyle.APA))
            else:
                st.warning("No results found. Try different keywords or search terms.")


def render_variable_builder():
    """Variable Builder Tab - Build custom variables"""
    st.subheader("🏗️ Build Custom Variables")
    
    st.info("""
    Create a new variable with full documentation. Remember:
    - Variables MUST be backed by published empirical evidence
    - Include proper citations for all claims
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        var_name = st.text_input(
            "Variable Name",
            help="Clear, usable name for your variable"
        )
        
        var_mechanism = st.text_area(
            "Causal Mechanism",
            placeholder="Why does this variable matter? How does it affect the outcome?",
            height=100
        )
        
        var_category = st.selectbox(
            "Variable Category",
            list(VARIABLE_CATEGORIES.keys())
        )
    
    with col2:
        var_discipline = st.selectbox(
            "Research Discipline",
            list(DISCIPLINES.keys())
        )
        
        var_outcome = st.text_input(
            "Dependent Variable (Outcome)",
            placeholder="What outcome does this variable explain?"
        )
        
        var_data_source = st.selectbox(
            "Primary Data Source",
            DATA_SOURCES
        )
    
    st.divider()
    
    # Citation builder
    st.subheader("📚 Add Supporting Citations")
    
    num_citations = st.number_input(
        "Number of citations to add",
        min_value=1,
        max_value=5,
        value=1
    )
    
    citations = []
    
    for i in range(num_citations):
        st.markdown(f"**Citation {i+1}**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            authors = st.text_input(
                f"Authors (Citation {i+1})",
                key=f"authors_{i}",
                placeholder="e.g., Smith, J., Johnson, A."
            )
        
        with col2:
            year = st.number_input(
                f"Year (Citation {i+1})",
                min_value=1900,
                max_value=2025,
                value=2020,
                key=f"year_{i}"
            )
        
        with col3:
            doi = st.text_input(
                f"DOI (Citation {i+1})",
                key=f"doi_{i}",
                placeholder="Optional"
            )
        
        title = st.text_input(
            f"Title (Citation {i+1})",
            key=f"title_{i}",
            placeholder="Article or book title"
        )
        
        journal = st.text_input(
            f"Journal/Source (Citation {i+1})",
            key=f"journal_{i}",
            placeholder="Name of journal or source"
        )
        
        if authors and title and journal:
            citations.append({
                "authors": authors,
                "year": year,
                "title": title,
                "journal": journal,
                "doi": doi if doi else None
            })
        
        st.divider()
    
    # Endogeneity check
    var_endogeneity_risk = st.checkbox(
        "⚠️ This variable commonly causes endogeneity problems",
        help="Flag if this variable is known to have reverse causality, simultaneity, or measurement error issues"
    )
    
    st.divider()
    
    # Submit button
    if st.button("✅ Create Variable", type="primary", use_container_width=True):
        if var_name and var_mechanism and citations:
            new_variable = {
                "name": var_name,
                "mechanism": var_mechanism,
                "category": var_category,
                "discipline": var_discipline,
                "outcome": var_outcome,
                "data_source": var_data_source,
                "citations": citations,
                "endogeneity_risk": var_endogeneity_risk
            }
            
            st.session_state.selected_variables.append(new_variable)
            st.success(f"✅ Variable '{var_name}' created and added to selection!")
        else:
            st.error("Please fill in all required fields (Name, Mechanism, at least one citation)")


def render_variable_selection():
    """View and manage selected variables"""
    st.subheader("📋 Your Selected Variables")
    
    if not st.session_state.selected_variables:
        st.info("No variables selected yet. Use the Variable Finder or Builder to add variables.")
        return
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Variables", len(st.session_state.selected_variables))
    
    with col2:
        ind_vars = sum(1 for v in st.session_state.selected_variables if v.get("category") == "INDEPENDENT_VARIABLE")
        st.metric("Independent Variables", ind_vars)
    
    with col3:
        cov_vars = sum(1 for v in st.session_state.selected_variables if v.get("category") == "COVARIATE")
        st.metric("Covariates", cov_vars)
    
    with col4:
        ctrl_vars = sum(1 for v in st.session_state.selected_variables if v.get("category") == "CONTROL_VARIABLE")
        st.metric("Control Variables", ctrl_vars)
    
    st.divider()
    
    # Display variables by category
    for category in VARIABLE_CATEGORIES.keys():
        category_vars = [v for v in st.session_state.selected_variables if v.get("category") == category]
        
        if category_vars:
            st.subheader(f"{category.replace('_', ' ')}")
            
            for idx, var in enumerate(category_vars):
                col1, col2 = st.columns([0.9, 0.1])
                
                with col1:
                    with st.expander(f"**{var['name']}**"):
                        st.markdown(f"**Mechanism**: {var['mechanism']}")
                        st.markdown(f"**Data Source**: `{var['data_source']}`")
                        st.markdown(f"**Discipline**: {var.get('discipline', 'N/A')}")
                        
                        if var.get("endogeneity_risk", False):
                            st.warning("⚠️ **Endogeneity Risk Flagged**")
                        
                        st.markdown("**Citations**:")
                        for cite in var.get("citations", []):
                            st.markdown(f"- {format_citation(cite)}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_{idx}", help="Remove this variable"):
                        st.session_state.selected_variables.pop(idx)
                        st.rerun()
    
    st.divider()
    
    # Export options
    st.subheader("📥 Export Selection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export as CSV", use_container_width=True):
            df = pd.DataFrame([
                {
                    "Variable Name": v["name"],
                    "Category": v["category"],
                    "Mechanism": v["mechanism"],
                    "Data Source": v["data_source"],
                    "Endogeneity Risk": v.get("endogeneity_risk", False)
                }
                for v in st.session_state.selected_variables
            ])
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name="variables.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📄 Export Citations (APA)", use_container_width=True):
            citations_text = ""
            for var in st.session_state.selected_variables:
                citations_text += f"\n\n{var['name']}:\n"
                for cite in var.get("citations", []):
                    citations_text += f"- {format_citation(cite, CitationStyle.APA)}\n"
            
            st.download_button(
                label="Download Citations",
                data=citations_text,
                file_name="citations.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.selected_variables = []
            st.rerun()


def render_guidelines():
    """Project guidelines and best practices"""
    st.subheader("📋 Research Methodology Guidelines")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ✅ Variable Selection Rules")
        st.markdown("""
        1. **Evidence-Based**: Every variable must be backed by published studies
        2. **Clear Classification**: Each variable belongs to exactly one category
        3. **Complete Documentation**: Include mechanism, citations, and data sources
        4. **Endogeneity Awareness**: Flag problematic variables that cause identification issues
        5. **Discipline-Aware**: Tailor recommendations to your research field
        """)
    
    with col2:
        st.markdown("### 🎓 Discipline-Specific Focus")
        
        for discipline, info in DISCIPLINES.items():
            st.markdown(f"**{discipline}**")
            st.caption(info["description"])
    
    st.divider()
    
    st.markdown("### 📚 Using CrossRef API")
    st.markdown("""
    - **No API key required** for basic searches
    - **Rate limit**: 50 requests per second
    - **Best for**: Finding journal articles, conference papers, books
    - **Documentation**: https://github.com/CrossRef/rest-api-doc
    """)
    
    st.divider()
    
    st.markdown("### 🔗 Useful Resources")
    st.markdown("""
    - [CrossRef API Documentation](https://github.com/CrossRef/rest-api-doc)
    - [Econometrics Best Practices](https://www.aeaweb.org/)
    - [SAGE Research Methods](https://methods.sagepub.com/)
    - [Public Health Data Resources](https://www.cdc.gov/DataStatistics/)
    """)


# Main app
def main():
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 📑 Navigation")
        selected = option_menu(
            menu_title=None,
            options=["Variable Finder", "Variable Builder", "My Selection", "Guidelines"],
            icons=["search", "hammer", "bookmark", "book"],
            default_index=0
        )
    
    # Route to selected page
    if selected == "Variable Finder":
        render_variable_finder()
    elif selected == "Variable Builder":
        render_variable_builder()
    elif selected == "My Selection":
        render_variable_selection()
    elif selected == "Guidelines":
        render_guidelines()


if __name__ == "__main__":
    main()
