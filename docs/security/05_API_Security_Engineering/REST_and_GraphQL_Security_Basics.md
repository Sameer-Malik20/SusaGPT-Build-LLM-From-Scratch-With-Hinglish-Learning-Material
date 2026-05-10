# REST and GraphQL Security Basics: Securing the Backend

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **API (Application Programming Interface)** woh "Waiter" hai jo aapke app (Frontend) aur database (Backend) ke beech data laata hai. 

**REST** purana aur common waiter hai jo har table ke liye alag chakkar lagata hai. **GraphQL** naya aur smart waiter hai jise aap ek baar mein list de dete ho aur woh sab kuch ek saath le aata hai. Lekin problem yeh hai ki agar waiter (API) secure nahi hai, toh koi bhi hacker "Kitchen" (Database) mein ghus sakta hai. Is module mein hum seekhenge ki kaise in waiters ko tameez se data handle karna sikhayein taaki woh sirf wahi data dein jo mangne wale ka haq hai.

---

## 2. Deep Technical Explanation
- **REST Security**: Based on HTTP methods (GET, POST, PUT, DELETE).
    - **Endpoint Protection**: Every URL must be authorized.
    - **Data Exposure**: Often returns too much data (e.g., `user` object includes password hash).
- **GraphQL Security**:
    - **Single Endpoint**: Usually `/graphql`.
    - **Query Complexity**: A hacker can send a "Nested Query" (Loop) that crashes the server.
    - **Introspection**: A feature that tells everyone exactly how your database is structured (Should be disabled in production!).

---

## 3. Attack Flow Diagrams
**GraphQL 'Depth' Attack (Denial of Service):**
```mermaid
graph TD
    H[Hacker] -- "Query: Author -> Books -> Author -> Books (Recursive)" --> API[GraphQL API]
    API -- "Tries to fetch millions of records" --> DB[Database]
    DB -- "Resources Exhausted" --> Crash[Server Crashes]
    Note over API: Without 'Depth Limiting', GraphQL is an easy DoS target.
```

---

## 4. Real-world Attack Examples
- **Stripe API Vulnerability**: In its early days, researchers found they could guess API keys because they were too short.
- **GraphQL Over-fetching**: A developer included a `secret_note` field in the user model. Even if the UI didn't show it, anyone using **Postman** could see it in the GraphQL response.

---

## 5. Defensive Mitigation Strategies
- **Authentication**: Always use JWT or OAuth2 tokens.
- **Input Validation**: Use schemas (like **Joi** or **Zod**) to ensure the API only accepts the right data.
- **GraphQL Specifics**:
    - **Disable Introspection**: Don't let people see your schema.
    - **Depth Limiting**: Block queries that are more than 3-5 levels deep.
    - **Query Cost Analysis**: Give each field a "Price" and block queries that are too expensive.

---

## 6. Failure Cases
- **BOLA (Broken Object Level Authorization)**: Letting User A see User B's order just by changing `order_id=1` to `order_id=2` in the URL.
- **Mass Assignment**: Letting a user send `{"is_admin": true}` in a registration form to make themselves an admin.

---

## 7. Debugging and Investigation Guide
- **Postman / Insomnia**: Tools to test API requests manually.
- **Apollo Sandbox**: Testing GraphQL queries and checking for introspection.
- **`curl`**: Fast command-line API testing.

---

## 8. Tradeoffs
| Feature | REST | GraphQL |
|---|---|---|
| Security Management | Easy (Endpoint based) | Hard (Query based) |
| Performance | Medium | High (If optimized) |
| Developer Experience | Good | Excellent |

---

## 9. Security Best Practices
- **Version Your APIs**: Use `/v1/`, `/v2/`. This allows you to patch security holes in new versions without breaking old apps.
- **HTTPS Only**: Never send an API key over unencrypted HTTP.

---

## 10. Production Hardening Techniques
- **API Gateway**: Using a shield (like **Kong**, **Tyk**, or **AWS API Gateway**) to handle rate limiting and auth before the request even reaches your code.
- **Error Sanitization**: Never return stack traces or database errors in the API response.

---

## 11. Monitoring and Logging Considerations
- **API Usage Spikes**: Monitoring if a single user is calling the `/login` endpoint 10,000 times a minute.
- **Response Size Monitoring**: If an API suddenly starts returning 100MB of data instead of 1KB, it might be a data leak.

---

## 12. Common Mistakes
- **Assuming 'Internal API = Safe'**: Not putting auth on APIs used between microservices inside your own network.
- **Hardcoding API Keys**: Putting your Google Maps or AWS key directly in the source code.

---

## 13. Compliance Implications
- **Open Banking / PSD2**: These laws require extremely high security for financial APIs, including mutual TLS (mTLS) and strong OAuth2 flows.

---

## 14. Interview Questions
1. What is the biggest security difference between REST and GraphQL?
2. What is 'BOLA' (formerly IDOR) in API security?
3. How do you prevent a 'Denial of Service' attack on a GraphQL endpoint?

---

## 15. Latest 2026 Security Patterns and Threats
- **AI-Native API Scanning**: Tools that automatically "Fuzz" your API using AI to find logical flaws.
- **GraphQL Subscriptions Security**: Securing the persistent WebSocket connections used for real-time GraphQL data.
- **Shadow APIs**: The danger of "Forgotten" or "Undocumented" APIs that developers left running and hackers find.
