# modbus notes
here's a bunch of random notes i'm taking on how modbus and the click plus plc work together...

## address mapping

### X Addresses
- Read only
- Data Type: Bit

click | modbus
-- | --
001-016 | `100001`-`100016`
021-036 | `100017`-`100032`
101-116 | `100033`-`100048`
201-216 | `100065`-`100080`
301-316 | `100097`-`100112`
401-416 | `100129`-`100114`
501-516 | `100161`-`100176`
601-616 | `100193`-`100208`
701-716 | `100225`-`100240`
801-816 | `100257`-`100272`

### Y Addresses
- Read AND Write
- Data Type: Bit

click | modbus 
-- | --
001-016 | `8193`-`8208`
021-036 | `8209`-`8224`
101-116 | `8225`-`8240`
201-216 | `8257`-`8272`
301-316 | `8289`-`8304`
401-416 | `8321`-`8336`
501-516 | `8353`-`8368`
601-616 | `8385`-`8400`
701-716 | `8417`-`8432`
801-816 | `8449`-`8464`

### C Addresses
- Read AND Write
- Data Type: Bit

These are easy.
click | modbus
-- | --
1-2000 | `16385`-`18384`

### T Addresses
- Read Only
- Data Type: Bit

Also easy...
click | modbus 
-- | --
1-500 | `145057`-`145556`

### CT Addresses
- Read Only
- Data Type: Bit

click | modbus
-- | --
1-250 | `149153`-`149402`

### SC Addresses
- MIXED (some are writable)
- Data Type: Bit

click | modbus | R/W
-- | -- | --
1-49 | `161441`-`161489` | R
50-51 | `061490`-`061491` | RW
52 | `161492` | R
53 | `061493` | RW
54 | `161494` | R
55 | `061495` | RW
56-59 | `161496`-`161499` | R
60-61 | `061500`-`061501` | RW
62-64 | `161502`-`161504` | R
65-67 | `061505`-`061507` | RW
68-74 | `161508`-`161514` | R
75-76 | `061515`-`061516` | RW
77-119 | `161517`-`161559` | R
120-121 | `061560`-`061561` | RW
122-302 | `161562`-`161742` | R
303-306 | `061743`-`061746` | RW
307-322 | `161747`-`161762` | R
323-326 | `061763`-`061766` | RW
327-1000 | `161767`-`162440` | R

### DS Addresses
- Read AND Write
- Data Type: Int

click | modbus
-|-
1-4500 | `400001`-`404500`

### DD Addresses
- Read AND Write
- Data Type: Int2 (2 words)

click | modbus
-|-
1-1000 | `416385`-`418383` (odds only) (because it's 2 words each) (duh)

### DH Addresses
- Read AND Write
- Data Type: Hex

click | modbus
-|-
1-500 | `424577`-`425076`

### DF Addresses
- Read AND Write
- Data Type: Float

click | modbus
-|-
1-500 | `428673`-`429671` (odds only)
