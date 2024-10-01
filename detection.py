import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
import time

# Function to process image and detect contours
def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, image

# Function to place vertical stitching points and ensure the rect encloses all contours
def detect_wound_and_stitches(image, contours, num_stitching_points):
    # Get the bounding rectangle that encloses all contours
    if len(contours) == 0:
        print("No contours found!")
        return image, []

    all_contours = np.vstack(contours)  # Combine all contours into one array
    x, y, w, h = cv2.boundingRect(all_contours)  # Get the enclosing bounding rectangle

    # Draw the bounding rectangle around the wound
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Calculate evenly spaced stitching points along the top and bottom edges
    top_edge_points = np.linspace(x, x + w, num_stitching_points, dtype=int)
    bottom_edge_points = np.linspace(x, x + w, num_stitching_points, dtype=int)

    # List to store the stitching points pairs (top and bottom)
    stitching_points = []

    for i in range(len(top_edge_points)):
        top_point = (top_edge_points[i], y)
        bottom_point = (bottom_edge_points[i], y + h)

        # Draw stitching points as red circles
        cv2.circle(image, top_point, 4, (0, 0, 255), -1)
        cv2.circle(image, bottom_point, 4, (0, 0, 255), -1)

        # Draw the stitch (line) vertically between top and bottom points
        cv2.line(image, top_point, bottom_point, (0, 0, 255), 2)

        # Add the stitching points to the list in the required format [[(x1, y1), (x2, y2)], ...]
        stitching_points.append([top_point, bottom_point])

    return image, stitching_points

# Function to send stitching points to an Arduino using serial communication
def send_data_to_arduino(stitching_points, port='COM3', baud_rate=9600):
    try:
        # Open the serial port
        arduino = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for the connection to establish

        # Format the stitching points as a string to send over serial
        formatted_points = ""
        for pair in stitching_points:
            top_point = f"({pair[0][0]},{pair[0][1]})"
            bottom_point = f"({pair[1][0]},{pair[1][1]})"
            formatted_points += f"{top_point},{bottom_point};"  # Separate pairs by semicolon

        # Send the formatted points over the serial port
        arduino.write(formatted_points.encode())

        # Print the sent data for debugging
        print(f"Sent to Arduino: {formatted_points}")

        # Close the serial port after sending the data
        arduino.close()

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. Ensure Arduino is connected.")
        print(e)

# Main function
def main(image_path, num_stitching_points=10):
    contours, image = process_image(image_path)

    # Detect wound, place stitching points
    stitched_image, stitch_points = detect_wound_and_stitches(image, contours, num_stitching_points)

    # Display the image with stitching points
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(stitched_image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Wound with Vertical Stitching Points')
    plt.axis('off')
    plt.show()

    # Print the stitching points
    print("Stitching points (top and bottom pairs):")
    print(stitch_points)

    # Send the stitching points to Arduino
    send_data_to_arduino(stitch_points, port='COM3', baud_rate=9600)

# Example usage
image_path = '14.png'  # Wound image path
main(image_path, num_stitching_points=10)
