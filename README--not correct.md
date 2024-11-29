# Face Recognition Attendance System

## Overview

This project is an automated attendance system that uses face recognition to mark attendance. It utilizes OpenCV to detect faces and `sklearn`'s K-Nearest Neighbors (KNN) algorithm to recognize them. When a face is recognized, the system logs the person's attendance along with the time, and the data is stored in a CSV file. The system uses Python's `sys` module to accept the name as a command-line argument for adding new faces.

## Features

1. **Face Detection**: Uses OpenCV's Haar Cascades to detect faces in real-time from the webcam.
2. **Face Recognition**: Uses K-Nearest Neighbors (KNN) to recognize faces based on previously stored data.
3. **Automated Attendance**: Logs attendance in a CSV file with the current timestamp.
4. **Voice Feedback**: Provides audible feedback when attendance is successfully marked.
5. **Command-line Integration**: Accepts the employee's name as an argument when adding a new face to the system.

## Project Structure

- **`test.py`**: Main script to run the face detection and recognition system.
- **`add_faces.py`**: Script to add a new employee's face data to the database (invoked by `test.py`).
- **`data/`**: Directory containing Haar Cascade files for face detection, and pickled files for face data and labels.
- **`Attendance/`**: Directory where the CSV files for attendance logs are stored.

## Requirements

To run this project, you need the following libraries:

- OpenCV (`cv2`)
- scikit-learn (`sklearn`)
- numpy (`numpy`)
- win32com.client (for text-to-speech functionality)
- pickle (for loading saved face data)

You can install the required packages using pip:

```bash
pip install opencv-python scikit-learn numpy pywin32
```

## How It Works

1. **Face Detection and Recognition**:
   - The system opens the webcam and starts detecting faces using the Haar Cascade classifier.
   - Once a face is detected, it is resized and flattened into a 1D array.
   - The KNN model is used to predict the identity of the person.
   
2. **Attendance Logging**:
   - If the person's face is recognized and a certain amount of time (60 seconds by default) has passed since their last attendance marking, the system logs the name and time into a CSV file.
   - The CSV file is named as `Attendance_<date>.csv`, where `<date>` is the current date.

3. **Voice Notification**:
   - The system uses Python's win32com client to provide audible feedback when attendance is marked.

4. **Adding New Faces**:
   - The system accepts a name as a command-line argument when running the script. This allows for adding new employees' faces into the database.

## Usage

### Running the System to Mark Attendance

To run the system and mark attendance using the webcam, use the following command:

```bash
python test.py
```

### Adding a New Employee's Face

To add a new employee's face, run the script with the employee's name as an argument:

```bash
python test.py "John Doe"
```

The script will start capturing frames from the webcam and will save the face data for the new employee, associating it with the provided name.

### Exiting the System

To exit the attendance marking system, press the 'q' key.

## Code Explanation

### `add_face(name)`

This function captures face data from the webcam and adds it to the existing face dataset.

- **Parameters**: 
  - `name`: The name of the employee to be added.
  
- **Working**:
  1. Captures face images using the webcam.
  2. Uses Haar Cascades for face detection.
  3. Adds the detected face to the existing dataset of faces.
  4. Marks the attendance with the current timestamp for that employee.

### Command-Line Argument Handling

The script uses `sys.argv` to accept a name as a command-line argument when adding new faces. If no name is provided, it will print an error message.

```python
if __name__ == '__main__':
    if len(sys.argv) > 1:
        name_argument = sys.argv[1]
        add_face(name_argument)
    else:
        print("Error: No name provided as an argument.")
```

### Attendance CSV

The attendance is stored in the `Attendance/Attendance_<date>.csv` file, where each entry consists of:
- `NAME`: The name of the employee
- `TIME`: The timestamp when the attendance was marked

## Conclusion

This face recognition system offers a convenient and automated way to mark attendance. By integrating it with a database of employee faces, you can easily track attendance and receive real-time feedback on the process. It can be further extended to improve accuracy, security, or user interface features.