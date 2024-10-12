import cv2, pygame

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

# Set up the Pygame display
screen = pygame.display.set_mode((640, 480))  # Adjust the resolution as needed

# Main loop
while True:
    # Read the frame
    ret, cv2_cam = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(cv2_cam, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(cv2_cam, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(cv2_cam, (200, y), (300, y + h), (255, 0, 0), 2)
        y1 = y
        y2 = y + h
        midy = (y1 + y2) / 2

    # Convert OpenCV image to Pygame surface
    cv2_cam = cv2.cvtColor(cv2_cam, cv2.COLOR_BGR2RGB)
    cv2_cam_surface = pygame.surfarray.make_surface(cv2_cam)
    cv2_cam_surface = pygame.transform.rotate(cv2_cam_surface, 270)

    # Blit the surface onto the Pygame screen
    screen.blit(cv2_cam_surface, (0, 0))

    # Update the display
    pygame.display.update()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            break

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()