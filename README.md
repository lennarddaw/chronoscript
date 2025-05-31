# ⏳ Chronoscript

**Chronoscript** is a domain-specific language (DSL) for **time-based automation**, enabling intuitive scheduling, condition handling, and action execution in a human-readable format.

Whether you're automating system events, creating simulation flows, or building reactive systems — Chronoscript lets you describe **what happens, when, for how long, and under which conditions**.

---

## 🚀 Example

```chronoscript
loop every 2h if market_down(5%) {
    rebalance();
    log("Portfolio rebalanced.");
}
