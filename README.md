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

![alt text](image.png)

---

## **Environment Setup**
To replicate the development environment:
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/JB250101/INFO8665--Airplane.git
   cd INFO8665--Airplane

# 🚀 **Flight Fare Prediction API (MLOps Use Case)**

This repository contains a **Flask-based MLOps pipeline** for predicting flight fares using Machine Learning. It consists of **three microservices**:

1. **Preprocessing Service** (`preprocessing.py`) - Cleans & encodes input data.
2. **Training Service** (`train_service.py`) - Trains the flight fare prediction model.
3. **Prediction Service** (`prediction_service.py`) - Predicts flight fares using the trained model.

---

## Directory Structure

# INFO8665--AIRPLANE

### Project and environment setup

1. Move to project directory "INFO8665" where you have cloned the project
2. Create virtual environment with name **"airplanevenve"**
    - Make sure ```python --version``` is set to **12.3.6** in your system
    - ```python -m venv airplanevenve```
3. Activate environment
    - ```.\airplanevenve\Scripts\Activate.ps1```
    - In case you are using visual studio code, Choose the environment from menu as active environment
4. Install packages mentioned in **"requirements.txt"**
    - ```pip install -r requirements.txt```
5. Select **"airplanevenve"** environment in your IDE
6. Create folder named **"dataset"** in your project directory
7. Move all files downloaded from Kaggle dataset in the "Dataset" Directory


### Update Requirements.txt file once installing new packages

```pip freeze > requirements.txt```

    
**data/**:
- This directory contains the dataset(s) required for analysis.
- Place any CSV, JSON, or other data files within this directory.

**.gitignore**:
- A configuration file used to exclude certain files and directories from being tracked by Git. 
- Common exclusions include the `airplanevenv/` directory, temporary files, and large datasets.

**airplane.ipynb**:
- The main Jupyter Notebook where data analysis, preprocessing, and model training are performed.
- Open this using Jupyter Notebook or Visual Studio Code to explore the project.

**README.md**:
- This project documentation file explains the structure, setup instructions, and project details.

**docs**:
- This directory contains all the html pages, document report for every sprints

2. **Azure DevOps Integration:**
    Follow Azure Boards integration setup guidelines as outlined in [Azure Boards Link](https://dev.azure.com/Jburman0180/Airplane%20Fare%20Price/).

---

# Downloadables

-   **Training dataset:** Available in the `data/` folder.
    You can download dataset from [Kagglel](https://www.kaggle.com/datasets/shubhamsarafo/flight-price)
-   **Pre-trained models:** Stored in `models/`.

# Pre-requisites
-   Python 3.x installed on the machine.
-   Azure DevOps configured with project access.
-   Git installed and set up.





---

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd INFO8665--AIRPLANE

2. ## ** Install Required Dependencies**
    Before running the services, install the required Python packages:

```bash
pip install flask pandas scikit-learn joblib requests openpyxl
```

3. ## Run Preprocessing Service
    This service processes flight details into a model-friendly format.

    ```python preprocessing.py```

    ✅ Runs on: ```http://127.0.0.1:5002/preprocess```


    Example Request:
   
```bash 
   {
        "Date_of_Journey": "12/03/2024",
        "Airline": "Indigo",
        "Source": "Delhi",
        "Destination": "Mumbai"
    }
```

    Example Response:
    
```bash
    {
    "status": "Success",
    "processed_data":[[2.42, 0.04, 3.09, 12, 3]]
    }
```
4. ## Run Training Service:

This service trains the model using the dataset and saves it.

```bash
    python train_service.py
```
Runs on: ```http://127.0.0.1:5003/train```

    Example Response:

    ```bash
        {
    "status": "Success",
    "message": "Model trained successfully!",
    "MAE": 1550.92
        }
    ```

5. ## Run Prediction Service:
This service predicts flight fares for a given input.

```bash
    python prediction_service.py
```

Runs on: ```http://127.0.0.1:5004/predict```

 Example Request:
 
 ```bash
    {
    "processed_data": [[2.42, 0.04, 3.09, 12, 3]]
    }
 ```

 Example Response:

 ```bash
    {
    "status": "Success",
    "predicted_price": [7740.42]
    }
 ```
