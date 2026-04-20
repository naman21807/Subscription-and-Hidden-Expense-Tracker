"""Tkinter subscriptions list screen."""

import tkinter as tk


class ViewSubscriptionsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        tk.Label(
            self,
            text="Your Subscriptions",
            font=("Segoe UI", 28, "bold"),
            fg=controller.text_color,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(10, 6))

        tk.Label(
            self,
            text="A full list of every saved plan.",
            font=("Segoe UI", 13),
            fg=controller.muted_text,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(0, 24))

        self.card = tk.Frame(
            self,
            bg="white",
            highlightbackground=controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        self.card.pack(fill="both", expand=True)

        self.list_frame = self._build_scroll_area()

    def _build_scroll_area(self):
        self.canvas = tk.Canvas(self.card, bg="white", highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self.card, orient="vertical", command=self.canvas.yview)
        list_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=list_frame, anchor="nw", tags="content")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        list_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure("content", width=event.width),
        )
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        return list_frame

    def refresh(self):
        for child in self.list_frame.winfo_children():
            child.destroy()

        subscriptions = self.controller.tracker.get_subscriptions(self.controller.current_user_id)
        if not subscriptions:
            tk.Label(
                self.list_frame,
                text="No subscriptions added yet.",
                font=("Segoe UI", 13),
                fg=self.controller.muted_text,
                bg="white",
            ).pack(anchor="w", padx=24, pady=24)
            return

        for subscription in subscriptions:
            item = tk.Frame(
                self.list_frame,
                bg="#FFF9FB",
                highlightbackground=self.controller.border_color,
                highlightthickness=1,
                bd=0,
            )
            item.pack(fill="x", padx=20, pady=(16, 0))

            tk.Label(
                item,
                text=subscription.name,
                font=("Segoe UI", 16, "bold"),
                fg=self.controller.dark_pink,
                bg="#FFF9FB",
            ).pack(anchor="w", padx=16, pady=(14, 4))

            tk.Label(
                item,
                text=(
                    f"Monthly Cost: Rs. {subscription.cost:.2f}\n"
                    f"Renewal Date: {subscription.renewal_date}\n"
                    f"Last Used: {subscription.last_used}"
                ),
                font=("Segoe UI", 12),
                fg=self.controller.text_color,
                bg="#FFF9FB",
                justify="left",
            ).pack(anchor="w", padx=16, pady=(0, 14))

        self.canvas.yview_moveto(0)

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
