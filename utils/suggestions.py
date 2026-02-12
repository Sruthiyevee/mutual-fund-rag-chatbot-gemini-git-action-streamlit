import random
from typing import List


class SuggestionsHandler:
    """
    Provides relevant clickable question suggestions based on context.
    Used when no answer is available or for advisory refusals.
    """
    
    def __init__(self):
        self.suggestion_bank = {
            'no_answer': [
                "What is the expense ratio of HDFC Midcap Fund?",
                "How do I download my capital gains statement?",
                "What is the lock-in period for ELSS funds?",
                "What is the minimum SIP amount for HDFC Flexi Cap Fund?",
                "What is the exit load for HDFC Small Cap Fund?",
                "What is the riskometer rating of HDFC Large Cap Fund?",
            ],
            'advisory_refusal': [
                "What is the expense ratio of HDFC Midcap Fund?",
                "What is the exit load for HDFC Small Cap Fund?",
                "How to download my account statement?",
                "What is the riskometer rating of HDFC Large Cap Fund?",
                "What is the minimum SIP amount?",
                "What is the lock-in period for ELSS funds?",
            ],
            'fund_specific': {
                'midcap': [
                    "What is the expense ratio of HDFC Midcap Fund?",
                    "What is the benchmark for HDFC Midcap Fund?",
                ],
                'elss': [
                    "What is the lock-in period for ELSS funds?",
                    "What is the tax benefit for ELSS investments?",
                ],
                'flexi_cap': [
                    "What is the minimum SIP amount for HDFC Flexi Cap Fund?",
                    "What is the expense ratio of HDFC Flexi Cap Fund?",
                ],
            }
        }
    
    def get_suggestions(self, context: str = 'no_answer', count: int = 2) -> List[str]:
        """
        Get suggested questions based on context.
        
        Args:
            context: 'no_answer', 'advisory_refusal', or fund name
            count: Number of suggestions to return (default 2)
            
        Returns:
            List of suggested question strings
        """
        if context in self.suggestion_bank:
            suggestions = self.suggestion_bank[context]
        elif context in self.suggestion_bank.get('fund_specific', {}):
            suggestions = self.suggestion_bank['fund_specific'][context]
        else:
            # Default to no_answer suggestions
            suggestions = self.suggestion_bank['no_answer']
        
        # Return random sample
        return random.sample(suggestions, min(count, len(suggestions)))
    
    def get_no_answer_suggestions(self, count: int = 2) -> List[str]:
        """Get suggestions for when no answer is available."""
        return self.get_suggestions('no_answer', count)
    
    def get_advisory_refusal_suggestions(self, count: int = 2) -> List[str]:
        """Get suggestions for advisory refusals."""
        return self.get_suggestions('advisory_refusal', count)


# Test
if __name__ == "__main__":
    handler = SuggestionsHandler()
    
    print("No Answer Suggestions:")
    print(handler.get_no_answer_suggestions())
    
    print("\nAdvisory Refusal Suggestions:")
    print(handler.get_advisory_refusal_suggestions())
