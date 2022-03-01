# The library
ARINC429 is python library designed to translate [ARINC 429](https://en.wikipedia.org/wiki/ARINC_429) words.
If provided with an ICD it can also parse incoming data.
ARINC429 is 100% Python with zero to none external dependencies.
# Quick guide to ARINC429 library and protocol
## Physical layout of Arinc 429 lines
The ARINC 429 protocol is widely used on board of helicopters and airplanes to transport data from one source to up to 20 destinations. Data travels as 32 bit packets along a single wire.
<pre><code>
+-----+     +-----+     +-----+     +-----+     +-----+
|dest1|     |dest2|     |dest3|     |dest4|     |dest5|
|     |     |     |     |     |     |     |     |     |
+-----+     +-----+     +-----+     +-----+     +-----+
   |           |           |           |           |
   ^           ^           ^           ^           ^
   |           |           |           |           |
   +-----<-----+----<------+----->-----+----->-----+
                           |
                           ^
                           |
                        +-----+
                        |     |
                        | src |
                        +-----+
</code></pre>
## Arinc 429 data frame
<pre><code>
|32|31|30|29|28|27|26|25|24|23|22|21|20|19|18|17|16|15|14|13|12|11|10| 9| 8| 7| 6| 5| 4| 3| 2| 1|
|PB| SSM |MSB                         Payload                  LSB| SDI |LSB      Label      MSB|
</code></pre>

An Arinc 429 Frame is made up of 32 bit, the rightmost bit being number 1 and the leftmost being number 32.<br>
- bit **32** is the parity bit. The majority of ARINC 429 applications enforce odd-parity
- bits **31-30** are the Status Signal Matrix (SSM) used to give indication about the status of transmitted data.
    - 00 for **Failure Warning**
    - 01 for **Functional Test**
    - 10 for **Not Computed Data**
    - 11 for **Normal Operation**
- bits **29-11** are the payload. payload can be tailored to user needs. Currently, supported data format are:
   - BNR for binary coded numbers (INT, UINT, FLOAT)
   - ENUM for enumerated types, stored as UINT
- bits **10-9** carry the Source Destination Identifier (SDI). It can be used to identify the intended recipent for the message or it can extend the payload by being appended to it. Labels using the SDI to carry an increased payload are called "Extended labels"
- bits **8-1** are the label bits. The label identifies the nature of the payload according to source device manufacturer. Labels are reported in octal format and **reversed**: bit 8 is the LSB for the label.

## ICD file
To translate the bits of an A429 frame to useful engineering values an ICD file is needed.<br>
An ICD file consists in a csv file, separated by semicolons. The columns must be arranged in the following order
   - Field Name: carries the name of the data being descripted
   - Channel: Defines from which channel the frame is intended to be received. The same label could have different meaning depending on which device is sending it
   - Label: the label carrying the data being described
   - Encoding: Describes how the data is encoded in the payload. possible values are: 
      - BNR
      - ENUM 
   - MSB: defines from which bit of the frame (starting from number 32 on the left) the data begins
   - LSB: defines at which bit of the frame (starting from number 32 on the left) the data ends
   - Field type: defines how the payload must be interpreted. Current version offers following types:
      - for BNR: integrer (INT), unsigned integer (UINT), floating point (FLOAT)
      - for ENUM: this field holds the literal values for the enumerator starting from zero and separated by comma
   - RESOLUTION: this fields hold the resolution for FLOAT data (see specific chapter)
   - SDI: specifies the SDi for this particular data. If SDI = XX, the SDI bits will be attached to the payload (Extended label)