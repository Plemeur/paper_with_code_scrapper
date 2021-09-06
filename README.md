## Project description

Using web scrapping libraries such as Selenium and BeautifulSoup, the goal is to be able to create a dataset of abstract from `Papers with code`.

Each data point would be `[abstract, tasks]`, and using NLP I make a multiclass classification model to be able to get relevant tasks in new arXiv publication.

I would then store them in a database, probably object database because I do not know the number of applicable tasks.

I could then either link that to the Notion API to get an updated list everyday, and get an easy way of sorting the items. Or I could make kind of a reader app for android, where I could make a more automated tracking of my readings, and an easy download system.

## TODO's

- [ ] Function to get the papers abstract
- [ ] Function to store the abstract
- [ ] Machine learning model for documents clustering
  - [ ] Training part
  - [ ] Inference part
- [ ] Time function to get current
