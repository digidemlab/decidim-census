# Decidim Census

Decidim Census is a project aiming to gather key figures and statistics about instances of the Decidim platform.

It's making use of the open GraphQL API that all Decidim platforms have to fetch information periodically.

Right now, the project only consists of a script to fetch the data. That script is run once a day using Github Actions and saving the output on the repository.

In the future, a frontend could be built. In the meantime, I recommend to use [flatgithub.com](https://flatgithub.com/digidemlab/decidim-census?filename=organizations.csv).
