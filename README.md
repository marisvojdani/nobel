# The Nobel Prize Winners with Highest Goodreads Rating

The goal of this project was to find average book ratings for the Nobel literature winners. In order to do that two datasets were obtained from Kaggle. First one contained data about all Nobel prize winners: [nobelfoundation/nobel-laureates](https://www.kaggle.com/nobelfoundation/nobel-laureates). The dataset that contained data about 1000 people was filtered to only include the 119 literature winners:

```python
laureates = []
with open('nobel_latest.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Category'] == 'literature':
            laureates.append(row['Firstname'] + ' ' + row['Lastname'])
```

The books and the ratings were taken from another Kaggle dataset: [jealousleopard/goodreadsbooks](https://www.kaggle.com/jealousleopard/goodreadsbooks). This dataset contained data of about 11 000 books scraped from Goodreads. Goodreads is a website where users can rate and review books. The dataset was filtered to only include the books of the literature winners:

```python
nobel_books = []
with open('books.csv') as file :
     books = csv.DictReader(file)
     for i in books :
        for j in laureates:
            #cut off everything after first / in authors
            i['authors'] = i['authors'].split('/')[0]
            if re.match('.*\\b' + j + '\\b.*', i['authors']) :
                nobel_books.append(i)
```

## Computing the average ratings

Then the average ratings were calculated for each literature winner. First a dictionary was created with the author as key and a list of ratings as value. Then the average rating was computed for each author.

```python
authors_avg = {}
# Create a dict with the author as key and a list of ratings as value
for book in nobel_books:
    author = book['authors']
    rating = float(book['average_rating'])
    if author in authors_avg:
        authors_avg[author].append(rating)
    else:
        authors_avg[author] = [rating]
# Compute the average rating for each author
for author in authors_avg:
    ratings = authors_avg[author]
    avg_rating = sum(ratings) / len(ratings)
    authors_avg[author] = avg_rating
```

## Computing the Best Book of each author

In order to find the best book of each author, we first create a dictionary with the author as key and a tuple of the highest rating and the title of the book as value. Then, we iterate through the Nobel Prize winners and find the best book of each author.

```python
best_book = {}
for author in authors_avg:
    max_rating = 0
    max_book = ""
    for book in nobel_books:
        if book['authors'] == author:
            rating = float(book['average_rating'])
            if rating > max_rating:
                max_rating = rating
                max_book = book['title']
    best_book[author] = (max_rating, max_book)
```

## Results

The results were written into a CSV file [results_nobel.csv](results_nobel.csv). The top 12 authors with the highest average ratings and their best books were:

| Author | Average Rating | Best Book | Rating of Best Book |
| --- | --- | --- | --- |
| Pablo Neruda | 4.34 | The Essential Neruda: Selected Poems | 4.46 |
| Octavio Paz | 4.22 | The Collected Poems 1957-1987 | 4.30 |
| Isaac Bashevis Singer | 4.20 | Collected Stories III: One Night in Brazil to The Death of Methuselah | 4.61 |
| Sigrid Undset | 4.17 | The Son Avenger (The Master of Hestviken #4) | 4.40 |
| Eugene O'Neill | 4.11 | Complete Plays 1920–1931 | 4.18 |
| Seamus Heaney | 4.10 | New Selected Poems 1966-1987 | 4.19 |
| Thomas Mann | 4.08 | Doctor Faustus | 4.08 |
| Samuel Beckett | 4.05 | Molloy; Malone Dies; The Unnamable (The Trilogy #1-3) | 4.28 |
| T.S. Eliot | 4.05 | The Waste Land and Other Writings | 4.21 |
| Bob Dylan | 4.04 | The Essential Interviews | 4.11 |
| Boris Pasternak | 4.04 | Letters: Summer 1926 | 4.26 |
| Albert Camus | 4.04 | The Plague, The Fall, Exile and the Kingdom, and Selected Essays | 4.34 |

