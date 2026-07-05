# Academic Metrics & Rubric Specifications

This document defines the evaluation criteria, scoring rubrics, and scaling rules used by the AI sub-agents to calculate student performance metrics. These metrics are logged to Airtable to serve as empirical proof of program value for future funding proposals.

---

## 1. The Core Academic Triad

To measure academic competency growth, the **`academic_auditor.py`** agent scores the student's report on three core academic dimensions on a scale of 1 to 10:

### 1.1 Scientific Methodology (1-10)
*   **Evaluation Focus**: Rigor of research questions, logical conceptual models, and feasibility of experimental or survey designs.
*   **Rubric Guidelines**:
    *   `10`: Exceptionally clear research questions linked directly to measurable, feasible parameters with full mathematical or procedural specification.
    *   `7-9`: Complete methodology with clear steps, but minor parameter gaps or slightly oversized scope.
    *   `5-6`: Basic methodology outlined, but lacks details on variables, parameters, or sampling size.
    *   `1-4`: Vague, purely descriptive study lacking structured experimental design.

### 1.2 Data Triangulation (1-10)
*   **Evaluation Focus**: Integration of primary field measurements with secondary literature, regional database validation, and reference baseline comparison.
*   **Rubric Guidelines**:
    *   `10`: Exhaustive comparison of primary field data against historical baselines, government datasets, and peer-reviewed literature.
    *   `7-9`: Compares field data with at least one external dataset or literature source, showing logical correlations.
    *   `5-6`: Simple reporting of primary data without external validation or contextual comparison.
    *   `1-4`: Descriptive logs without structured data variables or reference baselines.

### 1.3 Academic Writing Clarity (1-10)
*   **Evaluation Focus**: Structure, formatting, citation logic, and vocabulary precision.
*   **Rubric Guidelines**:
    *   `10`: Flawless structural flow, formal academic language, precise terminology, and complete citation maps.
    *   `7-9`: Minor grammatical errors or citation gaps, but clear logical structure and professional tone.
    *   `5-6`: Readable, but relies on informal descriptions or lacks proper academic structuring.
    *   `1-4`: Unstructured prose, missing sections, and colloquial formatting.

---

## 2. Sponsor Alignment Index (SAI)

The **`alignment_agent.py`** compares the student's report against the sponsor's original problem statement, outputting an alignment index from 1% to 100%.

### 2.1 Evaluation Dual Checks
The Sponsor Alignment Index is calculated at two critical gate check-points:
1.  **Inception Gate (Month 1)**: Checked to prevent early research drift and verify that the proposed conceptual models actively target the sponsor's practical questions.
2.  **Final Thesis Submission (Exit Gate)**: Evaluated to measure the overall research utility and provide a quantitative proof of impact to the sponsor.

---

## 3. Proportional Rigor Adjustments

To ensure evaluations are fair, the AI sub-agents adjust their grading rubrics dynamically based on two metadata variables:

### 3.1 Degree Level
*   **BSc**: Evaluated primarily on **feasibility and direct observations**. Grading favors simple primary data collection, basic household surveys, and logical field schedules. High triangulation is not expected.
*   **MSc**: Evaluated on **rigorous data triangulation**. The student must correlate primary measurements with secondary databases (e.g., KSNMDC, Central Ground Water Board) and employ statistical correlation models.
*   **PhD**: Evaluated on **theoretical novelty, modeling depth, and publication readiness**. The student must build advanced system dynamics, hydrologic models, or novel algorithms, and write in a peer-review publishable format.

### 3.2 Program Duration
*   **6-Month Cohort**: Prioritizes rapid fieldwork execution, immediate data checks, and direct observational timelines. Literature reviews are expected to be focused and concise.
*   **10-Month Cohort**: Demands exhaustive literature studies, seasonal comparison cycles (pre- and post-monsoon tracking), and highly refined thesis drafting stages.
