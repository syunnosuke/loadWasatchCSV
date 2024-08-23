# loadWasatchCSV
Load CSV file of Wasatch Photonics Raman spectrometer, and extract single spectrum data

python version: 3.7
library requirement: Pandas

Procedure
1. Place load.py at suitable directory
2. create sub-directory named data
3. place the CSV file in data directory
4. Run load.py as follows: python load.py (name of CSV file).csv
5. Add options if necessary (-od: omit extracting dark reference spectra, -or: omit extracting raw spectra)
6. Extracted spectra are stored in the directory of the same name as CSV file
