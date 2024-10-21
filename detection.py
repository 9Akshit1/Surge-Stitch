import cv2
import numpy as np
import pygame
import serial
import time
from tkinter import Tk, filedialog

# Initialize pygame
pygame.init()

# Screen constants
WIDTH = 1200
HEIGHT = 900
SCROLL_SPEED = 15
CONTENT_PADDING = 40

# Color Palette
COLOR_PALETTE = {
    'BG_COLOR': (240, 248, 255),  # Alice Blue
    'PRIMARY_BLUE': (0, 123, 255),  # Dodger Blue
    'PRIMARY_BLUE_HOVER': (0, 105, 217),  # Darker Blue
    'PRIMARY_GREEN': (40, 167, 69),  # Forest Green
    'PRIMARY_GREEN_HOVER': (33, 136, 56),  # Darker Green
    'TEXT_COLOR': (33, 37, 41),  # Dark Gray
    'CARD_BG': (255, 255, 255),  # White
    'CARD_BORDER': (222, 226, 230),  # Light Gray
    'ACCENT_COLOR': (255, 193, 7),  # Amber
}

# Fonts
pygame.font.init()
# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("serif", 48, bold=True)
HEADER_FONT = pygame.font.SysFont("serif", 32)
BODY_FONT = pygame.font.SysFont("serif", 18)

class ScrollableInterface:
    def __init__(self):
        self.scroll_y = 0
        self.total_height = 0
        self.content_surfaces = {}
        self.button_states = {'upload': False, 'submit': False}

    def create_card(self, width, height, with_border=True):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, COLOR_PALETTE['CARD_BG'], (0, 0, width, height), border_radius=10)
        if with_border:
            pygame.draw.rect(surface, COLOR_PALETTE['CARD_BORDER'], (0, 0, width, height), width=2, border_radius=10)
        return surface

    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def create_button(self, text, width, height, color, hover=False):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_color = color[0] if not hover else color[1]
        self.draw_rounded_rect(surface, button_color, (0, 0, width, height), 10)

        # Add subtle gradient effect
        gradient = pygame.Surface((width, height // 2), pygame.SRCALPHA)
        gradient.fill((255, 255, 255, 30))
        surface.blit(gradient, (0, 0))

        # Add text with a centered position
        text_surface = BODY_FONT.render(text, True, COLOR_PALETTE['CARD_BG'])
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        surface.blit(text_surface, text_rect)

        return surface

    def check_button_click(self, buttons_y, mouse_pos):
        upload_rect = pygame.Rect(WIDTH // 4 - 100, buttons_y + self.scroll_y, 200, 50)
        submit_rect = pygame.Rect(3 * WIDTH // 4 - 100, buttons_y + self.scroll_y, 200, 50)

        if upload_rect.collidepoint(mouse_pos):
            return 'upload'
        elif submit_rect.collidepoint(mouse_pos):
            return 'submit'
        return None

    def handle_mouse_move(self, buttons_y, pos):
        upload_rect = pygame.Rect(WIDTH // 4 - 100, buttons_y + self.scroll_y, 200, 50)
        submit_rect = pygame.Rect(3 * WIDTH // 4 - 100, buttons_y + self.scroll_y, 200, 50)

        self.button_states['upload'] = upload_rect.collidepoint(pos)
        self.button_states['submit'] = submit_rect.collidepoint(pos)

    def render_multiline_text(self, text, max_width, font, color):
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + ' ', True, color)
            word_width = word_surface.get_width()

            if current_width + word_width > max_width:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width

        if current_line:
            lines.append(' '.join(current_line))

        line_height = font.get_linesize()
        total_height = line_height * len(lines)
        text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            text_surface.blit(line_surface, (0, i * line_height))

        return text_surface

    def handle_scroll(self, event):
        max_scroll = min(0, HEIGHT - self.total_height)
        self.scroll_y = min(0, max(self.scroll_y + event.y * SCROLL_SPEED, max_scroll))

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, image

def detect_wound_and_stitches(image, contours, num_stitching_points):
    if len(contours) == 0:
        return image, []

    all_contours = np.vstack(contours)
    x, y, w, h = cv2.boundingRect(all_contours)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    top_edge_points = np.linspace(x, x + w, num_stitching_points, dtype=int)
    bottom_edge_points = np.linspace(x, x + w, num_stitching_points, dtype=int)

    stitching_points = []
    for i in range(len(top_edge_points)):
        top_point = (top_edge_points[i], y)
        bottom_point = (bottom_edge_points[i], y + h)
        cv2.circle(image, top_point, 4, (0, 0, 255), -1)
        cv2.circle(image, bottom_point, 4, (0, 0, 255), -1)
        cv2.line(image, top_point, bottom_point, (0, 0, 255), 2)
        stitching_points.append([top_point, bottom_point])

    return image, stitching_points

def send_data_to_arduino(stitching_points, port='COM4', baud_rate=9600):
    try:
        arduino = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)
        formatted_points = ""
        for pair in stitching_points:
            top_point = f"{pair[0][0]},{pair[0][1]}"
            bottom_point = f"{pair[1][0]},{pair[1][1]}"
            formatted_points += f"{top_point},{bottom_point};"
        if formatted_points:
            formatted_points = formatted_points[:-1]
        arduino.write(formatted_points.encode())
        arduino.close()
    except serial.SerialException as e:
        print(f"Error: {e}")

def open_file_dialog():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    return file_path

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Surge Stitch")
    clock = pygame.time.Clock()
    interface = ScrollableInterface()

    # Description text
    description_text = [
        "Infection and wound dehiscence—where sutures fail and a wound reopens—are significant risks in medical procedures. If a suture comes apart, patients may experience severe symptoms such as broken sutures, swelling, pus, bleeding, and even fever. For those suffering from diabetes or obesity, arterial bleeding can further complicate the situation. Infections can lead to sepsis, a condition that affects over 1 MILLION people annually in the U.S. ALONE (compared to heart disease which kills around 700K only), with a mortality rate as high as 50%. Once sepsis sets in, oxygen struggles to reach vital organs, leading to organ failure, septic shock, and often, death.",
        "This is where Surge Stitch steps in. By automating the suturing process, our system reduces the likelihood of suture failure and infection, providing a more reliable and sterile wound closure solution. Using advanced computer vision, Surge Stitch precisely identifies wound boundaries and calculates optimal stitching points. The stitching robot performs the procedure with unparalleled accuracy, lowering the risk of wound dehiscence and life-threatening complications like sepsis.",
        "In emergency settings, where every second counts and human error can have devastating consequences, Surge Stitch is designed to deliver safe, efficient, and precise wound closures. Thank you and please run our application."
    ]

    # Initial variables
    image_path = None
    uploaded_image = None
    stitched_image = None
    message_text = "Awaiting Image Upload..."
    fade_alpha = 0
    buttons_y = 0

    running = True
    while running:
        screen.fill(COLOR_PALETTE['BG_COLOR'])
        mouse_pos = pygame.mouse.get_pos()
        interface.handle_mouse_move(buttons_y, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                interface.handle_scroll(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    action = interface.check_button_click(buttons_y, mouse_pos)
                    if action == 'upload':
                        image_path = open_file_dialog()
                        if image_path:
                            contours, uploaded_image = process_image(image_path)
                            if uploaded_image is not None and uploaded_image.any():
                                message_text = "Image Uploaded! Click Process to continue."
                                fade_alpha = 0  # Reset fade for new image
                            else:
                                message_text = "Error loading image. Please try again."
                    elif action == 'submit' and uploaded_image is not None and uploaded_image.any():
                        try:
                            # Process the image and create stitched version
                            contours, image = process_image(image_path)
                            stitched_image, stitching_points = detect_wound_and_stitches(image.copy(), contours, num_stitching_points=5)
                            send_data_to_arduino(stitching_points)
                            pygame.image.save(pygame.surfarray.make_surface(stitched_image), "output_image.jpg")
                            message_text = "Image Processed Successfully!"
                        except Exception as e:
                            message_text = f"Error processing image: {str(e)}"

        # Draw title card
        title_card = interface.create_card(WIDTH - 2 * CONTENT_PADDING, 100)
        title_text = TITLE_FONT.render("Surge Stitch", True, COLOR_PALETTE['PRIMARY_BLUE'])
        title_rect = title_text.get_rect(center=(title_card.get_width() // 2, title_card.get_height() // 2))
        title_card.blit(title_text, title_rect)
        screen.blit(title_card, (CONTENT_PADDING, 50 + interface.scroll_y))

        # Draw description
        current_y = 170
        for text in description_text:
            text_surface = interface.render_multiline_text(text, WIDTH - 2 * CONTENT_PADDING - 40, BODY_FONT, COLOR_PALETTE['TEXT_COLOR'])
            description_card = interface.create_card(WIDTH - 2 * CONTENT_PADDING, text_surface.get_height() + 40)
            description_card.blit(text_surface, (20, 20))
            screen.blit(description_card, (CONTENT_PADDING, current_y + interface.scroll_y))
            current_y += text_surface.get_height() + 60

        # Draw buttons
        upload_button = interface.create_button("Upload Image", 200, 50,
                                                (COLOR_PALETTE['PRIMARY_BLUE'], COLOR_PALETTE['PRIMARY_BLUE_HOVER']),
                                                interface.button_states['upload'])
        submit_button = interface.create_button("Process Image", 200, 50,
                                                (COLOR_PALETTE['PRIMARY_GREEN'], COLOR_PALETTE['PRIMARY_GREEN_HOVER']),
                                                interface.button_states['submit'])

        buttons_y = current_y
        screen.blit(upload_button, (WIDTH // 4 - 100, current_y + interface.scroll_y))
        screen.blit(submit_button, (3 * WIDTH // 4 - 100, current_y + interface.scroll_y))
        current_y += 80

        # Draw message
        message_surface = HEADER_FONT.render(message_text, True, COLOR_PALETTE['ACCENT_COLOR'])
        message_rect = message_surface.get_rect(center=(WIDTH // 2, current_y + 30))
        screen.blit(message_surface, (message_rect.x, message_rect.y + interface.scroll_y))
        current_y += 80

        # Draw images if available
        if uploaded_image is not None and uploaded_image.any():
            fade_alpha = min(fade_alpha + 5, 255)

            # Create image cards
            img_card_width = WIDTH - 2 * CONTENT_PADDING
            img_card_height = 400

            uploaded_card = interface.create_card(img_card_width, img_card_height)
            screen.blit(uploaded_card, (CONTENT_PADDING, current_y + interface.scroll_y))

            # Convert the NumPy array from BGR to RGB if necessary
            if uploaded_image.shape[-1] == 3:  # Ensure image has 3 color channels
                uploaded_image_rgb = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)  # Use OpenCV for BGR to RGB conversion

            # Convert the NumPy array (uploaded_image_rgb) into a Pygame Surface
            pygame_image = pygame.surfarray.make_surface(np.transpose(uploaded_image_rgb, (1, 0, 2)))  # Transpose to match Pygame format

            # Scale image to fit card while maintaining aspect ratio
            img_rect = pygame_image.get_rect()
            scale = min(
                (img_card_width - 60) / img_rect.width,
                (img_card_height - 60) / img_rect.height
            )
            new_width = int(img_rect.width * scale)
            new_height = int(img_rect.height * scale)

            scaled_image = pygame.transform.scale(pygame_image, (new_width, new_height))
            scaled_image.set_alpha(fade_alpha)

            # Center image in card
            image_x = CONTENT_PADDING + (img_card_width - new_width) // 2
            image_y = current_y + interface.scroll_y + (img_card_height - new_height) // 2
            screen.blit(scaled_image, (image_x, image_y))

            # Add a label for the uploaded image
            label_surface = BODY_FONT.render("Uploaded Image", True, COLOR_PALETTE['TEXT_COLOR'])
            label_rect = label_surface.get_rect(center=(WIDTH // 2, current_y + interface.scroll_y + img_card_height + 20))
            screen.blit(label_surface, label_rect)

            current_y += img_card_height + 60

        # Repeat the same process for the stitched image
        if stitched_image is not None and stitched_image.any():
            stitched_card = interface.create_card(img_card_width, img_card_height)
            screen.blit(stitched_card, (CONTENT_PADDING, current_y + interface.scroll_y))

            # Convert the NumPy array from BGR to RGB if necessary
            if stitched_image.shape[-1] == 3:  # Ensure image has 3 color channels
                stitched_image_rgb = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2RGB)  # Use OpenCV for BGR to RGB conversion

            # Convert the NumPy array (stitched_image_rgb) into a Pygame Surface
            pygame_image_stitched = pygame.surfarray.make_surface(np.transpose(stitched_image_rgb, (1, 0, 2)))  # Transpose to match Pygame format

            scaled_stitched = pygame.transform.scale(pygame_image_stitched, (new_width, new_height))
            scaled_stitched.set_alpha(fade_alpha)

            image_x = CONTENT_PADDING + (img_card_width - new_width) // 2
            image_y = current_y + interface.scroll_y + (img_card_height - new_height) // 2
            screen.blit(scaled_stitched, (image_x, image_y))

            # Add a label for the processed image
            label_surface = BODY_FONT.render("Processed Image", True, COLOR_PALETTE['TEXT_COLOR'])
            label_rect = label_surface.get_rect(center=(WIDTH // 2, current_y + interface.scroll_y + img_card_height + 20))
            screen.blit(label_surface, label_rect)

            current_y += img_card_height + 60

        interface.total_height = current_y

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()