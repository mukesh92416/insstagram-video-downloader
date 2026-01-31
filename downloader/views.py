from django.shortcuts import render
import instaloader

L = instaloader.Instaloader()

def home(request):
    return render(request, "downloader/home.html")

def downloader(request):
    media_url = None
    message = None

    if request.method == "POST":
        url = request.POST.get("url")

        try:
            shortcode = url.strip("/").split("/")[-1]
            post = instaloader.Post.from_shortcode(
                L.context, shortcode
            )

            if post.is_video:
                media_url = post.video_url
            else:
                media_url = post.url

        except Exception:
            message = "Invalid or private post."

    return render(request, "downloader/downloader.html", {
        "media_url": media_url,
        "message": message
    })
