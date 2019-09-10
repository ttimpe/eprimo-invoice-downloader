# Eprimo Invoice Downloader
## Introduction
This script allows customers of the German energy provider eprimo to automatically download their invoices in PDF format.

## Usage
Place a file called config.json containing your login credentials into the same directory as the script as follows:

```json
{
	"username": "USERNAME",
	"password": "PASSWORD",
	"folder": "FOLDER IN WHICH TO SAVE THE INVOICES",
	"chown": {
		"uid": UID_FOR_CHOWN,
		"gid": GID_FOR_CHOWN
	}
}
```

Then the script will automatically read the login credentials from the file and use the python requests module for making the HTTP requests neccessary to download the latest invoice and save it at the specified location

## Caution

This script could break anytime as it is simply scraping the website of the customer support center.

