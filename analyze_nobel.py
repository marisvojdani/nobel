import csv
import re


# Create a list of laureates
laureates = []
with open('nobel_latest.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Category'] == 'literature':
            laureates.append(row['Firstname'] + ' ' + row['Lastname'])

print(laureates)

# Create a list of books written by laureates
nobel_books = []
with open('books.csv') as file :
     books = csv.DictReader(file)
     for i in books :
        for j in laureates:
            #cut off everything after first / in authors
            i['authors'] = i['authors'].split('/')[0]
            if re.match('.*\\b' + j + '\\b.*', i['authors']) :
                nobel_books.append(i)


# COMPUTING AVERAGE RATINGS & BEST BOOKS
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

# Find book with maximum rating
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

# add a negative value for each laureate that has no books in the dataset
for laureate in laureates:
    if laureate not in authors_avg:
        authors_avg[laureate] = -1
        best_book[laureate] = (-1, "No book in dataset")

# sort the authors by average rating
authors = {k: v for k, v in sorted(authors_avg.items(), key=lambda item: item[1], reverse=True)}

#output authors to csv file
with open('results_nobel.csv', 'w', newline='') as csvfile:
    fieldnames = ['author', 'average_rating', 'best_book', 'best_book_rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    # write the laureates to the csv file
    for author in authors:
        writer.writerow({'author': author, 'average_rating': round(authors[author],2), 'best_book': best_book[author][1], 'best_book_rating': best_book[author][0]})