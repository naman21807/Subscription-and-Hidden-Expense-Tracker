"""Login and signup screen."""

import tkinter as tk


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f8")
        self.controller = controller

        wrapper = tk.Frame(self, bg="white", padx=30, pady=30)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            wrapper,
            text="Subscription Tracker",
            font=("Arial", 18, "bold"),
            bg="white",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(wrapper, text="Username", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(wrapper, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(wrapper, text="Password", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(wrapper, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        self.message_label = tk.Label(wrapper, text="", fg="red", bg="white")
        self.message_label.grid(row=3, column=0, columnspan=2, pady=(10, 10))

        button_frame = tk.Frame(wrapper, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Login", width=12, command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Sign Up", width=12, command=self.signup).grid(row=0, column=1, padx=5)

    def refresh(self):
        self.password_entry.delete(0, tk.END)
        self.message_label.config(text="")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, result = self.controller.auth_manager.login(username, password)

        if success:
            self.message_label.config(text="Login successful.", fg="green")
            self.controller.login_user(result)
        else:
            self.message_label.config(text=result, fg="red")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, result = self.controller.auth_manager.signup(username, password)

        if success:
            self.message_label.config(
                text="Signup successful. Please log in.",
                fg="green",
            )
            self.password_entry.delete(0, tk.END)
        else:
            self.message_label.config(text=result, fg="red")
