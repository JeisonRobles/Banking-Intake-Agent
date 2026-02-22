from src.tools.policy_search import policy_search

if __name__ == "__main__":
    q = "When should the agent ask for customer ID and phone?"
    print(policy_search(q, top_k=4))