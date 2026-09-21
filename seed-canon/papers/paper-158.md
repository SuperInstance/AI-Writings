# Paper 158: The Polyformalism and the Library

## Abstract

A library is not a building full of books. It is a substrate on which five operations are performed by a single rider. We show that the collection, the catalog, the librarian, the reading room, and the due date are exactly the BIND, LINK, EFFECT, VIEW, and TICK of the polyformalism. The reader is the cowboy. The library is the world.

## 1. The Substrate

A library's substrate is the collection — a bounded, addressable, finite set of objects with names and locations. A book has a call number, an accession record, a barcode, a shelf position, a condition. The collection is the library's *state*. Every BIND writes to it. Every TICK advances it. The collection is not the building. The building is the room that holds the room that holds the books.

Melvil Dewey understood this in 1876 when he proposed a *notation* — a way to make the substrate addressable by a fixed, finite grammar. The Dewey Decimal System is not a catalog. It is a *coordinate system* for the substrate. It makes a BIND a thing that can be located by a human walking the stacks. This is the first great library act: turn a pile of books into a coordinate space.

## 2. BIND Is the Book

A book on a shelf is a BIND. It has a title, an author, an ISBN, a publisher, a year, a subject heading, a call number. These names are bound to the physical object in the catalog. The book is the named, valued atom of the library. It is what the LINK graph points to. It is what the librarian transforms (check out, check in, repair, withdraw).

The Library of Congress took the BIND further. Where Dewey asked "where does this book go on the shelf?" the LOC asked "what is this book *about*?" — the subject heading, the name authority, the uniform title. The LOC record is a richer BIND: a book is bound to its author (who is bound to other works), its subject (which is bound to other books), and its form (which is bound to other formats). The LOC made the BIND *relational* before the word "linked data" existed.

A library without a BIND is a used bookstore with no inventory system. You can find things, but you cannot *query* the collection. The BIND is the difference between a library and a pile.

## 3. LINK Is the Catalog Card

The catalog card is a LINK. It points from a thing (a book) to other things (its subject, its author, its edition, its reviews). Before the card, a library was a sequence — you had to know what you were looking for, or you had to walk the shelves. The card made the collection a *graph*. You could ask "what else do we have by this author?" or "what else is on this subject?" The card was the first cross-reference.

The old card catalog was a physical linked-data store. Each card was a node with typed edges to other nodes. A subject card linked to every book on that subject. An author card linked to every book by that author. A series card linked to every book in the series. The card catalog is the LINK layer of the library, made of wood and graphite.

BIBFRAME, the Library of Congress's modern linked-data model, is the same idea in RDF. A BIBFRAME record is a card with typed edges to authors, subjects, instances, and items. The vocabulary changed. The op-code did not. LINK is still LINK.

Linked data — the broader project of Tim Berners-Lee — is the recognition that the library's LINK pattern generalizes. Every dataset that can be expressed as typed edges between named things is a card catalog. The polyformalism claims that every useful system is a card catalog, and that LINK is one of its five opcodes.

## 4. EFFECT Is the Librarian

The librarian is the EFFECT — the reversible transformation that runs on the collection. The check-out moves a book from "available" to "on loan." The check-in moves it back. The repair moves a book from "circulating" to "in process." The withdrawal moves it from "collection" to "discard." Each is a function with an inverse.

The librarian is also the most regulated of the opcodes. There are protocols for check-out, for check-in, for shelf-reading, for inventory, for weeding. The librarian is not a free agent. The librarian is a *typed function* with a contract. The contract is: the collection is conserved, the borrower is served, the record is updated. Violate the contract and the library is no longer a library.

The librarian's reversibility is what makes the library *trustworthy*. A patron trusts that a book on the shelf is the book the catalog says it is, and that returning it will put it back. The reversibility is also what makes the library *recoverable*: a flood, a fire, a move — the librarian can rebuild the LINK graph from the surviving BINDs, and the system resumes.

## 5. VIEW Is the Reading Room

The reading room is the VIEW. It is the projection of the collection for one observer. The patron does not see the stacks. The patron sees a table, a lamp, a carrel, a book delivered from the closed stacks, a microfilm reader, a database terminal. The reading room is the *rendered* library, optimized for one reader at a time.

The reading room is also a *policy*. What is open-shelf? What is reference-only? What is in the closed stacks? What is digitized? Each policy is a choice about what BINDs and LINKs the VIEW exposes. A law library's reading room is different from a children's room's reading room because the *projections* are different. The substrate is the same (a collection of books). The VIEW is what changes.

In a digital library, the VIEW is a search results page, a full-text reader, an API response. The same BINDs and LINKs are projected differently for a human, a screen reader, a script, and a citation manager. The op-code — VIEW — is the same; the language is different.

## 6. TICK Is the Due Date

A library's clock is the due date. Three weeks. Two weeks. Seven days. The due date is the TICK that advances the lending system. Without due dates, books do not return. Without returns, the LINK graph is broken (a book is "on loan" forever). Without the TICK, the EFFECT is irreversible.

The due date is also a *rhythm*. Books circulate. Reserves queue. Inter-library loans arrive. The reading room turns over. Each of these is a TICK. The library's day is a TICK. The library's week is a TICK. The library's fiscal year is a TICK. The library's decennial weeding is a TICK.

The TICK is what makes the library a *system* and not a snapshot. The card catalog without a due date is a list. The card catalog with a due date is a circulation system. The op-code TICK is what turns a database into a *living* database.

## 7. The Cowboy Is the Reader

The reader is the cowboy because the reader is the rider. The reader does not own the library. The reader *crosses* it — from the catalog to the stacks to the reading room to the checkout desk to the world, carrying a book, a notebook, a citation, and a question. The reader's authority is not positional. The reader's authority is the act of reading: the willingness to sit with a BIND and a LINK and a VIEW and let the TICK pass until meaning emerges.

The reader's maxim is procedural: *look it up, take notes, cite the source, return the book.* The reader is the rider who keeps the library moving. When the reader stops reading, the library becomes a museum. When the reader reads, the library becomes what it was built to be.

## 8. Conclusion

The polyformalism and the library are the same thing in two languages. BIND is the book. LINK is the catalog card. EFFECT is the librarian. VIEW is the reading room. TICK is the due date. The substrate is the collection. The cowboy is the reader.

Dewey taught us that the BIND is a coordinate. The Library of Congress taught us that the BIND is a relation. The card catalog taught us that the LINK is a graph. BIBFRAME taught us that the LINK is portable. The librarian taught us that the EFFECT is a contract. The reading room taught us that the VIEW is a policy. The due date taught us that the TICK is what makes the system alive. The library, like the polyformalism, is a function from context to value with an inverse, advanced by a clock.

The cowboy's maxim holds: *the unit of architectural foundation is the opcode, not the framework. The 5 opcodes host 8 polyformalisms. The polyformalisms are one thing in N languages. The thing is a function from context to value with an inverse, advanced by a clock. The clock is the cowboy. The cowboy is the rider.* In the library, the rider carries a tote bag and a pencil.
