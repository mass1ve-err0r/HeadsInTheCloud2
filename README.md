# HeadsInTheCloud 2
> Python 3.6+ | Fast | Any SDK

## Prelude
Limneos' provides a wonderful service which basically lets you browse headers online from various SDKs.The only gripe I take with his site is the slight drawbacks with speed, that's how I came to make HeadsInTheCloud - short _HITC_.

If you've seen V1 ([Repository](https://github.com/mass1ve-err0r/HeadsInTheCloud), [Announcement tweet](https://twitter.com/saadat603/status/1271274140939534337?s=21)), this is the official successor to it and a complete rewrite!

This takes a radically different approach to how headers are _"generated"_, see below.

## Internals
_HITC v1_ was based on Flask and rendered each header dynamically.

_HITC v2_ is based on sanic and takes a different approach to rendering headers: It doesn't.

The headers are pre-generated with -in this case- the included `converter.py` which has HTML wraps specific to my personal setting _(you can change that though)_ and uses `pygments` to generate HTML from a header file.

sidenotes:
- the generated html from the header gets _"pasted"_  between the html wraps to build a full page
- stylization is handled through the explicit `header_view.css`, you can mix&match values there to generate your own individual style!
- the header files are _(in best case)_ served through nginx to spare the backend of doing the lengthy work of sending the rendered header. This is the secret to the speediness!

## Requirements + Setup
If you wish to deploy your own instance, here's the steps to deploy it with sanic serving the files instead of Nginx:
- Linux VPS
	- Python 3.6+, python3-venv
- yup, that's it.

The static directory is `/static`, place your generated headers' in their respective SDK there. The layout for an SDK has changed since _HITC v1_ since we no longer need the actual files but prerendered HTMLs, here's an overview for these:
- SDK _\<Version\>_
	- Frameworks
		- _all `.framework` folder (private and public)_
			- _\<header_name\>.html_
		- _all `.dylib` folder (if any at all)_
			- _\<header_name\>.html_
	- protocols
		- _\<header_name\>.html_

Since sanic provides it's own webserver which is solid enough, you can of course opt to use somethin like gunicorn et al.

If everything is setup, just fire sanic up!

If you'd like to have this managed by PM2, here's a quick recap on how to make it use the appropriate venv:
- `pm2 <location/to/server.py> --interpreter <location/to/its/venv/bin/python>`

## Credits
- Limneos for the original idea
- SparkDev for the iOS 14.0 SDK dump
- EzioChiu for the iOS 12.1.2 SDK dump
- Local Pigeons for supporting me by just being fluffy companions lmao

## License
This Project is licensed under the **AGPL v3**.
