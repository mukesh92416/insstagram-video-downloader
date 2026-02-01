from django.shortcuts import render
import instaloader
import urllib.parse
import requests
def clean_instagram_url(url):
    # Handle l.instagram.com redirect links
    if "l.instagram.com" in url:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        if "u" in query:
            url = urllib.parse.unquote(query["u"][0])

    # Remove tracking parameters
    url = url.split("?")[0]

    return url


L = instaloader.Instaloader()

def home(request):
    return render(request, "downloader/home.html")

def downloader(request):
    media_url = None
    message = None

    if request.method == "POST":
        raw_url = request.POST.get("url")
        url = clean_instagram_url(raw_url)


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
