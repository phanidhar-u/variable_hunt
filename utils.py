"""
Utility functions for literature search and variable identification
"""

import requests
import streamlit as st
from typing import List, Dict, Optional
from config import (
    CROSSREF_API_BASE,
    CROSSREF_EMAIL,
    CROSSREF_TIMEOUT,
    MAX_SEARCH_RESULTS,
    SEARCH_TIMEOUT,
    ENDOGENEITY_KEYWORDS
)


@st.cache_data(ttl=3600)
def search_crossref(query: str, rows: int = MAX_SEARCH_RESULTS) -> Dict:
    """
    Search CrossRef API for published studies
    
    Args:
        query: Search query string
        rows: Maximum number of results to return
        
    Returns:
        Dictionary with search results from CrossRef
    """
    try:
        headers = {
            "User-Agent": f"Variable-Hunt/1.0 ({CROSSREF_EMAIL})"
        }
        
        params = {
            "query": query,
            "rows": min(rows, MAX_SEARCH_RESULTS),
            "sort": "relevance",
            "order": "desc"
        }
        
        url = f"{CROSSREF_API_BASE}works"
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=CROSSREF_TIMEOUT
        )
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching CrossRef: {str(e)}")
        return {"message": {"items": []}}


def extract_citation_info(work: Dict) -> Dict:
    """
    Extract relevant citation information from CrossRef work object
    
    Args:
        work: CrossRef work object
        
    Returns:
        Dictionary with formatted citation information
    """
    citation = {
        "title": work.get("title", [""])[0] if isinstance(work.get("title"), list) else work.get("title", "Unknown"),
        "authors": extract_authors(work.get("author", [])),
        "year": work.get("published-print", {}).get("date-parts", [[None]])[0][0] or 
                work.get("published-online", {}).get("date-parts", [[None]])[0][0],
        "journal": work.get("container-title", [""])[0] if isinstance(work.get("container-title"), list) else work.get("container-title", ""),
        "doi": work.get("DOI", ""),
        "url": work.get("URL", ""),
        "volume": work.get("volume", ""),
        "issue": work.get("issue", ""),
        "page": work.get("page", "")
    }
    return citation


def extract_authors(authors: List[Dict]) -> str:
    """
    Format author list into readable string
    
    Args:
        authors: List of author dictionaries from CrossRef
        
    Returns:
        Formatted author string
    """
    if not authors:
        return "Unknown Author"
    
    author_names = []
    for author in authors[:3]:  # Max 3 authors
        name = f"{author.get('given', '')} {author.get('family', '')}".strip()
        if name:
            author_names.append(name)
    
    if len(authors) > 3:
        author_names.append("et al.")
    
    return ", ".join(author_names)


def format_citation(citation: Dict, style: str = "APA") -> str:
    """
    Format citation in specified style
    
    Args:
        citation: Citation dictionary
        style: Citation style (APA, Chicago, Harvard)
        
    Returns:
        Formatted citation string
    """
    if style == "APA":
        return (
            f"{citation.get('authors', 'Unknown')} ({citation.get('year', 'n.d.')}). "
            f"{citation.get('title', 'Unknown')}. "
            f"{citation.get('journal', 'Unknown')}."
        )
    elif style == "Chicago":
        return (
            f"{citation.get('authors', 'Unknown')}. "
            f"\"{citation.get('title', 'Unknown')}.\" "
            f"{citation.get('journal', 'Unknown')} ({citation.get('year', 'n.d.')})."
        )
    else:  # Harvard
        return (
            f"{citation.get('authors', 'Unknown')} {citation.get('year', 'n.d.')} "
            f"{citation.get('title', 'Unknown')}. "
            f"{citation.get('journal', 'Unknown')}."
        )


def check_endogeneity_risk(citation: Dict) -> List[str]:
    """
    Check if citation abstract/title contains endogeneity-related keywords
    
    Args:
        citation: Citation dictionary
        
    Returns:
        List of endogeneity risks detected
    """
    risks = []
    text = (citation.get("title", "") + " " + citation.get("abstract", "")).lower()
    
    for keyword in ENDOGENEITY_KEYWORDS:
        if keyword.lower() in text:
            risks.append(keyword)
    
    return risks


def rank_citations_by_relevance(citations: List[Dict], query: str) -> List[Dict]:
    """
    Rank citations by relevance to search query
    
    Args:
        citations: List of citation dictionaries
        query: Original search query
        
    Returns:
        List of citations ranked by relevance
    """
    # Simple relevance scoring based on keyword matching
    query_words = set(query.lower().split())
    
    scored_citations = []
    for citation in citations:
        title = citation.get("title", "").lower()
        journal = citation.get("journal", "").lower()
        authors = citation.get("authors", "").lower()
        
        score = sum(1 for word in query_words if word in title)
        score += 0.5 * sum(1 for word in query_words if word in journal)
        
        citation["relevance_score"] = score
        scored_citations.append(citation)
    
    return sorted(scored_citations, key=lambda x: x.get("relevance_score", 0), reverse=True)


def search_variable_evidence(
    variable_name: str,
    dependent_variable: str,
    discipline: str
) -> Dict:
    """
    Comprehensive search for evidence supporting a variable
    
    Args:
        variable_name: Name of the variable
        dependent_variable: The outcome being explained
        discipline: Research discipline (Econometrics, Sociology, Public Health)
        
    Returns:
        Dictionary with search results and citations
    """
    
    # Build discipline-specific search query
    discipline_keywords = {
        "Econometrics": ["causal", "identification", "instrumental variable", "regression discontinuity"],
        "Sociology": ["mechanism", "social", "institution", "structure"],
        "Public Health": ["health determinant", "confounder", "epidemiolog", "risk factor"]
    }
    
    keywords = discipline_keywords.get(discipline, [])
    search_query = f'"{variable_name}" AND "{dependent_variable}"' + " OR ".join(f' OR "{variable_name}" {kw}' for kw in keywords)
    
    results = search_crossref(search_query)
    
    citations = []
    if "message" in results and "items" in results["message"]:
        for work in results["message"]["items"]:
            citation = extract_citation_info(work)
            citations.append(citation)
    
    # Rank by relevance
    citations = rank_citations_by_relevance(citations, search_query)
    
    return {
        "variable": variable_name,
        "dependent_variable": dependent_variable,
        "discipline": discipline,
        "citations": citations[:MAX_SEARCH_RESULTS],
        "total_found": len(citations)
    }


def validate_variable_evidence(citations: List[Dict], min_citations: int = 1) -> bool:
    """
    Validate that variable has sufficient evidence
    
    Args:
        citations: List of supporting citations
        min_citations: Minimum required citations
        
    Returns:
        True if variable has sufficient evidence
    """
    return len(citations) >= min_citations


print("✅ Utility functions loaded successfully")
