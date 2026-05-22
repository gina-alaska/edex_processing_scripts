# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
## [Unreleased]
## [1.0.21] - 2020-02-17
- modified nucaps conversion script

## [1.0.20] - 2019-11-06
- updated to include changes to scmiMosaic.py scripts

## [1.0.19] - 2019-08-30
- updated to add the new SCMI mosaic creation tool and startup shell script

#### [1.0.18] - 2019-06-11
- minor changes to script processing ldm data

## [1.0.17] - 2019-06-25
- minor tweaks to processing scripts

## [1.0.16] - 2019-02-22
- update for new GOES and Test LDM processing scripts along with other minor tweaks

## [1.0.15] - 2019-06-11
- changes to ldm scripts

## [1.0.14] = 2019-2-22
- update for new GOES and Test LDM processing scripts along with other minor tweska

## [1.0.12] - 2018-10-04
- update to NRT retreval script (getGINAsat.py) for CLAVR-X and to add file string matching

## [1.0.11] - 2018-08-03
- minor error checking for LDM processing scripts..particularly for NUCAPS

## [1.0.10] - 2018-06-14
- updated LDM processing script processLDM_SSEC.py to handle MIMIC data
- added LDM processing script for SCMI (Not usually needed)
- added script for viewing LDM queue
- minor additional script updates

## [1.0.9] - 2018-05-18
- added a new LDM processing script for NUCAPS soundings
- added nucaps4awips.py script to modify NUCAPS files for AWIPS 
- modified existing LDM processing scripts for catching file move failures

## [1.0.8] - 2018-04-05
- updated getGINAsat.py so that it does not stop for download failure
## [1.0.7] - 2018-02-15
- changed makeMosaic.py compositing time length
- remove obsolete scripts still looking for data on hippy
- added pixel count utility for SCMI tiles
## [1.0.6] - 2018-01-31
- updated getGINAsat.py AWIPS retrieval/ingest script to include NUCAPS
- added nucaps4awips.py and ncImage.py scripts which are called as modules
  to the retrieval script.
- added chgvtime.py script for changing the valid time of a satellite image. This
  is used to compare different versions of the same image for debugging.
## [1.0.5] - 2018-01-18
- updated AWIPS fetching/ingest script
## [1.0.4] - 2018-01-07
- added missing product to SPoRT LDM script 
## [1.0.3] - 2018-01-04
- fixed type with the SPoRT LDM processing script to changes
## [1.0.2] - 2018-01-04
- modified the SPoRT LDM processing script to change an attribute on some incoming
  netcdf files. Needed to prevent conflicts with a few GINA files.
## [1.0.1] - 2017-10-19
### Added
- add `bin/getSST.sh` and `bin/getSST.py` - scripts to get SST 
- added a CHANGELOG.md file
### Fixed
- `bin/getMIRS.py` - bug fix for MIRS BTs
- `bin/makeMosaic.py` - bug fix for composititing NOAA POES
- `bin/processLDM_SSEC.py` - fix for river script problem
- `bin/makeMosiac.py` - bug fixes for latest version 2 of awips

## [1.0.0] - 2017-06-20
- initial 1.0.0 version to capture what was being done on EDEX

