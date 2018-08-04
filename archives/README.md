# archives
This section contains deprecated stuff.

## PHP Web App
The first public website of CryptoPredicted was primarily a platform with charts for analysis.

![](https://i.imgur.com/RD1vmmE.png)

The back-end architecture was not ideal, which why this project became deprecated. Initially it was developed in an unorthodox manner using Python + PHP + jQuery. The API code (found in ui/ dir) executes python scripts (found in presenters/ dir) as a "sort of" internal API.
This became a bottleneck with terrible performance, so it was partially reworked to use native PHP, and later it solely used NodeJS API for data access.

If you wish to reconstruct this web app, you'll need PHPv7 and it will work out of the box. However, it is possible that some features (like the 3D charts) still use the bad Python-based API scripts.

It's highly recommended not to use the scripts in presenters/ directory in any release for performance reasons, unless you use them for R&D.
