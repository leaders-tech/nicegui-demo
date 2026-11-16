"""Show the shared counter page and its small HTTP API. Edit the page and routes here."""

import os

from nicegui import app, binding, ui

import db


class Counter:
    # Every label bound to `value` changes when it changes, in every open tab.
    value = binding.BindableProperty()

    def __init__(self):
        self.value = 0


counter = Counter()


def load_counter() -> None:
    db.initialize()
    counter.value = db.read()


def add_one() -> int:
    # The button and the API both call this. SQLite stays the source of truth.
    counter.value = db.increment()
    return counter.value


app.on_startup(load_counter)


@ui.page("/")
def counter_page():
    with ui.column().classes("w-full max-w-md mx-auto p-8 gap-4"):
        ui.label("NiceGUI counter").classes("text-3xl font-bold")
        ui.label("One shared counter, saved in SQLite.")
        # The click reaches this Python process over NiceGUI's WebSocket.
        # No HTTP request is needed: the handler calls the database code directly.
        ui.button("Add 1", on_click=add_one)
        ui.label().classes("text-2xl").bind_text_from(
            counter, "value", backward=lambda value: f"Count: {value}"
        )


# NiceGUI's `app` is a FastAPI app, so HTTP routes live in the same process.
# They are only for other programs (curl, scripts); the page does not use them.
# `async def` keeps them on the same thread as the page.
@app.get("/api/health")
async def health() -> dict[str, str]:
    db.read()  # Report healthy only if the database can also be read.
    return {"status": "ok"}


@app.get("/api/counter")
async def read_counter() -> dict[str, int]:
    return {"value": db.read()}


@app.post("/api/counter/increment")
async def increment_counter() -> dict[str, int]:
    return {"value": add_one()}


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")),
           title="NiceGUI counter", reload=False, show=False,
           fastapi_docs=True)  # Interactive API documentation at /docs.
