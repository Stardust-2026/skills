# DeepSeek search workflow

Use DeepSeek's [Search API](https://api-docs.deepseek.com/api/search/) as a discovery channel. The [official guide](https://api-docs.deepseek.com/guides/search/) documents date, language and domain filters. Use an existing `DEEPSEEK_API_KEY` supplied through the runtime's secret configuration and an environment that permits HTTPS to `api.deepseek.com`. Never request a pasted key in chat or store a key in the skill.

From the skill directory, run the helper with public topic queries only. Replace the example date with the applicable cutoff.

```bash
python3 scripts/deepseek_search.py --count 8 \
  'DeepSeek 模型 API 更新 lang:zh,en after:2026-11-06' \
  '通义千问 豆包 Kimi 智能体 发布 lang:zh after:2026-11-06'
```

Use targeted queries for China policy, energy storage and cross-border trade as well as apps. Begin with two to four queries and refine as needed. Results are discovery leads. Open original URLs, confirm event date and availability, and independently corroborate material claims. Send no private project names, documents, user identifiers, or API credentials in query text. If the API is unavailable, continue with standard web research. If the user supplies results from DeepSeek's web or app search, verify those URLs in the same way.
