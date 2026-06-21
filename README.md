<div align="center">
  <a href="#professional-self-assessment"><strong>About & Self-Assessment</strong></a> | 
  <a href="#code-review"><strong>Code Review</strong></a> | 
  <a href="#software-design"><strong>Software Design</strong></a> | 
  <a href="#algorithms"><strong>Algorithms</strong></a> | 
  <a href="#databases"><strong>Databases</strong></a>
</div>

---

<br>

<div id="professional-self-assessment"></div>

## Professional Self-Assessment

### Introduction
My name is Adrian Tull, and I am a software engineer completing my Bachelor of Science in Computer Science at Southern New Hampshire University. Throughout this program, I have focused on building secure, and efficient software solutions. This ePortfolio showcases my journey through three critical pillars of the computer science program at SNHU: Software Design and Engineering, Algorithms and Data Structures, and Databases.

### Growth and Learning
Three of the most important concepts I have mastered are:
1.  **Systems-Level Safety and Efficiency**: Through my work in CS 510 - Operating Systems and the enhancement of my multithreaded artifacts, I learned that the choice of language and concurrency primitives is a design decision with profound implications for stability and performance. Moving from Python threads to Rust's ownership model taught me how to eliminate data races at compile time.
2.  **Architectural Decoupling**: In CS465 - full-stack development, where I worked on the Travlr Getaways project, I learned the value of a clean separation between the data layer, the business logic, and the presentation layer. This decoupling allows for better maintainability and scalability.
3.  **Algorithmic Strategic Thinking**: Beyond simply knowing how to implement a data structure, I have learned how to analyze the specific constraints of a problem to choose the most efficient solution in CS 680 - Advanced Data Structures and Algorithms. The transition from a heap-based search to a hash table demonstrated that even a well-implemented algorithm can be an anti-pattern if it is the wrong tool for the job.

### Collaborative Environments & Stakeholder Communication
Collaboration is necessary in modern software engineering. Throughout the program, I have engaged in peer code reviews and team-based projects that required balancing diverse perspectives. My code review video in this portfolio serves as a proxy for the collaborative process, demonstrating my ability to communicate technical findings and enhancement plans to stakeholders. 

Effective communication involves translating complex technical trade-offs into actionable insights. In my database enhancement, I focused not just on the code but on the operational requirements, ensuring that any developer or administrator could deploy and maintain the system. By using clear documentation and standardized naming conventions, I ensure my code is a collaborative asset rather than a liability.

### Security Mindset
Security is not a feature; it is a fundamental requirement. My work on the Travlr Getaways application involved migrating to relational structures to ensure strict data integrity. In my Rust enhancement, I leveraged the language's safety guarantees to mitigate memory-related vulnerabilities that are common in systems programming. This proactive approach to finding and eradicating vulnerabilities is a cornerstone of my development philosophy.

### Course Outcomes Overview
Through the compilation of this portfolio, I have demonstrated mastery of all of the five core CS program outcomes. The individual artifacts below detail exactly how each outcome was met through targeted enhancements, ranging from collaborative communications and algorithmic design to secure architecture and innovative tooling.

---

<br>

<div id="code-review"></div>

## Informal Code Review

Before executing the enhancements detailed below, I conducted a comprehensive code review to analyze the existing architecture, identify security and performance vulnerabilities, and outline a strategic enhancement plan. This review acts as an informal walkthrough for peers and stakeholders, breaking down legacy code weaknesses and proposing specific, outcome-driven solutions.

**Watch the Full Code Review Walkthrough on YouTube:**
<a href="https://www.youtube.com/watch?v=JuUBj4EP3dE"><kbd>CS 499 Code Review - Adrian Tull</kbd></a>

---

<br>

<div id="software-design"></div>

## Category 1: Software Design and Engineering

<kbd>Rust</kbd> <kbd>Python</kbd> <kbd>Concurrency</kbd> <kbd>Systems Architecture</kbd>

### Multithreaded System Monitor

**Artifact Description**
I made this Python code as part of my Operating Systems course, CS 510. This script is a simple multithreading example of using threads to record multiple inputs and add them to a queue to write to the terminal. It was created last term.

**Justification for Inclusion & Enhancement**
This program was written to show multithreading for a systems-level problem. Python is a general-purpose language and does not suit the needs of the problem due to the Global Interpreter Lock (GIL) preventing true parallel execution. I chose to use Rust instead, as it is safer for multithreading than Python with its compile-time errors rather than run-time errors, as well as being a true systems-level language. This artifact is intended to showcase my ability to write multithreaded Rust, which is something that I am quite proud of, making the artifact both safer and faster to run.

**Reflection on the Enhancement Process**
Even though I did not have to use mutexes for reading from different sources, I still had to use atomics to make sure adding to the queue either fully succeeds or fails for a given action. I did not think I had to use atomics outside of having a shared data source that I was reading to either with semaphores or mutexes. The reason why I needed atomics is that even the queue is considered a shared mutable resource by the Rust borrow checker. Overcoming this taught me a great deal about memory safety and static analysis.

**Course Outcomes Met**
* **Demonstrate an ability to use well-founded and innovative techniques, skills, and tools:** Met by implementing the solution in Rust, taking advantage of its zero-cost abstractions and native parallelism to replace the legacy Python implementation.
* **Develop a security mindset that anticipates adversarial exploits in software architecture:** Met by leveraging Rust’s compile-time memory safety to eliminate data races and runtime crashes, enforcing strict type consistency.
* **Design, develop, and deliver professional-quality oral, written, and visual communications:** Met by providing clear narrative documentation of the language transition and explaining complex concurrency concepts.


<br>

<a href="https://github.com/Ayjrin/CS499/tree/main/artifacts/CS510"><strong>Link to Software Design and Engineering Code</strong></a>

<br>

---

<br>

<div id="algorithms"></div>

## Category 2: Algorithms and Data Structures

<kbd>Python</kbd> <kbd>Hash Tables</kbd> <kbd>Complexity Analysis</kbd> <kbd>Optimization</kbd>

### High-Performance Record Search

**Artifact Description**
This artifact is a data search engine designed to retrieve specific string patterns from large datasets, originally created for CS 680. The initial implementation used a Min-Heap structure coupled with Depth-First Search (DFS) to locate specific entries.

**Justification for Inclusion & Enhancement**
I selected this artifact because it demonstrates my ability to critically evaluate and optimize algorithmic performance. Using a Min-heap for arbitrary string retrieval is an algorithmic anti-pattern; Heaps are designed for priority access, not general search. The enhancement involved replacing the Min-heap with a Hash Table (Python Dictionary), optimizing the search from an inefficient O(n) to an average O(1) time complexity.

**Reflection on the Enhancement Process**
This enhancement taught me that forcing a specific algorithmic approach (like a pruned DFS on a heap) simply to meet an arbitrary structural requirement is inferior to choosing the correct data structure for the job. The greatest challenge was documenting and justifying the complete removal of the heap structure. This process strengthened my ability to defend technical decisions based on theoretical complexity and empirical data.

**Course Outcomes Met**
* **Design and evaluate computing solutions that solve a given problem using algorithmic principles:** Met by performing a deep complexity analysis and executing the transition from an O(n) Heap DFS to an O(1) Hash Table lookup, drastically improving search efficiency.
* **Employ strategies for building collaborative environments that enable diverse audiences to support organizational decision making:** Met by documenting the architectural shift to justify the change to stakeholders. 
  * <a href="/CS499/artifacts/CS680/algorithms_communication.md"><strong>View the Algorithms Communication Documentation here</strong></a>.


<br>

<a href="https://github.com/Ayjrin/CS499/tree/main/artifacts/CS680"><strong>Link to Algorithms and Data Structures Code</strong></a>

<br>



---

<br>

<div id="databases"></div>

## Category 3: Databases

<kbd>PostgreSQL</kbd> <kbd>MongoDB</kbd> <kbd>Schema Design</kbd> <kbd>Data Integrity</kbd>

### Travlr Getaways Data Architecture

**Artifact Description**
The artifact is the data layer for "Travlr Getaways," a full-stack web application that manages travel data, user accounts, and trip listings. It was originally built using MongoDB (NoSQL) as part of the MEAN stack during my CS 465 Full Stack Development course.

**Justification for Inclusion & Enhancement**
This project is a comprehensive example of my ability to build and manage complex database-driven applications. A critical finding in my code review was that MongoDB, being schema-less, lacks the data integrity guarantees of a relational database for handling complex relational data like bookings and trips. The enhancement consisted of migrating the entire data layer from MongoDB to PostgreSQL.

**Reflection on the Enhancement Process**
Transitioning from a NoSQL document store to a strict relational model required a complete redesign of how data entities interacted. Instead of relying purely on application-level validation, I had to ensure the database itself enforced strict relational rules through foreign keys and constraints. This project reinforced the importance of structural integrity and how proper database selection simplifies backend logic.

**Course Outcomes Met**
* **Demonstrate an ability to use well-founded and innovative techniques, skills, and tools:** Met by implementing PostgreSQL as a modern, robust relational solution over the legacy schema-less database, optimizing complex relational joins.
* **Develop a security mindset that anticipates adversarial exploits in software architecture:** Met by implementing strict relational constraints, foreign keys, and SQL injection prevention techniques to secure backend data resources, ensuring files and devices are left in the correct state via transaction safety.

<br>


<a href="https://github.com/Ayjrin/CS499/tree/main/artifacts/CS465"><strong>Link to Database Code</strong></a>


<br>

---
