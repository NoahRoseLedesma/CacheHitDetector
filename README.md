# CacheHitDetector
Tool for determining the sequence of cache hits/misses for ECS154 final.

Requires Python 3

Installation:
* Clone this repo or download as a zip
* If required, make "Detector.py" executable with `chmod +x Detector.py`


How To Use:
* Run Detector.py with the test file to analyze `./Detector.py test/final_test.txt`
* For detailed information add the flag `--verbose=true`
  * e.g. `./Detector.py --verbose=true test/final_test.txt`
* The verbose output can be very long, consider using output redirection to put the result in a file
  * e.g. `./Detector.py --verbose=true test/final_test.txt > Detected.txt`

Example output:

```
Input 12 Write Set: 1 Tag: 4 Offset: 1 Value: 0b1011 Miss
Evict line 1
	Line 0 Tag 7 Age 2
	Line 1 Tag 4 Age 0
	Line 2 Tag 3 Age 1
```

This means that test case #12 is a write operation on set '1' to tag 4 offset 1. 
The value being written is the binary value '1011' and the write is a cache miss.
Line '1' of set '1' is being overwritten for this write.
After the write, the ages and tags of the three lines in set '1' are displayed.

Important notes: 
* Lines are numbered [0,2] and sets are numbered [0,1].
* It is assumed that lines are validated in the order 0, 1, 2.
