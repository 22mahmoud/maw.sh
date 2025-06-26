import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # Optional: only if you're not using proper CSRF tokens
def fetch_leetcode_data(request):
    slug = request.GET.get("slug")
    if not slug:
        return JsonResponse({"error": "Missing slug"}, status=400)

    graphql_query = {
        "query": f"""
        {{
          question(titleSlug: "{slug}") {{
            content
            questionFrontendId
            title
            titleSlug
            difficulty
            codeSnippets {{
              langSlug
              code
            }}
          }}
        }}
        """
    }

    try:
        res = requests.post(
            "https://leetcode.com/graphql/",
            json=graphql_query,
            headers={"Content-Type": "application/json"},
        )
        data = res.json().get("data", {}).get("question")
        if not data:
            return JsonResponse({"error": "Problem not found"}, status=404)

        ts_code = next(
            (c["code"] for c in data["codeSnippets"] if c["langSlug"] == "typescript"),
            "",
        )

        return JsonResponse(
            {
                "title": data["title"],
                "title_slug": data["titleSlug"],
                "id": data["questionFrontendId"],
                "difficulty": data["difficulty"].lower(),
                "content": data["content"],
                "code_ts": ts_code,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
