# Created by Stefen Labinay | BSCS 3-5
import tkinter
import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kingkaytadmin",
    database="exercises"
)
cursor = db_connection.cursor()
db_connection.commit()


# This is second window
def second_window():
    main_window.destroy() #vDestroy the main window
    class AttendanceApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Attendance App")
            self.root.minsize(621,570)
            self.root.maxsize(621,570) 

            self.frame = tkinter.Frame(root,bg="#e3e384",width=608, height=578)
            self.frame.place(anchor='center', relx=0.5, rely=0.5)

            # GUI elements 
            # studentNum label
            self.studentNum_label = Label(root, text="Student Number", fg="black", bg="#e3e384")
            self.studentNum_label.configure(height=1, width=20) 

            # studentNum textbox
            self.studentNum = Entry(root, width=30, fg="black", bg="white")
            
            # Name label
            self.name_label = Label(root, text="Name", fg="black", bg="#e3e384")
            self.name_label.configure(height=1, width=20)

            # Name textbox
            self.name_entry = Entry(root, width=30, fg="black", bg="white")
            
            # Status label
            self.status_label = Label(root, text="Status", fg="black", bg="#e3e384")
            self.status_label.configure(height=1, width=20)

            # Status textbox
            # self.status_entry = Entry(root, width=30, fg="black", bg="white")

            # Dropdown Manu
            self.options = ["Present", "Absent"]
            self.selected_option = tk.StringVar(root)
            self.selected_option.set(self.options[0])  # Set the default option

            self.dropdown = tk.OptionMenu(root, self.selected_option, *self.options)
            self.dropdown.configure(height=1, width=20)

            # Add button
            self.add_button = tk.Button(root, text="ADD", fg="#f7f9fc", bg="#47b564", command=self.add_record)
            self.add_button.configure(height=2, width=10, borderwidth=0)

            # Delete button
            self.delete_button = Button(root, text="DELETE", fg="#f7f9fc", bg="#bf4343", command=self.delete_record)
            self.delete_button.configure(height=2, width=10, borderwidth=0)

            # Display button
            self.display_button = Button(root, text="DISPLAY", fg="#f7f9fc", bg="#3a5587", command=self.display_records)
            self.display_button.configure(height=2, width=10, borderwidth=0)

            # TreeView to display records
            self.tree = ttk.Treeview(root, columns=("StudentNumber", "name", "status"), show="headings")
            self.tree.heading("StudentNumber", text="Student Number")
            self.tree.heading("name", text="Name")
            self.tree.heading("status", text="Status")

            # grid layouts of the Elements
            self.studentNum_label.grid(row=0, column=1, padx=30, pady=20)
            self.studentNum.grid(row=0, column=2, padx=10, pady=10)

            self.name_label.grid(row=1, column=1, padx=10, pady=20)
            self.name_entry.grid(row=1, column=2, padx=10, pady=10)

            self.status_label.grid(row=2, column=1, padx=10, pady=20)
            #self.status_entry.grid(row=2, column=2, padx=10, pady=20)
            self.dropdown.grid(row=2, column=2, padx=10, pady=20)

            self.add_button.grid(row=3, column=1, padx=10, pady=20,)
            self.delete_button.grid(row=3, column=2, padx=10, pady=20)
            self.display_button.grid(row=3, column=3, padx=10, pady=20)

            self.tree.grid(row=4, column=1, columnspan=3, padx=10, pady=40)
            

            # Function to add records
        def add_record(self):
            studentNum = self.studentNum.get()
            name = self.name_entry.get()
            status = self.selected_option.get()

            if studentNum and name and status:
                cursor.execute("INSERT INTO attendance (StudentNumber, name, status) VALUES (%s, %s, %s)", (studentNum, name, status))
                db_connection.commit()
                self.clear_entries()
                messagebox.showinfo("Success", "Record added successfully!")
                self.display_records_in_treeview()
            else:
                messagebox.showwarning("Warning!", "Please enter the required data!")

        # Function to delete records
        def delete_record(self):
            name = self.name_entry.get()

            if name:
                cursor.execute("DELETE FROM attendance WHERE name = %s", (name,))
                db_connection.commit()
                self.clear_entries()
                messagebox.showinfo("Success", "Record deleted successfully!")
                self.display_records_in_treeview()
            else:
                messagebox.showwarning("Warning!", "Please enter name to delete!")

        # Calls the function to display records in treeview
        def display_records(self):
            self.display_records_in_treeview()


        # Function to display records
        def display_records_in_treeview(self):

            # Clear previous items in the TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            cursor.execute("SELECT * FROM attendance")
            records = cursor.fetchall()

            if records: 
                for record in records:
                    self.tree.insert("", "end", values=record)

        # Function to clear records
        def clear_entries(self):
            self.studentNum.delete(0, END)
            self.name_entry.delete(0, END)

    # Run the Tkinter app
    if __name__ == "__main__":
        root = Tk()
        app = AttendanceApp(root)
        root.mainloop()

    # Close the database connection
    cursor.close()
    db_connection.close()



# Main window
main_window = Tk()

# Load the icon image 
icon_image = tk.PhotoImage(file="AdetApp\logo.png")
main_window.iconphoto(True, icon_image)

main_window.title("Simple Attendance App") # Title
main_window.minsize(550,600)
main_window.maxsize(550,600)

frame = tkinter.Frame(main_window,bg="gray",width=500, height=100)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("AdetApp\Logo.png"))

label = tkinter.Label(frame,image = img)
label.pack(padx=10,pady=10)

# Button for Attendance
button = tkinter.Button(frame, width=30, borderwidth=0, fg="black", bg="white", text="Attendance", command=second_window)
button.pack(padx=10, pady=10)

main_window.mainloop()

# Created by Stefen Labinay | BSCS 3-5


