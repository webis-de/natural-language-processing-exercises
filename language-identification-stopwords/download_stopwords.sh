mkdir -p stopwords && cd stopwords

for lang_code in af az bg cs da de el en es fi fr hr it ko nl no pl ru ur zh; do
    wget -O stopwords-$lang_code.txt https://raw.githubusercontent.com/stopwords-iso/stopwords-$lang_code/master/stopwords-$lang_code.txt
done

wget -O https://github.com/nltk/nltk_data/raw/gh-pages/packages/corpora/stopwords.zip
unzip stopwords.zip
mv stopwords/azerbaijani stopwords-az.txt
rm -rf stopwords stopwords.zip