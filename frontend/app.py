"""Show the NiceGUI counter. Edit the page here; copy for another API-driven page."""

import os

import httpx
from nicegui import ui

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8081")


@ui.page("/")
def counter_page():
    with ui.column().classes("w-full max-w-md mx-auto p-8 gap-4"):
        ui.label("NiceGUI counter").classes("text-3xl font-bold")
        ui.label("One shared counter, saved in SQLite.")

        async def update_counter(increase: bool = False):
            button.disable()
            try:
                # The browser event reaches Python over NiceGUI's WebSocket.
                # Python then makes a real HTTP request to the separate API.
                async with httpx.AsyncClient(timeout=5) as client:
                    if increase:
                        response = await client.post(f"{API_URL}/api/counter/increment")
                    else:
                        response = await client.get(f"{API_URL}/api/counter")
                    response.raise_for_status()
                count.set_text(f"Count: {response.json()['value']}")
                status.set_text("")
            except httpx.HTTPError:
                status.set_text("Cannot reach the API. Please try again.")
            finally:
                button.enable()

        button = ui.button("Add 1", on_click=lambda: update_counter(increase=True))
        count = ui.label("Loading counter...").classes("text-2xl")
        status = ui.label("").props('role="alert"')
        # Load after the page is built so an unavailable API cannot block the page.
        ui.timer(0.1, update_counter, once=True)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), title="NiceGUI counter", reload=False, show=False)
