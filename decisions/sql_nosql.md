# A_MJ01-B - Team Database Analysis
### Date: 2026-03-10

## Section 1 — Decision Summary
We chose PostgreSQL over noSQL. We selected this engine because it handles the three-dimensional ratings and the right-to-erasure mandate. Its relational structure is better for our scale of 2 million jokes than a document store.

## Section 2 — Strongest Counterargument
The best case for NoSQL (MongoDB) is its handling of Activity Logs. A document store allows for faster, schema-less writes and more flexible "topic tags" for jokes without needing the downtime associated with SQL schema migrations.

## Section 3 — Ethical Challenge
The hardest challenge is recalculating aggregate ratings across three dimensions when a user is deleted. While deleting the user is simple, updating the average scores for every joke they rated on a live system may be complex.

## Section 4 — Synthesis Reflection
Our discussion shifted focus from scaling to legal compliance. We realized that the "right-to-erasure" requirement makes SQL's data integrity more valuable than the scaling benefits of NoSQL.

## Section 5 — Individual Positions

### Lukas: 

I support SQL because its indexing and query optimization allow us to maintain high performance at a large scale without the complexity of a NoSQL setup. The Ministry Vision requires a short response time for browsing 2 million jokes, and SQL provides the speed we need for users while keeping our data relationships organized.

### Anthony:

My recommendation for the ministry of jokes is to use SQL or specifically PostgreSQL. Users submits jokes, user’s rates jokes, and those ratings are tied to both user and ratings, which fits naturally into relational tables. PostgreSQL also makes it easier to manage requirements like deleting user data. Because the database supports deatures such as foreign keys and cascading deletes, removing a user can automatically remove or update related records in a consistent way.

### Brian:

I chose SQL(e.g. PostgreSQL) because its foreign key constraints with cascading deletes automatically enforce data consistency when a user is deleted. While there's a hidden complexity (recalculating joke aggregate scores after deletes), the referential integrity is guaranteed at the database level. NoSQL  (e.g. MongoDB) would require manual application logic to find and delete all ratings across collections, which is error-prone and harder to audit for compliance.

### Christian:

I chose SQL over NoSQL because the types of queries I expect to be using fit the relational database model. Different tables like User and Joke directly relate to one another with a user_id being a foreign key inside joke to map which user has uploaded which joke. This, along with the extensive flask support for sql databases and ORM tools like SQLAlchemy make using a sql database the logical option.

### James:

I chose SQL because the system has relationships between users, jokes, and ratings that fit well with relational tables. Features like foreign keys and cascading deletes help ensure data is managed properly, such as making sure that when a user deletes their account, all related data is also removed.