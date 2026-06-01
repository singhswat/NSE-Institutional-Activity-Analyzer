# Dashboard Placeholder

Recommended stack:

```bash
npx create-next-app@latest dashboard
```

Suggested pages:

- `/` - market overview
- `/accumulation` - top accumulation stocks
- `/distribution` - top distribution stocks
- `/stocks/[symbol]` - stock history and signal chart

Call FastAPI endpoints:

```text
GET http://localhost:8000/signals/latest
GET http://localhost:8000/signals/accumulation
GET http://localhost:8000/signals/distribution
```
