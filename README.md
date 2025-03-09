# INFO8665--Airplane
Predicting flight patterns for DSS

## Project Description
This project focuses on building a machine learning model to predict airplane fare prices based on factors like airline, journey date, source, destination, and total stops. The project is developed collaboratively using **GitHub** and **Azure Boards** for effective project management and collaboration.

## **Goals**
- Develop a robust fare prediction model with optimized performance.
- Implement CI/CD workflows for smooth integration and deployment.
- Collaborate efficiently using Azure Boards and GitHub workflows.


Team Members
| Student ID | Name |
|--------------------------------|---------------------|
| 8930180 | Jaiv Burman |
| 8952840 | Harsh Joshi |
| 8993410 | Prashansa Rathod |
| 8983991 | Nilkumar Patel |
| 9041129 | Nidhi Ahir |

## **Project Workflow Structure**
### **Branching Strategy**
- Each feature or task is handled under separate **sprint branches** following a predefined branching structure:
  - `main`: Stable code ready for deployment.
  - `sprint/[sprint-number]`: Contains work done under specific sprints.
  - Development starts with branching from `main` and ends with merging the work back through a **pull request**.
  - The professor will review pull requests before merging them into `main`.

---

### **Pull Request Workflow**
1. Create a new branch for each sprint using the naming convention: `sprint/[task-id]`.
2. Implement the task in the respective branch.
3. Create a pull request with proper description and linked Azure Board tasks.
4. The professor reviews the pull request.
5. If approved, the branch is merged into `main`.

---

## **Folder Structure**
├── data-collection/ # Contains datasets used for training and testing ├── dev/ # Development scripts and helper modules ├── documentation/ # Documentation files ├── orchestrator.ipynb # Main orchestration notebook ├── README.md # Project documentation └── trained-models/ # Trained models stored by version


## Directory Structure
1. **airplanevenv/**:
    - The virtual environment directory, where all the project-specific dependencies are installed.
    - To activate the virtual environment, use the appropriate command based on your system:
      - **Windows**: `.\airplanevenv\Scripts\activate`
      - **Mac/Linux**: `source airplanevenv/bin/activate`

2. **data/**:
    - This directory contains the dataset(s) required for analysis.
    - Place any CSV, JSON, or other data files within this directory.

3. **.gitignore**:
    - A configuration file used to exclude certain files and directories from being tracked by Git. 
    - Common exclusions include the `airplanevenv/` directory, temporary files, and large datasets.

4. **airplane.ipynb**:
    - The main Jupyter Notebook where data analysis, preprocessing, and model training are performed.
    - Open this using Jupyter Notebook or Visual Studio Code to explore the project.

5. **README.md**:
    - This project documentation file explains the structure, setup instructions, and project details.

---

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd INFO8665--AIRPLANE
