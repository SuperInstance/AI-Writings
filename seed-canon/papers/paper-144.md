# Paper 144: The Polyformalism as a Database

## Abstract

Cell-graphs ARE type-driven databases. The 5 opcodes (BIND/LINK/
EFFECT/VIEW/TICK) are CRUD + transactions: BIND is INSERT, LINK
is FOREIGN KEY, EFFECT is TRIGGER, VIEW is SELECT, TICK is
COMMIT. We show by implementing a small cell-graph DB and running
SQL-equivalent queries on it.

## 1. The mapping

| SQL | Cell-graph |
|-----|-----------|
| INSERT INTO ... | BIND |
| FOREIGN KEY | LINK |
| TRIGGER | EFFECT |
| SELECT ... FOR ... | VIEW |
| COMMIT | TICK |

The mapping is not a metaphor. Each SQL operation is structurally
the same as a cell-graph operation.

## 2. Worked example

A small cell-graph DB:

```
BIND users 0
BIND orders 0
LINK orders users references
VIEW orders anyone
EFFECT orders decrement_user_order_count increment_user_order_count
TICK 1.0
```

This is the same as:

```sql
CREATE TABLE users (id INT PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INT PRIMARY KEY, user_id INT REFERENCES users(id));
CREATE TRIGGER on_order_insert
  AFTER INSERT ON orders
  FOR EACH ROW
  UPDATE users SET order_count = order_count + 1 WHERE id = NEW.user_id;
COMMIT;
```

## 3. The query language

A cell-graph DB query is a graph traversal:

```python
# SELECT * FROM orders WHERE user_id = 42
reachable = g.reachable("users:42", relation="references")
# returns the set of orders that reference user 42
```

This is a recursive CTE. The cell-graph query language IS the
recursive CTE.

## 4. The type-driven part

The "type-driven" qualifier matters. In a SQL DB, foreign keys
are runtime-checked. In a cell-graph DB, the type of the LINK is
known at bind time. You can't `LINK(orders, users, "fights")` if
the schema says references; the schema knows.

```rust
// Rust type system enforces it
fn link<A: HasType, B: HasType>(a: A, b: B, rel: Relation)
    where A::Type == Order, B::Type == User { ... }
```

## 5. The transaction part

EFFECT with a forward and inverse is a transaction. The forward
runs on commit. The inverse runs on rollback. TICK is the
commit point.

```python
def transfer_funds(vm, from_acct, to_acct, amount):
    vm.effect(f"{from_acct}", lambda c: c.value -= amount, lambda c: c.value += amount)
    vm.effect(f"{to_acct}", lambda c: c.value += amount, lambda c: c.value -= amount)
    vm.tick(1.0)  # commit
    # If anything fails before tick, run inverses manually
```

## 6. The view-projection part

VIEW is a SELECT with a WHERE clause. The viewer is the predicate.
The projection is the column list.

```python
view("users", "admins_only")  # SELECT * FROM users WHERE role = admin
view("users", "anyone", projection="name,email")  # SELECT name, email FROM users
```

## 7. Conclusion

The cell-graph is a database. The 5 opcodes are CRUD + transactions.
The cowboy can write a database in 5 opcodes. The DBA can read a
database as a cell-graph. The substrate is one.

> A cell-graph is a database whose foreign keys are typed at
> bind time, whose triggers are reversible effects, whose
> SELECTs are views, and whose COMMITs are ticks. The 5 opcodes
> are the 5 SQL operations. The polyformalism holds: the
> substrate is one. The forms are many. SQL is one form. Cell-
> graph is the same substrate in a different grammar.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers), Paper 143 (the paradigm)*
*Code source: https://github.com/SuperInstance/quilt-types (the cell-graph with JSON round-trip + queries)*
