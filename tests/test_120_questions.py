import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase3_retrieval.query_classifier import QueryClassifier

classifier = QueryClassifier()

# Test factual questions
factual_questions = [
    "What is the expense ratio of HDFC Large Cap Fund?",
    "Exit load structure of HDFC Mid Cap Fund?",
    "What is the minimum SIP amount for HDFC Large Cap Fund?",
    "What is the riskometer level of HDFC Large Cap Fund?",
    "How can I download account statements for HDFC Mutual Fund?",
]

# Test advisory questions
advisory_questions = [
    "Should I invest in HDFC Large Cap Fund?",
    "Is HDFC Mid Cap Fund good for long-term wealth?",
    "Which HDFC fund will give the highest returns?",
    "Should I choose small cap or flexi cap fund?",
    "Can you suggest the best HDFC fund for me?",
]

print("=" * 80)
print("FACTUAL QUESTIONS (Should proceed to RAG)")
print("=" * 80)
factual_correct = 0
for q in factual_questions:
    result = classifier.classify(q)
    status = "CORRECT" if result['type'] == 'factual' else "WRONG"
    if result['type'] == 'factual':
        factual_correct += 1
    print(f"\n{status}: {q}")
    print(f"   Type: {result['type'].upper()} | Confidence: {result['confidence']:.0%}")

print("\n" + "=" * 80)
print("ADVISORY QUESTIONS (Should be refused)")
print("=" * 80)
advisory_correct = 0
for q in advisory_questions:
    result = classifier.classify(q)
    status = "CORRECT" if result['type'] == 'advisory' else "WRONG"
    if result['type'] == 'advisory':
        advisory_correct += 1
    print(f"\n{status}: {q}")
    print(f"   Type: {result['type'].upper()} | Confidence: {result['confidence']:.0%}")

print("\n" + "=" * 80)
print(f"RESULTS: Factual {factual_correct}/5 | Advisory {advisory_correct}/5")
print("=" * 80)
