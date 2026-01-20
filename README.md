# Investment Calculator

An interactive investment calculator application built with Python and Tkinter. This project is designed to calculate compound interest and visualize financial growth over time. It features a bilingual interface (English/Arabic), real-time charting, and professional PDF report generation.

## System Requirements

- Operating System: Linux (Developed and tested on Kali Linux)
- Python Version: 3.13.6
- Basic system resources for rendering charts

## Dependencies

The project requires the following Python libraries:

- tkinter (Standard Linux package)
- matplotlib
- reportlab
- arabic-reshaper
- python-bidi

## Installation and Usage

1. Install the required libraries using pip:
   pip install matplotlib reportlab arabic-reshaper python-bidi

2. Ensure Tkinter is installed on your Linux system:
   sudo apt-get install python3-tk

3. Run the application:
   python3 main.py

## Project Structure

The project is divided into three main files for modularity:

- main.py: The entry point of the application.
- app_gui.py: Contains the main application logic, GUI layout, chart generation, and PDF export functionality.
- helpers.py: Contains helper functions for Arabic text processing and input validation.

## Technical Challenges and Solutions

During development on Linux, we solved specific challenges regarding text rendering and file export.

### 1. Arabic Text Support on Linux
Problem:
Tkinter on Linux does not natively support Right-to-Left (RTL) text rendering or Arabic ligatures, causing text to appear disconnected and reversed.

Solution:
We implemented a text processing pipeline using 'arabic-reshaper' (to connect letters) and 'python-bidi' (to fix direction). A helper function in 'helpers.py' processes all Arabic strings before display.

### 2. Chart Integration in PDF Reports
Problem:
Exporting the dynamically generated Matplotlib chart into a static PDF report using ReportLab caused format compatibility issues. The PDF engine could not directly read the image stream from memory buffers.

Solution:
We used `io.BytesIO` to save the chart as an image in memory, and then utilized `reportlab.lib.utils.ImageReader` to correctly process and buffer the image data before drawing it onto the PDF canvas.

## Features

- Compound Interest Calculation: accurate monthly calculation logic.
- Data Visualization: Interactive Matplotlib charts showing total value vs. invested principal.
- PDF Export: Generates a detailed financial report including the summary and the growth chart.

<img width="1366" height="732" alt="Screenshot_2026-01-20_09-03-21" src="https://github.com/user-attachments/assets/219a37be-747b-4e82-aa37-19528a55445b" />

<img width="1366" height="733" alt="Screenshot_2026-01-20_09-04-16" src="https://github.com/user-attachments/assets/0003b0d5-02b5-4fb5-9908-645de3c2af96" />

<img width="485" height="295" alt="Screenshot_2026-01-20_09-04-42" src="https://github.com/user-attachments/assets/dc136957-79e9-4d75-a333-6e12aacc5eab" />

<img width="587" height="597" alt="Screenshot_2026-01-20_09-05-15" src="https://github.com/user-attachments/assets/e13229df-eca0-4288-adf3-5770831be287" />

