# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

