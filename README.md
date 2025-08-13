# qpbeaver

## Dependencies

- [qpdf](https://github.com/qpdf/qpdf)
- [typst](https://github.com/typst/typst)

For Ubuntu-based systems:

```bash
sudo apt-get install qpdf
sudo snap install typst
```

## split

```bash
python main.py split --source input.pdf --pages-data pages.csv --out-dir data/pdfs/
```
where

- `--source`, `-s` is the PDF to process
- `--pages-data`, `-p` is a comma-separated file that has (name, pages) in each row
- The resulting parts will be created in `--out-dir`, `-o`, or by default, `data/pdfs/` in this directory.


Example of `pages.csv`:
```csv
front,1-5
AQ,6-10
```

Which will create `data/pdfs/front.pdf` and `data/pdfs/AQ.pdf`.

The page parts are directly passed to qpdf, where

- `<n>`: Single page number (e.g., `5`)
- `<a>-<b>`: Page range (e.g., `1-10`)
- `<a>,<b>,<c>`: Comma-separated pages (e.g., `2,4,6`)

... are supported (not rejected).

## build

```bash
python main.py build --source-dir data/pdf/ --build-directive build.csv --out build/output.pdf
```

- `--source-dir`, `-s` contains the PDFs to look for (subdirectories are also searched). Use the directory specified in `--out-dir` in the split command above. Defaults to `data/pdfs/` in this directory.
- `--build-directive`, `-b` is a CSV file where parts to join are listed.
- `--out`, `-o` is the output. If not specified, a new file with a random name will be created under the `build/` directory here.
- If `--no-append-checklist`, `--nc` is given, the checklist will not be appended in the back of the resulting pdf.

`build.csv` should include one part (stem name of the PDF) per line, optionally followed by a comma and a name to use in the checklist that will be automatically appended to the PDF:

```csv
front
AQ
questionnaire_two,AnotherName
```
