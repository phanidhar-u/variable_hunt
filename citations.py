"""
Citation management and formatting module
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class CitationStyle(Enum):
    """Supported citation styles"""
    APA = "APA"
    CHICAGO = "Chicago"
    HARVARD = "Harvard"
    BIBTEX = "BibTeX"


@dataclass
class Citation:
    """Citation data class"""
    authors: str
    year: int
    title: str
    journal: str
    doi: Optional[str] = None
    url: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    page: Optional[str] = None
    
    def __post_init__(self):
        """Validate citation data"""
        if not self.authors:
            self.authors = "Unknown Author"
        if not self.year:
            self.year = 2024
        if not self.title:
            self.title = "Untitled"
        if not self.journal:
            self.journal = "Unknown Journal"


class CitationManager:
    """Manages citation formatting and storage"""
    
    def __init__(self):
        self.citations: List[Citation] = []
    
    def add_citation(self, citation: Citation) -> None:
        """Add a citation to the manager"""
        self.citations.append(citation)
    
    def format_citation(
        self,
        citation: Citation,
        style: CitationStyle = CitationStyle.APA
    ) -> str:
        """
        Format a citation in the specified style
        
        Args:
            citation: Citation object
            style: Citation style to use
            
        Returns:
            Formatted citation string
        """
        if style == CitationStyle.APA:
            return self._format_apa(citation)
        elif style == CitationStyle.CHICAGO:
            return self._format_chicago(citation)
        elif style == CitationStyle.HARVARD:
            return self._format_harvard(citation)
        elif style == CitationStyle.BIBTEX:
            return self._format_bibtex(citation)
        else:
            return self._format_apa(citation)
    
    @staticmethod
    def _format_apa(citation: Citation) -> str:
        """APA format (Author, Year)"""
        base = f"{citation.authors} ({citation.year}). {citation.title}. {citation.journal}"
        
        if citation.volume:
            base += f", {citation.volume}"
            if citation.issue:
                base += f"({citation.issue})"
        
        if citation.page:
            base += f", {citation.page}"
        
        base += "."
        
        if citation.doi:
            base += f" https://doi.org/{citation.doi}"
        
        return base
    
    @staticmethod
    def _format_chicago(citation: Citation) -> str:
        """Chicago format"""
        base = f"{citation.authors}. \"{citation.title}.\" {citation.journal} {citation.year}"
        
        if citation.volume:
            base += f", vol. {citation.volume}"
            if citation.issue:
                base += f", no. {citation.issue}"
        
        if citation.page:
            base += f": {citation.page}"
        
        base += "."
        
        if citation.doi:
            base += f" https://doi.org/{citation.doi}"
        
        return base
    
    @staticmethod
    def _format_harvard(citation: Citation) -> str:
        """Harvard format"""
        base = f"{citation.authors}, {citation.year}. {citation.title}. {citation.journal}"
        
        if citation.volume:
            base += f", {citation.volume}"
            if citation.issue:
                base += f"({citation.issue})"
        
        if citation.page:
            base += f", pp.{citation.page}"
        
        base += "."
        
        if citation.doi:
            base += f" Available at: https://doi.org/{citation.doi}"
        
        return base
    
    @staticmethod
    def _format_bibtex(citation: Citation) -> str:
        """BibTeX format"""
        # Generate a key from author and year
        author_key = citation.authors.split()[0].lower() if citation.authors else "unknown"
        key = f"{author_key}{citation.year}"
        
        bibtex = f"@article{{{key},\n"
        bibtex += f"  author = {{{citation.authors}}},\n"
        bibtex += f"  year = {{{citation.year}}},\n"
        bibtex += f"  title = {{{citation.title}}},\n"
        bibtex += f"  journal = {{{citation.journal}}}"
        
        if citation.volume:
            bibtex += f",\n  volume = {{{citation.volume}}}"
        
        if citation.issue:
            bibtex += f",\n  number = {{{citation.issue}}}"
        
        if citation.page:
            bibtex += f",\n  pages = {{{citation.page}}}"
        
        if citation.doi:
            bibtex += f",\n  doi = {{{citation.doi}}}"
        
        if citation.url:
            bibtex += f",\n  url = {{{citation.url}}}"
        
        bibtex += "\n}"
        
        return bibtex
    
    def export_all_citations(
        self,
        style: CitationStyle = CitationStyle.APA
    ) -> str:
        """
        Export all citations in specified format
        
        Args:
            style: Citation style to use
            
        Returns:
            All citations formatted and separated by newlines
        """
        formatted = []
        for i, citation in enumerate(self.citations, 1):
            formatted.append(f"{i}. {self.format_citation(citation, style)}")
        
        return "\n\n".join(formatted)
    
    def to_dict(self) -> List[Dict]:
        """Convert all citations to dictionary format"""
        return [
            {
                "authors": c.authors,
                "year": c.year,
                "title": c.title,
                "journal": c.journal,
                "doi": c.doi,
                "url": c.url,
                "volume": c.volume,
                "issue": c.issue,
                "page": c.page
            }
            for c in self.citations
        ]


def create_citation_from_dict(data: Dict) -> Citation:
    """
    Create Citation object from dictionary
    
    Args:
        data: Dictionary with citation data
        
    Returns:
        Citation object
    """
    return Citation(
        authors=data.get("authors", "Unknown Author"),
        year=data.get("year", 2024),
        title=data.get("title", "Untitled"),
        journal=data.get("journal", "Unknown Journal"),
        doi=data.get("doi"),
        url=data.get("url"),
        volume=data.get("volume"),
        issue=data.get("issue"),
        page=data.get("page")
    )


print("✅ Citation management module loaded successfully")
