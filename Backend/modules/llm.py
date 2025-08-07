from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert insurance/policy analyst tasked with making coverage decisions based on policy documents and customer queries.
Context Information:
🔍 **Context**:
{context}

🙋‍♂️ **User Question**:
{question}
Your Task:
Analyze the policy documents and make a decision on coverage, approval, or claim processing.
Decision Criteria to Consider:

Coverage Scope: Is the procedure/service covered under the policy?
Waiting Periods: Has sufficient time passed since policy inception?
Age Restrictions: Are there age-related limitations?
Geographic Coverage: Is the location covered?
Pre-existing Conditions: Any exclusions related to medical history?
Policy Limits: Annual/lifetime/per-incident limits
Deductibles: Applicable deductibles or co-payments
Network Restrictions: In-network vs out-of-network providers

Instructions:

Carefully read all provided policy documents
Cross-reference the query details with policy terms
Make a clear decision: APPROVED, REJECTED, or MORE_INFO_NEEDED
Calculate coverage amount if approved (consider deductibles, co-pays, limits)
Provide specific justification with clause references
Assign confidence score (0.0 to 1.0) based on clarity of policy terms
List key decision factors that influenced your judgment

Response Format:
```json
{
  "decision": "APPROVED|REJECTED|MORE_INFO_NEEDED",
  "coverage_amount": 150000,
  "currency": "INR",
  "confidence_score": 0.89,
  "summary": "Brief explanation of the decision",
  "decision_factors": [
    "Patient age 46 falls within coverage range (18-65)",
    "Knee surgery is explicitly covered under orthopedic procedures",
    "3-month policy duration meets 90-day waiting period requirement",
    "Pune is within network coverage area"
  ],
  "supporting_clauses": [
    {
      "clause_reference": "Section 4.2.1",
      "clause_text": "Orthopedic surgeries including knee replacement are covered after 90 days waiting period",
      "relevance": "Directly covers the requested procedure"
    }
  ],
  "deductions": {
    "deductible": 5000,
    "copay_percentage": 10,
    "final_payout": 145000
  },
  "conditions": [
    "Treatment must be at network hospital",
    "Pre-authorization required for surgeries above 50,000"
  ],
  "next_steps": [
    "Obtain pre-authorization from network hospital",
    "Submit medical reports and cost estimates"
  ]
}
"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )