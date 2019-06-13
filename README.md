
#![picturealt](canary.png "Canary Logo") Canary Summary
canary is a command line tool to scrape html elements, test availability of links and images, and build an easy to read report

##` WARNING!:`
`Be careful about the number of urls being verified / scraped.`
`Frequent Use may be viewed by Web Application Firewalls / IDPS systems as a DoS Attack` 

`Do Not use this tool on any websites without the owner's permission.`
`Symbiotech LLC is not liable / responsible for how this tool is used.`


# Canary Commands: #
### List all available options (help) ###
canary.exe `-h`

### Output in excel format ###
canary.exe `--excel`


### Define Urls to test: ###
canary.exe `-u "http://www.google.com" -u "https://www.yahoo.com"`


### Test with a .txt containing a list of urls: ###
canary.exe `-f "filepath.txt"`


### Prepend domain to paths: ###
canary.exe `-f "filepath.txt" -base "https://www.mydomain.com"`

    filepath.txt:
      1. /home.html
      2. /sitemap.html

    would test:
      1. https://www.mydomain.com/home.html
      2. https://www.mydomain.com/sitemap.html


### Scrape webpage and build report: ###
Report will contain the following: 

*  anchor links `<a>`
*  images `<img>`
*  forms / input fields (`<button>, <input>, etc..`)



canary.exe -u "https://www.google.com" `-scrape`


### Scrape webpage, Verify images / links, and build report:
Report will contain:

* all anchor links `<a>`, status code, status code message, and page title
* images `<img>`,status code, status code message, and page title
* forms / input fields

canary.exe -u "https://www.google.com" `-verify`

### Request using basic authentication: 
You will be prompted for password. This is to help maintain security and hide password from cmdline history. 

`Warning:` You may still be able to see password sent in clear text if capturing network packets or monitoring the network 

canary.exe -u "https://www.google.com" -verify `-webuser "grimm"` 

### Limit requests to only url's in the specified domain: 
It is sometimes common to see links to facebook, twitter, and other sites when scraping. This will limit the results to
what you care about. 

canary.exe -u "https://www.mydomain.com" -verify `--limit "https://www.mydomain.com"` 

### Exclude specified domains when testing: 
Exclude urls that have the specified domain 

canary.exe -u "https://www.google.com" -verify `--exclude "https://www.facebook.com"` 



#### Output is saved in the current directory of the script / executable under a Results directory
