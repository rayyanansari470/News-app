import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
from PIL import Image, ImageTk
import requests
# from bs4 import BeautifulSoup

# Function to fetch headlines (title and description)
def fetch_headlines():
    query = query_entry.get()
    url = f"https://newsapi.org/v2/everything?q={query}&from=2024-08-18&sortBy=publishedAt&apiKey=62414d6c177044198076577b0dbd2f24"
    response = requests.get(url)
    news = response.json()

    # Create a new window to display headlines
    headlines_window = tk.Toplevel(root)
    headlines_window.title("News Headlines")
    headlines_window.geometry("800x600")

    # Create a scrolled text widget
    text_widget = scrolledtext.ScrolledText(headlines_window, wrap=tk.WORD, bg='#ffffff', fg='#000000')
    text_widget.pack(expand=True, fill='both')

    for article in news["articles"]:
        title = article["title"]
        description = article["description"]

        text_widget.insert(tk.END, f"Title: {title}\nDescription: {description}\n")
        text_widget.insert(tk.END, "-" * 100 + "\n")


# Function to fetch full articles (title and content)
def fetch_articles():
    query = query_entry.get()
    url = f"https://newsapi.org/v2/everything?q={query}&from=2024-08-18&sortBy=publishedAt&apiKey=62414d6c177044198076577b0dbd2f24"
    response = requests.get(url)
    news = response.json()

    # Create a new window to display full articles
    articles_window = tk.Toplevel(root)
    articles_window.title("Full Articles")
    articles_window.geometry("800x600")

    # Create a scrolled text widget
    text_widget = scrolledtext.ScrolledText(articles_window, wrap=tk.WORD, bg='#ffffff', fg='#000000')
    text_widget.pack(expand=True, fill='both')

    for article in news["articles"]:
        title = article["title"]
        content = article["content"]

        # Uncomment the following lines if you need to use Beautiful Soup
        # article_url = article["url"]
        # article_response = requests.get(article_url)
        # soup = BeautifulSoup(article_response.content, 'html.parser')
        # paragraphs = soup.find_all('p')
        # full_text = ''.join([para.get_text() for para in paragraphs])

        text_widget.insert(tk.END, f"Title: {title}\nContent: {content}\n")
        text_widget.insert(tk.END, "-" * 100 + "\n")


def on_entry_click(event):
    """Remove placeholder text when the user clicks on the entry field."""
    if query_entry.get() == placeholder_text:
        query_entry.delete(0, "end")  # Delete all text
        query_entry.config(fg='black')  # Set text color to black


def on_focusout(event):
    """Restore placeholder text when the entry field is unfocused and empty."""
    if query_entry.get() == "":
        query_entry.insert(0, placeholder_text)
        query_entry.config(fg='grey')  # Set text color to grey


def on_enter(e):
    e.widget['background'] = '#819db5'  # Change background on hover


def on_leave(e):
    e.widget['background'] = '#6a8ba3'  # Restore the original background


# Initialize Tkinter window
root = tk.Tk()
root.configure(bg='#e0f7fa')
root.title("News App")
root.geometry('800x500')

image = Image.open('newspaper.png')
image = image.resize((200, 200), Image.Resampling.LANCZOS)
image = image.convert("RGBA")

# Get the data of the image (pixel by pixel)
data = image.getdata()

# Create a new image list to hold pixels
new_data = []

# Specify the background color to remove (e.g., white)
bg_color = (255, 255, 255)  # White

# Iterate through each pixel
for item in data:
    # Change all white (or near-white) pixels to transparent
    if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:  # Adjust the tolerance if needed
        new_data.append((255, 255, 255, 0))  # Make the pixel transparent
    else:
        new_data.append(item)  # Keep the pixel unchanged

# Update the image with the new data
image.putdata(new_data)

# Convert the image to a Tkinter-compatible format
tk_image = ImageTk.PhotoImage(image)

# Display the image
label = Label(root, image=tk_image, bg='#e0f7fa')
label.place(x=800, y=80)

placeholder_text = "What type of news are you interested in?"

# Label and entry to take user input for news query
query_entry = tk.Entry(root, width=50)
query_entry.insert(0, placeholder_text)

# Bind the Entry widget to events
query_entry.bind("<FocusIn>", on_entry_click)
query_entry.bind("<FocusOut>", on_focusout)
query_entry.place(x=750, y=430)

# Buttons to fetch either headlines or full articles
button1 = tk.Button(root, text="Fetch Headlines", command=fetch_headlines, width=20, height=2, bg='#6a8ba3',
                    fg='#ffffff')
button2 = tk.Button(root, text="Fetch Full Articles", command=fetch_articles, width=20, height=2, bg='#6a8ba3',
                    fg='#ffffff')
button1.place(x=700, y=650)
button2.place(x=1010, y=650)
button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)

# Run the Tkinter event loop
root.mainloop()
