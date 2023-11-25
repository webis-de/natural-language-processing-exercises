I took a random sample of 1000 clueweb09 and 1000 clueweb12 documents.

From the [official spam rank documentation](https://plg.uwaterloo.ca/~gvcormac/clueweb09spam/):

The percentile score indicates the percentage of the documents in the corpus that are "spammier." That is, the spammiest 1% of the documents have percentile-score=0, the next spammiest have percentile-score=1, and so on. The least spammy 1% have percentile-score=99. 

If you just want the best of the four sets of scores, choose Fusion. If you just want to label pages as spam or not, label those with percentile-score<70 to be spam, and the rest non-spam. For more details, read the paper

Run it via: 

./step-02-create-dataset.py -i cw09-spam-ranks -o cw-09 --dataset-id clueweb09

./step-02-create-dataset.py -i cw12-spam-ranks -o cw-12 --dataset-id clueweb12
