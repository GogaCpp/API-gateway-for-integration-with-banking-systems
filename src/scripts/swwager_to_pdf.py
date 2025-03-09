import requests
from weasyprint import HTML


def save_swwager():

    try:
        html_path = "src/temp/FastAPI - Swagger UI.html"
        save_path = "src/temp/docs.pdf"

        HTML(filename=html_path).write_pdf(save_path)

    except requests.RequestException as e:
        print(e)


if __name__ == "__main__":
    save_swwager()
