# ⚙️ Environment Verification for Data Science Setup

## 📌 Overview

This document verifies that my local system is fully ready for Data Science work. It confirms that Python, Conda environments, and Jupyter Notebook are functioning correctly and can be reliably used throughout the sprint.

---

## 💻 System Information

- Operating System: Windows  
- Python Version: Verified via terminal  
- Conda Version: Verified via terminal  
- Environment Used: base / ds_env  

---

## 🐍 Python Verification

Python is installed and accessible via the terminal.

**Command Used:**  
`python --version`

**Verification:**  
The command runs successfully and confirms that Python is installed and working correctly.

Additionally, Python interpreter was launched using:
`python`

Simple commands were executed successfully inside the Python REPL, confirming that Python is stable.

---

## 🧪 Conda Verification

Conda is installed and functioning correctly.

**Command Used:**  
`conda --version`

**Verification:**  
The output confirms that Conda is installed and accessible.

---

## 🔁 Conda Environment Verification

Conda environments are working correctly.

**Commands Used:**

`conda env list`  
`conda activate ds_env`

**Verification:**  
- Available environments are listed successfully  
- Environment activates correctly  
- Active environment is visible in terminal prompt  

This confirms that Conda environment management is working properly.

---

## 📓 Jupyter Notebook Verification

Jupyter Notebook launches successfully and executes Python code.

**Command Used:**  
`jupyter notebook`

**Verification Steps:**
- Jupyter opens in browser without errors  
- A new notebook is created  
- A Python cell is executed successfully  

**Example Code Run:**  
`print("Environment Setup Successful")`

**Verification:**  
The output is displayed correctly, confirming that Jupyter is working properly with Python.

---

## ✅ Final Verification Status

- Python is installed and working correctly  
- Conda is installed and environments are functional  
- Conda environment activation works correctly  
- Jupyter Notebook launches successfully  
- Python code executes correctly inside Jupyter  

The system is fully ready for Data Science workflows.

---

## 🧠 Environment Consistency

To ensure consistent behavior across systems:

- Conda environments will be used to manage dependencies  
- Same Python version will be maintained across team members  
- Jupyter will use the correct environment kernel  

This prevents issues such as:
- Version mismatches  
- Missing libraries  
- Different behavior across machines  

---

## 🚀 Conclusion

The environment has been successfully verified and is stable, consistent, and ready for Data Science development. This setup will be used throughout the sprint to ensure reliable and reproducible results.