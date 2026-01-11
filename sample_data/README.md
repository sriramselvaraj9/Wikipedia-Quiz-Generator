# Sample Wikipedia URLs for Testing

This folder contains sample quiz outputs for various Wikipedia articles demonstrating the system's capabilities.

## Test URLs

1. **Alan Turing**
   - URL: https://en.wikipedia.org/wiki/Alan_Turing
   - File: alan_turing.json
   - Category: Biography
   - Complexity: Medium

2. **Artificial Intelligence**
   - URL: https://en.wikipedia.org/wiki/Artificial_intelligence
   - File: artificial_intelligence.json
   - Category: Technology
   - Complexity: High

3. **World War II**
   - URL: https://en.wikipedia.org/wiki/World_War_II
   - Category: History
   - Complexity: High

4. **Albert Einstein**
   - URL: https://en.wikipedia.org/wiki/Albert_Einstein
   - Category: Biography
   - Complexity: Medium

5. **Python (Programming Language)**
   - URL: https://en.wikipedia.org/wiki/Python_(programming_language)
   - Category: Technology
   - Complexity: Medium

## Additional Test URLs

- https://en.wikipedia.org/wiki/Machine_learning
- https://en.wikipedia.org/wiki/Isaac_Newton
- https://en.wikipedia.org/wiki/Ancient_Egypt
- https://en.wikipedia.org/wiki/Climate_change
- https://en.wikipedia.org/wiki/Bitcoin

## Sample Output Structure

Each JSON file contains:

```json
{
  "id": 1,
  "url": "Wikipedia article URL",
  "title": "Article title",
  "summary": "2-3 sentence summary",
  "key_entities": {
    "people": ["Person 1", "Person 2"],
    "organizations": ["Org 1", "Org 2"],
    "locations": ["Location 1", "Location 2"]
  },
  "sections": ["Section 1", "Section 2"],
  "quiz": [
    {
      "question": "Question text?",
      "options": ["A", "B", "C", "D"],
      "answer": "Correct option",
      "difficulty": "easy|medium|hard",
      "explanation": "Explanation referencing article content"
    }
  ],
  "related_topics": ["Topic 1", "Topic 2"],
  "created_at": "ISO 8601 timestamp"
}
```

## Testing Guidelines

1. **Diversity**: Test articles from different categories (biography, history, science, technology)
2. **Length**: Try both short and long articles
3. **Complexity**: Test simple and complex topics
4. **Edge Cases**: Articles with special characters, redirects, disambiguation pages

## Expected Performance

- Scraping time: 2-5 seconds
- Quiz generation time: 15-30 seconds
- Total time: ~20-35 seconds
- Question count: 8-10 questions
- Difficulty distribution: 30-40% easy, 30-40% medium, 20-30% hard
