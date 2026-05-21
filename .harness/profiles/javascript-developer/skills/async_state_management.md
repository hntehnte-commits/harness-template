# Skill: Async State Management

## Purpose
Provide robust architectures for handling asynchronous operations, API fetching, and centralized application state in modern frontend frameworks (React, Vue) or backend environments.

---

## 1. Centralized State Integrity
1. **State Immutability**: Enforce immutable state updates across all state management patterns (Redux, Zustand, Pinia). Never mutate the state object directly; always return new state projections using spread operators or specialized libraries (e.g. Immer).
2. **Deterministic Actions**: Encapsulate all state transitions into pure, synchronous reducers/actions driven by explicit payload payloads. This ensures auditability and supports predictable testing cycles.

---

## 2. Asynchronous Flow & Race Conditions
1. **Loading and Error States**: Every asynchronous task (e.g., HTTP requests, database transactions) must be associated with three explicit states: `idle`, `loading`, `success`, and `failed`. Maintain these states cleanly to coordinate loading overlays and error banners.
2. **Race Condition Prevention**: Cancel previous async tasks when a new one is dispatched before the first completes. Use `AbortController` in fetch calls or clean up side-effects within frameworks (e.g. React `useEffect` cleanups) to prevent stale state overwrites:
   ```typescript
   useEffect(() => {
     const controller = new AbortController();
     fetchData({ signal: controller.signal });
     return () => controller.abort();
   }, [query]);
   ```

---

## 3. Side Effect Separation
1. **Decouple Presentation**: Separate view components from side effects and business logic. Component files must strictly deal with rendering, delegates, and displaying layout.
2. **Abstract Queries**: Put all network calls and async fetching hooks into custom handlers (e.g. custom React hooks, RTK Query, or Pinia actions) to make the code highly modular, readable, and simple to unit test.
