# Sus-o-meter
Detecting sussy links in a user's search history

Sus-o-meter works by reading the browser history of all installed browsers. Then, it checks if any links match the primary-dataset. Finally, it attempts to load each of the pages detected and compares the page title to the data in the secondary-dataset.

## Why?
Idk, it sounded funny in my head.

# Usage
Clone the repository:
```bash
git clone https://github.com/Sidpatchy/Sus-o-meter/
cd Sus-o-meter/
```

Install the required dependencies:
```bash
pip install tqdm beautifulsoup4 browser_history
```

Run sus-o-meter.py:
```bash
python sus-o-meter.py
```
