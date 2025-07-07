🚦 Traffic Data Analysis & Visualization

This Python project reads traffic survey data from CSV files and visualizes the data as a histogram using a custom graphics library based on Tkinter.

---

🧠 Features

- Validates and processes real-world traffic data
- Asks users for a date and attempts to load the corresponding CSV (e.g., `traffic_data15062024.csv`)
- Analyzes:
  - Total vehicle counts
  - Vehicle types (trucks, bikes, scooters, buses)
  - Speed violations
  - Peak traffic hours
  - Weather conditions (e.g., rain)
- Saves all results to a `results_all.txt` file
- Creates a bar chart using a GUI to display hourly vehicle counts for:
  - Elm Avenue / Rabbit Road
  - Hanley Highway / Westway

---

📊 Technologies Used

- Python 3
- Custom `graphics.py` (John Zelle's graphics library)
- CSV file parsing
- File I/O and logging
- Basic math/statistics
- GUI with Tkinter-based drawing

---

🛠 How to Run

1. Clone the repository or download the files.
2. Ensure Python 3 is installed.
3. Place your CSV file in the same directory, named as `traffic_dataDDMMYYYY.csv`.
4. Run the script:
   ```bash
   python w2077028.py
