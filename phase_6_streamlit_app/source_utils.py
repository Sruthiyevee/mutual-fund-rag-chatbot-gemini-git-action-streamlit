def get_source_display_name(source_url: str) -> str:
    """
    Convert a source URL to a friendly display name.
    
    Examples:
    - KIM PDF → "HDFC Midcap Fund - KIM"
    - SID PDF → "HDFC Large Cap Fund - SID"
    - Factsheet → "HDFC Flexi Cap Fund - Factsheet"
    - Fund Page → "HDFC Small Cap Fund - Fund Page"
    """
    if not source_url:
        return "Source Document"
    
    # Extract document type from URL
    url_lower = source_url.lower()
    
    # Determine document type
    if 'kim' in url_lower:
        doc_type = "KIM"
    elif 'sid' in url_lower:
        doc_type = "SID"
    elif 'factsheet' in url_lower or 'fact' in url_lower:
        doc_type = "Factsheet"
    elif 'presentation' in url_lower:
        doc_type = "Presentation"
    elif 'hdfcfund.com/explore/mutual-funds' in url_lower:
        doc_type = "Fund Page"
    else:
        doc_type = "Document"
    
    # Extract fund name from URL
    fund_name = "HDFC Fund"
    if 'mid-cap' in url_lower or 'midcap' in url_lower:
        fund_name = "HDFC Mid Cap Fund"
    elif 'large-cap' in url_lower or 'large_cap' in url_lower:
        fund_name = "HDFC Large Cap Fund"
    elif 'small-cap' in url_lower or 'small_cap' in url_lower:
        fund_name = "HDFC Small Cap Fund"
    elif 'flexi-cap' in url_lower or 'flexi_cap' in url_lower:
        fund_name = "HDFC Flexi Cap Fund"
    elif 'multi-cap' in url_lower or 'multi_cap' in url_lower:
        fund_name = "HDFC Multi Cap Fund"
    
    return f"{fund_name} - {doc_type}"
