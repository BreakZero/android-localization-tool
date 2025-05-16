# 🌍 Multilingual Translation Manager with Google Sheets + CSV/XML

This repository offers a lightweight and collaborative solution for managing multilingual translations. It integrates **Google Sheets** for real-time preview and editing, and includes Python scripts to convert between **CSV files and Android `strings.xml`** format.

## ✨ Features

- 🔁 **Bidirectional conversion**: Convert between CSV and Android `strings.xml`
- 🌐 **Google Sheets integration**: Manage and preview translations collaboratively online
- ➕ **Add languages easily**: Simply add new columns in the CSV to support additional languages
- 📤 **Multi-language export/import**: Simplify localization across different markets

---

## Usage
### xml to csv

```sh
python3 batch_convert_xml2csv.py xml output/csv
```

### csv to xml

```sh
python3 csv2xml.py csv/example.csv output/xml/
```
