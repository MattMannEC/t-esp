import fitz
import re
import json

def read_pdf_with_pymupdf(filepath):
    text = ""
    pdf_document = fitz.open(filepath)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text() + "\n"
    pdf_document.close()
    return text

def parse_constitution(text):
    constitution_json = []
    title_id = 0

    sections = re.split(r"(Titre .*?:)", text)

    for i in range(1, len(sections), 2):
        title_raw = sections[i].strip()
        content = sections[i + 1].strip()

        aperçu_match = re.search(r":\s*(.+)", title_raw)
        aperçu = aperçu_match.group(1).strip() if aperçu_match else ""

        title = title_raw.replace(":", "").strip()

        articles = []
        article_id = 0
        matches = re.split(r"(Article \d+[-\dA-Za-z]*)\n", content)

        for j in range(1, len(matches), 2):
            article_title = matches[j].strip()
            article_text = matches[j + 1].strip()

            articles.append({
                "id": article_id,
                "title": article_title,
                "text": article_text
            })
            article_id += 1

        constitution_json.append({
            "id": title_id,
            "title": title,
            "aperçu": aperçu,
            "articles": articles
        })
        title_id += 1

    return constitution_json
def save_to_json(data, output_filepath):
    with open(output_filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def main():
    input_file = "../constitution-1958.pdf"
    output_file = "../chatbot/src/assets/data/constitution.json"

    raw_text = read_pdf_with_pymupdf(input_file)
    parsed_data = parse_constitution(raw_text)

    save_to_json(parsed_data, output_file)
    print(f"Fichier JSON enregistré : {output_file}")

if __name__ == "__main__":
    main()
