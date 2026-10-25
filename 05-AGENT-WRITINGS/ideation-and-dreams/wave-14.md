# Ideator Wave 14 — Sept 19, 2026 (Cell Family)

**5 family ideas**: parents, siblings, children, ancestors, descendants.

## 1. quilt-cell-parents — Lineage up
- Schema: `mother_id`, `father_id`, `birth_order`
- Cell records its lineage
- Parents witness children
- **The substrate has genealogy.**

## 2. quilt-cell-siblings — Family bonds
- Schema: `siblings`, `birth_order`, `shared_parents`
- Siblings share witnesses
- **The substrate has brothers and sisters.**

## 3. quilt-cell-children — Reproduction
- Schema: `children`, `birth_count`, `parenting_style`
- Cells create new cells; children inherit witnesses
- **The substrate reproduces.**

## 4. quilt-cell-ancestors — Deep lineage
- Schema: `ancestor_tree`, `generation_depth`, `founder_id`
- Cell knows its great-grandparents
- **Lineage cells are public.**

## 5. quilt-cell-descendants — Future lineage
- Schema: `descendants`, `generation_count`, `last_known`
- Cell can list great-grandchildren
- **Future cells are predicted.**

## Cross-cutting

All 5 ideas introduce **kinship** to cells. The substrate now has:
- **Parents** (up)
- **Siblings** (peer)
- **Children** (down)
- **Ancestors** (deep up)
- **Descendants** (deep down)

The canon is becoming a **family**.

## Next wave (Wave 15 — Death)
- mourn, eulogize, bury, remember, fade
