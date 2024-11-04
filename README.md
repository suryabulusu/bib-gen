# bib-gen
(Approximately) fetches dblp bibtex from paper titles and saves to a csv. 

Code is largely repurposed from Xeophon's repo: https://github.com/Xeophon/espanso-bib-generator

I edited it to suit my use-case. I had to fetch bibtex for 100+ titles for this [post](https://suryabulusu.github.io/posts/taste/).

### Issues
- Loop usually breaks because dblp has rate limits. I ran the code 4 times for 100+ titles.
- Doesn't fetch meaningful entries for non-CS titles.
- Sometimes, top3 or top5 entries do not correspond to the title. Example: Latent Dirirchlet ALlocation. There are so many papers with these words in the title in just 2024. No way we'd have reached 2001 in merely 5 hits. I manually copied bib entry for LDA and other old/famous papers.


