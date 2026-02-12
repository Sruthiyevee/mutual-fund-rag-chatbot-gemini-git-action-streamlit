from typing import Dict, Any
import random


class RefusalHandler:
    """
    Handles polite refusals for advisory/opinion questions.
    Provides educational links and suggested factual questions.
    """
    
    def __init__(self):
        self.refusal_templates = {
            'investment_advice': {
                'message': "I can't help with investment opinions or recommendations.\n\nI can, however, share factual information from official sources.",
                'educational_link': 'https://www.amfiindia.com/investor-corner/knowledge-center'
            },
            'portfolio_advice': {
                'message': "I can't help with portfolio decisions.\n\nI can, however, share factual information from official sources.",
                'educational_link': 'https://www.amfiindia.com/investor-corner/knowledge-center/basics-of-mutual-funds'
            },
            'comparison': {
                'message': "I can't compare or recommend funds.\n\nI can, however, share factual information about individual funds from official sources.",
                'educational_link': 'https://www.amfiindia.com/investor-corner/knowledge-center/how-to-invest-in-mutual-funds'
            },
            'timing': {
                'message': "I can't advise on market timing or when to invest.\n\nI can, however, share factual information from official sources.",
                'educational_link': 'https://www.amfiindia.com/investor-corner/knowledge-center/understanding-risk-and-return'
            },
            'default': {
                'message': "I can only provide factual information from official sources, not investment advice.\n\nI can, however, help you with specific fund details.",
                'educational_link': 'https://www.amfiindia.com/investor-corner/knowledge-center'
            }
        }
        
        # Educational links database
        self.educational_links = {
            'investment_basics': 'https://www.amfiindia.com/investor-corner/knowledge-center/basics-of-mutual-funds',
            'how_to_invest': 'https://www.amfiindia.com/investor-corner/knowledge-center/how-to-invest-in-mutual-funds',
            'risk_return': 'https://www.amfiindia.com/investor-corner/knowledge-center/understanding-risk-and-return',
            'tax_implications': 'https://www.amfiindia.com/investor-corner/knowledge-center/tax-implications',
            'sebi_advisors': 'https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=34'
        }
    
    def get_refusal(self, query: str = None, classification: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get appropriate refusal message based on query type.
        
        Args:
            query: Original user query (optional)
            classification: Classification result from QueryClassifier (optional)
            
        Returns:
            {
                'message': str (refusal message),
                'educational_link': str (AMFI/SEBI link),
                'suggestions': list (2 factual questions)
            }
        """
        # Determine refusal type based on query content
        refusal_type = 'default'
        
        if query:
            query_lower = query.lower()
            if any(word in query_lower for word in ['recommend', 'suggest', 'best', 'better', 'which']):
                refusal_type = 'comparison'
            elif any(word in query_lower for word in ['portfolio', 'allocation', 'diversif']):
                refusal_type = 'portfolio_advice'
            elif any(word in query_lower for word in ['good time', 'right time', 'when to']):
                refusal_type = 'timing'
            elif any(word in query_lower for word in ['should i', 'advice', 'advise']):
                refusal_type = 'investment_advice'
        
        template = self.refusal_templates.get(refusal_type, self.refusal_templates['default'])
        
        return {
            'message': template['message'],
            'educational_link': template['educational_link'],
            'suggestions': self.get_factual_suggestions()
        }
    
    def get_factual_suggestions(self, count: int = 2) -> list:
        """
        Get suggested factual questions.
        
        Args:
            count: Number of suggestions to return
            
        Returns:
            List of suggested questions
        """
        suggestion_bank = [
            "What is the expense ratio of HDFC Midcap Fund?",
            "How do I download my capital gains statement?",
            "What is the lock-in period for ELSS funds?",
            "What is the minimum SIP amount for HDFC Flexi Cap Fund?",
            "What is the exit load for HDFC Small Cap Fund?",
            "What is the riskometer rating of HDFC Large Cap Fund?",
            "What is the benchmark for HDFC Multi Cap Fund?",
            "How to download my account statement?",
        ]
        
        return random.sample(suggestion_bank, min(count, len(suggestion_bank)))


# Test cases
if __name__ == "__main__":
    handler = RefusalHandler()
    
    test_queries = [
        "Should I buy HDFC Midcap Fund?",
        "Which fund is better?",
        "What's a good portfolio allocation?",
        "Is this a good time to invest?",
    ]
    
    print("Refusal Handler Test Results:")
    print("=" * 80)
    for query in test_queries:
        refusal = handler.get_refusal(query)
        print(f"\nQuery: {query}")
        print(f"Message: {refusal['message']}")
        print(f"Link: {refusal['educational_link']}")
        print(f"Suggestions: {refusal['suggestions']}")
