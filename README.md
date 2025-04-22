# Data Warehouse - Program Design

---

## Start the Project

To start the project you need the follow the following steps:

(Run the following commands in the terminal)

1. **Initialise Project**

   ```bash
   python3 setup_project.py
   ```

> **Note:** If `Initialise Project` does not work , you can activate the virtual environment and install the requirements manually:
>
>
> **Create a virtual environment**
>   ```bash
>   python3 -m venv venv
>    ```
> **Activate the virtual environment**
> 
> Windows (CMD)
>  ```bash
> venv\Scripts\activate.bat
> ```
> Windows (PowerShell)
> ```bash
> venv\Scripts\Activate.ps1
> ```
> MacOS
>   ```bash
>   source venv/bin/activate
> ```
> 
> **Install dependencies**
> 
> Run inside the virtual environment:
>   ```bash
>   pip install -r requirements.txt
>   ```


2. **Install Neo4j**
    - Go to following [Website](https://neo4j.com/download/) and download **Neo4j Desktop**.
    - Fill out the **form** to register (tip: you can fill out the form with random data if you don't want to
      expose private data)
    - Copy `Activation Key` to clipboard (you need the key later on)
    - Follow casual installation process
    - After you have agreeded the terms you can paste your `Activation Key` to the **Software Key** field
      to finish the installation process.

3. **Set up the Neo4j database**
    - To create a new project, click the button in the top-left corner.
    - To add a local DBMS, click the blue "Add" button in the middle of the screen.
    - Enter "neo4j" as the name and "test1234" as the password. You can choose any name and password,
      but you'll need to make a change in the init_connection function.
    - Click on "Create" and then start the database by clicking "Start"
    - You can now run the Jupyter Notebook. If you used a different combination
      of USERNAME and PASSWORD than neo4j and test1234, be sure to change the values in the helper_functions file
      `init_connection()`.

4. Run the `main.ipynb` notebook and select the virtual environment as kernel
5. Optional: You get a modal where you should click `Install`

---

## Structure of the Project

### main.ipynb

This notebook is used to create the knowledge graph.

### io / export.ipynb

This notebook is used to export the data from the graph to Excel files.

### io / import.ipynb

This notebook is used to import new data from an Excel file into the graph.

### helpers / helper_functions.py

This Python file contains all necessary functions used in the notebooks listed above.
This is needed to avoid Code duplication and keep the whole project clean.

### data - Directory

In this directory there is one `export` and one `import` directory. In the `export` directory all exports will be
saved. In the `import` directory you can store the data that should be added to the graph the next time you run
the import notebook.

### tests / tests.ipynb

This notebook contains all functional and non-functional tests regarding this project.

### setup.py

This Python file is used to setup the whole project correctly. It's necessary to import all packages
correctly afterwards.

---

## Structure of Knowledge Graph

### There are following nodes:

- Doctor
- Topic
- SubTopic
- Illness
- Symptom
- Cause
- Treatment
- Patient
- Drug
- Diagnosis
- Hospital
- Allergy
- Insurance
- Department

### There are following relationships:

- Doctor -> Topic: SPECIALIST_IN
- Doctor -> Treatment: PRESCRIBES
- Doctor -> Diagnosis: HAS_DIAGNOSED
- Doctor -> Drug: PRESCRIBES
- Doctor -> Patient: TREATS
- Doctor -> Hospital: WORKS_IN

- Topic -> SubTopic: INCLUDES

- Illness -> Cause: CAUSED_BY
- Illness -> SubTopic: BELONGS_TO
- Illness -> Treatment: TREATED_BY

- Symptom -> Illness: SYMPTOM_OF

- Patient -> Illness: HAS
- Patient -> Symptom: SHOWS
- Patient -> Treatment: RECEIVES
- Patient -> Drug: TAKES
- Patient -> Diagnosis: RECEIVES
- Patient -> Allergy: HAS
- Patien -> Insurance: HAS
- Patient -> Hospital: VISITS

- Hospital -> Department: HAS
