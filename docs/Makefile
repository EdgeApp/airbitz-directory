
build:
	Rscript -e "library(knitr); knit('curl_examples.Rmd'); "
	sed -i 's/| .\/split_curl.py//g' curl_examples.md
	Rscript -e "library(knitr); pandoc('curl_examples.md', format='html', config='config.pandoc')"

clean:
	rm *.md

