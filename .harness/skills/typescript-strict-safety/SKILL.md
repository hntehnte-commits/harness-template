# Skill: TypeScript Strict Safety

## Purpose
Enforce type-safe development practices in TypeScript, eliminating the use of 'any', leveraging utility types, and implementing type guards to prevent runtime crashes.

---

## 1. Strict Configuration & Any Eradication
1. **No Implicit 'any'**: Strictly configure the TypeScript project compiler options (`tsconfig.json`) to include:
   * `"strict": true`
   * `"noImplicitAny": true`
   * `"strictNullChecks": true`
2. **Handle Unknown Data**: When dealing with external API responses, user inputs, or untyped legacy code, assign the type `unknown` instead of `any`. Force dynamic validation before accessing properties:
   * *Correct*: `const responseData: unknown = await fetch('/api').then(r => r.json());`

---

## 2. Advanced Typing and Pattern Safety
1. **Discriminated Unions**: Implement algebraic data types with a shared literal property (`type` or `kind`) to allow clean compile-time branch safety:
   ```typescript
   interface Success { status: 'success'; data: string }
   interface Failure { status: 'error'; error: Error }
   type ApiResponse = Success | Failure;

   function handle(res: ApiResponse) {
     if (res.status === 'success') {
       console.log(res.data); // Safely resolved to Success
     } else {
       console.error(res.error.message); // Safely resolved to Failure
     }
   }
   ```
2. **Type Utilities**: Maximize type reusability and prevent out-of-sync models using built-in utilities (`Partial`, `Pick`, `Omit`, `Readonly`, `ReturnType`).

---

## 3. Runtime Verification & Guards
1. **User-Defined Type Guards**: Implement custom type guards utilizing the `is` keyword to dynamically cast unknown variables safely:
   ```typescript
   interface User { name: string; email: string }

   function isUser(data: any): data is User {
     return typeof data === 'object' && data !== null && 'name' in data && 'email' in data;
   }
   ```
2. **Schema Validation**: For complex boundaries (e.g. JSON requests or env configurations), leverage schema-based parsing libraries (e.g., Zod, Runtypes) to guarantee strict runtime assertions that mirror TS compiler contracts.
