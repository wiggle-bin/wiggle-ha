from homeassistant.components.http import HomeAssistantView
from datetime import datetime
import os


class WiggleBinUploadView(HomeAssistantView):
    url = "/api/wiggle/upload"
    name = "api:wiggle_upload"
    requires_auth = False  # Set to True if you want to secure it

    async def post(self, request):
        data = await request.read()

        if not data:
            return self.json({"error": "No data received"}, status_code=400)

        try:
            now = datetime.now()
            date_str = now.strftime("%Y_%m_%d")
            time_str = now.strftime("%H_%M_%S")

            # Folder path: /media/wigglebin/YYYY_MM_DD
            media_dir = os.path.join("/media", "wigglebin", date_str)
            os.makedirs(media_dir, exist_ok=True)

            # Filename: YYYY_MM_DD_HH_MM_SS.jpg
            filename = f"{date_str}_{time_str}.jpg"
            media_path = os.path.join(media_dir, filename)

            # Save image
            with open(media_path, "wb") as file_out:
                file_out.write(data)

            return self.json(
                {
                    "status": "ok",
                    "folder": f"wigglebin/{date_str}",
                    "filename": filename,
                }
            )

        except Exception as e:
            return self.json({"error": str(e)}, status_code=500)
