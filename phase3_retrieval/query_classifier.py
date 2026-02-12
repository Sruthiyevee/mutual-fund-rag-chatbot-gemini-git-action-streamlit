import re
from typing import Dict, Any


class QueryClassifier:
    """
    Classifies user queries as 'advisory' or 'factual'.
    Advisory queries are investment advice/recommendations.
    Factual queries are information requests about fund details.
    """
    
    def __init__(self):
        # Advisory patterns - trigger refusal
        self.advisory_patterns = [
            r'\b(should i|shall i|can i|would you recommend)\b',
            r'\b(recommend|suggestion|suggest|advice|advise)\b.*\bfund\b',
            r'\b(best fund|better fund|which fund|what fund should)\b',
            r'\b(buy|sell|invest in|switch to|move to)\b.*\bfund\b',
            r'\b(good time|right time|when to)\b.*\b(invest|buy|sell)\b',
            r'\b(portfolio|allocation|diversif)\b',
            r'\bis .* better than\b',
            r'\bshould i (buy|sell|invest|switch)\b',
            r'\b(worth investing|good investment)\b',
            r'\b(compare|comparison)\b.*\bfund',
            r'\b(good for|suitable for|right for)\b.*\b(me|my|long.?term|wealth|retirement)\b',
            r'\b(highest|maximum|best) (return|profit|gain)',
            r'\b(will (give|provide|generate))\b.*\b(return|profit)',
            r'\b(safer|riskier|risky to invest)\b',
            r'\b(perform better|outperform|beat)\b',
        ]
        
        # Factual keywords - proceed to RAG
        self.factual_keywords = [
            'expense ratio', 'exit load', 'minimum sip', 'lock-in', 'lock in',
            'elss', 'riskometer', 'benchmark', 'download statement',
            'nav', 'aum', 'fund manager', 'investment objective',
            'asset allocation', 'portfolio holdings', 'top holdings',
            'what is', 'how to', 'when does', 'where can i',
            'how do i', 'how can i', 'tell me about', 'explain',
            'factsheet', 'scheme information', 'fund details',
            'capital gains', 'dividend', 'returns', 'performance'
        ]
        
        # Compile regex patterns for efficiency
        self.advisory_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.advisory_patterns]
    
    def classify(self, query: str) -> Dict[str, Any]:
        """
        Classify a query as advisory or factual.
        
        Args:
            query: User's question string
            
        Returns:
            {
                'type': 'advisory' | 'factual',
                'confidence': float (0-1),
                'reason': str (explanation)
            }
        """
        query_lower = query.lower().strip()
        
        # Exclude operational/factual queries that might match advisory patterns
        operational_keywords = [
            'download', 'access', 'get', 'find', 'where', 'how to', 'how do i',
            'how can i', 'steps to', 'guide', 'instructions', 'process'
        ]
        is_operational = any(keyword in query_lower for keyword in operational_keywords)
        
        # Check for advisory patterns
        advisory_matches = []
        for pattern in self.advisory_regex:
            if pattern.search(query_lower):
                advisory_matches.append(pattern.pattern)
        
        if advisory_matches and not is_operational:
            return {
                'type': 'advisory',
                'confidence': 0.9,
                'reason': f"Detected advisory pattern: {advisory_matches[0]}"
            }
        
        # Check for factual keywords
        factual_score = 0
        for keyword in self.factual_keywords:
            if keyword in query_lower:
                factual_score += 1
        
        if factual_score > 0:
            return {
                'type': 'factual',
                'confidence': min(0.9, 0.5 + (factual_score * 0.1)),
                'reason': f"Contains {factual_score} factual keyword(s)"
            }
        
        # Default to factual (let RAG handle it)
        # If no answer is found, the system will show suggestions
        return {
            'type': 'factual',
            'confidence': 0.5,
            'reason': "No strong indicators, defaulting to factual"
        }
    
    def is_advisory(self, query: str) -> bool:
        """Quick check if query is advisory."""
        return self.classify(query)['type'] == 'advisory'
    
    def is_factual(self, query: str) -> bool:
        """Quick check if query is factual."""
        return self.classify(query)['type'] == 'factual'


# Test cases
if __name__ == "__main__":
    classifier = QueryClassifier()
    
    test_queries = [
        # Advisory (should be refused)
        "Should I buy HDFC Midcap Fund?",
        "Which fund is better for me?",
        "Is this a good time to invest?",
        "Can you recommend a fund?",
        "Should I switch from Fund A to Fund B?",
        
        # Factual (should proceed to RAG)
        "What is the expense ratio of HDFC Midcap Fund?",
        "How do I download my capital gains statement?",
        "What is the lock-in period for ELSS funds?",
        "Tell me about HDFC Small Cap Fund",
        "What is the minimum SIP amount?",
    ]
    
    print("Query Classification Test Results:")
    print("=" * 80)
    for query in test_queries:
        result = classifier.classify(query)
        print(f"\nQuery: {query}")
        print(f"Type: {result['type'].upper()}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reason: {result['reason']}")
