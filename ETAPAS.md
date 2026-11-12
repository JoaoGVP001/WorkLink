# Worklink — four stages for the group review

The code was organized into four stages so the group can review the decisions in order. The reviewer for each stage should run the commands in the README after receiving the project and check that the behavior matches the UML and report.

## Stage 1 — Domain model and POO foundations

**Files:** `enums.py`, `models.py`

This stage defines the account roles and application/vacancy states, the abstract `User` class, the three user profiles, `ProfessionalProfile`, `Company`, `Vacancy` and `Application`.

**Review together:** Are the class and method names understandable? Do the properties protect internal fields? Does each child class return different permissions? Are company, vacancy and application references represented on both sides of the relationships?

## Stage 2 — In-memory service

**File:** `services.py`

This stage creates the first administrator, registers candidates and privileged accounts, stores companies and users, links recruiters to companies, and lists open vacancies. Data lasts only while the program is running.

**Review together:** Does the service avoid duplicating the rules already held by the model classes? Does an admin operation require an active administrator?

## Stage 3 — Console demonstration

**File:** `main.py`

This stage creates sample objects, connects them, prints the different permissions, creates an application, changes its status and shows that a duplicate application is blocked.

**Review together:** Can someone unfamiliar with the code follow the scenario from the output? Does the demonstration show real interaction between the objects?

## Stage 4 — Tests, README and final review

**Files:** `tests/test_rules.py`, `README.md`, `ETAPAS.md`

This stage records the expected behavior as tests and explains how to run and present the project.

From this folder:

```bash
python main.py
python -m unittest discover -s tests -v
```

**Review together:** Do tests include accepted and rejected operations? Can every group member explain one rule and one POO concept? Are the repository and README ready for the Classroom submission?
