

Anything you can get to using your browser, you can find using Python (or virtually any other programming language).

The first important thing to know about retrieving things from the web is that
it is really not that different from obtaining data from any other source.

The biggest difference is that getting data over the Internet is a lot slower than accessing local resources on your computer.
Still, it is easily possible to retrieve hundreds of things per second over the Internet.


There are, broadly speaking, two categories of things we would want to do over the internet:
* Obtaining data - text, images, files, structured data, etc.
* Submitting data - e.g. submitting a form, uploading a file, or otherwise requesting the server to do something.

Examples of obtaining data could be:
* Getting a Wikipedia page, eithr as html, or the raw wiki-markup text.
* Downloading an image or other file.
* Getting a section of a map from Google Maps.
* Getting structured information, e.g. currency exchange rate, or information about where the buses are.

Examples of submitting data:
* Posting an updated version of a Wikipedia page.
* Uploading a file to Wikipedia.
* Asking Wikipedia to move/rename a particular page.
* Creating a new Wikipedia user.


Examples - official web APIs:
* Currency exchange rate, stocks,
* Maps
* Wikipedia (encyclopedia)
* Github stats.
* Real-time travel info
* Auth: API-keys, oAuth, or cookie injection.


Examples - unofficial web APIs:
* NuPack
* IDT
* NEB



Real-time travel info:
* MBTA: http://realtime.mbta.com/Portal/Home/Documents - OBS: Pooling is limited to 1 requests per 10 seconds!
* Transloc: http://transloc.com/
** Transloc endpoints:
*** Agencies: https://feeds.transloc.com/3/agencies
*** Routes: https://feeds.transloc.com/3/routes?agencies=64  (MASCO: agency=64)
*** Real-time updates: https://feeds.transloc.com/3/vehicle_statuses?agencies=64,52
* Transloc UIs:
** More info: https://masco.transloc.com/info/mobile
** MASCO: https://www.masco.org/lma-shuttles/live-view - Uses transloc API, src="https://masco.transloc.com/embed.js"
* Harvard M2 web-view: https://m.harvard.edu/transit/route?feed=transit-transloc&direction=loop&agency=64&route=4008182
** Note: While the Harvard M2 real-time web-view uses Transloc data,
   the Harvard web-view actually seems to use server-side rendering, and sends html to the client.
   Still, each response is only about 2 kb, one response per second, so actually not too bad in terms of overhead.
   The JavaScript library is `kgo`, `kgoui`, `kgomap`? Maybe this https://www.npmjs.com/package/kgo ? Or this: Wijmo ?
** Harvard M2 API endpoint: https://m.harvard.edu/transit/route.json
* MTA:



Track your ride online with the TransLoc Real-Time Tracking app. See in real-time where all vehicles are.
Choose your map mode:
    https://masco.transloc.com (The live location map) TransLoc Real-Time Tracking
    https://masco.transloc.com/info/mobile (TransLoc Tracking for your mobile phone) Mobile Access
    https://masco.transloc.com/t/ (An accessible Tracking app) Text Version


Refs:
* https://en.wikipedia.org/wiki/Web_API
* https://en.wikipedia.org/wiki/Overview_of_RESTful_API_Description_Languages
* https://en.wikipedia.org/wiki/List_of_open_APIs
* https://www.openapis.org/
* https://github.com/toddmotto/public-apis

